# Resident Evil UDEM — Simulación de propagación de infección

Descripción del proyecto
- Simulación en consola de propagación de una infección entre personas que se mueven en una matriz NxN.
- Cada persona tiene nivel de defensa; al compartir celda con infectados pierde defensa y se infecta si llega a 0.
- Se mantiene un árbol de contagios que registra quién contagió a quién y permite curaciones con reparenting.

Cómo ejecutar la simulación
1. Requisitos: Python 3.10+ instalado.
2. Abrir terminal en la carpeta del proyecto.
3. Ejecutar:
   - python src/main.py
4. Opcional: fijar semilla para reproducibilidad editando `src/main.py` antes de crear la simulación:
   - import random
   - random.seed(12345)
5. En la ejecución se solicitará tamaño del tablero y número de personas; luego elegir opciones por ronda (siguiente ronda, curar, agregar persona, salir).

Estructura de clases
- Persona
  - id, x, y, nivel_defensa, estado ("sano"|"infectado"), representación coloreada.
- Celda
  - posicion, lista de ocupantes, ocupada (bool), estado de celda ("vacia"|"sano"|"infectado").
- Tablero
  - matriz NxN de Celdas y métodos para gestionar ocupantes.
- ArbolInfectado
  - estructura de árbol que registra propagación; soporta registrar contagios, curar con reparenting y remapear IDs.
- Simulacion
  - lógica principal: inicialización reproducible, movimiento (toroide), reglas de contagio, curación, agregar personas, visualización en consola y validación de integridad.

Supuestos asumidos
- Movimiento: modo toroide (envolvimiento al cruzar bordes).
- Defensa inicial por defecto: 3 (ajustable en código si se desea).
- Regla de contagio: por celda, cada persona sana pierde 1 punto de defensa por cada infectado presente; al llegar a 0 se infecta inmediatamente.
- Curación: `curar(x,y)` cura a una persona infectada en la celda; si el nodo está en el árbol se realiza reparenting de sus hijos. No se puede curar al paciente cero (raíz).
- Agregar personas: se permite añadir nuevas personas sanas en coordenadas válidas; reciben ID único.
- Incremento de defensa: cada 3 rondas, las personas sanas incrementan su defensa en 1 (implementación incluida en simulación).
- Visualización: salida en consola con IDs (p1, p2, ...) y colores ANSI para estado.
- Reproducibilidad: usar `random.seed` en `main.py` para repetir experimentos.

Notas
- El proyecto prioriza separación entre lógica de simulación, estructuras de datos y visualización en consola.
- Para pruebas reproducibles, fijar semilla y ejecutar las mismas entradas.
