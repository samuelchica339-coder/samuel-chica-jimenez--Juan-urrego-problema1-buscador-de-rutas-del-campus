import heapq
import json
import os

class GrafoDijkstra:
    def __init__(self, archivo="grafo.json"):
        self.archivo = archivo
        self.grafo = {}
        self.cargar_desde_archivo()
    
    # ============================================================
    # 1. Cargar ubicaciones y conexiones desde archivo
    # ============================================================
    def cargar_desde_archivo(self):
        """Carga el grafo desde un archivo JSON"""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r') as f:
                    datos = json.load(f)
                    # Convertir las claves a enteros
                    self.grafo = {int(k): [(int(v), p) for v, p in val] 
                                  for k, val in datos.items()}
                print(f"✅ Grafo cargado desde {self.archivo}")
            except:
                print("⚠️ Error al cargar, usando grafo de 27 nodos")
                self.grafo_real()
        else:
            print("📁 No se encontró archivo, usando grafo de 27 nodos")
            self.grafo_real()
    
    def grafo_real(self):
        """Crea el grafo real con 27 nodos (tus datos)"""
        self.grafo = {
            1: [(4, 3), (21, 3), (25, 8), (27, 3)],
            2: [(4, 3), (7, 1), (27, 2)],
            3: [(4, 1), (5, 0.5), (12, 2)],
            4: [(1, 3), (2, 3), (3, 1), (19, 1)],
            5: [(3, 0.5), (6, 0.5), (10, 0.5)],
            6: [(5, 0.5), (7, 2), (8, 1)],
            7: [(2, 1), (6, 2), (8, 1)],
            8: [(6, 1), (7, 1), (9, 2)],
            9: [(8, 2), (10, 0.5), (11, 2)],
            10: [(5, 0.5), (9, 0.5), (12, 1)],
            11: [(9, 2), (12, 0.5), (14, 2)],
            12: [(3, 2), (10, 1), (11, 0.5), (14, 0.5), (19, 5)],
            13: [(15, 2), (16, 1.5)],
            14: [(11, 2), (12, 0.5), (15, 0.3)],
            15: [(13, 2), (14, 0.3), (16, 0.2)],
            16: [(13, 1.5), (15, 0.2)],
            17: [(18, 0.1), (20, 1.5)],
            18: [(17, 0.1), (19, 0.2)],
            19: [(4, 1), (12, 5), (18, 0.2)],
            20: [(17, 1.5), (22, 3)],
            21: [(1, 3), (22, 1)],
            22: [(20, 3), (21, 1)],
            23: [(24, 2), (25, 3)],
            24: [(23, 2), (25, 1.5)],
            25: [(1, 8), (23, 3), (24, 1.5), (26, 2)],
            26: [(25, 2)],
            27: [(1, 3), (2, 2)]
        }
    
    def guardar_en_archivo(self):
        """Guarda el grafo en un archivo JSON"""
        # Convertir a JSON serializable
        datos_serializables = {str(k): [(str(v), p) for v, p in val] 
                               for k, val in self.grafo.items()}
        with open(self.archivo, 'w') as f:
            json.dump(datos_serializables, f, indent=2)
        print(f"💾 Grafo guardado en {self.archivo}")
    
    # ============================================================
    # 2. Agregar y eliminar una ubicación (nodo)
    # ============================================================
    def agregar_ubicacion(self, nodo):
        """Agrega un nuevo nodo al grafo"""
        if nodo in self.grafo:
            print(f"❌ La ubicación {nodo} ya existe")
            return False
        
        self.grafo[nodo] = []
        self.guardar_en_archivo()
        print(f"✅ Ubicación {nodo} agregada correctamente")
        return True
    
    def eliminar_ubicacion(self, nodo):
        """Elimina un nodo y todas sus conexiones"""
        if nodo not in self.grafo:
            print(f"❌ La ubicación {nodo} no existe")
            return False
        
        # Eliminar el nodo de las listas de adyacencia de otros nodos
        for n in list(self.grafo.keys()):
            self.grafo[n] = [(v, p) for v, p in self.grafo[n] if v != nodo]
        
        # Eliminar el nodo
        del self.grafo[nodo]
        self.guardar_en_archivo()
        print(f"✅ Ubicación {nodo} eliminada correctamente")
        return True
    
    # ============================================================
    # 3. Agregar y eliminar una ruta entre dos ubicaciones
    # ============================================================
    def agregar_ruta(self, origen, destino, peso):
        """Agrega una ruta bidireccional entre dos nodos"""
        if origen not in self.grafo:
            print(f"❌ La ubicación {origen} no existe")
            return False
        if destino not in self.grafo:
            print(f"❌ La ubicación {destino} no existe")
            return False
        if peso <= 0:
            print(f"❌ El peso debe ser positivo")
            return False
        
        # Verificar si ya existe la ruta
        for v, p in self.grafo[origen]:
            if v == destino:
                print(f"⚠️ La ruta ya existe con peso {p}")
                return False
        
        # Agregar ruta en ambos sentidos (grafo no dirigido)
        self.grafo[origen].append((destino, peso))
        self.grafo[destino].append((origen, peso))
        self.guardar_en_archivo()
        print(f"✅ Ruta {origen} ↔ {destino} agregada con peso {peso}")
        return True
    
    def eliminar_ruta(self, origen, destino):
        """Elimina una ruta entre dos nodos"""
        if origen not in self.grafo or destino not in self.grafo:
            print(f"❌ Una o ambas ubicaciones no existen")
            return False
        
        # Contar antes/después
        len_antes_origen = len(self.grafo[origen])
        
        # Eliminar ruta en ambos sentidos
        self.grafo[origen] = [(v, p) for v, p in self.grafo[origen] if v != destino]
        self.grafo[destino] = [(v, p) for v, p in self.grafo[destino] if v != origen]
        
        if len(self.grafo[origen]) < len_antes_origen:
            self.guardar_en_archivo()
            print(f"✅ Ruta {origen} ↔ {destino} eliminada correctamente")
            return True
        else:
            print(f"❌ La ruta {origen} ↔ {destino} no existe")
            return False
    
    # ============================================================
    # 4. Calcular ruta más corta (Dijkstra)
    # ============================================================
    def ruta_mas_corta(self, inicio, fin):
        """Calcula la ruta más corta usando Dijkstra"""
        if inicio not in self.grafo or fin not in self.grafo:
            return None, None, "❌ Una o ambas ubicaciones no existen"
        
        # Dijkstra
        dist = {n: float('inf') for n in self.grafo}
        dist[inicio] = 0
        padre = {inicio: None}
        pq = [(0, inicio)]
        
        while pq:
            d_act, act = heapq.heappop(pq)
            if d_act > dist[act]:
                continue
            if act == fin:
                break
            
            for vec, p in self.grafo[act]:
                nd = d_act + p
                if nd < dist[vec]:
                    dist[vec] = nd
                    padre[vec] = act
                    heapq.heappush(pq, (nd, vec))
        
        if dist[fin] == float('inf'):
            return None, None, "❌ No existe ruta entre las ubicaciones"
        
        # Reconstruir ruta
        ruta = []
        act = fin
        while act is not None:
            ruta.append(act)
            act = padre.get(act)
        
        return ruta[::-1], dist[fin], "✅ Ruta encontrada"
    
    # ============================================================
    # 5. Mostrar matriz de adyacencia
    # ============================================================
    def mostrar_matriz_adyacencia(self):
        """Muestra la matriz de adyacencia completa"""
        nodos = sorted(self.grafo.keys())
        n = len(nodos)
        idx = {nodo: i for i, nodo in enumerate(nodos)}
        
        # Crear matriz
        matriz = [[0] * n for _ in range(n)]
        for i, nodo in enumerate(nodos):
            for vecino, peso in self.grafo[nodo]:
                j = idx[vecino]
                matriz[i][j] = peso
        
        # Mostrar matriz
        print("\n" + "="*80)
        print("📊 MATRIZ DE ADYACENCIA")
        print("="*80)
        
        # Encabezado
        print("     ", end="")
        for nodo in nodos:
            print(f"{nodo:4}", end="")
        print("\n" + "     " + "-" * (4 * n))
        
        # Filas
        for i, nodo in enumerate(nodos):
            print(f"{nodo:3} | ", end="")
            for j in range(n):
                if matriz[i][j] != 0:
                    print(f"{matriz[i][j]:4.1f}", end="")
                else:
                    print(f"   .", end="")
            print()
        print("="*80)
    
    def mostrar_lista_adyacencia(self):
        """Muestra la lista de adyacencia"""
        print("\n" + "="*60)
        print("📋 LISTA DE ADYACENCIA")
        print("="*60)
        for nodo in sorted(self.grafo.keys()):
            if self.grafo[nodo]:
                vecinos = ", ".join([f"{v}({p})" for v, p in sorted(self.grafo[nodo])])
                print(f"  {nodo:2} → [{vecinos}]")
            else:
                print(f"  {nodo:2} → []")
    
    def guardar_como_json(self):
        """Guarda el grafo actual como archivo JSON"""
        self.guardar_en_archivo()


