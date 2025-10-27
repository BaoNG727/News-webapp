# 📰 Django News Portal

> A full-featured news portal built with Django 3.1 featuring admin panel, comments, categories, trending news, and more.

![Django](https://img.shields.io/badge/Django-3.1.14-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🌟 Features

### Frontend (Public)
- 📱 **Responsive Design** - Mobile-friendly interface
- 📰 **News Articles** - Browse and read news with images
- 🔍 **Search Functionality** - Full-text search across articles
- 🏷️ **Tags & Categories** - Organized content structure
- 💬 **Comments System** - User engagement with moderation
- 📊 **Trending News** - Popular articles section
- 🔗 **Social Sharing** - Share on Facebook, Twitter, LinkedIn, WhatsApp
- 📚 **Related Articles** - Content discovery
- 🔐 **User Registration** - Account creation and login

### Backend (Admin Panel)
- 🎛️ **Custom Admin Interface** - Enhanced Django admin
- ✍️ **Article Management** - Create, edit, delete news
- ✅ **Publish/Draft System** - Control article visibility
- 📝 **Comment Moderation** - Approve/reject comments
- 👥 **User Management** - Manage writers and permissions
- 📂 **Category Management** - Organize content
- 📧 **Newsletter System** - Collect emails and phone numbers
- 📊 **Statistics** - View counts and analytics
- 🔒 **IP Blacklist** - Security features
- 🎨 **Rich Text Editor** - CKEditor integration

### Technical Features
- 🚀 **Performance Optimized** - Database indexes, query optimization
- 🖼️ **Image Optimization** - Automatic resize and compression
- 🔐 **Security** - CSRF protection, environment variables
- 📱 **SEO Friendly** - Meta tags, slugs, clean URLs
- 🔄 **Auto-generated Slugs** - User-friendly URLs
- 🔍 **Advanced Search** - Multi-field search capability
- 📧 **Email Validation** - Proper form validation

---

## 📁 Project Structure

```
News-webapp/
│
├── 📂 main/                    # Main app (home, about, contact)
│   ├── templates/
│   │   ├── front/             # Frontend templates
│   │   │   ├── widgets/       # Reusable components
│   │   │   │   ├── related_articles.html
│   │   │   │   └── social_share.html
│   │   │   ├── master.html
│   │   │   ├── home.html
│   │   │   └── ...
│   │   └── back/              # Admin panel templates
│   │       ├── master.html
│   │       ├── home.html
│   │       └── ...
│   ├── static/                # CSS, JS, images
│   ├── views.py               # Main views
│   ├── search_views.py        # Search functionality
│   ├── models.py              # Site settings model
│   └── urls.py
│
├── 📂 news/                    # News articles app
│   ├── models.py              # News model with SEO fields
│   ├── views.py               # News CRUD operations
│   ├── admin.py               # Custom admin interface
│   ├── search.py              # Search utilities
│   ├── image_utils.py         # Image optimization
│   └── urls.py
│
├── 📂 comment/                 # Comments system
│   ├── models.py              # Comment model
│   ├── views.py               # Comment management
│   ├── admin.py               # Comment moderation
│   └── urls.py
│
├── 📂 cat/                     # Categories app
│   ├── models.py              # Category model
│   ├── views.py               # Category CRUD
│   └── urls.py
│
├── 📂 subcat/                  # Subcategories app
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 📂 trending/                # Trending news
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 📂 newsletter/              # Newsletter system
│   ├── models.py              # Email/phone collection
│   ├── views.py
│   └── urls.py
│
├── 📂 manager/                 # User management
│   ├── models.py              # Manager profiles
│   ├── views.py               # User/group/permission management
│   └── urls.py
│
├── 📂 contactform/             # Contact form
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 📂 blacklist/               # IP blacklist
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 📂 newsportal/              # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── 📂 media/                   # User uploaded files
├── 📂 static/                  # Collected static files
├── 📂 venv/                    # Virtual environment
│
├── 📄 manage.py                # Django management script
├── 📄 requirements.txt         # Python dependencies
├── 📄 db.sqlite3              # SQLite database
│
├── 📄 setup.bat               # Auto setup script
├── 📄 run.bat                 # Run development server
├── 📄 migrate.bat             # Database migrations
├── 📄 test.bat                # Run tests
├── 📄 collectstatic.bat       # Collect static files
│
├── 📄 .env.example            # Environment variables template
├── 📄 .gitignore              # Git ignore rules
├── 📄 README.md               # This file
├── 📄 IMPROVEMENTS.md         # Feature improvements
└── 📄 BACKUP_INSTRUCTIONS.md  # Backup guide
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)
- Git (optional)

### Installation

#### Method 1: Automatic Setup (Windows)

```bash
# 1. Clone or download the project
git clone https://github.com/IamOmaR22/Online-News-Portal-with-Django.git
cd News-webapp

# 2. Run setup script
setup.bat

# 3. Run development server
run.bat
```

#### Method 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env
# Edit .env with your settings

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

### Access the Application

- **Frontend**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Custom Panel**: http://127.0.0.1:8000/panel/

---

## 📝 Configuration

### Environment Variables

Edit `.env` file:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL in production)
# DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

### Settings.py Important Configurations

```python
# Security
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## 🎯 Usage Guide

### For Administrators

#### 1. Creating News Articles

1. Login to admin panel at `/panel/`
2. Navigate to "News" → "Add News"
3. Fill in:
   - Title (slug auto-generated)
   - Short description
   - Full content
   - Upload image (auto-optimized)
   - Select category
   - Add tags (comma-separated)
   - SEO fields (optional)
4. Click "Publish" or save as draft

#### 2. Managing Comments

1. Go to "Comments" → "Comments List"
2. View all comments
3. Approve/Reject with bulk actions
4. Delete spam comments

#### 3. Managing Categories

1. Navigate to "Category" → "Category List"
2. Add new categories
3. Import categories from CSV
4. Export categories to CSV

#### 4. User Management

1. Go to "Manager" → "Manager List"
2. View all registered users
3. Assign users to groups
4. Set permissions

### For Users

#### Search Articles

```
/search/?q=keyword
```

#### Browse by Tag

```
/tag/tagname/
```

#### View Article

```
/news/article-title/
```

#### Short URL (QR Code)

```
/urls/20240127001/
```

---

## 🛠️ Development

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Or use the batch script
migrate.bat
```

### Collect Static Files

```bash
python manage.py collectstatic

# Or use batch script
collectstatic.bat
```

### Run Tests

```bash
python manage.py test

# Or use batch script
test.bat
```

### Create Superuser

```bash
python manage.py createsuperuser
```

---

## 📊 Database Models

### News Model

```python
- name (title)
- slug (auto-generated URL)
- short_txt (description)
- body_txt (content)
- picname, picurl (image)
- writer (author)
- catname, catid (category)
- tag (tags)
- act (published/draft)
- show (view count)
- meta_description (SEO)
- meta_keywords (SEO)
- created_at, updated_at
```

### Comment Model

```python
- name (commenter name)
- email (commenter email)
- cm (comment text)
- news_id (related article)
- status (pending/approved)
- created_at
```

---

## 🔧 Utilities & Helpers

### Search Functionality

```python
from news.search import NewsSearch

# Full-text search
results = NewsSearch.search('keyword', published_only=True)

# Search by tag
results = NewsSearch.search_by_tag('python', published_only=True)

# Get related articles
related = NewsSearch.get_related_articles(news_obj, limit=5)
```

### Image Optimization

```python
from news.image_utils import ImageOptimizer

# Optimize image
ImageOptimizer.optimize_image(path, max_width=1200, quality=85)

# Validate upload
is_valid, error = ImageOptimizer.validate_image(file, max_size_mb=5)

# Create thumbnail
ImageOptimizer.create_thumbnail(image_path, thumb_path, size=(300, 300))
```

---

## 🎨 Frontend Templates

### Using Widgets

#### Related Articles Widget

```django
{% include 'front/widgets/related_articles.html' with related_articles=related %}
```

#### Social Sharing Widget

```django
{% include 'front/widgets/social_share.html' with article_title=news.name %}
```

### Search Form

```django
<form action="{% url 'search' %}" method="get">
    <input type="text" name="q" placeholder="Search...">
    <button type="submit">Search</button>
</form>
```

---

## 📦 Dependencies

Main packages (see `requirements.txt` for complete list):

- Django==3.1.14
- Pillow==9.0.1 (Image processing)
- django-humanize (Date formatting)
- django-crontab (Scheduled tasks)
- django-qr-code (QR code generation)
- bleach (HTML sanitization)
- selenium (Testing)
- gunicorn (Production server)
- whitenoise (Static files)

---

## 🔐 Security Features

- CSRF protection enabled
- Environment variables for secrets
- Password validation
- SQL injection protection (Django ORM)
- XSS protection (template escaping)
- IP blacklist functionality
- Comment moderation
- User permissions & groups

---

## 🚀 Deployment

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Set proper `ALLOWED_HOSTS`
3. Use strong `SECRET_KEY`
4. Use PostgreSQL instead of SQLite
5. Setup HTTPS
6. Configure static files serving
7. Setup email backend
8. Enable logging
9. Setup backups
10. Configure caching

### Example Production Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Use PostgreSQL
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📚 Additional Documentation

- [IMPROVEMENTS.md](IMPROVEMENTS.md) - New features and improvements
- [BACKUP_INSTRUCTIONS.md](BACKUP_INSTRUCTIONS.md) - Database backup guide
- [.env.example](.env.example) - Environment variables template

---

## 🐛 Troubleshooting

### Common Issues

**1. Module not found error**
```bash
pip install -r requirements.txt
```

**2. Database migrations error**
```bash
python manage.py migrate --run-syncdb
```

**3. Static files not loading**
```bash
python manage.py collectstatic --clear
```

**4. Port already in use**
```bash
python manage.py runserver 8080
```

**5. Image upload error**
```bash
pip install Pillow
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.


## 🙏 Acknowledgments

- Django Framework
- Bootstrap (Frontend)
- Font Awesome (Icons)
- CKEditor (Rich text editing)
- All contributors and users

---

## 📞 Support

For issues and questions:

1. Check the documentation files
2. Search existing GitHub issues
3. Create a new issue with detailed information

---

**Made with ❤️ using Django**
