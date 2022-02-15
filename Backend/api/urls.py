
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
	#Authentication Related Urls
	path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('register/', RegisterUserView.as_view()),
	path('register/verify-otp/', VerifyOTP.as_view()),
	path('register/resend-otp/', ResendOtp.as_view()),
	path('forgot-password/', ForgotPassword.as_view()),
	path('forgot-password/new-password/', NewPassword.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])