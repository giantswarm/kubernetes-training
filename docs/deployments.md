# Deployments

Bring up a container:


In fact this this brings up a `Deployment` that creates a `Pod` in which our container is running. The `Deployment` manifest states that the `Pod` should always be running.

See the `Manifest`:
```
kubectl get pod/<pod-id> --output yaml
```


Let's check out what happens when we just delete the `Pod`:
```
kubectl delete pod/<pod-id>
```
