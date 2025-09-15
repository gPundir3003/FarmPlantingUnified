
from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static
from main.views import profile_view

urlpatterns = [
    path('main/', include('main.urls')),
    path('', views.LandingPage, name='LandingPage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
    path('', views.LandingPage, name='LandingPage'),  
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('crops/', include('crops.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('layout-planning/', views.layout_planning, name='layout_planning'),
    path('calendar/', views.calendar_view, name='calendar'),
    path("ai-assistant/", views.ai_crop_assistant, name="ai_crop_assistant"),

    
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
