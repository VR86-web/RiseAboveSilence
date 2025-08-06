
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile
from .. import settings

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_and_send_email(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        send_mail(
            subject='Welcome to Rise Above Silence!',
            message='Thanks for joining our community. You can now create and share posts.',
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False,
        )

