## 🛎️ Signals

Signals in Django act as **event listeners** — they allow certain logic to run automatically when specific actions occur, such as saving a model. Below are the custom signals implemented in **Rise Above Silence**.

---

### 🪧 Signal: `create_user_and_send_email`

#### 📋 Overview
This signal ensures that:
- A `Profile` is automatically created when a new `CustomUser` is registered.
- A welcome email is sent to the user after successful registration.

#### ⚙️ How It Works

- **Signal Type**: `post_save`  
- **Triggered When**: A new user is created (`created=True`)

#### 🔄 Behavior
When a new user registers:
1. Django fires the `post_save` signal.
2. The receiver:
   - Ensures the user has a `Profile` using `get_or_create()`.
   - Sends a welcome email using `send_mail()`.

#### 📘 Example Code

```python
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
```

---

### 🪧 Signal: `notify_moderators_on_post_create`

#### 📋 Overview
Notifies moderators via email when a **new post** is created but **not yet approved**.

#### ⚙️ How It Works

- **Signal Type**: `post_save`
- **Triggered When**: A new `Post` is created with `is_approved=False`

#### 🔄 Behavior
1. Looks for users in the `Post Approvers` group.
2. Sends an email notification to all their email addresses.

#### 📘 Example Code

```python
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from RiseAboveSilence import settings
from RiseAboveSilence.posts.models import Post

@receiver(post_save, sender=Post)
def notify_moderators_on_post_create(sender, instance, created, **kwargs):
    if created and not instance.is_approved:
        try:
            group = Group.objects.get(name='Post Approvers')
            emails = group.user_set.values_list('email', flat=True)
            send_mail(
                subject='A new post is awaiting approval',
                message=f'Title: {instance.title}\nUser: {instance.user.username}',
                from_email=settings.COMPANY_EMAIL,
                recipient_list=list(emails),
                fail_silently=False,
            )
        except Group.DoesNotExist:
            pass
```

---

### 🪧 Signal: `cache_approval_status`

#### 📋 Overview
Stores the **previous approval status** of a post before saving, so you can detect approval changes.

#### ⚙️ How It Works

- **Signal Type**: `pre_save`
- **Triggered When**: A `Post` is about to be saved

#### 🔄 Behavior
- Retrieves the current `is_approved` value from the database.
- Caches it on the instance using `instance._was_approved`.

#### 📘 Example Code

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from RiseAboveSilence.posts.models import Post

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
```

---

### 🪧 Signal: `notify_user_post_approved`

#### 📋 Overview
Sends an email to the user **only when their post has just been approved**.

#### ⚙️ How It Works

- **Signal Type**: `post_save`
- **Triggered When**:
  - Post is updated (not newly created)
  - `is_approved` changed from `False` to `True`

#### 🔄 Behavior
- Uses the `_was_approved` flag set by the `pre_save` signal.
- Sends an email to the post author confirming approval.

#### 📘 Example Code

```python
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from RiseAboveSilence import settings
from RiseAboveSilence.posts.models import Post

@receiver(post_save, sender=Post)
def notify_user_post_approved(sender, instance, created, **kwargs):
    if not created and not getattr(instance, "_was_approved", True) and instance.is_approved:
        send_mail(
            subject='Your post has been approved!',
            message=f'Your post "{instance.title}" is now live on the site.',
            from_email=settings.COMPANY_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=False,
        )
```
