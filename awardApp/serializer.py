from rest_framework import serializers
from .models import Profile, Post
from django.contrib.auth.models import User


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'profile_picture', 'bio', 'location', 'contact']


class Post_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'url', 'description', 'technologies', 'photo', 'date', 'user']

class User_Serializer(serializers.ModelSerializer):
    profile = Profile_Serializer(read_only=True)
    posts = Post_Serializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'profile', 'posts']

