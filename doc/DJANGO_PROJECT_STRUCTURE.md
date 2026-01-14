# Django Project Structure Explained

## Overview
When you run `django-admin startproject projectname`, Django creates a default project structure. Here's a complete breakdown of each folder and file.

## Default Folder Structure

```
socket2026/                    # Root project directory
├── manage.py                  # Django's command-line utility
├── db.sqlite3                 # SQLite database (created after migrations)
└── socket2026/                # Project package (inner directory)
    ├── __init__.py           # Makes the directory a Python package
    ├── settings.py           # Project settings/configuration
    ├── urls.py               # Root URL configuration
    ├── wsgi.py               # WSGI config for production deployment
    └── asgi.py               # ASGI config for async/WebSocket support
```

---

## File-by-File Explanation

### 1. `manage.py`
**Location:** Root directory  
**Purpose:** Django's command-line utility for administrative tasks

**Functions:**
- **`main()`**: Entry point that:
  1. Sets the default Django settings module (`DJANGO_SETTINGS_MODULE`)
  2. Imports Django's command execution system
  3. Executes commands from the command line (like `runserver`, `migrate`, `createsuperuser`)

**Common Commands:**
- `python manage.py runserver` - Start development server
- `python manage.py migrate` - Apply database migrations
- `python manage.py createsuperuser` - Create admin user
- `python manage.py makemigrations` - Create migration files
- `python manage.py shell` - Open Django shell

---

### 2. `socket2026/__init__.py`
**Location:** `socket2026/socket2026/__init__.py`  
**Purpose:** Makes the directory a Python package (allows imports)

**Content:** Usually empty, but can contain initialization code that runs when the package is imported.

---

### 3. `socket2026/settings.py`
**Location:** `socket2026/socket2026/settings.py`  
**Purpose:** Central configuration file for your Django project

**Key Settings Explained:**

#### **Path Configuration**
- **`BASE_DIR`**: Points to the project root directory (parent of settings.py)
  ```python
  BASE_DIR = Path(__file__).resolve().parent.parent
  ```

#### **Security Settings**
- **`SECRET_KEY`**: Cryptographic key for sessions, CSRF protection, etc. (KEEP SECRET!)
- **`DEBUG`**: 
  - `True` = Development mode (shows detailed error pages)
  - `False` = Production mode (hides errors, shows generic pages)
- **`ALLOWED_HOSTS`**: List of host/domain names your site can serve (empty = localhost only)

#### **Application Definition**
- **`INSTALLED_APPS`**: List of Django applications enabled for this project
  - `django.contrib.admin` - Admin interface
  - `django.contrib.auth` - Authentication system
  - `django.contrib.contenttypes` - Content type framework
  - `django.contrib.sessions` - Session framework
  - `django.contrib.messages` - Messaging framework
  - `django.contrib.staticfiles` - Static file handling

#### **Middleware**
- **`MIDDLEWARE`**: List of middleware classes (processes requests/responses)
  - `SecurityMiddleware` - Security enhancements
  - `SessionMiddleware` - Session management
  - `CommonMiddleware` - Common operations
  - `CsrfViewMiddleware` - CSRF protection
  - `AuthenticationMiddleware` - User authentication
  - `MessageMiddleware` - Message framework
  - `XFrameOptionsMiddleware` - Clickjacking protection

#### **URL Configuration**
- **`ROOT_URLCONF`**: Points to the root URL configuration file (`'socket2026.urls'`)

#### **Templates**
- **`TEMPLATES`**: Template engine configuration
  - `BACKEND`: Template engine (Django templates)
  - `DIRS`: Additional template directories
  - `APP_DIRS`: Search for templates in app directories
  - `context_processors`: Variables available in all templates

#### **Database**
- **`DATABASES`**: Database configuration
  - Default: SQLite (`db.sqlite3` file)
  - Can be changed to PostgreSQL, MySQL, etc.

#### **Password Validation**
- **`AUTH_PASSWORD_VALIDATORS`**: Password strength validators
  - Checks similarity to user attributes
  - Minimum length requirements
  - Common password detection
  - Numeric-only password detection

