// NetworkUtils.h
#ifndef NETWORK_UTILS_H
#define NETWORK_UTILS_H

#include <iostream>
#include <string>
#include <arpa/inet.h>
#include <unistd.h>

std::string receiveDataFunction(int socket)
{
    std::string data;
    char buffer;
    while (true)
    {
        ssize_t bytesRead = read(socket, &buffer, 1); // Read one byte at a time
        if (bytesRead <= 0)
        { // Check for end of stream or error
            // Handle error or disconnection
            break;
        }
        if (buffer == '\n')
        {          // Check for end-of-message symbol
            break; // Stop reading when end-of-message symbol is found
        }
        data += buffer; // Append the byte to the data string
    }
    return data;
}

void sendResponseFunction(int socket, const std::string &response)
{
    std::string message = response + "\n"; // Append end-of-message symbol

    ssize_t totalBytesSent = 0;
    while (totalBytesSent < message.size())
    {
        ssize_t bytesSent = send(socket, message.c_str() + totalBytesSent, message.size() - totalBytesSent, 0);
        if (bytesSent < 0)
        {
            std::cerr << "Failed to send data.\n";
            return;
        }
        totalBytesSent += bytesSent;
    }
}

#endif // NETWORK_UTILS_H
