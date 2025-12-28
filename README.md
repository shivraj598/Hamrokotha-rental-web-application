# 🏠 HamroKotha - Rental Property Platform

> Find your perfect rental property in Kathmandu Valley

A comprehensive rental property platform connecting landlords and tenants across Kathmandu, Bhaktapur, and Lalitpur districts in Nepal.

## 🌟 Features

### For Tenants
- 🔍 **Advanced Search** - Filter properties by district, price, type with case-insensitive matching
- ❤️ **Save Favorites** - Bookmark properties for later reference
- 📝 **Send Inquiries** - Direct messaging to landlords
- 🏠 **Find Room Service** - Request assistance finding rental properties
- 🚚 **Shift Home Service** - Moving and relocation services
- 📊 **Property Details** - View full property information with multiple images

### For Landlords
- ➕ **Create Properties** - List properties with multiple images (up to 10)
- 📊 **Dashboard** - View all your properties and statistics
- 💬 **Manage Inquiries** - Receive and respond to tenant inquiries
- ✏️ **Edit Properties** - Update property details anytime
- 🗑️ **Delete Properties** - Remove listings from three convenient locations
- ✅ **Status Tracking** - Track properties from pending approval to rented

### Admin Panel
- 👥 **User Management** - Verify, approve, and manage users
- 🏢 **Property Approval** - Review and approve/reject property listings
- 💬 **Inquiry Management** - Monitor all inquiries and communications
- 📈 **Analytics** - View platform statistics and activity
- 🔍 **Case-Insensitive Filters** - Search across all management views
- 📋 **Activity Logging** - Track all platform activities

## 🛠️ Tech Stack

- **Backend:** Django 5.2.9 (Python 3.14.1)
- **Frontend:** HTML5, Tailwind CSS 3, Alpine.js 3
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Additional Libraries:**
  - Django Crispy Forms
  - Pillow (Image processing)
  - Python-dotenv

## 📁 Project Structure

```
hamrokotha-rental-web-application/
├── manage.py
├── requirements.txt
├── .env.example
├── config/                          # Django settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── accounts/                   # User authentication & profiles
│   │   ├── models.py              # Custom User model with roles
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── urls.py
│   ├── properties/                 # Property listings management
│   │   ├── models.py              # Property, PropertyImage models
│   │   ├── views.py               # CRUD operations
│   │   ├── forms.py               # PropertyForm, PropertyImageForm
│   │   └── urls.py
│   ├── inquiries/                  # Booking inquiries & messages
│   │   ├── models.py              # Inquiry model
│   │   ├── views.py
│   │   └── urls.py
│   ├── services/                   # Find Room & Shift Home
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── admin_panel/                # Custom admin dashboard
│   │   ├── views.py               # Admin-only views
│   │   └── urls.py
│   └── core/                       # Shared utilities
├── static/                          # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── images/
├── media/                           # Uploaded property images
├── templates/                       # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── properties/
│   ├── accounts/
│   ├── includes/
│   └── admin_panel/
└── venv/                            # Virtual environment
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git
- (Optional) PostgreSQL for production

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/hamrokotha-rental-web-application.git
   cd hamrokotha-rental-web-application
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser account**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files (production only)**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Django Admin: http://127.0.0.1:8000/admin/
   - Custom Admin Panel: http://127.0.0.1:8000/admin-dashboard/

## 👤 Test Credentials (Development)

Default admin account:
- **Username:** admin
- **Password:** admin123

Test user accounts:
- **Landlord:** shivraj (password: landlord123)
- **Tenant:** sagar (password: tenant123)

> ⚠️ **IMPORTANT:** Change all default credentials immediately in production!

## 📌 API & URL Endpoints

### Public Routes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Homepage with hero section |
| `/properties/` | GET | Property listings with search |
| `/properties/<id>/` | GET | Property detail view |
| `/register/` | GET, POST | User registration |
| `/login/` | GET, POST | User login |
| `/logout/` | POST | User logout |

### Authenticated User Routes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dashboard/` | GET | User dashboard |
| `/profile/` | GET, POST | User profile management |
| `/favorites/` | GET | Saved favorite properties |
| `/inquiries/` | GET | User inquiries |

### Landlord Routes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/properties/create/` | GET, POST | Create new property |
| `/properties/<id>/edit/` | GET, POST | Edit property |
| `/properties/<id>/delete/` | POST | Delete property |
| `/properties/my-properties/` | GET | Landlord's properties |

