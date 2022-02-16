import math
from rest_framework import serializers
from .models import *


class BlogSerializer(serializers.ModelSerializer):
	read_time = serializers.SerializerMethodField()
	is_liked = serializers.SerializerMethodField()
	is_bookmark = serializers.SerializerMethodField()
	is_author = serializers.SerializerMethodField()
	
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
			'author',
			'read_time',
			'likes_count',
			'is_liked',
			'is_bookmark',
			'is_author',
		]
	
	def get_read_time(self, blog):
		length = len(blog.content)
		minutes = math.floor(length/150)
		return minutes
	
	def get_is_liked(self, blog):
		return self.context.get('is_liked')
	
	def get_is_bookmark(self, blog):
		return self.context.get('is_bookmarked')
		
	def get_is_author(self, blog):
		return self.context.get('is_author')


class PostBlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ['title', 'content', 'category', 'thumbnail',]


class CommentSerializer(serializers.ModelSerializer):
	img = serializers.SerializerMethodField()
	
	class Meta:
		model = Comment
		# include author's username thorugh methodfield!
		fields = ['id', 'author', 'content', 'created_on', 'modified_on', 'img',]
	
	def get_img(self, comment):
		return comment.author.avatar.url


class PostCommentSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Comment
		fields = ['content',]
