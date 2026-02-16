from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Reset Postgres sequences'

    def handle(self, *args, **options):
        print("🔄 STARTING SEQUENCE RESET...")

        try:
            with connection.cursor() as cursor:
                # Método alternativo: buscar todas las secuencias directamente
                cursor.execute("""
                               SELECT schemaname,
                                      sequencename,
                                      split_part(sequencename, '_', 1) || '_' ||
                                      split_part(sequencename, '_', 2) as table_name
                               FROM pg_sequences
                               WHERE schemaname = 'public'
                               """)

                sequences = cursor.fetchall()
                print(f"📊 Found {len(sequences)} sequences")

                for schema, seq_name, table_name in sequences:
                    # Obtener el MAX de la tabla
                    try:
                        cursor.execute(f"SELECT MAX(id) FROM {table_name}")
                        max_val = cursor.fetchone()[0] or 0

                        # Resetear la secuencia
                        cursor.execute(f"SELECT setval('{seq_name}', {max(max_val, 1)}, true)")

                        print(f'✅ Reset: {seq_name} → {max_val}')
                    except Exception as e:
                        print(f'⚠️  Skip {seq_name}: {e}')

            print("✅ SEQUENCE RESET COMPLETED!")
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise