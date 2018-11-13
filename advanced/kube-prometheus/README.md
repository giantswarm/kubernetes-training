# kube-prometheus

https://github.com/jsonnet-bundler/jsonnet-bundler

```bash
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


```bash
# v1.12.2
# v1.11.4
# v1.10.9
# v1.10.1
minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook \
  --extra-config=scheduler.address=0.0.0.0 \
  --extra-config=controller-manager.address=0.0.0.0 \
  --extra-config=kubelet.rotate-server-certificates=true



https://github.com/kubernetes/kubernetes/issues/63164
  > TLS bootstrapping only sets up api client certificates for the kubelet currently. If you want a serving cert for the kubelet that is signed by the apiserver's --kubelet-certificate-authority you must provide it. Otherwise the kubelet generates a self-signed serving cert.


```






https://github.com/DirectXMan12/k8s-prometheus-adapter/blob/master/docs/walkthrough.md

TODO
- show resulting kubelet config



TODO
- show access via kubectl-port-forward, instead of node-port


TODO
- show jsonnet/grafonnet


---
later:
- use keycload to authorize with grafana



https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/#appendix-horizontal-pod-autoscaler-status-conditions
autoscaling/v2beta2


---

https://github.com/kubernetes-incubator/apiserver-builder/blob/master/docs/concepts/auth.md#serving-certificates-authentication-and-authorization

> CA (Certificate Authority) certificates are used to delegate trust. Whenever something trusts the CA, it can trust any certificates signed by the CA private key by verifying the signature using the CA public certificate.

For the API servers created by apiserver-builder
- serving CA


minikube ssh -- ls -l /var/lib/minikube/certs/

minikube ssh -- cat /var/lib/minikube/certs/ca.crt | openssl x509 -in - -noout -text

openssl verify -CAfile /path/to/kubernetes/ca.crt /path/to/kubelet/serving.crt


eval (minikube docker-env)
docker build -t openssl ./minikube/alpine-openssl/

minikube ssh

docker run -v /var/lib/minikube/certs:/var/lib/minikube/certs \
  openssl x509 -in /var/lib/minikube/certs/ca.crt -noout -text

docker run -v /var/lib/minikube/certs:/var/lib/minikube/certs \
  openssl verify -CAfile /var/lib/minikube/certs/ca.crt /var/lib/minikube/certs/apiserver.crt


docker run -v /var/lib/minikube/certs:/var/lib/minikube/certs \
  openssl x509 -in /var/lib/minikube/certs/apiserver-kubelet-client.crt -noout -text

    X509v3 extensions:
        X509v3 Key Usage: critical
            Digital Signature, Key Encipherment
        X509v3 Extended Key Usage: 
            TLS Web Client Authentication

    usages:
    - digital signature
    - key encipherment
    - server auth

