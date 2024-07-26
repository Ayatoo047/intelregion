from rest_framework.permissions import BasePermission
from post.models import Blog, Comment
from django.contrib.auth.models import User


from rest_framework.permissions import BasePermission

class IsBlogOwner(BasePermission):
    """
    Custom permission to allow update on blogs only to their owners.
    """

    def has_permission(self, request, view):
        try:
            blog = view.get_queryset().get(pk=view.kwargs['pk'])
            return request.user == blog.owner
        except (Blog.DoesNotExist, KeyError):
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class IsCommentOwner(BasePermission):
    """
    Custom permission to allow update on comment only to their owners.
    """

    def has_permission(self, request, view):
        try:
            comment = view.get_queryset().get(pk=view.kwargs['pk'])
            return request.user == comment.owner
        except (Comment.DoesNotExist, KeyError):
            return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
