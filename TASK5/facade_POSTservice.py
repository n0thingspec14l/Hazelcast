from flask import Flask, request
import pika  

import consul

app = Flask(__name__)

def get_service_address(service_name):
    consul_client = consul.Consul(host='localhost', port=8500)
    services = consul_client.catalog.service(service_name)[1]
    if not services:
        raise Exception(f'Service {service_name} not found in Consul')
    service = services[0]
    address = service['ServiceAddress']
    port = service['ServicePort']
    return address, port

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
    app.run(port=get_service_address("flask-post"))
