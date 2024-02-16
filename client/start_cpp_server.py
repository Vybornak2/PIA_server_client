import socket
import time
import subprocess


def is_server_ready(host, port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print('Tesiting if server is ready:')
                return True
        except (ConnectionRefusedError, socket.timeout):
            print('Waiting for server to get ready.')
            time.sleep(0.1)
    return False


def start_cpp_server(executable_path, host='localhost', port=12345):
    print(30 * '=')
    print('Starting server...')
    server_process = subprocess.Popen([executable_path])
    if is_server_ready(host, port):
        print("Server is ready.")
    else:
        print("Server failed to start within the timeout period.")
        server_process.terminate()
        raise RuntimeError("Server startup failed.")
    return server_process


if __name__ == "__main__":
    start_cpp_server()
