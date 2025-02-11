from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from .utils import process_and_save_avatar
import logging
from django.conf import settings
from PIL import Image
from io import BytesIO
import boto3

logger = logging.getLogger(__name__)

def process_and_save_avatar(user, avatar_file):
    """Process and upload the avatar to S3, logging errors."""
    try:
        # Open and resize the image
        image = Image.open(avatar_file)
        image = image.resize((300, 300), Image.LANCZOS)

        # Save to S3
        image_io = BytesIO()
        file_extension = avatar_file.name.split('.')[-1].lower()
        file_format = "JPEG" if file_extension == "jpg" else file_extension.upper()
        image.save(image_io, format=file_format)

        user.avatar.save(f"avatars/{user.username}.{file_extension}", image_io, save=True)
        logger.info(f"✅ Avatar successfully uploaded to S3: {user.avatar.url}")

    except Exception as e:
        logger.error(f"🛑 Error uploading avatar to S3: {e}")
        raise

@login_required
def update_profile(request):
    """View to Update User Profile and Upload Avatar to AWS S3"""
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            # Process avatar if uploaded
            if 'avatar' in request.FILES:
                avatar_file = request.FILES['avatar']
                success = process_and_save_avatar(user, avatar_file)
                if not success:
                    messages.error(request, "Error processing avatar image.")

            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:update_profile')

    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'user/update_profile.html', {'form': form})

def register(request):
    """User Registration View with Avatar Upload to AWS S3"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Process avatar if uploaded
            if 'avatar' in request.FILES:
                avatar_file = request.FILES['avatar']
                success = process_and_save_avatar(user, avatar_file)
                if not success:
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