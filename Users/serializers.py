from rest_framework import serializers
from Users.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.models import User as DjangoUser

class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ['id', 'username', 'email']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    user = DjangoUserSerializer()  # Nested serializer for the user field

    class Meta:
        model = UserProfile
        fields = ['user', 'email', 'address', 'is_admin']




    
