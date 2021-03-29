from django.core.validators import ValidationError
from django.contrib.auth import get_user_model
from .utils import custom_slugify
from django.test import TestCase
from django.conf import settings
from faker import Factory
from .models import Idea
import datetime

faker = Factory.create()
Account = get_user_model()
faker.seed(0)


def setup_account():
    return Account.objects.create(username=faker.user_name(), email=faker.email(),
                                  password=faker.password())


def setup_idea(founder, **kwargs):
    return Idea.objects.create(founder=founder, **kwargs)


class IdeaTests(TestCase):

    def test_title_slug(self):
        """
        Check if slug is properly made.
        """
        title = faker.text(max_nb_chars=200)
        result = custom_slugify(title)
        expected = '-'.join(title.split()).replace(".", "").lower() + '---'
        self.assertEqual(result[:-5], expected)

    def test_validate_founder(self):
        f"""
        Check if founder can create more than {settings.FOUNDER_IDEAS_LIMIT} ideas.
        """
        account = setup_account()
        for i in range(settings.FOUNDER_IDEAS_LIMIT+1):
            try:
                title = faker.text(max_nb_chars=200)
                description = faker.text(max_nb_chars=200)
                setup_idea(account.founder, title=title, description=description)
            except ValidationError:
                continue
