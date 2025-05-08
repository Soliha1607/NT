from django.db.models.signals import pre_save, post_save,post_delete
from django.dispatch import receiver
from .models import Video,Category, Course, Student,Group,Module,Homework,Teacher
from django.core.cache import cache

@receiver(post_save,sender = Video)
def update_status_to_ready(sender,instance,**kwargs):
    if instance.file:
        if instance.status == 'uploading':
            instance.status = 'ready'
            instance.save()


@receiver([post_save, post_delete], sender=Category)
@receiver([post_save, post_delete], sender=Homework)
@receiver([post_save, post_delete], sender=Video)
@receiver([post_save, post_delete], sender=Module)
@receiver([post_save, post_delete], sender=Teacher)
@receiver([post_save, post_delete], sender=Group)
@receiver([post_save, post_delete], sender=Course)
@receiver([post_save, post_delete], sender=Student)
def update_or_delete_cache(sender, instance, **kwargs):
    model_name = sender.__name__.lower()

    if model_name == 'category':
        cache.delete(f'categories')
        cache.delete(f'category-{instance.pk}')
    elif model_name == 'course':
        cache.delete(f'course')
        cache.delete(f'course-{instance.category.pk}')
    elif model_name == 'student':
        cache.delete(f'students')
        cache.delete(f'student-{instance.pk}')
    elif model_name == 'homework':
        cache.delete(f'homework')
        cache.delete(f'homework-{instance.module.pk}')
    elif model_name == 'video':
        cache.delete(f'video')
        cache.delete(f'video-{instance.module.pk}')
    elif model_name == 'module':
        cache.delete(f'module')
        cache.delete(f'module-{instance.pk}')
    elif model_name == 'teacher':
        cache.delete(f'teacher')
        cache.delete(f'teacher-{instance.pk}')
    elif model_name == 'group':
        cache.delete(f'group')
        cache.delete(f'group-{instance.pk}')