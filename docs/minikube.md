# Minikube



## Starting a local Kubernetes platform

```bash
minikube start \
  --vm-driver kvm \
  --memory 2048 \
  --logtostderr true \
  --v 4
```

```bash
kubectl cluster-info

> Kubernetes master is running at https://192.168.42.2:8443
> kubernetes-dashboard is running at https://192.168.42.2:8443/api/v1/proxy/namespaces/kube-system/services/kubernetes-dashboard
```

Watch the dashboard in a browser:
```bash
minikube dashboard
```

See what's running from the commandline:
```bash
kubectl get --all-namespaces pods
```
