from techstack.models import Technology, Framework,  Specialization, Experience
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField
from django.conf import settings
from django.utils import timezone
from .utils import custom_slugify
from django.db import models
import datetime


class Status(models.TextChoices):
    """
    Used to define the status of idea.
    """
    OPEN          = 'O', _('Recruitment open')
    SUSPENDED     = 'S', _('Recruitment suspended')
    CLOSED        = 'C', _('Recruitment closed')


title_help_text       = "Enter a title that best reflects your idea"
finders_help_text     = "Choose the partners you would like to join the idea"
technology_help_text  = "Choose technologies you would like to see in your idea."
framework_help_text   = "Choose frameworks you would like to use in your idea."
specialize_help_text  = "Choose specializations that match needs of your idea."
advancement_help_text = "Try to gauge overall experience(s) required for this idea."
repo_help_text        = "You can provide url to repository of your idea if exist."
repo_regex_text       = "Provide correct url to repository of your idea."
description_help_text = "Describe your idea, its genesis, provide information that " \
                        "will help others understand it."
team_size_help_text   = "Determine the size of the team."


class Idea(models.Model):
    title           = models.CharField(_('Idea title'), max_length=200,
                                  help_text=_(title_help_text))
    title_slug      = AutoSlugField(populate_from='title', db_index=True, unique=True,
                               slugify_function=custom_slugify)
    # change it later
    founder         = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Idea founder'),
                                   on_delete=models.CASCADE, related_name=_('founder'))
    # change it later
    finders         = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Idea finders'),
                                        related_name=_('finders'), help_text=_(finders_help_text),
                                        blank=True)

    technologies    = models.ManyToManyField(Technology, verbose_name=_('Technologies'),
                                        related_name=_('ideas'), help_text=_(technology_help_text),
                                        blank=True)
    frameworks      = models.ManyToManyField(Framework, verbose_name=_('Frameworks'),
                                        related_name=_('ideas'), help_text=_(framework_help_text),
                                        blank=True)
    specializations = models.ManyToManyField(Specialization, verbose_name=_('Specializations'),
                                        related_name=_('ideas'), help_text=_(specialize_help_text),
                                        blank=True)
    advancement     = MultiSelectField(_('Advancement of idea'), choices=Experience.choices, max_length=4,
                                    blank=True, help_text=_(advancement_help_text))
    repository      = models.URLField(_('Repository'), max_length=80, blank=True, null=True,
                                  help_text=_(repo_help_text),
                                  # any A-z 0-9 _ - character followed or not by @
                                  # regex matches 0 or 1 http(s)://
                                  # any A-z 0-9 _ - character followed or not by @
                                  # slashes, dots for suburls and 0 or 1 .git at the end
                                  # credits: https://stackoverflow.com/a/63283134
                                  # partly modified by me, also used in userdata.models
                                  validators=[RegexValidator(r'^(([A-Za-z0-9]+@|http(|s)\:\/\/)|'
                                                           r'(http(|s)\:\/\/[A-Za-z0-9]+@))'
                                                           r'([A-Za-z0-9.]+(:\d+)?)(?::|\/)'
                                                           r'([\d\/\w.-]+?)((\.git)?){1}$',
                                                           _(repo_regex_text), 'invalid'), ])
    description    = models.TextField(_('Idea description'), max_length=2000, blank=False,
                                      help_text=_(description_help_text))
    date_created   = models.DateTimeField(_('Date created'), default=timezone.now, editable=False)
    status         = models.CharField(_('Idea status'), max_length=4, choices=Status.choices,
                                      default=Status.OPEN)
    team_size      = models.PositiveSmallIntegerField(_('Idea team size'), blank=False,
                                                      help_text=team_size_help_text)

    class Meta:
        verbose_name        = _('idea')
        verbose_name_plural = _('ideas')

    def __str__(self):
        return f'{self.title} - Idea by {self.founder}'

    def was_recently_created(self):
        now = timezone.now()
        interval = datetime.timedelta(days=7)
        return now - interval <= self.date_joined <= now
