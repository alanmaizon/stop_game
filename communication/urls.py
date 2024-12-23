from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('submit-word/', views.submit_word, name='submit_word'),
    path('review-submissions/', views.review_submissions, name='review_submissions'),
    path('approve-submission/<int:submission_id>/', views.approve_submission, name='approve_submission'),
    path('reject-submission/<int:submission_id>/', views.reject_submission, name='reject_submission'),
]
