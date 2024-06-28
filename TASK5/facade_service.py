import requests
from flask import Flask, jsonify, abort, request
import random
import consul
app = Flask(__name__)

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

logging_service_instances = ["http://",f"{get_service_address("logging-service")[0]}",":",f"{get_service_address("logging-service")[1]}"]
messages_service_instances = ["http://",f"{get_service_address("messages-service")[0]}",":",f"{get_service_address("messages-service")[1]}"]

@app.route('/messages', methods=['POST'])
def post_message():
    message = request.json.get('message')
    if not message:
        abort(400, 'No message provided')

    for instance in logging_service_instances:
        try:
            requests.post(f"{get_service_address("logging-service")[0]}:{get_service_address("logging-service")[1]}/messages", json={'message': message})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error posting to {instance}: {str(e)}")

    for instance in messages_service_instances:
        try:
            requests.post(f"{get_service_address("messages-service")[0]}:{get_service_address("messages-service")[1]}", json={'message': message})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error posting to {instance}: {str(e)}")

    return 'Messages posted\n'

@app.route('/combined-messages', methods=['GET'])
def get_combined_messages():
    combined_messages = []
    for instance in logging_service_instances:
        try:
            response = requests.get(f"{get_service_address("logging-service")[0]}:{get_service_address("logging-service")[1]}/messages")
            if response.status_code == 200:
                combined_messages.extend(response.json().get('messages', []))
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error getting from {instance}: {str(e)}")

    for instance in messages_service_instances:
        try:
            response = requests.get(f"{get_service_address("messages-service")[0]}:{get_service_address("messages-service")[1]}/messages")
            if response.status_code == 200:
                combined_messages.extend(response.json().get('messages', []))
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error getting from {instance}: {str(e)}")

    return jsonify({'combined_messages': combined_messages})

if __name__ == '__main__':
    app.run(debug=True)
