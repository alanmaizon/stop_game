from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import WordSubmission, Notification
from game.models import Category, Player

class CommunicationTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.admin_user = get_user_model().objects.create_superuser(username='adminuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.player = Player.objects.create(user=self.user)
        self.submission = WordSubmission.objects.create(
            player=self.user,
            category=self.category,
            word='testword',
            status='pending'
        )

    def test_submit_word(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('communication:submit_word'), {
            'category': self.category.id,
            'word': 'newword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(WordSubmission.objects.filter(word='newword').exists())

    def test_review_submissions(self):
        self.client.login(username='adminuser', password='password')
        response = self.client.get(reverse('communication:review_submissions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testword')

    def test_approve_submission(self):
        self.client.login(username='adminuser', password='password')
        response = self.client.post(reverse('communication:approve_submission', args=[self.submission.id]))
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, 'approved')
        self.assertTrue(Notification.objects.filter(player=self.user, message__contains='approved').exists())

    def test_reject_submission(self):
        self.client.login(username='adminuser', password='password')
        response = self.client.post(reverse('communication:reject_submission', args=[self.submission.id]), {
            'feedback': 'Not a valid word'
        })
        self.submission.refresh_from_db()
        self.assertEqual(self.submission.status, 'rejected')
        self.assertTrue(Notification.objects.filter(player=self.user, message__contains='rejected').exists())
