from django.shortcuts import HttpResponse
from django.conf import settings
from .test_tasks import send_email_task


def test_email(request):
    subject = 'This is test email.'
    message = "Lorem ipsum dolor sit a"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['contact.insparty@gmail.com']
    # I noticed that the celery was unable to deliver more complex messages
    # (like with newlines in the example above causing following error)
    # >> AttributeError: 'NoneType' object has no attribute 'rsplit'
    # so the quick solution was to
    # rsplit message at first and then make it a 'cleaned' string again.
    # TODO: discover what causes this error
    message = ' '.join(message.rsplit())
    message = str(message)
    send_email_task.delay(subject, message, from_email, recipient_list)
    return HttpResponse('<center><h1> Email has been sent! <h1></center>')
