
# Property Information Management Django Application #

This Django application is designed to store and manage property information using the Django admin interface. It includes models for properties, images, locations, and amenities. The application uses PostgreSQL as the database and enables CRUD operations for all models while maintaining their relationships. Additionally, it provides a CLI application to migrate data from a Scrapy project database to Django.


## Features ##

- **Django Admin Interface:** Manage property information with proper authentication.
- **PostgreSQL Database:** Use PostgreSQL for data storage.
- **Django ORM:** Use Django ORM for database interactions.
- **Data Migration:** CLI tool to migrate data from a Scrapy project database.

## Index ##
- 👉 [Installation](#Installation "Go to: Installation")
- 👉 [Admin Interface](#Admin-Interface "Go to: Admin Interface")
- 👉 [Using the CLI application](#Using-the-CLI-application "Go to: Using the CLI application")
- 👉 [Models](#Models "Go to: Models")

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

    Copy the .env.sample file to .env and fill in the required database configuration.
    - On macOS/Linux:
        ```bash
        cp .env.sample .env
        ```
    - On windows:
        ```bash
        copy .env.sample .env
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

## Admin Interface ##
Once the server is running, the Djnago admin interface can be accessed at:
> http://localhost:8000/admin

## Using the CLI application ##
This CLI application imports `title`, `location`, `latitude`, `longitude` and `image` for each hotel into the Django databse.

1. **Configure environment variables.**

    Make sure to set "IMPORT_IMAGES_FOLDER_PATH" to allow the CLI application to function properly.
    
    To get the path of a directory:
    
    - Navigate to the directory.
    - Open the terminal.
    - Type the following command:
        - On macOS/Linux:
            ```bash
            pwd
            ```
        - On Windows:
            ```bash
            cd
            ```
            Alternatively, you can copy the path directly from the File Explorer address bar.

    **Example:**

    If the path of an image in the Scrapy database is:
    ```
    /home/user/Desktop/ScrapyProject/images/hotel_1.png
    ```
    Then set `IMPORT_IMAGES_FOLDER_PATH` as:
    ```
    IMPORT_IMAGES_FOLDER_PATH=/home/user/Desktop/ScrapyProject/
    ```
2. **Start the CLI application**
    ```bash
    python manage.py import_data
    ```
Upon running the application, you will be prompted to enter the superuser admin `username` and `password`.

If authenticated successfully, a list of table names from the database will appear, such as:
1. paris
2. lijiang

Type the corresponding number to select the table. For example, type `1` to select the `paris` table. The application will then import all the data from the selected table into the Django database.

## Models

### PropertyInfo
Represents a property with detailed information and relationships to other models.

- **title**: `CharField` - Title of the property.
- **description**: `TextField` - Detailed description of the property (nullable).
- **locations**: `ManyToManyField` - Relationship to the `Location` model, representing a many-to-many relationship.
- **amenities**: `ManyToManyField` - Relationship to the `Amenity` model, representing a many-to-many relationship.
- **created_date**: `DateTimeField` - Timestamp of when the property was created.
- **updated_date**: `DateTimeField` - Timestamp of when the property was last updated.

**Meta Options:**
- `db_table`: 'property_info'.
- `verbose_name_plural`: 'Property Info'.

### Image
Represents an image associated with a property.

- **property_info**: `ForeignKey` - Relationship to the `PropertyInfo` model.
- **img_path**: `ImageField` - Path to the image file, with a custom filename generator.
- **created_date**: `DateTimeField` - Timestamp of when the image was uploaded.
- **updated_date**: `DateTimeField` - Timestamp of when the image was last updated.

**Meta Options:**
- `db_table`: 'image'.
- `verbose_name_plural`: 'Images'.

**Additional Functionality:**
- **delete**: Custom delete method to remove the image file from the filesystem when the image object is deleted.
- **pre_delete Signal**: Signal to remove the image file from the filesystem when the image object is deleted.

### Location
Represents a geographical location with different types (country, state, city).

- **name**: `CharField` - Name of the location.
- **type**: `CharField` - Type of the location (choices: Country, State, City).
- **latitude**: `DecimalField` - Latitude coordinate of the location (nullable).
- **longitude**: `DecimalField` - Longitude coordinate of the location (nullable).
- **created_date**: `DateTimeField` - Timestamp of when the location was created.
- **updated_date**: `DateTimeField` - Timestamp of when the location was last updated.

**Meta Options:**
- `unique_together`: Ensures a unique combination of name and type.
- `db_table`: 'location'.
- `verbose_name_plural`: 'Locations'.

### Amenity
Represents an amenity that can be associated with a property.

- **name**: `CharField` - Name of the amenity (unique).
- **created_date**: `DateTimeField` - Timestamp of when the amenity was created.
- **updated_date**: `DateTimeField` - Timestamp of when the amenity was last updated.

**Meta Options:**
- `db_table`: 'amenity'.
- `verbose_name_plural`: 'Amenities'.

## Notes

- Ensure PostgreSQL is running and accessible with the credentials provided in the .env file.