### Admin Routes
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/admin-dashboard/` | GET | Admin dashboard |
| `/admin-dashboard/users/` | GET | User management |
| `/admin-dashboard/properties/` | GET | Property approvals |
| `/admin-dashboard/inquiries/` | GET | Inquiry management |

## � Supported Districts

### Kathmandu
- Central areas: Thamel, Basantapur, Durbar Square
- Eastern: Bhotebahal, Chabahil, Kamal Pokhari
- Western: Naxal, Lazimpat, Dilli Bazaar
- And 15+ more areas

### Bhaktapur
- Durbar Square, Taumadhi, Tachapal
- Suryabinayak, Banepa, Madhyapur
- And 9+ more areas

### Lalitpur
- Patan, Imadol, Lubhu
- Godavari, Harisiddhi, Sunakothi
- And 15+ more areas

## 💰 Currency

All prices are in **NPR (Nepali Rupees)**

## � Security Features

- ✅ CSRF Protection (Django built-in)
- ✅ SQL Injection Prevention (Django ORM)
- ✅ XSS Protection (Template auto-escaping)
- ✅ Role-Based Access Control (RBAC)
  - TENANT: Browse and inquire
  - LANDLORD: Create, edit, delete properties
  - ADMIN: Approve/reject, manage users
- ✅ Secure Password Hashing (PBKDF2)
- ✅ Image File Validation (Size & format checks)
- ✅ User Email Verification (optional)
- ✅ Session Management

## 📦 Dependencies

Key packages included in `requirements.txt`:
- Django==5.2.9
- Pillow (Image handling)
- python-dotenv (Environment configuration)
- django-crispy-forms (Form styling)
- crispy-tailwind (Tailwind form templates)

See `requirements.txt` for complete list.

## 🎨 UI/UX Features

- **Responsive Design** - Works on mobile, tablet, and desktop
- **Dark Navigation** - Modern dark navbar matching footer
- **Transparent Search Box** - Hero section with transparency effects
- **Nepal Mountain Background** - Beautiful Kathmandu Valley imagery
- **Case-Insensitive Filters** - User-friendly search across all views
- **Alpine.js Interactions** - Smooth dropdown menus and interactions
- **Tailwind CSS** - Modern, accessible styling

## 🔄 Property Lifecycle

```
User Creates Property
        ↓
    [PENDING] (Awaiting Admin Review)
        ↓
    ├─→ [APPROVED] → Visible to Tenants
    │       ↓
    │   [RENTED] (Property Rented Out)
    │
    └─→ [REJECTED] (Admin Rejected)
```

## 📝 Database Models

### User Model
- Custom user model with roles: LANDLORD, TENANT, ADMIN
- Profile picture, email verification, phone number

### Property Model
- Title, description, address, district
- Price, property type, bedrooms, bathrooms
- Status (PENDING, APPROVED, REJECTED, RENTED)
- Multiple images (PropertyImage model)
- Timestamps (created_at, updated_at)

### Inquiry Model
- Sender (Tenant) → Recipient (Landlord)
- Property reference
- Message content
- Status tracking

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📚 Documentation

- API endpoints documented in code comments
- Model relationships clearly defined
- Form validation rules specified
- View permission mixins for access control

## 🐛 Known Issues

- None currently reported

## 🚀 Future Enhancements

- [ ] Email notifications for inquiries
- [ ] Property reviews and ratings
- [ ] Advanced reporting features
- [ ] Google Maps integration
- [ ] Multiple language support (Nepali/English)
- [ ] Mobile app (React Native)
- [ ] Payment integration
- [ ] Property scheduling/viewing

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**Shivraj Timilsena**
- GitHub: [@shivrajtimilsena](https://github.com/shivrajtimilsena)
- Email: shivraj@example.com

## 📧 Support & Contact

For questions, issues, or suggestions:
- Open an issue on GitHub
- Email: support@hamrokotha.com
- Visit: www.hamrokotha.com

## 🙏 Acknowledgments

- Django community for the amazing framework
- Tailwind CSS for utility-first styling
- Unsplash for beautiful imagery
- All contributors and testers

---

<div align="center">

Made with ❤️ for Kathmandu Valley | Find Your Perfect Home Today! 🏡

⭐ If you like this project, please consider giving it a star!

</div>