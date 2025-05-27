from django.contrib.auth.models import User
from django.db import models

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