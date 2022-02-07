import math
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import password_validation
from .models import *


class BlogSerializer(serializers.ModelSerializer):
	read_time = serializers.SerializerMethodField()
	
	class Meta:
		model = Blog
		fields = [
			'id',
			'title',
			'content',
			'category',
			'thumbnail',
			'published_on',
			'modified_on',
			'likes',
			'author',
			'read_time',
		]
	
	def get_read_time(self, blog):
		length = len(blog.content)
		minutes = math.floor(length/240)
		return minutes
	
class PostBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ['title', 'content', 'category', 'thumbnail',]



def ValidPassword(password, confirm_password, username):
	errors = dict()
	
	if password != confirm_password:
		errors['password_error'] =  ('Both Passwords must match.')
	elif len(username) and username.casefold() in password.casefold():
		errors['password_error'] = ('The password is too similar to the username.')
	else:
		try:
			password_validation.validate_password(password)
		except exceptions.ValidationError as e:
			errors['password_error'] = list(e.messages)
	
	if errors:
		return errors
	return ()


class RegisterUser(serializers.ModelSerializer):
	confirm_password = serializers.CharField(style={'input_type': "password"}, write_only=True,)

	class Meta:
		model = MyUser
		fields = ['name', 'email', 'username', 'password', 'confirm_password']
		extra_kwargs = {'password': {'write_only':True}}
	
	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		confirm_password = validated_data['confirm_password']
		
		errors = ValidPassword(password, confirm_password, username)
		
		if errors:
			raise serializers.ValidationError(errors)
		
		user = MyUser.objects.create(
			username = validated_data['username'],
			name = validated_data['name'],
			email = validated_data['email'],
			password = validated_data['password'],
		)
		user.set_password(password)
		user.is_active = False
		user.save()
		return user


class UserDetailSerializer(serializers.ModelSerializer):
	folower_count = serializers.SerializerMethodField()
	
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email',
			'name',
			'follower_count',
			'date_joined',
			'last_login',
			'avatar',
			'bookmark_count',
			'blog_count',
		]
	
	def get_follower_count(self, MyUser):
		return self.followers.count()
	

