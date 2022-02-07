from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	#Post Related Routes
	path('blog/', views.BlogView.as_view()),						# To List all blogs or Create a new post
	path('blog/<int:pk>/', views.BlogDetail.as_view()),				# To Get the detail view of blogs

	
	#User Related Routes
	path('user/<int:pk>/', views.UserDetail.as_view()),				# To Get the detials of a user
	path('user/my-blogs/', views.MyBlogs.as_view()),				# To Get the detials of a user
	path('user/update-avatar/', views.UpdateAvatar.as_view()),		# To Change the avatar of the user

	#Authentication Related Routes
	path('auth/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('auth/register/', views.RegisterUserView.as_view()),
	path('auth/register/verify-otp/', views.VerifyOTP.as_view()),
	path('auth/register/resend-otp/', views.ResendOtp.as_view()),
	path('auth/forgot-password/', views.ForgotPassword.as_view()),
	path('auth/forgot-password/new-password/', views.NewPassword.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
