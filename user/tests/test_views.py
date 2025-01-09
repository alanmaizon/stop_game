from django.test import TestCase
from user.views import YourViewFunction

class TestUserViews(TestCase):
    def test_your_view_function(self):
        response = self.client.get('/your-url/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expected Content')