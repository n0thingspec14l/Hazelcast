from flask import Flask, request
import pika  

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='messages_queue')

@app.route('/messages', methods=['POST'])
def post_message():
    message = request.json.get('message')
    if message:
        channel.basic_publish(exchange='', routing_key='messages_queue', body=message)
        return 'Message sent to queue\n'
    else:
        return 'No message provided\n', 400

if __name__ == '__main__':
    app.run(debug=True, port=5015)
