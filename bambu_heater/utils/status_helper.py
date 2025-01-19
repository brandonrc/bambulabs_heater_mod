
import ssl
from aiomqtt import Client
import json



async def grab_status(host, port, username, password, topic, callback):
    # Create an SSL context that doesn't verify certificates
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # Connect and subscribe to the topic
    async with Client(hostname=host, port=port, username=username, password=password, tls_context=ssl_context) as client:
        await client.subscribe(topic)
        async for message in client.messages:
            try:
                # Parse the JSON payload
                payload = message.payload.decode("utf-8")
                # Extract temperature
                data = json.loads(payload)
                await callback(data)
            except Exception as e:
                print(f"Error processing message: {e}")