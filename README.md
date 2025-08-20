
# Thillai Matrimony – Django 4 App

Public listing + profile view with filters (Gender, Caste, Subcaste, Age).  
Full **Django Admin** CRUD for **Gender**, **Caste**, **Subcaste**, and **Profile**.  
Public users can browse without login; admin requires login.

## Quick Start
```bash
# 1) Create virtualenv (optional)
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2) Install deps
pip install -r requirements.txt

# 3) Migrate DB
python manage.py migrate

# 4) Create superuser for Admin
python manage.py createsuperuser  # follow prompts

# (optional) Seed basic data
python manage.py loaddata profiles/fixtures/genders.json
python manage.py loaddata profiles/fixtures/castes.json
python manage.py loaddata profiles/fixtures/subcastes.json
python manage.py loaddata profiles/fixtures/profiles.json

# 5) Run
python manage.py runserver
```

## URLs
- Public listing: `http://127.0.0.1:8000/` or `/profiles/`
- Profile detail: `/profiles/<id>/<slug>/`
- Admin: `/admin/`

## Hosting
- Configure `DEBUG = False`, set `ALLOWED_HOSTS`, and use a real DB (MySQL/PostgreSQL).  
- Serve static files via WhiteNoise or your web server; media files under `/media/`.
