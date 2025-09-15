# main/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.utils import timezone

from .models import Notification, Task, Profile, UserCrop
from .forms import EditProfileForm, UserCropForm

import os, json, requests, calendar
from datetime import datetime, date
from decouple import config
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# Auth
# -----------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            return redirect(next_url or 'dashboard')
        return render(request, 'index.html', {'error': 'Invalid username or password'})
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        password = request.POST.get('password')
        confirm  = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered.'})
        if password != confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------
# Dashboard — shows planner tasks
# -----------------------------
@login_required
def dashboard(request):
    user_crops = UserCrop.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)

    now = timezone.now().date()
    for t in tasks:
        if t.date:
            formatted_date = t.date.strftime("%d %b %Y")   
            formatted_time = t.time if t.time else "unspecified time"

            if t.date == now:
                if not Notification.objects.filter(
                    title="📅 Task Due Today", message__icontains=t.description
                ).exists():
                    Notification.objects.create(
                        user=request.user,
                        title="📅 Task Due Today",
                        message=f"Task '{t.description}' is due today ({formatted_date}, {formatted_time})."
                    )
            elif t.date < now:
                if not Notification.objects.filter(
                    title="⚠️ Overdue Task", message__icontains=t.description
                ).exists():
                    Notification.objects.create(
                        user=request.user,
                        title="⚠️ Overdue Task",
                        message=f"Task '{t.description}' was due on {formatted_date} at {formatted_time}. Please update it."
                    )

    unread_notifications = Notification.objects.filter(user=request.user, read=False).count()

    return render(request, "dashboard.html", {
        "tasks": tasks,
        "user_crops": user_crops,
        "unread_notifications": unread_notifications,
    })


# -----------------------------
# Calendar helpers + page
# -----------------------------
def _shift_month(y, m, delta):
    m2 = m + delta
    y += (m2 - 1) // 12
    m2 = (m2 - 1) % 12 + 1
    return y, m2


@login_required
def calendar_view(request):
    today = date.today()
    try:
        y = int(request.GET.get('y', today.year))
    except (TypeError, ValueError):
        y = today.year
    try:
        m = int(request.GET.get('m', today.month))
    except (TypeError, ValueError):
        m = today.month

    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(y, m)
    prev_year, prev_month = _shift_month(y, m, -1)
    next_year, next_month = _shift_month(y, m, +1)

    context = {
        "current_month": f"{calendar.month_name[m]} {y}",
        "calendar_data": month_days,
        "day_headers": ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
        "today": today.day if (y == today.year and m == today.month) else 0,
        "prev_year": prev_year, "prev_month": prev_month,
        "next_year": next_year, "next_month": next_month,
        "tasks_by_day": {},
        "view_year": y, "view_month": m,
    }
    return render(request, "calendar.html", context)


# -----------------------------
# Planner <-> DB APIs
# -----------------------------
@login_required
@require_http_methods(["GET"])
def tasks_by_day_api(request):
    try:
        y = int(request.GET.get("y"))
        m = int(request.GET.get("m"))
        d = int(request.GET.get("d"))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Bad params")

    qs = (Task.objects
          .filter(user=request.user, date=date(y, m, d))
          .order_by("time", "id")
          .values("id", "time", "description", "is_done", "notes"))
    return JsonResponse({"ok": True, "tasks": list(qs)})


