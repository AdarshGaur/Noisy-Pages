from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
	#User Related Routes
	path('<int:pk>/', UserDetail.as_view()),				# To Get the detials of a user
	path('my-blogs/', MyBlogs.as_view()),					# To Get the detials of a user
	path('update-avatar/', UpdateAvatar.as_view()),			# To Change the avatar of the user
	path('<int:pk>/follow/', UserFollow.as_view()),			# To Follow/Unfollow the user
	path('saved/', MySavedBlogs.as_view()),					# To Get the saved/bookmarked blogs
	path('followers/', MyFollowers.as_view()),				# To Get the list of my followers
	path('followings/', MyFollowing.as_view()),				# To Get the list of my followings

]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