# ============================================================
# MENÚ PRINCIPAL INTERACTIVO
# ============================================================
def menu():
    print("\n" + "="*60)
    print("🚀 SISTEMA DE RUTAS - DIJKSTRA")
    print("="*60)
    print("   Cargando grafo con 27 nodos...")
    
    grafo = GrafoDijkstra()
    
    while True:
        print("\n" + "="*60)
        print("🎯 MENÚ PRINCIPAL")
        print("="*60)
        print("  1. 📋 Mostrar lista de adyacencia")
        print("  2. 📊 Mostrar matriz de adyacencia")
        print("  3. ➕ Agregar ubicación")
        print("  4. ➖ Eliminar ubicación")
        print("  5. 🛣️  Agregar ruta entre ubicaciones")
        print("  6. 🚫 Eliminar ruta entre ubicaciones")
        print("  7. 🧭 Calcular ruta más corta (Dijkstra)")
        print("  8. 💾 Guardar grafo en JSON")
        print("  0. 🚪 Salir")
        print("="*60)
        
        opcion = input("➡️  Elige una opción: ").strip()
        
        if opcion == "1":
            grafo.mostrar_lista_adyacencia()
        
        elif opcion == "2":
            grafo.mostrar_matriz_adyacencia()
        
        elif opcion == "3":
            try:
                nodo = int(input("   📍 ID de la nueva ubicación: "))
                grafo.agregar_ubicacion(nodo)
            except ValueError:
                print("   ❌ Ingresa un número válido")
        
        elif opcion == "4":
            try:
                nodo = int(input("   📍 ID de la ubicación a eliminar: "))
                grafo.eliminar_ubicacion(nodo)
            except ValueError:
                print("   ❌ Ingresa un número válido")
        
        elif opcion == "5":
            try:
                origen = int(input("   📍 Ubicación origen: "))
                destino = int(input("   📍 Ubicación destino: "))
                peso = float(input("   ⚖️  Peso (tiempo/distancia): "))
                grafo.agregar_ruta(origen, destino, peso)
            except ValueError:
                print("   ❌ Ingresa valores válidos")
        
        elif opcion == "6":
            try:
                origen = int(input("   📍 Ubicación origen: "))
                destino = int(input("   📍 Ubicación destino: "))
                grafo.eliminar_ruta(origen, destino)
            except ValueError:
                print("   ❌ Ingresa números válidos")
        
        elif opcion == "7":
            try:
                print("\n" + "-"*40)
                print("🔍 CÁLCULO DE RUTA MÁS CORTA")
                print("-"*40)
                inicio = int(input("   🚀 Ubicación de inicio: "))
                destino = int(input("   🎯 Ubicación de destino: "))
                ruta, distancia, mensaje = grafo.ruta_mas_corta(inicio, destino)
                
                print(f"\n{mensaje}")
                if ruta:
                    print(f"   🗺️  Ruta: {' → '.join(map(str, ruta))}")
                    print(f"   📏 Distancia total: {distancia}")
            except ValueError:
                print("   ❌ Ingresa números válidos")
        
        elif opcion == "8":
            grafo.guardar_como_json()
        
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("   ❌ Opción no válida. Elige 0-8.")


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    menu()