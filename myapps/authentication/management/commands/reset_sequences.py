from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Reset Postgres sequences'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name, column_name
                FROM information_schema.columns
                WHERE column_default LIKE 'nextval%'
                    AND table_schema = 'public'
            """)

            for table, column in cursor.fetchall():
                cursor.execute(f"""
                    SELECT setval(
                        pg_get_serial_sequence('{table}', '{column}'),
                        COALESCE((SELECT MAX({column}) FROM {table}), 1),
                        true
                    );
                """)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully reset sequences: {table} - {column}')
                )