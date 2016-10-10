

Not stable yet as of version 1.4:
- [Dramatically Simplify Kubernetes Cluster Creation](https://github.com/kubernetes/features/issues/11)
- [ScheduledJobs](https://github.com/kubernetes/features/issues/19)
- [Configurable Dynamic Provisioning aka StorageClass](https://github.com/kubernetes/features/issues/36)
- [Kubelet TLS Bootstrap](https://github.com/kubernetes/features/issues/43)
- [Federation](https://github.com/kubernetes/features/issues?q=is%3Aissue+is%3Aopen+label%3Ateam%2FSIG-Federation)

Future Features:
- [Encrypt secrets in etcd](https://github.com/kubernetes/features/issues/92)
- [Authenticated/Authorized access to kubelet API](https://github.com/kubernetes/features/issues/89)
- [Simplify HA Setup for Master](https://github.com/kubernetes/features/issues/48)
- [etcd v3 API storage backend](https://github.com/kubernetes/features/issues/44)
- [Inter-pod affinity/anti-affinity](https://github.com/kubernetes/features/issues/60)
- [AppController - statefull app deployments](https://github.com/kubernetes/features/issues/42)
- [Add a simple template API object that assists with config parameterization](https://github.com/kubernetes/features/issues/35)
- [Kubectl login subcommand](https://github.com/kubernetes/features/issues/32)
- for a lot more see:
  - [Feature Tracking and Backlog](https://github.com/kubernetes/features/issues)


Kelsey Hightower (@kelseyhightower) [August 3, 2016](https://twitter.com/kelseyhightower/status/760832204100345856)
> In the future we will see tons of Kubernetes controllers that focus on managing complex applications such as multi-node redis clusters.
> These controllers will be driven by declarative configs and actually manage applications; not simply deploy them. There is a difference.
> Future Kubernetes controllers will not be generic. They will be hyper focused on a single application and will be driven by third parties.
