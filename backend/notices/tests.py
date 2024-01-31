from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from notices.models import NotificationsModel
from users.models import User


class NotificationTests(APITestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        self.recipient = User.objects.create_user(
            username='recipientuser',
            password='recipientpassword',
            email='recipient@example.com'
        )

        self.token = Token.objects.create(user=self.sender)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_notifications_successful(self):

        self.token = Token.objects.create(user=self.recipient)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        notification1 = NotificationsModel.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            message='Test notification 1'
        )
        notification2 = NotificationsModel.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            message='Test notification 2'
        )

        url = reverse('notices:notices-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['message'], 'Test notification 1')
        self.assertEqual(response.data[1]['message'], 'Test notification 2')

    def test_create_notification_successful(self):
        url = reverse('notices:create-notice', kwargs={'pk': self.recipient.pk})
        data = {'message': 'Test notification'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NotificationsModel.objects.count(), 1)

        notice = NotificationsModel.objects.get()
        self.assertEqual(notice.sender, self.sender)
        self.assertEqual(notice.recipient, self.recipient)
        self.assertEqual(notice.message, 'Test notification')
        self.assertFalse(notice.is_read)

        # Test for removal coin
        self.assertEqual(notice.sender.coins, 4)

    def test_create_notification_to_current_user(self):
        url = reverse('notices:create-notice', kwargs={'pk': self.sender.pk})
        data = {'message': 'Test notification'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You can\'t send a message to yourself', response.data['detail'])

    def test_create_notification_to_nonexistent_user(self):
        url = reverse('notices:create-notice', kwargs={'pk': 3})
        data = {'message': 'Test notification'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found.', response.data['detail'])

    def test_delete_notification_successful(self):

        notification = NotificationsModel.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            message='Test notification'
        )

        url = reverse('notices:delete-notice', kwargs={'pk': notification.id})

        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['detail'], 'Notice deleted successfully')

    def test_delete_notification_with_bad_permission(self):

        self.other_user = User.objects.create_user(
            username='other_user',
            password='other_userpassword',
            email='other_user@example.com'
        )

        self.token = Token.objects.create(user=self.other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


        notification = NotificationsModel.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            message='Test notification'
        )

        url = reverse('notices:delete-notice', kwargs={'pk': notification.id})

        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You\'re not a sender or rcipient')

    def test_create_notification_without_coins(self):
        self.sender.coins = 0
        self.sender.save()

        url = reverse('notices:create-notice', kwargs={'pk': self.recipient.pk})
        data = {'message': 'Test notification'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough coins to send a message', response.data['detail'])
