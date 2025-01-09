from django.test import TestCase

class AppTests(TestCase):
    def test_app_functionality(self):
        self.assertEqual(1 + 1, 2)

    def test_another_app_functionality(self):
        self.assertTrue(True)