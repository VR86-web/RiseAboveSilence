## 📝 Overview

The **Rise Above Silence Platform** is a social content and communication system where users can create posts, comment, like content, and share news updates. The models are designed to keep the system modular and scalable, enabling new social features to be added with minimal changes to the core structure.

The main components are:

- **CustomUser Model:** A custom authentication model replacing Django’s default user, using email and username as unique identifiers.
- **Profile Model:** Extends the user with additional personal information like name, date of birth, country, and profile picture.
- **Post and Comment Models:** Allow users to publish content and engage in threaded discussions.
- **Like Model:** Captures user reactions to posts.
- **News Model:** Supports publishing announcements or news items to the community.

These models work together to support a flexible, user-driven content ecosystem.


---

### 📄 Model: CustomUser

**CustomUser**  
A custom user model that uses email and username as unique identifiers. It is the foundation for authentication and permission management.

| Field            | Type                     | Description                                               |
|------------------|--------------------------|-----------------------------------------------------------|
| email            | EmailField               | Unique email address.                                     |
| username         | CharField                | Unique username used for authentication.                 |
| is_active        | BooleanField             | Whether the account is active. Default is `True`.        |
| is_staff         | BooleanField             | Indicates if the user has staff privileges.              |
| password         | (inherited)              | Hashed password field from `AbstractBaseUser`.           |
| groups           | (inherited)              | User groups for permission management.                   |
| user_permissions | (inherited)              | Specific permissions assigned to the user.               |

**Meta Options**  
- No additional options specified (uses Django defaults).  
- `__str__`: Returns the username for clarity.

---

### 📄 Model: Profile

**Profile**  
Extends the user with optional personal information, allowing each user to enrich their identity within the system.

| Field            | Type            | Description                                                |
|------------------|-----------------|------------------------------------------------------------|
| user             | OneToOneField   | Links to `CustomUser`. Primary key.                       |
| first_name       | CharField       | Optional first name.                                      |
| last_name        | CharField       | Optional last name.                                       |
| date_of_birth    | DateField       | Optional date of birth.                                   |
| country          | CountryField    | Optional country selection.                               |
| profile_picture  | CloudinaryField | Optional profile image uploaded to Cloudinary.            |

**Meta Options**  
- `__str__`: Returns full name if available, otherwise email.

---

### 📄 Model: Post

**Post**  
Represents a user-created post. Serves as a primary content unit in the platform for engagement.

| Field       | Type          | Description                                     |
|-------------|---------------|-------------------------------------------------|
| title       | CharField     | Title of the post.                              |
| content     | TextField     | Main content/body of the post.                  |
| user        | ForeignKey    | Author of the post (`CustomUser`).              |
| created_at  | DateTimeField | Timestamp when the post was created.            |

**Meta Options**  
- `ordering = ['-created_at']`: Latest posts appear first.  
- `__str__`: Returns a truncated title for easy identification.

---

### 📄 Model: Comment

**Comment**  
Allows users to leave feedback or reply to posts and other comments in a nested structure.

| Field      | Type          | Description                                                     |
|------------|---------------|-----------------------------------------------------------------|
| to_post    | ForeignKey    | The post this comment belongs to.                               |
| user       | ForeignKey    | Author of the comment (`CustomUser`).                           |
| content    | TextField     | Text content of the comment.                                    |
| created_at | DateTimeField | Timestamp when the comment was created.                         |
| parent     | ForeignKey    | Optional link to parent comment for nested replies.             |

**Meta Options**  
- `ordering = ['created_at']`: Oldest comments appear first.  
- `__str__`: Returns a preview of the comment content.  
- `indexes`: Could be added for `to_post` and `parent` to improve query speed.

---

### 📄 Model: Like

**Like**  
Captures user engagement on posts. Each like is tied to a user and a post.

| Field    | Type        | Description                                     |
|----------|-------------|-------------------------------------------------|
| to_post  | ForeignKey  | The post that was liked.                        |
| user     | ForeignKey  | User who liked the post (`CustomUser`).         |

**Meta Options**  
- `unique_together = ('to_post', 'user')`: Prevents duplicate likes by the same user.  
- `__str__`: Returns a formatted string indicating the user and post liked.

---

### 📄 Model: News

**News**  
Represents an informational update or announcement shared by the platform administrators.

| Field       | Type            | Description                                         |
|-------------|-----------------|-----------------------------------------------------|
| title       | CharField       | Title of the news item.                              |
| content     | TextField       | Main body of the news.                               |
| image       | CloudinaryField | Optional image associated with the news.            |
| created_at  | DateTimeField   | Timestamp when the news was created.                |

**Meta Options**  
- `ordering = ['-created_at']`: Newest news items appear first.  
- `__str__`: Returns the title for quick identification.

---
