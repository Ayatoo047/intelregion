from rest_framework.permissions import BasePermission
from post.models import Blog, Comment
from django.contrib.auth.models import User


class IsPostAuthor(BasePermission):
    def has_permission(self, request, view):
        blog_id = view.kwargs.get('pk')
        blog = Blog.objects.filter(id=blog_id).first()
        if blog:
            try:
                user : User =request.user
            except User.DoesNotExist:
                return False
            if blog.owner == user:
                return True
            else:
                return False

class IsCommentAuthor(BasePermission):
    def has_permission(self, request, view):
        comment_id = view.kwargs.get('pk')
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            try:
                user : User = request.user
            except User.DoesNotExist:
                return False
            if comment.owner == user:
                return True
            else:
                return False