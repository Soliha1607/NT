from rest_framework.permissions import BasePermission
from django.utils import timezone
from rest_framework import permissions
from datetime import timedelta, datetime


class CanEditWithinSpecialTime(permissions.BasePermission):
    message = 'User Or Time exception'

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user.username != 'oyposh':
                return False

            deadline = datetime.now(obj.created_at.tzinfo) - obj.created_at
            print(deadline)
            return deadline < timedelta(hours=2)

        return True

# class IsWithinWorkingHours(BasePermission):
#     message = 'You can only access this resource during working hours (09:00 - 18:00).'
#
#     def has_permission(self, request, view):
#         current_time = timezone.localtime(timezone.now()).time()
#         start_time = timezone.datetime.strptime('09:00', '%H:%M').time()
#         end_time = timezone.datetime.strptime('18:00', '%H:%M').time()
#
#         if start_time <= current_time <= end_time:
#             return True
#         return False
