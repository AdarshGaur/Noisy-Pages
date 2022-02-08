from __future__ import absolute_import
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


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
	# test for instance.title and instance.email
	if isinstance(instance, MyUser):
		return '/'.join(['avatars', instance.email, filename])
	return '/'.join(['img', instance.title, filename])


class Blog(models.Model):
	title 			= models.CharField(max_length=30)
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
	blog 			= models.ForeignKey(Blog, related_name='comments_on', on_delete=models.CASCADE)
	commenter 		= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='commenter', on_delete=models.CASCADE)
	content 		= models.TextField(blank=False, null=False)
	created_on 		= models.DateTimeField(auto_now_add=True)
	is_active 		= models.BooleanField(default=True)
	
	def __str__(self):
			return 'comment {} on blog {} by {}'.format(self.content, self.blog, self.commenter)
	
	class Meta:
		ordering = ['-created_on']


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The User must have an email.')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		if extra_fields.get('is_active') is not True:
			raise ValidationError('Superuser must have is_active=True by default.')
		return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
	# regex validators
	name_regex 		= RegexValidator('^[a-zA-Z ]+$', 'Only letters and spaces are allowed in Name.')
	email_regex 	= RegexValidator('^[a-zA-Z0-9]+([-._][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([-.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,7}$', 'Invalid Email Address')

	username 		= models.CharField(max_length=40, unique=True)
	email 			= models.EmailField(max_length=40, unique=True, help_text='Required', validators=[email_regex])
	name 			= models.CharField(blank=False, max_length=50,validators=[name_regex])
	date_joined 	= models.DateTimeField(auto_now_add=True)
	last_login 		= models.DateTimeField(auto_now=True)
	about 			= models.CharField(max_length=300, blank=True, null=True)
	followers 		= models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by')
	avatar 			= models.ImageField(upload_to=img_path, default='default-avatar.png')
	bookmarks	 	= models.ManyToManyField(Blog, blank=True, related_name='my_bookmarks')
	post_count 		= models.PositiveIntegerField(default=0)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'username']

	objects = UserManager()

	def __str__(self):
		return self.email
	
	def count_followers(self):
		return self.followers.count()
	
	def count_bookmarks(self):
		return self.bookmarks.count()


class OtpModel(models.Model):
	otp 			= models.IntegerField()
	email 			= models.EmailField(blank=False, unique=True)
	time 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		name = str(self.otp) + ' of ' + str(self.email)
		return name
