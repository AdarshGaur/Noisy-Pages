from rest_framework import serializers
from .models import MyUser


class UserDetailSerializer(serializers.ModelSerializer):
	follower_count = serializers.SerializerMethodField()
	bookmark_count = serializers.SerializerMethodField()
		
	class Meta:
		model = MyUser
		fields = [
			'id',
			'username',
			'email',
			'name',
			'about',
			'follower_count',
			'date_joined',
			'last_login',
			'avatar',
			'bookmark_count',
			'post_count',
		]
	
	def get_follower_count(self, user):
		return user.count_followers()
	
	def get_bookmark_count(self, user):
		return user.count_bookmarks()

	
class UserCardSerializer(serializers.ModelSerializer):
	class Meta:
		model = MyUser
		fields = ['id', 'name', 'username', 'email', 'avatar', 'last_login',]
