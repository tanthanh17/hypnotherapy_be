# views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from core_app.serializers import (
    UserSerializer,
    UserProfileSerializer,
    BookingSerializer,
    BookingDashboardSerializer,
    UserBookingSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    PasswordResetChangeSerializer,
    RegistrationSerializer,
    ServiceTypeSerializer
)
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from core_app.models import Booking, ServiceType
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

# Admin User Management View (ModelViewSet)
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admin users can access this
    # Enable filtering and searching
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # Define fields for filtering
    filterset_fields = ['is_active']
    # Define fields for searching
    search_fields = ['full_name', 'phone', 'id']

    def get_queryset(self):
        # Optionally, filter the queryset based on request parameters
        return get_user_model().objects.exclude(id=self.request.user.id)

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [AllowAny]  # Only admin users can access this

    def get_queryset(self):
        # Optionally, filter the queryset based on request parameters
        return ServiceType.objects.all()
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny(),]
        else:
            return [IsAdminUser(),]
    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint

    def get(self, request, *args, **kwargs):
        # Get the current authenticated user
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class RegistrationView(APIView):
    permission_classes = [AllowAny]  # Only authenticated users can access this endpoint

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully.", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin Booking Management View (ModelViewSet)
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]  # Only admin users can access this
    
    # Enable filtering and searching
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # Define fields for filtering
    filterset_fields = ['status', 'payment_status', 'service_type']

    # Define fields for searching
    search_fields = ['client_name', 'phone', 'booking_id']

    def get_queryset(self):
        # Optionally, filter the queryset based on request parameters
        return Booking.objects.all()
    
class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this endpoint

    def get(self, request, *args, **kwargs):
        # Get the bookings for the current authenticated user
        user_bookings = Booking.objects.filter(user=request.user)
        serializer = UserBookingSerializer(user_bookings, many=True)
        return Response(serializer.data)

class BookingAPIViewForUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["email"]
            
            serializer.create_otp(user)  # Generate OTP and send it
            return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetChangeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = PasswordResetChangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardAPIView(APIView):
    permission_classes = [IsAdminUser]  # Ensure the API is accessible only to authenticated users

    def get(self, request, *args, **kwargs):
        # Calculate metrics
        total_users = get_user_model().objects.count()
        total_bookings = Booking.objects.count()
        data_bookings = Booking.objects.all()

        serializer = BookingDashboardSerializer(data_bookings, many=True)
        data = {
            "total_users": total_users,
            "total_bookings": total_bookings,
            "data_bookings": serializer.data
        }
        return Response(data)