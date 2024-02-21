import pika
import time

def connect_to_rabbitmq():
    # RabbitMQ credentials
    credentials = pika.PlainCredentials('solver_user', 'solver_password')

    while True:
        try:
            print("Trying to connect to RabbitMQ")
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', credentials=credentials))
            print("Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Failed to connect to RabbitMQ. Retrying in 1 second...")
            time.sleep(1)

def callback(ch, method, properties, body):
    print(f"Received message on consumer: {body}")

def consume_messages():
    connection = connect_to_rabbitmq()
    channel = connection.channel()

    # Declare a queue named 'messages'
    channel.queue_declare(queue='messages')

    # Start consuming messages from the queue
    channel.basic_consume(queue='messages', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    while True:
        try:
            consume_messages()
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print("Attempting to reconnect...")
