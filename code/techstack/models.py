from django.utils.translation import ugettext_lazy as _
from django.db import models

name_error_text = "Already exists."


class Tech(models.Model):
    """
    Abstract class not used in any database table.
    Subclassed by Technology and Specialization models.
    """
    name = models.CharField(_('Name'), max_length=50, unique=True,
                            help_text="Name",
                            error_messages={'unique': _(name_error_text), })

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Technology(Tech):
    """
    Technology services.
    """

    class Meta:
        abstract = False
        verbose_name        = _('technology')
        verbose_name_plural = _('technologies')


class Framework(Tech):
    """
    Technology services frameworks.
    """

    class Meta:
        abstract = False
        verbose_name        = _('framework')
        verbose_name_plural = _('frameworks')


class Specialization(Tech):
    """
    Technology roles.
    """
    class Meta:
        abstract = False
        verbose_name        = _('specialization')
        verbose_name_plural = _('specializations')
