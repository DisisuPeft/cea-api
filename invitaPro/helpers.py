from datetime import date, timedelta
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

def generar_fechas_cobro(fecha_inicio: date, unidad: str, intervalo: int, numero_pagos: int):
    fechas = []
    actual = fecha_inicio
    for _ in range(numero_pagos):
        fechas.append(actual)
        if unidad == "days":
            actual = actual + timedelta(days=intervalo)
        elif unidad == "weeks":
            actual = actual + timedelta(weeks=intervalo)
        elif unidad == "months":
            actual = actual + relativedelta(months=+intervalo)
        elif unidad == "years":
            actual = actual + relativedelta(years=+intervalo)
        else:
            # fallback a meses
            actual = actual + relativedelta(months=+intervalo)
    return fechas