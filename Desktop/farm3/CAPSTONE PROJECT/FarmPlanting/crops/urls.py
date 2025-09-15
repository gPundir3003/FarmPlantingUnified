from django.urls import path
from . import views

urlpatterns = [
    path('', views.crop_list, name='crop_list'),
    path('<int:id>/', views.crop_detail, name='crop_detail'),
    path('add/', views.add_user_crop, name='add_crop'),
]
