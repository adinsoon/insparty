from .models import Technology, Specialization
from django.db.utils import IntegrityError
from django.test import TestCase
from faker import Factory

faker = Factory.create()


def setup_techs(name: str):
    """
    Create technology with given name.
    """
    return Technology.objects.create(name=name)


def setup_specs(name: str):
    """
    Create specialization with given name.
    """
    return Specialization.objects.create(name=name)


class TechsTests(TestCase):

    def test_create_existing_technology(self):
        """
        Check if it is possible to create technology with existing name.
        """
        name = faker.word()
        tech = setup_techs(name=name)
        self.assertRaises(IntegrityError, setup_techs, name)


class SpecsTests(TestCase):

    def test_create_existing_specialization(self):
        """
        Check if it is possible to create specialization with existing name.
        """
        name = faker.word()
        spec = setup_specs(name=name)
        self.assertRaises(IntegrityError, setup_specs, name)
