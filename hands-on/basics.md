## Basic Concepts in Kubernetes I

### Pods

#### Run

```bash
kubectl run webservice \
  --image giantswarm/helloworld-caddy
```

#### Inspect

```bash
kubectl get deployments

kubectl describe deployment webservice

kubectl get deployment webservice \
  --output yaml

kubectl explain deployment

kubectl explain replicaset

kubectl get replicasets

kubectl get replicaset webservice-3142165772 \
  --output yaml

kubectl get replicaset webservice-3142165772 \
  --output json | jq '.'

kubectl get replicaset webservice-3142165772 \
  --output json | jq '.spec.template.spec'

# see ip addresses
kubectl get pods \
  --all-namespaces \
  --output wide

# jump in a container
# and inspect from there
kubectl run utils \
  --stdin \
  --tty \
  --restart Never \
  --image webwurst/curl-utils \
    sh

  hostname
  ip addr
  ping <ip-addr of pod>
  curl <ip-addr of pod>

# pod still exists
kubectl get --all-namespaces pods --show-all

kubectl logs webservice-3142165772-penwp
  # hint: central logging

kubectl delete pod utils

# now with `--rm`
kubectl run utils \
  --stdin \
  --tty \
  --restart Never \
  --rm \
  --image webwurst/curl-utils \
  --command /bin/sh
```

#### Why does this not create a deployment?

```bash
kubectl run --help
```
> --restart string
>
>   The restart policy for this Pod.  Legal values [Always, OnFailure, Never].  If set to 'Always' a deployment is created for this pod, if set to 'OnFailure', a job is created for this pod, if set to 'Never', a regular pod is created. For the latter two --replicas must be 1.

FIXME job, later


### Labels & Selectors

```bash
kubectl get pods --show-labels

kubectl get pods,replicasets,deployments \
  --show-labels
```

### Deployments (& Replica Sets)




### Services

```bash
kubectl expose --help
```

> Looks up a deployment, service, replica set, replication controller or pod by name and uses the selector for that resource as the selector for a new service on the specified port.

```bash
kubectl expose deployment webservice \
  --port=80 \
  --type NodePort

```
> --type string<br/>
    Type for this service: ClusterIP (default), NodePort, or LoadBalancer.

> --cluster-ip string<br/>
    ClusterIP to be assigned to the service. Leave empty to auto-allocate, or set to 'None' to create a headless service.

FIXME headless, example "prometheus-node-exporter"?, later

```bash
kubectl get services \
  --all-namespaces \
  --output wide

kubectl run utils \
  --stdin \
  --tty \
  --restart Never \
  --rm \
  --image webwurst/curl-utils \
  --command /bin/sh

  ping <ip-addr of service>
  ping webservice.default.svc
  curl http://webservice.default.svc
```

FIXME minikube service webservice

### Ingress
