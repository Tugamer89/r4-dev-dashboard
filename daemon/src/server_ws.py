"""Asynchronous WebSocket server for Arduino communication."""

import asyncio
import json

import websockets

# Keep track of connected Arduino clients
connected_clients = set()


async def ws_handler(websocket):
    """Handle individual WebSocket client connections."""
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Handle incoming messages from the Arduino if needed
            print(f"Received from R4: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)


async def start_server(host: str = "0.0.0.0", port: int = 8765) -> None:
    """Initialize and start the WebSocket server."""
    print(f"Starting WebSocket server on ws://{host}:{port}")
    async with websockets.serve(ws_handler, host, port):
        await asyncio.Future()  # Run forever


def broadcast_payload(payload: dict) -> None:
    """Broadcast the telemetry payload to all connected clients."""
    if not connected_clients:
        return
    message = json.dumps(payload)
    websockets.broadcast(connected_clients, message)
