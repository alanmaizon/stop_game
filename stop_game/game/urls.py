from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('start/', views.start_game, name='start'),
    path('submit/<int:round_id>/', views.submit_words, name='submit'),
    path('results/<int:round_id>/', views.show_results, name='results'),
    path('stop/<int:round_id>/', views.stop_round, name='stop_round'),
]
