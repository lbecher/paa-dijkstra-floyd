import sys
import time
import os

repeticoes = 5

def dijkstra(matriz_adj, inicio, fim):
    n = len(matriz_adj)
    distancias = [sys.maxsize] * n
    distancias[inicio] = 0
    visitados = [False] * n
    for _ in range(n):
        u = -1
        for i in range(n):
            if not visitados[i] and (u == -1 or distancias[i] < distancias[u]):
                u = i
        if distancias[u] == sys.maxsize:
            break
        visitados[u] = True
        for v in range(n):
            if matriz_adj[u][v] > 0 and not visitados[v]:
                nova_distancia = distancias[u] + matriz_adj[u][v]
                if nova_distancia < distancias[v]:
                    distancias[v] = nova_distancia
    return distancias[fim]

with open("Saida/Dijkstra.csv", "w", encoding='utf-8') as saida:
    arquivos = [arq for arq in os.listdir('Entradas') if arq.endswith('.txt')]
    saida.write("Arquivo;MediaTempo;MenorDistancia;\n")
    for arquivo in arquivos:
        with open(f'Entradas/{arquivo}', 'r') as f:
            V = int(f.readline())
            matriz_adj = [[int(num) for num in line.split()] for line in f]
            # Substitui 0 por infinito, exceto na diagonal
            for x, row in enumerate(matriz_adj):
                for y, elem in enumerate(row):
                    if x != y and elem == 0:
                        matriz_adj[x][y] = sys.maxsize
            menor_dist = 0
            media_tempo = 0
            for _ in range(repeticoes):
                inicio = time.time()
                menor_dist = dijkstra(matriz_adj, 0, V-1)
                fim = time.time()
                media_tempo += fim - inicio
            media_tempo /= repeticoes
            media_tempo *= 1000  # Converte de segundos para milissegundos
            print(f"A menor distância do vértice 0 até o vértice {V-1} no dataset {arquivo} é: {menor_dist}")
            saida.write(f"{arquivo};{media_tempo};{menor_dist}\n")