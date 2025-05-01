from django.urls import path
from erp.views import *

urlpatterns = [
    #categories
    path('categories/', CategoryViewSet.as_view()),
    path('categories/<int:course_id>/', CategoryViewSet.as_view()),

    #courses
    path('courses/<int:category_id>/', CourseViewSet.as_view()),

    #groups
    path('groups/<int:course_id>/', GroupViewSet.as_view()),

    #modules
    path('modules/<int:group_id>/', ModuleViewSet.as_view()),

    #homework
    path('homework/', HomeworkViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('homework/<int:pk>/', HomeworkViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    #student
    path('students/', StudentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('students/<int:group_id>/', StudentViewSet.as_view({'get': 'list'})),

    #teachers
    path('teachers/', TeacherViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('teachers/<int:pk>/', TeacherViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    #supports
    path('supports/', SupportViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('supports/<int:pk>/', SupportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    #video
    path('videos/', VideoListCReateApiView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailAPiView.as_view(), name='video-by-module'),
]
