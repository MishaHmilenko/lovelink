from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from chat.models import Chat
from users.models import User


class ChatTests(APITestCase):

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

    def test_create_chat_successful(self):

        url = reverse('chat:chat-create')
        response = self.client.post(url, data='{"members": [{"id": ' + str(self.user2.id) + '}]}',
                                    content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Chat created successfully')
        self.assertEqual(Chat.objects.count(), 1)

        chat = Chat.objects.get()
        self.assertTrue(chat.members.filter(id=self.user1.id).exists())
        self.assertTrue(chat.members.filter(id=self.user2.id).exists())

    def test_get_chat_successful(self):
        self.chat = Chat.objects.create()
        self.chat.members.add(self.user1, self.user2)

        url = reverse('chat:chat-create')
        response = self.client.post(url, data='{"members": [{"id": ' + str(self.user2.id) + '}]}',
                                    content_type='application/json', follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.redirect_chain)

        redirect_url = response.redirect_chain[-1][0]

        response_after_redirect = self.client.get(redirect_url)
        self.assertEqual(response_after_redirect.status_code, status.HTTP_200_OK)
        self.assertIn('Chat is empty', response_after_redirect.data)

    def test_create_chat_with_nonexistent_user(self):

        url = reverse('chat:chat-create')
        response = self.client.post(url, data='{"members": [{"id": ' + '1231233' + '}]}',
                                    content_type='application/json', follow=True)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User matching query does not exist.', response.data['error'])

