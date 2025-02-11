from django.urls import path
from .views import home_page, debug_static_media

urlpatterns = [
    path('', home_page, name='home'),
    path("debug-static/", debug_static_media),
]
