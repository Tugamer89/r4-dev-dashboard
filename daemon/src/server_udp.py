import asyncio
import json

# Keep track of connected Arduino clients (IP, Port)
connected_clients = set()
_transport = None


class UDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        # Only register clients that send the exact exact expected PING handshake
        if data.strip() == b"PING" and addr not in connected_clients:
            print(f"Registered new R4 client at {addr}")
            connected_clients.add(addr)


async def start_server(host: str = "0.0.0.0", port: int = 8765) -> None:
    """Initialize and start the UDP server."""
    global _transport
    loop = asyncio.get_running_loop()
    print(f"Starting UDP server on {host}:{port}")

    # Create the UDP endpoint listening for incoming pings
    transport, _ = await loop.create_datagram_endpoint(
        lambda: UDPProtocol(), local_addr=(host, port)
    )
    _transport = transport

    try:
        await asyncio.Future()  # Run forever
    finally:
        transport.close()


def broadcast_payload(payload: dict) -> None:
    """Send the telemetry payload to all registered Arduino clients."""
    if not connected_clients or not _transport:
        return

    message = json.dumps(payload).encode("utf-8")

    # Iterate over a copy of the set to safely remove disconnected clients if needed
    for addr in connected_clients:
        try:
            _transport.sendto(message, addr)
        except Exception as e:
            print(f"Failed to send to {addr}: {e}")
            connected_clients.remove(addr)
