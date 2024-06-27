import logging
from flask import Flask, request
import hazelcast

app = Flask(__name__)

client = hazelcast.HazelcastClient(c)

client = hazelcast.HazelcastClient(servers=[
    'localhost:5701',  # Assuming Hazelcast instance 1
    'localhost:5702',  # Assuming Hazelcast instance 2
    'localhost:5703'   # Assuming Hazelcast instance 3
])

messages_map = client.get_map("messages")

@app.route('/messages', methods=['POST'])
def receive_message():
    message = request.json.get('message')
    if message:
        messages_map.put(request.remote_addr, message)
        app.logger.info(f"Received message: {message}")
        return 'Message received and logged\n'
    else:
        return 'No message provided\n', 

if __name__ == '__main__':
    app.run(debug=True, port=5001) 
