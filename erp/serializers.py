from rest_framework import serializers
from erp.models import Category, Course, Student, Module, Homework, Video


class CourseModelSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.id', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        exclude = ('is_given',)


class HomeworkSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(read_only=True)
    module = serializers.CharField(source='module.id', read_only=True)

    class Meta:
        model = Homework
        fields = '__all__'

    def save(self, **kwargs):
        homework = super().save(**kwargs)
        module = homework.module
        module.is_given = True
        module.save()
        return homework


class VideoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    module = serializers.CharField(source='module.id', read_only=True)

    class Meta:
        model = Video
        fields = ['name', 'file', 'status', 'file_size', 'module', 'created_at']

