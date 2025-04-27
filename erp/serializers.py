from rest_framework import serializers
from erp.models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    video = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ["id", "title", "is_given", "video", "students"]

    def get_video(self, instance):
        videos = instance.videos.all()
        if videos.exists():
            return [video.video.url for video in videos]
        return None  # yoki return []

    def get_students(self, instance):
        if instance.group and instance.group.students.exists():
            return instance.group.students.count()
        return 0


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name", "started_at", "ended_at", "status"]


class HomeworkSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Homework
        fields = ["id", "overview", "file_url", "deadline"]

    def get_file_url(self, instance):
        return instance.file.url if instance.file else None


class StudentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "gender", "phone_number", "password", "image_url", "student_code"]

    def get_image_url(self, instance):
        request = self.context.get('request')
        if instance.image and request:
            return request.build_absolute_uri(instance.image.url)
        return None



class TeacherSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ["id", "first_name", "last_name", "phone_number", "password", "image_url", "username"]

    def get_image_url(self, instance):
        return instance.image.url if instance.image else None


class SupportSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ["id", "first_name", "last_name", "phone_number", "password", "image_url", "username"]

    def get_image_url(self, instance):
        return instance.image.url if instance.image else None