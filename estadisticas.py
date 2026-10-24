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


