from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from PIL import Image
from django.conf import settings
import os
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

def register(request):
    """User Registration View with Avatar Upload to AWS S3"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Check if an avatar was uploaded
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']

                try:
                    # Open the image
                    image = Image.open(avatar)

                    # Crop to square
                    width, height = image.size
                    min_dim = min(width, height)
                    left = (width - min_dim) / 2
                    top = (height - min_dim) / 2
                    right = (width + min_dim) / 2
                    bottom = (height + min_dim) / 2
                    image = image.crop((left, top, right, bottom))

                    # Resize to 300x300
                    image = image.resize((300, 300), Image.Resampling.LANCZOS)

                    # Save image to S3 (in memory)
                    image_io = BytesIO()
                    file_extension = avatar.name.split('.')[-1].lower()
                    file_format = "JPEG" if file_extension == "jpg" else file_extension.upper()
                    image.save(image_io, format=file_format)

                    # Save directly to S3 using Django's ImageField
                    user.avatar.save(f"avatars/{user.username}.{file_extension}", image_io, save=True)

                    logger.info(f"Avatar successfully uploaded to S3 for user: {user.username}")

                except Exception as e:
                    logger.error(f"Error processing avatar: {e}")
                    messages.error(request, "Error processing avatar image.")

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
    """View to Update User Profile and Upload Avatar to AWS S3"""
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Check if an avatar was uploaded
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']

                try:
                    # Open the image
                    image = Image.open(avatar)

                    # Crop to square
                    width, height = image.size
                    min_dim = min(width, height)
                    left = (width - min_dim) / 2
                    top = (height - min_dim) / 2
                    right = (width + min_dim) / 2
                    bottom = (height + min_dim) / 2
                    image = image.crop((left, top, right, bottom))

                    # Resize to 300x300
                    image = image.resize((300, 300), Image.Resampling.LANCZOS)

                    # Save image to S3 (in memory)
                    image_io = BytesIO()
                    file_extension = avatar.name.split('.')[-1].lower()
                    file_format = "JPEG" if file_extension == "jpg" else file_extension.upper()
                    image.save(image_io, format=file_format)

                    # Save directly to S3 via Django ImageField
                    user.avatar.save(f"avatars/{user.username}.{file_extension}", image_io, save=True)

                    logger.info(f"Avatar successfully uploaded to S3 for user: {user.username}")

                except Exception as e:
                    logger.error(f"Error processing avatar: {e}")
                    messages.error(request, "Error processing avatar image.")

            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:update_profile')

    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'user/update_profile.html', {'form': form})