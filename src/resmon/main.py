import threading
import time
import copy
import re
import logging
from datetime import datetime, timezone
from kubernetes import client, config
from flask import Flask, request


NODES = {}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)

try:
    config.load_incluster_config()
except config.config_exception.ConfigException:
    logger.warning(
        'Failed to load incluster config. Loading from ~/.kube/config.'
    )
    config.load_kube_config()
v1 = client.CoreV1Api()


def update_node_list(k8s_client: client.CoreV1Api=v1) -> None:
    while True:
        nodes = k8s_client.list_node()
        node_dict = {
            'last_updated': datetime.now(tz=timezone.utc),
            'nodes': {}
        }
        for node in nodes.items:
            node_dict['nodes'][str(node.metadata.name)] = {
                'cpu': float(node.status.capacity['cpu']),
                'ram': node.status.capacity['memory']
            }

        global NODES
        NODES = node_dict
        time.sleep(10)


def _convert_stupid_si_units(value: str) -> int:
    _si_map = {
        'Ki': 2**10,
        'Mi': 2**20,
        'Gi': 2**30,
        'Ti': 2**40,
        'Pi': 2**50
    }

    match = re.match(r'([0-9]+)([a-zA-Z]+)', value)
    if match:
        assert len(match.groups()) == 2, f'Something weird is up with {value}'
    else:
        raise ValueError(
            'Are you running this on an internet-connected toaster? '
            'Is all your memory swap? What\'s going on here?')

    items = match.groups()
    size_in_bytes = int(items[0]) * _si_map.get(items[1], -1)

    if size_in_bytes < 0:
        raise ValueError(
            'Hmm... it looks like you\'ve got an exabyte or more of RAM. '
            'Are you really sure about that? Seems like some tomfoolery '
            'to me...'
        )
    return int(size_in_bytes * 10**-6)


# it's probably worth a TODO that I'll never follow up on to note
# that I'm basically just yeeting this thread into the void and
# never really circling back to check on whether or not, ya know,
# it still is alive? So like maybe let's not use this on any
# production systems or anything, but if nothing else there's
# always the last-updated timestamp in the response body which
# should give an indication of things being silently broken
# if it's more than ~10 seconds apart from current time.
t = threading.Thread(target=update_node_list, args=(v1,))
t.daemon = True
t.start()
t.setName('nodeUpdater')


@app.route('/v1/resources', methods=['GET'])
@app.route('/v1/resources/', methods=['GET'])
def check_node_resources():
    cpu = request.args.get('cpu', 0., type=float)
    ram = request.args.get('ram', 0, type=int)

    node_status = copy.deepcopy(NODES)
    for node_name, node_val in node_status['nodes'].items():
        # URL parameter is in MB, value returned from K8s API is not
        # https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/resources.md#resource-quantities
        _ram = _convert_stupid_si_units(node_val['ram'])
        if (node_val['cpu'] >= cpu) and (_ram >= ram):
            node_status['nodes'][node_name]['status'] = 'OK'
        else:
            node_status['nodes'][node_name]['status'] = 'NOTOKAY'

    return node_status


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080)
