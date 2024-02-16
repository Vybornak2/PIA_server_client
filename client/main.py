import pathlib
import time

from start_cpp_server import start_cpp_server
from connection_handler import run_client


def main():
    cpp_server_path = pathlib.Path(__file__).parent.parent.absolute() / "server" / "server"
    print(f'Does server path exist: {cpp_server_path.exists()}')
    server_process = start_cpp_server(cpp_server_path)

    time.sleep(1)
    print(30 * '=')

    run_client()

    server_process.terminate()

if __name__ == "__main__":
    main()
