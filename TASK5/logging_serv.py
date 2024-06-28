from flask import Flask, request
import hazelcast
import consul

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def receive_message():
    message = request.json.get('message')
    if message:
        messages_map.put(request.remote_addr, message)
        app.logger.info(f"Received message: {message}")
        return 'Message received and logged\n'
    else:
        return 'No message provided\n', 

def register(consul_client, service_id, port):
    consul_client.agent.service.register(
        'logging_service',
        service_id=f"logging_service_{service_id}",
        address=f"logging_service_{service_id}",
        port=port)

def get_key_value(ccli, name):
    node = consul_client.kv.get("hz_cluster")[1]['Value'].decode().strip("',").split('\n')
    nodes = []
    for i in node:
        i = i.strip("',")
        nodes.append(i)
    return nodes

if __name__ == '__main__':
    consul_client = consul.Consul()
    client = hazelcast.HazelcastClient(cluster_members=get_key_value(consul_client, "hz_cluster"))
    messages_map = client.get_map("messages")
    app.run(host="0.0.0.0",
            debug=True)










