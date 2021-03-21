from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import Founder, Finder
from django.conf import settings
from idea.models import Idea


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_founder(sender, instance, created, **kwargs):
    if created:
        Founder.objects.create(account=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_finder(sender, instance, created, **kwargs):
    if created:
        Finder.objects.create(account=instance)


# @receiver(m2m_changed, sender=Idea.finders.through)
# def limit_ideas_created(sender, instance, action, reverse, model, pk_set, **kwargs):
#     to-do
