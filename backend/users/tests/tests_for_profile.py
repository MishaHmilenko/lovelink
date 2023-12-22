import django

from userprofile.serializers import ProfileSerializer

django.setup()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpassword',
            email='other@example.com'
        )
        self.url_current_user = reverse('userprofile:profile_by_current_user')
        self.url_other_user = reverse('userprofile:profile_by_pk', kwargs={'pk': self.other_user.id})

# Tests with current user
    def test_user_get_profile_successful(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url_current_user)

        expected_data = ProfileSerializer(self.user).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_user_get_profile_non_authorization(self):
        response = self.client.get(self.url_current_user)

        expected_data = {'username': '', 'birthday': None, 'bio': None, 'image': None}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_user_patch_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(self.url_current_user, data={'bio': 'test update'})

        expected_data = {'username': 'testuser', 'birthday': None, 'bio': 'test update', 'gender': '', 'image': None}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

# Test with other user

    def test_other_user_get_profile_successful(self):
        response = self.client.get(self.url_other_user)

        expected_data = ProfileSerializer(self.other_user).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_non_other_user_profile(self):
        self.url_other_user = reverse('userprofile:profile_by_pk', kwargs={'pk': 999})

        response = self.client.get(self.url_other_user)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual('User does not exists', response.data['error'])

    def test_try_update_other_user(self):
        response = self.client.patch(self.url_other_user, data={'bio': 'try update other user profile'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual('You do not have permission to perform this action.', response.data['error'])
