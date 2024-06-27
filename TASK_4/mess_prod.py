import logging
from flask import Flask, request

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def receive_message():
    message = request.json.get('message')
    if message:
        app.logger.info(f"Received message: {message}")
        return 'Message received and logged\n'
    else:
        return 'No message provided\n', 400

if __name__ == '__main__':
    app.run(debug=True, port=5005) 
