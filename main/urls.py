from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/<int:day>/', views.date_detail, name='calendar_day'),
    path("weather/", views.weather_view, name="weather"),
    path('popular/', views.popular, name='popular'),
    path('trending/', views.trending, name='trending'),
    path('today/', views.today, name='today'),
    path('favourite/', views.favourite, name='favourite'),
    path('download/', views.download, name='download'),
    path('toggle-darkmode/', views.toggle_darkmode, name='toggle_darkmode'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.dashboard, name='dashboard'),  # or your main view
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
