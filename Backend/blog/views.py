import datetime
from functools import partial
from random import randint

from django.conf import settings
from django.core.mail import send_mail

from rest_framework import generics, status, permissions

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .models import *
from .serializer import *
from .permission import IsAuthorOrReadOnly

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
	
	def get_blog_object(self, pk):
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist:
			raise Response({'message':'Blog Does Not Exist.'}, status=status.HTTP_400_BAD_REQUEST)
		return blog
	
	def get(self, request, pk, format=None):
		blog = self.get_blog_object(pk)
		serializer = BlogSerializer(blog, context={'request':request})
		print(blog)
		return Response(serializer.data)
	
	def put(self, request, pk, format=None):
		blog = self.get_blog_object(pk)
		serializer = BlogSerializer(blog, data=request.data, partial=True, context={'request':request})
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
		return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
	
	def delete(self, request, pk, format=None):
		blog = self.get_blog_object(pk)
		user = request.user
		if user != blog.author:
			return Response({'message':'Only Author can delete his/her blog.'}, status=status.HTTP_401_UNAUTHORIZED)
		blog.delete()
		user.blog_count = F('blog_count')-1
		user.save()
		return Response({'message':'Blog Deleted Successfully'}, status=status.HTTP_200_OK)


class UserDetail(APIView):
	
	def get(self, request, pk, format=None):
		try:
			user = MyUser.objects.get(pk=pk)
			print(str(user))
		except MyUser.DoesNotExist:
			return Response({'message':'User Does Not Exist'}, status=status.HTTP_400_BAD_REQUEST)
		
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


class MyBlogs(APIView):
	permission_classes = [permissions.IsAuthenticated]
	
	def get(self, request, format=None):
		user = request.user
		queryset = Blog.objects.filter(author=user)
		serializer = BlogSerializer(queryset, many=True, context={'request':request})
		return Response(serializer.data)


def Verification(email):
	# First create the otp object and save it
	otp = randint(100000, 999999)
	print(otp)
	try:
		myotp = OtpModel.objects.get(email__iexact=email)
		myotp.delete()
	except:
		pass
	OtpModel.objects.create(otp=otp, email=email)

	# send the otp throuh verification email
	to_email = [email]
	email_from = settings.EMAIL_HOST_USER
	send_mail(
		'Verification Email !',
		'Your 6 digit Verification Pin is {} .\nArigato Gozaimasu, For Registering on Noisy Pages, Hope you have a lot of noisy ideas'.format(otp),
		email_from,
		to_email,
		fail_silently = False,
	)
	print('Email Sended.')
	message = {'message': 'Otp Sended Successfully'}
	return message

def GiveToken(user):
	r_token = TokenObtainPairSerializer().get_token(user)
	a_token = AccessToken().for_user(user)
	token = {
		'refresh' : str(r_token),
		'access': str(a_token),
	}
	return token


class RegisterUserView(APIView):

	def post(self, request, format=None):
		email = request.data.get('email')
		try :
			user_exist = MyUser.objects.get(email__iexact = email)
			if user_exist.is_active is not True:
				user_exist.delete()
			else:
				message = {'message': 'User Already Exists.'}
				return Response(message, status = status.HTTP_406_NOT_ACCEPTABLE)
		except MyUser.DoesNotExist:
			pass
		
		serializer = RegisterUser(data=request.data)

		if serializer.is_valid():
			serializer.save()
			message = Verification(email)
			return Response(message, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class VerifyOTP(APIView):

	def post(self, request):
		email = request.data.get('email')
		# check for the is_active of the user, it should be false
		otp = request.data.get('otp')
		if not otp.isnumeric():
			return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
		try:
			email_to_verify = OtpModel.objects.get(email__iexact=email)
		except OtpModel.DoesNotExist:
			message = {'message': "Register First."}
			return Response(message, status=status.HTTP_401_UNAUTHORIZED)
		
		current_time = datetime.datetime.now()
		time_limit = email_to_verify.time + datetime.timedelta(minutes=5)
		if(current_time > time_limit):
			message = {'message': 'otp expired'}
			email_to_verify.delete()
			return Response(message, status=status.HTTP_401_UNAUTHORIZED)
		elif email_to_verify.otp != int(otp):
			message = {'message': 'Wrong OTP'}
			return Response(message, status=status.HTTP_401_UNAUTHORIZED)
		
		user_to_allow = MyUser.objects.get(email__iexact=email)
		user_to_allow.is_active = True
		user_to_allow.save()
		email_to_verify.delete()

		# introduce token here later
		token = GiveToken(user_to_allow)
		return Response(token, status=status.HTTP_200_OK)


class ResendOtp(APIView):
	
	def post(self, request, format=None):
		email = request.data.get('email')
		try:
			user = MyUser.objects.get(email__iexact=email)
		except MyUser.DoesNotExist:
			return Response({'message':'Register First'}, status=status.HTTP_401_UNAUTHORIZED)
		message = Verification(email)
		return Response(message, status=status.HTTP_200_OK)


class ForgotPassword(APIView):

	def post(self, request, format=None):
		email = request.data.get('email')
		
		try:
			user_to_verify = MyUser.objects.get(email__iexact=email)
		except MyUser.DoesNotExist:
			message = {'messgae': 'Register First.'}
			return Response(message, status=status.HTTP_401_UNAUTHORIZED)
		
		if user_to_verify.is_active is not True:
			message = {'message': 'Register First.'}
			return Response(message, status=status.HTTP_401_UNAUTHORIZED)
		
		message = Verification(email)
		return Response(message, status=status.HTTP_200_OK)


class NewPassword(APIView):

	def post(self, request, format=None):
		email = request.data.get('email')
		try:
			user = MyUser.objects.get(email__iexact=email)
		except MyUser.DoesNotExist:
			message = {'message': 'User Does Not Exist.'}
			return Response(message, status=status.HTTP_400_BAD_REQUEST)

		new_password = request.data.get('password')
		confirm_password = request.data.get('confirm_password')

		if str(new_password) != str(confirm_password):
			message = {'message': 'Both Passwords Must Match'}
			return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)
		
		user.set_password(new_password)
		user.save()

		#token
		token = GiveToken(user)
		return Response(token, status=status.HTTP_202_ACCEPTED)


class LikeBlog(APIView):
	permission_classes = [permissions.IsAuthenticated]
	def post(self, request, pk, format=None):
		user = request.user
		try:
			blog = Blog.objects.get(pk=pk)
		except Blog.DoesNotExist:
			return Response({'message': "Blog Does Not Exist."}, status=status.HTTP_400_BAD_REQUEST)
		
		if blog.likers.filter(id=user.id).exists():
			blog.likers.remove(user)
			message = {'message': 'Unliked'}
		else:
			blog.likers.add(user)
			message = {'message': 'Liked'}
		
		return Response(message, status=status.HTTP_200_OK)


