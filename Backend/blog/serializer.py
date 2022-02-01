from rest_framework import serializers
from django.contrib.auth import password_validation
from .models import (
	Post,
	MyUser,
	Comment,
)

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


class RegisterUser(serializers.ModelSerializer):
	confirm_password = serializers.CharField(style={'input_type': "password"}, write_only=True,)

	class Meta:
		model = MyUser
		fields = ['name', 'email', 'username', 'password', 'confirm_password']
		extra_kwargs = {'password': {'write_only':True}}
	
	def create(self, validated_data):
		password = validated_data['password']
		confirm_password = validated_data['confirm_password']

		if password != confirm_password:
			raise serializers.ValidationError({'password_error': 'Both Passwords must match.'})

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


