import random
from persona import Persona
from tablero import Tablero
from arbol_infeccion import ArbolInfectado
from arbol_infeccion import NodoInfectado

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
        
        
        paciente_cero = random.choice(self.personas)
        paciente_cero.estado = "infectado"

        celda_cero = self.tablero.matriz[paciente_cero.x][paciente_cero.y]
        celda_cero.estado = "infectado"

        self.arbol.root = NodoInfectado(paciente_cero.id)

        print(f"Paciente cero: Persona {paciente_cero.id} en posición ({paciente_cero.x}, {paciente_cero.y})")
        
    
    def mostrar_estado_inicial(self) -> None:
        print("\n=== ESTADO INICIAL DE LA SIMULACIÓN ===")
        for persona in self.personas:
            estado_icono = "🟥" if persona.estado == "infectado" else "🟩"
            print(f"{estado_icono} Persona {persona.id}: posición ({persona.x}, {persona.y}), defensa={persona.nivel_defensa}")
