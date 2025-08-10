from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from RiseAboveSilence import settings
from RiseAboveSilence.posts.models import Post


# 1. Notify moderators when a new post is created (and not yet approved)

UserModel = get_user_model()


@receiver(post_save, sender=Post)
def notify_moderators_on_post_create(sender, instance, created, **kwargs):
    if created and not instance.is_approved:
        try:
            group = Group.objects.get(name="Post Approvers")
            emails = list(group.user_set.values_list("email", flat=True))
            if emails:
                subject = "A new post is awaiting approval"

                # Safely get username or fallback to email
                username = getattr(instance.user, "username", None) or instance.user.email

                plain_message = f"Title: {instance.title}\nUser: {username}"

                # Simple HTML version
                html_message = render_to_string('email/email.html', {
                    'subject': subject,
                    'recipient_name': username,
                    'message_body': f'Title: {instance.title}\nUser: {username}',
                })

                email = EmailMultiAlternatives(subject, plain_message, settings.COMPANY_EMAIL, emails)
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=False)
        except Group.DoesNotExist:
            pass


@receiver(pre_save, sender=Post)
def cache_approval_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Post.objects.get(pk=instance.pk)
            instance._was_approved = old_instance.is_approved
        except Post.DoesNotExist:
            instance._was_approved = False
    else:
        instance._was_approved = False


@receiver(post_save, sender=Post)
def notify_user_post_approved(sender, instance, created, **kwargs):
    if (
        not created
        and not getattr(instance, "_was_approved", True)
        and instance.is_approved
    ):
        username = getattr(instance.user, "username", None) or instance.user.email

        subject = "Your post has been approved!"
        plain_message = f'Your post "{instance.title}" is now live on the site.'

        html_message = render_to_string('email/email.html', {
            'subject': subject,
            'recipient_name': username,
            'message_body': f'Your post "{instance.title}" is now live on the site.',
        })

        email = EmailMultiAlternatives(subject, plain_message, settings.COMPANY_EMAIL, [instance.user.email])
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
