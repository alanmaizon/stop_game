from django.shortcuts import render
from django.shortcuts import redirect

def home_page(request):
    """Home Page View"""
    if request.user.is_authenticated:
        return redirect('game:lobby')
    return render(request, 'core/index.html')
