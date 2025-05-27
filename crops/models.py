from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    uses = models.TextField()
    growing_regions = models.TextField()
    climate = models.TextField()
    harvest_time = models.CharField(max_length=100)
    water_needs = models.CharField(max_length=100)
    sunlight = models.CharField(max_length=100)
    clipart = models.ImageField(upload_to='crop_cliparts/')

    def __str__(self):
        return self.name
