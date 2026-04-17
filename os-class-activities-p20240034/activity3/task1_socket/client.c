#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8080
#define BUFFER_SIZE 1024

int main() {
    int sock_fd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE] = {0};
    const char *message = "Hello from client!";

    sock_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (sock_fd == -1) { perror("socket"); exit(EXIT_FAILURE); }
    printf("Client: socket created\n");

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect"); exit(EXIT_FAILURE);
    }
    printf("Client: connected to server\n");

    send(sock_fd, message, strlen(message), 0);
    printf("Client: sent message: '%s'\n", message);

    int bytes = recv(sock_fd, buffer, BUFFER_SIZE, 0);
    printf("Client: received response: '%s'\n", buffer);

    close(sock_fd);
    printf("Client: connection closed\n");
    return 0;
}
