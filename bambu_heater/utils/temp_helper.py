
import ssl
from aiomqtt import Client




async def grab_temperature(host, port, username, password, topic):
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
                # print(f"Received: {payload}")

                # Extract temperature
                import json
                data = json.loads(payload)
                chamber_temp = data.get("print", {}).get("chamber_temper")
                if chamber_temp is not None:
                    print(f"Chamber Temperature: {chamber_temp}")
            except Exception as e:
                print(f"Error processing message: {e}")