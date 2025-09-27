# Deployment Guide

## GitHub Setup

1. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name your repository (e.g., "washwish-laundry")
   - Make it public or private as needed
   - Don't initialize with README (we already have one)

2. **Push your code to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

## Render Deployment

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account

### Step 2: Create PostgreSQL Database
1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Configure:
   - Name: `washwish-db`
   - Database Name: `washwish`
   - User: `washwish`
   - Region: Choose closest to your users
   - Plan: Free tier is fine for testing
4. Click "Create Database"
5. **Save the connection details** (you'll need the DATABASE_URL)

### Step 3: Create Web Service
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `washwish`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn detergee.wsgi:application`
   - **Plan**: Free tier for testing

### Step 4: Environment Variables
Add these environment variables in Render:

```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
PYTHON_VERSION=3.9.18
DATABASE_URL=postgresql://user:password@host:port/database
```

**To generate a SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your application

### Step 6: Custom Domain (Optional)
1. In your web service settings
2. Go to "Custom Domains"
3. Add your domain
4. Configure DNS records as instructed

## Auto-Deployment

The project is configured for automatic deployment:
- Every push to `main` branch triggers a new deployment
- GitHub Actions runs tests before deployment
- Render automatically deploys if tests pass

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `django-insecure-xyz...` |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@host:5432/db` |
| `PYTHON_VERSION` | Python version | `3.9.18` |

## Troubleshooting

### Common Issues:

1. **Build fails**: Check build logs in Render dashboard
2. **Database connection error**: Verify DATABASE_URL is correct
3. **Static files not loading**: Ensure `python manage.py collectstatic` runs in build
4. **500 errors**: Check application logs in Render dashboard

### Useful Commands:

```bash
# Local testing
python manage.py runserver

# Check for issues
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Create superuser (run in Render shell)
python manage.py createsuperuser
```

## Monitoring

- **Logs**: Available in Render dashboard
- **Metrics**: CPU, memory usage in Render dashboard
- **Health checks**: Render automatically monitors your app

## Scaling

- **Horizontal**: Upgrade to paid plan for multiple instances
- **Database**: Upgrade PostgreSQL plan for more connections/storage
- **CDN**: Consider adding CloudFlare for static files