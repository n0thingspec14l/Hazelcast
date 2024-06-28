from flask import Flask, jsonify
import random
import requests
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

#цього тут немає:
###message_service_instances = ['http://localhost:5001', 'http://localhost:5002']

@app.route('/combined-messages', methods=['GET'])
def get_messages():
    selected_instance = get_service_address("messages-service")
    try:
        response = requests.get(selected_instance + '/messages')
        if response.status_code == 200:
            return jsonify({'messages': response.json()})
        else:
            return 'Failed to retrieve messages\n', 500
    except requests.exceptions.RequestException as e:
        return f'Error: {str(e)}\n', 500

if __name__ == '__main__':
    app.run(port=get_service_address("flask-get"))
