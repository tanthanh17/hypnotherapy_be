# Django Project

This project is built with **Django 4.2.16**. Follow the steps below to set it up and run.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- PostgreSQL 16

## How to Run

1. Clone the repository:

   ```bash
   cd hypnotherapy_be

2. Create and activate a virtual environment
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

2. Install dependencies:
    ```bash
    pip install -r requirements.txt

3. Apply migrations to set up the database:
    ```bash
    python manage.py migrate

4. Start the development server
    ```bash
    python manage.py runserver