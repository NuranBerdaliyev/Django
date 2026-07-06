#users/tests.py
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from book_app.models import Author, Genre


User = get_user_model()


class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.password = 'BookPortalSecure2026!'

        self.user = User.objects.create_user(
            username='existing_user',
            password=self.password,
        )

        self.author = Author.objects.create(
            fullname='Ursula K. Le Guin',
            biography='American writer.',
        )

        self.genre = Genre.objects.create(
            name='Fantasy',
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse('api_register'),
            {
                'username': 'new_user',
                'password': 'NewUserSecure2026!',
                'password_confirm': 'NewUserSecure2026!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'new_user')
        self.assertNotIn('password', response.data)
        self.assertNotIn('password_confirm', response.data)

        created_user = User.objects.get(username='new_user')

        self.assertTrue(
            created_user.check_password('NewUserSecure2026!')
        )

    def test_registration_fails_when_passwords_do_not_match(self):
        response = self.client.post(
            reverse('api_register'),
            {
                'username': 'new_user',
                'password': 'NewUserSecure2026!',
                'password_confirm': 'DifferentPassword2026!',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn('password_confirm', response.data)
        self.assertFalse(
            User.objects.filter(username='new_user').exists()
        )

    def test_user_can_obtain_jwt_tokens(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'existing_user',
                'password': self.password,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_can_refresh_access_token(self):
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'existing_user',
                'password': self.password,
            },
            format='json',
        )

        refresh_token = token_response.data['refresh']

        response = self.client.post(
            reverse('token_refresh'),
            {
                'refresh': refresh_token,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_invalid_credentials_cannot_obtain_tokens(self):
        response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'existing_user',
                'password': 'WrongPassword2026!',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_access_token_allows_protected_book_creation(self):
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {
                'username': 'existing_user',
                'password': self.password,
            },
            format='json',
        )

        access_token = token_response.data['access']

        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )

        response = self.client.post(
            reverse('api_book_list_create'),
            {
                'title': 'A Wizard of Earthsea',
                'description': 'Fantasy novel.',
                'published_year': 1968,
                'author': self.author.pk,
                'genres': [self.genre.pk],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
