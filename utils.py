# utils.py - Funciones de utilidad para el cajero automático.
import hashlib
import math
from datetime import datetime


def validar_dni(dni):
    """Verifica que el DNI tenga 7 u 8 dígitos. Retorna True si es válido."""
    return dni.isdigit() and 7 <= len(dni) <= 8

def obtener_fecha_hora_actual():
    """Devuelve la fecha y hora actual en formato de cadena."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")




def hashear_pin(pin):
    """Hashea el PIN utilizando SHA-256
     Parametros:
        pin (str): PIN a hashear.
     Retorna:
        str: PIN hasheado."""
    pin_en_bytes = pin.encode("utf-8")
    return hashlib.sha256(pin_en_bytes).hexdigest()   


def validar_pin(pin):
    """Validez el PIN. Retorna True o False
    Parametros:
        pin (str): PIN a validar.
    Retorna:
        bool: True si el PIN es válido, False en caso contrario."""
    return len(pin) == 4 and pin.isdigit()   


def validar_monto(texto):
    """Validez el monto. Retorna el monto (float) o None si no es válido.
    Parametros:
        texto (str): texto a validar.
    Retorna:
        float or None: monto válido o None si no es válido."""
    try:
        monto = float(texto)                     
    except ValueError:
        return None                             
    if monto > 0 and math.isfinite(monto):
        return monto
    return None

"""
if __name__ == "__main__":
    print(obtener_fecha_hora_actual())
    print(hashear_pin("1234"))
    print(validar_pin("1234"), validar_pin("123"), validar_pin("12a4"))
    for texto in ["1500.50", "0", "-5", "abc", "", "inf"]:
        print(repr(texto), "->", validar_monto(texto))
"""