
# 🛠️ Project Setup Instructions

## ✅ Prerequisites

To run this project, you will need:

- Python 3.10+
- PostgreSQL (for database)
- pip (Python package installer)
- virtualenv (recommended)

---

## 📦 Setup Guide

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

---

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables

Copy the `.env.template` file and rename it to `.env`:

```bash
cp .env.template .env
```

Edit the `.env` file and fill in the required values:

- `SECRET_KEY`: Django secret key.
- `DEBUG`: `True` for development, `False` for production.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`: PostgreSQL DB settings.
- `ALLOWED_HOSTS`: Hosts allowed to serve the app.
- `CSRF_TRUSTED_ORIGINS`: For CSRF protection.
- `EMAIL_*`: SMTP email credentials.
- `CLOUDINARY_*`: Cloudinary media storage keys.
- `GOOGLE_MAPS_API_KEY`: Used in map-related features.

---

### Step 5: Set Up the Database

Make sure PostgreSQL is running and you’ve created a database with matching credentials.

Apply migrations:

```bash
python manage.py migrate
```

---

### Step 6: Create a Superuser

To access the Django admin and other restricted areas:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your superuser account.

---

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The app will be accessible at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔍 API & URL Overview

- Home: `/`
- About: `/about/`
- Auth: `/accounts/login/`, `/accounts/register/`, `/accounts/logout/`
- Posts: `/post/all_posts/`, `/post/add_post/`, `/post/<id>/details/`, etc.
- Comments: `/<post_id>/comments/`, `/<post_id>/comment/<comment_id>/reply/`
- API (AJAX):
  - Toggle Like: `/api/posts/<post_id>/like/`
  - New Comments Polling: `/api/new-comments/`

---

## 🧪 Running Tests

To run the test suite:

```bash
python manage.py test
```

Tests are located in the `tests/` directory.

---

## 📝 Notes

- Static files are managed using WhiteNoise.
- Media files are stored in Cloudinary.
- Admin Panel uses **django-unfold** for a modern interface.