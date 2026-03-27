import pandas as pd

class csv_processing:

    #Balance general
    def procesar_bg_csv(ruta_csv: str) -> dict:
        df = pd.read_csv(ruta_csv)

        resultado = {}

        # A (Activos) -> B (columna sin nombre)
        dict_activos = dict(zip(df['Activos'], df['Unnamed: 1']))

        # C (Pasivos) -> D (columna sin nombre)
        dict_pasivos = dict(zip(df['Pasivos'], df['Unnamed: 3']))

        resultado.update(dict_activos)
        resultado.update(dict_pasivos)

        return resultado

    #Estado de Resultados
    def procesar_er_csv(ruta_csv: str) -> dict:
        df = pd.read_csv(ruta_csv)

        # A (columna sin nombre) -> B (columna sin nombre)
        return dict(zip(df['Unnamed: 0'], df['Unnamed: 1']))