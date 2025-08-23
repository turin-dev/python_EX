"""Examples of building simple network servers."""

from __future__ import annotations

import socketserver
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading


class EchoHandler(socketserver.BaseRequestHandler):
    """Echo back whatever data is received."""
    def handle(self) -> None:
        data = self.request.recv(1024)
        print("Server received:", data)
        self.request.sendall(data)


def start_echo_server(host: str = "localhost", port: int = 9999) -> socketserver.TCPServer:
    server = socketserver.TCPServer((host, port), EchoHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Echo server running on {host}:{port}")
    return server


def start_http_server(host: str = "localhost", port: int = 8000) -> HTTPServer:
    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print(f"HTTP server running on {host}:{port}")
    return httpd


if __name__ == "__main__":
    # Start an echo server and an HTTP server for demonstration
    echo_server = start_echo_server()
    http_server = start_http_server()
    try:
        input("Servers are running. Press Enter to stop…\n")
    finally:
        echo_server.shutdown(); echo_server.server_close()
        http_server.shutdown(); http_server.server_close()