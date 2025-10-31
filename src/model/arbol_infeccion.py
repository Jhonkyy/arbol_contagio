from model.persona import Persona

class NodoInfectado:
    def __init__(self, persona_id: int):
        self.id: int = persona_id
        self.hijos: list[NodoInfectado] = []
    
    def mostrar(self, prefix="", is_last=True) -> str:
        tree_str = prefix + ("'-- " if is_last else "|-- ") + f"Persona({self.id})\n"
        prefix += "    " if is_last else "|   "
        for i, hijo in enumerate(self.hijos):
            tree_str += hijo.mostrar(prefix, i == len(self.hijos) - 1)
        return tree_str

    def __repr__(self) -> str:
     
        return self.mostrar()

class ArbolInfectado:
    def __init__(self):
        self.root: NodoInfectado = None

    def registrar_contagio( self, infectador: Persona, infectado: Persona, current: NodoInfectado = None, flag: bool = True) -> bool:

        if flag:
            current = self.root
            flag = False

        if self.root is None:
            self.root = NodoInfectado(infectador.id)
            current = self.root
            current.hijos.append(NodoInfectado(infectado.id))
            return True

        if current.id == infectador.id:
            current.hijos.append(NodoInfectado(infectado.id))
            return True


        for hijo in current.hijos:
            inserted = self.registrar_contagio(infectador, infectado, hijo, flag)
            if inserted:
                return True

        return False
    
    def curar(self, id:int, current:NodoInfectado = None, flag: bool = True):
        if flag:
            current = self.root
            flag = False
            
        if current is None:
            return False
        
        if self.root.id == id:
            print("No se puede curar al paciente cero")
            return False
        
        if current.id == id:
            return True
        
        for hijo in current.hijos[:]:  
            if self.curar(id, hijo, flag):
                for nieto in hijo.hijos:
                    current.hijos.append(nieto)
                current.hijos.remove(hijo)
                return True  
        return False

    def remap_ids(self, mapping: dict) -> None:
        if self.root is None:
            return
        def _remap(node: NodoInfectado) -> None:
            node.id = mapping.get(node.id, node.id)
            for hijo in node.hijos:
                _remap(hijo)
        _remap(self.root)

    def __repr__(self):
        if self.root is None:
            return "<Empty Tree>"
        return repr(self.root)