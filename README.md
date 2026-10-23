# Cajero Automático

Proyecto Integrador — Programación I — IES 9-008 "Manuel Belgrano" — Comisión 1° Primera (Viernes)

## Integrantes

- [Quinteros Ivar]
- [Aguero Sol]
- [Montivero Mariana]

## Descripción

Cajero automático de consola desarrollado en Python con programación estructurada (sin clases). Permite crear cuentas, iniciar sesión con DNI y PIN, y operar sobre la cuenta: consultar saldo, retirar, depositar, transferir, ver el historial de movimientos, sacar estadísticas y exportar los datos a CSV.

## Requisitos

- Python 3.10 o superior.
- No usa librerías externas.

## Cómo ejecutarlo

```
git clone https://github.com/ivarquinteros55-sys/cajero-automatico.git
cd cajero-automatico
python3 main.py
```

## Funcionalidades

**Menú principal:** iniciar sesión, crear cuenta y salir.

**Menú de cuenta (después de iniciar sesión):**

1. Consultar saldo
2. Retirar dinero
3. Depositar dinero
4. Transferir dinero a otra cuenta (por DNI)
5. Historial de movimientos (submenú: ver todos, filtrar por tipo u ordenar por monto)
6. Estadísticas de la cuenta
7. Exportar el historial a CSV
0. Cerrar sesión

**Reglas del sistema:**

- DNI de 7 u 8 dígitos y PIN de 4 dígitos.
- Máximo de 3 intentos de PIN al iniciar sesión.
- Límite diario de retiro por cuenta (50.000 por defecto).
- Un retiro o una transferencia no pueden superar el saldo disponible.

## Estructura del proyecto

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Menús y flujo general. No contiene lógica de cálculo. |
| `estructuras.py` | Constructores de cuentas y movimientos, ID autoincremental y búsqueda por DNI. |
| `operaciones.py` | Reglas del cajero: consultar saldo, retirar, depositar y transferir. |
| `consultas.py` | Filtro de movimientos y ordenamiento por inserción. |
| `estadisticas.py` | Conteo por tipo, promedio, mínimo y máximo de montos. |
| `persistencia.py` | Lectura y escritura de JSON, exportación a CSV y log de texto. |
| `utils.py` | Validaciones, hash del PIN y formato de fecha y de movimientos. |
| `test_cajero.py` | Pruebas unitarias. |

## Persistencia

Los archivos se guardan en la carpeta `datos/`:

- `cajero.json`: cuentas y movimientos. Se carga al iniciar y se guarda después de cada alta y de cada operación.
- `historial_movimientos.csv`: se genera al exportar y se sobrescribe en cada exportación.
- `log_operaciones.txt`: registro con fecha y hora de altas, inicios de sesión (correctos y fallidos), operaciones y exportaciones.

Git ignora estos archivos de datos para no subir información de prueba.

## Eje de investigación (Opción E)

Seguridad del PIN con `hashlib`. El PIN nunca se guarda en texto plano: se almacena su hash SHA-256 y, al iniciar sesión, se hashea lo ingresado y se compara con el guardado. El login muestra el mismo mensaje si falla el DNI o el PIN, para no revelar qué DNI están registrados.

## Algoritmos

- **Filtro:** recorre los movimientos y devuelve los del tipo pedido.
- **Ordenamiento:** inserción, implementado en el proyecto y aplicado sobre una copia de la lista.
- **Estadísticas:** conteo por tipo de movimiento, promedio de montos y monto mínimo y máximo.

## Pruebas

```
python3 -m unittest -v test_cajero
```

Son 5 pruebas: 2 de lógica de dominio (retiro correcto y retiro con saldo insuficiente), 2 de persistencia (guardar y cargar JSON, y cargar un archivo inexistente) y 1 de validación (formato del PIN). Las pruebas de persistencia usan una carpeta temporal, así que no modifican los datos reales.

## Uso de IA

El uso de IA está documentado en `PROMPTS.md`, y el historial de commits muestra la evolución del proyecto.

## Limitaciones conocidas

- El conteo de 3 intentos se reinicia al volver a elegir "Iniciar sesión", por lo que no hay bloqueo real de la cuenta.
- El hash del PIN no usa "sal", y un PIN de 4 dígitos tiene solo 10.000 combinaciones posibles.
- La exportación a CSV reemplaza el archivo anterior.
