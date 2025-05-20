from django.contrib import admin
from .models import Crop
from main.models import UserCrop

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'growing_regions']

admin.site.register(UserCrop)
