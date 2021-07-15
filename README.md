# Kubernetes Resource Monitor

This is a simple K8s service to monitor the system RAM and CPU of each node in
a Kubernetes cluster and that exposes a RESTful API endpoint to easily check
which nodes, if any, meet specific resource requirements (e.g., "Are there
any nodes with at least 8GB RAM")

## Prerequisites

  - **Docker**. Please see the [Get Docker](https://docs.docker.com/get-docker/)
    page for installation instructions specific to your distribution. The Docker
    daemon must be running before executing the `bootstrap.sh` script. Checking
    the daemon's status and invoking it if dead is outside the scope of what I've
    built here.
  - **Minikube**. If developing locally, Minikube probably is a good idea. The
    bootstrap script provided in this repository's root assumes a Minikube
    binary is available in your PATH. I developed this with Minikube 1.22.0,
    but any reasonably modern release should also work OOTB.
  - **kubectl**. Please reference the [installation docs](https://kubernetes.io/docs/tasks/tools/#kubectl)
    for your distribution.

## Usage

Assuming all prerequisites are met, you should be able to just
```
./bootstrap.sh
```
to start the cluster. You can optionally also supply an `-n <INT>` parameter
to specify the number of nodes you'd like to provision. By default, we set
the number of nodes to 4.

After the cluster is provisioned and all services are deployed onto it,
you can access the REST API at `localhost:8080/v1/resources/`. This endpoint
accepts 2 optional URL parameters, `cpu=<float>` and `ram=<int>`, where
`cpu` is the minimum number of CPU units a node must have and `ram` is
the minimum amount of system RAM in megabytes.

`minikube delete` will deprovision this cluster and destroy all associated
resources.


## Caveats

Please note that GitHub is only hosting a mirror of this repository and is not
the authoritative source. Pull requests cannot be accepted.
