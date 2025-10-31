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
    
    def simular_ronda(self):
        self.mover_personas()
        self.contagiar()
        self.mostrar_tablero()
        
    def mover_personas(self) -> None:
        direcciones = [
            (-1, 0),  # norte
            (1, 0),   # sur
            (0, -1),  # oeste
            (0, 1),   # este
            (-1, -1), # noroeste
            (-1, 1),  # noreste
            (1, -1),  # suroeste
            (1, 1)    # sureste
        ]

        for persona in self.personas:
            dx, dy = random.choice(direcciones)
            nuevo_x = persona.x + dx
            nuevo_y = persona.y + dy
           
            if not (0 <= nuevo_x < self.tamano and 0 <= nuevo_y < self.tamano):
                continue
           
            celda_actual = self.tablero.matriz[persona.x][persona.y]
            celda_actual.ocupada = False
            celda_actual.ocupante = None
            celda_actual.estado = "vacia"

            persona.x = nuevo_x
            persona.y = nuevo_y

            celda_nueva = self.tablero.matriz[nuevo_x][nuevo_y]
            celda_nueva.ocupada = True
            celda_nueva.ocupante = persona
            celda_nueva.estado = persona.estado

    def mostrar_tablero(self) -> None:
        print("\n=== TABLERO ===")
        for i in range(self.tamano):
            fila = ""
            for j in range(self.tamano):
                celda = self.tablero.matriz[i][j]
                if celda.ocupada and celda.ocupante is not None:
                    icono = "🟥" if celda.ocupante.estado == "infectado" else "🟩"
                    fila += f"{icono}{celda.ocupante.id:02d} "
                else:
                    fila += "⬜  "
            print(fila)

    def contagiar(self) -> None:
        for persona in self.personas:
            if persona.estado == "infectado":
      
                for otra in self.personas:
                    if otra.estado == "sano" and persona.x == otra.x and persona.y == otra.y:
                       
                        otra.estado = "infectado"
                        
                        self.tablero.matriz[otra.x][otra.y].estado = "infectado"
                     
                        self.arbol.registrar_contagio(persona, otra)
                        print(f"Persona {otra.id} ha sido infectada por Persona {persona.id}")
