# DTC Campus Hub

A media-first campus platform for Delhi Technical Campus, built for the HackIndia Pixel to Product hackathon.

## Stack
- Django + PostgreSQL (SQLite automatically used locally if DATABASE_URL is absent)
- HTML/CSS/JavaScript frontend
- Django authentication + role system
- Django admin for super-admin content control
- Render deployment configuration

## Run locally
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000

### Demo super admin
- Email: `admin@dtc.ac.in`
- Password: `Admin@123`

Change this password before any real deployment.

## Main modules
- Technical clubs: ACE, AIR, CESTA, E-Cell, FOSS, GDG, GFG, INDUS RISE
- Cultural societies: Aavansh, Ameya, Artistia, Awaaz, Conchord, IBTIDAA, Tasveer
- Club/society pages with people, updates, events, media and follow
- Campus news and event calendar
- GGSIPU + AKTU academic hubs: syllabus, exams, calendar, notices, results, study resources
- Cafeteria + mess
- Sports: teams, tournaments, fixtures, results, photos, registration and notices
- Student profiles, login/signup, notifications
- Super-admin and organization-scoped community studio

## Render
The included `render.yaml` creates a web service + PostgreSQL database. After connecting the repo to Render, deploy from the Blueprint. For production media uploads, use object storage such as Cloudinary or S3 because Render's local filesystem is not intended for permanent user-uploaded media.

## Before judging
Replace demo academic resources, event URLs, emails and placeholder community content with your college's verified data. Add official GGSIPU/AKTU logo assets and the real club logos from the student bodies.
