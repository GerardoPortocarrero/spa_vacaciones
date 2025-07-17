import pandas as pd
import polars as pl

# Eliminar columnas innecesarias
def get_relevant_columns(df, document):
    return df[document['relevant_columns']]

# Filtrar ruido (obtener la tabla principal)
def filter_noise(df):
    df.columns = df.iloc[0].astype(str).str.strip()
    return df.iloc[1:].reset_index(drop=True)

# Procesar dataframe
def process_data(VACACIONES, document):
    # Leer Excel con pandas
    df_pd = pd.read_excel(
        VACACIONES['file_name'],
        sheet_name=VACACIONES['sheet_name'],
        header=None
    )

    # Limpiar datos
    df_pd = filter_noise(df_pd)
    df_pd = get_relevant_columns(df_pd, document)

    # Convertir a polars directamente
    df_pl = pl.from_pandas(df_pd)

    return df_pl
