# reading_tracker/serializers.py
from rest_framework import serializers
from .models import Book, ReadingSession, UserProfile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year_of_publication', 'short_description']


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ReadingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingSession
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
