from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cv_pdf = models.FileField(upload_to='cvs/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    languages = models.TextField(blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Ensure this line exists

    def __str__(self):
        return self.user.username
    
class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    company = models.CharField(max_length=255, default='Unknown')  # Provide default
    salary = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    experience_level = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    languages = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.interested_user.username} is interested in {self.job_post.title}"
    
    
    

class JobSeekerPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.CharField(max_length=500)  # Consider ManyToManyField for multiple skills
    experience_level = models.CharField(max_length=50, choices=[
        ('Junior', 'Junior'),
        ('Mid-Level', 'Mid-Level'),
        ('Senior', 'Senior'),
    ])
    preferred_location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=50, choices=[
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Freelance', 'Freelance'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    ])
    industry = models.CharField(max_length=100)  # Consider choices if predefined
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title
    
    

class Message(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"