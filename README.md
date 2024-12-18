# Let’s build a **Stop!** game step by step using **Django**.

---

### 🎯 **Goal**: Build a web-based *Stop!* game
Players will compete by filling categories with words that begin with a specific letter. At the end of the round, scores are calculated.

---

### 🛠️ **Project Plan**
1. **Setup Django Project**: Create a new project and app.
2. **Data Modeling**:
   - Players, categories, rounds, and scores.
3. **Game Logic**:
   - Generate a random letter.
   - Allow players to submit words for given categories.
   - Calculate scores based on unique and valid answers.
4. **Frontend**:
   - Game pages: Start, Play, and Results.
   - HTML templates, forms, and basic styling.
5. **Testing and Enhancements**.

---

### 🚀 **Step 1: Django Setup**
Follow these steps to set up your Django environment:

#### 1.1 Install Django
If you haven’t already installed Django:
```bash
pip install django
```

#### 1.2 Create a New Project
```bash
django-admin startproject stop_game
cd stop_game
python manage.py startapp game
```

#### 1.3 Register the App
Add `'game'` to your `INSTALLED_APPS` in `settings.py`.

```python
INSTALLED_APPS = [
    # Default apps...
    'game',
]
```

---

### 📊 **Step 2: Data Modeling**

Let’s design the database schema for the game. Add the following models to `game/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
import random

class Category(models.Model):
    """Categories like Country, Animal, Food, etc."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Round(models.Model):
    """A game round with a specific letter."""
    letter = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_letter():
        return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

class Player(models.Model):
    """Players of the game."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

class Submission(models.Model):
    """Player submissions for each round."""
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.player} - {self.category}: {self.word}"
```

#### 💾 Apply Migrations
Run the following commands to apply the models:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 🔨 **Step 3: Views and Game Logic**

Here are the views to:
1. Start the game and generate a random letter.
2. Accept submissions from players.
3. Calculate and display scores.

Add this to `game/views.py`:

```python
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Category, Round, Submission, Player
from django.contrib.auth.decorators import login_required

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
    })

@login_required
def submit_words(request, round_id):
    """Submit words for the round."""
    if request.method == 'POST':
        round_obj = Round.objects.get(id=round_id)
        player, _ = Player.objects.get_or_create(user=request.user)
        categories = Category.objects.all()

        for category in categories:
            word = request.POST.get(f'category_{category.id}')
            if word:
                Submission.objects.create(
                    player=player,
                    round=round_obj,
                    category=category,
                    word=word.capitalize()
                )
        return redirect('game:results', round_id=round_obj.id)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def show_results(request, round_id):
    """Show results for the round."""
    round_obj = Round.objects.get(id=round_id)
    submissions = Submission.objects.filter(round=round_obj)
    players = Player.objects.all()

    # Scoring: +10 points for unique valid words
    scores = {}
    for player in players:
        player_score = 0
        for category in Category.objects.all():
            player_words = submissions.filter(player=player, category=category)
            if player_words.exists():
                word = player_words.first().word
                if submissions.filter(category=category, word=word).count() == 1:
                    player_score += 10  # Unique word
        scores[player.user.username] = player_score
        player.score += player_score
        player.save()

    return render(request, 'game/results.html', {
        'round': round_obj,
        'scores': scores,
    })
```

---

### 📝 **Step 4: URLs**

Configure the URLs for the game. Add this to `game/urls.py`:

```python
from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('start/', views.start_game, name='start'),
    path('submit/<int:round_id>/', views.submit_words, name='submit'),
    path('results/<int:round_id>/', views.show_results, name='results'),
]
```

Include the app URLs in `stop_game/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('game/', include('game.urls')),
]
```

---

### 🎨 **Step 5: Templates**

Create HTML templates for the game:

1. **Start Game (`game/templates/game/start.html`)**:
```html
<h1>Stop! Game</h1>
<p>Letter: <strong>{{ letter }}</strong></p>
<form method="POST" action="{% url 'game:submit' round.id %}">
    {% csrf_token %}
    {% for category in categories %}
        <label>{{ category.name }}:</label>
        <input type="text" name="category_{{ category.id }}">
        <br>
    {% endfor %}
    <button type="submit">Submit</button>
</form>
```

2. **Results Page (`game/templates/game/results.html`)**:
```html
<h1>Game Results</h1>
{% for player, score in scores.items %}
    <p>{{ player }}: {{ score }} points</p>
{% endfor %}
```

---

### 🎮 **Step 6: Run the Game**

1. Create categories in the database:
   - Access the admin panel and add categories like *Country, Animal, Food, etc.*
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Visit the game URL:
   - Start a new round at `/game/start/`.

---