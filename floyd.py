import sys
import time
import os

repeticoes = 5

def floyd_warshall(matriz_adj):
    n = len(matriz_adj)
    distancias = [[sys.maxsize] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                distancias[i][j] = 0
            elif matriz_adj[i][j] != 0:
                distancias[i][j] = matriz_adj[i][j]
            else:
                distancias[i][j] = sys.maxsize
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distancias[i][k] + distancias[k][j] < distancias[i][j]:
                    distancias[i][j] = distancias[i][k] + distancias[k][j]
    return distancias

with open("Saida/FloydWarshall.csv", "w", encoding='utf-8') as saida:
    arquivos = [arq for arq in os.listdir('Entradas') if arq.endswith('.txt')]
    saida.write("Arquivo;MediaTempo;MenorDistancia;\n")
    for arquivo in arquivos:
        with open(f'Entradas/{arquivo}', 'r') as f:
            V = int(f.readline())
            matriz_adj = [[int(num) for num in line.split()] for line in f]
            menor_dist = 0
            media_tempo = 0
            for _ in range(repeticoes):
                inicio = time.time()
                distancias = floyd_warshall(matriz_adj)
                menor_dist = distancias[0][V-1]
                fim = time.time()
                media_tempo += fim - inicio
            media_tempo /= repeticoes
            media_tempo *= 1000  # Converte de segundos para milissegundos
            print(f"A menor distância do vértice 0 até o vértice {V-1} no dataset {arquivo} é: {menor_dist}")
            saida.write(f"{arquivo};{media_tempo};{menor_dist}\n")