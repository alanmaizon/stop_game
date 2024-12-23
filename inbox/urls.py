from django.urls import path
from . import views

app_name = 'inbox'

urlpatterns = [
    path('notifications-with-archived/', views.notifications_with_archived, name='notifications_with_archived'),
    path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/archive/<int:notification_id>/', views.archive_notification, name='archive_notification'),
    path('submissions-with-submit/', views.submissions_with_submit, name='submissions_with_submit'),
]
