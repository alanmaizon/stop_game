from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from communication.models import WordSubmission, Notification
from communication.forms import WordSubmissionForm
from django.contrib import messages

@login_required
def notifications_with_archived(request):
    """Combined view for notifications and archived notifications."""
    notifications = Notification.objects.filter(player=request.user, is_archived=False).order_by('-created_at')
    archived_notifications = Notification.objects.filter(player=request.user, is_archived=True).order_by('-created_at')
    return render(request, 'inbox/notifications_with_archived.html', {
        'notifications': notifications,
        'archived_notifications': archived_notifications,
    })

@login_required
def submissions_with_submit(request):
    """Combined view for My Submissions and Submit Word."""
    if request.method == 'POST':
        form = WordSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.player = request.user
            submission.save()
            messages.success(request, 'Your word has been submitted for review!')
            return redirect(f'{request.path}?tab=submissions')
    else:
        form = WordSubmissionForm()

    submissions = WordSubmission.objects.filter(player=request.user)
    return render(request, 'inbox/submissions_with_submit.html', {
        'form': form,
        'submissions': submissions,
    })

@login_required
def notifications_list(request):
    """Player's notifications inbox."""
    notifications = Notification.objects.filter(player=request.user, is_archived=False).order_by('-created_at')
    return render(request, 'inbox/notifications_list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    """Mark a notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, player=request.user)
    notification.is_read = True
    notification.save()
    return redirect('inbox:notifications_list')

@login_required
def archive_notification(request, notification_id):
    """Archive a notification."""
    notification = get_object_or_404(Notification, id=notification_id, player=request.user, is_read=True)
    notification.is_archived = True
    notification.save()
    return redirect('inbox:notifications_list')

@login_required
def archived_notifications(request):
    """View archived notifications."""
    archived_notifications = Notification.objects.filter(player=request.user, is_archived=True).order_by('-created_at')
    return render(request, 'inbox/archived_notifications.html', {'notifications': archived_notifications})
