from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from chat.models import Chat, Message
from users.models import User


class MessageTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='user1password',
            email='user1@example.com'
        )

        self.user2 = User.objects.create_user(
            username='testuser2',
            password='user2password',
            email='user2@example.com'
        )

        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user1.key)

        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1, self.user2)

    def test_create_message_successful(self):
        url = reverse('chat:create-message', kwargs={'pk': self.chat.id})
        data = {'content': 'Test message'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)

        message = Message.objects.get()
        self.assertEqual(message.user, self.user1)
        self.assertEqual(message.content, 'Test message')

    def test_create_message_with_nonexistent_chat(self):
        print(self.chat)
        url = reverse('chat:create-message', kwargs={'pk': 1})
        data = {'content': 'Test message'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_message_with_bad_permission(self):
        other_user = User.objects.create_user(
            username='other_user',
            password='other_userpassword',
            email='other_user@example.com'
        )

        self.token_other_user = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_other_user.key)

        url = reverse('chat:create-message', kwargs={'pk': self.chat.id})
        data = {'content': 'Test message'}

        response = self.client.post(path=url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You are not a member of chat')

    def test_update_message_successful(self):
        self.message = Message.objects.create(user=self.user1, chat=self.chat, content={'content': 'test message'})

        url = reverse('chat:update-message', kwargs={'pk': self.message.id})
        response = self.client.patch(path=url, data={'content': 'test update message'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'test update message')

    def test_update_message_with_bad_permission(self):
        other_user = User.objects.create_user(
            username='other_user',
            password='other_userpassword',
            email='other_user@example.com'
        )

        self.token_other_user = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_other_user.key)

        self.message = Message.objects.create(user=self.user1, chat=self.chat, content={'content': 'test message'})

        url = reverse('chat:update-message', kwargs={'pk': self.message.id})
        response = self.client.patch(path=url, data={'content': 'test update message'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'That`s not your message')

    def test_delete_message_successful(self):
        self.message = Message.objects.create(user=self.user1, chat=self.chat, content={'content': 'test message'})

        url = reverse('chat:delete-message', kwargs={'pk': self.message.id})
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_message_with_bad_permission(self):
        other_user = User.objects.create_user(
            username='other_user',
            password='other_userpassword',
            email='other_user@example.com'
        )

        self.token_other_user = Token.objects.create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_other_user.key)

        self.message = Message.objects.create(user=self.user1, chat=self.chat, content={'content': 'test message'})

        url = reverse('chat:delete-message', kwargs={'pk': self.message.id})
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'That`s not your message')

    def test_delete_nonexistent_message(self):

        url = reverse('chat:delete-message', kwargs={'pk': 0})
        response = self.client.delete(path=url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Not found', response.data['detail'])
