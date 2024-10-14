import psycopg
from psycopg import sql
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a PostgreSQL database if it does not exist'

    def handle(self, *args, **kwargs):
        db_name = 'scraper_db'
        db_user = 'postgres'
        db_password = 'PostAdmin#121' # Postgres Password
        db_host = 'localhost'
        db_port = '5432'

        scraper_db_admin = 'sheeshir'  # New admin user for this database
        scraper_db_pass = 'Sheeshir#121'  # Password for the new admin user

        try:
            conn = psycopg.connect(
                dbname='postgres', # need to connect to postgres to create others
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            exists = cur.fetchone()

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Database '{db_name}' already exists"))

            cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname = '{scraper_db_admin}'")
            user_exists = cur.fetchone()

            if not user_exists:
                
                cur.execute(sql.SQL(
                    "CREATE USER {} WITH PASSWORD %s"
                ).format(sql.Identifier(scraper_db_admin)), [scraper_db_pass])

                cur.execute(sql.SQL(
                    "ALTER USER {} WITH SUPERUSER"
                ).format(sql.Identifier(scraper_db_admin)))

                self.stdout.write(self.style.SUCCESS(f"Admin user '{scraper_db_admin}' created successfully"))
            else:
                self.stdout.write(self.style.WARNING(f"Admin user '{scraper_db_admin}' already exists"))

            cur.execute(sql.SQL(
                "GRANT ALL PRIVILEGES ON DATABASE {} TO {}"
            ).format(sql.Identifier(db_name), sql.Identifier(scraper_db_admin)))

            self.stdout.write(self.style.SUCCESS(f"Granted all privileges on '{db_name}' to '{scraper_db_admin}'"))

            cur.close()
            conn.close()

        except psycopg.DatabaseError as error:
            self.stdout.write(self.style.ERROR(f"Error: {error}"))
