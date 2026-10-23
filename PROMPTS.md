# PROMPTS.md — Registro de uso de IA

**Proyecto:** Sistema de Cajero Automático
**Asignatura:** Programación I — IES 9-008 "Manuel Belgrano" — Comisión 1° Primera (Viernes)
**Herramienta utilizada:** Claude (Anthropic), chat web

**Criterio de registro:** se documentan solo las interacciones significativas (planificación, diseño de módulos, depuración y publicación del proyecto). Se omiten las consultas puntuales, como dudas de sintaxis o confirmaciones de resultados. Ninguna entrega se tomó sin probarla y compartirla con el equipo: el código sugerido se completó, se ejecutó y se corrigió antes de commitearlo.

**Total de interacciones registradas:** 9

---

## 1. Planificación del proyecto a partir de la consigna

- **Fecha:** 2026-10-01
- **Herramienta:** Claude
- **Prompt:** Adjunté la consigna del Proyecto Integrador, el modelo del Hito 1 y el modelo del Hito 2, y pedí trabajar un proyecto colaborativo de Python sobre un cajero automático, siguiendo el modelo y los hitos de esos documentos.
- **Resultado:** resumen de fechas, requisitos técnicos y reglas de la cátedra (módulos, mínimo de funciones, persistencia, tests, eje de investigación). Propuesta de diseño: entidades `cuentas` y `movimientos` como diccionarios, menú con funcionalidades y uso de `hashlib` como eje de investigación.
- **Modificaciones propias:** Se decidio el alcance del Hito 1: login con PIN, consultar saldo, retirar y persistencia en JSON.
- **Estado:** aceptado, con el alcance adaptado por mí.

## 2. Organización por módulos y hoja de ruta del Hito 1

- **Fecha:** 2026-10-01
- **Herramienta:** Claude
- **Prompt:** Pedí que me guiara en el Hito 1 con el plan elegido y consulté por dónde empezar a programar con los archivos ya creados.
- **Resultado:** estructura de carpetas y módulos (`main.py`, `estructuras.py`, `persistencia.py`, `utils.py` y un módulo extra `operaciones.py`), funciones mínimas por módulo en snake_case y un orden de trabajo de abajo hacia arriba para poder probar cada pieza.
- **Modificaciones propias:** creé el repositorio, los archivos y la carpeta `datos/`, y seguí el orden propuesto, probando cada módulo antes de pasar al siguiente.
- **Estado:** aceptado.

## 3. Constructores y búsqueda en `estructuras.py`

- **Fecha:** 2026-10-02
- **Herramienta:** Claude
- **Prompt:** Pedí más detalle sobre cómo armar para zanjear diferencias de diseño grupal e irpor una estructura mas neutral en `estructuras.py`.
- **Resultado:** explicación de funciones, diccionarios y `return`, un ejemplo resuelto en otro dominio, la función auxiliar `generar_siguiente_id()` y esqueletos para `crear_cuenta()`, `buscar_cuenta_por_dni()` y `crear_movimiento()`.
- **Modificaciones propias:** completé `crear_cuenta()`, `buscar_cuenta_por_dni()` y `crear_movimiento()`, escribí los docstrings, definí el límite diario por defecto y probé con un bloque de prueba (que estaba mal ubicado dentro de comillas y corregí). Probé los casos con IDs consecutivos y DNI inexistente.
- **Estado:** modificado y verificado. La función `generar_siguiente_id()` fue sugerida por la IA.

## 4. Hash del PIN y validaciones en `utils.py`

- **Fecha:** 2026-10-03
- **Herramienta:** Claude
- **Prompt:** Pedí avanzar con las funciones de utilidades y consulté cómo pasar el PIN a bytes y por qué fallaba mi código.
- **Resultado:** esqueletos de `hashear_pin()` (SHA-256 con `hashlib`), `validar_pin()`, `validar_monto()` y `obtener_fecha_hora_actual()`. Explicación del `encode`, y diagnóstico de que el fallo era por imports faltantes.
- **Modificaciones propias:** escribí las funciones, agregué los imports de `hashlib` y `math`, eliminé un bloque de prueba duplicado, agregué `validar_dni()` y verifiqué el hash de `"1234"` contra el valor de referencia.
- **Estado:** modificado y verificado.

## 5. Persistencia en JSON y log de operaciones

