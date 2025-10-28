from persona import Persona

class Celda:
    def __init__(self,):
        self.posicion: tuple[int,int] = (0,0)
        self.ocupada: bool = False 
        self.ocupante: Persona | None = [] 
        self.estado: str = "vacia"

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