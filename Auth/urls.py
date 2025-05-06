from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView

urlpatterns = [
    path("login/",TokenObtainPairView.as_view(),name="login-view"),
    path("logout/",TokenBlacklistView.as_view(),name="logout-view"),

    path("password/reset/",PasswordResetView.as_view(),name="password-resert-view"),
    path("password/reset/confirm/",PasswordResetConfirmView.as_view(),name="password-reset-confirm-view"),

    # path("password-change/",PasswordChangeView.as_view(),name="password-change-view"),

    path("registration/",RegistrationView.as_view(),name="registration-view"),
    path("registration/verify/email/",VerifyOtpView.as_view(),name="email-verification"),
    path("registration/resend/email/",ResendEmailView.as_view(),name="resend-email-verification"),
]