
# Property Information Management Django Application #

This Django application is designed to store and manage property information using the Django admin interface. It includes models for properties, images, locations, and amenities. The application uses PostgreSQL as the database and enables CRUD operations for all models while maintaining their relationships. Additionally, it provides a CLI application to migrate data from a Scrapy project database to Django.


## Features ##

- **Django Admin Interface:** Manage property information with proper authentication.
- **PostgreSQL Database:** Use PostgreSQL for data storage.
- **Django ORM:** Use Django ORM for database interactions.
- **Data Migration:** CLI tool to migrate data from a Scrapy project database.

## Index ##
- 👆🏼 [Installation](#Installation "Go to: Installation")
- 👆🏼 [Using the CLI application](#Using-the-CLI-application "Go to: Using the CLI application")

## Installation ##

### Prerequisites ###
- Python
- PostgreSQL

### Steps ###

1. **Clone and navigate to the the Repository.**
    ```bash
    git clone https://github.com/mashrufehsan/W3-Django-Assignment.git
    cd W3-Django-Assignment
    ```
2. **Create and Activate Virtual Environment.**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
3. **Install Dependencies.**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set up the database.**

    Create a PostgreSQL database. You can do this using the psql command-line tool or a PostgreSQL client.
    ```bash
    CREATE DATABASE property_db;
    ```
5. **Configure environment variables.**

    Copy the .env.sample file to .env and fill in the required configuration:

    ```bash
    cp .env.sample .env
    ```
    Update the .env file with your PostgreSQL database credentials.
6. **Run Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7. **Create Superuser**
    ```bash
    python manage.py createsuperuser
    ```
8. **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

## Using the CLI application ##
Continuing