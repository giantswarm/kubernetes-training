```bash

minikube delete

minikube start --bootstrapper kubeadm --kubernetes-version "v1.10.5" --memory 8192 --cpus 4 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook \
  --extra-config=scheduler.address=0.0.0.0 \
  --extra-config=controller-manager.address=0.0.0.0

kubectl get --watch --all-namespaces pods
kubectl get nodes
kubectl describe nodes

# --- preload container images

minikube ssh

images="k8s.gcr.io/kube-apiserver-amd64:v1.10.5 k8s.gcr.io/kube-proxy-amd64:v1.10.5 k8s.gcr.io/kube-controller-manager-amd64:v1.10.5 k8s.gcr.io/kube-scheduler-amd64:v1.10.5 redis:latest quay.io/coreos/prometheus-config-reloader:v0.20.0 quay.io/coreos/prometheus-operator:v0.20.0 k8s.gcr.io/elasticsearch:v6.2.4 grafana/grafana:5.1.0 docker.elastic.co/kibana/kibana-oss:6.2.4 giantswarm/tiny-tools:latest quay.io/coreos/kube-rbac-proxy:v0.3.0 quay.io/coreos/kube-state-metrics:v1.3.0 quay.io/prometheus/prometheus:v2.2.1 k8s.gcr.io/etcd-amd64:3.1.12 k8s.gcr.io/kube-addon-manager:v8.6 quay.io/prometheus/alertmanager:v0.14.0 alpine:3.6 k8s.gcr.io/k8s-dns-dnsmasq-nanny-amd64:1.14.8 k8s.gcr.io/k8s-dns-sidecar-amd64:1.14.8 k8s.gcr.io/k8s-dns-kube-dns-amd64:1.14.8 k8s.gcr.io/pause-amd64:3.1 quay.io/prometheus/node-exporter:v0.15.2 gcr.io/k8s-minikube/storage-provisioner:v1.8.1 quay.io/coreos/configmap-reload:v0.0.1 giantswarm/thux-resolver:latest giantswarm/thux-tracker:latest dockermuenster/caddy:0.9 giantswarm/thux-frontend:latest giantswarm/thux-cleaner:latest quay.io/coreos/addon-resizer:1.0 k8s.gcr.io/fluentd-elasticsearch:v2.1.0"

for image in $images; do
  docker pull $image
done

# ---


# kubernetes/kubernetes
kubectl label node minikube beta.kubernetes.io/fluentd-ds-ready=true
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/fluentd-elasticsearch.yaml
  # based on https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/fluentd-elasticsearch

kubectl --namespace kube-system describe pod elasticsearch-logging-0
kubectl --namespace kube-system logs elasticsearch-logging-0

minikube service list
minikube service --namespace kube-system kibana-logging


# coreos/prometheus-operator
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/kube-prometheus.yaml
  # based on https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus/manifests

minikube service --namespace monitoring grafana
  # login: admin/admin


# giantswarm/twitter-hot-urls-example
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/twitter-hot-urls-example.yaml
  # based on https://github.com/giantswarm/twitter-hot-urls-example/tree/master/manifests

kubectl --namespace thux \
  create secret generic twitter-api \
  --from-file=twitter-consumer-key=./twitter-consumer-key \
  --from-file=twitter-consumer-secret=./twitter-consumer-secret \
  --from-file=twitter-access-token=./twitter-access-token \
  --from-file=twitter-access-token-secret=./twitter-access-token-secret \
  --dry-run --output yaml \
    > ./twitter-secret.yaml

# giantswarm/kubernetes-training/hands-on/twitter-secrets
kubectl apply --filename ./twitter-secret.yaml

kubectl --namespace thux scale deployment tracker --replicas=0


# giantswarm/twitter-hot-urls-example
kubectl apply --filename https://raw.githubusercontent.com/giantswarm/kubernetes-training/master/hands-on/twitter-hot-urls-example-monitoring.yaml

minikube service --namespace thux grafana
```
