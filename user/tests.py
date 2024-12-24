from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import User as CustomUser
from .forms import UserRegistrationForm, UserProfileUpdateForm

class UserTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

    def test_register_view(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/register.html')

        response = self.client.post(reverse('user:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_login_view(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

        response = self.client.post(reverse('user:login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to lobby

    def test_update_profile_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('user:update_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/update_profile.html')

        response = self.client.post(reverse('user:update_profile'), {
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to update profile
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_user_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword',
            'password2': 'newpassword'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_profile_update_form(self):
        form_data = {
            'email': 'updated@example.com'
        }
        form = UserProfileUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
