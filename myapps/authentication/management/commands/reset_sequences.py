from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset Postgres sequences'

    def handle(self, *args, **options):
        print("STARTING SEQUENCE RESET...")  # Agregado

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                               SELECT table_name, column_name
                               FROM information_schema.columns
                               WHERE column_default LIKE 'nextval%'
                                 AND table_schema = 'public'
                               """)

                tables = cursor.fetchall()
                print(f"Found {len(tables)} sequences to reset")  # Agregado

                for table, column in tables:
                    cursor.execute(f"""
                        SELECT setval(
                            pg_get_serial_sequence('{table}', '{column}'),
                            COALESCE((SELECT MAX({column}) FROM {table}), 1),
                            true
                        );
                    """)
                    print(f'Reset: {table}.{column}')  # Cambiado a print

            print("SEQUENCE RESET COMPLETED!")  # Agregado
        except Exception as e:
            print(f"ERROR: {e}")  # Agregado
            raise