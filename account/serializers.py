from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from intelregion.modules.utils import api_response
from intelregion.modules.exceptions import InvalidRequestException
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
        
    def create(self, validated_data):
        if validated_data.get('email', None) is None:
            raise InvalidRequestException()
        user = super().create(validated_data)
        print(user)
        return CreateUserSerializerOut(
            user, context={"request": self.context.get("request")}
        ).data
        
        
class CreateUserSerializerOut(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class LoginSerializerIn(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def create(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
        
        user = User.objects.filter(username=username).first()
        if user:
            if user.is_authenticated:
                return user
        user = authenticate(username=username, password=password)
        print(user)
        if not user:
            response = api_response(message="Invalid email or password", status=False)
            raise InvalidRequestException(response)
        
        return user


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'username']

