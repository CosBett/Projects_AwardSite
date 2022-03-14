from rest_framework import serializers
from .models import Profile, Post
from django.contrib.auth.models import User


class Profile_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'profile_picture', 'bio', 'location', 'contact']

