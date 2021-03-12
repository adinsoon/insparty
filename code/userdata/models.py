from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.validators import RegexValidator, EmailValidator, ValidationError
from techstack.models import Technology, Framework, Specialization
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.db import models
import datetime
import re


class Sex(models.TextChoices):
    MALE       = 'M', _('Male')
    FEMALE     = 'F', _('Female')
    OTHER      = 'O', _('Other')
    PREFER_NOT = 'P', _('Prefer Not To Say')


class Experience(models.TextChoices):
    NOVICE     = 'N', _('Novice (little to no experience)')
    JUNIOR     = 'J', _('Junior (base experience)')
    REGULAR    = 'R', _('Regular (significant experience)')
    SENIOR     = 'S', _('Senior (high experience)')
    EXPERT     = 'E', _('Expert (superior experience)')


def validate_users_over_14_years(value: datetime.date):
    """
    Validator checks if user is at least 14 years old
    """
    now = datetime.date.today()
    if (now-value).days/365 >= 14:
        return value
    else:
        raise ValidationError(birthdate_valid_text)


user_help_text       = "Enter unique username - 30 characters or fewer. Letters, digits and _ only."
user_regex_text      = "Enter a valid username. This value may contain only letters, numbers and _ character."
user_error_text      = "The username is already taken."
email_help_text      = "Enter unique e-mail address."
email_error_text     = "An user with that e-mail already exists."
email_regex_text     = "E-mail must consist of username, @ symbol, domain name, dot and domain."
phone_regex_text     = "Phone number must be entered in the format: 123456789 or +48123456789. " \
                     "Up to 12 digits allowed."
verify_help_text     = "Indicates whether the user has verified his account by e-mail and is " \
                     "ready to log-in. Un-select in order to let the user activate his account."
linkedin_help_text   = "You can provide url to your linkedin profile."
linkedin_regex_text  = "Linkedin Profile must be entered in the format: linkedin.com/in/user or " \
                       "http(s)://linkedin.com/in/user . Limited address size."
repo_help_text       = "You can provide url to your repository or profile."
repo_regex_text      = "Provide correct url to your repository or profile."
experience_help_text = "Be honest about your overall programming experience."
technology_help_text = "Choose technologies you feel good in."
framework_help_text  = "Choose frameworks you use."
specialize_help_text = "Choose specializations that match your role."
birthdate_help_text  = "You need to meet the age requirements to have an account."
birthdate_valid_text = "You must be at least 14 years old in order to have an account. "


