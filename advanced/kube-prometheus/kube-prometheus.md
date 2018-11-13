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

curl -SLO https://raw.githubusercontent.com/coreos/prometheus-operator/master/contrib/kube-prometheus/build.sh \
  && chmod +x build.sh

./build.sh minikube-edit.jsonnet

# 
kubectl apply -f ./manifests

kubectl 

kubectl -n monitoring logs -f prometheus-adapter-d8bf44f59-mxzpg



curl -SLO https://raw.githubusercontent.com/coreos/prometheus-operator/master/contrib/kube-prometheus/example.jsonnet

local kp = (import 'kube-prometheus/kube-prometheus.libsonnet') +
           (import 'kube-prometheus/kube-prometheus-kubeadm.libsonnet') + {
  _config+:: {
    namespace: 'monitoring',
    prometheus+:: {
        names: 'k8s',
        replicas: 1,
        rules: {},
    },
    alertmanager+:: {
      name: 'main',
      replicas: 1,
    },
    grafana+:: {
      config: { // http://docs.grafana.org/installation/configuration/
        sections: {
          "auth.anonymous": {enabled: true},
        },
      },
    },
  },
};

{ ['00namespace-' + name]: kp.kubePrometheus[name] for name in std.objectFields(kp.kubePrometheus) } +
{ ['0prometheus-operator-' + name]: kp.prometheusOperator[name] for name in std.objectFields(kp.prometheusOperator) } +
{ ['node-exporter-' + name]: kp.nodeExporter[name] for name in std.objectFields(kp.nodeExporter) } +
{ ['kube-state-metrics-' + name]: kp.kubeStateMetrics[name] for name in std.objectFields(kp.kubeStateMetrics) } +
{ ['alertmanager-' + name]: kp.alertmanager[name] for name in std.objectFields(kp.alertmanager) } +
{ ['prometheus-' + name]: kp.prometheus[name] for name in std.objectFields(kp.prometheus) } +
{ ['prometheus-adapter-' + name]: kp.prometheusAdapter[name] for name in std.objectFields(kp.prometheusAdapter) } +
{ ['grafana-' + name]: kp.grafana[name] for name in std.objectFields(kp.grafana) }

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

minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2 \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook \
  --extra-config=scheduler.address=0.0.0.0 \
  --extra-config=controller-manager.address=0.0.0.0



  --extra-config=apiserver.requestheader-allowed-names=""
  --extra-config=controller-manager.horizontal-pod-autoscaler-use-rest-clients=false 


minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2 \
  --extra-config=kubelet.rotate-server-certificates=true \
  --extra-config=kubelet.authentication-token-webhook=true \
  --extra-config=kubelet.authorization-mode=Webhook



  --extra-config=apiserver.kubelet-certificate-authority=/var/lib/minikube/certs/ca.crt

or
minikube addons enable metrics-server
minikube addons disable metrics-server
minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2


minikube delete ; minikube start --kubernetes-version=v1.12.2 --memory=4096 --bootstrapper=kubeadm --vm-driver kvm2 \
  --extra-config=apiserver.kubelet-certificate-authority=/var/lib/minikube/certs/ca.crt



/usr/bin/kubelet --cluster-dns=10.96.0.10 --cgroup-driver=cgroupfs --fail-swap-on=false \
  --kubeconfig=/etc/kubernetes/kubelet.conf \
  --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf \
  --hostname-override=minikube \
  --allow-privileged=true \
  --pod-manifest-path=/etc/kubernetes/manifests \
  --cluster-domain=cluster.local \
  --authorization-mode=Webhook \
  --client-ca-file=/var/lib/minikube/certs/ca.crt


