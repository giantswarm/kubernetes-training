# kube-prometheus

https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus

https://github.com/jsonnet-bundler/jsonnet-bundler



```bash

# Install some dependencies. On Mac `brew` can help out.

# jsonnet
sudo docker run -v $PWD:/go/bin golang:1.11 \
  sh -c "go get github.com/google/go-jsonnet/jsonnet"
sudo mv ./jsonnet /usr/local/bin/

# jb
sudo docker run -v $PWD:/go/bin golang:1.11 \
  sh -c "go get github.com/jsonnet-bundler/jsonnet-bundler/cmd/jb"
sudo mv ./jb /usr/local/bin/

# gojsontoyaml
sudo docker run -v $PWD:/go/bin golang:1.11 \
  sh -c "go get github.com/brancz/gojsontoyaml"
sudo mv ./gojsontoyaml /usr/local/bin/


# bring in kube-prometheus!
jb init
jb install github.com/coreos/prometheus-operator/contrib/kube-prometheus/jsonnet/kube-prometheus

# and an example!
curl -SLO https://raw.githubusercontent.com/coreos/prometheus-operator/master/contrib/kube-prometheus/examples/minikube.jsonnet

curl -SLO https://raw.githubusercontent.com/coreos/prometheus-operator/master/contrib/kube-prometheus/build.sh
chmod +x build.sh

./build.sh minikube.jsonnet

# to the cluster!
kubectl apply -f ./manifests

kubectl get --all-namespaces pods --watch

kubectl -n monitoring logs -f prometheus-adapter-d8bf44f59-mxzpg

kubectl top node


```
