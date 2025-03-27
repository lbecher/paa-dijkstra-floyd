#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <sys/time.h>

#define INF 99999

// Função auxiliar para encontrar o vértice com menor distância
int minDistance(int *dist, int *visited, int size) {
    int min = INF, min_index;
    for (int v = 0; v < size; v++) {
        if (!visited[v] && dist[v] <= min) {
            min = dist[v];
            min_index = v;
        }
    }
    return min_index;
}

// Algoritmo de Dijkstra para um vértice de origem
void dijkstra(int **graph, int src, int size, int *dist) {
    int visited[size];
    
    for (int i = 0; i < size; i++) {
        dist[i] = INF;
        visited[i] = 0;
    }
    
    dist[src] = 0;
    
    for (int count = 0; count < size - 1; count++) {
        int u = minDistance(dist, visited, size);
        visited[u] = 1;
        
        for (int v = 0; v < size; v++) {
            if (!visited[v] && graph[u][v] && dist[u] != INF && 
                dist[u] + graph[u][v] < dist[v]) {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Uso: %s <arquivo_de_entrada>\n", argv[0]);
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (!file) {
        perror("Erro ao abrir o arquivo");
        return 1;
    }

    int size;
    fscanf(file, "%d", &size);

    int **graph = (int **)malloc(size * sizeof(int *));
    for (int i = 0; i < size; i++) {
        graph[i] = (int *)malloc(size * sizeof(int));
        for (int j = 0; j < size; j++) {
            fscanf(file, "%d", &graph[i][j]);
            if (graph[i][j] == 0 && i != j) {
                graph[i][j] = INF;
            }
        }
    }
    fclose(file);

    // Matriz para armazenar todos os resultados do Dijkstra
    int **all_distances = (int **)malloc(size * sizeof(int *));
    for (int i = 0; i < size; i++) {
        all_distances[i] = (int *)malloc(size * sizeof(int));
    }

    // Medição de tempo
    struct timeval start, end;
    gettimeofday(&start, NULL);
    
    // Executa Dijkstra para cada vértice (V vezes)
    for (int src = 0; src < size; src++) {
        dijkstra(graph, src, size, all_distances[src]);
    }
    
    gettimeofday(&end, NULL);

    // Cálculo do tempo em microssegundos
    long seconds = end.tv_sec - start.tv_sec;
    long microseconds = end.tv_usec - start.tv_usec;
    double total_microseconds = seconds * 1e6 + microseconds;

    // Menor caminho de 0 até size-1 (equivalente ao Floyd-Warshall)
    int menor_caminho = all_distances[0][size - 1];

    printf("Tempo do Dijkstra (executado %d vezes): %.6f ms\n", size, total_microseconds);
    printf("Menor caminho de 0 -> %d: %d\n", size - 1, menor_caminho);

    // Liberação de memória
    for (int i = 0; i < size; i++) {
        free(graph[i]);
        free(all_distances[i]);
    }
    free(graph);
    free(all_distances);

    return 0;
}