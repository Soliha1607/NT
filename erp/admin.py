from django.contrib import admin
from erp.models import Category, Course, Module, Student, Group, Teacher, Homework, Video

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_code', 'group')


admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Teacher)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    fields = ('title', 'group')
    list_display = ('title', 'group', 'is_given')


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Homework._meta.fields]