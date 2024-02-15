import socket
import json
import random

from value_generator import generate_vector3

def generate_vector_pair():
    """Generates a pair of 3D vectors with random components."""
    return [generate_vector3(-10, 10) for _ in range(2)] 

def main(host='localhost', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        for _ in range(5):  # Send 5 pairs of vectors as an example
            vector_pair = generate_vector_pair()
            serialized_data = json.dumps(vector_pair).encode('utf-8')
            sock.sendall(serialized_data)
            
            # Wait for the response
            response = sock.recv(4096)  # Adjust buffer size as needed
            print("Response from server:", response.decode('utf-8'))
            
            # Example pause between sends
            import time
            time.sleep(1)

if __name__ == "__main__":
    main()
