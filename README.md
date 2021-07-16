# Kubernetes Resource Monitor

This is a simple K8s service to monitor the system RAM and CPU of each node in
a Kubernetes cluster and that exposes a RESTful API endpoint to easily check
which nodes, if any, meet specific resource requirements (e.g., "Are there
any nodes with at least 8GB RAM")

## Prerequisites

  - **Docker**. Please see the [Get Docker](https://docs.docker.com/get-docker/)
    page for installation instructions specific to your distribution. The Docker
    daemon must be running before executing the `bootstrap.sh` script. Checking
    the daemon's status and invoking it if dead is outside the scope of what
    I've built here.
  - **Minikube**. If developing locally, Minikube probably is a good idea. The
    bootstrap script provided in this repository's root assumes a Minikube
    binary is available in your PATH. I developed this with Minikube 1.22.0,
    but any reasonably modern release should also work OOTB.
  - **kubectl**. Please reference the [installation docs](https://kubernetes.io/docs/tasks/tools/#kubectl)
    for your distribution.
  - **skaffold**. Please reference the [installation docs](https://skaffold.dev/docs/install/)
    for your distribution

## Usage

Assuming all prerequisites are met, you should be able to just
```
./bootstrap.sh
```
to start the cluster. By default, we set the number of nodes to 3.

After the cluster is provisioned and all services are deployed onto it,
you can access the REST API at `localhost:8080/v1/resources/`. This endpoint
accepts 2 optional URL parameters, `cpu=<float>` and `ram=<int>`, where
`cpu` is the minimum number of CPU units (in threads) a node must have and
`ram` is the minimum amount of system RAM in megabytes.

For example, a GET request to `http://127.0.0.1:8080/v1/resources/?cpu=30&ram=4096`
yields (on my local machine - YMMV):
```
{
  "last_updated": "Fri, 16 Jul 2021 00:47:21 GMT",
  "nodes": {
    "resmon": {
      "cpu": 16,
      "ram": "32890948Ki",
      "status": "NOTOKAY"
    },
    "resmon-m02": {
      "cpu": 16,
      "ram": "32890948Ki",
      "status": "NOTOKAY"
    },
    "resmon-m03": {
      "cpu": 16,
      "ram": "32890948Ki",
      "status": "NOTOKAY"
    }
  }
}
```

`minikube delete --profile resmon` will deprovision this cluster and destroy all
associated resources.


## Caveats

Please note that GitHub is only hosting a mirror of this repository and is not
the authoritative source. Pull requests cannot be accepted.
