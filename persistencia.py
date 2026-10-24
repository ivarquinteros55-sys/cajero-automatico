# persistencia.py - ...

import json
import csv

from utils import obtener_fecha_hora_actual

RUTA_ARCHIVO_JSON = "datos/cajero.json"
RUTA_ARCHIVO_LOG = "datos/log_operaciones.txt"
RUTA_ARCHIVO_CSV = "datos/historial_movimientos.csv"
CAMPOS_CSV = ["id_movimiento", "id_cuenta", "tipo", "monto", "fecha", "saldo_resultante"]

def cargar_datos_json(ruta, valor_por_defecto):
    """Carga los datos desde un archivo json
       Parametros:ruta (str): ruta del archivo json.
                  valor_por_defecto (any): valor a devolver si el archivo no existe o está dañado
        Retorna:
            any: los datos cargados o el valor por defecto."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)                                      # leé el JSON con json.load
    except FileNotFoundError:
        return valor_por_defecto                           # si no existe, devolvé el valor por defecto
    except json.JSONDecodeError:
        print("El archivo de datos está dañado.")
        return valor_por_defecto                           # idem


def guardar_datos_json(ruta, datos):
    """Guarda los datos en un archivo json.
    Parametros:
        ruta (str): ruta del archivo json.
        datos (any): datos a guardar.
    """
    try:
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
    except OSError:
        print("No se pudo guardar el archivo.")


def registrar_log(ruta, mensaje):
    """Registra una entrada en el archivo de log.
    Parametros:
        ruta (str): ruta del archivo de log.
        mensaje (str): mensaje a registrar.
    """
    try:
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{obtener_fecha_hora_actual()}]: {mensaje}\n")
    except OSError:
        print("No se pudo escribir en el log.")

def exportar_movimientos_csv(ruta, movimientos):
    """Exporta los movimientos a un archivo CSV.
    Parametros:
        ruta (str): ruta del archivo CSV.
        movimientos (list): lista de diccionarios con los movimientos.
    Retorna:
        bool: True si se exportó, False si hubo un error."""
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
            escritor.writeheader()
            escritor.writerows(movimientos)
        return True
    except OSError:
        print("No se pudo exportar el archivo CSV.")
        return False


