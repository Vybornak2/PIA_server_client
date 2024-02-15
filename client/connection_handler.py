import socket
import threading

class ConnectionHandler:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True


    def send_data(self):
        try:
            while self.running:
                text = input("Enter text (or 'exit' to close): ")
                if text == "exit":
                    self.running = False
                self.socket.sendall(text.encode('utf-8'))
        except Exception as e:
            print(f"Send error: {e}")
            self.running = False


    def receive_data(self):
        try:
            while self.running:
                response = self.socket.recv(1024)
                if not response:
                    break  # Server closed connection
                print(f"Characters received from server: {response.decode('utf-8')}")
        except Exception as e:
            print(f"Receive error: {e}")
        finally:
            self.running = False


    def start_client(self):
        threading.Thread(target=self.send_data, daemon=True).start()
        threading.Thread(target=self.receive_data, daemon=True).start()

        while self.running:
            pass  # Keep the main thread running while send/receive threads are active

        self.socket.close()
        print("Connection closed.")


if __name__ == "__main__":
    handler = ConnectionHandler()
    handler.start_client()
