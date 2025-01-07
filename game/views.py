from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Category, Round, Submission, Player, ValidAnswer
from django.contrib.auth.decorators import login_required
from communication.models import WordSubmission
from django.db.models import Count, Sum
import requests
import logging

logger = logging.getLogger(__name__)

from django.core.paginator import Paginator

@login_required
def lobby(request):
    players = Player.objects.all().order_by('-score')
    player_points = {player.id: Submission.objects.filter(player=player).aggregate(Sum('score_calculated'))['score_calculated__sum'] or 0 for player in players}
    player_games_played = {player.id: Submission.objects.filter(player=player).values('round').distinct().count() for player in players}

    ranked_players = []
    for rank, player in enumerate(players, start=1):
        ranked_players.append({
            'rank': rank,
            'player': player,
            'points_awarded': player_points[player.id],
            'games_played': player_games_played[player.id]
        })

    paginator = Paginator(ranked_players, 10)  # Show 10 players per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'game/lobby.html', context)

@login_required
def is_valid_word(word, round_letter, category_name):
    """Validate the word against the ValidAnswer table."""
    word = word.strip().lower()

    # Debug: Log inputs
    logger.debug(f"Validating word: {word}, Round Letter: {round_letter}, Category: {category_name}")

    # Check if the word starts with the required letter
    if not word.startswith(round_letter.lower()):
        logger.debug("Validation failed: Word does not start with the required letter.")
        return False, "Word does not start with the required letter."

    # Check if the word exists in the ValidAnswer table for the category
    valid_in_category = ValidAnswer.objects.filter(
        category__name=category_name,  # Match category name
        word=word                     # Match word
    ).exists()

    # Debug: Log query result
    logger.debug(f"Query result for word '{word}' in category '{category_name}': {valid_in_category}")

    if not valid_in_category:
        logger.debug(f"Validation failed: Word '{word}' is not a valid {category_name.lower()}.")
        return False, f"Word is not a valid {category_name.lower()}."

    logger.debug(f"Validation passed for word: {word}")
    return True, "Valid word."

@login_required
def submit_words(request, round_id):
    """Submit words and validate them."""
    if request.method == 'POST':
        round_obj = Round.objects.get(id=round_id)
        player, _ = Player.objects.get_or_create(user=request.user)
        categories = Category.objects.all()

        for category in categories:
            word = request.POST.get(f'category_{category.id}')
            if word:
                is_valid, reason = is_valid_word(word, round_obj.letter, category.name)

                # Debug: Log validation result
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
    round_time = 60
    return render(request, 'game/start.html', {
        'round': round_obj,
        'letter': letter,
        'categories': categories,
        'round_time': round_time,
    })

@login_required
def stop_round(request, round_id):
    round_obj = Round.objects.get(id=round_id)
    round_obj.is_active = False
    round_obj.save()
    return redirect('game:results', round_id=round_id)

@login_required
def show_results(request, round_id):
    """Show results for the round."""
    round_obj = Round.objects.get(id=round_id)
    submissions = Submission.objects.filter(round=round_obj).select_related('player', 'category')
    player = submissions.first().player if submissions.exists() else None

    # Scoring: +10 points for unique valid words
    player_score = 0
    all_correct = True
    for category in Category.objects.all():
        player_words = submissions.filter(player=player, category=category)
        if player_words.exists():
            word = player_words.first().word
            # Add 10 points if the word is valid and unique
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