- **Fecha:** 2026-10-03
- **Herramienta:** Claude
- **Prompt:** Pedí avanzar con `persistencia.py` y consulté si debía crear el archivo JSON antes de programar.
- **Resultado:** decisión de usar un único JSON con las listas de cuentas y movimientos, esqueleto de `cargar_datos_json()`, `guardar_datos_json()` y `registrar_log()` con `with` y `try/except`, y una prueba de dos ejecuciones para comprobar que los datos sobreviven.
- **Modificaciones propias:** completé las funciones, ejecuté la prueba dos veces y comprobé los archivos generados. Corregí el log para usar el formato de fecha acordado y resolví un problema con `git add` creando el archivo `.gitignore`.
- **Estado:** modificado y verificado.

## 6. Retiro y límite diario en `operaciones.py` (depuración)

- **Fecha:** 2026-10-04
- **Herramienta:** Claude
- **Prompt:** Pedí avanzar con la lógica de retiro, y luego reporté el error de ejecución ("puede que haya omitido algún parámetro") y que no se estaba leyendo el límite diario.
- **Resultado:** esqueleto de `consultar_saldo()`, `calcular_total_retirado_hoy()`, `validar_limite_diario()` y `retirar()` (con retorno `(exito, mensaje)`). Explicación del alcance de las variables (`NameError`), corrección de las líneas con errores y localización del bug que dejaba el total diario en 0 (comparación contra el texto `"id_cuenta"` entre comillas).
- **Modificaciones propias:** corregí las líneas con errores, comparé las salidas contra lo esperado, detecté que el límite no se aplicaba, decidí bajar el límite por defecto a 50.000 y hacer que `validar_limite_diario()` lea el límite de cada cuenta. Probé con casos límite.
- **Estado:** modificado, depurado y verificado.

## 7. Integración en `main.py`: menús, alta, login y retiro

- **Fecha:** 2026-10-04
- **Herramienta:** Claude
- **Prompt:** Pedí avanzar con `main.py`, mostré los resultados de las pruebas del menú y del login y los analizamos juntos.
- **Resultado:** diseño del flujo (menú principal, alta de cuentas, login, submenú de cuenta), esqueletos de las funciones de `main.py` y decisiones de seguridad: mismo mensaje de error para DNI inexistente y PIN incorrecto, máximo de 3 intentos y registro de intentos en el log.
- **Modificaciones propias:** completé las funciones, probé el flujo completo (alta, login correcto y fallido, retiro, saldo insuficiente) y verifiqué que el saldo persiste al reiniciar el programa. Detecté que la validación del monto en el retiro había quedado sin probar.
- **Estado:** modificado y verificado.

## 8. Informe de avance del Hito 1

- **Fecha:** [2026-10-05]
- **Herramienta:** Claude
- **Prompt:** Pedí un modelo para  el informe del Hito 1 y que lo generara en Word, para poder editarlo y modificarlo a la necesidad del proyecto con los aportes grupales.
- **Resultado:** borrador con las cuatro secciones del modelo, a partir de lo construido (funcionalidades, persistencia, arquitectura por módulo), exportado a un archivo Word con los datos pendientes resaltados.
- **Modificaciones propias:** completé mis datos, el enlace al repositorio y el número de interacciones registradas, y revisé que los nombres de funciones coincidan con mi código.
- **Estado:** aceptado con ajustes.

## 9. Publicación del proyecto en GitHub

- **Fecha:** [2026-10-09]
- **Herramienta:** Claude
- **Prompt:** Consulté cómo compartir el cajero con mis compañeros dado que la version final se ejecuto y subio desde mi equipo, reporté los errores de permisos y de conexión con GitHub, y pedí el procedimiento para actualizar los commits antes de subir.
- **Resultado:** recomendación de usar un repositorio en GitHub, reglas de `.gitignore` y `.gitkeep` para no subir los datos de prueba, y diagnóstico del error de `remote origin` apuntando a un repositorio eliminado.
- **Modificaciones propias:** configuré el `.gitignore`, hice los commits de docstrings por módulo, corregí la dirección del remoto y subí el proyecto con `git push`.
- **Estado:** resuelto y verificado.

---

# Hito 2

## 10. Planificación del Hito 2

- **Fecha:** 2026-10-22
- **Herramienta:** Claude
- **Prompt:** Avanzamos con el Hito 2, a partir del modelo del Hito 2 y la consigna del proyecto.
- **Resultado:** comparación entre lo ya construido y los requisitos del hito (funcionalidades, filtro, ordenamiento, estadísticas, CSV, tests, README, informe y video), plan de trabajo por etapas con calendario hasta la entrega.
- **Modificaciones propias:** definí el orden de trabajo y el reparto del tiempo hasta la entrega.
- **Estado:** aceptado.

