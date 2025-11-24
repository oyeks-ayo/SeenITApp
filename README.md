# SeenIT App — Complete Documentation

A professional portfolio and project showcase platform built with Flask and PostgreSQL. SeenIT enables creatives, artisans, and service professionals to display their work, build profiles, and connect with potential clients.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Database Configuration](#database-configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Overview

**SeenIT** is a full-stack web application that serves as a portfolio showcase platform. Users can:
- Create detailed professional profiles with skills, services, and work categories
- Upload and share project portfolios (images and videos)
- Browse and filter projects by category, skills, location, and services
- Connect with other professionals and showcase their expertise

The application is built using Flask with a PostgreSQL database backend and follows modern web development practices.

---

## Features

### User Management
- User registration with email, phone, and username validation
- Secure authentication (password hashing with werkzeug)
- Session-based login system
- Password reset functionality

### Professional Profiles
- Comprehensive profile creation with:
  - Personal information (DOB, gender, location)
  - Profile and cover photos
  - Bio and slogan
  - Skills selection (50+ predefined skills)
  - Services offered (10+ service types)
  - Work categories (12 categories: fashion, beauty, graphics, photography, etc.)
  - Social media and blog links

### Project Showcase
- Upload projects with title and description
- Multi-file support (images and videos)
- Project filtering by category, skills, services, and location
- Browse all projects or filter by specific user
- Project detail pages with owner information

### Admin Dashboard
- Admin authentication
- User management (view/delete users)
- Project management (view/delete projects)
- Contact message viewing

### Security
- CSRF protection on all forms
- Password hashing
- Session management with login decorators
- Secure file upload validation

---

## Tech Stack

### Backend
- **Framework:** Flask 3.1.1
- **Database:** PostgreSQL (via psycopg2-binary)
- **ORM:** SQLAlchemy 2.0.41 / Flask-SQLAlchemy 3.1.1
- **Migrations:** Alembic 1.16.4 / Flask-Migrate 4.1.0
- **Authentication:** Flask-HTTPAuth 4.8.0
- **Forms:** Flask-WTF 1.2.2, WTForms 3.2.1
- **Email:** Flask-Mail 0.10.0
- **Environment:** python-dotenv 1.1.1

### Frontend
- **Template Engine:** Jinja2 3.1.6
- **CSS Framework:** Bootstrap (minified)
- **JavaScript:** jQuery 3.7.1
- **Icons:** FontAwesome

### Server
- **Development:** Werkzeug 3.1.3
- **Production:** Gunicorn (recommended)

---

## Requirements

- **Python:** 3.11+ (tested on Python 3.13)
- **Database:** PostgreSQL 12+ (running on localhost:5432)
- **OS:** Windows, macOS, or Linux
- **Virtual Environment:** Recommended (vseenit/ included)

---

## Installation & Setup

### 1. Clone the Repository

```bash
cd /path/to/your/projects
# If you're setting up from the backup, you're already here
```

### 2. Set Up Virtual Environment

#### Windows PowerShell
```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Activate virtual environment
& .\vseenit\Scripts\Activate.ps1
```

#### Command Prompt
```cmd
vseenit\Scripts\activate.bat
```

#### Git Bash / macOS / Linux
```bash
source vseenit/bin/activate
```

### 3. Install Dependencies

```bash
# Verify you're in the virtual environment
python --version
which python  # or 'where python' on Windows

# Install all required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The `.env` file in the root directory contains sensitive configuration:

```bash
# .env file (already configured)
SECRET_KEY='your-secret-key-here'
SQLALCHEMY_DATABASE_URI='postgresql://postgres:0000@localhost:5432/seenITApp'
```

**Security Note:** Never commit the `.env` file to version control. It's already in `.gitignore`.

---

## Database Configuration

### PostgreSQL Setup

1. **Install PostgreSQL** (if not already installed)
   - Download from: https://www.postgresql.org/download/

2. **Start PostgreSQL Service**

   **Windows:**
   ```cmd
   net start postgresql-x64-14
   # or
   pg_ctl start -D "C:\Program Files\PostgreSQL\14\data"
   ```

   **macOS:**
   ```bash
   brew services start postgresql@14
   ```

   **Linux:**
   ```bash
   sudo systemctl start postgresql
   ```

3. **Create Database**

   ```bash
   # Connect to PostgreSQL
   psql -U postgres

   # Create database
   CREATE DATABASE "seenITApp";

   # Exit
   \q
   ```

### Run Database Migrations

```bash
# Activate virtual environment first
source vseenit/bin/activate  # or appropriate activation for your OS

# Apply all migrations
flask --app starter.py db upgrade

# Or using alembic directly
alembic -c migrations/alembic.ini upgrade head
```

### Migration Commands Reference

```bash
# Check current migration version
flask --app starter.py db current

# View migration history
flask --app starter.py db history

# Create a new migration (after model changes)
flask --app starter.py db migrate -m "Description of changes"

# Apply migrations
flask --app starter.py db upgrade

# Rollback last migration
flask --app starter.py db downgrade
```

---

## Running the Application

### Development Server

```bash
# Ensure virtual environment is active
python starter.py
```

The application will start on: **http://127.0.0.1:5030**

### Key URLs

- **Homepage:** http://127.0.0.1:5030
- **User Registration:** http://127.0.0.1:5030/signup
- **User Login:** http://127.0.0.1:5030/userlogin
- **Admin Login:** http://127.0.0.1:5030/admin/login
- **About Us:** http://127.0.0.1:5030/about
- **Contact Us:** http://127.0.0.1:5030/contact

### Debug Mode

Debug mode is **enabled** by default in `starter.py`. This provides:
- Auto-reload on code changes
- Detailed error pages
- Debugger PIN for interactive debugging

**Production Note:** Disable debug mode in production by setting `debug=False` in `starter.py`.

---

## Project Structure

```
SEENITAPP/
├── .env                          # Environment variables (SECRET_KEY, DATABASE_URI)
├── .gitignore                    # Git ignore rules
├── starter.py                    # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # Quick start guide
│
├── pkg/                          # Main application package
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration class
│   ├── models.py                # SQLAlchemy database models
│   ├── forms.py                 # WTForms form definitions
│   ├── user_routes.py           # User-facing routes (35+ endpoints)
│   ├── admin_routes.py          # Admin dashboard routes
│   ├── dbroutes.py              # Database operations/API routes
│   │
│   ├── static/                  # Static assets
│   │   ├── bootstrap.min.css
│   │   ├── jquery-3.7.1.min.js
│   │   ├── fontawesome/         # Icon fonts
│   │   ├── uploads/             # User-uploaded files
│   │   ├── profile_page/        # Profile assets
│   │   ├── homepage-pix/        # Homepage images
│   │   └── ...
│   │
│   └── templates/               # Jinja2 HTML templates
│       ├── format.html          # Base template
│       ├── navbar.html          # Navigation component
│       ├── footer.html          # Footer component
│       ├── admin/               # Admin templates
│       │   ├── admin_login.html
│       │   └── admin.html
│       └── users/               # User templates
│           ├── homepage.html
│           ├── sign_up.html
│           ├── user_login.html
│           ├── profile_form.html
│           ├── profile_page.html
│           ├── seenITHub.html
│           ├── all_projects.html
│           └── ...
│
├── instance/                     # Instance-specific config
│   └── config.py                # Overrides for pkg/config.py
│
├── migrations/                   # Alembic migration scripts
│   ├── alembic.ini
│   ├── env.py
│   └── versions/                # Migration version files
│       ├── 92368f14e902_.py
│       ├── a9ce37dc777f_.py
│       └── ...
│
├── vseenit/                      # Virtual environment (do not commit)
│
└── DOCS/                         # Documentation
    └── README.md                # This file
```

---

## Database Schema

### Core Tables

#### Users
- User accounts with authentication
- Fields: id, fname, lname, mname, username, email, phone, user_pwd, terms, datereg_signup

#### Profile
- Extended user profiles with portfolio information
- Fields: id, dob, gender, address, profile_pix, cover_pix, slogan, bio, social_media, blog, user_id (FK), state_id (FK), category_id (FK)

#### Admin
- Admin accounts for dashboard access
- Fields: id, fname, lname, username, email, phone, admin_pwd, datereg_signup

#### Project
- User projects and portfolio items
- Fields: project_id, title, description, datereg_project, user_id (FK), profile_id (FK)

#### ProjectMedia
- Images and videos for projects
- Fields: id, project_id (FK), file_type ('image'/'video'), filename

### Reference Tables

- **Skill:** Available skills (50+ entries)
- **Service:** Service types (10+ entries)
- **Category:** Work categories (12 entries)
- **State:** Geographic states

### Junction Tables

- **ProfileSkill:** Many-to-many relationship between Profile and Skill
- **ProfileService:** Many-to-many relationship between Profile and Service

### Other Tables

- **ContactSeenIT:** Contact form submissions
- **State:** Location data

---

## API Endpoints

### User Routes (`user_routes.py`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage |
| `/signup` | GET | User registration page |
| `/signup/submit/` | POST | Process registration |
| `/userlogin` | GET | User login page |
| `/userlogin/submit/` | POST | Process login |
| `/logout` | GET | User logout |
| `/profile` | GET, POST | Profile creation/edit |
| `/profile/<username>` | GET | View user profile |
| `/seenithub` | GET, POST | Project upload page |
| `/all_projects` | GET | Browse all projects |
| `/project/<project_id>` | GET | View project details |
| `/projectfilter` | GET | Filter projects |
| `/search` | GET | Search profiles |
| `/about` | GET | About page |
| `/contact` | GET, POST | Contact form |

### Admin Routes (`admin_routes.py`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin/login` | GET, POST | Admin login |
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/users` | GET | View all users |
| `/admin/projects` | GET | View all projects |
| `/admin/delete_user/<id>` | POST | Delete user |
| `/admin/delete_project/<id>` | POST | Delete project |

### Database Routes (`dbroutes.py`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/skills` | GET | Get all skills |
| `/api/services` | GET | Get all services |
| `/api/categories` | GET | Get all categories |
| `/api/states` | GET | Get all states |

---

## Configuration

### Configuration Files

1. **`.env`** (root) - Main environment variables
   ```
   SECRET_KEY='your-secret-key'
   SQLALCHEMY_DATABASE_URI='postgresql://user:password@localhost:5432/dbname'
   ```

2. **`pkg/config.py`** - Configuration class
   - Reads from environment variables
   - Provides fallback defaults

3. **`instance/config.py`** - Instance-specific overrides
   - Optional
   - Overrides settings from `pkg/config.py`
   - Not committed to version control

### Key Configuration Options

```python
# pkg/config.py
class Appconfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", 'fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                       'postgresql://postgres:password@localhost:5432/seenITApp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Changing Configuration

To change database credentials or other settings:

1. Edit `.env` file in the root directory
2. Restart the application for changes to take effect

```bash
# Example .env changes
SECRET_KEY='new-secret-key-here'
SQLALCHEMY_DATABASE_URI='postgresql://newuser:newpass@localhost:5432/newdb'
```

---

## Development Workflow

### 1. Making Code Changes

```bash
# Activate virtual environment
source vseenit/bin/activate

# Make your changes to .py files
# Flask auto-reloads in debug mode, so changes take effect immediately
```

### 2. Adding New Dependencies

```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### 3. Database Model Changes

```bash
# After editing models.py, create a migration
flask --app starter.py db migrate -m "Description of changes"

# Review the generated migration in migrations/versions/

# Apply the migration
flask --app starter.py db upgrade
```

### 4. Testing Changes

```bash
# Run the application
python starter.py

# Test in browser at http://127.0.0.1:5030
```

### 5. Version Control

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature description"

# Push to remote
git push origin your-branch-name
```

---

## Troubleshooting

### Common Issues

#### 1. **Port Already in Use**
```
Error: Address already in use
```

**Solution:**
```bash
# Find process using port 5030
# Windows:
netstat -ano | findstr :5030
taskkill /PID <process_id> /F

# macOS/Linux:
lsof -ti:5030 | xargs kill -9
```

#### 2. **Database Connection Failed**
```
sqlalchemy.exc.OperationalError: connection to server failed
```

**Solution:**
- Verify PostgreSQL is running: `pg_isready`
- Check database credentials in `.env`
- Ensure database exists: `psql -U postgres -l`

#### 3. **Module Not Found Error**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source vseenit/bin/activate  # or Windows equivalent

# Reinstall dependencies
pip install -r requirements.txt
```

#### 4. **Migration Conflicts**
```
alembic.util.exc.CommandError: Target database is not up to date
```

**Solution:**
```bash
# Check current version
flask --app starter.py db current

# View history
flask --app starter.py db history

# Upgrade to latest
flask --app starter.py db upgrade head
```

#### 5. **CSRF Token Missing**
```
400 Bad Request: The CSRF token is missing
```

**Solution:**
- Ensure forms include `{{ form.csrf_token }}`
- Check `SECRET_KEY` is set in `.env`
- Clear browser cookies and try again

#### 6. **File Upload Errors**
```
Error: File type not allowed
```

**Solution:**
- Supported image formats: jpg, jpeg, png, webp, gif
- Supported video formats: mp4, mov, webm
- Check file size limits in code

---

## Deployment

### Production Checklist

- [ ] Set `debug=False` in `starter.py`
- [ ] Use strong `SECRET_KEY` (generate with `secrets.token_hex(32)`)
- [ ] Use production database (not localhost)
- [ ] Set up Gunicorn or uWSGI
- [ ] Configure Nginx as reverse proxy
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure environment variables on server
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring (e.g., Sentry)

### Deployment with Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5030 "pkg:app"
```

### Environment Variables for Production

```bash
# Set on production server
export SECRET_KEY='production-secret-key'
export SQLALCHEMY_DATABASE_URI='postgresql://user:pass@prod-host:5432/dbname'
export FLASK_ENV='production'
```

---

## Contributing

### Contribution Guidelines

1. **Fork the repository** and create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style
   - Use descriptive variable names
   - Add comments for complex logic
   - Follow PEP 8 style guide

3. **Test your changes** thoroughly
   - Test all affected endpoints
   - Check database operations
   - Verify form validation

4. **Commit your changes** with clear messages
   ```bash
   git commit -m "feat: Add user profile search functionality"
   ```

5. **Update documentation** if needed
   - Update README if adding features
   - Add docstrings to new functions
   - Update API endpoint documentation

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Commit Message Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## License

[Add your license information here]

---

## Contact & Support

For questions, issues, or contributions, please contact:
- **Project Repository:** [Add repository URL]
- **Issues:** [Add issues page URL]
- **Email:** [Add contact email]

---

## Acknowledgments

Built with:
- Flask - The Python micro web framework
- PostgreSQL - The world's most advanced open source database
- Bootstrap - The most popular HTML, CSS, and JS library
- SQLAlchemy - The Python SQL toolkit

---

**Last Updated:** November 2025
