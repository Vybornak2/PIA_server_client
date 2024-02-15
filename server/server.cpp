#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>
#include <thread>
#include "NetworkUtils.h"
#include "VectorProcessing.h"

void handleClient(int clientSocket)
{
    try
    {
        bool keepRunning = true;
        while (keepRunning)
        {
            std::string receivedData = receiveDataFunction(clientSocket);
            if (receivedData.empty() || receivedData == "end")
            { // Example "end" signal check
                keepRunning = false;
                break;
            }

            auto vectors = nlohmann::json::parse(receivedData);

            std::pair<std::vector<float>, std::vector<float>> vectorPair = extractVectors(vectors);
            std::pair<std::vector<float>, std::vector<float>> ampMean = getAmpMean(vectorPair);
            std::vector<float> MohrParamsAmp = getMohrParams(ampMean.first);
            std::vector<float> MohrParamsMean = getMohrParams(ampMean.second);

            const std::vector<std::vector<float>> computedValues = {MohrParamsAmp, MohrParamsMean};
            std::string response = nlohmann::json(computedValues).dump();
            sendResponseFunction(clientSocket, response);
        }
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error handling client: " << e.what() << std::endl;
    }
    std::cout << "Closing connection\n";
    close(clientSocket);
}

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

    std::cout << "Server is running on port 12345\n";

    // Accept and process connections
    while (true)
    {
        std::cout << "Waiting for a connection...\n";
        int client_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t *)&addrlen);
        if (client_socket < 0)
        {
            std::cout << "Failed to accept connection\n";
            perror("accept");
            continue;
        }
        std::cout << "Client connected\n";

        // Spawn a new thread to handle the client connection
        std::thread clientThread(handleClient, client_socket);
        clientThread.detach(); // Detach the thread to allow it to run independently
    }

    close(server_fd); // Cleanup
    return 0;
}
