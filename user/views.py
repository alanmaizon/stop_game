from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    """User Registration View"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:update_profile')
    else:
        form = UserProfileUpdateForm(instance=user)
    return render(request, 'user/update_profile.html', {'form': form})
