import socket
import time
import subprocess
import pathlib

from connection_handler import ConnectionHandler


def is_server_ready(host, port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.1)
    return False


def start_cpp_server(executable_path, host='localhost', port=12345):
    server_process = subprocess.Popen([executable_path])
    if is_server_ready(host, port):
        print("Server is ready.")
    else:
        print("Server failed to start within the timeout period.")
        server_process.terminate()
        raise RuntimeError("Server startup failed.")
    return server_process


if __name__ == "__main__":
    cpp_server_path = pathlib.Path(__file__).parent.parent.absolute() / "server" / "server"
    print(cpp_server_path)
    print(cpp_server_path.exists())
    server_process = start_cpp_server(cpp_server_path)

    handler = ConnectionHandler()
    handler.start_client()

    server_process.terminate()
