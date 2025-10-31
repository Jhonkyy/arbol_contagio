from model.simulacion import Simulacion

import sys
sys.path.append("src")

if __name__ == "__main__":
    
    print("******************    Bienvenid@ a Resident evil Udem     ***********************")
    tamaño = int(input("digite el tamaño del tablero: "))
    n_personas = int(input("Digite personas habran en el tablero: "))
    sim = Simulacion(tamaño,n_personas)
    sim.mostrar_estado_inicial()
    sim.mostrar_tablero()

    ronda = 0
    while True:
        ronda += 1
        
        
        if sim.sanos_restantes() == False:
            print("Simulacion terminada, no hay sobrevivientes")
            break
        
        print(f"\n===== RONDA {ronda} =====")
        
        
        if ronda % 3 == 0:
            print("Todos los sanos reciben +3 de nivel de defensa\n")
            sim.curar_sanos()
        
        opcion = int(input("Seleccione una opcion:\n1. Siguiente ronda\n2.curar\n3. agregar personas\n4. Salir\n"))
        
        if opcion == 1:
            sim.simular_ronda()
        elif opcion == 2:
            x = int(input("posicion X de persona a sanar: "))
            y = int(input("posicion y de la persona a sanar: "))
            sim.curar(x,y)
        elif opcion == 3:
            x = int(input("posicion X de persona a agregar: "))
            y = int(input("posicion y de persona a agregar: "))
            sim.agregar_personas(x,y)
        elif opcion == 4:
            break
        print(sim.arbol)

