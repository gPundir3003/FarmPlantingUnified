from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from main import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("notifications/", views.notifications_view, name="notifications"),
    path('add_task/', views.add_task_api, name='add_task'),
    path("api/task/delete/",  views.delete_task,  name="delete_task"),
    path("api/tasks/add/", views.add_task_api,  name="add_task_api"),
    path("api/tasks/day/", views.tasks_by_day_api, name="tasks_by_day_api"),
    path("api/tasks/all/", views.tasks_all_json, name="tasks_all_json"),
    path("api/task/toggle/", views.toggle_task, name= "toggle_task"),
    path("api/task/update/", views.update_task, name="update_task"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_view, name='logout'),
    path("login/", views.login_view, name="login"),
    path('calendar/', views.calendar_view, name='calendar'),
    path("tasks/add/", views.add_task_api, name="tasks_add"),
    path("tasks/by-day/", views.tasks_by_day_api, name="tasks_by_day_api"),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.date_detail, name='calendar_day'),
    path("weather/", views.weather_view, name="weather"),
    path('popular/', views.popular, name='popular'),
    path('trending/', views.trending, name='trending'),
    path('today/', views.today, name='today'),
    path('favourite/', views.favourite, name='favourite'),
    path('download/', views.download, name='download'),
    path('toggle-darkmode/', views.toggle_darkmode, name='toggle_darkmode'),
    path('', views.dashboard, name='dashboard'),  # or your main view
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path("ai-crop-assistant/", views.ai_crop_assistant, name="ai_crop_assistant"),
    path("layout-planning/", views.layout_planning, name="layout_planning"),
]
