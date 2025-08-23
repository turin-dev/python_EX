# 40. Networking with the `socket` module

Python’s `socket` module is a thin wrapper around the BSD sockets API.  The
documentation notes that the module “provides access to the BSD socket
interface” and that the Python interface is a “straightforward transliteration”
of the underlying system calls【634526119538162†L67-L86】.  This means you can
create TCP and UDP clients and servers without leaving Python.

## Socket basics

* **Cross‑platform:** The module works on modern Unix systems, Windows and
  macOS.  The underlying behaviour may vary slightly by platform because it
  wraps the operating system APIs【634526119538162†L67-L86】.
* **Creating a socket:** Call `socket.socket(family, type)` to create a new
  socket object.  Common address families are `AF_INET` for IPv4 and
  `AF_INET6` for IPv6, and common types are `SOCK_STREAM` for TCP and
  `SOCK_DGRAM` for UDP.  The returned object exposes methods like `bind()`,
  `listen()`, `accept()`, `connect()`, `sendall()` and `recv()`.
* **Addresses:** For `AF_INET` sockets the address is a `(host, port)` pair where
  `host` is a hostname or IP and `port` is an integer【634526119538162†L121-L134】.

## Building a simple TCP server

The following example implements a minimal echo server.  It accepts one
connection, receives data and sends it back to the client.

```python
import socket

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Non‑privileged port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f'Listening on {HOST}:{PORT}')
    conn, addr = server.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
```

Clients connect with `socket.socket().connect((HOST, PORT))` and then call
`sendall()` and `recv()` on the socket.  Remember to close sockets with
`with` or `socket.close()` when you are finished to free system resources.

## UDP datagrams

For connectionless communication use `SOCK_DGRAM`.  UDP does not guarantee
delivery or order of packets.  The server binds to an address and uses
`recvfrom()` to receive data and the client sends datagrams with `sendto()`.

## Timeout and blocking behaviour

Sockets block by default.  You can set a timeout with
`socket.setdefaulttimeout(seconds)` or per‑socket with `settimeout()`.  When
timeouts expire a `socket.timeout` exception is raised.

## Summary

The `socket` module makes network programming in Python accessible because it
exposes the familiar BSD sockets API with Pythonic objects.  You can build
servers, clients and custom protocols using the same primitives used in C
programs【634526119538162†L67-L86】.
