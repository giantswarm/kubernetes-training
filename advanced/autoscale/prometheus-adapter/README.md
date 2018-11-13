
[ WORK IN PROGRESS ]

https://github.com/DirectXMan12/k8s-prometheus-adapter/blob/master/docs/walkthrough.md

```bash
kubectl apply -f sample-app.deploy.yaml

kubectl create service clusterip sample-app --tcp=80:8080

FIXME create ingress


kubectl create -f https://k8s.io/examples/admin/dns/busybox.yaml
kubectl exec -ti busybox -- wget -qO - sample-app/metrics


kubectl apply -f sample-app-hpa.yaml

kubectl apply -f service-monitor.yaml


minikube service list

```


https://github.com/coreos/prometheus-operator/tree/master/contrib/kube-prometheus

https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/