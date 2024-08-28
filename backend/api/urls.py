# urls.py

from django.urls import path
from .views import UserCreate, UserProfileView
from .views import JobPostListCreateView
from .views import ShowInterestView, ListInterestedUsers
from .views import CurrentUserView, JobPostDetailView, ShowInterestView, ListInterestsView

urlpatterns = [
    path('user/create/', UserCreate.as_view(), name='user-create'),
    path('user/profile/', UserProfileView.as_view(), name='user-profile-self'),
    path('user/profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('job-posts/', JobPostListCreateView.as_view(), name='job-post-list-create'),
    path('job-posts/<int:pk>/interest/', ShowInterestView.as_view(), name='show-interest'),
    path('job-posts/<int:pk>/interested/users/', ListInterestedUsers.as_view(), name='list-interested-users'),
    path('job-posts/<int:pk>/', JobPostDetailView.as_view(), name='job-post-detail'),
]