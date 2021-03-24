from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db import models

"""
So here I could use inheritance and create an abstract class Role from which 
the Founder and Finder classes would inherit. The problem would be with defining 
the related_name attribute, which in this case would have to be overwritten 
several times in derived classes. 
Hence, it will be easier for me to create two classes without inheritance,
even if a couple of fields are repeated between them.
"""


class Founder(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('account'),
                                   on_delete=models.CASCADE, related_name='founder')

    class Meta:
        verbose_name        = _('founder')
        verbose_name_plural = _('founders')

    def __str__(self):
        return f'{self.account.username} - Founder'


class Finder(models.Model):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('account'),
                                   on_delete=models.CASCADE, related_name='finder')

    class Meta:
        verbose_name        = _('finder')
        verbose_name_plural = _('finders')

    def __str__(self):
        return f'{self.account.username} - Finder'
