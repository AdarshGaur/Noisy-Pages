from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
	#Blog Related Routes
	path('', BlogView.as_view()),
	path('blog/', BlogView.as_view()),										# To List all blogs or Create a new Blog
	path('blog/<int:pk>/', BlogDetail.as_view()),							# To Get the detail view of blogs
	path('blog/<int:pk>/like/', LikeBlog.as_view()),						# To Like/Unlike the Blog
	path('blog/<int:pk>/bookmark/', BookmarkBlog.as_view()),				# To add/remove bookmark
	path('blog/<int:pk>/comments/', CommentView.as_view()),					# To add/get comments on a Blog
	path('blog/<int:pk>/comments/<int:pk_alt>/', UpdateComment.as_view()),	# To update the comment on a blog
	path('blog/categories/', CategoriesView.as_view()),						# To get the specific ordered blog list
	path('blog/search/', SearchBlogView.as_view()),							# To search the blog by their title
]


urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json'])
