from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class CoreTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_home_page_view_anonymous(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_home_page_view_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Redirect to lobby
        self.assertRedirects(response, reverse('game:lobby'))
