from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Try to find the user by email
        user = get_user_model().objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('No user found with this email.')

        # Check if the user is active
        if not user.is_active:
            raise AuthenticationFailed('User account is deactivated.')

        # Check the password
        if not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials.')

        # If user is valid, return the user object for token generation
        return {
            'user': user
        }

    def get_token(self, user):
        # Create and return a refresh token for the user
        refresh = RefreshToken.for_user(user)
        return refresh

# Custom Token Obtain Pair View using email
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the token using the serializer and user data
        user = serializer.validated_data['user']
        refresh = serializer.get_token(user)

        # Return the tokens as a JSON response
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })
