from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import UserProfile, ReadingSession


@shared_task
def update_user_reading_statistics(user_id):
    user_profile, created = UserProfile.objects.get_or_create(user_id=user_id)

    # Collect daily statistics for the last 7 days
    for days_ago in range(1, 8):
        start_date = timezone.now() - timedelta(days=days_ago)
        end_date = start_date + timedelta(days=1)
        total_reading_time = ReadingSession.objects.filter(
            user_id=user_id,
            start_time__gte=start_date,
            start_time__lt=end_date,
            end_time__isnull=False
        ).aggregate(total=sum('reading_time'))['total'] or 0

        setattr(user_profile, f'reading_time_last_7_days_{days_ago}', total_reading_time)

    # Collect daily statistics for the last 30 days
    for days_ago in range(1, 31):
        start_date = timezone.now() - timedelta(days=days_ago)
        end_date = start_date + timedelta(days=1)
        total_reading_time = ReadingSession.objects.filter(
            user_id=user_id,
            start_time__gte=start_date,
            start_time__lt=end_date,
            end_time__isnull=False
        ).aggregate(total=sum('reading_time'))['total'] or 0

        setattr(user_profile, f'reading_time_last_30_days_{days_ago}', total_reading_time)

    user_profile.save()
