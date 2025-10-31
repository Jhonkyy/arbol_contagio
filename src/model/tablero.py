from model.persona import Persona

class Celda:
    def __init__(self,):
        self.posicion: tuple[int,int] = (0,0)
        self.ocupada: bool = False 
        self.ocupantes: list = []
        self.estado: str = "vacia"

    def agregar_ocupante(self, persona):
        if persona not in self.ocupantes:
            self.ocupantes.append(persona)
        self.ocupada = bool(self.ocupantes)

    def remover_ocupante(self, persona):
        if persona in self.ocupantes:
            self.ocupantes.remove(persona)
        self.ocupada = bool(self.ocupantes)
        if not self.ocupantes:
            self.estado = "vacia"

class Tablero:
    def __init__(self, tamano: int):
        self.tamano = tamano
        self.matriz: list[list[Celda]] = []
        
        for i in range(tamano):
            fila = []
            for j in range(tamano):
                celda = Celda()
                celda.posicion = (i, j)
                fila.append(celda)
            self.matriz.append(fila)