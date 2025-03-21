import websockets
import asyncio

async def test_websocket():
    uri = "ws://127.0.0.1:8000/audio-stream/"
    async with websockets.connect(uri) as ws:
        print("Connected!")

asyncio.run(test_websocket())
