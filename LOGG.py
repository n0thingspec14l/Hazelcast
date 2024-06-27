from flask import Flask, request, jsonify
import hazelcast

app = Flask(__name__)


client = hazelcast.HazelcastClient(
            cluster_name="dev")
messages_map = client.get_map("messages").blocking()

@app.route('/', methods=['POST'])
def log_message():
    data = request.json
    print(data)
    message_id = data.get("id")
    message_content = data.get("msg")
    if message_id or message_content != 0:
        messages_map.put(message_id, message_content)
        return jsonify({"status": "success"}), 200
    return(message_id ,message_content)


@app.route('/', methods=['GET'])
def get_messages():
    messages = messages_map.entry_set()
    messages_dict = {key: value for key, value in messages}
    return jsonify(messages_dict), 200


if __name__ == "__main__":
    app.run(port=5001)
