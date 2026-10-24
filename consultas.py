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

