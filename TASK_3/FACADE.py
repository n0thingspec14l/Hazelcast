from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

LOGGING_SERVICE_URL = [
    "http://192.168.1.7:5701/", 
    "http://192.168.1.7:5702/"
    "http://192.168.1.7:5703/"]

LOG_URL = "http://127.0.0.1:5001"
MESSAGES_SERVICE_URL = "http://127.0.0.1:5002"

@app.route('/', methods=['POST'])
def post_message():
    msg = request.json.get('msg')
    if not msg:
        return jsonify({'error': 'Message content is required'}), 400
    unique_id = str(uuid.uuid4())
    data = {'id': unique_id, 'msg': msg}

    
    response = requests.post(LOG_URL, json=data)
    print("response from logg ", response)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to log message'}), response.status_code
    return jsonify({'id': unique_id}), response.status_code

@app.route('/', methods=['GET'])
def get_messages():
    log_response = requests.get(LOG_URL)

    if log_response.status_code != 200:
        return jsonify({'error': 'Failed to get logs'}), log_response.status_code 
    
    logs = log_response.json()
    msg_response = requests.get(MESSAGES_SERVICE_URL)
    if msg_response.status_code != 200:
        return jsonify({'error': 'Failed to get static message'}), msg_response.status_code

    static_msg = msg_response.text
    full_response = {"logs": logs, "static_message": static_msg}
    print(msg_response)
    return msg_response, 200

if __name__ == "__main__":
    app.run(port=5000)
