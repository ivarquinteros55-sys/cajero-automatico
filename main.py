# main.py - Programa principal del cajero automático: menús y flujo general.

from estructuras import crear_cuenta, buscar_cuenta_por_dni,TIPOS_MOVIMIENTO
from persistencia import (cargar_datos_json, guardar_datos_json, registrar_log,exportar_movimientos_csv,
                          RUTA_ARCHIVO_JSON, RUTA_ARCHIVO_LOG,RUTA_ARCHIVO_CSV)
from utils import hashear_pin, validar_pin, validar_dni, validar_monto, formatear_movimiento
from operaciones import consultar_saldo, retirar, depositar, transferir
from consultas import obtener_movimientos_de_cuenta, filtrar_movimientos_por_tipo, ordenar_movimientos
from estadisticas import (contar_movimientos_por_tipo, calcular_promedio_monto,
                          obtener_monto_minimo_y_maximo)


MAX_INTENTOS_LOGIN = 3

DATOS_INICIALES = {"cuentas": [], "movimientos": []}


def mostrar_menu_principal():
    """Muestra el menú principal del cajero automático."""
    print("\n=== CAJERO AUTOMÁTICO ===")
    print("1. Iniciar sesión")
    print("2. Crear cuenta")
    print("0. Salir")


def registrar_cuenta_nueva(datos):
    """Registra una nueva cuenta. Pide los datos, valida y crea la cuenta.
    parametros: datos (dict): Diccionario con las cuentas y movimientos.
    Retorna: None"""
    dni = input("DNI (7 u 8 dígitos): ").strip()
    if not validar_dni(dni):
        print("DNI inválido.")
        return
    if buscar_cuenta_por_dni(datos["cuentas"], dni) is not None:
        print("Ya existe una cuenta con ese DNI.")
        return
    titular = input("Nombre completo: ").strip()
    if titular == "":
        print("El nombre no puede estar vacío.")
        return
    pin = input("PIN de 4 dígitos: ").strip()
    if not validar_pin(pin):
        print("PIN inválido.")
        return
    saldo_inicial = validar_monto(input("Saldo inicial: ").strip())
    if saldo_inicial is None:
        print("Monto inválido.")
        return
    cuenta = crear_cuenta(datos["cuentas"], titular, dni, hashear_pin(pin), saldo_inicial)
    datos["cuentas"].append(cuenta)
    guardar_datos_json(RUTA_ARCHIVO_JSON, datos)
    registrar_log(RUTA_ARCHIVO_LOG, f"Cuenta creada: id {cuenta['id_cuenta']}")
    print("Cuenta creada con éxito.")


def main():
    """Funcion del menu. Bucle del menú principal
    parametros:Diccionario con las cuentas y movimientos
    retorna: None"""
    datos = cargar_datos_json(RUTA_ARCHIVO_JSON, DATOS_INICIALES)
    while True:
        mostrar_menu_principal()
        opcion = input("Elegí una opción: ").strip()
        
        if opcion == "1":
            cuenta = iniciar_sesion(datos)
            if cuenta is not None:
                menu_cuenta(cuenta, datos)          
        elif opcion == "2":
            registrar_cuenta_nueva(datos)
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")




def iniciar_sesion(datos):
    """Inicia sesión en el sistema. Retorna la cuenta si el login es correcto, o None.
    parametros: datos (dict): Diccionario con las cuentas y movimientos
    retorna: cuenta (dict) o None"""
    dni = input("DNI: ").strip()
    for intento in range(MAX_INTENTOS_LOGIN):
        pin = input("PIN: ").strip()
        cuenta = buscar_cuenta_por_dni(datos["cuentas"], dni)
        if cuenta is not None and cuenta["pin_hash"] == hashear_pin(pin):
            registrar_log(RUTA_ARCHIVO_LOG, f"Login correcto: cuenta {cuenta['id_cuenta']}")
            return cuenta
        registrar_log(RUTA_ARCHIVO_LOG, f"Login fallido para DNI {dni}")
        print("DNI o PIN incorrectos.")
    print("Demasiados intentos fallidos.")
    return None


def mostrar_menu_cuenta(cuenta):
    """Muestra el menú de la cuenta."""
    print(f"\n--- Bienvenido/a, {cuenta['titular']} ---")
    print("1. Consultar saldo")
    print("2. Retirar dinero")
    print("3. Depositar dinero")
    print("4. Transferir dinero")
    print("5. Ver historial de movimientos")
    print("6. Ver estadísticas")
    print("7. Exportar datos a CSV")
    print("0. Cerrar sesión")


def opcion_consultar_saldo(cuenta):
    """Muestra el saldo de la cuenta."""
    print(f"Saldo actual: {consultar_saldo(cuenta)}")


def opcion_retirar(cuenta, datos):
    """Realiza un retiro de dinero."""
    monto = pedir_monto("Monto a retirar: ")
    if monto is None:
        return
    exito, mensaje = retirar(cuenta, datos["movimientos"], monto)
    print(mensaje)
    if exito:
        guardar_y_registrar(datos, f"Retiro de {monto} en cuenta {cuenta['id_cuenta']}")

