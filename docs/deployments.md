# Deployments

FIXME!
  - provide images with webpage "hello world" / "holla mundo"


Bring up a container:

```bash
kubectl run webservice \
  --image dockermuenster/caddy

kubectl get deployments
kubectl describe deployment webservice

kubectl get deployment webservice \
  --output yaml

kubectl explain deployment
kubectl explain replicaset

kubectl get replicasets
kubectl get replicaset webservice-1566548561 \
  --output yaml

kubectl get replicaset webservice-1566548561 \
  --output json | jq '.'

kubectl get replicaset webservice-1566548561 \
  --output json | jq '.spec.template.spec'


kubectl get pods
kubectl get pod webservice-1566548561-rs651 \
  --output yaml

kubectl get

kubectl run utils \
  --stdin \
  --tty \
  --restart Never \
  --image webwurst/curl-utils \
    sh

  ping 10.3.52.2
  ping 192.168.249.206
  curl http://192.168.249.206
  ping webservice.default.svc

kubectl run --help

# --restart string
#   The restart policy for this Pod.  Legal values [Always, OnFailure, Never].  If set to 'Always' a deployment is created for this pod, if set to 'OnFailure', a job is created for this pod, if set to 'Never', a regular pod is created. For the latter two --replicas must be 1.  Default 'Always' (default "Always")

FIXME
  - kubectl run "once" showing env
  - kubectl get pods --show-all
kubectl get pods --show-labels


kubectl expose --help

# Looks up a deployment, service, replica set, replication controller or pod by name and uses the selector
for that resource as the selector for a new service on the specified port.


kubectl expose deployment webservice \
  --port=80 \
  --target-port=80 \
  --type

  > --type string
    Type for this service: ClusterIP, NodePort, or LoadBalancer. Default is 'ClusterIP'.
  > --cluster-ip string
    ClusterIP to be assigned to the service. Leave empty to auto-allocate, or set to 'None' to create a headless service.


kubectl get services
kubectl get service webservice \
  --output yaml

kubectl run utils \
  --stdin \
  --tty \
  --restart Never \
  --rm \
  --image webwurst/curl-utils \
    sh

kubectl get pods --show-all

  ping webservice.default.svc
  curl webservice.default.svc




kubectl run nginx \
  --image nginx \
  --overrides '{ "apiVersion": "v1", "spec": { ... } }'

kubectl --namespace testing run pi \
  --image perl \
  --restart OnFailure \
  -- \
    perl -Mbignum=bpi -wle 'print bpi(2000)'
```


In fact this brings up a `Deployment` that creates a `Pod` in which our container is running. The `Deployment` manifest states that the `Pod` should always be running.

See the `Manifest`:
```
kubectl get pod/<pod-id> --output yaml
```


Let's check out what happens when we just delete the `Pod`:
```
kubectl delete pod/<pod-id>
```


add configmap
  html page
  hugo-setup?
    store in database?

  service/ingress then?

  later:
    persistency?



kubectl rollout

kubectl apply / edit / patch? / replace?

  delete

---
Nice to know:
- kubectl explain pods.spec
