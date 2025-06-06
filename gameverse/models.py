from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db import models

from django.utils import timezone
# Create your models here.
class User_Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'Normal User'),
        ('organizer', 'Event Organizer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # image = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    image = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    # @property
    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    timestamp = models.DateTimeField(default=now)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=250, default="No content")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contents
    

class Resources(models.Model):
    FILE_CHOICES = (
        ('Text', 'Text'),
        ('PDF', 'PDF'),
        ('Photo', 'Photo'),
        ('Video', 'Video'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    file_type = models.CharField(max_length=20, choices=FILE_CHOICES)
    text_content = models.TextField(blank=True, null=True)
    resource_file = models.FileField(upload_to='resources/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    date_uploaded = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.file_type} by {self.user.username if self.user else 'Unknown'}"
    

# Image Post (General post)
class OrganizerPost(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='organizer_posts/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Tournament Form Post
class TournamentFormPost(models.Model):
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    num_players_per_team = models.IntegerField()
    fields_required = models.JSONField(default=list)  # list of fields per player
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TournamentRegistration(models.Model):
    tournament = models.ForeignKey(TournamentFormPost, on_delete=models.CASCADE, related_name='tournamentregistration_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField()  # this will store the field data per player
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tournament.title}"
