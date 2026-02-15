from django.db import connection

def fetch_all_parser(cursor):
    col = [col[0] for col in cursor.description] #esto obtiene el nombre de las columnas
        
    return [
        dict(zip(col, row)) for row in cursor.fetchall()
        #fetchall obtiene la lista de tuplas con los resultados de la bd
    ]

class FichasService:
    
    @staticmethod
    def get_fichas(user_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pe.nombre as inscrito, ee.email,CONCAT(pu.nombre,' ',pu.apellidoP,' ',pu.apellidoM) as nombreAlumno, f.autorizado, c.monto as comision, ee.id as identificador_alumno, f.id  FROM control_escolar_fichas f
                INNER JOIN crm_campaniaprograma cp on f.campania_programa_id = cp.id
                INNER JOIN control_escolar_programaeducativo pe on cp.programa_id = pe.id
                INNER JOIN estudiantes_estudiante ee on f.estudiante_id = ee.id
                INNER JOIN perfil_user pu on ee.perfil_id = pu.id
                INNER JOIN control_escolar_inscripcion i on ee.id = i.estudiante_id
                INNER JOIN control_escolar_comisiones c on f.id = c.ficha_id
                INNER JOIN authentication_usercustomize as u on f.vendedor_id = u.id
                WHERE u.id = %s
            """, [user_id])
            # print(f"{result}")
            # print(f"type{result}")

            return fetch_all_parser(cursor)