## 11. Depósito y transferencia en `operaciones.py`

- **Fecha:** 2026-10-23
- **Herramienta:** Claude
- **Prompt:** Avanzamos con `depositar()` y `transferir()`, y se consultó cómo probarlas.
- **Resultado:** Ejemplos de funciones y sugerencias de diseño: la transferencia valida todo antes de modificar los saldos, no aplica el límite diario (que es solo para retiros) y registra dos movimientos, `transferencia_enviada` y `transferencia_recibida`. Advertencia sobre agregar el primer movimiento a la lista antes de crear el segundo, para no repetir IDs.
- **Modificaciones propias:** completamos las funciones y se probaron los casos: depósito, transferencia correcta, saldo insuficiente y transferencia a la propia cuenta. Verifiqué los saldos y los movimientos generados.
- **Estado:** modificado y verificado.

## 12. Filtro y ordenamiento propio en `consultas.py`

- **Fecha:** 2026-10-23
- **Herramienta:** Claude
- **Prompt:** Avanzar con el historial de movimientos, con filtro y ordenamiento.
- **Resultado:** propuesta de un módulo nuevo con tres funciones (movimientos de una cuenta, filtro por tipo y ordenamiento por inserción), el esqueleto del algoritmo, y explicaciones sobre trabajar con una copia de la lista y sobre ordenar fechas como texto.
- **Modificaciones propias:** completamos las funciones, probamos con una lista de cuatro movimientos y comprobamos que el orden y los filtros eran los esperados y que la lista original no se alteraba.
- **Estado:** modificado y verificado.

## 13. Estadísticas y exportación a CSV

- **Fecha:** 2026-10-23
- **Herramienta:** Claude
- **Prompt:** continuemos con las estadísticas y luego con la exportación a CSV.
- **Resultado:** esqueletos de `contar_movimientos_por_tipo()`, `calcular_promedio_monto()` y `obtener_monto_minimo_y_maximo()` (que devuelve una tupla), contemplando la lista vacía, y de `exportar_movimientos_csv()` con `csv.DictWriter`, junto con la regla de `.gitignore` para no subir el CSV de prueba.
- **Modificaciones propias:** se completaron las funciones, escribimos los docstrings, probamos con datos de ejemplo y comprobamos el contenido del archivo CSV generado.
- **Estado:** modificado y verificado.

## 14. Integración al menú y depuración de las opciones 6 y 7

- **Fecha:** 2026-10-23
- **Herramienta:** Claude
- **Prompt:** Pedimos sugerencias conectar las nuevas funciones en `main.py`, y después reporté que las opciones 6 y 7 no funcionaban (el número se borraba y volvía al menú), adjuntando mi `main.py` y `estadisticas.py`.
- **Resultado:** esqueletos de las nuevas opciones del menú, los ayudantes `pedir_monto()` y `guardar_y_registrar()` para evitar código duplicado, y el submenú del historial. Para el problema, revisión de imports y `elif`, y pruebas de cada módulo por separado para aislar la falla.
- **Modificaciones propias:** completé e integré las opciones, juntamos las pruebas aisladas y volví a ejecutar. Se resolvio el problema de las opciones 6 y 7, rearmando los imports y se encontro que la falla estaba en un error de sintaxis(estaba mas escrito los imports). Verifiqué las siete opciones del menú.
- **Estado:** resuelto y verificado.

## 15. Pruebas unitarias en `test_cajero.py`

- **Fecha:** 2026-10-23
- **Herramienta:** Claude
- **Prompt:** Pedí armar las pruebas unitarias exigidas por la consigna y reporté el error al ejecutarlas.
- **Resultado:** sugerencia de las cinco pruebas con `unittest` (2 de dominio, 2 de persistencia y 1 de validación), uso de una carpeta temporal para no tocar los datos reales, y diagnóstico del `ModuleNotFoundError` (el archivo no estaba en la carpeta desde donde se ejecutaba).
- **Modificaciones propias:** Armamos la función, moví el archivo a la raíz del proyecto y ejecuté las pruebas: las cinco pasan.
- **Estado:** modificado y verificado.

## 16. Documentación: README y guion de defensa

- **Fecha:** 2026-10-23
- **Herramienta:** Claude
- **Prompt:** Pedí sugerencias para el README del proyecto
- **Resultado:** README con instrucciones de ejecución, estructura, persistencia, pruebas y limitaciones.
- **Modificaciones propias:** Ajuste de valores respecto al proyecto,asi como tambien las reglas de negocio del trabajo.
- **Estado:** pmodificado y verificado.
