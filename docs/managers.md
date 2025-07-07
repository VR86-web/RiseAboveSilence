## ⚙️ Managers

Managers in Django handle model-level operations and encapsulate query logic and object creation workflows. This project defines a custom manager for the `CustomUser` model to replace Django’s default user creation mechanisms.

---

### 🧩 Manager: CustomUserManager

**Overview**

`CustomUserManager` is a specialized manager responsible for creating user and superuser accounts in a consistent, secure way. It overrides the default behavior to support the custom `CustomUser` model, ensuring email normalization and proper flag settings for staff and superuser roles.

---

#### 📘 Methods

| Method | Description |
|--------|-------------|
| **_create_user(username, email, password, \*\*extra_fields)** | Core utility method that handles user creation. Normalizes the email and username, hashes the password, and saves the user instance. Used internally by `create_user()` and `create_superuser()`. |
| **create_user(username, email=None, password=None, \*\*extra_fields)** | Public method for creating regular users. Automatically sets `is_staff=False` and `is_superuser=False`. |
| **create_superuser(username, email=None, password=None, \*\*extra_fields)** | Public method for creating superusers. Validates that `is_staff` and `is_superuser` are both `True`. |

---

#### 🛡️ Important Details

- **Validation:**  
  - Ensures `username` is always provided.
  - Enforces that superusers have both `is_staff` and `is_superuser` set to `True`.

- **Password Security:**  
  - Uses `make_password()` to securely hash the password before storing it.

- **Normalization:**  
  - Email addresses are normalized via `self.normalize_email(email)`.
  - Usernames are normalized using Django’s `normalize_username()`.

---

#### ✨ Example Usage

```python
# Create a regular user
CustomUser.objects.create_user(
    username="john_doe",
    email="john@example.com",
    password="securepassword123"
)

# Create a superuser
CustomUser.objects.create_superuser(
    username="admin",
    email="admin@example.com",
    password="supersecurepassword"
)
