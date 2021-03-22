from django.urls import path
from .test_views import test_email

urlpatterns = [
    path('', test_email, name='email')
]
