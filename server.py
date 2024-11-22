import asyncio #multiprocessser good for sockets
import websockets 
import wave 
import os #library for anything that has to do with your hard-drive
from french import stt

async def handle_connection(websocket):
    print(f"Client connected, {websocket.remote_address}")

    
    try:
        data= await websocket.recv()
        print(f"data: {data}") 
        fpath="received_audio.wav"
        with open(fpath, "wb") as audio_file: #received_audio is f.open, initialising this file. audio_file is the variable
                audio_file.write(data)
        da_words = stt(fpath) 
        print("Received audio file and saved as 'received_audio.wav'")
        await websocket.send(da_words) #waits until the sockets has sent everything and the pipe closes
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Client disconnected")

async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_connection, "localhost", 8765, ssl=None):  # Standarised way of building a websocket. ssl not done yet!! (certificate)
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__": #when you use a multi processer load, you use this so it doesnt crash. with asyncio you always have to do it
    asyncio.run(main())
