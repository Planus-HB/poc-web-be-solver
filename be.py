import asyncio
import websockets
import pika
import time

# RabbitMQ credentials
credentials = pika.PlainCredentials('be_user', 'be_password')

# Function to establish RabbitMQ connection with retries
def connect_to_rabbitmq():
    while True:
        try:
            print("Trying to connect to RabbitMQ")
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
            print("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to RabbitMQ. Retrying in 1 second...")
            time.sleep(1)

# Define the WebSocket server logic
async def server(websocket, path):
    # Establish connection to RabbitMQ
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue='messages')

    try:
        # This function handles incoming messages and sends responses
        async for message in websocket:
            print(f"Received message on server: {message}")
            
            # Send the message to the RabbitMQ queue
            channel.basic_publish(exchange='', routing_key='messages', body=message)
            
            await websocket.send(f"Received: {message}")

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"WebSocket connection closed: {e}")

    finally:
        # Close the RabbitMQ connection
        connection.close()

# Start the WebSocket server
start_server = websockets.serve(server, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
