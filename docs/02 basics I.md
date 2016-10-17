# Running Containers and Exposing Services I

## Minikube

### Minikube
> Minikube is a tool that makes it easy to run Kubernetes locally. Minikube runs a single-node Kubernetes cluster inside a VM on your laptop

### Current Features

- DNS
- NodePorts
- ConfigMaps and Secrets
- Dashboards
- Container Runtime: Docker, and rkt
- Enabling CNI (Container Network Interface)

### Usage

```bash
minikube start \
  --vm-driver kvm \
  --memory 2048 \
  --logtostderr true \
  --v 4
```

```bash
kubectl cluster-info

> Kubernetes master is running at https://192.168.42.2:8443
> kubernetes-dashboard is running at https://192.168.42.2:8443/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard
```

Watch the dashboard in a browser:
```bash
minikube dashboard
```

See what's running from the commandline:
```bash
kubectl get --all-namespaces pods
```

```bash
minikube stop
```

```bash
minikube delete
```

## Basic Concepts in Kubernetes

Pods

Labels
  Metadata

Deployments (& Replica Sets)

Services

Ingress

(maybe keep ingress theory only)
