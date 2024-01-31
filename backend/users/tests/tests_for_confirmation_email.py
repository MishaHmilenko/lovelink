from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import EmailConfirmationToken, User


class ConformationEmailTests(APITestCase):

    def test_send_email_confirmation_with_unauthorized_user(self):
        url = reverse('users:send-confirmation-email')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_send_email_confirmation_create_token(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        url = reverse('users:send-confirmation-email')
        self.client.force_authenticate(user=user)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = EmailConfirmationToken.objects.filter(user=user).first()
        self.assertIsNotNone(token)
