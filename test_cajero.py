# test_cajero.py - Pruebas unitarias del cajero automático.

import os
import tempfile
import unittest

from estructuras import crear_cuenta
from operaciones import retirar,esta_bloqueada, bloquear_cuenta
from persistencia import guardar_datos_json, cargar_datos_json
from utils import validar_pin


class TestCajero(unittest.TestCase):

    # --- Lógica de dominio ---
    def test_retirar_descuenta_saldo(self):
        cuenta = crear_cuenta([], "Ana", "30123456", "x", 1000)
        movimientos = []
        exito, _ = retirar(cuenta, movimientos, 300)
        self.assertTrue(exito)
        self.assertEqual(cuenta["saldo"], 700)
        self.assertEqual(len(movimientos), 1)

    def test_retirar_rechaza_saldo_insuficiente(self):
        cuenta = crear_cuenta([], "Ana", "30123456", "x", 1000)
        movimientos = []
        exito, _ = retirar(cuenta, movimientos, 5000)
        self.assertFalse(exito)
        self.assertEqual(cuenta["saldo"], 1000)
        self.assertEqual(len(movimientos), 0)

    # --- Persistencia ---
    def test_guardar_y_cargar_json(self):
        datos = {"cuentas": [{"id_cuenta": 1, "titular": "Ana"}], "movimientos": []}
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "prueba.json")
            guardar_datos_json(ruta, datos)
            cargados = cargar_datos_json(ruta, {"cuentas": [], "movimientos": []})
        self.assertEqual(cargados, datos)

    def test_cargar_json_inexistente_devuelve_valor_por_defecto(self):
        por_defecto = {"cuentas": [], "movimientos": []}
        resultado = cargar_datos_json("ruta/que/no/existe.json", por_defecto)
        self.assertEqual(resultado, por_defecto)

    # --- Validación ---
    def test_validar_pin(self):
        self.assertTrue(validar_pin("1234"))
        self.assertFalse(validar_pin("123"))   
        self.assertFalse(validar_pin("123a"))   

   ## --- Bloqueo de cuenta ---
    def test_bloquear_cuenta(self):
        cuenta = crear_cuenta([], "Ana", "30123456", "x", 1000)
        self.assertFalse(esta_bloqueada(cuenta))
        bloquear_cuenta(cuenta)
        self.assertTrue(esta_bloqueada(cuenta))


if __name__ == "__main__":
    unittest.main()