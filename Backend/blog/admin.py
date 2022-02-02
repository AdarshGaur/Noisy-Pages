from django.contrib import admin
from django.contrib import messages

from .models import(
	MyUser,
	Post,
	Comment,
	OtpModel,
)

class MyUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'id', 'pk', 'active', 'date_joined')
	
	def active(self, user):
		return user.is_active
	
	active.boolean = True
	
	def make_active(modeladmin, request, queryset):
		queryset.update(is_active = 1)
		messages.success(request, "Selected Record(s) Marked as Active Successfully !!")
	
	def make_inactive(modeladmin, request, queryset):
		queryset.update(is_active = 0)
		messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")
	
	admin.site.add_action(make_active, "Make Active")
	admin.site.add_action(make_inactive, "Make Inactive")


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(OtpModel)
