# SubGuard API

A subscription tracking and financial monitoring backend built with Django REST Framework and JWT authentication.

---

## 🚀 Features

- JWT Authentication (SimpleJWT)
- Subscription management system
- Charge tracking system
- Risk analysis engine (low / medium / high)
- Automated alert generation
- Financial analytics dashboard
- Swagger / Redoc API documentation
- User-based data isolation

---

## 🧠 Tech Stack

- Django 6
- Django REST Framework
- SimpleJWT
- SQLite (development)
- drf-yasg (Swagger)

---

## 🔐 Authentication

All endpoints (except token endpoints) require JWT authentication.

### Step 1: Get Token

POST `/api/token/`

Request body:
{
  "username": "admin",
  "password": "your_password"
}

Response:
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}

---

### Step 2: Use Token

Add this header to all protected requests:

Authorization: Bearer <access_token>

---

## 📊 API ENDPOINTS

### Dashboard
GET /api/v1/dashboard/

Returns:
- total subscriptions
- total spend
- risk distribution
- subscription breakdown

---

### Subscriptions

GET /api/v1/subscriptions/
POST /api/v1/subscriptions/
GET /api/v1/subscriptions/{id}/
PATCH /api/v1/subscriptions/{id}/
DELETE /api/v1/subscriptions/{id}/

---

### Charges

GET /api/v1/charges/
POST /api/v1/charges/

---

### Alerts

GET /api/v1/alerts/

---

## 📈 DASHBOARD RESPONSE FORMAT

{
  "status": "success",
  "data": {
    "summary": {
      "total_subscriptions": 3,
      "total_spend": "12000.00",
      "active_subscriptions": 2
    },
    "insights": {
      "risk_distribution": {
        "low": 2,
        "medium": 1,
        "high": 0
      },
      "avg_spend_per_subscription": "4000.00"
    },
    "subscriptions": [
      {
        "subscription": {
          "id": 1,
          "name": "Netflix",
          "amount": "4000.00",
          "currency": "NGN",
          "billing_cycle": "monthly",
          "next_billing_date": "2026-05-06",
          "is_active": true
        },
        "latest_charge": {
          "amount": "4000.00",
          "date": "2026-05-01"
        },
        "risk": {
          "level": "LOW",
          "reason": "Normal usage pattern"
        },
        "alerts_count": 2
      }
    ]
  }
}

---

## 📚 API DOCUMENTATION

Swagger UI:
http://127.0.0.1:8000/swagger/

Redoc:
http://127.0.0.1:8000/redoc/

---

## ⚙️ LOCAL SETUP

1. Clone repository
2. Create virtual environment
3. Activate virtual environment
4. Install dependencies:
   pip install -r requirements.txt
5. Run migrations:
   python manage.py migrate
6. Create superuser:
   python manage.py createsuperuser
7. Run server:
   python manage.py runserver

---

## 🧠 PROJECT PURPOSE

This project demonstrates:

- REST API architecture
- JWT authentication
- Financial tracking system
- Risk analysis logic
- SaaS-style backend design
- Clean Django REST structure

---

## 📌 STATUS

- Backend complete
- Authentication working
- Dashboard analytics implemented
- Swagger documentation active
- Production-ready structure achieved

---

## 🚀 FUTURE IMPROVEMENTS

- Email alert system
- Celery scheduled billing simulation
- PostgreSQL migration
- Docker deployment
- Rate limiting and caching