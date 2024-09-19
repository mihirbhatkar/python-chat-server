import asyncio
import json
from websockets.server import serve

CLIENTS = set()
chat_history = []

async def broadcast(message):
    for ws in CLIENTS:
        await ws.send(message)

async def server(ws):
    async for data in ws:
        message, name = json.loads(data)
        if ws not in CLIENTS: 
            CLIENTS.add(ws)
            await broadcast(f'{name} has entered the chat!')
        else:
            chat_history.append(f'{name}: {message}')
            await broadcast(chat_history[-1])

async def main():
    async with serve(server, "localhost", 8765):
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())