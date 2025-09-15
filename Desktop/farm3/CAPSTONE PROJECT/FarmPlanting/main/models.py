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
