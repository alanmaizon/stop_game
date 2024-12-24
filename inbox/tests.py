from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from communication.models import Notification, WordSubmission

class InboxTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.notification = Notification.objects.create(player=self.user, message='Test Notification')
        self.submission = WordSubmission.objects.create(player=self.user, word='TestWord')

    def test_notifications_with_archived_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('inbox:notifications_with_archived'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/notifications_with_archived.html')

    def test_submissions_with_submit_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('inbox:submissions_with_submit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/submissions_with_submit.html')

    def test_mark_as_read_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('inbox:mark_as_read', args=[self.notification.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to notifications list
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_archive_notification_view(self):
        self.notification.is_read = True
        self.notification.save()
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('inbox:archive_notification', args=[self.notification.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to notifications list
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_archived)

    def test_archived_notifications_view(self):
        self.notification.is_archived = True
        self.notification.save()
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('inbox:notifications_with_archived'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inbox/notifications_with_archived.html')
