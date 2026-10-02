# estructuras.py - Constructores de las entidades del cajero (cuentas y movimientos).

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

