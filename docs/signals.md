## 🛎️ Signals

Signals are hooks that allow you to **execute logic automatically** when certain events occur in your Django application.

---

### 🪧 Signal: create_user_profile

**Overview**

The `create_user_profile` signal ensures that **every user has an associated profile**.  
When a new `CustomUser` is created, this signal automatically generates a linked `Profile` instance.

---

#### ⚙️ How It Works

- **Signal Type:**  
  `post_save` — fires after a `CustomUser` is saved to the database.

- **Trigger Condition:**  
  Only runs when:
  - A new user is created (`created=True`), and
  - The user does not already have a related `Profile`.

---

#### 🔄 Behavior

When a user is created:
1. Django fires the `post_save` signal.
2. The `create_user_profile` receiver checks whether this is a **new instance**.
3. If the user has no profile yet, a new `Profile` object is created and linked to the user.

---

#### 📘 Example Code

```python
@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
