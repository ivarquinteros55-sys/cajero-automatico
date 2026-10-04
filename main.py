# main.py - Programa principal del cajero automático: menús y flujo general.

from estructuras import crear_cuenta, buscar_cuenta_por_dni
from persistencia import (cargar_datos_json, guardar_datos_json, registrar_log,
                          RUTA_ARCHIVO_JSON, RUTA_ARCHIVO_LOG)
from utils import hashear_pin, validar_pin, validar_dni, validar_monto
from operaciones import consultar_saldo, retirar

MAX_INTENTOS_LOGIN = 3

DATOS_INICIALES = {"cuentas": [], "movimientos": []}


def mostrar_menu_principal():
    """Muestra el menú principal del cajero automático."""
    print("\n=== CAJERO AUTOMÁTICO ===")
    print("1. Iniciar sesión")
    print("2. Crear cuenta")
    print("0. Salir")


def registrar_cuenta_nueva(datos):
    """Docstring completo. Pide los datos, valida y crea la cuenta."""
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
    """Docstring completo. Bucle del menú principal."""
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
    """Docstring completo. Retorna la cuenta si el login es correcto, o None."""
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
    """Docstring completo."""
    print(f"\n--- Bienvenido/a, {cuenta['titular']} ---")
    print("1. Consultar saldo")
    print("2. Retirar dinero")
    print("0. Cerrar sesión")


def opcion_consultar_saldo(cuenta):
    """Docstring completo."""
    print(f"Saldo actual: {consultar_saldo(cuenta)}")


def opcion_retirar(cuenta, datos):
    """Docstring completo. Pide el monto, retira y guarda si salió bien."""
    monto = validar_monto(input("Monto a retirar: ").strip())
    if monto is None:
        print("Monto inválido.")
        return
    exito, mensaje = retirar(cuenta, datos["movimientos"], monto)
    print(mensaje)
    if exito:
        guardar_datos_json(RUTA_ARCHIVO_JSON, datos)
        registrar_log(RUTA_ARCHIVO_LOG, f"Retiro de {monto} en cuenta {cuenta['id_cuenta']}")


def menu_cuenta(cuenta, datos):
    """Docstring completo. Bucle del submenú de la cuenta."""
    while True:
        mostrar_menu_cuenta(cuenta)
        opcion = input("Elegí una opción: ").strip()
        if opcion == "1":
            opcion_consultar_saldo(cuenta)
        elif opcion == "2":
            opcion_retirar(cuenta, datos)
        elif opcion == "0":
            print("Sesión cerrada.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
