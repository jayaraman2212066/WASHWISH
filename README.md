# 🧺 WashWish - Laundry Management System

[![Django](https://img.shields.io/badge/Django-3.1.7-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

A comprehensive Django-based laundry management system that digitizes and streamlines laundry service operations. Built with modern web technologies and designed for scalability and user experience.

## 🚀 Features

### Customer Features
- 👤 **User Registration & Authentication** - Secure account creation and login
- 🛍️ **Service Booking** - Easy online laundry service booking
- 📱 **Order Tracking** - Real-time order status updates
- 💳 **Payment Processing** - Online payment and Cash on Delivery options
- 🏠 **Home Delivery** - Convenient pickup and delivery service
- 📧 **Email Notifications** - Automated order confirmations and updates
- 💬 **Feedback System** - Customer review and rating system

### Admin Features
- 📊 **Admin Dashboard** - Comprehensive business analytics
- 📈 **Reports & Analytics** - Revenue tracking and business insights
- 👥 **User Management** - Customer and staff account management
- 🔄 **Order Management** - Complete order lifecycle management
- 🎯 **Service Management** - Add/edit laundry services and pricing
- 🚚 **Delivery Management** - Track and manage home deliveries
- 💰 **Payment Tracking** - Monitor payment status and collections
- 🎁 **Discount Management** - Create and manage promotional offers

## 🛠️ Technology Stack

- **Backend**: Django 3.1.7 with Python 3.9+
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 4
- **Authentication**: Django's built-in authentication system
- **Security**: CSRF protection, XSS prevention, SQL injection protection
- **Deployment**: Render.com with Docker support
- **Static Files**: WhiteNoise for efficient static file serving
- **Email**: SMTP integration for notifications

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