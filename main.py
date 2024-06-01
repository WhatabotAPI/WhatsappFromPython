import asyncio
import websockets
import json
import ssl

class WhatabotRealtimeClient:
    def __init__(self):
        self.api_key = "YOUR_API_KEY"
        self.chat_id = "YOUR_PHONE_NUMBER"
        self.url = "wss://api.whatabot.io/realtimeMessages"
        self.connect_message = json.dumps({"protocol": "json", "version": 1}) + '\u001e'

    async def run_websocket(self):
        while True:
            try:
                async with websockets.connect(
                        self.url,
                        extra_headers={
                            "x-api-key": self.api_key,
                            "x-chat-id": self.chat_id,
                            "x-platform": "whatsapp"
                        },
                        ssl=ssl.create_default_context()
                ) as ws:
                    await ws.send(self.connect_message)
                    print("Connected")

                    async for message in ws:
                        await self.receive_message(ws, message)
            except Exception as ex:
                print("ERROR:", ex)

            print("Attempting to reconnect...")
            await asyncio.sleep(20)

    async def receive_message(self, ws, message):
        try:
            message = message.rstrip('\u001e')
            json_message = json.loads(message)
            arguments_array = json_message.get("arguments")
            message_target = json_message.get("target")

            if message_target == "ReceiveMessage" and arguments_array:
                text_inside_arguments = arguments_array[0]
                if text_inside_arguments:
                
                    upper_text = text_inside_arguments.upper()
                    
                    #Here you can create your functions
                    if upper_text == "START":
                        print("Starting the process...")
                    elif upper_text == "STOP":
                        print("Stopping the process...")
                    elif upper_text == "PAUSE":
                        print("Pausing the process...")                        
                    elif upper_text == "RESUME":
                        print("Resuming the process...")
                    else:
                        print("Unknown command")
                        
                    response_message = json.dumps({"type": 1, "target": "SendMessage", "arguments": [f"Pong: {text_inside_arguments}"]}) + '\u001e'
                    await ws.send(response_message)
                    print("Message sent:", f"Pong: {text_inside_arguments}")

        except json.JSONDecodeError:
            print("Error parsing the message")
        except Exception as ex:
            print("Error:", ex)

async def main():
    client = WhatabotRealtimeClient()
    await client.run_websocket()

if __name__ == "__main__":
    asyncio.run(main())