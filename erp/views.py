from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from erp.serializers import *
from rest_framework.permissions import AllowAny

class CategoryViewSet(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        if course_id:
            return Category.objects.filter(courses__id=course_id)
        return Category.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context



class CourseViewSet(generics.ListAPIView):
    queryset = Course.objects.filter()
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
    permission_classes = [AllowAny]

    def get_video(self, instance):
        videos = instance.videos.all()
        print("Videos found:", videos)
        return [video.video.url for video in videos]


class HomeworkViewSet(ModelViewSet):
    serializer_class = HomeworkSerializer

    def get_queryset(self):
        module_id = self.request.query_params.get('module_id')
        if module_id:
            return Homework.objects.filter(module_id=module_id)
        return Homework.objects.all()


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        group_id = self.kwargs.get("group_id")
        return Student.objects.filter(group=group_id)


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class SupportViewSet(ModelViewSet):
    queryset = Support.objects.all()
    serializer_class = TeacherSerializer

class VideoViewSet(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        module_id = self.kwargs.get("module_id")
        if module_id:
            return Video.objects.filter(module_id=module_id)
        return Video.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
