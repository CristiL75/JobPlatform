from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .models import JobPost
from .models import UserInterest

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "password_confirmation", "email", "first_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password_confirmation": {"write_only": True},
        }

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError({"password_confirmation": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name')
        )
        return user


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')  # Add this line if not present

    class Meta:
        model = UserProfile
        fields = ['username', 'city', 'education', 'experience', 'skills', 'certifications', 'languages', 'interests', 'resume']
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        
# Example JobPostSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .models import JobPost
from .models import UserInterest

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "password_confirmation", "email", "first_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password_confirmation": {"write_only": True},
        }

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError({"password_confirmation": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name')
        )
        return user


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')  # Add this line if not present

    class Meta:
        model = UserProfile
        fields = ['username', 'city', 'education', 'experience', 'skills', 'certifications', 'languages', 'interests', 'resume']
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        
        
# Example JobPostSerializer
class JobPostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)  # Nested serializer to include the username

    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'description', 'location', 'company', 'salary',
            'employment_type', 'domain', 'experience_level', 'job_type',
            'languages', 'skills', 'created_at', 'created_by'
        ]
class UserInterestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = UserInterest
        fields = ['user', 'job_post']

class UserInterestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = UserInterest
        fields = ['user', 'job_post']