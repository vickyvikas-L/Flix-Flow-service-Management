# FlixFlow - Smart Service Management & Customer Support Platform   

FlixFlow is a full-stack, multi-tenant enterprise Service Request and Customer Support platform designed for appliance and electronics repair companies. It bridges **Customers**, **Technicians**, and **Administrators** into a unified, real-time workflow ecosystem.  

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin)](https://www.linkedin.com/in/vickyvikasl/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/vickyvikas-L/Flix-Flow-service-Management)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Django%20%7C%20DRF%20%7C%20JavaScript-6366f1)
![License](https://img.shields.io/badge/License-MIT-green)   

---

## 🌟 Key Features

### 👤 1. Role-Based Authentication & Permissions 
- **Customer**: Create service requests, attach issue notes, track status pipelines, view assigned technicians, download invoices, and rate completed repairs.
- **Technician**: View assigned jobs, update work stage (`Pending` → `Assigned` → `In Progress` → `Completed`), log work notes (*"Charging IC replaced..."*), and add spare part charges.
- **Administrator**: High-level KPI control metrics, customer & technician directory management, job dispatching/assignment, service category configuration, and revenue analytics.

### ⚡ 2. Ticket Tracking Pipeline 
- Real-time visual progress pipeline tracking each request from receipt to resolution.
- Multi-criteria filtering by **Status** (`Pending`, `Assigned`, `In Progress`, `Completed`) and **Priority** (`High`, `Medium`, `Low`).
- Instant live search across Ticket ID, Customer Name, Category, and Problem Description.

### 🧾 3. Automated Invoicing System
- Auto-generates itemized invoices upon repair completion.
- Calculates base service fees, spare parts/labor charges, taxes, and total payable amount.
- Printable & downloadable clean PDF/invoice layout.

### 🔔 4. Notifications & In-App Alerts
- Real-time notifications dispatched upon technician assignment, status updates, and invoice generation. 

---

## 💻 Tech Stack

- **Backend**: Python 3.13, Django 6.x, Django REST Framework (DRF), JWT Authentication (`djangorestframework-simplejwt`), CORS Headers, Pillow.
- **Frontend**: Vanilla JavaScript (ES6+ SPA architecture), Modern CSS3 (Glassmorphism design system, Outfit & Inter typography, responsive CSS Grid), FontAwesome 6 icons.
- **Database**: SQLite (Out-of-the-box local zero setup) / MySQL compatible.

---

## 📂 Project Structure

```
FixFlow/
│
├── backend/
│   ├── manage.py
│   ├── fixflow/            # Core settings, URL routing, WSGI/ASGI
│   ├── users/              # Custom User model (Customer, Technician, Admin)
│   ├── services/           # Service Categories & Pricing
│   ├── tickets/            # Service Requests, Status Pipeline & Ratings
│   ├── payments/           # Invoices & Admin KPI Analytics
│   └── notifications/      # In-App Notification System
│
├── frontend/
│   ├── index.html          # Main Unified Portal HTML
│   ├── css/
│   │   └── style.css       # Design Tokens, Glassmorphism, Print Layout
│   └── js/
│       └── app.js          # REST Client, State Manager, Dynamic Renderers
│
├── requirements.txt        # Dependencies
├── .env.example            # Environment configurations
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start & Installation

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/your-username/FixFlow.git
cd FixFlow

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Apply Migrations & Seed Initial Data
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

### 3. Run Development Server
```bash
python manage.py runserver
```
Visit **`http://127.0.0.1:8000/`** in your browser.

---

## 🔑 Demo Login Credentials

The app includes a 1-click **Quick Demo Switcher** bar at the top of the screen:

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Customer** | `vikas` | `vikas123` | Pre-loaded with Laptop, AC, and Printer repair tickets |
| **Technician** | `tech` | `tech123` | Assigned to Ticket #1024 (Ramesh Kumar) |
| **Admin** | `admin` | `admin123` | Full system metrics, revenue & dispatch control |

---

## 🌐 REST API Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register new customer account |
| `POST` | `/api/auth/login/` | Obtain JWT Auth Access & Refresh Tokens |
| `GET` | `/api/auth/me/` | Current user profile details |
| `GET` | `/api/auth/technicians/` | List all registered technicians |
| `GET` | `/api/services/` | Fetch service categories & base prices |
| `GET` | `/api/tickets/` | List tickets (with `search`, `status`, `priority` filters) |
| `POST` | `/api/tickets/` | Create a new service ticket |
| `POST` | `/api/tickets/<id>/assign/` | Admin assigns technician to ticket |
| `POST` | `/api/tickets/<id>/status/` | Technician updates status & adds work notes |
| `POST` | `/api/tickets/<id>/rate/` | Customer submits star rating & review |
| `GET` | `/api/payments/` | View itemized invoices |
| `GET` | `/api/payments/reports/stats/` | Admin KPI stats (Revenue, Ticket breakdown) |
| `GET` | `/api/notifications/` | Fetch unread & read user notifications |

---

## 💼 Interview Talking Points

> *"I developed **FixFlow**, a full-stack Service Management & Customer Support application using Python, Django, Django REST Framework, JavaScript, and MySQL/SQLite. I implemented role-based authentication with custom permissions for Customers, Technicians, and Admins, an automated ticket assignment and lifecycle tracking pipeline, real-time in-app notifications, and itemized invoice generation."*

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
