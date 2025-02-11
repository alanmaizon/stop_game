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
from django.http import JsonResponse
import cloudinary.uploader

logger = logging.getLogger(__name__)


def process_and_save_avatar(user, avatar_file):
    """Process and upload the avatar to Cloudinary."""
    try:
        # Open and resize the image
        image = Image.open(avatar_file)
        image = image.resize((300, 300), Image.LANCZOS)

        # Save to an in-memory file
        image_io = BytesIO()
        file_extension = avatar_file.name.split('.')[-1].lower()
        file_format = "JPEG" if file_extension == "jpg" else file_extension.upper()
        image.save(image_io, format=file_format)
        image_io.seek(0)

        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            image_io,
            folder="avatars",
            public_id=user.username,  # Use username as the Cloudinary public ID
            overwrite=True,
            resource_type="image"
        )

        # Save Cloudinary URL to user model
        user.avatar = response['secure_url']
        user.save()
        
        logger.info(f"✅ Avatar successfully uploaded to Cloudinary: {response['secure_url']}")
        return True  # Indicate success

    except Exception as e:
        logger.error(f"🛑 Error uploading avatar to Cloudinary: {e}")
        return False  # Indicate failure


@login_required
def update_profile(request):
    """Update profile and upload avatar to Cloudinary"""
    user = request.user
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if 'avatar' in request.FILES:
                avatar_file = request.FILES['avatar']
                try:
                    response = cloudinary.uploader.upload(
                        avatar_file,
                        folder="avatars",
                        public_id=user.username,  # Unique naming
                        overwrite=True
                    )
                    logger.info(f"✅ Cloudinary Upload Success: {response}")  # Debug log
                    user.avatar = response.get('secure_url', '')  # Save Cloudinary URL
                    user.save()
                except Exception as e:
                    logger.error(f"🛑 Cloudinary Upload Failed: {e}")
                    messages.error(request, "Avatar upload failed. Please try again.")

            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:update_profile')

    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, 'user/update_profile.html', {'form': form})

def register(request):
    """User Registration View with Avatar Upload to Cloudinary"""
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