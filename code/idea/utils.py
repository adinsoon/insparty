from django.utils.crypto import get_random_string
from django.utils.text import slugify


def custom_slugify(content):
    content = slugify(content)
    addon = get_random_string(5)
    content = content + '-' + addon
    return content
