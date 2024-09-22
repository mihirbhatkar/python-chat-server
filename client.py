from websockets.asyncio.client import connect
import asyncio
import json
import sys

async def receive_message(ws, name):
    while True:
        latest_message = await ws.recv()
        sys.stdout.write('\r' + ' ' * (len(latest_message) + 50) + '\r')
        print(f"{latest_message}")
        
        sys.stdout.write(f'{name}: ')
        sys.stdout.flush()
        await asyncio.sleep(1)

async def send_message(name, ws):
    while True:
        # Use asyncio.to_thread to run the blocking input() in a separate thread
        msg = await asyncio.to_thread(input, f'{name}: ')
        await ws.send(json.dumps([msg, name]))

async def main():
    name = input("Enter your name to start chatting: ")
    async with connect("ws://localhost:8765") as ws:
        # Create and manage the receive and send tasks concurrently
        await asyncio.gather(
            receive_message(ws, name),
            send_message(name, ws)
        )

asyncio.run(main())