class Account(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(_('Username'), max_length=30, unique=True,
                                       help_text=_(user_help_text),
                                       # regex matches 1 or more of any word character
                                       # (alnum + underscore)
                                       validators=[RegexValidator(r'^\w+$', _(user_regex_text),
                                                                  'invalid'), ],
                                       error_messages={'unique': _(user_error_text), })
    email           = models.EmailField(_('E-mail address'), unique=True,
                                       help_text=_(email_help_text),
                                       validators=[EmailValidator(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+'
                                                                  r'\.[a-zA-Z0-9-.]+$)',
                                                                 _(email_regex_text))],
                                       error_messages={'unique': _(email_error_text), })
    firstname       = models.CharField(_('First name'), max_length=30, blank=True)
    lastname        = models.CharField(_('Last name'), max_length=30, blank=True)

    phone           = models.CharField(_('Phone number'), max_length=12, blank=True, null=True,
                                       # regex matches 0 or 1 '+' character and
                                       # from 9 to 12 of any digit characters
                                       validators=[RegexValidator(r'^\+?1?\d{9,12}$', _(phone_regex_text),
                                                               'invalid'), ])
    linkedin        = models.URLField(_('Linkedin Profile'), max_length=80, blank=True, null=True,
                                help_text=_(linkedin_help_text),
                                # regex matches 0 or 1 http(s)://
                                # only 1 full expression linkedin.com/
                                # any A-z 0-9 _ - character
                                # 0 or 1 / ending slash and nothing else further
                                # to avoid any unvalidated redirect
                                # https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html
                                validators=[RegexValidator(r'^(\S*)(http(s)?:\/\/([\w]+\.)?)?'
                                                           r'linkedin\.com\/in\/[A-z0-9_-]+\/?$',
                                            _(linkedin_regex_text), 'invalid'), ])
    repository      = models.URLField(_('Repository'), max_length=80, blank=True, null=True,
                                help_text=_(repo_help_text),
                                # any A-z 0-9 _ - character followed or not by @
                                # regex matches 0 or 1 http(s)://
                                # any A-z 0-9 _ - character followed or not by @
                                # slashes, dots for suburls and 0 or 1 .git at the end
                                # credits: https://stackoverflow.com/a/63283134
                                # partly modified by me
                                 validators=[RegexValidator(r'^(([A-Za-z0-9]+@|http(|s)\:\/\/)|'
                                                           r'(http(|s)\:\/\/[A-Za-z0-9]+@))'
                                                           r'([A-Za-z0-9.]+(:\d+)?)(?::|\/)'
                                                           r'([\d\/\w.-]+?)((\.git)?){1}$',
                                                           _(repo_regex_text), 'invalid'), ])
    experience      = models.CharField(_('Stage of advancement'), max_length=4, choices=Experience.choices,
                                    blank=True, help_text=_(experience_help_text))
    technologies    = models.ManyToManyField(Technology, blank=True, related_name=_('accounts'),
                                            help_text=_(technology_help_text))
    frameworks      = models.ManyToManyField(Framework, blank=True,  related_name=_('accounts'),
                                            help_text=_(framework_help_text))
    specializations = models.ManyToManyField(Specialization, blank=True, related_name=_('accounts'),
                                            help_text=_(specialize_help_text))
    # rating       = models.

    sex             = models.CharField(_('Sex'), max_length=4, choices=Sex.choices, blank=True)
    birthdate       = models.DateField(_('Date of birth'), blank=True, null=True,
                                       help_text=_(birthdate_help_text),
                                       validators=[validate_users_over_14_years])
    description     = models.TextField(_('Description of user'), max_length=200, blank=True)

    is_staff        = models.BooleanField(_('Staff status'), default=False)
    is_active       = models.BooleanField(_('Active status'), default=True)

    date_joined     = models.DateTimeField(_('Account created'), default=timezone.now, editable=False)
    last_seen       = models.DateTimeField(_('Last seen'), auto_now=True, db_index=True)
    is_verified     = models.BooleanField(_('Account verified'), default=False, blank=True,
                                       help_text=_(verify_help_text))

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        abstract = False
        verbose_name        = _('account')
        verbose_name_plural = _('accounts')
        indexes = [
            models.Index(
                name="account_is_verified",
                fields=["is_verified"],
                condition=Q(is_verified=True), ), ]

    def __str__(self):
        return f'{self.username} account'

    def has_recently_joined(self):
        now = timezone.now()
        interval = datetime.timedelta(days=7)
        return now - interval <= self.date_joined <= now

    def set_new_username(self, new_username: str):
        new_username = self.normalize_username(new_username)
        if not re.match(r'^\w+$', new_username):
            raise ValueError(user_help_text)
        if Account.objects.filter(username=new_username).exists():
            raise ValueError(user_error_text)
        else:
            if new_username != self.username:
                self.username = new_username
            else:
                raise ValueError("New username cannot be old username")

    def set_new_email(self, new_email: str):
        new_email = self.normalize_email(new_email)
        if not re.match(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]+$", new_email):
            raise ValueError(email_regex_text)
        if Account.objects.filter(email=new_email).exists():
            raise ValueError(email_error_text)
        else:
            if new_email != self.email:
                self.email = new_email
            else:
                raise ValueError("New email cannot be old email")

    @staticmethod
    def normalize_email(new_email: str):
        return new_email.lower()
