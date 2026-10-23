def obtener_movimientos_de_cuenta(movimientos, id_cuenta):
    """Obtiene todos los movimientos de una cuenta específica.
    Parametros:
        movimientos (list): lista de movimientos existentes.
        id_cuenta (int): ID de la cuenta a filtrar.
    Retorna:
        list: lista de movimientos de la cuenta especificada."""
    resultado = []
    for movimiento in movimientos:
        if movimiento["id_cuenta"] == id_cuenta:
            resultado.append(movimiento)
    return resultado


def filtrar_movimientos_por_tipo(movimientos, tipo):
    """Filtra movimientos por tipo.
    Parametros:
        movimientos (list): lista de movimientos existentes.
        tipo (str): tipo de movimiento a filtrar.
    Retorna:
        list: lista de movimientos del tipo especificado."""
    resultado = []
    for movimiento in movimientos:
        if movimiento["tipo"] == tipo:
            resultado.append(movimiento)
    return resultado


def ordenar_movimientos(movimientos, campo="fecha", descendente=False):
    """Ordena por inserción sin modificar la lista original.
    Parametros:
        movimientos (list): lista de movimientos existentes.
        campo (str): campo por el cual ordenar (por defecto "fecha").
        descendente (bool): si es True, ordena en forma descendente.
    Retorna:
        list: lista de movimientos ordenados."""
    ordenados = list(movimientos)
    for i in range(1, len(ordenados)):
        actual = ordenados[i]
        j = i - 1
        while j >= 0 and ordenados[j][campo] > actual[campo]:   # ¿qué comparación?
            ordenados[j + 1] = ordenados[j]
            j -= 1
        ordenados[j + 1] = actual
    if descendente:
        ordenados.reverse()
    return ordenados

if __name__ == "__main__":
    movimientos = [
        {"id_movimiento": 1, "id_cuenta": 1, "tipo": "retiro", "monto": 2000, "fecha": "2026-10-20 10:00:00", "saldo_resultante": 8000},
        {"id_movimiento": 2, "id_cuenta": 2, "tipo": "deposito", "monto": 500, "fecha": "2026-10-21 09:00:00", "saldo_resultante": 1500},
        {"id_movimiento": 3, "id_cuenta": 1, "tipo": "deposito", "monto": 800, "fecha": "2026-10-19 18:30:00", "saldo_resultante": 8800},
        {"id_movimiento": 4, "id_cuenta": 1, "tipo": "retiro", "monto": 300, "fecha": "2026-10-22 12:00:00", "saldo_resultante": 8500},
    ]
    de_cuenta_1 = obtener_movimientos_de_cuenta(movimientos, 1)
    print(len(de_cuenta_1))
    retiros = filtrar_movimientos_por_tipo(de_cuenta_1, "retiro")
    print([m["id_movimiento"] for m in retiros])
    por_monto = ordenar_movimientos(de_cuenta_1, "monto")
    print([m["monto"] for m in por_monto])
    por_fecha_desc = ordenar_movimientos(de_cuenta_1, "fecha", True)
    print([m["id_movimiento"] for m in por_fecha_desc])
    print([m["id_movimiento"] for m in de_cuenta_1])