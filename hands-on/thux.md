
## Start Minikube

On Linux run:
```bash
minikube start --memory 4096 --cpus 4 --vm-driver kvm
```

On Mac run:
```bash
minikube start --memory 4096 --cpus 4
```

## Preload Docker images

To safe some time during the next steps, it is possible to load the needed Docker images upfront in Minikube:
```
minikube ssh
```
```
images="docker:latest giantswarm/tiny-tools:latest redis:latest busybox:latest gcr.io/google_containers/nginx-ingress-controller:0.9.0-beta.8 quay.io/prometheus/alertmanager:v0.7.1 prom/prometheus:v1.7.0 giantswarm/helloworld:latest gcr.io/google_containers/kubernetes-dashboard-amd64:v1.6.1 gcr.io/google_containers/k8s-dns-sidecar-amd64:1.14.2 gcr.io/google_containers/k8s-dns-kube-dns-amd64:1.14.2 gcr.io/google_containers/k8s-dns-dnsmasq-nanny-amd64:1.14.2 gcr.io/google_containers/kube-state-metrics:v0.5.0 grafana/grafana:4.2.0 kibana:5.2.2 prom/node-exporter:v0.14.0 gcr.io/google_containers/heapster:v1.3.0 giantswarm/eventrouter:0.1.2 giantswarm/tiny-tools:0.1.0 giantswarm/filebeat:5.2.2 gcr.io/google-containers/kube-addon-manager:v6.4-beta.1 docker.elastic.co/elasticsearch/elasticsearch:5.2.2 docker.elastic.co/elasticsearch/elasticsearch:5.3.3 dockermuenster/caddy:0.9.3 marian/rebrow:latest giantswarm/thux-resolver:latest giantswarm/thux-tracker:latest dockermuenster/caddy:0.9 giantswarm/thux-frontend:latest giantswarm/thux-cleaner:latest gcr.io/google_containers/pause-amd64:3.0 gcr.io/google_containers/defaultbackend:1.0"

for image in $images; do
  docker pull $image
done
```
It is fine to stop Minikube after this and start later. Just don't run `minikube delete` in between.


## Prepare Minikube for Elastic Stack

```bash
minikube ssh

sudo sh -c "sed -i 's/^ExecStart=\/usr\/bin\/docker daemon.*$/& --log-opt labels=io.kubernetes.container.hash,io.kubernetes.container.name,io.kubernetes.pod.name,io.kubernetes.pod.namespace,io.kubernetes.pod.uid/' /lib/systemd/system/docker.service"

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

For the case the dashboards are missing run this to reconfigure them:
```
kubectl --namespace monitoring delete job grafana-import-dashboards
```

## Logging

```bash
kubectl apply \
  --filename https://raw.githubusercontent.com/giantswarm/kubernetes-elastic-stack/master/manifests-all.yaml
```
```bash
minikube service --namespace logging elasticsearch
minikube service --namespace logging kibana
```

In Kibana set `filebeat-*` as `Index name or pattern` and use `json.timestamp` for fot the `Time Filter field name`.
After that you can switch over to the `Discovery` menu item.

## Twitter Example App

```bash
kubectl create namespace thux
kubectl apply \
  --filename https://raw.githubusercontent.com/giantswarm/twitter-hot-urls-example/master/manifests-all.yaml
```

## Creating the Twitter api secrets manifest

To really bring this application up you need to get four values from your personal Twitter [account](https://twitter.com/signup) and add them to `secrets/twitter-api-secret.yaml`. For some background see the Twitter documentation about [streaming API](https://dev.twitter.com/streaming/overview/connecting).

Go to [Twitter Application Management](https://apps.twitter.com/) and create a [new](https://apps.twitter.com/app/new) application. Enter some details like these:

    Name: thux
    Description: Tracks URLs mentioned on Twitter and creates a ranked list
    Website: https://github.com/giantswarm/twitter-hot-urls-example
    Callback URL: <leave this field blank>

After that also create an Access Token under "Keys and Access Tokens". Create a file `twitter-api-secret.yaml` and fill all four data fields with the corresponding [`base64` encoded values]((http://kubernetes.io/docs/user-guide/secrets/#creating-a-secret-manually)).

```
# twitter-api-secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: twitter-api
  namespace: thux
  labels:
    app: thux
type: Opaque
data:
  # values must be base64 encoded
  # with no a trailing newline.
  # use something like this:
  # printf "exampletokenxyz" | base64
  twitter-consumer-key:
  twitter-consumer-secret:
  twitter-access-token:
  twitter-access-token-secret: 
```

```bash
kubectl apply --filename twitter-api-secret.yaml
```

## Scaling up and down

```bash
kubectl --namespace thux scale deployments/resolver --replicas 3

# there is an api limit. don't track too much, to pause the tracker like this:
kubectl --namespace thux scale deployments/tracker --replicas 0
```
