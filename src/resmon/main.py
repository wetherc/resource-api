import threading
import time
import copy
from kubernetes import client, config
from flask import Flask, request


NODES = {}
app = Flask(__name__)
config.load_kube_config()
v1 = client.CoreV1Api()


def update_node_list(k8s_client=v1):
    while True:
        nodes = k8s_client.list_node()
        node_dict = {}
        for node in nodes.items:
            node_dict[str(node.metadata.name)] = {
                'cpu': float(node.status.capacity['cpu']),
                'ram': int(node.status.capacity['memory'].strip('Ki'))
            }

        global NODES
        NODES = node_dict
        time.sleep(10)


t = threading.Thread(target=update_node_list, args=(v1,))
t.daemon = True
t.start()
t.setName('nodeUpdater')


@app.route('/v1/resources', methods=['GET'])
@app.route('/v1/resources/', methods=['GET'])
def check_node_resources():
    _cpu = request.args.get('cpu', 0., type=float)

    # URL parameter is in MB, value returned from K8s API is in KB
    _ram = request.args.get('ram', 0, type=int) * 1000

    node_status = copy.deepcopy(NODES)
    for node_name, node_val in node_status.items():
        if (node_val['cpu'] >= _cpu) and (node_val['ram'] >= _ram):
            node_status[node_name]['status'] = 'OK'
        else:
            node_status[node_name]['status'] = 'NOTOKAY'

    return node_status


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080)
