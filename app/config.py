import pandas as pd
import polars as pl
import os
from datetime import datetime
import math

# Constantes
START_YEAR = 2020
TODAY = datetime.today().date()
THIS_YEAR = TODAY.year
PROJECT_ADRESS = os.path.dirname(os.path.abspath(__file__))
LOGO_AYA = 'logo.png'
PORT = 8001

# Listas
VACATION_PERIODS = [f"Vacaciones {y}-{y+1}" for y in range(START_YEAR, THIS_YEAR)]

# Diccionarios
MONTHS = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 
    11: 'Noviembre', 12: 'Diciembre'
}
VACACIONES = {
    "name": "Gestor de Vacaciones",
    "file_name": "DATOS_VACACIONES.xlsx",
    "sheet_name": "DATOS",
    "relevant_columns": [
        'APELLIDOS',
        'NOMBRES',
        'DNI',
        'CARGO',
        'Fecha Ingreso',
        *VACATION_PERIODS
    ],
    "states": {
        0: 'Gozó',
        1: 'Gozando',
        2: 'Por gozar',
        3: 'No aplica',
    },
}