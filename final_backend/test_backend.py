import asyncio
import websockets
import json

async def send_audio():
    # Replace with your backend WebSocket URL
    uri = "ws://localhost:8000/audio-stream/"

    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server")

        # Load the .wav file
        with open("test_audio.wav", "rb") as audio_file:
            audio_data = audio_file.read()

        # Send the audio data to the backend
        await websocket.send(audio_data)
        print("Audio data sent to backend")

        # Receive the response from the backend
        response = await websocket.recv()
        response_data = json.loads(response)
        print("Received response from backend:", response_data)

# Run the test
async def main():
    await send_audio()

# Explicitly create and run the event loop
if __name__ == "__main__":
    asyncio.run(main())