$ ls /var/lib/minikube/certs/ -l
total 76
-rw-r--r-- 1 root root 1090 Nov 10 01:49 apiserver-etcd-client.crt
-rw------- 1 root root 1675 Nov 10 01:49 apiserver-etcd-client.key
-rw-r--r-- 1 root root 1099 Nov 10 01:49 apiserver-kubelet-client.crt
-rw------- 1 root root 1675 Nov 10 01:49 apiserver-kubelet-client.key
-rw-r--r-- 1 root root 1298 Nov 10 01:48 apiserver.crt
-rw------- 1 root root 1679 Nov 10 01:48 apiserver.key
-rw-r--r-- 1 root root 1066 Nov 10 01:48 ca.crt
-rw------- 1 root root 1675 Nov 10 01:48 ca.key
drwxr-xr-x 2 root root 4096 Nov 10 01:49 etcd
-rw-r--r-- 1 root root 1038 Nov 10 01:49 front-proxy-ca.crt
-rw------- 1 root root 1675 Nov 10 01:49 front-proxy-ca.key
-rw-r--r-- 1 root root 1058 Nov 10 01:49 front-proxy-client.crt
-rw------- 1 root root 1675 Nov 10 01:49 front-proxy-client.key
-rw-r--r-- 1 root root 1074 Nov 10 01:48 proxy-client-ca.crt
-rw------- 1 root root 1679 Nov 10 01:48 proxy-client-ca.key
-rw-r--r-- 1 root root 1103 Nov 10 01:48 proxy-client.crt
-rw------- 1 root root 1675 Nov 10 01:48 proxy-client.key
-rw------- 1 root root 1675 Nov 10 01:49 sa.key
-rw------- 1 root root  451 Nov 10 01:49 sa.pub
$ 



https://github.com/kubernetes/kubernetes/issues/63164
  > TLS bootstrapping only sets up api client certificates for the kubelet currently. If you want a serving cert for the kubelet that is signed by the apiserver's --kubelet-certificate-authority you must provide it. Otherwise the kubelet generates a self-signed serving cert.


```

```
kubectl apply -f ~/Development/github.com/coreos/prometheus-operator/contrib/kube-prometheus/manifests-all.yaml
FIXME upload file to gist?

https://github.com/kubernetes-incubator/metrics-server/issues/133

https://github.com/coreos/prometheus-operator/issues/1859#issuecomment-419518130



```

https://github.com/coreos/prometheus-operator/blob/master/contrib/kube-prometheus/manifests/prometheus-adapter-roleBindingAuthReader.yaml

kubectl create rolebinding -n kube-system \
    resource-metrics-auth-reader \
  --role=extension-apiserver-authentication-reader \
  --serviceaccount=monitoring:prometheus-adapter


role extension-apiserver-authentication-reader


```
kubectl apply -f ~/Development/github.com/kubernetes-incubator/metrics-server/deploy/manifests-all.yaml
FIXME upload file to gist?
```





W1109 23:22:00.064515       1 authentication.go:245] Unable to get configmap/extension-apiserver-authentication in kube-system.  Usually fixed by 'kubectl create rolebinding -n kube-system ROLE_NAME --role=extension-apiserver-authentication-reader --serviceaccount=YOUR_NS:YOUR_SA'
F1109 23:22:00.064552       1 adapter.go:206] unable to install resource metrics API: open /tmp/client-ca-file514069564: no such file or directory

? https://medium.com/@vanSadhu/kubernetes-api-aggregation-setup-nuts-bolts-733fef22a504




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


sudo systemctl cat kubelet


sudo grep 'client-certificate-data' /etc/kubernetes/kubelet.conf | awk '{print $2}' | base64 -d | docker run -i openssl x509 -noout -text



sudo curl -k -v \
  --cacert /var/lib/minikube/certs/ca.crt \
  --key /var/lib/minikube/certs/apiserver.key \
  --cert /var/lib/minikube/certs/apiserver.crt \
  https://localhost:10250/metrics



echo | openssl s_client -showcerts -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -inform pem -noout -text


openssl s_client -showcerts -connect localhost:10250


docker run -v /var/lib/minikube/certs:/var/lib/minikube/certs --network host \
  openssl s_client -connect localhost:10250 \
    -cert /var/lib/minikube/certs/apiserver.crt \
    -key /var/lib/minikube/certs/apiserver.key \
    -state -debug


docker run -v /var/lib/minikube/certs:/var/lib/minikube/certs --network host \
  openssl s_client -connect localhost:10250 \
    -CAfile /var/lib/minikube/certs/ca.crt \
    -cert /var/lib/minikube/certs/apiserver.crt \
    -key /var/lib/minikube/certs/apiserver.key \
    -showcerts


