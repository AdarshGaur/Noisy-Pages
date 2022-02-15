from django.http import Http404
from rest_framework import status, permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Blog, Comment
from .serializer import *
from .permission import IsAuthorOrReadOnly, IsCommenterorAuthor

from django.db.models import F



class BlogView(APIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	def get(self, request, format=None):
		queryset = Blog.objects.all()
		serializer = BlogSerializer(queryset, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		user = request.user
		serializer = PostBlogSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=user)
			user.post_count = F('post_count')+1
			user.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetail(APIView):
	permission_classes = [IsAuthorOrReadOnly]
	
	def get_blog_object(self, request, pk):
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist:
			raise Http404
		return blog
	
	def get(self, request, pk, format=None):
		blog = self.get_blog_object(request, pk)
		is_bookmarked = is_liked = is_author = False
		if not request.user.is_anonymous:
			if blog.likers.filter(pk=request.user.pk).exists():
				is_liked = True
			if request.user.bookmarks.filter(pk=pk).exists():
				is_bookmarked = True
			if request.user == blog.author:
				is_author = True
		serializer = BlogSerializer(
			blog,
			context={
				'request' : request,
				'is_bookmarked' : is_bookmarked,
				'is_liked' : is_liked,
				'is_author': is_author,
			}
		)
		print(blog)
		return Response(serializer.data)
	
	def put(self, request, pk, format=None):
		blog = self.get_blog_object(request, pk)
		serializer = BlogSerializer(blog, data=request.data, partial=True, context={'request':request})
		self.check_object_permissions(request, blog)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
	
	def delete(self, request, pk, format=None):
		blog = self.get_blog_object(request, pk)
		user = request.user
		self.check_object_permissions(request, blog)
		blog.delete()
		user.post_count = F('post_count')-1
		user.save()
		return Response({'message':'Blog Deleted Successfully'}, status=status.HTTP_200_OK)


class LikeBlog(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request, pk, format=None):
		user = request.user
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist:
			raise Http404
		
		if blog.likers.filter(id=user.id).exists():
			blog.likers.remove(user)
			message = {'message': 'Unliked'}
		else:
			blog.likers.add(user)
			message = {'message': 'Liked'}
		
		return Response(message, status=status.HTTP_200_OK)


class BookmarkBlog(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request, pk, format=None):
		user = request.user
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist:
			raise Http404
		
		if user.bookmarks.filter(id=blog.id).exists():
			user.bookmarks.remove(blog)
			message = {'message':'Bookmark removed Successfully.'}
		else:
			user.bookmarks.add(blog)
			message = {'message':'Bookmark added Successfully.'}
		
		return Response(message, status=status.HTTP_200_OK)


class CommentView(APIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	def find_blog(self, pk):
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist :
			raise Http404
		return blog
	
	def get(self, request, pk, format=None):
		blog = self.find_blog(pk)
		comments = blog.comments.all()
		serializer = CommentSerializer(comments, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	
	def post(self, request, pk, format=None):
		user = request.user
		blog = self.find_blog(pk)
		serializer = PostCommentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(author=user, blog=blog)
			return Response({'message':'Comment Posted.'}, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UpdateComment(APIView):
	permission_classes = [IsCommenterorAuthor]
	
	def find_blog(self, pk):
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist :
			raise Http404
		return blog
	
	def put(self, request, pk, pk_alt, format=None):
		blog = self.find_blog(pk=pk)
		try:
			comment = Comment.objects.get(pk=pk_alt)
		except Comment.DoesNotExist:
			return Response({'message':'Comment Does Not Exists.'}, status=status.HTTP_400_BAD_REQUEST)
		self.check_object_permissions(request, comment)
		serializer = PostCommentSerializer(comment, data=request.data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
		
	def delete(self, request, pk, pk_alt, format=None):
		blog = self.find_blog(pk=pk)
		try:
			comment = Comment.objects.get(pk=pk_alt)
		except Comment.DoesNotExist:
			return Response({'message':'Comment Does Not Exist.'}, status=status.HTTP_400_BAD_REQUEST)
		self.check_object_permissions(request, comment)
		comment.delete()
		return Response({'message':'Comment Deleted Successfully.'}, status=status.HTTP_200_OK)

