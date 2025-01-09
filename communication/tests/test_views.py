from django.test import TestCase
from communication.views import YourViewFunction

class ViewTests(TestCase):
    def test_your_view_function(self):
        response = self.client.get('/your-url/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Expected Content')