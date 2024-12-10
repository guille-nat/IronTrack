from django.db.models.signals import post_save
from django.dispatch import receiver
from guardian.shortcuts import assign_perm
from .models import UserProfile
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group


@receiver(post_save, sender=UserProfile)
def assign_user_profile_permissions(sender, instance, created, **kwargs):
    if created:
        # Asignar permiso para que el usuario acceda a su propio perfil
        assign_perm('view_own_profile', instance.user, instance)


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='usuario')
