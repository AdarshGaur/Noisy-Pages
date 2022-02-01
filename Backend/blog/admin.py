import imp
from django.contrib import admin

from .models import(
	MyUser,
	Post,
	Comment,
	OtpModel,
)

admin.site.register(MyUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(OtpModel)
