#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

int main()
{
    int server_fd;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    // Creating socket file descriptor
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Forcefully attaching socket to the port 12345
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt)))
    {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(12345);

    // Bind
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0)
    {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen
    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    // Accept and process connections
    while (true)
    {
        char buffer[1024] = {0};
        std::cout << "Waiting for connections..." << std::endl;

        int new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen);
        if (new_socket < 0)
        {
            perror("accept");
            continue;
        }

        int valread = read(new_socket, buffer, 1024);
        if (valread > 0)
        {
            buffer[valread] = '\0'; // Null-terminate the string
            std::cout << "Client: " << buffer << std::endl;

            if (strcmp(buffer, "exit") == 0)
            {
                std::cout << "Shutdown command received. Exiting." << std::endl;
                break;
            }

            std::string response = std::to_string(strlen(buffer));
            for (int i = 0; i < 10; i++)
            {
                send(new_socket, response.c_str(), response.length(), 0);
                sleep(1);
            }
        }

        close(new_socket); // Close the connection
    }

    close(server_fd); // Cleanup
    return 0;
}
