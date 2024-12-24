from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Round, Player, Submission, ValidAnswer

class GameTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Animal')
        self.round = Round.objects.create(letter='A')
        self.player = Player.objects.create(user=self.user)
        self.valid_answer = ValidAnswer.objects.create(category=self.category, word='Antelope')

    def test_lobby_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('game:lobby'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/lobby.html')

    def test_start_game_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('game:start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/start.html')

    def test_submit_words_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('game:submit', args=[self.round.id]), {
            f'category_{self.category.id}': 'Antelope'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to results
        submission = Submission.objects.get(player=self.player, round=self.round, category=self.category)
        self.assertTrue(submission.is_valid)

    def test_show_results_view(self):
        self.client.login(username='testuser', password='testpass')
        Submission.objects.create(player=self.player, round=self.round, category=self.category, word='Antelope', is_valid=True)
        response = self.client.get(reverse('game:results', args=[self.round.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game/results.html')

    def test_is_valid_word(self):
        from .views import is_valid_word
        is_valid, message = is_valid_word('Antelope', 'A', 'Animal')
        self.assertTrue(is_valid)
        self.assertEqual(message, 'Valid word.')
