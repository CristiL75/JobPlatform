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

    def post(self, request, format=None):
        # Get current user's profile
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