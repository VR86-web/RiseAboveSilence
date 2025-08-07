from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from RiseAboveSilence import settings
from RiseAboveSilence.posts.models import Post


# 1. Notify moderators when a new post is created (and not yet approved)
@receiver(post_save, sender=Post)
def notify_moderators_on_post_create(sender, instance, created, **kwargs):
    if created and not instance.is_approved:
        try:
            group = Group.objects.get(name="Post Approvers")
            emails = group.user_set.values_list("email", flat=True)
            send_mail(
                subject="A new post is awaiting approval",
                message=f"Title: {instance.title}\nUser: {instance.user.username}",
                from_email=settings.COMPANY_EMAIL,
                recipient_list=list(emails),
                fail_silently=False,
            )
        except Group.DoesNotExist:
            pass


# 2. Cache old is_approved value BEFORE saving
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


# 3. Notify user only if post was just approved
@receiver(post_save, sender=Post)
def notify_user_post_approved(sender, instance, created, **kwargs):
    if (
        not created
        and not getattr(instance, "_was_approved", True)
        and instance.is_approved
    ):
        print(f"✅ Post approved. Sending email to: {instance.user.email}")

        send_mail(
            subject="Your post has been approved!",
            message=f'Your post "{instance.title}" is now live on the site.',
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=False,
        )
