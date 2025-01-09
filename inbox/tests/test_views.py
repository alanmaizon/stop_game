from django.test import TestCase
from inbox.views import YourViewClass

class YourViewClassTest(TestCase):
    def test_view_function(self):
        response = self.client.get('/your-url/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'your_template.html')

    def test_another_functionality(self):
        response = self.client.post('/your-url/', {'key': 'value'})
        self.assertEqual(response.status_code, 302)  # Assuming a redirect
        self.assertRedirects(response, '/redirect-url/')