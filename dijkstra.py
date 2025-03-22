import sys
import time
import os

repeticoes = 5

class Grafo():
    def __init__(self, vertices):
        self.num_vertices = vertices
        self.grafo = [[0 for coluna in range(vertices)] for linha in range(vertices)]

    def imprimir_solucao(self, distancias):
        print("Distânica:")
        for no in range(self.num_vertices):
            print(no, "\t", distancias[no])

    def distancia_minima(self, distancias, conjunto_spt):
        min_valor = sys.maxsize
        for v in range(self.num_vertices):
            if distancias[v] < min_valor and not conjunto_spt[v]:
                min_valor = distancias[v]
                indice_minimo = v
        return indice_minimo

    def dijkstra(self, origem):
        distancias = [sys.maxsize] * self.num_vertices
        distancias[origem] = 0
        conjunto_spt = [False] * self.num_vertices
        for _ in range(self.num_vertices):
            atual = self.distancia_minima(distancias, conjunto_spt)
            conjunto_spt[atual] = True
            for vertice in range(self.num_vertices):
                if self.grafo[atual][vertice] > 0 and not conjunto_spt[vertice] and distancias[vertice] > distancias[atual] + self.grafo[atual][vertice]:
                    distancias[vertice] = distancias[atual] + self.grafo[atual][vertice]

with open("Saida/Dijkstra.csv", "w", encoding='utf-8') as output:
    arquivos = [arq for arq in os.listdir("Entradas") if arq.endswith(".txt")]
    output.write("Arquivo;TempoMedio;\n")
    for arquivo in arquivos:
        with open(f'Entradas/{arquivo}', 'r') as f:
            num_vertices = int(f.readline())
            matriz = [[int(num) for num in line.split()] for line in f]
        grafo = Grafo(num_vertices)
        grafo.grafo = matriz
        tempo = 0
        for execucao in range(repeticoes):
            inicio = time.perf_counter()
            for vertice in range(num_vertices):
                grafo.dijkstra(vertice)
            fim = time.perf_counter()
            tempo += fim - inicio
        output.write(f"{arquivo};{tempo/repeticoes};\n")