import asyncio
import websockets

async def send_audio():
    uri = "ws://127.0.0.1:8000/audio-stream/"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")

        # Read the audio file as binary
        with open("test_audio_hackathon.wav", "rb") as audio_file:
            audio_data = audio_file.read()

        # Send the audio data
        await websocket.send(audio_data)

        # Receive the response
        response = await websocket.recv()
        print("Received:", response)

asyncio.run(send_audio())
