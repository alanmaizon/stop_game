from django.test import TestCase
from game.models import YourModel

class YourModelTestCase(TestCase):
    def setUp(self):
        self.instance = YourModel.objects.create(field1='value1', field2='value2')

    def test_model_method(self):
        result = self.instance.your_method()
        self.assertEqual(result, expected_value)

    def test_another_model_method(self):
        result = self.instance.another_method()
        self.assertTrue(result)