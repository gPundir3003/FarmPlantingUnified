from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserCropForm
from main.models import UserCrop
from TaskManager.models import Task
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from openai import OpenAI
from dotenv import load_dotenv


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
