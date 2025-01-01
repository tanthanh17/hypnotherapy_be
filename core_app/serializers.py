# serializers.py
import random
import string
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core_app.models import Booking, PasswordResetOTP, ServiceType
from rest_framework import serializers
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from hypnotherapy import settings

# Serializer for User model (Admin)
class UserSerializer(serializers.ModelSerializer):
    # Password is write-only to ensure it's never exposed in API responses
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'full_name', 'roles', 'is_active', 'is_staff', 'date_joined', 'username', 'phone']
        read_only_fields = ['id', 'date_joined']  # Prevent these fields from being modified

    def create(self, validated_data):
        """
        Override the create method to handle password hashing.
        Admins can provide a plain-text password, which will be hashed
        before storing it in the database.
        """
        email_prefix = validated_data['email'].split('@')[0]
        random_suffix = get_random_string(length=4, allowed_chars='0123456789')
        username = f"{email_prefix}_{random_suffix}"
        
        validated_data['username'] = username
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Override the update method to handle password changes.
        If a new password is provided, it will be hashed before updating the user.
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().update(instance, validated_data)
    
    def validate_email(self, value):
        """
        Ensure the email is unique before creating or updating a user.
        """
        User = get_user_model()
        instance = self.instance
        if instance:
            if User.objects.filter(email=value).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        else:
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("A user with this email already exists.")
        return value

# Serializer for User Profile (Me endpoint)
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'full_name', 'roles', 'date_joined', 'is_superuser']

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['full_name', 'email', 'password']

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        email_prefix = validated_data['email'].split('@')[0]
        random_suffix = get_random_string(length=4, allowed_chars='0123456789')
        username = f"{email_prefix}_{random_suffix}"

        validated_data['username'] = username
        validated_data['password'] = make_password(validated_data['password'])
        return get_user_model().objects.create(**validated_data)
        
# Booking Serializer for Admin
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'client_name', 'service_type', 'booking_id', 'status', 'payment_status', 'phone', 'duration', 'created_at', 'updated_at']
        # Add any other fields you want to expose to the admin

class BookingSerializer(serializers.ModelSerializer):
    service_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'session_datetime', 'start_time', 'end_time', 
            'duration', 'client_name', 'message', 'service_type', 'phone',
            'payment_status', 'status', 'service_type_name'
        ]
        read_only_fields = ['booking_id', 'service_type_name', 'phone']

    def get_service_type_name(self, obj):
        """
        This method retrieves the name of the service type.
        Assuming service_type is a ForeignKey pointing to a model with a 'name' field.
        """
        return obj.service_type.name if obj.service_type else None

    def create(self, validated_data):
        # Create booking ID
        validated_data['booking_id'] = f"APPT-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
        validated_data['payment_status'] = 'unpaid'  # Default
        validated_data['status'] = 'pending'  # Default
        return super().create(validated_data)
    
class BookingDashboardSerializer(serializers.ModelSerializer):
    service_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'booking_id', 'session_datetime', 'start_time', 'end_time', 
            'duration', 'client_name', 'message', 'service_type', 'phone',
            'payment_status', 'status', 'service_type_name'
        ]

    def get_service_type_name(self, obj):
        """
        This method retrieves the name of the service type.
        Assuming service_type is a ForeignKey pointing to a model with a 'name' field.
        """
        return obj.service_type.name if obj.service_type else None

# Booking Serializer for User Profile (Me endpoint)
class UserBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'client_name', 'service_type', 'booking_id', 'status', 'payment_status', 'phone', 'duration', 'created_at', 'updated_at']
        # You can add more fields here if needed

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = get_user_model().objects.get(email=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return user

    def create_otp(self, user):
        PasswordResetOTP.clean_expired_otps()
        
        existing_otp = PasswordResetOTP.objects.filter(user=user, expires_at__gt=timezone.now()).first()
        if existing_otp:
            existing_otp.delete()
        
        otp = get_random_string(length=4, allowed_chars='0123456789')  # 4-digit OTP
        otp_entry = PasswordResetOTP(user=user, otp=otp)
        otp_entry.save()

        # Send OTP to user's email
        send_mail(
            'Password Reset OTP from HYPNOTHERAPY',
            f'Your OTP for password reset is {otp}. It will expire in 10 minutes.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return otp_entry


class PasswordResetVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")

        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email address."})

        otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp).first()
        if not otp_entry or otp_entry.is_expired():
            raise serializers.ValidationError({"otp": "OTP is invalid or expired."})

        # Include the user object for further steps
        attrs["user"] = user
        return attrs

class PasswordResetChangeSerializer(serializers.Serializer):
    # Email of the user requesting password reset
    email = serializers.EmailField()
    # OTP sent to the user's email
    otp = serializers.CharField(max_length=4, write_only=True, required=True)
    # New password to set
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        # Retrieve email and OTP from the request data
        email = attrs.get("email")
        otp = attrs.get("otp")

        # Check if the user with the provided email exists
        try:
            user = get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError({"email": "Invalid email address."})

        # Validate the OTP for the user
        otp_entry = PasswordResetOTP.objects.filter(user=user, otp=otp).first()
        if not otp_entry or otp_entry.is_expired():
            raise serializers.ValidationError({"otp": "OTP is invalid or expired."})

        # Store the user object in validated data for further use
        attrs["user"] = user
        return attrs

    def save(self):
        # Retrieve the user and new password from validated data
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]

        # Set the new password for the user
        user.set_password(new_password)
        user.save()

        # Delete all OTPs associated with the user after resetting the password
        PasswordResetOTP.objects.filter(user=user).delete()
