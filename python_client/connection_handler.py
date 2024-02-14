import socket

class ConnectionHandler:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Server listening on {self.host}:{self.port}...")
            conn, addr = server_socket.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode('utf-8')
                    print(f"Received message: {message}")
                    break  # For this simple example, close after receiving a message
                conn.sendall(b"ack")  # Send acknowledgment

if __name__ == "__main__":
    handler = ConnectionHandler()
    handler.start_server()
