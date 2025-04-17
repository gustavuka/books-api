import asyncio
from typing import AsyncGenerator, List

from fastapi import HTTPException


class EventManager:
    def __init__(self):
        self.connections: List[asyncio.Queue] = []

    async def subscribe(self) -> AsyncGenerator[str, None]:
        queue = asyncio.Queue()
        self.connections.append(queue)
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n"
        finally:
            self.connections.remove(queue)

    async def broadcast(self, message: str):
        for connection in self.connections:
            await connection.put(message)


# Global event manager instance
event_manager = EventManager()
