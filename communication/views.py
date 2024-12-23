from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import WordSubmissionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import WordSubmission, Notification
from game.models import ValidAnswer, Player

@staff_member_required
def review_submissions(request):
    """Admin reviews player submissions."""
    submissions = WordSubmission.objects.filter(status='pending')
    return render(request, 'communication/review_submissions.html', {'submissions': submissions})

@staff_member_required
def approve_submission(request, submission_id):
    """Admin approves a player submission."""
    submission = get_object_or_404(WordSubmission, id=submission_id)
    submission.status = 'approved'
    submission.points_awarded = 10  # Example points adjustment
    submission.save()

    # Add word to ValidAnswer
    ValidAnswer.objects.create(category=submission.category, word=submission.word.lower())

    # Update player's score
    player = Player.objects.get(user=submission.player)
    player.score += submission.points_awarded
    player.save()

    # Notify player
    Notification.objects.create(
        player=submission.player,
        message=f"Your word '{submission.word}' has been approved, and you were awarded {submission.points_awarded} points!"
    )

    return redirect('communication:review_submissions')

@staff_member_required
def reject_submission(request, submission_id):
    """Admin rejects a player submission."""
    submission = get_object_or_404(WordSubmission, id=submission_id)
    submission.status = 'rejected'
    submission.feedback = request.POST.get('feedback', 'Your submission was not approved.')
    submission.save()

    # Notify player
    Notification.objects.create(
        player=submission.player,
        message=f"Your word '{submission.word}' has been rejected. Reason: {submission.feedback}"
    )

    return redirect('communication:review_submissions')

@login_required
def submit_word(request):
    """Player submits a word for review."""
    if request.method == 'POST':
        form = WordSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.player = request.user
            submission.save()
            messages.success(request, 'Your submission has been sent for review!')
            return redirect(f'{request.path}?tab=submissions')
    else:
        form = WordSubmissionForm()
    submissions = WordSubmission.objects.filter(player=request.user)
    
    return render(request, 'inbox/submissions_with_submit.html', {
        'form': form,
        'submissions': submissions,
    })
