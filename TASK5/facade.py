import requests
from flask import Flask, jsonify, abort, request
import random
import consul
import hazelcast

app = Flask(__name__)

def any_logging_ins():
    return f"http://{discover_service('logging_service')}/"

def any_message_ins():
    return f"http://{discover_service('messages_service')}/"

@app.route('/messages', methods=['POST'])
def post_message():
    message = request.json.get('message')
    if not message:
        abort(400, 'No message provided')
    try:
        requests.post(f"{instance}/messages", json={'message': message})
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error posting to {instance}: {str(e)}")
    for instance in any_message_ins:
        try:
            requests.post(f"{instance}/messages", json={'message': message})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error posting to {instance}: {str(e)}")
    return 'Messages posted\n'

@app.route('/combined-messages', methods=['GET'])
def get_combined_messages():
    combined_messages = []
    for instance in any_logging_ins():
        try:
            response = requests.get(f"{instance}/messages")
            if response.status_code == 200:
                combined_messages.extend(response.json().get('messages', []))
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error getting from {instance}: {str(e)}")

    for instance in any_message_ins():
        try:
            response = requests.get(f"{instance}/messages")
            if response.status_code == 200:
                combined_messages.extend(response.json().get('messages', []))
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error getting from {instance}: {str(e)}")
    return jsonify({'combined_messages': combined_messages})

def register(consul_client, service_id, port):
    consul_client.agent.service.register(
        'logging_service',
        service_id=f"logging_service_{service_id}",
        address=f"logging_service_{service_id}",
        port=port)

def get_key_value(ccli, name):
    node = ccli.kv.get(name)[1]['Value'].decode().strip("',").split('\n')
    nodes = []
    for i in node:
        i = i.strip("',")
        nodes.append(i)
    return nodes

if __name__ == '__main__':
    consul_client = consul.Consul()
    client = hazelcast.HazelcastClient(cluster_members=get_key_value(consul_client, "hz_cluster"))
    messages_map = client.get_map("messages")
    print(consul_client)
    print(client)
    app.run(debug=True)