#### **Internationalization**
- **`LANGUAGE_CODE`**: Default language (`'en-us'`)
- **`TIME_ZONE`**: Default timezone (`'UTC'`)
- **`USE_I18N`**: Enable internationalization
- **`USE_TZ`**: Enable timezone support

#### **Static Files**
- **`STATIC_URL`**: URL prefix for static files (`'static/'`)

---

### 4. `socket2026/urls.py`
**Location:** `socket2026/socket2026/urls.py`  
**Purpose:** Root URL dispatcher - maps URLs to views

**Functions:**
- **`urlpatterns`**: List of URL patterns
  - `path('admin/', admin.site.urls)` - Maps `/admin/` to Django admin interface

**How it works:**
- Django starts here when a request comes in
- Matches URL patterns and routes to corresponding views
- Can include other URL configurations using `include()`

**Example:**
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # Include app URLs
    path('', views.home, name='home'),    # Map to a view function
]
```

---

### 5. `socket2026/wsgi.py`
**Location:** `socket2026/socket2026/wsgi.py`  
**Purpose:** WSGI (Web Server Gateway Interface) configuration for production deployment

**Functions:**
- **`get_wsgi_application()`**: Returns the WSGI application callable
- **`application`**: WSGI application object used by production servers

**Usage:**
- Used by production servers (Gunicorn, uWSGI, Apache mod_wsgi)
- Standard interface between web servers and Python web applications
- Synchronous (traditional request/response)

**Key Code:**
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socket2026.settings')
application = get_wsgi_application()
```

---

### 6. `socket2026/asgi.py`
**Location:** `socket2026/socket2026/asgi.py`  
**Purpose:** ASGI (Asynchronous Server Gateway Interface) configuration for async/WebSocket support

**Functions:**
- **`get_asgi_application()`**: Returns the ASGI application callable
- **`application`**: ASGI application object used by async servers

**Usage:**
- Used for WebSocket support, async views, and HTTP/2
- Required for Django Channels (real-time features)
- Can handle both sync and async requests

**Key Code:**
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socket2026.settings')
application = get_asgi_application()
```

**Difference from WSGI:**
- WSGI: Synchronous, traditional HTTP requests
- ASGI: Asynchronous, supports WebSockets, HTTP/2, and async views

---

## Additional Files Created During Development

### `db.sqlite3`
- SQLite database file (created after running `migrate`)
- Stores all your application data
- **Note:** Not included in version control typically

### `__pycache__/`
- Python bytecode cache directory
- Created automatically by Python
- Speeds up imports
- **Note:** Not included in version control

---

## Typical Workflow

1. **Create Project:** `django-admin startproject projectname`
2. **Create App:** `python manage.py startapp appname`
3. **Configure:** Edit `settings.py` (add app, configure database, etc.)
4. **Create Models:** Define models in `appname/models.py`
5. **Create Migrations:** `python manage.py makemigrations`
6. **Apply Migrations:** `python manage.py migrate`
7. **Create Views:** Define views in `appname/views.py`
8. **Configure URLs:** Add URL patterns in `appname/urls.py` and include in root `urls.py`
9. **Run Server:** `python manage.py runserver`

---

## Summary

| File | Purpose | Key Function |
|------|---------|--------------|
| `manage.py` | Command-line utility | `main()` - Executes Django commands |
| `settings.py` | Project configuration | Contains all settings (database, apps, middleware, etc.) |
| `urls.py` | URL routing | `urlpatterns` - Maps URLs to views |
| `wsgi.py` | Production deployment (sync) | `application` - WSGI callable |
| `asgi.py` | Async/WebSocket support | `application` - ASGI callable |
| `__init__.py` | Package marker | Makes directory a Python package |

---

## Best Practices

1. **Never commit `SECRET_KEY`** - Use environment variables in production
2. **Set `DEBUG = False`** in production
3. **Configure `ALLOWED_HOSTS`** for production
4. **Use environment variables** for sensitive settings
5. **Keep `db.sqlite3`** out of version control (use `.gitignore`)
6. **Use `ASGI`** if you need WebSocket or async support
