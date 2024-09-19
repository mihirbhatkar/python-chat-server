from websockets.client import connect
import asyncio
import json

flag = False
name = "User"
async def chat():
    global flag
    global name
    if flag is False:
        name = input("Enter your name to start chatting: ")
    async with connect("ws://localhost:8765") as ws:

        if flag is False:
            await ws.send(json.dumps(["", name]))
            flag = True
        else:
            message = input(f'{name}: ')
            await ws.send(json.dumps([message, name]))

            latest_message = await ws.recv()
            print(latest_message)
        await chat()
        
asyncio.run(chat())