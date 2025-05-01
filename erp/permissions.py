from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'student')

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'teacher')
