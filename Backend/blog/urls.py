from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
	path('', views.ListPosts.as_view()),
	path('post/<int:pk>/', views.DetailPosts.as_view()),

	#Authentication Related Routes
	path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('auth/register/', views.RegisterUserView.as_view()),
	path('auth/register/verify-otp/', views.VerifyOTP.as_view()),
	path('auth/register/resend-otp/', views.ResendOtp.as_view()),
	path('auth/forgot-password/', views.ForgotPassword.as_view()),
	path('auth/forgot-password/new-password/', views.NewPassword.as_view()),
]

