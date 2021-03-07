from django.utils.translation import ugettext_lazy as _
from django.db import models

name_error_text = "Already exists."


class Tech(models.Model):
    name = models.CharField(_('Name'), max_length=50, unique=True,
                            help_text="Name",
                            error_messages={'unique': _(name_error_text), })

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return '%(class)'


class Technology(Tech):

    class Meta:
        abstract = False
        verbose_name        = _('technology')
        verbose_name_plural = _('technologies')

    def __str__(self):
        return self.name


class Specialization(Tech):

    class Meta:
        abstract = False
        verbose_name        = _('specialization')
        verbose_name_plural = _('specializations')

    def __str__(self):
        return self.name
