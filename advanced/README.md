# Minikube Setup

```bash

# prepull and copy images
images="k8s.gcr.io/kube-proxy:v1.13.4 k8s.gcr.io/kube-scheduler:v1.13.4 k8s.gcr.io/kube-apiserver:v1.13.4 k8s.gcr.io/kube-controller-manager:v1.13.4 grafana/grafana:6.0.0-beta1 quay.io/coreos/prometheus-config-reloader:v0.28.0 quay.io/coreos/prometheus-operator:v0.28.0 quay.io/coreos/kube-rbac-proxy:v0.4.1 quay.io/prometheus/alertmanager:v0.16.0 quay.io/coreos/kube-state-metrics:v1.5.0 quay.io/coreos/k8s-prometheus-adapter-amd64:v0.4.1 quay.io/prometheus/node-exporter:v0.17.0 quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0 quay.io/prometheus/prometheus:v2.5.0 k8s.gcr.io/coredns:1.2.6 k8s.gcr.io/etcd:3.2.24 k8s.gcr.io/kube-addon-manager:v8.6 k8s.gcr.io/pause:3.1 gcr.io/k8s-minikube/storage-provisioner:v1.8.1 gcr.io/google_containers/defaultbackend:1.4 gcr.io/google-containers/addon-resizer-amd64:2.1 quay.io/coreos/configmap-reload:v0.0.1 alpine:3.7 postgres:9.6 k8s.gcr.io/kube-proxy:v1.13.4 k8s.gcr.io/kube-apiserver:v1.13.4 k8s.gcr.io/kube-scheduler:v1.13.4 k8s.gcr.io/kube-controller-manager:v1.13.4 jboss/keycloak:4.8.3.Final quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0 k8s.gcr.io/coredns:1.2.6 k8s.gcr.io/etcd:3.2.24 k8s.gcr.io/kube-addon-manager:v8.6 k8s.gcr.io/pause:3.1 gcr.io/google-samples/hello-app:1.0 gcr.io/k8s-minikube/storage-provisioner:v1.8.1 gcr.io/google_containers/defaultbackend:1.4 gcr.io/heptio-images/gangway:v3.0.0"


# pull on host
for image in $images; do
  sudo docker pull $image
done

# check minikube for current version
minikube version
# -> minikube version: v0.35.0

# start minikube. edit `--vm-driver` for your environment
minikube delete ; minikube start --cpus 4 --memory 8192 --vm-driver kvm2 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.rotate-server-certificates=true

# copy to minikube
for image in $images; do
  sudo docker save $image | (eval $(minikube docker-env --shell bash) && docker load) || true
done

```

Hackpad for random ephemeral public notes:
  https://hackmd.okfn.de/LGSXzhMRTCu76LASIOnI8g#



## Notes


Horizontal Pod Autoscaler Walkthrough
  https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/


OpenID-Connect
  https://openid.net/foundation/presentations-videos/


Custom metrics
  https://github.com/giantswarm/kubernetes-training/blob/master/hands-on/thux2.md

  https://github.com/giantswarm/twitter-hot-urls-example/blob/master/docker-images/resolver/resolve.py#L46-L47
  https://github.com/giantswarm/twitter-hot-urls-example/blob/master/manifests/resolver-deployment.yaml#L32-L37


Vault
  https://github.com/banzaicloud/bank-vaults/#mutating-webhook
  https://github.com/kubevault/docs/tree/master/docs/concepts


PDB
  https://kubernetes.io/docs/tasks/run-application/configure-pdb/#specifying-a-poddisruptionbudget

