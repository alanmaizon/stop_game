from django.test import TestCase
from inbox.models import YourModel

class YourModelTestCase(TestCase):
    def test_field1_max_length(self):
        max_length = self.instance._meta.get_field('field1').max_length
        self.assertEqual(max_length, expected_max_length)

    def test_object_str(self):
        self.assertEqual(str(self.instance), expected_str_representation)

    def test_default_field2_value(self):
        instance = YourModel.objects.create(field1='value1')
        self.assertEqual(instance.field2, expected_default_value)