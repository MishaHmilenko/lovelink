import django
from rest_framework.authtoken.models import Token

django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersRegistrationTests(APITestCase):

    def setUp(self):
        self.data = {
            'username': 'test',
            'birthday': '1990-01-01',
            'gender': 'M',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        self.url = reverse('users:registration')

    def test_user_create(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_user_create_with_wrong_birthdate(self):
        self.data['birthday'] = '2023-01-01'
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You must be over 10 years old', response.data['errors']['non_field_errors'][0])

    def test_user_create_with_different_passwords(self):
        self.data['password2'] = 'differentpassword'
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Password do not match', response.data['errors']['non_field_errors'][0])

    def test_user_create_with_any_blank_line(self):
        self.data['username'] = ''
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This field may not be blank', response.data['errors']['username'][0])


class UserLoginTests(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'test',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(username=self.data['username'], password=self.data['password'])
        self.url = reverse('users:login')

    def test_login_user_successful(self):
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)

        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)

    def test_login_user_unsuccessful(self):
        self.data['password'] = 'wrongpassword'
        response = self.client.post(self.url, self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIn('errors', response.data)
