from django.test import TestCase
from user.models import YourModel

class YourModelTestCase(TestCase):
    def setUp(self):
        YourModel.objects.create(field1='value1', field2='value2')

    def test_model_method(self):
        instance = YourModel.objects.get(field1='value1')
        self.assertEqual(instance.some_method(), 'expected_value')