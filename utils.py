# utils.py - Funciones de utilidad para el cajero automático.

from datetime import datetime


def obtener_fecha_hora_actual():
    """Devuelve la fecha y hora actual en formato de cadena."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    print(obtener_fecha_hora_actual())