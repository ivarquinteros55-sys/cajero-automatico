# operaciones.py - Lógica de negocio del cajero: consultar saldo y retirar dinero.

from estructuras import crear_movimiento
from utils import obtener_fecha_hora_actual


def consultar_saldo(cuenta):
    """Devuelve el saldo de la cuenta
        Parametros: Cuenta(donde consultara el saldo restante)
        Return:El saldo de la cuenta."""
    return cuenta["saldo"]


def calcular_total_retirado_hoy(movimientos, id_cuenta):
    """Suma los retiros de la cuenta realizados hoy
        Parametros:Movimientos,id_cuenta,obtener_fecha_hora_actual
        Return:.Suma de las operaciones realizadas en el dia"""
    hoy = obtener_fecha_hora_actual()[:10]   
    total = 0
    for movimiento in movimientos:
        es_de_la_cuenta = movimiento["id_cuenta"] == id_cuenta
        es_retiro = movimiento["tipo"] == "retiro"
        es_de_hoy = movimiento["fecha"][:10] == hoy
        if es_de_la_cuenta and es_retiro and es_de_hoy:
            total += movimiento["monto"]
    return total


def validar_limite_diario(cuenta, movimientos, monto):
    """Valida si lo retirado no supera el limite diario
        Parametros:Cuenta,Movimientos,Monto    
    . Retorna True o False."""
    retirado_hoy = calcular_total_retirado_hoy(movimientos, cuenta["id_cuenta"])
    return retirado_hoy + monto <= cuenta["limite_diario"]


def retirar(cuenta, movimientos, monto):
    """Operacion que nos deja realizar un retiro de la cuenta
        Parametros:Cuenta,Movimientos,Monto
    . Retorna (True, mensaje de extraccion exitosa) o (False, mensaje de error)."""
    if monto > cuenta["saldo"]:
        return False, "Saldo insuficiente."
    if not validar_limite_diario(cuenta, movimientos, monto):
        return False, "El monto supera el límite diario de retiro."
    cuenta["saldo"] -= monto                     
    movimiento = crear_movimiento(movimientos, cuenta["id_cuenta"], "retiro", monto, cuenta["saldo"])
    movimientos.append(movimiento)
    return True, f"Retiro realizado. Nuevo saldo: {cuenta['saldo']}"


"""if __name__ == "__main__":
    from estructuras import crear_cuenta

    print(crear_cuenta([], "Ana", "30123456", "x")["limite_diario"])

    cuenta = crear_cuenta([], "Ana", "30123456", "x", 100000)
    movimientos = []
    print(retirar(cuenta, movimientos, 30000))
    print(retirar(cuenta, movimientos, 30000))
    print("Total hoy:", calcular_total_retirado_hoy(movimientos, 1))
    print(retirar(cuenta, movimientos, 30000))
    print(retirar(cuenta, movimientos, 20000))
    print(retirar(cuenta, movimientos, 1))

    cuenta_chica = crear_cuenta([], "Luis", "28999111", "x", 100000)
    cuenta_chica["limite_diario"] = 10000
    print(retirar(cuenta_chica, [], 10001))"""