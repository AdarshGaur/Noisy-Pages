from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
	#Blog Related Routes
	path('blog/', BlogView.as_view()),											# To List all blogs or Create a new Blog
	path('blog/<int:pk>/', BlogDetail.as_view()),								# To Get the detail view of blogs
	path('blog/<int:pk>/like/', LikeBlog.as_view()),							# To Like/Unlike the Blog
	path('blog/<int:pk>/bookmark/', BookmarkBlog.as_view()),					# To add/remove bookmark
	path('blog/<int:pk>/comments/', CommentView.as_view()),						# To add/get comments on a Blog
	path('blog/<int:pk>/comments/<int:pk_alt>/', UpdateComment.as_view()),		# To update the comment on a blog

	
	#User Related Routes
	path('user/<int:pk>/', UserDetail.as_view()),					# To Get the detials of a user
	path('user/my-blogs/', MyBlogs.as_view()),						# To Get the detials of a user
	path('user/update-avatar/', UpdateAvatar.as_view()),			# To Change the avatar of the user
	path('user/<int:pk>/follow/', UserFollow.as_view()),			# To Follow/Unfollow the user
	path('user/saved/', MySavedBlogs.as_view()),					# To Get the saved/bookmarked blogs
	path('user/followers/', MyFollowers.as_view()),					# To Get the list of my followers
	path('user/followings/', MyFollowing.as_view()),				# To Get the list of my followings


	#Authentication Related Routes
	path('auth/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('auth/register/', RegisterUserView.as_view()),
	path('auth/register/verify-otp/', VerifyOTP.as_view()),
	path('auth/register/resend-otp/', ResendOtp.as_view()),
	path('auth/forgot-password/', ForgotPassword.as_view()),
	path('auth/forgot-password/new-password/', NewPassword.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
