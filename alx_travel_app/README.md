# Travel App 🧳

A Django project for managing travel-related listings.  
This repo currently includes one Django app called **`listing`** with models, serializers, and database seeding functionality.

---

## 🚀 Project Setup

### 1. Create Django Project
```bash
django-admin startproject travel_app
cd travel_app
```

### 2. Create Django App
```bash
python manage.py startapp listing
```
The new app `listing` was added and registered in `INSTALLED_APPS` inside **`settings.py`**.

---

## 📦 Models

The `listing` app contains models to represent travel-related data.  
Example (simplified):
```python
from django.db import models

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Run migrations after defining models:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🎯 Serializers

The app includes **serializers** for converting model instances to JSON (for APIs).

Example:
```python
from rest_framework import serializers
from .models import Listing

class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
```

---

## 🌱 Database Seeding

Custom seeding script was added for populating the database with initial data.

Example approach:
```python
from django.core.management.base import BaseCommand
from listing.models import Listing

class Command(BaseCommand):
    help = 'Seed database with sample listings'

    def handle(self, *args, **kwargs):
        listings = [
            {"title": "Paris Getaway", "description": "3 nights in Paris", "price": 500},
            {"title": "Beach Resort", "description": "Luxury resort by the sea", "price": 750},
        ]
        for data in listings:
            Listing.objects.create(**data)
        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
```

Run seeder:
```bash
python manage.py seed
```

---

## ✅ Completed Steps
- [x] Created Django project `travel_app`
- [x] Created Django app `listing`
- [x] Added models
- [x] Added serializers
- [x] Added seeding script
- [x] Applied migrations

---

## 📌 Next Steps (Future Work)
- Add API endpoints using Django REST Framework views/viewsets  
- Implement authentication (JWT or session-based)  
- Add tests for models, serializers, and APIs  
- Deploy project (Heroku, Railway, or Docker)  

---

## 📝 Requirements

Install dependencies:
```bash
pip install django djangorestframework
```

---

## ⚡ Quick Start

```bash
git clone <your-repo-url>
cd travel_app
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then visit [http://127.0.0.1:8000](http://127.0.0.1:8000).

---
