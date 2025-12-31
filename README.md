# Hamrokotha — Rental Web Application 🏡

**Hamrokotha** is a Django-based rental web application that helps landlords list properties and tenants find and inquire about rentals. It includes account management (tenant, landlord, admin), property listings, inquiries, chat, admin panel, and service listings.

---

## Project Details — What this project is about

Hamrokotha is a web application that connects landlords, tenants, and service providers in the Kathmandu Valley. Its mission is to simplify property listings, tenant-landlord communication, and moving services while remaining lightweight and easy to deploy.

Primary goals:
- Enable landlords to list properties quickly (with images and detailed metadata).
- Allow tenants to search, filter, favorite, and send inquiries for properties.
- Provide an admin dashboard for approvals, analytics, and user management.
- Offer service listings (e.g., find-room, moving/shift-home services) and basic messaging between users.

Target users:
- Tenants searching for rental properties
- Landlords managing multiple properties
- Site administrators and operators

---

## Technology Stack (expanded)

- Backend: Django (5.x), Python (3.10+ recommended)
- Frontend: HTML5 templates, Tailwind CSS, Alpine.js for lightweight interactivity
- Database: SQLite for development; PostgreSQL recommended for production
- Images & File Uploads: Pillow (local storage in development; S3 or other object store recommended for production)
- Forms & UI Helpers: django-crispy-forms (+ Tailwind integration)
- Optional extras: Redis + Django Channels for realtime chat, Celery for background tasks
- Static asset management: Django staticfiles, collectstatic for production

---

## Architecture & Design

- Monolithic Django project split into small, focused apps in `apps/` (accounts, properties, inquiries, services, admin_panel, chat, core).
- Server-side rendered templates with reusable partials in `templates/includes/`.
- Media uploads live under `media/` and are referenced from models like `PropertyImage` and `Profile`.
- Role-based access control (RBAC): custom user model supports `TENANT`, `LANDLORD`, and `ADMIN` roles.
- Admin panel: custom views provide property approval workflow and analytics over site activity.

---

## Key Models & Data

- User (custom): roles, profile data, avatar, contact info
- Property: title, description, address, district, price, features, status (PENDING/APPROVED/REJECTED/RENTED)
- PropertyImage: linked images for properties
- Inquiry: messages from tenants to landlords referencing a property
- ServiceRequest: (Find room / Shift home) user-submitted service inquiries

---

## Configuration & Important Environment Variables

Add the following to your `.env` (or set via your deployment environment):

- SECRET_KEY — Django secret
- DEBUG — `True` for dev, `False` for prod
- ALLOWED_HOSTS — comma-separated hostnames
- DATABASE_URL — e.g. `sqlite:///db.sqlite3` or a PostgreSQL URL
- EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD — for outgoing emails
- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME — when using S3 for media/static
- REDIS_URL — when using Channels/Celery

---

## Roadmap (short)

- Add email notifications for inquiries and account events
- Integrate S3 (or another cloud store) for media files
- Add optional realtime chat via Django Channels
- Add tests for `accounts`, `properties`, and `inquiries` to increase coverage

---

## ✨ Features

- Multi-role Accounts: tenant, landlord, admin
- Property management (create, edit, delete, list, favorites)
- Inquiries and contact forms
- Built-in chat for messaging
- Admin panel with analytics and user management
- Services listing (find room, shift home, etc.)
- Responsive templates and static assets

---

## 📦 Requirements

- Python 3.10+
- pip
- Virtual environment (`venv`, `virtualenv`) recommended
- See `requirements.txt` for Python package dependencies

---

## ⚙️ Environment & Configuration

1. Create a `.env` file (example variables):

```env
SECRET_KEY=replace_with_secure_value
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3  # or configure postgres
EMAIL_BACKEND=smtp
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=you@example.com
EMAIL_HOST_PASSWORD=supersecret
```

2. Update `config/settings.py` to load environment variables (project already has a `config/` module).

---

## 🛠 Development: Get Started Locally

1. Clone the repo

```bash
git clone <repo-url>
cd Hamrokotha-rental-web-application
```

2. Create and activate a virtualenv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure environment variables

```bash
cp .env.example .env
# edit .env with your values
```

4. Apply migrations and create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Collect static files (for production or to view static assets served)

```bash
python manage.py collectstatic
```

6. Run the development server

```bash
python manage.py runserver
# Visit http://127.0.0.1:8000
```

---

## 🔁 Tests

Run Django tests:

```bash
python manage.py test
```

(There are tests in `apps/properties/tests/` and other apps — add/extend tests as you add features.)

---

## 📁 Project Structure (high-level)

- `manage.py` — Django management entrypoint
- `config/` — Django settings, URLs, ASGI/WGSI
- `apps/` — Django apps (accounts, properties, inquiries, chat, services, admin_panel, core)
- `templates/` — HTML templates (base, pages, apps)
- `static/` — CSS, JS, images
- `media/` — Uploaded media (profiles, property images)

---

## 🔧 Deployment Notes

- Use PostgreSQL in production and set `DEBUG=False`.
- Configure proper `ALLOWED_HOSTS` and secure `SECRET_KEY` via environment variables.
- Serve static files with a CDN or `whitenoise` / proper webserver configuration.
- Media files should be stored on S3 or equivalent in production.
- Run migrations during deployment: `python manage.py migrate`.

Optional: containerize with Docker and use a process manager (Gunicorn + Nginx) for production.

---

## ✅ Common Management Commands

- `python manage.py createsuperuser` — create an admin
- `python manage.py collectstatic` — collect static assets
- `python manage.py loaddata <fixture>` — load fixtures
- `python manage.py shell` — interactive shell

---

## 💡 Contributing

Thanks for considering contributing! A suggested workflow:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Add tests and ensure existing tests pass
4. Run `flake8` / linters if configured
5. Open a pull request with a clear description

Please follow the existing code patterns in `apps/` and keep changes scoped to one purpose per PR.

---


## 📞 Contact

For questions or help, open an issue or reach out to the maintainers in this repository.

---

*Generated by GitHub Copilot using project files — customize any section above as needed.*
