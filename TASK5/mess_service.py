import flask
import threading
import consul
import sys
import hazelcast


connection = pika.BlockingConnection(pika.ConnectionParameters(host_kv))
channel = connection.channel()
channel.queue_declare(queue='messages_queue')
msg = []
msg_lock = threading.Lock()

consul_client = consul.Consul()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/health', methods=['GET'])
def health():
    return app.response_class(status=200)

@app.route('/messages-service', methods=['GET'])
def message():
    global msg
    if len(msg) == 0:
        return "Insufficient messages count"
    with msg_lock:
        wiped_msg = msg.copy()
        msg.clear()    
    return ','.join(wiped_msg)

def get_key_value(c, name):
    return c.kv.get(name)[1]['Value'].decode()[1:-1]

def register(service_id, port):
    c = consul.Consul()
    c.agent.service.register(
        'messages_service',
        service_id=f"messages_service_{service_id}",
        address=f"messages_service_{service_id}",
        port=port)
#        check=check_http)

if __name__ == '__main__':
    service_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1 
    register(service_id, port)
    app.run(host="0.0.0.0",
            debug=False)
