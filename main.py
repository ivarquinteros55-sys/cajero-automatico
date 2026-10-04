# main.py - Programa principal del cajero automático: menús y flujo general.

from estructuras import crear_cuenta, buscar_cuenta_por_dni
from persistencia import (cargar_datos_json, guardar_datos_json, registrar_log,
                          RUTA_ARCHIVO_JSON, RUTA_ARCHIVO_LOG)
from utils import hashear_pin, validar_pin, validar_dni, validar_monto

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
            print("Próximamente.")          
        elif opcion == "2":
            registrar_cuenta_nueva(datos)
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()