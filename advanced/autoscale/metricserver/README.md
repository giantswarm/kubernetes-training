
https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/


```bash
# eval $(minikube docker-env --shell bash)
# docker build -t php-apache .

kubectl apply -f ./manifests-all.yaml

kubectl run php-apache --image=k8s.gcr.io/hpa-example --requests=cpu=200m --expose --port=80
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10

minikube addons enable dashboard
minikube dashboard

kubectl -n kube-system get pods
kubectl -n kube-system logs -f metrics-server-5cbbc84f8c-xhv65

kubectl get csr
kubectl certificate approve csr-6khkt

kubectl top node

kubectl run -i --tty load-generator --image=busybox /bin/sh

  while true; do wget -q -O- http://php-apache.default.svc.cluster.local; done
  exit

kubectl get hpa --watch

```


hackmd for random ephemeral notes:
  https://hackmd.okfn.de/CGcHugn6TjuEsZPWU7hnxw#
