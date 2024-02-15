import socket
import struct
import threading
import json

import value_generator
import time
from itertools import count


class ConnectionHandler:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.running = True
        self.threads = [] 

        print(f"Connected to server at {self.host}:{self.port}")

    def serialize_data(self, data):
        return json.dumps(data).encode('utf-8')

    def send_data(self, vectors):
        if not self.running:  # Check if the connection has been closed
            print("Connection closed. Cannot send data.")
            return
        try:
            serialized_vectors = self.serialize_data(vectors)
            message = serialized_vectors + b"\n"
            self.socket.sendall(message)
        except BrokenPipeError as e:
            print("Send error: Broken pipe. Server has closed the connection.")
            self.running = False
        except Exception as e:
            print(f"Send error: {e}")
            self.running = False
    

    def send_end_signal(self):
        if not self.running:
            print("Connection already closed.")
            return
        try:
            end_signal = b"end\n"  # Assuming "end\n" is the agreed-upon signal
            self.socket.sendall(end_signal)
            print("End signal sent.")
        except Exception as e:
            print(f"Error sending end signal: {e}")
        finally:
            self.running = False  # Optionally stop further sends
            self.socket.close()  # Optionally close the socket immediately after sending end signal
            print("Connection closed.")


    def receive_data(self):
        try:
            while self.running:
                received_data = b""
                while True:
                    chunk = self.socket.recv(1024)  # Adjust buffer size as needed
                    if not chunk:
                        self.running = False  # Signal to shut down
                        break  # Connection closed or error
                    received_data += chunk
                    if b"\n" in chunk:
                        break  # End-of-message symbol found

                if not self.running:
                    break  # Exit the outer loop if no more data is received

                # Split by newline and process each message (there might be more than one message in the buffer)
                messages = received_data.split(b"\n")
                for msg in messages[:-1]:  # Exclude the last split since it might be empty due to the newline delimiter
                    print(f"Received: {msg.decode('utf-8')}")
        except Exception as e:
            print(f"Receive error: {e}")
            self.running = False


    def start_client(self):
        recv_thread = threading.Thread(target=self.receive_data, daemon=False)
        recv_thread.start()
        self.threads.append(recv_thread)  # Store the thread for later joining
    

    def join_threads(self):
        for thread in self.threads:
            thread.join()
        print("All threads joined.")


if __name__ == "__main__":
    iterations = 10
    vector_pairs = [[value_generator.generate_vector3(-10, 10) for _ in range(2)] for _ in range(iterations)]
    handler = ConnectionHandler()
    handler.start_client()  # Start listening for responses in a separate thread

    try:
        print("Sending data...")
        for i, vector_pair in enumerate(vector_pairs):
            handler.send_data(vector_pair)
            time.sleep(1)  # Example delay between sends
        handler.send_end_signal()
    finally:
        handler.join_threads()


