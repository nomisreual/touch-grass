from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("contact:contact")

    def test_get_contact_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contact/contact.html")

    @patch("contact.views.send_mail")
    def test_post_valid_contact_form(self, mock_send_mail):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Test Message",
        }
        response = self.client.post(self.url, data)
        mock_send_mail.assert_called_once()
        self.assertRedirects(response, reverse("main:index"))
        self.assertEqual(
            mock_send_mail.call_args[1].get("subject"),
            "Received contact from form submission",
        )
        self.assertTrue(
            data.get("name") in mock_send_mail.call_args[1].get("message"),
        )
        self.assertTrue(
            data.get("email") in mock_send_mail.call_args[1].get("message"),
        )
        self.assertTrue(
            data.get("subject") in mock_send_mail.call_args[1].get("message"),
        )
        self.assertTrue(
            data.get("message") in mock_send_mail.call_args[1].get("message"),
        )
        self.assertEqual(
            mock_send_mail.call_args[1].get("message"),
            "\n                Received message below from John Doe (john@example.com),\n                Subject: Test Subject\n                -------------------------------------------------\n\n                Test Message\n            ",
        )
        self.assertEqual(
            mock_send_mail.call_args[1].get("from_email"),
            settings.DEFAULT_FROM_EMAIL,
        )
        self.assertEqual(
            mock_send_mail.call_args[1].get("recipient_list"),
            [settings.NOTIFY_EMAIL],
        )

    def test_post_invalid_contact_form(self):
        # TODO: to be implemented
        pass
