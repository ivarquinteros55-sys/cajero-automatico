def contar_movimientos_por_tipo(movimientos):
    """Cuenta los movimientos por tipo. Retorna un diccionario {tipo: cantidad}."""
    conteo = {}
    for movimiento in movimientos:
        tipo = movimiento["tipo"]
        conteo[tipo] = conteo.get(tipo, 0) + 1
    return conteo


def calcular_promedio_monto(movimientos):
    """Calcula el promedio de los montos de los movimientos. Retorna 0 si no hay movimientos."""
    if len(movimientos) == 0:
        return 0
    total = 0
    for movimiento in movimientos:
        total += movimiento["monto"]
    return total / len(movimientos)


def obtener_monto_minimo_y_maximo(movimientos):
    """Obtiene el monto minimo y maximo de los movimientos. Retorna (minimo, maximo) o (None, None) si no hay movimientos."""
    if len(movimientos) == 0:
        return None, None
    minimo = movimientos[0]["monto"]
    maximo = minimo
    for movimiento in movimientos:
        monto = movimiento["monto"]
        if monto < minimo:
            minimo = monto
        if monto > maximo:
            maximo = monto
    return minimo, maximo


"""if __name__ == "__main__":
    movimientos = [
        {"id_movimiento": 1, "id_cuenta": 1, "tipo": "retiro", "monto": 2000, "fecha": "2026-10-20 10:00:00", "saldo_resultante": 8000},
        {"id_movimiento": 2, "id_cuenta": 2, "tipo": "deposito", "monto": 500, "fecha": "2026-10-21 09:00:00", "saldo_resultante": 1500},
        {"id_movimiento": 3, "id_cuenta": 1, "tipo": "deposito", "monto": 800, "fecha": "2026-10-19 18:30:00", "saldo_resultante": 8800},
        {"id_movimiento": 4, "id_cuenta": 1, "tipo": "retiro", "monto": 300, "fecha": "2026-10-22 12:00:00", "saldo_resultante": 8500},
    ]
    print(contar_movimientos_por_tipo(movimientos))
    print(calcular_promedio_monto(movimientos))
    print(obtener_monto_minimo_y_maximo(movimientos))
    print(calcular_promedio_monto([]), obtener_monto_minimo_y_maximo([]))"""