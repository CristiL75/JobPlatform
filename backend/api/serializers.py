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
from .models import JobSeekerPost
from rest_framework import serializers

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
        

class JobSeekerPostSerializer(serializers.ModelSerializer):
    # Use CharField to accept username as a string for input and output
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = JobSeekerPost
        fields = '__all__'

    def create(self, validated_data):
        # Extract the username from the nested dictionary created_by
        username = validated_data.pop('created_by')['username']

        # Get the User instance corresponding to the username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"created_by": "User with this username does not exist."})

        # Create the JobSeekerPost instance with the user
        job_seeker_post = JobSeekerPost.objects.create(created_by=user, **validated_data)
        return job_seeker_post

    def update(self, instance, validated_data):
        # Similar to create, handle the update with the username
        username = validated_data.pop('created_by', {}).get('username', None)
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError({"created_by": "User with this username does not exist."})
            instance.created_by = user

        # Update the rest of the fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
