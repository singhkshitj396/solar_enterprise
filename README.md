# S.K Bright Solar Energy

A responsive Django website for S.K Bright Solar Energy, with customer site-visit requests and a staff area for branch appointment management.

## Requirements

- Python 3.11 or newer
- Django, PyMySQL and Gunicorn (listed in `requirements.txt`)
- SQLite for local preview, or a MySQL database for a MySQL-backed environment

## Run locally

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

Open `http://127.0.0.1:8000/`. Local development uses SQLite and creates `db.sqlite3` in this folder.

## Prepare the super-admin

```bash
python manage.py createsuperuser
```

Sign in at `/admin/`. Create the actual branch records first, then add staff users from **Users**. Mark staff users as staff and attach a branch through their **Staff profile**. Superusers can manage all branches and appointments. Branch staff can see and update appointments assigned to their branch at `/staff/appointments/`.

When a customer submits a visit request, it is associated with an active branch whose city matches the customer's city. Requests without a matching branch remain unassigned for the super-admin to review.

No branch names, branch locations, staff accounts, project claims or customer testimonials have been invented. Add the four real branch locations, staff and verified customer content in the admin area when that information is available.

## Use MySQL

Copy `.env.example` to `.env` or set the same values in the environment. Configure:

```text
DJANGO_SECRET_KEY=<a long random value>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=your-domain.example
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.example
DB_ENGINE=mysql
MYSQL_DATABASE=sk_bright_solar
MYSQL_USER=sk_bright_app
MYSQL_PASSWORD=<database password>
MYSQL_HOST=<mysql host>
MYSQL_PORT=3306
```

Create the MySQL database and database user before running `python manage.py migrate`. Keep credentials in the hosting provider's secrets manager; do not commit them or include them in this ZIP.

For a production server, collect static files and run Gunicorn:

```bash
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Included features

- Public company site with On-Grid, Off-Grid and Hybrid solutions, services, solar applications, FAQ, contact information and appointment form
- Accessible mobile navigation, project category filters, reduced-motion support and responsive layout
- Appointment validation and persistent storage, with a staff status dashboard
- Super-admin management of branch records, staff profiles and appointment routing
- Local Bootstrap assets and a locally stored solar image
- SEO description, Open Graph metadata, structured business data and descriptive image alt text

The visit form records a requested time; it does not promise a confirmed appointment. Staff should contact the customer to confirm.
