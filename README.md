# 🏠 HamroKotha - Rental Property Platform

> Find your perfect rental property in Kathmandu Valley

A comprehensive rental property platform connecting landlords and tenants across Kathmandu, Bhaktapur, and Lalitpur districts in Nepal.

## 🌟 Features

### For Tenants
- 🔍 Search properties with advanced filters (district, price, type, bedrooms)
- ❤️ Save favorite properties
- 📝 Send inquiries to landlords
- 🏠 Request "Find Room" service
- 🚚 Request "Shift Home" moving service

### For Landlords
- ➕ List properties with multiple images
- 📊 Dashboard with property statistics
- 💬 Receive and respond to tenant inquiries
- ✅ Mark properties as rented

### Admin Panel
- 👥 User management (approve, ban, verify)
- 🏢 Property approval workflow
- 📈 Platform analytics and statistics
- 🚨 Report and fraud detection
- 📋 Activity logging

## 🛠️ Tech Stack

- **Backend:** Django 5.x (Python)
- **Frontend:** HTML, Tailwind CSS, JavaScript (Alpine.js)
- **Database:** PostgreSQL (SQLite for development)
- **Additional:** Django REST Framework, Crispy Forms

## 📁 Project Structure

```
rental_platform/
├── manage.py
├── config/                 # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/          # User authentication & profiles
│   ├── properties/        # Property listings
│   ├── inquiries/         # Booking inquiries & messages
│   ├── services/          # Find Room & Shift Home features
│   ├── admin_panel/       # Custom admin dashboard
│   └── core/              # Shared utilities
├── static/                # CSS, JS, images
├── media/                 # Uploaded property images
└── templates/             # HTML templates
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL (optional, SQLite works for development)
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hamrokotha-rental-web-application.git
   cd hamrokotha-rental-web-application
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the application**
   - Frontend: http://localhost:8000
   - Admin: http://localhost:8000/admin/
   - Custom Admin Panel: http://localhost:8000/admin-dashboard/

## 📌 URL Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Homepage |
| `/properties/` | Property listings |
| `/properties/search/` | Search with filters |
| `/properties/<id>/` | Property detail |
| `/register/` | User registration |
| `/login/` | User login |
| `/dashboard/` | User dashboard |
| `/services/find-room/` | Find room request |
| `/services/shift-home/` | Shift home request |
| `/admin-dashboard/` | Custom admin panel |

## 🌏 Kathmandu Valley Coverage

**Districts:**
- Kathmandu (25+ areas)
- Bhaktapur (14+ areas)
- Lalitpur (19+ areas)

**Currency:** NPR (Nepali Rupees)

## 🔒 Security Features

- CSRF Protection
- SQL Injection Prevention (Django ORM)
- XSS Protection (Template Auto-escaping)
- Role-based Access Control
- Secure Password Hashing
- Image File Validation
- Rate Limiting for Inquiries

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, contact: contact@hamrokotha.com

---

Made with ❤️ for Kathmandu Valley