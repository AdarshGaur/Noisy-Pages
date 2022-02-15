from django.db import models
from django.conf import settings


categories_choices = [
	('travel', 'Travel'),
	('food', 'Food'),
	('culture', 'Culture and Tradition'),
	('tech', 'Technology'),
	('edu', 'Educational'),
	('social', 'Social Life'),
	('entertainment', 'Entertainment'),
	('psychology', 'Psychology'),
	('others', 'Others'),
]


def img_path(instance, filename):
	return '/'.join(['img', instance.title, filename])


class Blog(models.Model):
	title 			= models.CharField(max_length=30, unique=True)
	content 		= models.TextField(blank=False, null=False)
	category		= models.TextField(choices=categories_choices, default='Others')
	thumbnail 		= models.ImageField(upload_to=img_path, null=False, blank=False)
	author 			= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blogs', on_delete=models.CASCADE)
	published_on	= models.DateTimeField(auto_now_add=True)
	modified_on		= models.DateTimeField(auto_now=True)
	likers 			= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_by', blank=True)

	def __str__(self):
		return self.title
	
	def count_likes(self):
		return self.likers.count()
	
	class Meta:
		ordering = ['-published_on']


class Comment(models.Model):
	blog 			= models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
	author	 		= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commenter', on_delete=models.CASCADE)
	content 		= models.TextField(blank=False, null=False)
	created_on 		= models.DateTimeField(auto_now_add=True)
	modified_on		= models.DateTimeField(auto_now=True)
	
	def __str__(self):
			return 'comment id = {} on blog {} by {}'.format(self.id, self.blog, self.commenter)
	
	class Meta:
		ordering = ['-created_on']

