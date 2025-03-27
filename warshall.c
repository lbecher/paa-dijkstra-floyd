#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <sys/time.h> // Para gettimeofday()

#define INF 99999

void floydWarshall(int **dist, int size) {
    for (int k = 0; k < size; k++) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (dist[i][k] + dist[k][j] < dist[i][j]) {
                    dist[i][j] = dist[i][k] + dist[k][j];
                }
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

    int **dist = (int **)malloc(size * sizeof(int *));
    for (int i = 0; i < size; i++) {
        dist[i] = (int *)malloc(size * sizeof(int));
        for (int j = 0; j < size; j++) {
            dist[i][j] = graph[i][j];
        }
    }

    // Medição de tempo com gettimeofday()
    struct timeval start, end;
    gettimeofday(&start, NULL);
    floydWarshall(dist, size);
    gettimeofday(&end, NULL);

    long seconds = end.tv_sec - start.tv_sec;
    long microseconds = end.tv_usec - start.tv_usec;
    double total_microseconds = seconds * 1e6 + microseconds;

    int menor_caminho = dist[0][size - 1];

    printf("Tempo do Floyd-Warshall: %.6f ms\n", total_microseconds);
    printf("Menor caminho de 0 -> %d: %d\n", size - 1, menor_caminho);

    for (int i = 0; i < size; i++) {
        free(graph[i]);
        free(dist[i]);
    }
    free(graph);
    free(dist);

    return 0;
}