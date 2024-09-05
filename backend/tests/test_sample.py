import os
import django
import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import JobPost, Message


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

class UserCreateTest(APITestCase):
    def test_create_user(self):
        url = reverse('user-create')
        data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class JobPostListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_job_post(self):
        url = reverse('jobpost-list-create')
        data = {
            'title': 'Test Job',
            'description': 'This is a test job description',
            'location': 'Remote',
            'salary': '5000',
            'employment_type': 'Full-time',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(JobPost.objects.count(), 1)
        self.assertEqual(JobPost.objects.get().title, 'Test Job')

    def test_list_job_posts(self):
        url = reverse('jobpost-list-create')
        JobPost.objects.create(title='Test Job 1', description='Description 1', location='Location 1', created_by=self.user)
        JobPost.objects.create(title='Test Job 2', description='Description 2', location='Location 2', created_by=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ChatbotViewTest(APITestCase):
    def test_chatbot_response(self):
        url = reverse('chatbot-view')
        data = {
            'message': 'hello'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Hello!', response.data['response'])

    def test_invalid_message(self):
        url = reverse('chatbot-view')
        data = {}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
