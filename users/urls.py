from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from .views import (
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    CustomUserDetailsViewSet,
    EmployerProfileViewSet,
    JobseekerProfileViewSet,
)

router = routers.DefaultRouter()
router.register(
    r'jobseeker/profile', JobseekerProfileViewSet, 
    basename='jobseeker_profile',
)

router.register(
    r'employer/profile', EmployerProfileViewSet, 
    basename='employer_profile',
)

router.register(
    r'auth/user/me', CustomUserDetailsViewSet, 
    basename='custom_user_details_view',
)


from dj_rest_auth.jwt_auth import get_refresh_view

from .views import (
    CustomPasswordChangeView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    CustomResendEmailVerificationView,
    CustomTokenVerifyView,
    CustomVerifyEmailView,
    DeleteUserAccountView,
    LoginStateView,
)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('auth/logout/', CustomLogoutView.as_view(), name='custom_logout'),

    # switch from employer to jobseeker profile
    path('auth/login-state/switch/', LoginStateView.as_view(), name='profile_switch'),

    # send an email after successful signup
    path('account-confirm-email/<str:key>/', TemplateView.as_view(), name='account_confirm_email'),
    path('auth/confirm-email/', CustomVerifyEmailView.as_view(), name='account_email_verification_sent'),

    # resend verification email
    path('auth/resend-confirmation-email/', CustomResendEmailVerificationView.as_view(), name='rest_resend_email'),

    # password change
    path('auth/password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    
    # password reset
    path('password-reset/confirm/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),
    path('auth/password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('auth/password/reset/confirm/', CustomPasswordResetConfirmView.as_view(), name='password_reset_complete'),

    # tokens
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    
    # extra
    # path('auth/', include('dj_rest_auth.urls')),
]

# account_confirm_email
