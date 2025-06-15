from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserCropForm
from main.models import UserCrop
from django.contrib.auth import logout
from TaskManager.models import Task
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from openai import OpenAI
from dotenv import load_dotenv
from .models import Profile
from .forms import EditProfileForm
import requests
from django.conf import settings
from decouple import config
from datetime import datetime, timedelta
from calendar import Calendar
from calendar import monthrange
from datetime import date
import calendar
from django.contrib.auth.views import LoginView

load_dotenv("./env")
client = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=os.getenv("GITHUB_TOKEN")
)
#openai.api_key = os.getenv("OPENAI_API_KEY")

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')  # default fallback
        else:
            return render(request, 'index.html', {'error': 'Invalid username or password'})

    return render(request, 'index.html')

# REGISTER VIEW
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken.'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered.'})

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'register.html')

@login_required
def add_user_crop(request):
    if request.method == 'POST':
        form = UserCropForm(request.POST, request.FILES)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.user = request.user
            crop.save()
            return redirect('crop_list')
    else:
        form = UserCropForm()
    return render(request, 'add_crop.html', {'form': form})

@login_required
def dashboard(request):
    user_crops = UserCrop.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)[:3]  # top 3 upcoming
    return render(request, 'dashboard.html', {
        'user_crops': user_crops,
        'tasks': tasks,
    })

@login_required
def layout_planning(request):
    return render(request, 'layout_planning.html')

@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

@csrf_exempt
@login_required
def ai_crop_assistant(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user_message = body.get('message', '')

        crops = UserCrop.objects.filter(user=request.user)
        crop_info = "\n".join([f"{c.name}: {c.harvest_time}, {c.region}" for c in crops])

        system_prompt = (
            "You are an AI crop assistant helping a farmer. "
            f"Here are the crops they grow:\n{crop_info}\n"
            "Now answer their question based on this."
        )

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an AI assistant for crops."},
                    {"role": "user", "content": user_message}
                ],
                temperature=1,
                max_tokens=1024,
                top_p=1
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"There was an error getting advice: {str(e)}"

        return JsonResponse({'response': answer})

# LANDING PAGE
def LandingPage(request):
    return render(request, 'LandingPage.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')  # default fallback
        else:
            return render(request, 'index.html', {'error': 'Invalid username or password'})

    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('login')  

@login_required
def toggle_darkmode(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.is_dark_mode = not profile.is_dark_mode
        profile.save()
    return redirect('profile')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return redirect('profile')
    else:
        form = EditProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'edit_profile.html', {
        'form': form,
    })

@login_required
def popular(request):
    return render(request, 'coming_soon.html', {'section': 'Popular'})

@login_required
def trending(request):
    return render(request, 'coming_soon.html', {'section': 'Trending'})

@login_required
def today(request):
    return render(request, 'coming_soon.html', {'section': 'Today'})

@login_required
def favourite(request):
    return render(request, 'coming_soon.html', {'section': 'Favourite'})

@login_required
def download(request):
    return render(request, 'coming_soon.html', {'section': 'Download'})

API_KEY = config('OPENWEATHER_API_KEY')  # stored in .env
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def weather_view(request):
    city = request.GET.get('city', 'Brisbane,AU')

    # Use metric units for Celsius
    current_url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    current_res = requests.get(current_url).json()

    forecast_url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    forecast_res = requests.get(forecast_url).json()

    context = {
        'city': current_res['name'],
        'country': current_res['sys']['country'],
        'date': datetime.now().strftime('%A, %B %d, %Y at %I:%M %p'),
        'temperature': round(current_res['main']['temp']),
        'feels_like': round(current_res['main']['feels_like']),
        'description': current_res['weather'][0]['description'].title(),
        'icon': current_res['weather'][0]['icon'],
        'temp_max': round(current_res['main']['temp_max']),
        'temp_min': round(current_res['main']['temp_min']),
        'humidity': current_res['main']['humidity'],
        'wind': round(current_res['wind']['speed']),
        'forecast': []
    }

    # Grab one forecast per day
    seen_days = set()
    for item in forecast_res['list']:
        day = datetime.fromtimestamp(item['dt']).strftime('%A')
        if day not in seen_days:
            seen_days.add(day)
            context['forecast'].append({
                'day': day,
                'temp_max': round(item['main']['temp_max']),
                'temp_min': round(item['main']['temp_min']),
                'description': item['weather'][0]['description'].title(),
                'icon': item['weather'][0]['icon']
            })
        if len(context['forecast']) == 5:
            break

    return render(request, 'weather.html', context)

def calendar_view(request):
    today = date.today()
    year, month = today.year, today.month

    # Get month calendar as a list of weeks (each week is a list of 7 ints)
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)

    day_headers = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    context = {
        'current_month': today.strftime("%B %Y"),
        'calendar_data': month_days,
        'day_headers': day_headers,
        'today': today.day
    }

    return render(request, 'calendar.html', context)

def date_detail(request, year, month, day):
    selected_date = datetime(year, month, day)
    return render(request, 'date_detail.html', {'selected_date': selected_date})