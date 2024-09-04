# views.py

from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import JobPost
from .serializers import JobPostSerializer
from .models import JobPost, UserInterest
from .serializers import UserInterestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import JobSeekerPostSerializer
from rest_framework import viewsets
from .models import JobSeekerPost
from .serializers import JobSeekerPostSerializer
from django.http import JsonResponse
import json 
import requests
import logging
from django.conf import settings
from django.views import View
from .models import Message
from django.shortcuts import render

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None, format=None):
        # Fetch profile by username if provided, otherwise get current user's profile
        if username:
            profile = get_object_or_404(UserProfile, user__username=username)
        else:
            profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    
    def post(self, request, username=None, format=None):
        if username:
            profile = get_object_or_404(UserProfile, user__username=username)
        else:
            profile, created = UserProfile.objects.get_or_create(user=request.user)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    

    


class JobPostListCreateView(generics.ListCreateAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Permite vizualizarea anunțurilor fără autentificare, dar pentru a crea un anunț trebuie să fie autentificat

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ShowInterestView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the view requires authentication

    def post(self, request, pk):
        user = request.user
        try:
            job_post = JobPost.objects.get(pk=pk)
            # Handle the interest logic here
            interest, created = UserInterest.objects.get_or_create(user=user, job_post=job_post)
            if created:
                return Response({'message': 'Interest recorded'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Already showed interest'}, status=status.HTTP_400_BAD_REQUEST)
        except JobPost.DoesNotExist:
            return Response({'error': 'Job post not found'}, status=status.HTTP_404_NOT_FOUND)
class ListInterestedUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            job_post = JobPost.objects.get(pk=pk)
            if request.user != job_post.created_by:
                return Response({'error': 'You are not authorized to view this list'}, status=status.HTTP_403_FORBIDDEN)

            interests = UserInterest.objects.filter(job_post=job_post)
            serializer = UserInterestSerializer(interests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobPost.DoesNotExist:
            return Response({'error': 'Job post not found'}, status=status.HTTP_404_NOT_FOUND)

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            # Include other user fields if needed
        })
        
class JobPostDetailView(generics.RetrieveDestroyAPIView):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            return Response({'error': 'Job post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class ListInterestsView(generics.ListAPIView):
    serializer_class = UserInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return UserInterest.objects.filter(user=user)
    

class JobSeekerPostViewSet(viewsets.ModelViewSet):
    queryset = JobSeekerPost.objects.all()
    serializer_class = JobSeekerPostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        username = self.request.data.get('created_by')
        if username:
            try:
                user = User.objects.get(username=username)
                serializer.save(created_by=user)
            except User.DoesNotExist:
                return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        # Get the username from request headers
        request_username = request.headers.get('Username')
        if post.created_by.username != request_username:
            return Response({'error': 'You are not allowed to edit this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        # Get the username from request headers
        request_username = request.headers.get('Username')
        if post.created_by.username != request_username:
            return Response({'error': 'You are not allowed to delete this post.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(f"Serializer errors: {serializer.errors}")  # Debug output
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobSeekerPostListCreateView(generics.ListCreateAPIView):
    queryset = JobSeekerPost.objects.all()
    serializer_class = JobSeekerPostSerializer
    
class JobSeekerPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSeekerPost.objects.all()
    serializer_class = JobSeekerPostSerializer
    

logger = logging.getLogger(__name__)


# Set up the API with the token


import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text



def get_bot_response(user_message):
    user_message = user_message.lower()

    # ** Introduction **
    greetings = ["hello", "hi", "hey", "greetings", "what's up", "yo", "howdy", "help", "start"]
    if any(word in user_message for word in greetings):
        return ("Hello! I'm your job platform assistant. I'm here to help you with job postings, job seeker posts, user profiles, and more. "
                "You can ask me about job openings, job details, job seeker posts, or how to manage your account. How can I assist you today?")

    # ** Job Posts **
    if "job openings" in user_message or "available jobs" in user_message:
        jobs = JobPost.objects.all().order_by('-created_at')[:5]
        if jobs:
            job_list = ', '.join([job.title for job in jobs])
            return f"Here are some of the latest job openings: {job_list}. For more details, please visit our job board."
        return "There are currently no job openings available."

    if "job details" in user_message:
        job_title = user_message.replace("job details", "").strip()
        job = JobPost.objects.filter(title__icontains=job_title).first()
        if job:
            return (f"Job Title: {job.title}\nDescription: {job.description}\nLocation: {job.location}\n"
                    f"Company: {job.company}\nSalary: {job.salary}\nEmployment Type: {job.employment_type}\n"
                    f"Domain: {job.domain}\nExperience Level: {job.experience_level}\nJob Type: {job.job_type}\n"
                    f"Languages: {job.languages}\nSkills: {job.skills}")
        return "Sorry, I couldn't find any job details matching that description."

    if "search job" in user_message:
        keywords = user_message.replace("search job", "").strip()
        jobs = JobPost.objects.filter(title__icontains=keywords)[:5]
        if jobs:
            job_list = ', '.join([job.title for job in jobs])
            return f"Here are some jobs matching your search: {job_list}."
        return "No jobs found matching your search criteria."

    # ** Job Seeker Posts **
    if "job seeker posts" in user_message:
        posts = JobSeekerPost.objects.all().order_by('-created_at')[:5]
        if posts:
            post_list = ', '.join([post.title for post in posts])
            return f"Here are some of the latest job seeker posts: {post_list}. For more details, please visit our job board."
        return "There are currently no job seeker posts available."

    if "job seeker post details" in user_message:
        post_title = user_message.replace("job seeker post details", "").strip()
        post = JobSeekerPost.objects.filter(title__icontains=post_title).first()
        if post:
            return (f"Post Title: {post.title}\nDescription: {post.description}\nSkills: {post.skills}\n"
                    f"Experience Level: {post.experience_level}\nPreferred Location: {post.preferred_location}\n"
                    f"Employment Type: {post.employment_type}\nIndustry: {post.industry}\n"
                    f"Created By: {post.created_by.username}\nCreated At: {post.created_at.strftime('%Y-%m-%d')}")
        return "Sorry, I couldn't find any job seeker post details matching that description."

    # ** User Profiles **
    if "user profile" in user_message:
        username = user_message.replace("user profile", "").strip()
        user = User.objects.filter(username__icontains=username).first()
        if user:
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                return (f"Username: {user.username}\nCity: {profile.city}\nEducation: {profile.education}\n"
                        f"Experience: {profile.experience}\nSkills: {profile.skills}\nCertifications: {profile.certifications}\n"
                        f"Languages: {profile.languages}\nInterests: {profile.interests}")
            return "User profile found, but no additional details available."
        return "Sorry, I couldn't find any user profile matching that username."

    if "update profile" in user_message:
        return ("To update your profile, log in and go to the 'Profile' section. You can edit your personal information, resume, and other details.")

    if "create an account" in user_message or "register" in user_message:
        return ("To create an account, click on 'Sign Up' and provide the required information. You will then be able to post jobs, apply for jobs, and manage your profile.")

    if "delete an account" in user_message or "remove account" in user_message:
        return ("If you want to delete your account, please contact our support team at supportJobsOnline@example.com, and we will assist you with the process.")

    if "contact support" in user_message or "help" in user_message:
        return ("If you need assistance, you can contact our support team at supportJobsOnline@example.com. We're here to help!")

    if "privacy policy" in user_message or "terms of service" in user_message:
        return ("You can review our privacy policy and terms of service on our website under the 'Legal' section.")

    if "feedback" in user_message or "suggestions" in user_message:
        return ("We value your feedback! Please send your suggestions or comments to feedbackJobsOnline@yahoo.com.")

    return ("Sorry, I don't have information on that topic. Please visit our platform or contact our support team for more details.")

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            if not user_message:
                return JsonResponse({'error': 'No message provided.'}, status=400)

            # Obține răspunsul botului
            bot_response = get_bot_response(user_message)
            
            # Salvează conversația în baza de date
            Message.objects.create(user_message=user_message, bot_response=bot_response)
            
            return JsonResponse({'response': bot_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
     
        