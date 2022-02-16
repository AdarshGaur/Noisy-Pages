from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from blog.models import Blog

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



def user_img_path(instance, filename):
	return '/'.join(['avatars', instance.email, filename])


class MyUser(AbstractUser):
	# regex validators
	name_regex 		= RegexValidator('^[a-zA-Z ]+$', 'Only letters and spaces are allowed in Name.')
	email_regex 	= RegexValidator('^[a-zA-Z0-9]+([-._][a-zA-Z0-9]+)*@[a-zA-Z0-9]+([-.][a-zA-Z0-9]+)*\.[a-zA-Z]{2,7}$', 'Invalid Email Address')

	username 		= models.CharField(max_length=40, unique=True)
	email 			= models.EmailField(max_length=40, unique=True, help_text='Required', validators=[email_regex])
	name 			= models.CharField(blank=False, max_length=50,validators=[name_regex])
	date_joined 	= models.DateTimeField(auto_now_add=True)
	last_login 		= models.DateTimeField(auto_now=True)
	about 			= models.TextField(max_length=500, blank=True, null=True)
	followers 		= models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by')
	avatar 			= models.ImageField(upload_to=user_img_path, default='default-avatar.png')
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

