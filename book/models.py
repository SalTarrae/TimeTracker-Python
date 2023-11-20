from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    # Model representing a book.

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year_of_publication = models.IntegerField()
    short_description = models.TextField(max_length=255, null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=63, null=True, blank=True)
    country = models.CharField(max_length=255, default="Unknown")

    def __str__(self):
        # String representation of the book (used in the admin interface).
        return f"{self.title} - {self.author}. {self.year_of_publication}"


class ReadingSession(models.Model):
    # Model representing a reading session for a book.

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)

    @property
    def reading_time(self):
        # Calculate the reading time for the session.
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        # If the session is ongoing, return None.
        return None

    def __str__(self):
        # String representation of the reading session (used in the admin interface).
        return f"{self.user.username} - {self.book.title} - {self.start_time} to {self.end_time}"


class UserProfile(models.Model):
    # Model representing a User.

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_reading_time = models.FloatField(default=0)
