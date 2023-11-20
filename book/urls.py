from django.urls import path
from .views import (GetBookList, GetReadingSessionList, StartReadingSession, EndReadingSession, BookDetail,
                    BookReadingTime, UserStatistics)

urlpatterns = [
    # API endpoints for managing books
    path('books/', GetBookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('books/<int:pk>/reading-time/', BookReadingTime.as_view(), name='book-reading-time'),

    # API endpoints for managing reading sessions
    path('reading-sessions/', GetReadingSessionList.as_view(), name='reading-session-list'),
    path('start-reading-session/<int:book_id>/', StartReadingSession.as_view(), name='start-reading-session'),
    path('end-reading-session/<int:pk>/', EndReadingSession.as_view(), name='end-reading-session'),

    # API endpoint for user statistics
    path('user-statistics/', UserStatistics.as_view(), name='user-statistics'),
]
