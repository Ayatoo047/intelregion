from rest_framework import serializers
from .models import Blog, Comment
from django.contrib.auth.models import User


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    class Meta:
        model = Blog
        exclude = ['content']


class BlogDetailSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    class Meta:
        model = Blog
        fields = '__all__'


class BlogSerializerIn(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content']


    def create(self, validated_data):
        user_id = self.context['user_id']
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return
        blog = Blog.objects.create(
            owner = user,
            **validated_data
        )

        return BlogDetailSerializer(
            blog, context={"request": self.context.get("request")}
        ).data
    
    def update(self, instance, validated_data):
        blog = super().update(instance, validated_data)
        return BlogDetailSerializer(
            blog, context={"request": self.context.get("request")}
        ).data
class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username')
    blogs = serializers.CharField(source='blogs.title')
    class Meta:
        model = Comment
        fields = '__all__'
        
class CommentSerializerIn(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']

    def create(self, validated_data):
        print(self.context)
        user_id = self.context['user_id']
        blogs_id = self.context['blog_id']
        user = User.objects.filter(id=user_id).first()
        blog = Blog.objects.filter(id=blogs_id).first()
        if user is None or blog is None:
            return
        comment = Comment.objects.create(
            owner = user,
            blogs = blog,
            **validated_data
        )
        return CommentSerializer(
            comment, context={"request": self.context.get("request")}
        ).data
    
    def update(self, instance, validated_data):
        comment = super().update(instance, validated_data)
        return CommentSerializer(
            comment, context={"request": self.context.get("request")}
        ).data