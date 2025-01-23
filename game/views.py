from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from communication.models import WordSubmission
from .models import Category, Round, Submission, Player, ValidAnswer
import logging

logger = logging.getLogger(__name__)

from django.db.models import Sum, Count

@login_required
def lobby(request):
    """Display the multiplayer lobby with player rankings."""
    # Query all players ordered by score
    players = Player.objects.all().order_by('-score')

    # Calculate points awarded using WordSubmission
    player_points = {
        player.id: WordSubmission.objects.filter(player=player.user)  # Use player.user for User instance
            .aggregate(total_points=Sum('points_awarded'))['total_points'] or 0
        for player in players
    }

    # Calculate games played as the count of unique rounds the player has participated in
    player_games_played = {
        player.id: Submission.objects.filter(player=player).values('round').distinct().count()
        for player in players
    }

    # Create ranked players list
    ranked_players = [
        {
            'rank': rank,
            'player': player,
            'points_awarded': player_points[player.id],
            'games_played': player_games_played[player.id],
        }
        for rank, player in enumerate(players, start=1)
    ]

    # Paginate results
    paginator = Paginator(ranked_players, 10)  # Show 10 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'game/lobby.html', context)


def is_valid_word(word, round_letter, category_name):
    """Validate the word against the ValidAnswer table."""
    word = word.strip().lower()
    logger.debug(f"Validating word: {word}, Round Letter: {round_letter}, Category: {category_name}")

    if not word.startswith(round_letter.lower()):
        logger.debug("Validation failed: Word does not start with the required letter.")
        return False, "Word does not start with the required letter."

    valid_in_category = ValidAnswer.objects.filter(
        category__name=category_name,
        word=word
    ).exists()

    logger.debug(f"Validation result for '{word}': {valid_in_category}")
    if not valid_in_category:
        return False, f"Word is not a valid {category_name.lower()}."

    return True, "Valid word."


@login_required
def submit_words(request, round_id):
    """Submit words for a round and validate them."""
    if request.method == 'POST':
        round_obj = get_object_or_404(Round, id=round_id)
        player, _ = Player.objects.get_or_create(user=request.user)
        categories = Category.objects.all()

        for category in categories:
            word = request.POST.get(f'category_{category.id}')
            if word:
                is_valid, reason = is_valid_word(word, round_obj.letter, category.name)
                logger.debug(f"Word: {word}, Is Valid: {is_valid}, Reason: {reason}")

                Submission.objects.create(
                    player=player,
                    round=round_obj,
                    category=category,
                    word=word.capitalize(),
                    is_valid=is_valid,
                    validation_message=reason
                )
        return redirect('game:results', round_id=round_obj.id)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def start_game(request):
    """Start a new round with a random letter."""
    letter = Round.generate_letter()
    round_obj = Round.objects.create(letter=letter)
    categories = Category.objects.all()
    return render(request, 'game/start.html', {
        'round': round_obj,
        'letter': letter,
        'categories': categories,
        'round_time': 60,
    })


@login_required
def stop_round(request, round_id):
    """Stop a round and redirect to results."""
    round_obj = get_object_or_404(Round, id=round_id)
    round_obj.is_active = False
    round_obj.save()
    return redirect('game:results', round_id=round_id)


@login_required
def show_results(request, round_id):
    """Display results for a specific round."""
    round_obj = get_object_or_404(Round, id=round_id)
    submissions = Submission.objects.filter(round=round_obj).select_related('player', 'category')
    player = submissions.first().player if submissions.exists() else None

    player_score = 0
    all_correct = True

    for category in Category.objects.all():
        player_words = submissions.filter(player=player, category=category)
        if player_words.exists():
            word = player_words.first().word
            if submissions.filter(category=category, word=word, is_valid=True).count() == 1:
                player_score += 10
            else:
                all_correct = False
        else:
            all_correct = False

    if all_correct:
        player_score *= 2

    if player and not submissions.filter(score_calculated=True).exists():
        player.score += player_score
        player.save()
        submissions.update(score_calculated=True)

    return render(request, 'game/results.html', {
        'round': round_obj,
        'player_score': player_score,
        'all_correct': all_correct,
        'submissions': submissions,
        'player': player,
    })
