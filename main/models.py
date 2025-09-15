from django.contrib.auth.models import User
from django.db import models

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)  # To check if it's read by the user

    def __str__(self):
        return self.title
    
class UserCrop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_planted = models.DateField()
    region = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='user_crops/')

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_dark_mode = models.BooleanField(default=False)
    wifi_only = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="main_tasks", null=True, blank=True)
    date = models.DateField()
    time = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time", "id"]

    def __str__(self):
        return f"{self.date} {self.time} - {self.description}"