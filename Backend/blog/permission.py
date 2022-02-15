from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		print("has permission called just now !")
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user.is_authenticated
	
	def has_object_permission(self, request, view, obj):
		print('Has object check is finally done now !!!!!')
		return obj.author == request.user


class IsCommenterorAuthor(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user.is_authenticated
	
	def has_object_permission(self, request, view, comment):
		if request.method == 'PUT' or request.method == 'PATCH':
			return request.user == comment.author
		return request.user == comment.author or request.user == comment.blog.author
			

