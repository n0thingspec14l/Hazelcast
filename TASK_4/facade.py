import requests
from flask import Flask, jsonify, abort, request
import random

app = Flask(__name__)

logging_service_instances = ['http://localhost:5001', 'http://localhost:5002', 'http://localhost:5003']
messages_service_instances = ['http://localhost:5004', 'http://localhost:5005']

@app.route('/messages', methods=['POST'])
def post_message():
    message = request.json.get('message')
    if not message:
        abort(400, 'No message provided')

    for instance in logging_service_instances:
        try:
            requests.post(f"{instance}/messages", json={'message': message})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error posting to {instance}: {str(e)}")

    for instance in messages_service_instances:
        try:
            requests.post(f"{instance}/messages", json={'message': message})
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error posting to {instance}: {str(e)}")

    return 'Messages posted\n'

@app.route('/combined-messages', methods=['GET'])
def get_combined_messages():
    combined_messages = []
    for instance in logging_service_instances:
        try:
            response = requests.get(f"{instance}/messages")
            if response.status_code == 200:
                combined_messages.extend(response.json().get('messages', []))
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error getting from {instance}: {str(e)}")

    for instance in messages_service_instances:
        try:
            response = requests.get(f"{instance}/messages")
            if response.status_code == 200:
                combined_messages.extend(response.json().get('messages', []))
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Error getting from {instance}: {str(e)}")

    return jsonify({'combined_messages': combined_messages})

if __name__ == '__main__':
    app.run(debug=True)
