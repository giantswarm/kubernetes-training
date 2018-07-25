## Start Minikube
Make sure any old minikube VM is deleted.
```bash
minikube delete
```

Start with custom flags for better usage.
```bash
minikube start --bootstrapper kubeadm --kubernetes-version "v1.10.5" --memory 8192 --cpus 4 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook \
  --extra-config=scheduler.address=0.0.0.0 \
  --extra-config=controller-manager.address=0.0.0.0
```

Inspect the cluster.

```bash
kubectl cluster-info
kubectl get --watch --all-namespaces pods
kubectl get nodes
kubectl describe nodes
```

## Preload Docker Images
To safe some time during the next steps, it is possible to load the needed Docker images upfront in Minikube:

```bash
minikube ssh
```

```bash
images="k8s.gcr.io/kube-apiserver-amd64:v1.10.5
k8s.gcr.io/kube-proxy-amd64:v1.10.5
k8s.gcr.io/kube-controller-manager-amd64:v1.10.5
k8s.gcr.io/kube-scheduler-amd64:v1.10.5 redis:latest
quay.io/coreos/prometheus-config-reloader:v0.20.0
quay.io/coreos/prometheus-operator:v0.20.0 k8s.gcr.io/elasticsearch:v6.2.4
grafana/grafana:5.1.0 docker.elastic.co/kibana/kibana-oss:6.2.4
giantswarm/tiny-tools:latest quay.io/coreos/kube-rbac-proxy:v0.3.0
quay.io/coreos/kube-state-metrics:v1.3.0 quay.io/prometheus/prometheus:v2.2.1
k8s.gcr.io/etcd-amd64:3.1.12 k8s.gcr.io/kube-addon-manager:v8.6
quay.io/prometheus/alertmanager:v0.14.0 alpine:3.6
k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64:1.14.8
k8s.gcr.io/k8s-dns-sidecar-amd64:1.14.8 k8s.gcr.io/k8s-dns-kube-dns-amd64:1.14.8
k8s.gcr.io/pause-amd64:3.1 quay.io/prometheus/node-exporter:v0.15.2
gcr.io/k8s-minikube/storage-provisioner:v1.8.1
quay.io/coreos/configmap-reload:v0.0.1 giantswarm/thux-resolver:latest
giantswarm/thux-tracker:latest dockermuenster/caddy:0.9
giantswarm/thux-frontend:latest giantswarm/thux-cleaner:latest
quay.io/coreos/addon-resizer:1.0 k8s.gcr.io/fluentd-elasticsearch:v2.1.0
giantswarm/thux-cleaner:latest marian/rebrow:latest"

for image in $images; do
  docker pull $image
done
```

It is fine to stop Minikube after this and start later. Just don't run `minikube delete` in between.

## Kubernetes Dashboard
```bash
minikube dashboard
```

## Install the Logging Stack
Based on https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/fluentd-elasticsearch
```bash
# Enable minikube to run fluentd daemonset
kubectl label node minikube beta.kubernetes.io/fluentd-ds-ready=true
# Apply fluentd+elasticsearch templates
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/fluentd-elasticsearch.yaml
```


View the elasticsearch pod:
```bash
kubectl --namespace kube-system describe pod elasticsearch-logging-0
```

Access the elasticsearch logs:
```bash
kubectl --namespace kube-system logs elasticsearch-logging-0
```

### View the exposed Services and IPs
```bash
minikube service list
```
```bash
minikube service --namespace kube-system kibana-logging
```


## Install Prometheus Stack
Based on https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus/manifests
```bash
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/kube-prometheus.yaml
```

Open Grafana:
```bash
# login: admin/admin
minikube service --namespace monitoring grafana
```


## Install Twitter Hot Urls Example
Based on https://github.com/giantswarm/twitter-hot-urls-example/tree/master/manifests
```bash
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/twitter-hot-urls-example.yaml
```


## Create Twitter Credentials Secrets
Twitters API needs credentials to be accessed. We store them in form of secrets,
that our resources have access to.
```bash
kubectl --namespace thux \
  create secret generic twitter-api \
  --from-file=twitter-consumer-key=./twitter-consumer-key \
  --from-file=twitter-consumer-secret=./twitter-consumer-secret \
  --from-file=twitter-access-token=./twitter-access-token \
  --from-file=twitter-access-token-secret=./twitter-access-token-secret \
  --dry-run --output yaml \
    > ./twitter-secret.yaml
```

```bash
kubectl apply --filename ./twitter-secret.yaml
```

Scale tracker down to 0 pods.
```bash
kubectl --namespace thux scale deployment tracker --replicas=0
```

## Install Monitoring for the Twitter Hot Urls Example
```bash
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/twitter-hot-urls-example-monitoring.yaml
```

Open thux Grafana:
```bash
minikube service --namespace thux grafana
```
