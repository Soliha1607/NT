import random
from datetime import timedelta
from django.db import models
from django.utils import timezone


# Create your models here.

def generate_student_code():
    while True:
        code = str(random.randint(10_000, 99_999))
        if not Student.objects.filter(student_code=code).exists():
            return code


def default_deadline():
    # timezone.now() ga 48 soat qoâ€˜shib qaytaramiz
    return timezone.now() + timedelta(hours=48)


class Teacher(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='teacher/images/', default='images/default.png')
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, default='default')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Dars davomiyligi oylarda", default=4)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='courses')


class Group(models.Model):
    class StatusChoice(models.TextChoices):
        NOT_STARTED = 'boshlanmagan'
        ACTIVE = 'faol'
        FINISHED = 'tugagan'

    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='groups')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, related_name='groups', null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    status = models.CharField(choices=StatusChoice.choices, default=StatusChoice.NOT_STARTED.value)

    def __str__(self):
        return self.name


class Module(models.Model):
    title = models.CharField(max_length=150)
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='modules')
    is_given = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Homework(models.Model):
    overview = models.TextField()
    file = models.FileField(upload_to='homework/files/')
    deadline = models.DateTimeField(default=default_deadline,
                                    help_text="Avtomatik: hozirgi vaqtdan 48 soat keyingi muddat"
                                    )
    module = models.ForeignKey(Module,
                               on_delete=models.CASCADE,
                               related_name='homework')

    def __str__(self):
        return self.overview


class Video(models.Model):
    video = models.FileField(upload_to='video/files/')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos')


class Student(models.Model):
    gender_choices = (
        ("MALE", "male"),
        ("FEMALE", "female"),
        ("OTHER", "other"),
    )

    status = (
        ("ACTIVE", "active"),
        ("GRADUATED", "graduated"),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=gender_choices, default="MALE")
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=255)
    image = models.ImageField(upload_to='student/images/', default='images/default.png')
    student_code = models.CharField(
        max_length=5,
        unique=True,
        default=generate_student_code,
        editable=False,
        help_text="Avtomatik yaratilgan 5 xonali student kod"
    )
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='students', null=True)

    def __str__(self):
        return self.student_code