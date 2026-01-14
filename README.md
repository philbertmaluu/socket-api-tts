# Socket API 2026

Django-based API project with a structured architecture.

## Project Structure

```
socket2026/
├── apps/                    # Application modules
│   ├── users/              # Users app
│   │   ├── models/         # Database models
│   │   ├── views/          # API views
│   │   ├── serializers/    # API serializers
│   │   ├── services/       # Business logic
│   │   ├── selectors/      # Database queries
│   │   ├── signals/        # Django signals
│   │   └── tests/          # Test files
│   ├── sockets/            # Sockets app (to be implemented)
│   └── other/              # Other apps (to be implemented)
├── config/                 # Project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # Root URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── requirement/            # Requirements files
│   ├── base.txt            # Base dependencies
│   ├── development.txt     # Development dependencies
│   └── production.txt      # Production dependencies
└── manage.py               # Django management script
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirement/base.txt
```

### 3. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` and set your configuration:
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### 4. Database Setup

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Architecture

### Models
- Located in `apps/{app_name}/models/`
- Each model should be in its own file
- Export models from `models/__init__.py`

### Views
- Located in `apps/{app_name}/views/`
- Handle HTTP requests and responses

### Serializers
- Located in `apps/{app_name}/serializers/`
- Handle data serialization/deserialization

### Services
- Located in `apps/{app_name}/services/`
- Contains business logic
- Should be called from views

### Selectors
- Located in `apps/{app_name}/selectors/`
- Contains database query logic
- Separates query logic from views and services

## Custom User Model

This project uses a custom User model (`apps.users.models.User`). Make sure to run migrations before creating any users.

## Testing

Run tests:

```bash
python manage.py test
```

## Security Notes

⚠️ **Important**: 
- Never commit `.env` file to version control
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data

## License

[Add your license here]
