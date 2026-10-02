# PocketSmart AI

PocketSmart AI is a Generative AI powered personal planning application.

The application provides:

- Home Interior Planner
- Party Planner
- Jewelry Planner
- User registration
- User login
- JWT based authentication
- SQLite database
- AI generated recommendations
- Recommendation history
- Dashboard
- Optional jewelry image upload
- REST API
- Swagger API documentation
- Fallback recommendations when Gemini is unavailable

---

# Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 templates

## Backend

- Python
- FastAPI
- Uvicorn

## Database

- SQLite

## Authentication

- JWT
- bcrypt password hashing

## AI

- Google Gemini API

---

# Project Structure

PocketSmartAI/

    app/
        main.py

        models/
            schemas.py

        routers/
            auth.py
            pages.py
            planners.py

        services/
            auth.py
            config.py
            db.py
            recommender.py

        static/
            css/
                style.css

            js/
                app.js

            uploads/

        templates/
            base.html
            dashboard.html
            history.html
            home.html
            index.html
            jewelry.html
            login.html
            party.html
            register.html

    tests/
        test_app.py

    requirements.txt
    .env.example
    .gitignore
    run.bat
    run.sh

---

# Requirements

Install Python 3.10 or newer.

Check Python:

python --version

---

# VS Code Setup

Open the PocketSmartAI folder in VS Code.

Open the VS Code terminal.

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

If PowerShell blocks activation, run:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Then activate again:

.venv\Scripts\activate

---

# Install Dependencies

Run:

pip install -r requirements.txt

---

# Environment Configuration

Copy:

.env.example

to:

.env

Example:

SECRET_KEY=your-secret-key

DATABASE_PATH=pocketsmart.db

GEMINI_API_KEY=your-gemini-api-key

GEMINI_MODEL=gemini-2.5-flash

FRONTEND_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

The Gemini API key is optional.

If the Gemini API key is not configured, PocketSmart AI will use local fallback recommendations.

---

# Run the Application

Run:

uvicorn app.main:app --reload

The application will start at:

http://127.0.0.1:8000

Open this address in your browser.

---

# Available Pages

Home:

/

Home Interior Planner:

/home

Party Planner:

/party

Jewelry Planner:

/jewelry

Login:

/login

Register:

/register

Dashboard:

/dashboard

History:

/history

Swagger API:

/docs

ReDoc:

/redoc

Health check:

/health

---

# Using PocketSmart AI

## Step 1

Open:

http://127.0.0.1:8000

## Step 2

Create an account.

## Step 3

Login.

## Step 4

Choose one of:

- Home Interior Planner
- Party Planner
- Jewelry Planner

## Step 5

Enter your requirements.

## Step 6

Click:

Generate AI Plan

## Step 7

The AI recommendation will appear below the form.

---

# Gemini AI

The application uses Google's Gemini API when a Gemini API key is configured.

The AI receives structured information from the selected planner and generates recommendations.

If the Gemini API is unavailable, PocketSmart AI automatically uses fallback recommendations.

This means the application can still be demonstrated without an API key.

---

# Database

The application automatically creates:

pocketsmart.db

The database contains:

users

recommendations

The users table stores:

- id
- username
- email
- password hash
- creation date

The recommendations table stores:

- recommendation id
- user id
- planner type
- input data
- generated result
- creation date

---

# Authentication

PocketSmart AI uses:

- bcrypt password hashing
- JWT access tokens
- HTTP-only cookies

Passwords are never stored directly in the database.

---

# API Endpoints

## Authentication

POST /auth/register

POST /auth/login

POST /auth/logout

GET /auth/session-info

GET /auth/session-data

## AI Planners

POST /generate-home

POST /generate-party

POST /generate-jewelry

## History

GET /api/history

GET /recommendations-details/{rid}

## System

GET /health

---

# Testing

Install dependencies first.

Then run:

pytest -q

Expected result:

all tests passed

---

# API Documentation

After starting the application, open:

http://127.0.0.1:8000/docs

FastAPI automatically provides interactive Swagger documentation.

You can test the APIs from the browser.

---

# Windows Shortcut

You can also run:

run.bat

---

# Linux/macOS

Make the script executable:

chmod +x run.sh

Then:

./run.sh

---

# Troubleshooting

## Python not found

Install Python and make sure it is added to PATH.

## ModuleNotFoundError

Run:

pip install -r requirements.txt

## Gemini errors

Check the GEMINI_API_KEY value in .env.

The application will use fallback recommendations if Gemini is unavailable.

## Database problems

Stop the application and remove:

pocketsmart.db

Then restart the application.

The database will be created automatically.

---

# Important

This project is designed for academic/project demonstration.

For production deployment, additional security features should be added, including:

- CSRF protection
- Rate limiting
- Secure production cookies
- HTTPS
- Strong secret management
- Production database
- Input validation
- Monitoring
- Error logging