from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Book, ReadingSession, UserProfile
from .serializers import BookSerializer, BookListSerializer, ReadingSessionSerializer, UserProfileSerializer
from .tasks import update_user_reading_statistics
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated


class GetBookList(generics.ListAPIView):
    # API view for listing and creating books.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    queryset = Book.objects.all()
    serializer_class = BookListSerializer


class GetReadingSessionList(generics.ListAPIView):
    # API view for listing and creating reading sessions.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer


class StartReadingSession(generics.CreateAPIView):
    # API view for starting a reading session.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    serializer_class = ReadingSessionSerializer

    def perform_create(self, serializer):
        # Implement the logic to start a reading session.

        user = self.request.user
        book_id = self.kwargs.get('book_id')

        # Check if the user has an active session with another book and end it
        active_session = ReadingSession.objects.filter(user=user, end_time__isnull=True).first()
        if active_session and active_session.book_id != book_id:
            active_session.end_time = timezone.now()
            active_session.save()

        book = get_object_or_404(Book, pk=book_id)
        serializer.save(user=user, book=book, start_time=timezone.now())


class EndReadingSession(generics.UpdateAPIView):
    # API view for ending a reading session.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer

    def perform_update(self, serializer):
        serializer.save(end_time=timezone.now())

    def get_object(self):
        # Implement the logic to end a reading session.
        user = self.request.user
        book_id = self.kwargs.get('book_id')
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset, user=user, book_id=book_id, end_time__isnull=True)
        return obj


class BookDetail(generics.RetrieveAPIView):
    # API view for retrieving a single book detail.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')
        user = self.request.user
        book = get_object_or_404(Book, pk=book_id)
        reading_session = ReadingSession.objects.filter(user=user, book=book, end_time__isnull=True).first()

        if reading_session:
            serializer = ReadingSessionSerializer(reading_session)
        else:
            serializer = BookSerializer(book)

        return Response(serializer.data)


class BookReadingTime(generics.RetrieveAPIView):
    # API view for retrieving the reading time of a book.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def retrieve(self, request, *args, **kwargs):
        # Implement the logic to calculate and return the reading time of a book.
        book = self.get_object()
        reading_sessions = ReadingSession.objects.filter(book=book, end_time__isnull=False)
        total_reading_time = sum([(session.end_time - session.start_time).total_seconds() for session in reading_sessions], 0)
        book.total_reading_time = total_reading_time
        serializer = self.get_serializer(book)
        return Response(serializer.data)


class UserStatistics(generics.RetrieveAPIView):
    # API view for retrieving user statistics.

    permission_classes = [IsAuthenticated]      # Ensure only authenticated users can access this view
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        # Implement the logic to retrieve and return user statistics.
        user = self.request.user
        obj, created = UserProfile.objects.get_or_create(user=user)
        return obj


def update_user_statistics(request):
    user_id = request.user.id
    update_user_reading_statistics.delay(user_id)
    return JsonResponse({'status': 'Task triggered successfully'})
