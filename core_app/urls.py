"""
URL configuration for marumado project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include # type: ignore
from core_app.jwt import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from core_app.views import (
    UserViewSet,
    ServiceTypeViewSet,
    UserProfileView,
    PasswordResetRequestView,
    PasswordResetVerifyView,
    PasswordResetChangeView,
    RegistrationView,
    BookingAPIViewForUser,
    DashboardAPIView,
    BookingViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'service-type', ServiceTypeViewSet, basename='serivce_type')
router.register(r'bookings', BookingViewSet, basename='booking_admin')

urlpatterns = [
    # Custom login with email and password to obtain the token
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Token verification endpoint
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Token refresh endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('user/me/', UserProfileView.as_view(), name='user_profile'),
    path('signup/', RegistrationView.as_view(), name='register'),
    
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-verify/', PasswordResetVerifyView.as_view(), name='password_reset_verify'),
    path('password-reset-change/', PasswordResetChangeView.as_view(), name='password_reset_change'),
    
    path('booking-for-user/', BookingAPIViewForUser.as_view(), name='booking_for_user'),

    path('admin/dashboard/', DashboardAPIView.as_view(), name="admin_dashboard"),
    
    path('', include(router.urls)),
]
