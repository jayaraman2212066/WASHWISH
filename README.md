# WashWish - Laundry Management System

A Django-based laundry management system for managing laundry services, orders, and customer accounts.

## Features

- User registration and authentication
- Service management
- Order tracking
- Payment processing
- Admin dashboard
- Responsive web design

## Technology Stack

- **Backend**: Django 3.1.7
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Deployment**: Render

## Local Development Setup

### Prerequisites

- Python 3.9+
- pip
- Git

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd WASHWISH
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create environment file:
```bash
cp .env.example .env
```

6. Update `.env` with your configuration:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

7. Run migrations:
```bash
python manage.py migrate
```

8. Create superuser:
```bash
python manage.py createsuperuser
```

9. Collect static files:
```bash
python manage.py collectstatic
```

10. Run development server:
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## Deployment

### Render Deployment

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Connect your forked repository
5. Configure environment variables:
   - `SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: Set to `False`
   - `PYTHON_VERSION`: `3.9.18`
6. Deploy

The application will be automatically deployed with the build script.

## Project Structure

```
WASHWISH/
├── accounts/          # User authentication app
├── services/          # Services management app
├── detergee/          # Main Django project
├── templates/         # HTML templates
├── static/           # Static files (CSS, JS, images)
├── requirements.txt  # Python dependencies
├── manage.py        # Django management script
├── render.yaml      # Render deployment config
└── build.sh         # Build script
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.