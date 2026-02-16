from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset Postgres sequences'

    def handle(self, *args, **options):
        print("🔄 STARTING SEQUENCE RESET...")

        try:
            with connection.cursor() as cursor:
                # Primero verificar el MAX real
                cursor.execute("SELECT MAX(id) FROM authentication_usercustomize")
                max_id = cursor.fetchone()[0]
                print(f"📊 MAX ID in authentication_usercustomize: {max_id}")

                cursor.execute("""
                               SELECT table_name, column_name
                               FROM information_schema.columns
                               WHERE column_default LIKE 'nextval%'
                                 AND table_schema = 'public'
                               """)

                tables = cursor.fetchall()
                print(f"📊 Found {len(tables)} sequences to reset")

                for table, column in tables:
                    # Mostrar el MAX antes de resetear
                    try:
                        cursor.execute(f"SELECT MAX({column}) FROM {table}")
                        current_max = cursor.fetchone()[0]
                        print(f"📈 {table}.{column} - Current MAX: {current_max}")
                    except:
                        current_max = 0

                    # Resetear
                    cursor.execute(f"""
                        SELECT setval(
                            pg_get_serial_sequence('{table}', '{column}'),
                            GREATEST(COALESCE((SELECT MAX({column}) FROM {table}), 1), 1),
                            true
                        );
                    """)
                    print(f'✅ Reset: {table}.{column} to {current_max or 1}')

            print("✅ SEQUENCE RESET COMPLETED!")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise