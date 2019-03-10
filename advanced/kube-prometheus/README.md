# kube-prometheus

https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus

https://github.com/jsonnet-bundler/jsonnet-bundler


## Troubleshooting

https://github.com/kubernetes/minikube/issues/1378

minikube ssh -- docker run -i --rm --privileged --pid=host debian nsenter -t 1 -m -u -n -i date -u $(date -u +%m%d%H%M%Y)
minikube ssh -- docker run -it --rm --privileged --pid=host alpine nsenter -t 1 -m -u -n -i date -u $(date -u +%m%d%H%M%Y.%S)
minikube ssh -- docker run -i --rm --privileged --pid=host debian nsenter -t 1 -m -u -n -i hwclock -s

minikube ssh -- sudo date -u $(date -u +%m%d%H%M%Y.%S)
minikube ssh -- sudo hwclock -s

sudo systemctl restart systemd-timesyncd

```bash

# Install some dependencies. On Mac `brew` can help out.

# jsonnet
sudo docker run -v $PWD:/go/bin golang:1.12 \
  sh -c "go get github.com/google/go-jsonnet/jsonnet"
sudo mv ./jsonnet /usr/local/bin/
jsonnet --version

# jb
sudo docker run -v $PWD:/go/bin golang:1.12 \
  sh -c "go get github.com/jsonnet-bundler/jsonnet-bundler/cmd/jb"
sudo mv ./jb /usr/local/bin/
# FIXME create feature request for
#  jb --version

# gojsontoyaml
sudo docker run -v $PWD:/go/bin golang:1.12 \
  sh -c "go get github.com/brancz/gojsontoyaml"
sudo mv ./gojsontoyaml /usr/local/bin/


# bring in kube-prometheus!
jb init
jb install github.com/coreos/prometheus-operator/contrib/kube-prometheus/jsonnet/kube-prometheus

jb install github.com/coreos/prometheus-operator/contrib/kube-prometheus/jsonnet/kube-prometheus/@v0.29.0


# and an example!
curl -SLO https://raw.githubusercontent.com/coreos/prometheus-operator/master/contrib/kube-prometheus/examples/minikube.jsonnet

# curl -SLO https://raw.githubusercontent.com/coreos/prometheus-operator/master/contrib/kube-prometheus/build.sh
# chmod +x build.sh
# 
# ./build.sh minikube.jsonnet

mkdir -p manifests
rm -r manifests/*
jsonnet --jpath vendor --multi manifests "minikube.jsonnet" \
  | xargs -I{} sh -c 'cat {} | gojsontoyaml > {}.yaml; rm -f {}' -- {}



# to the cluster!
kubectl apply -f ./manifests

kubectl get --all-namespaces pods --watch

kubectl get certificatesigningrequests


kubectl -n monitoring logs -f prometheus-adapter-d8bf44f59-mxzpg

kubectl top node


```

# --extra-config=kubelet.authentication-token-webhook=true
# at least needed for metrics-server or prometheus-adapter

minikube delete ; minikube start --cpus 4 --memory 4096 --vm-driver kvm2 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.rotate-server-certificates=true

