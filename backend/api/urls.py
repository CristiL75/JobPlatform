# urls.py

from django.urls import path
from .views import UserCreate, UserProfileView
from .views import JobPostListCreateView
from .views import ShowInterestView, ListInterestedUsers
from .views import CurrentUserView, JobPostDetailView

urlpatterns = [
    path('user/create/', UserCreate.as_view(), name='user-create'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile-self'),  # For accessing current user's profile
    path('user/profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),  # For accessing other users' profiles  # Updated to include username
    path('job-posts/', JobPostListCreateView.as_view(), name='job-post-list-create'),
    path('job-posts/create/', JobPostListCreateView.as_view(), name='job-post-create'),
    path('job-posts/<int:pk>/interested/', ShowInterestView.as_view(), name='show_interest'),
    path('job-posts/<int:pk>/interested/users/', ListInterestedUsers.as_view(), name='list_interested_users'),
    path('job-posts/<int:pk>/', JobPostDetailView.as_view(), name='job-post-detail'), # Updated path

]