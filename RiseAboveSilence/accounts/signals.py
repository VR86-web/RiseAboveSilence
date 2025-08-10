from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from .. import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_and_send_email(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

        subject = "Welcome to Rise Above Silence!"
        from_email = settings.COMPANY_EMAIL
        to_email = instance.email

        recipient_name = getattr(instance, 'first_name', None)
        if not recipient_name:
            recipient_name = getattr(instance, 'username', None)
        if not recipient_name:
            recipient_name = instance.email

        context = {
            'subject': subject,
            'recipient_name': recipient_name,
            'message_body': "Thanks for joining our community. You can now create and share posts.",
        }

        html_content = render_to_string('email/email.html', context)

        text_content = f"""
        Hello {recipient_name},

        {context['message_body']}

        Best regards,
        Rise Above Silence Team

        If you no longer wish to receive these emails, please ignore this message.
        """

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)


