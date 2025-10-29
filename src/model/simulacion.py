import random
from persona import Persona
from tablero import Tablero
from arbol_infeccion import ArbolInfectado

class Simulacion:
    def __init__(self, tamano: int, num_personas: int, seed: int | None = None) -> None:
        if seed is not None:
            random.seed(seed)

        self.tamano: int = tamano
        self.num_personas: int = num_personas
        self.ronda: int = 0

        self.tablero: Tablero = Tablero(tamano)
        self.personas: list[Persona] = []
        self.arbol: ArbolInfectado = ArbolInfectado()

        print(f"Simulación creada con tablero {tamano}x{tamano} y {num_personas} personas.")
