# PIA - server - client communication

Package contains server (c++) which computes mean, amplitude vecotors for provided pair of vectors and than computes Mohr circle parameters of respective vecotors. These informations are then sent back to client.

Package also contains client for generation of random vector pairs that are being sent to server. Client also recives data from server and than displays it in terminal. 

Server utilizes port 12345

Entrypoint: **client.main.py** - starts server, starts client, sends data, receives data.

note: 

- make sure nothing else is listeing or running on selected port.
- lsof -i :12345 to check on linux

## Compatibily:
- linux

    *windows compatibility is unknown*

---
## Contents:

### 1. Server - C++

- server.cpp

    Contains main() function.

    Estabilishes connection and waits for client input. Input data are than transformed and sent back to cliend.
    
    Server also contains some basic error handling.

- NetworkUtils.h

    Functions to handle comunication, reading, sending data.

- VectorProcessing.h

    Functions to do required mathematical operations vectors.

### 2. Client - python

- main.py

    Serves as an entry point of whole package
    Starts server, client, sends some data.

- start_cpp_server.py 

    Handles start of the server. Tests connection.

- connection_handeler.py

    Contain class that handles connection to server, data sending and receiving.

- value_generator.py

    Basic function for generation of random vectors

