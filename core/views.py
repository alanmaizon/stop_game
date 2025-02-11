from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings

def home_page(request):
    """Home Page View"""
    if request.user.is_authenticated:
        return redirect('game:lobby')
    return render(request, 'core/index.html')

def debug_static_media(request):
    return JsonResponse({
        "DEBUG": settings.DEBUG,
        "STATIC_URL": settings.STATIC_URL,
        "STATIC_ROOT": settings.STATIC_ROOT,
        "MEDIA_URL": settings.MEDIA_URL,
        "MEDIA_ROOT": settings.MEDIA_ROOT,
        "STATICFILES_DIRS": settings.STATICFILES_DIRS if hasattr(settings, 'STATICFILES_DIRS') else None,
    })
