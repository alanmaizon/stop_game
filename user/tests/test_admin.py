from django.test import TestCase
from user.models import Admin

class AdminTests(TestCase):
    def setUp(self):
        self.admin = Admin.objects.create(username='admin', password='password')

    def test_admin_creation(self):
        self.assertIsInstance(self.admin, Admin)

    def test_admin_str(self):
        self.assertEqual(str(self.admin), 'admin')

    def test_admin_permissions(self):
        self.assertTrue(self.admin.has_perm('some_permission'))