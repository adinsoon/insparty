from django.contrib.auth import get_user_model
from .models import Founder, Finder
from django.test import TestCase
from faker import Factory

faker = Factory.create()
Account = get_user_model()
faker.seed(0)


def setup_account():
    return Account.objects.create(username=faker.user_name(), email=faker.email(),
                                  password=faker.password())


class FounderTests(TestCase):

    def test_founder_model_created(self):
        """
        Check if signal is properly designed for Founder model.
        """
        account = setup_account()
        self.assertTrue(Founder.objects.filter(account=account).exists())


class FinderTests(TestCase):

    def test_finder_model_created(self):
        """
        Check if signal is properly designed for Finder model.
        """
        account = setup_account()
        self.assertTrue(Finder.objects.filter(account=account).exists())
