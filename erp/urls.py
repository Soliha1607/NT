from django.urls import path
from erp.views import *

urlpatterns = [
    path('categories/', CategoryViewSet.as_view()),
    path('categories/<int:course_id>/', CategoryViewSet.as_view()),  # bitta kategoriyani course id orqali olish
    path('courses/<int:category_id>/', CourseViewSet.as_view()),
    path('groups/<int:course_id>/', GroupViewSet.as_view()),
    path('modules/<int:group_id>/', ModuleViewSet.as_view()),
    path('homework/', HomeworkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('homework/<int:group_id>/', HomeworkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('students/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('students/<int:group_id>/', StudentViewSet.as_view({'get': 'list'})),  # Group bo‘yicha filtrlangan studentlar
    path('teachers/', TeacherViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('teachers/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('supports/', SupportViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('supports/<int:pk>/', SupportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
