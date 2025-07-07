
# Documentation

___

## Project Overview

**"Rise Above Silence"** is an online platform dedicated to empowering women by providing crucial information and support to help prevent and respond to violence. It serves as a safe space where users can:

- Access educational resources on identifying and addressing abuse  
- Share personal experiences and coping strategies through posts  
- Read practical advice and real-life stories from others  

The platform’s goal is to raise awareness, foster community support, and encourage early action against gender-based violence.

***

## Contents

___

### Setup Tutorials

- 📦 **[Project Setup](docs/setup.md)**  
  Step-by-step instructions to get your development environment up and running.

***

## 📊 Entity Relationship Diagram

[View ER Diagram](docs/er_diagram.png)

___

### Key parts

- [Models](docs/models.md)
- [Managers](docs/managers.md)
- [Mixins](docs/mixins.md)
- [Signals](docs/signals.md)

***

### 🧩 Key Components

Below is a summary of the most important building blocks of the project and their purpose.

---

### 🔹 Custom User Model

We use a **custom user model (`CustomUser`)** based on `AbstractBaseUser` to allow authentication via email and username.  
This gives us flexibility to extend user fields and customize permissions.

---

### 🔹 Profile Model

A **Profile** model stores additional user information (first name, last name, date of birth, country, and profile picture).  
It is linked via a `OneToOneField` to ensure every user has exactly one profile.

---

### 🔹 Custom User Manager

The `CustomUserManager` handles **user creation logic**:
- `create_user()` creates a standard user.
- `create_superuser()` creates an admin with staff and superuser permissions.
- `_create_user()` normalizes email and username and securely hashes the password.

This centralizes the logic for creating any kind of user.

---

### 🔹 Signal for Automatic Profile Creation

A **post-save signal (`create_user_profile`)** automatically creates a `Profile` whenever a new user is registered.  
This guarantees that all users always have a profile without requiring extra steps.

---

### 🔹 DisableFieldsMixin

The `DisableFieldsMixin` is a form mixin used in delete forms.  
It automatically **disables fields in the form** when displaying confirmation dialogs, so users cannot modify data while deleting.  
You use this mixin, for example, in:
- Profile deletion forms
- Post deletion forms

---

### 🔹 Post, Comment, Like, and News Models

These models enable social features:
- **Post:** User-generated content.
- **Comment:** Hierarchical comments with optional nested replies.
- **Like:** Keeps track of which users liked which posts.
- **News:** Admin-created content for broadcasting announcements.

They form the backbone of user interaction and content sharing.

---

### 🔹 Media Handling with Cloudinary

**Profile pictures** and **news images** are stored via Cloudinary (`CloudinaryField`) for efficient media management and delivery.

---

### 🔹 Entity Relationship Diagram (ER Diagram)

The **ER diagram** visually illustrates all model relationships.


---

**Summary**

These components work together to create a **flexible, user-centric platform** that manages authentication, profiles, social content, and media—all while ensuring data consistency and a smooth user experience.
