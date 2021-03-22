from django.core.validators import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Factory
import datetime

faker = Factory.create()
Account = get_user_model()
faker.seed(0)


def setup_account():
    return Account.objects.create(username=faker.user_name(), email=faker.email(),
                                  password=faker.password())


class AccountTests(TestCase):

    def test_set_new_illegal_username(self):
        """
        Check if user can change his username using illegal characters.
        """
        account = setup_account()
        illegal_usernames = ['!l#g$l', 'johndoe ', 'john doe', '!john!doe', 'john@doe.com',
                             '_j)hn']
        for username in illegal_usernames:
            self.assertRaises(ValueError, account.set_new_username, username)

    def test_set_used_username(self):
        """
        Check if user can change his username using same username as before or using
        username used by someone else.
        """
        account_first  = setup_account()
        account_second = setup_account()
        used_username  = account_first.username
        self.assertRaises(ValueError, account_first.set_new_username, used_username)
        used_username  = account_second.username
        self.assertRaises(ValueError, account_first.set_new_username, used_username)

    def test_set_new_illegal_email(self):
        """
        Check if user can change his email using illegal record.
        """
        account = setup_account()
        illegal_emails = ['!l#g$l', '!l#g$l@example.com', '@example.com', '@', 'johndoe@example',
                         'johndoe@com.', 'sample.example@com', 'some white@space.com']
        for email in illegal_emails:
            self.assertRaises(ValueError, account.set_new_email, email)

    def test_set_used_email(self):
        """
        Check if user can change his email using same email as before or using
        email used by someone else.
        """
        account_first  = setup_account()
        account_second = setup_account()
        used_email = account_first.email
        self.assertRaises(ValueError, account_first.set_new_email, used_email)
        used_email = account_second.email
        self.assertRaises(ValueError, account_first.set_new_email, used_email)

    def test_clean_phone_validator(self):
        """
        Check if user can enter illegal phone number.
        """
        account = setup_account()
        illegal_phones = ['561781289d', '-561781289', '++561781289', '27636712+',
                          '123+123123', '+343334213 ']
        for phone in illegal_phones:
            account.phone = phone
            self.assertRaises(ValidationError, account.full_clean)

    def test_clean_linkedin_validator(self):
        """
        Check if user can enter illegal linkedin field url.
        """
        account = setup_account()
        illegal_urls = ["example.com", "https://sample.com", "sample.com/in/sample",
                        "linkedin.com/in//ss", "linkedin.com/in/ss?next=sample.com",
                        "linkedin.com/in/aa/ad", "linkedincom/in/aa",
                        "linkedin.com/insparty/aa", "linkedin.com/in/test.com",
                        " linkedin.com/in/test", "linkedin.com/in/test "]
        for url in illegal_urls:
            account.linkedin = url
            self.assertRaises(ValidationError, account.full_clean)

    def test_clean_repository_validator(self):
        """
        Check if user can enter illegal repository field url.
        """
        account = setup_account()
        illegal_repos = ["sample.com", " git@bitbucket.org:username/reponame.git",
                         "git@bitbucket.org:username/reponame.git ", "sample@git.com",
                         "git@git/repo.git?next=sample.com", "git@git/repo?next=sample.com",
                         "gitlab.com@git/git", "repo@repo.org/sample=sample"]
        for repo in illegal_repos:
            account.repository = repo
            self.assertRaises(ValidationError, account.full_clean)

    def test_clean_experience_validator(self):
        """
        Check if user can enter illegal experience choice.
        """
        account = setup_account()
        account.experience = "invalid"
        self.assertRaises(ValidationError, account.full_clean)

    def test_clean_multiple_experiences(self):
        """
        Check if user can enter multiple experience choices, even if they are correct.
        """
        account = setup_account()
        account.experience = ["N", "J"]
        self.assertRaises(ValidationError, account.full_clean)

    def test_clean_sex_validator(self):
        """
        Check if user can enter illegal sex choice.
        """
        account = setup_account()
        account.experience = "sensitive"
        self.assertRaises(ValidationError, account.full_clean)

    def test_clean_multiple_sex(self):
        """
        Check if user can enter multiple sex choices, even if they are correct.
        """
        account = setup_account()
        account.experience = ["M", "F"]
        self.assertRaises(ValidationError, account.full_clean)

    def test_birthdate_in_the_future(self):
        """
        Check if user can enter birthdate from future.
        """
        account = setup_account()
        now = datetime.datetime.today()
        future = now + datetime.timedelta(days=1)
        account.birthdate = future
        self.assertRaises(ValidationError, account.full_clean)

    def test_birthdate_current_date(self):
        """
        Check if user can enter current date as a birthdate
        """
        account = setup_account()
        now = datetime.datetime.today()
        account.birthdate = now
        self.assertRaises(ValidationError, account.full_clean)

    def test_birthdate_user_too_young(self):
        """
        Check if the user can use the site while being too young.
        """
        account = setup_account()
        now = datetime.datetime.today()
        year = 13
        birthdate = datetime.date(now.year-year, now.month, now.day)
        account.birthdate = birthdate
        self.assertRaises(ValidationError, account.full_clean)
