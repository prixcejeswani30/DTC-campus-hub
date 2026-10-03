# DTC Campus Hub

A media-first campus platform for Delhi Technical Campus, built for the HackIndia Pixel to Product hackathon.
https://dtc-campus-hub.onrender.com

## Hackathon track
DTC Campus Hub is designed for the **Your Media-Savvy Startup** track. Cloudinary is a core part of the product's media workflow, not just static hosting.

## Problem

Campus information is often scattered across different sources such as
club pages, social media, notices, event announcements and academic
resources. Students may have to check multiple places to find information
about clubs, societies, events, academics, sports and campus activities.

DTC Campus Hub addresses this by bringing these campus resources and
communities together in one centralized platform, while giving authorized
administrators and club/society teams tools to manage their own content.

## Stack
- Django + PostgreSQL (SQLite automatically used locally if DATABASE_URL is absent)
- HTML/CSS/JavaScript frontend
- Django authentication + role system
- Django admin for super-admin content control
- Cloudinary for campus image uploads, cloud storage, optimization, transformations and delivery
- Render deployment configuration

## Cloudinary workflow
User-uploaded campus media is stored through Cloudinary-backed Django fields. The app uses Cloudinary for:
- organization logos and covers
- student avatars
- news images
- event posters
- club/society gallery images
- cafeteria and sports images
- automatic upload constraints such as quality/format optimization and size limits
- transformed delivery on news and event pages using resize/crop plus automatic quality and format

The Cloudinary credential is read from the **CLOUDINARY_URL** environment variable. Never commit the credential to GitHub.

### Render setup
The included render.yaml declares CLOUDINARY_URL as a secret environment variable. In Render, open the service's environment variables and add the Cloudinary environment variable from your Cloudinary account. Keep it private.

### Local setup
Create a .env file locally if you want to test real Cloudinary uploads:
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME

Do not commit .env.

## Run locally
python -m venv .venv
Windows: .venv\\Scripts\\activate
macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_demo
python manage.py runserver

Open http://127.0.0.1:8000

### Demo super admin

The demo super-admin account is created by the `seed_demo` command.
The password is supplied through the `DEMO_ADMIN_PASSWORD` environment
variable and is not stored in the repository.

For deployment, set `DEMO_ADMIN_PASSWORD` privately in Render.

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
The included render.yaml creates a web service + PostgreSQL database and declares CLOUDINARY_URL as a private secret variable. The build runs Django migrations and collects static files before starting Gunicorn.

## Before judging
Replace demo academic resources, event URLs, emails and placeholder community content with your college's verified data. Add official GGSIPU/AKTU logo assets and the real club logos from the student bodies.

## Hackathon submission checklist
- [ ] Cloudinary environment variable added privately in Render
- [ ] Test an image upload from the admin/community studio
- [ ] Confirm the uploaded asset appears in the Cloudinary Media Library
- [ ] Confirm the website displays the Cloudinary-delivered image
- [ ] Keep Cloudinary credentials out of GitHub
- [ ] Record the 2–4 minute demo showing the product and Cloudinary workflow
- [ ] Include this repository and setup instructions in the submission
