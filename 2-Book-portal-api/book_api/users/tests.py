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

class AuthorAndGenreAdminAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            password='testpassword123',
            email='admin@example.com',
        )

        self.regular_user = User.objects.create_user(
            username='regular_user',
            password='testpassword123',
        )

        self.author = Author.objects.create(
            fullname='Isaac Asimov',
            biography='American science-fiction writer.',
        )

        self.genre = Genre.objects.create(
            name='Science Fiction',
        )

    def test_guest_can_read_authors_and_genres(self):
        authors_response = self.client.get(
            reverse('api_author_list_create')
        )

        genres_response = self.client.get(
            reverse('api_genre_list_create')
        )

        self.assertEqual(
            authors_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            genres_response.status_code,
            status.HTTP_200_OK,
        )

    def test_regular_user_cannot_create_author(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(
            reverse('api_author_list_create'),
            {
                'fullname': 'Ray Bradbury',
                'biography': 'American writer.',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_regular_user_cannot_update_author(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.patch(
            reverse(
                'api_author_detail_update_destroy',
                kwargs={'pk': self.author.pk},
            ),
            {
                'fullname': 'Changed Name',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.author.refresh_from_db()

        self.assertEqual(
            self.author.fullname,
            'Isaac Asimov',
        )

    def test_regular_user_cannot_delete_author(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.delete(
            reverse(
                'api_author_detail_update_destroy',
                kwargs={'pk': self.author.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Author.objects.filter(pk=self.author.pk).exists()
        )

    def test_admin_can_create_author(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(
            reverse('api_author_list_create'),
            {
                'fullname': 'Ray Bradbury',
                'biography': 'American writer.',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Author.objects.filter(
                fullname='Ray Bradbury',
            ).exists()
        )

    def test_admin_can_update_author(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.patch(
            reverse(
                'api_author_detail_update_destroy',
                kwargs={'pk': self.author.pk},
            ),
            {
                'fullname': 'Isaac Asimov Updated',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.author.refresh_from_db()

        self.assertEqual(
            self.author.fullname,
            'Isaac Asimov Updated',
        )

    def test_admin_can_delete_author(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(
            reverse(
                'api_author_detail_update_destroy',
                kwargs={'pk': self.author.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Author.objects.filter(pk=self.author.pk).exists()
        )

    def test_regular_user_cannot_create_genre(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(
            reverse('api_genre_list_create'),
            {
                'name': 'Fantasy',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_regular_user_cannot_update_genre(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.patch(
            reverse(
                'api_genre_detail_update_destroy',
                kwargs={'pk': self.genre.pk},
            ),
            {
                'name': 'Changed Genre',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.genre.refresh_from_db()

        self.assertEqual(
            self.genre.name,
            'Science Fiction',
        )

    def test_regular_user_cannot_delete_genre(self):
        self.client.force_authenticate(user=self.regular_user)

        response = self.client.delete(
            reverse(
                'api_genre_detail_update_destroy',
                kwargs={'pk': self.genre.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Genre.objects.filter(pk=self.genre.pk).exists()
        )

    def test_admin_can_create_genre(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(
            reverse('api_genre_list_create'),
            {
                'name': 'Fantasy',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            Genre.objects.filter(name='Fantasy').exists()
        )

    def test_admin_can_update_genre(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.patch(
            reverse(
                'api_genre_detail_update_destroy',
                kwargs={'pk': self.genre.pk},
            ),
            {
                'name': 'Science Fiction Updated',
            },
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.genre.refresh_from_db()

        self.assertEqual(
            self.genre.name,
            'Science Fiction Updated',
        )

    def test_admin_can_delete_genre(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(
            reverse(
                'api_genre_detail_update_destroy',
                kwargs={'pk': self.genre.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            Genre.objects.filter(pk=self.genre.pk).exists()
        )
