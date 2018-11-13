# Minikube Setup

```bash

# use separate kubeconfig file
export KUBECONFIGS=$HOME/kubeconfigs-workshop/
export KUBECONFIG=$KUBECONFIGS/minikube-cert-admin.conf
mkdir $KUBECONFIGS


# now bring up the machine!
# adjust `--vm-driver` for your environment
# probably `--vm-driver=virtualbox` for windows or mac
minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook \
  --extra-config=scheduler.address=0.0.0.0 \
  --extra-config=controller-manager.address=0.0.0.0 \
  --extra-config=kubelet.sync-frequency=1s \
  --extra-config=kubelet.rotate-server-certificates=true


kubectl get --all-namespaces pods --watch

# prepull and copy images
images="busybox k8s.gcr.io/hpa-example k8s.gcr.io/hpa-example k8s.gcr.io/hpa-example k8s.gcr.io/hpa-example k8s.gcr.io/coredns:1.2.2 gcr.io/google_containers/defaultbackend:1.4 k8s.gcr.io/etcd:3.2.24 k8s.gcr.io/kube-addon-manager:v8.6 k8s.gcr.io/kube-apiserver:v1.12.2 k8s.gcr.io/kube-controller-manager:v1.12.2 k8s.gcr.io/kube-proxy:v1.12.2 k8s.gcr.io/kube-scheduler:v1.12.2 k8s.gcr.io/kubernetes-dashboard-amd64:v1.10.0 k8s.gcr.io/metrics-server-amd64:v0.3.1 quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.19.0 gcr.io/k8s-minikube/storage-provisioner:v1.8.1 quay.io/prometheus/alertmanager:v0.15.2 quay.io/coreos/configmap-reload:v0.0.1 grafana/grafana:5.2.4 quay.io/coreos/kube-rbac-proxy:v0.4.0 quay.io/coreos/kube-rbac-proxy:v0.4.0 quay.io/coreos/kube-state-metrics:v1.4.0 quay.io/coreos/addon-resizer:1.0 quay.io/prometheus/node-exporter:v0.16.0 quay.io/coreos/kube-rbac-proxy:v0.4.0 directxman12/k8s-prometheus-adapter-amd64:v0.3.0 quay.io/prometheus/prometheus:v2.5.0 quay.io/coreos/prometheus-config-reloader:v0.25.0 quay.io/coreos/configmap-reload:v0.0.1 quay.io/coreos/prometheus-operator:v0.25.0⏎"

# pull on host
for image in $images; do
  sudo docker pull $image
done

# copy to minikube
for image in $images; do
  sudo docker save $image | (eval $(minikube docker-env --shell bash) && docker load) || true
done


```

Hackpad for random ephemeral public notes:
  https://hackmd.okfn.de/J_GRcBn9Ssei54Fts75ZxA#