"""Advanced asyncio examples: streams, synchronization and subprocesses."""

from __future__ import annotations

import asyncio


async def echo_server(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr = writer.get_extra_info("peername")
    print("Connection from", addr)
    while True:
        data = await reader.readline()
        if not data:
            break
        writer.write(data)
        await writer.drain()
    writer.close()
    await writer.wait_closed()


async def start_echo_server(host: str = "localhost", port: int = 9000) -> None:
    server = await asyncio.start_server(echo_server, host, port)
    addr = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Asyncio echo server running on {addr}")
    async with server:
        await server.serve_forever()


async def echo_client(host: str = "localhost", port: int = 9000) -> None:
    reader, writer = await asyncio.open_connection(host, port)
    message = "hello, async world!\n"
    writer.write(message.encode())
    await writer.drain()
    data = await reader.readline()
    print("Received from server:", data.decode().strip())
    writer.close()
    await writer.wait_closed()


async def main() -> None:
    server_task = asyncio.create_task(start_echo_server())
    # give server time to start
    await asyncio.sleep(0.1)
    await echo_client()
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass


if __name__ == "__main__":
    asyncio.run(main())