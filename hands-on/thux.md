
## Start Minikube

On Linux run:
```bash
minikube start --vm-driver kvm
```

On Mac run:
```bash
minikube start --vm-driver=xhyve
```


## Prepare Minikube for Elastic Stack

```bash
minikube ssh

sudo sh -c "sed -i 's/^ExecStart=\/usr\/bin\/docker daemon.*$/& --log-opt labels=io.kubernetes.container.hash,io.kubernetes.container.name,io.kubernetes.pod.name,io.kubernetes.pod.namespace,io.kubernetes.pod.uid/' /etc/systemd/system/docker.service"

sudo systemctl daemon-reload
sudo systemctl restart docker.service
```


## Dashboard

```bash
minikube dashboard
```


## Monitoring

```bash
kubectl apply \
  --filename https://raw.githubusercontent.com/giantswarm/kubernetes-prometheus/master/manifests-all.yaml
```
```bash
minikube service --namespace monitoring prometheus
minikube service --namespace monitoring grafana
```

Default username/password is "admin/admin".


## Logging

```bash
kubectl apply \
  --filename https://raw.githubusercontent.com/giantswarm/kubernetes-elastic-stack/master/manifests-all.yaml
```
```bash
minikube service --namespace logging elasticsearch
minikube service --namespace logging kibana
```

## Twitter Example App

```bash
kubectl \
  --filename https://raw.githubusercontent.com/giantswarm/twitter-hot-urls-example/master/manifests-all.yaml
```

FIXME add how to create secret here


https://github.com/giantswarm/twitter-hot-urls-example
