from django.db import connection

def fetch_all_parser(cursor):
    col = [col[0] for col in cursor.description] #esto obtiene el nombre de las columnas
        
    return [
        dict(zip(col, row)) for row in cursor.fetchall()
        #fetchall obtiene la lista de tuplas con los resultados de la bd
    ]

class ProgramaService:
    
    @staticmethod
    def get_programa_inscripcion(estudiante_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT cpe.id, c.nombre, cp.id as campania_programa
                FROM control_escolar_programaeducativo cpe
                INNER JOIN crm_campaniaprograma cp ON cp.programa_id = cpe.id
                INNER JOIN crm_campania c ON cp.campania_id = c.id
                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM control_escolar_inscripcion cei
                    WHERE cei.campania_programa_id = cp.id 
                    AND cei.estudiante_id = %s
                )
            """, [estudiante_id])
            # print(f"{result}")
            # print(f"type{result}")

            return fetch_all_parser(cursor)