import os
import threading
import time
import json
from kubernetes import client, config
from flask import Flask


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
                'cpu': node.status.capacity['cpu'],
                'ram': int(node.status.capacity['memory'].strip('Ki'))
            }

        global NODES
        NODES = node_dict
        time.sleep(10)


t = threading.Thread(target=update_node_list, args=(v1,))
t.daemon = True
t.start()
t.setName('nodeUpdater')


@app.route("/")
def hello_world():
    return NODES


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080)
