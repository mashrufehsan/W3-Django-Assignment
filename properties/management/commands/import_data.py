from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from django.conf import settings
from getpass import getpass
import psycopg2


class Command(BaseCommand):
    help = 'Import data after verifying superadmin credentials and print database config'

    def handle(self, *args, **options):
        username = input("Enter superadmin username: ")
        password = getpass("Enter superadmin password: ")
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            self.stdout.write(self.style.SUCCESS('Admin login success'))
            db_config = settings.DATABASES['default']
            self.stdout.write(self.style.SUCCESS(
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
