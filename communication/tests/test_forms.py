from django.test import TestCase

class FormHandlingTests(TestCase):
    def test_form_submission_success(self):
        response = self.client.post('/form-url/', {'field1': 'value1', 'field2': 'value2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Success message')

    def test_form_submission_failure(self):
        response = self.client.post('/form-url/', {'field1': '', 'field2': 'value2'})
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Error message')