@login_required
@require_POST
def add_task_api(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        y   = int(payload.get("year"))
        m   = int(payload.get("month"))
        d   = int(payload.get("day"))
        t   = (payload.get("time") or "").strip()
        desc = (payload.get("description") or "").strip()
        if not (y and m and d and desc):
            return HttpResponseBadRequest("Missing fields")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    obj = Task.objects.create(user=request.user, date=date(y, m, d), time=t, description=desc)
    return JsonResponse({"ok": True,
                         "task": {"id": obj.id, "time": obj.time, "description": obj.description}}, status=201)


@login_required
@require_POST
def toggle_task(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        tid = int(payload.get("id"))
        is_done = bool(payload.get("is_done"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    updated = Task.objects.filter(user=request.user, pk=tid).update(is_done=is_done)
    if updated == 0:
        return HttpResponseBadRequest("Task not found")
    return JsonResponse({"ok": True})


@login_required
@require_POST
def update_task(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        tid = int(payload.get("id"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    try:
        task = Task.objects.get(user=request.user, pk=tid)
    except Task.DoesNotExist:
        return HttpResponseBadRequest("Task not found")

    if payload.get("date"):
        try:
            y, m, d = str(payload["date"]).split("-")
            task.date = date(int(y), int(m), int(d))
        except Exception:
            return HttpResponseBadRequest("Bad date")

    if "time" in payload:
        task.time = (payload.get("time") or "").strip()
    if "description" in payload:
        task.description = (payload.get("description") or "").strip()
    if "notes" in payload:
        task.notes = (payload.get("notes") or "").strip()

    task.save()
    out = {
        "id": task.id,
        "date": task.date.isoformat(),
        "time": task.time,
        "description": task.description,
        "is_done": task.is_done,
        "notes": task.notes or "",
    }
    return JsonResponse({"ok": True, "task": out})


@login_required
@require_POST
def delete_task(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        tid = int(payload.get("id"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    deleted, _ = Task.objects.filter(user=request.user, pk=tid).delete()
    if not deleted:
        return HttpResponseBadRequest("Task not found")
    return JsonResponse({"ok": True})


@login_required
def tasks_all_json(request):
    qs = (Task.objects
          .filter(user=request.user)
          .order_by("date", "time", "id")
          .values("id", "date", "time", "description", "is_done", "notes"))
    data = [{
        "id": t["id"],
        "date": t["date"].isoformat(),
        "time": t["time"],
        "description": t["description"],
        "is_done": t["is_done"],
        "notes": t["notes"] or "",
    } for t in qs]
    return JsonResponse({"ok": True, "tasks": data})


@login_required
def date_detail(request, year, month, day):
    try:
        selected = date(year, month, day)
    except ValueError:
        return HttpResponseBadRequest("Invalid date")
    tasks = Task.objects.filter(user=request.user, date=selected).order_by("time", "id")
    return render(request, "date_detail.html", {"selected_date": selected, "tasks": tasks})


# -----------------------------
# Misc pages
# -----------------------------
@login_required
def layout_planning(request):
    return render(request, 'layout_planning.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

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
            request.user.last_name  = form.cleaned_data['last_name']
            request.user.email      = form.cleaned_data['email']
            request.user.save()
            return redirect('profile')
    else:
        form = EditProfileForm(initial={
            'first_name': request.user.first_name,
            'last_name' : request.user.last_name,
            'email'     : request.user.email,
        })
    return render(request, 'edit_profile.html', {'form': form})

def LandingPage(request):
    return render(request, 'LandingPage.html')

@login_required
def popular(request):   return render(request, 'coming_soon.html', {'section': 'Popular'})
@login_required
def trending(request):  return render(request, 'coming_soon.html', {'section': 'Trending'})
@login_required
def today(request):     return render(request, 'coming_soon.html', {'section': 'Today'})
@login_required
def favourite(request): return render(request, 'coming_soon.html', {'section': 'Favourite'})
@login_required
def download(request):  return render(request, 'coming_soon.html', {'section': 'Download'})


# -----------------------------
# Weather
# -----------------------------
API_KEY = config('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5/"

def weather_view(request):
    city = request.GET.get('city', 'Brisbane,AU')

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
    
    # ----------------------------
    # 🔔 Notification logic
    # ----------------------------
    weather_desc = current_res['weather'][0]['description'].lower()
    temp = round(current_res['main']['temp'])

    if "thunderstorm" in weather_desc:
        if not Notification.objects.filter(title="⚡ Thunderstorm Alert", message__icontains=weather_desc).exists():
            Notification.objects.create(
                user=request.user,
                title="⚡ Thunderstorm Alert",
                message=f"A thunderstorm is expected in {city}. Stay safe!"
            )

    elif "rain" in weather_desc:
        if not Notification.objects.filter(title="🌧 Rain Alert", message__icontains=weather_desc).exists():
            Notification.objects.create(
                user=request.user,
                title="🌧 Rain Alert",
                message=f"Rainfall detected in {city}. Protect your crops."
            )

    elif temp > 35:
        if not Notification.objects.filter(title="🔥 Heatwave Alert").exists():
            Notification.objects.create(
                user=request.user,
                title="🔥 Heatwave Alert",
                message=f"Extreme heat detected in {city} ({temp}°C). Take precautions!"
            )

    return render(request, 'weather.html', context)


# -----------------------------
# AI crop assistant
# -----------------------------
@csrf_exempt
@login_required
def ai_crop_assistant(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("POST only")
    try:
        body = json.loads(request.body)
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    user_message = body.get('message', '')
    crops = UserCrop.objects.filter(user=request.user)
    crop_info = "\n".join([f"{c.name}: {c.harvest_time}, {c.region}" for c in crops])

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


# -----------------------------
# Notifications
# -----------------------------
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-date_created") 
    
    # mark all as read
    notifications.update(read=True)

    return render(request, "notifications.html", {"notifications": notifications})
