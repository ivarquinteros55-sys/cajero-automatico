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


def depositar(cuenta, movimientos, monto):
    """Operacion que nos deja depositar dinero en la cuenta.
     Parametros:Cuenta,Movimientos,Monto
       Retorna (True, mensaje de deposito exitoso + nuevo saldo)."""
    cuenta["saldo"] += monto
    movimiento = crear_movimiento(movimientos, cuenta["id_cuenta"], "deposito", monto, cuenta["saldo"])
    movimientos.append(movimiento)
    return True, f"Depósito realizado. Nuevo saldo: {cuenta['saldo']:.2f}"


def transferir(cuenta_origen, cuenta_destino, movimientos, monto):
    """Operacion que nos deja transferir dinero entre cuentas.
     Parametros:Cuenta_origen,Cuenta_destino,Movimientos,Monto
       Retorna (True, mensaje de transferencia exitosa + nuevo saldo) o (False, mensaje de error)."""
    if cuenta_origen["id_cuenta"] == cuenta_destino["id_cuenta"]:
        return False, "No podés transferir a tu propia cuenta."
    if monto > cuenta_origen["saldo"]:
        return False, "Saldo insuficiente."
    cuenta_origen["saldo"] -= monto
    cuenta_destino["saldo"] += monto
    enviado = crear_movimiento(movimientos, cuenta_origen["id_cuenta"],
                               "transferencia_enviada", monto, cuenta_origen["saldo"])
    movimientos.append(enviado)
    recibido = crear_movimiento(movimientos, cuenta_destino["id_cuenta"], "transferencia_recibida", monto, cuenta_destino["saldo"])
    movimientos.append(recibido)
    return True, f"Transferencia realizada. Nuevo saldo: {cuenta_origen['saldo']:.2f}"


