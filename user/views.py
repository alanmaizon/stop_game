from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from PIL import Image
from django.conf import settings
import os

def register(request):
    """User Registration View"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                image = Image.open(avatar)
                width, height = image.size
                min_dim = min(width, height)
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2
                image = image.crop((left, top, right, bottom))
                image = image.resize((300, 300), Image.Resampling.LANCZOS)
                avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars', avatar.name)
                image.save(avatar_path)
                user.avatar = os.path.join('avatars', avatar.name)
                user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('user:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def login_view(request):
    """User Login View"""
    if request.user.is_authenticated:
        return redirect('game:lobby')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('game:lobby')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

@login_required
def update_profile(request):
    """View to Update User Profile"""
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                image = Image.open(avatar)
                width, height = image.size
                min_dim = min(width, height)
                left = (width - min_dim) / 2
                top = (height - min_dim) / 2
                right = (width + min_dim) / 2
                bottom = (height + min_dim) / 2
                image = image.crop((left, top, right, bottom))
                image = image.resize((300, 300), Image.Resampling.LANCZOS)
                avatar_path = os.path.join(settings.MEDIA_ROOT, 'avatars', avatar.name)
                image.save(avatar_path)
                user.avatar = os.path.join('avatars', avatar.name)
                user.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:update_profile')
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request, 'user/update_profile.html', {'form': form})
