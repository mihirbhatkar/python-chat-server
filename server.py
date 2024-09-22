import asyncio
import json
from websockets.asyncio.server import serve

CLIENTS = set()
chat_history = []

async def broadcast(message, current_user="none"):
    for ws in CLIENTS:
        if ws != current_user or current_user=="none":
            await ws.send(message)

# async def periodic_broadcast():
#     while True:
#         print(CLIENTS)
#         await broadcast('Hiiii!')
#         await asyncio.sleep(5)

async def handler(ws):
    # message, name = await json.loads(ws)
    if ws not in CLIENTS:
        CLIENTS.add(ws)
        await broadcast("Someone has joined the chat!")
    
    try:
        async for data in ws:
            message, name =  json.loads(data)
            print(message, name)
            chat_history.append(f'{name}: {message}')
            await broadcast(chat_history[-1], ws)
    except:
        # CLIENTS.remove(ws)
        print("Some exception")

async def main():
    # asyncio.create_task(periodic_broadcast())
    async with serve(handler, "localhost", 8765):
        await asyncio.get_running_loop().create_future()

asyncio.run(main())