def pedir_monto(mensaje):
    """Pide un monto al usuario. Retorna el monto validado o None si es inválido."""
    monto = validar_monto(input(mensaje).strip())
    if monto is None:
        print("Monto inválido.")
    return monto


def guardar_y_registrar(datos, mensaje_log):
    """Guarda los datos. Guarda el JSON y registra la operación en el log."""
    guardar_datos_json(RUTA_ARCHIVO_JSON, datos)
    registrar_log(RUTA_ARCHIVO_LOG, mensaje_log)

def opcion_depositar(cuenta, datos):
    """Docstring completo."""
    monto = pedir_monto("Monto a depositar: ")
    if monto is None:
        return
    exito, mensaje = depositar(cuenta, datos["movimientos"], monto)
    print(mensaje)
    if exito:
        guardar_y_registrar(datos, f"Depósito de {monto} en cuenta {cuenta['id_cuenta']}")


def opcion_transferir(cuenta, datos):
    """realiza una transferencia de dinero."""
    dni_destino = input("DNI de la cuenta destino: ").strip()
    cuenta_destino = buscar_cuenta_por_dni(datos["cuentas"], dni_destino)
    if cuenta_destino is None:
        print("La cuenta destino no existe.")
        return
    monto = pedir_monto("Monto a transferir: ")
    if monto is None:
        return
    exito, mensaje = transferir(cuenta, cuenta_destino, datos["movimientos"], monto)
    print(mensaje)
    if exito:
        guardar_y_registrar(datos, f"Transferencia de {monto}: cuenta {cuenta['id_cuenta']} a cuenta {cuenta_destino['id_cuenta']}")

def mostrar_movimientos(movimientos):
    """Muestra los movimientos en la consola."""
    if len(movimientos) == 0:
        print("No hay movimientos para mostrar.")
        return
    for movimiento in movimientos:
        print(formatear_movimiento(movimiento))


def menu_historial(cuenta, datos):
    """Muestra el historial y su menú. Submenú del historial de movimientos."""
    propios = obtener_movimientos_de_cuenta(datos["movimientos"], cuenta["id_cuenta"])
    while True:
        print("\n--- Historial de movimientos ---")
        print("1. Ver todos (más recientes primero)")
        print("2. Filtrar por tipo")
        print("3. Ordenar por monto (mayor a menor)")
        print("0. Volver")
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1":
            mostrar_movimientos(ordenar_movimientos(propios, "fecha", True))
        elif opcion == "2":
            tipo = input(f"Tipo ({', '.join(TIPOS_MOVIMIENTO)}): ").strip()
            if tipo in TIPOS_MOVIMIENTO:
                mostrar_movimientos(filtrar_movimientos_por_tipo(propios, tipo))
            else:
                print("Tipo inválido.")
        elif opcion == "3":
            mostrar_movimientos(ordenar_movimientos(propios, "monto", True))
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


def opcion_estadisticas(cuenta, datos):
    """Muestra estadisticas de la cuenta."""
    propios = obtener_movimientos_de_cuenta(datos["movimientos"], cuenta["id_cuenta"])
    if len(propios) == 0:
        print("Todavía no tenés movimientos.")
        return
    print("\n--- Estadísticas de tu cuenta ---")
    for tipo, cantidad in contar_movimientos_por_tipo(propios).items():
        print(f"{tipo}: {cantidad}")
    print(f"Monto promedio: {calcular_promedio_monto(propios):.2f}")
    minimo, maximo = obtener_monto_minimo_y_maximo(propios)
    print(f"Monto mínimo: {minimo:.2f} | Monto máximo: {maximo:.2f}")


def opcion_exportar_csv(cuenta, datos):
    """Exporta datos a un archivo CSV."""
    propios = obtener_movimientos_de_cuenta(datos["movimientos"], cuenta["id_cuenta"])
    if exportar_movimientos_csv(RUTA_ARCHIVO_CSV, propios):
        registrar_log(RUTA_ARCHIVO_LOG, f"Exportación CSV de cuenta {cuenta['id_cuenta']}")
        print(f"Historial exportado a {RUTA_ARCHIVO_CSV}")


def menu_cuenta(cuenta, datos):
    """Menu de sesión. Bucle del submenú de la cuenta.
    parametros: cuenta (dict): La cuenta del usuario
    datos (dict): Diccionario con las cuentas y movimientos
    retorna: None"""
    while True:
        mostrar_menu_cuenta(cuenta)
        opcion = input("Elegí una opción: ").strip()
        
        if opcion == "1":
            opcion_consultar_saldo(cuenta)
        elif opcion == "2":
            opcion_retirar(cuenta, datos)
        elif opcion == "3":
            opcion_depositar(cuenta, datos)
        elif opcion == "4":
            opcion_transferir(cuenta, datos)
        elif opcion == "5":
            menu_historial(cuenta, datos)
        elif opcion == "6":
            opcion_estadisticas(cuenta, datos)
        elif opcion == "7":
            opcion_exportar_csv(cuenta, datos)        
        elif opcion == "0":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")
       

if __name__ == "__main__":
    main()


