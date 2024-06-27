from flask import Flask, jsonify
import random
import requests

app = Flask(__name__)

message_service_instances = ['http://localhost:5001', 'http://localhost:5002']

@app.route('/combined-messages', methods=['GET'])
def get_messages():
    selected_instance = random.choice(message_service_instances)
    try:
        response = requests.get(selected_instance + '/messages')
        if response.status_code == 200:
            return jsonify({'messages': response.json()})
        else:
            return 'Failed to retrieve messages\n', 500
    except requests.exceptions.RequestException as e:
        return f'Error: {str(e)}\n', 500

if __name__ == '__main__':
    app.run(debug=True, port=5010)
