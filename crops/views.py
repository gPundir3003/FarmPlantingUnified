from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Crop
from main.forms import UserCropForm  # Make sure the form is in crops/forms.py
from main.models import UserCrop
from django.shortcuts import render, redirect

@login_required
def crop_list(request):  
    crops = Crop.objects.all()
    return render(request, 'crop_list.html', {'crops': crops})

@login_required
def crop_detail(request, id):
    crop = get_object_or_404(Crop, id=id)
    return render(request, 'crop_detail.html', {'crop': crop})

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