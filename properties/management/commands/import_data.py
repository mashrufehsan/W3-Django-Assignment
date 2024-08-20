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
    help = 'Import data after verifying superadmin credentials'

    def handle(self, *args, **options):
        try:
            username = input("Enter superadmin username: ")
            password = getpass("Enter superadmin password: ")
            user = authenticate(username=username, password=password)
            if user is not None and user.is_superuser:
                self.stdout.write(self.style.SUCCESS('\nAdmin login success!'))
                db_config = settings.DATABASES['default']
                self.stdout.write(self.style.WARNING(
                    'Using the database configuration from \'.env\' file.'))
                import_db_name = os.getenv('SCRAPY_DB_NAME')
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
                        f"\nTables in {import_db_name}:"))
                    for i, table in enumerate(tables, 1):
                        self.stdout.write(
                            self.style.SUCCESS(f"{i}. {table[0]}"))
                    self.stdout.write(self.style.SUCCESS("0. All Tables"))

                    while True:
                        try:
                            selection = int(
                                input("\nEnter the number of the table you want to select (0 for all tables): "))
                            if 0 <= selection <= len(tables):
                                if selection == 0:
                                    selected_tables = [table[0]
                                                       for table in tables]
                                    self.stdout.write(self.style.SUCCESS(
                                        "You selected: All Tables"))
                                else:
                                    selected_tables = [
                                        tables[selection - 1][0]]
                                    self.stdout.write(self.style.SUCCESS(
                                        f"You selected: {selected_tables[0]}"))

                                for selected_table in selected_tables:
                                    with conn.cursor() as cur:
                                        cur.execute(
                                            f"SELECT * FROM {selected_table}")
                                        rows = cur.fetchall()
                                        colnames = [desc[0]
                                                    for desc in cur.description]
                                        for row in rows:
                                            data = dict(zip(colnames, row))

                                            title = data.get('title')
                                            location_name = data.get(
                                                'location')
                                            latitude = data.get('latitude')
                                            longitude = data.get('longitude')
                                            img_path = data.get('images')

                                            location, created = Location.objects.get_or_create(
                                                name=selected_table.capitalize() + ' - ' + location_name,
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

                                            existing_property = PropertyInfo.objects.filter(
                                                title=title, locations=location).first()

                                            if existing_property:
                                                self.stdout.write(self.style.WARNING(
                                                    f"Import skipped for {title}. Reason: Already exists with location {location.name}."))
                                                continue

                                            property_info = PropertyInfo.objects.create(
                                                title=title,
                                            )
                                            property_info.locations.add(
                                                location)

                                            import_images_folder_path = os.getenv(
                                                'IMPORT_IMAGES_FOLDER_PATH')
                                            full_img_path = os.path.join(
                                                import_images_folder_path, img_path)

                                            new_img_filename = generate_image_filename(
                                                None, os.path.basename(full_img_path))
                                            new_img_path = os.path.join(
                                                settings.MEDIA_ROOT, new_img_filename)

                                            os.makedirs(os.path.dirname(
                                                new_img_path), exist_ok=True)

                                            shutil.copy(
                                                full_img_path, new_img_path)

                                            Image.objects.create(
                                                property_info=property_info,
                                                img_path=new_img_filename,
                                            )

                                        self.stdout.write(self.style.SUCCESS(
                                            f"Data import from {selected_table} completed."))

                                self.stdout.write(self.style.SUCCESS(
                                    "All selected data import completed."))
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

        except KeyboardInterrupt:
            self.stdout.write(self.style.ERROR(
                "\nProcess interrupted. Exiting..."))
