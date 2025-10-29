from dataclasses import dataclass

@dataclass
class Persona:
    
    def __init__(self, id: int, x: int = 0, y: int = 0) -> None:
        self.id: int = id
        self.x: int = x
        self.y: int = y
        self.nivel_defensa: int = 3
        self.estado: str = "sano"