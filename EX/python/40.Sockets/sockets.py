"""
Examples of using the socket module for basic networking.

This script implements both a simple TCP echo server and a client.  Run
`python sockets.py server` in one terminal to start the server and
`python sockets.py client` in another terminal to send a message.  The
server echoes back whatever it receives.
"""

import socket
import sys


def run_server(host: str = "127.0.0.1", port: int = 65432) -> None:
    """Start a simple echo server that accepts a single connection."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"Listening on {host}:{port}…")
        conn, addr = server.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print("Received:", data)
                conn.sendall(data)


def run_client(host: str = "127.0.0.1", port: int = 65432) -> None:
    """Connect to the server and send a message entered by the user."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        message = input("Enter message: ").encode()
        client.sendall(message)
        data = client.recv(1024)
        print("Echo:", data.decode())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sockets.py [server|client]")
        sys.exit(1)
    if sys.argv[1] == "server":
        run_server()
    elif sys.argv[1] == "client":
        run_client()
    else:
        print("Unknown mode", sys.argv[1])