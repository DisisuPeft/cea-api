from django.db import connection

def fetch_all_parser(cursor):
    col = [col[0] for col in cursor.description] #esto obtiene el nombre de las columnas
        
    return [
        dict(zip(col, row)) for row in cursor.fetchall()
        #fetchall obtiene la lista de tuplas con los resultados de la bd
    ]

class CampaniaProgramaService:
    
    @staticmethod
    def get_campanias_programas():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT cc.id as ID, cc2.nombre as nombre 
                FROM crm_campaniaprograma cc
                INNER JOIN crm_campania cc2 ON cc.campania_id = cc2.id
            """)
            # print(f"{result}")
            # print(f"type{result}")

            return fetch_all_parser(cursor)