from django.core import exceptions
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth import password_validation
from .models import *

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
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
		]


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

