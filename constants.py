import os
from datetime import datetime

# Constantes
THIS_YEAR = datetime.today().date().year
PROJECT_ADRESS = os.path.dirname(os.path.abspath(__file__))
LOGO_AYA = 'logo.png'

# Diccionarios
MONTHS = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 
    11: 'Noviembre', 12: 'Diciembre'
}
VACACIONES = {
    "name": "Gestor de Vacaciones",
    "file_name_xlsx": "DATOS_VACACIONES_2020-2025.xlsx",
    "file_name_csv": "vacaciones_data.csv",
    "sheet_name": "DATOS",
    "relevant_columns": [
        'APELLIDOS',
        'NOMBRES',
        'DNI',
        'CARGO',
        'Fecha Ingreso',
        'Vacaciones 2020-2021',
        'Vacaciones 2021-2022',
        'Vacaciones 2022-2023',
        'Vacaciones 2023-2024',
        'Vacaciones 2024-2025',
    ],
    "new_columns": [
        "DIAS_ACUMULADOS",
        "VACACIONES_GOZADAS",
        "VACACION_GOZADA_ACTUAL", # 3 estados (No vacaciono, esta vacacionando, por vacacionar)
        "VACACIONES_ACUMULADAS", # Dias de vacaciones acumuladas que tiene pendiente para gozar
    ]
}
VACACION_GOZADA_ACTUAL_ESTADOS = {
    0: f"Vacaciones no aplicables",
    1: f"Vacaciones {THIS_YEAR} gozadas",
    2: "Gozando vacaciones actualmente",
    3: f"Vacaciones {THIS_YEAR} por gozar",
}