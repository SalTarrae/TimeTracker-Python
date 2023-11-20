from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from celery.result import AsyncResult
from .tasks import update_user_reading_statistics
from .models import Book, ReadingSession, UserProfile


class TimeTrackerAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            year_of_publication=2023,
            short_description='Short description',
            full_description='Full description'
        )

    def create_reading_session(self):
        start_time = timezone.now() - timedelta(hours=1)
        end_time = start_time + timedelta(minutes=30)
        ReadingSession.objects.create(user=self.user, book=self.book, start_time=start_time, end_time=end_time)

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Book')

    def test_get_book_detail(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Book')

    def test_start_and_end_reading_session(self):
        start_url = reverse('start-reading-session', args=[self.book.id])
        response_start = self.client.post(start_url)
        self.assertEqual(response_start.status_code, status.HTTP_201_CREATED)

        self.create_reading_session()
        response_start_new = self.client.post(start_url)
        self.assertEqual(response_start_new.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ReadingSession.objects.filter(user=self.user, end_time__isnull=True).count(), 1)

        end_url = reverse('end-reading-session', args=[self.book.id])
        response_end = self.client.patch(end_url)
        self.assertEqual(response_end.status_code, status.HTTP_200_OK)
        self.assertEqual(ReadingSession.objects.filter(user=self.user, end_time__isnull=True).count(), 0)

    def test_get_user_statistics(self):
        url = reverse('user-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'total_reading_time')

    def test_update_user_statistics_task(self):
        task = update_user_reading_statistics.apply_async(args=[self.user.id])

        task_result = AsyncResult(task.id)
        task_result.get()

        user_profile = UserProfile.objects.get(user=self.user)
        self.assertNotEqual(user_profile.reading_time_last_7_days_1, None)
        self.assertNotEqual(user_profile.reading_time_last_30_days_1, None)

    def test_create_book(self):
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': 'New Author',
            'year_of_publication': 2023,
            'short_description': 'Short description',
            'full_description': 'Full description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)  # Assuming one book already exists in the setup
        self.assertEqual(Book.objects.last().title, 'New Book')

    def test_invalid_start_reading_session(self):
        # Trying to start a session for a non-existent book
        url = reverse('start-reading-session', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_end_reading_session(self):
        # Trying to end a session for a non-existent book
        url = reverse('end-reading-session', args=[999])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_user_statistics(self):
        # Trying to retrieve statistics for a non-existent user
        self.user.delete()
        url = reverse('user-statistics')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_statistics_task_invalid_user(self):
        # Trying to update statistics for a non-existent user
        task = update_user_reading_statistics.apply_async(args=[999])
        task_result = AsyncResult(task.id)
        task_result.get()

    def test_update_user_statistics_task_invalid_session(self):
        # Trying to update statistics for a user with no reading sessions
        user = User.objects.create_user(username='testuser2', password='testpass2')
        task = update_user_reading_statistics.apply_async(args=[user.id])
        task_result = AsyncResult(task.id)
        task_result.get()

    def test_book_detail_with_active_session(self):
        # Retrieve book details with an active reading session
        self.create_reading_session()
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Test Book')
        self.assertContains(response, 'Active Reading Session')

    def test_end_reading_session_with_invalid_book(self):
        # Trying to end a session with an invalid book ID
        url = reverse('end-reading-session', args=[999])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
