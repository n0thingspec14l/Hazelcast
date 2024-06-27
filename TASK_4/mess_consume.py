import pika  

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()
channel.queue_declare(queue='messages_queue')

messages = []

def callback(ch, method, properties, body):
    messages.append(body.decode())
    print(f"Received and stored message: {body.decode()}")

channel.basic_consume(queue='messages_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
