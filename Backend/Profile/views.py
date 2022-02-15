from django.http import Http404
from rest_framework import status, permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import MyUser
from .serializer import UserCardSerializer, UserDetailSerializer
from blog.serializer import BlogSerializer
from blog.models import Blog



class UserDetail(APIView):
	
	def get(self, request, pk, format=None):
		try:
			user = MyUser.objects.get(pk=pk)
			print(str(user))
		except MyUser.DoesNotExist:
			raise Http404
		
		serializer = UserDetailSerializer(user, context={'request':request})
		print(user)
		return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateAvatar(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def put(self, request, format=None):
		user = request.user
		serializer = UserDetailSerializer(user, data=request.data, partial=True, context={'request': request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserFollow(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request, pk, format=None):
		user = request.user
		try:
			follow_to = MyUser.objects.get(pk=pk)
		except MyUser.DoesNotExist:
			raise Http404
		
		if follow_to == user:
			return Response({'message':'User cannot follow themself.'}, status=status.HTTP_400_BAD_REQUEST)
		
		if follow_to.followers.filter(id=user.id).exists():
			follow_to.followers.remove(user)
			message = {'message':'Unfollowed.'}
		else:
			follow_to.followers.add(user)
			message = {'message':'Followed'}
		
		return Response(message, status=status.HTTP_200_OK)


class MyFollowers(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, format=None):
		user = request.user
		followers = user.followers.all()
		serializer = UserCardSerializer(followers, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class MyFollowing(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, format=None):
		user = request.user
		followings = MyUser.objects.filter(followers=user)
		serializer = UserCardSerializer(followings, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)



class MySavedBlogs(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def get(self, request, format=None):
		user = request.user
		saved_blogs = user.bookmarks.all()
		serializer = BlogSerializer(saved_blogs, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)



class MyBlogs(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self, request, format=None):
		user = request.user
		queryset = Blog.objects.filter(author=user)
		serializer = BlogSerializer(queryset, many=True, context={'request':request})
		return Response(serializer.data)

