from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.conf import settings
from getpass import getpass
import psycopg2
from properties.models import PropertyInfo, Location, Image, generate_image_filename
from dotenv import load_dotenv
import os
import shutil

load_dotenv()


class Command(BaseCommand):
    help = 'Import data after verifying superadmin credentials and print database config'

    def handle(self, *args, **options):
        username = input("Enter superadmin username: ")
        password = getpass("Enter superadmin password: ")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            self.stdout.write(self.style.SUCCESS('Admin login success'))
            db_config = settings.DATABASES['default']
            self.stdout.write(self.style.ERROR(
                'Using the database configuration from \'.env\' file'))
            import_db_name = input(
                "Enter the name of the database to import from: ")
            try:
                conn = psycopg2.connect(
                    dbname=import_db_name,
                    user=db_config['USER'],
                    password=db_config['PASSWORD'],
                    host=db_config['HOST'],
                    port=db_config.get('PORT', '5432')
                )
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    """)
                    tables = cur.fetchall()
                self.stdout.write(self.style.SUCCESS(
                    f"Tables in {import_db_name}:"))
                for i, table in enumerate(tables, 1):
                    self.stdout.write(self.style.SUCCESS(f"{i}. {table[0]}"))
                while True:
                    try:
                        selection = int(
                            input("Enter the number of the table you want to select (e.g. 1): "))
                        if 1 <= selection <= len(tables):
                            selected_table = tables[selection - 1][0]
                            self.stdout.write(self.style.SUCCESS(
                                f"You selected: {selected_table}"))

                            # Add this part to fetch the first row and import data
                            with conn.cursor() as cur:
                                cur.execute(
                                    f"SELECT * FROM {selected_table} LIMIT 1")
                                row = cur.fetchone()
                                if row:
                                    colnames = [desc[0]
                                                for desc in cur.description]
                                    data = dict(zip(colnames, row))

                                    # Extract data from the row
                                    title = data.get('title')
                                    location_name = data.get('location')
                                    latitude = data.get('latitude')
                                    longitude = data.get('longitude')
                                    img_path = data.get('images')

                                    # Create or update Location
                                    location, created = Location.objects.get_or_create(
                                        name=location_name,
                                        type='city',
                                        defaults={
                                            'latitude': latitude,
                                            'longitude': longitude,
                                        },
                                    )
                                    if not created:
                                        location.latitude = latitude
                                        location.longitude = longitude
                                        location.save()

                                    # Create PropertyInfo
                                    property_info = PropertyInfo.objects.create(
                                        title=title,
                                    )
                                    property_info.locations.add(location)

                                    # Handle Image Path
                                    import_images_folder_path = os.getenv(
                                        'IMPORT_IMAGES_FOLDER_PATH')
                                    full_img_path = os.path.join(
                                        import_images_folder_path, img_path)

                                    # Generate new image filename
                                    new_img_filename = generate_image_filename(
                                        None, os.path.basename(full_img_path))
                                    new_img_path = os.path.join(
                                        settings.MEDIA_ROOT, new_img_filename)

                                    # Copy the image to the new path
                                    shutil.copy(full_img_path, new_img_path)

                                    # Create Image
                                    Image.objects.create(
                                        property_info=property_info,
                                        img_path=new_img_filename,
                                    )

                                    self.stdout.write(self.style.SUCCESS(
                                        f"Data imported successfully for the first row of {selected_table}"))

                                else:
                                    self.stdout.write(self.style.ERROR(
                                        f"No data found in table {selected_table}"))

                            break
                        else:
                            self.stdout.write(self.style.ERROR(
                                "Invalid selection. Please try again."))
                    except ValueError:
                        self.stdout.write(self.style.ERROR(
                            "Invalid input. Please enter a number."))
                conn.close()

            except psycopg2.Error as e:
                self.stdout.write(self.style.ERROR(
                    f"Unable to connect to the database: {e}"))

        else:
            self.stdout.write(self.style.ERROR(
                'Invalid credentials or user is not a superadmin'))
