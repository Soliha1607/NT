from rest_framework.permissions import BasePermission
from django.utils import timezone
from datetime import timedelta

class CanEditWithinSpecialTime(BasePermission):
    message = 'You can only edit the video within 10 minutes of creation.'

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            limit_time = obj.created_at + timedelta(minutes=10)
            return timezone.now() <= limit_time
        return True

class IsWithinWorkingHours(BasePermission):
    message = 'You can only access this resource during working hours (09:00 - 18:00).'

    def has_permission(self, request, view):
        current_time = timezone.localtime(timezone.now()).time()
        start_time = timezone.datetime.strptime('09:00', '%H:%M').time()
        end_time = timezone.datetime.strptime('18:00', '%H:%M').time()

        if start_time <= current_time <= end_time:
            return True
        return False
