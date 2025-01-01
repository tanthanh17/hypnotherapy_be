from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import datetime

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(TimestampMixin):
    name = models.CharField(max_length=255, unique=True)

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "role"

class CustomUser(AbstractUser):
    # Adding a full_name field instead of first_name and last_name
    full_name = models.CharField(max_length=255, blank=True)
    
    roles = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    
    # Remove the default fields for first_name and last_name
    first_name = None
    last_name = None
    phone = models.CharField(max_length=20, default="")

    # Return full_name when the object is printed, otherwise use username
    def __str__(self):
        return self.full_name or self.username
    
    class Meta:
        db_table = "user"
        
class ServiceType(TimestampMixin):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "service_type"

class Booking(TimestampMixin):
    # Client's full name
    client_name = models.CharField(max_length=255)

    # Service type as a foreign key referencing the ServiceType model
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True)

    # Unique Booking ID
    booking_id = models.CharField(max_length=20, unique=True)

    # Status of the booking (Pending, Confirmed, Completed, etc.)
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Payment status (Paid, Unpaid, Pending)
    PAYMENT_STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('unpaid', 'Unpaid'),
        ('pending', 'Pending'),
    ]
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid'
    )

    # Client's phone number
    phone = models.CharField(max_length=20)

    # Duration in minutes
    duration = models.PositiveIntegerField()
    
    session_datetime = models.DateTimeField(default=timezone.now)
    message = models.TextField(blank=True, null=True)
    
    start_time = models.TimeField(default=datetime.time(0, 0))
    end_time = models.TimeField(default=datetime.time(0, 0)) 

    def __str__(self):
        return f"Booking {self.booking_id} - {self.client_name}"

    class Meta:
        # Optionally, you can order bookings by the creation date
        ordering = ['-created_at']
        
        db_table = "booking"
        
        
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new OTP, set expiry time
            self.expires_at = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP for {self.user.email} valid until {self.expires_at}"
    
    @classmethod
    def clean_expired_otps(cls):
        expired_otps = cls.objects.filter(expires_at__lt=timezone.now())
        expired_otps.delete()

    class Meta:
        db_table = "password_reset_otp"

