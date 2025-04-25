from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from erp.serializers import *
from django.shortcuts import get_object_or_404


class CategoryViewSet(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Course.objects.filter(category=category_id)


class GroupViewSet(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return Group.objects.filter(course=course_id)


class ModuleViewSet(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_video(self, instance):
        videos = instance.videos.all()
        print("Videos found:", videos)
        return [video.video.url for video in videos]


class HomeworkViewSet(ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        module_id = self.kwargs.get("module_id")
        return get_object_or_404(Module, pk=module_id)


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return Student.objects.filter(group=group_id)


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer