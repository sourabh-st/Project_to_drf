from pyexpat import model
from rest_framework import serializers
from .models import MyProfile, MyPost

class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        # fields = '__all__'
        exclude = ['user']


class MyPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPost
        fields = ['subject','cr_date', 'pic']

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

class PostCreateSerializer(serializers.Serializer):
    pic = serializers.ImageField()
    subject = serializers.CharField()
    cr_date = serializers.DateTimeField()


class ConnectionsSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()

class FollowSerializer(serializers.Serializer):
    id = serializers.IntegerField()