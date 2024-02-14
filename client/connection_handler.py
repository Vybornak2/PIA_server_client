import socket

class ConnectionHandler:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
    
    

    def start_client(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.host, self.port))
            while True:
                text = input("Enter text (or 'exit' to close): ")
                client_socket.sendall(text.encode('utf-8'))
                if text == "exit":
                    break
                response = client_socket.recv(1024)
                print(f"Characters received from server: {response.decode('utf-8')}")

if __name__ == "__main__":
    handler = ConnectionHandler()
    handler.start_client()
