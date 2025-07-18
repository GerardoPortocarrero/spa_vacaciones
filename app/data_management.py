import pandas as pd
import polars as pl
import math
from .config import NO_PROGRAMADO, DIAS_GOZADOS, SUBSIDIO

# Eliminar columnas innecesarias
def get_relevant_columns(df, document):
    return df[document['relevant_columns']]

# Filtrar ruido (obtener la tabla principal)
def filter_noise(df):
    df.columns = df.iloc[0].astype(str).str.strip()
    return df.iloc[1:].reset_index(drop=True)

# Expresión para limpiar y concatenar
def clean_and_concatenate():
    return (
        pl.col("NOMBRES")
        .str.replace_all(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]", "")  # Mantener letras con tilde, ñ y espacios
        .str.strip_chars()
        .str.strip_chars(" ")
        .str.strip_chars(".")
        + pl.lit(" ") +
        pl.col("APELLIDOS")
        .str.replace_all(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]", "")
        .str.strip_chars()
        .str.strip_chars(" ")
        .str.strip_chars(".")
    ).str.strip_chars()

# Convertir columna str a fecha
def str_to_date(df, column_name):
    return df.with_columns(
        pl.col(column_name)
        .str.strptime(pl.Date, format="%Y-%m-%d %H:%M:%S", strict=False)
    )

# Convertir valor str a fecha
def str_to_date_value(valor):
    # Usamos un DataFrame temporal con una sola fila y columna
    df = pl.DataFrame({"tmp": [valor]})
    
    try:
        df = df.with_columns(
            pl.col("tmp").str.strptime(pl.Date, format="%Y-%m-%d %H:%M:%S", strict=False)
        )
        return df[0, "tmp"]
    except:
        return None

# Calcular la nueva matriz de vacaciones
def calcular_dias(vacacion, ingreso, today, THIS_YEAR):
    aniversario = ingreso.replace(year=today.year)

    if str(vacacion) == NO_PROGRAMADO:
        if ingreso.year < THIS_YEAR:
            aniversario = aniversario.replace(year=aniversario.year - 1)
    elif (today < vacacion) or (today > vacacion and today < aniversario):
        aniversario = aniversario.replace(year=aniversario.year - 1)

    # Calcular días acumulados desde el aniversario hasta today
    dias_acumulados = ((today - aniversario).days / 365) * 30
    dias_acumulados = round(dias_acumulados, 2)

    # Redondear si aún positivo
    return dias_acumulados
    
def es_nan(vacacion):
    return (
        vacacion is None or
        (isinstance(vacacion, float) and math.isnan(vacacion)) or
        (isinstance(vacacion, str) and vacacion.strip().lower() in ("", "nan"))
    )

def expandir_vacaciones(df: pl.DataFrame, TODAY, THIS_YEAR, VACATION_PERIODS: list[str], states: dict[int, str]) -> pl.DataFrame:
    registros = []

    for col in VACATION_PERIODS:
        if not col.startswith("Vacaciones"):
            continue

        try:
            PERIOD_YEAR = int(col.split()[1].split("-")[1])
        except Exception:
            continue

        for row in df.iter_rows(named=True):
            nombre = row.get("NOMBRE", "").strip()
            dni = row.get("DNI", "")
            cargo = row.get("CARGO", "")
            ingreso = row.get("Fecha Ingreso", "")
            vacacion = row.get(col, None)
            estado = ""
            dias = ""

            # Si es SUBSIDIO
            if str(vacacion).strip().upper() == SUBSIDIO.upper():
                vacacion = SUBSIDIO
                estado = states[3]  # 'No aplica'
                dias = 0.0

            # Si está vacío tipo NaN y el periodo es menor al año actual
            elif  PERIOD_YEAR < THIS_YEAR:
                if es_nan(vacacion):
                    continue
                else:
                    vacacion = str_to_date_value(vacacion)
                    estado = states[0]  # 'Gozó'
                    dias = DIAS_GOZADOS

            # Si esta vacio o es fecha correcta y el periodo es del año actual
            else:                
                if PERIOD_YEAR == THIS_YEAR:
                    # Si la fecha esta vacia
                    if es_nan(vacacion):
                        vacacion = NO_PROGRAMADO
                        estado = states[3]  # 'No aplica'
                        dias = calcular_dias(vacacion, ingreso, TODAY, THIS_YEAR)
                    # Si la fecha es correcta
                    else:
                        vacacion = str_to_date_value(vacacion)
                        # Gozó
                        if vacacion < TODAY:                            
                            estado = states[0]
                            dias = calcular_dias(vacacion, ingreso, TODAY, THIS_YEAR)
                        # Gozando                            
                        elif vacacion.month == TODAY.month:
                            estado = states[1]
                            dias = calcular_dias(vacacion, ingreso, TODAY, THIS_YEAR)
                        # Por gozar
                        else:
                            estado = states[2]
                            dias = calcular_dias(vacacion, ingreso, TODAY, THIS_YEAR)

            registros.append({
                "Periodo": PERIOD_YEAR,
                "Nombre": nombre,
                "Dni": dni,
                "Cargo": cargo,
                "Ingreso": ingreso,
                "Vacaciones": str(vacacion),
                "Estado": estado,
                "Dias": dias
            })

    return pl.DataFrame(registros)

# Procesar dataframe
def process_data(VACACIONES):
    # Leer Excel con pandas
    df_pd = pd.read_excel(
        VACACIONES['file_name'],
        sheet_name=VACACIONES['sheet_name'],
        header=None
    )

    # Limpiar datos
    df_pd = filter_noise(df_pd)
    df_pd = get_relevant_columns(df_pd, VACACIONES)

    # Asegurarse que todo es str (para que acepte el cambio de pandas a polars
    # ya que hay columnas que son fecha y a la vez str como SUBSIDIO)
    df_pd = df_pd.astype(str)

    # Convertir a polars
    df_pl = pl.from_pandas(df_pd)    

    return df_pl

# Transformar dataframe
def transform_data(df, TODAY, THIS_YEAR, VACATION_PERIODS, STATES):
    # Aplicar la transformación
    df = df.with_columns(
        clean_and_concatenate().alias("NOMBRE")
    )

    # Cambiar tipo de columna a fecha
    df = str_to_date(df, 'Fecha Ingreso')

    # Calcular historial, vacaciones y estado
    df = expandir_vacaciones(df, TODAY, THIS_YEAR, VACATION_PERIODS, STATES)

    # content = df.write_csv(separator=";")
    # with open("file.csv", "w", encoding="utf-8-sig") as f_out:
    #     f_out.write(content)

    return df