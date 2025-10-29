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
        
        posiciones_ocupadas: set[tuple[int, int]] = set()
        for i in range(1, num_personas + 1):
            while True:
                x = random.randint(0, tamano - 1)
                y = random.randint(0, tamano - 1)
                if (x, y) not in posiciones_ocupadas:
                    posiciones_ocupadas.add((x, y))
                    break
            persona = Persona(i, x, y)
            self.personas.append(persona)
            celda = self.tablero.matriz[x][y]
            celda.ocupada = True
            celda.ocupante = persona
            celda.estado = "sano"

        print(f"{len(self.personas)} personas ubicadas aleatoriamente en el tablero.")