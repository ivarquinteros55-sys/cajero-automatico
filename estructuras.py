# estructuras.py - Constructores de las entidades del cajero (cuentas y movimientos).
from utils import obtener_fecha_hora_actual
LIMITE_DIARIO_POR_DEFECTO = 5000000


def generar_siguiente_id(lista, clave_id):
    """Devuelve el próximo ID para una lista de diccionarios.

    Parámetros:
        lista (list): lista de diccionarios existentes.
        clave_id (str): nombre de la clave que guarda el ID.

    Retorna:
        int: 1 si la lista está vacía, o el último ID + 1.
    """
    if len(lista) == 0:
        return 1
    return lista[-1][clave_id] + 1


def crear_cuenta(cuentas, titular, dni, pin_hash, saldo_inicial=0):
    """Crea un diccionario que representa una cuenta bancaria.
    
     Parámetros:
        cuentas (list): lista de cuentas existentes (para calcular el ID).
        titular (str): nombre completo del titular.
        dni (str): documento del titular.
        pin_hash (str): PIN ya hasheado.
        saldo_inicial (float): saldo con el que se abre la cuenta (por defecto 0).

        Retorna:
        dict: cuenta con id_cuenta, titular, dni, pin_hash, saldo y limite_diario.
        """
    id_nuevo = generar_siguiente_id(cuentas, "id_cuenta")
    cuenta = {
        "id_cuenta": id_nuevo,
        "titular": titular,
        "dni": dni,
        "pin_hash": pin_hash,
        "saldo": saldo_inicial,
        "limite_diario": LIMITE_DIARIO_POR_DEFECTO,  
    }
    return cuenta

def buscar_cuenta_por_dni(cuentas, dni):
    """Busca una cuenta en la lista de cuentas por su DNI.
    parámetros:
        cuentas (list): lista de cuentas existentes.
        dni (str): documento del titular a buscar.
    Retorna:
        dict: cuenta encontrada o None si no existe."""
    for cuenta in cuentas:           
        if cuenta["dni"] == dni:   
            return cuenta          
    return None   

def crear_movimiento(movimientos, id_cuenta, tipo, monto, saldo_resultante):
    """Crea un diccionario que representa un movimiento bancario.
    
    Parámetros:
        movimientos (list): lista de movimientos existentes (para calcular el ID).
        id_cuenta (int): ID de la cuenta involucrada.
        tipo (str): tipo de movimiento ("deposito", "retiro" o "transferencia").
        monto (float): cantidad de dinero involucrada.
        saldo_resultante (float): saldo de la cuenta después del movimiento.

    Retorna:
        dict: movimiento con id_movimiento, id_cuenta, tipo, monto, fecha y saldo_resultante.
    """
    id_nuevo = generar_siguiente_id(movimientos, "id_movimiento")
    movimiento = {
        "id_movimiento": id_nuevo,
        "id_cuenta": id_cuenta,
        "tipo": tipo,
        "monto": monto,
        "fecha": obtener_fecha_hora_actual(),
        "saldo_resultante": saldo_resultante,
    }
    return movimiento


""" bloque de prueba para ejecutar el código y ver si funciona correctamente
if __name__ == "__main__":
    cuentas = []
    cuenta_1 = crear_cuenta(cuentas, "Ana Pérez", "30123456", "hash_de_prueba")
    cuentas.append(cuenta_1)
    cuenta_2 = crear_cuenta(cuentas, "Luis Gómez", "28999111", "hash_de_prueba")
    
    cuentas = [cuenta_1, cuenta_2]
    print(buscar_cuenta_por_dni(cuentas, "28999111"))  # debe mostrar a Luis Gómez
    print(buscar_cuenta_por_dni(cuentas, "00000000"))  # debe mostrar None
    movimientos = []
    mov_1 = crear_movimiento(movimientos, 1, "retiro", 2000, 8000)
    movimientos.append(mov_1)
    mov_2 = crear_movimiento(movimientos, 1, "deposito", 500, 8500)
    print(mov_1)
    print(mov_2)
"""
