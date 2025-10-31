import random
from model.persona import Persona
from model.tablero import Tablero
from model.arbol_infeccion import ArbolInfectado
from model.arbol_infeccion import NodoInfectado

class Simulacion:
    def __init__(self, tamano: int, num_personas: int) -> None:


        self.tamano: int = tamano
        self.num_personas: int = num_personas
        self.ronda: int = 0
        self.toroidal: bool = True

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
            celda.agregar_ocupante(persona)
            celda.estado = "sano"

        print(f"{len(self.personas)} personas ubicadas aleatoriamente en el tablero.")
        
        
        self.paciente_cero = random.choice(self.personas)
        self.paciente_cero.estado = "infectado"

        celda_cero = self.tablero.matriz[self.paciente_cero.x][self.paciente_cero.y]
        celda_cero.estado = "infectado"

        self.arbol.root = NodoInfectado(self.paciente_cero.id)

    
        self.num_personas = len(self.personas)

        print(f"Paciente cero: Persona {self.paciente_cero.id} en posición ({self.paciente_cero.x}, {self.paciente_cero.y})")
        
    
    def mostrar_estado_inicial(self) -> None:
        print("\n=== ESTADO INICIAL DE LA SIMULACIÓN ===")
        for persona in self.personas:
            estado_icono = "R" if persona.estado == "infectado" else "V"
            print(f"{estado_icono} Persona {persona.id}: posición ({persona.x}, {persona.y}), defensa={persona.nivel_defensa}")
    
    def simular_ronda(self):
        
        self.mover_personas()
        self.contagiar()
        self.mostrar_tablero()
        self.mostrar_sanos()
        
        for persona in self.personas:
            print(f"posicion persona{persona.id} = {persona.x}{persona.y}")
        
    def mover_personas(self) -> None:
        direcciones = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

      
        propuestas: list[tuple[int,int]] = []
        for persona in self.personas:
            dx, dy = random.choice(direcciones)
            nx = persona.x + dx
            ny = persona.y + dy
            
            nx = nx % self.tamano
            ny = ny % self.tamano
            propuestas.append((nx, ny))

     
        nueva_matriz: list[list[list[Persona]]] = [[[] for _ in range(self.tamano)] for _ in range(self.tamano)]
        for persona, (nx, ny) in zip(self.personas, propuestas):
            persona.x = nx
            persona.y = ny
            nueva_matriz[nx][ny].append(persona)

       
        for i in range(self.tamano):
            for j in range(self.tamano):
                celda = self.tablero.matriz[i][j]
                celda.ocupantes = []
                celda.ocupada = False
                celda.estado = "vacia"

        for i in range(self.tamano):
            for j in range(self.tamano):
                ocupantes = nueva_matriz[i][j]
                if ocupantes:
                    celda = self.tablero.matriz[i][j]
                    for p in ocupantes:
                        if p not in celda.ocupantes:
                            celda.ocupantes.append(p)
                    celda.ocupada = True
                    celda.estado = "infectado" if any(p.estado == "infectado" for p in ocupantes) else "sano"

        self.validar_integridad()

    def mostrar_sanos(self):
        personas_sanas = []
        for persona in self.personas:
            if persona.estado == "sano":
                personas_sanas.append((persona,persona.nivel_defensa))
        print(personas_sanas) 
    
    def sanos_restantes(self) -> bool:
        return any(persona.estado == "sano" for persona in self.personas)
    
    def mostrar_tablero(self) -> None:
        print("\n=== TABLERO ===")
        for i in range(self.tamano):
            fila = ""
            for j in range(self.tamano):
                celda = self.tablero.matriz[i][j]
                if celda.ocupantes:
                    ocupantes_str = [repr(p) for p in celda.ocupantes]  
                    fila += "[" + ",".join(ocupantes_str) + "] "
                else:
                    fila += "[  ] "
            print(fila)

    def contagiar(self) -> None:
      
        for i in range(self.tamano):
            for j in range(self.tamano):
                celda = self.tablero.matriz[i][j]
           
                if len(celda.ocupantes) < 2:
                    continue
                
                
                infectados = [p for p in celda.ocupantes if p.estado == "infectado"]
                if not infectados:
                    continue

                
                for persona in celda.ocupantes:
                    if persona.estado == "sano":
                     
                        persona.nivel_defensa -= len(infectados)
                        if persona.nivel_defensa <= 0:
                            persona.estado = "infectado"
                            celda.estado = "infectado"
                          
                            infector = random.choice(infectados)
                            self.arbol.registrar_contagio(infector, persona)
                            print(f"Persona {persona.id} ha sido infectada por Persona {infector.id}")

    def curar(self, x, y):
        celda = self.tablero.matriz[x][y]
        infectados = [persona for persona in celda.ocupantes if persona.estado == "infectado"]
        if not infectados:
            print("No hay infectados en esta celda.")
            return
        persona_curar = None
        if len(infectados) > 1:
            print("Hay más de un infectado en la zona. ¿A quién querés sanar?")
            for persona in infectados:
                print(f"Persona {persona.id} - posición ({persona.x}, {persona.y})")
            try:
                id_curar = int(input("Ingrese el ID de la persona que desea curar: "))
            except ValueError:
                print("ID inválido.")
                return
            for persona in infectados:
                if persona.id == id_curar:
                    persona_curar = persona
            if persona_curar is None:
                print("No se encontró una persona infectada con ese ID en esta celda.")
                return
        else:
            persona_curar = infectados[0]

        result = self.arbol.curar(persona_curar.id)
        if not result:
            return
        persona_curar.estado = "sano"
        persona_curar.nivel_defensa = 3
        print(f"La Persona {persona_curar.id} ha sido curada exitosamente.")
        self.validar_integridad()

    def agregar_personas(self, x, y):
        if not (0 <= x < self.tamano and 0 <= y < self.tamano):
            print("Posición fuera del tablero")
            return

        nueva_id = max((p.id for p in self.personas), default=0) + 1
        persona_nueva = Persona(nueva_id, x, y)
        persona_nueva.estado = "sano"

        self.personas.append(persona_nueva)
      
        celda = self.tablero.matriz[x][y]
        if persona_nueva not in celda.ocupantes:
            celda.ocupantes.append(persona_nueva)
        celda.ocupada = True
        if any(p.estado == "infectado" for p in celda.ocupantes):
            celda.estado = "infectado"
        else:
            celda.estado = "sano"
        self.num_personas = len(self.personas)
        self.validar_integridad()

    def curar_sanos(self):
        for persona in self.personas:
            if persona.id == self.paciente_cero.id:
                pass
            elif persona.estado == "sano":
                persona.nivel_defensa+=1

    def validar_integridad(self) -> None:
       
        for i in range(self.tamano):
            for j in range(self.tamano):
                c = self.tablero.matriz[i][j]
                c.ocupantes = []
                c.ocupada = False
                c.estado = "vacia"

       
        for persona in self.personas:
            persona.x = persona.x % self.tamano
            persona.y = persona.y % self.tamano

      
        for persona in self.personas:
            celda = self.tablero.matriz[persona.x][persona.y]
            if all(p is not persona for p in celda.ocupantes):
                celda.ocupantes.append(persona)
            celda.ocupada = True
            if persona.estado == "infectado":
                celda.estado = "infectado"
            elif celda.estado != "infectado":
                celda.estado = "sano"

       
        present_ids = {p.id for row in self.tablero.matriz for c in row for p in c.ocupantes}
        for persona in self.personas:
            if persona.id not in present_ids:
                persona.x %= self.tamano
                persona.y %= self.tamano
                celda = self.tablero.matriz[persona.x][persona.y]
                if all(p is not persona for p in celda.ocupantes):
                    celda.ocupantes.append(persona)
                    celda.ocupada = True
                    if persona.estado == "infectado":
                        celda.estado = "infectado"
                    elif celda.estado != "infectado":
                        celda.estado = "sano"