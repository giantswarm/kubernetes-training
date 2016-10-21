# Outlook

## From the Kubernetes Roadmap

### Advanced Scheduling

- [Scheduled Jobs](http://kubernetes.io/docs/user-guide/scheduled-jobs/)
- [Inter-pod affinity & anti-affinity](https://github.com/kubernetes/kubernetes/blob/master/docs/design/podaffinity.md)
- [Node affinity](http://kubernetes.io/docs/user-guidenode-selection/#alpha-feature-in-kubernetes-v12-node-affinity)
- [Taints, Tolerations, and Dedicated Nodes](https://github.com/kubernetes/kubernetes/blob/release-1.4/docs/design/taint-toleration-dedicated.md)

### App Deployments and Reuse

- [Helm](http://blog.kubernetes.io/2016/10/helm-charts-making-it-simple-to-package-and-deploy-apps-on-kubernetes.html)
- [KPM](https://github.com/coreos/kpm)
- [AppController - statefull app deployments](https://github.com/Mirantis/k8s-AppController)
- [Templates & Parameterization](https://github.com/kubernetes/kubernetes/blob/master/docs/proposals/templates.md)

### Storage & Persistence

- [Pet Sets](http://kubernetes.io/docs/user-guide/petset/)
- [Configurable Dynamic Volume Provisioning aka StorageClass](https://github.com/kubernetes/kubernetes/blob/master/docs/proposals/volume-provisioning.md)

### Security & Compliance

- [RBAC and restricting access inside the cluster](https://github.com/TremoloSecurity/wiki/blob/master/kubernetes.md)  
- [Encrypt secrets in etcd](https://github.com/kubernetes/features/issues/92)
- [Kubectl login subcommand](https://github.com/kubernetes/kubernetes/blob/master/docs/proposals/kubectl-login.md)
- [Authenticated/Authorized access to kubelet API](https://github.com/kubernetes/kubernetes/blob/master/docs/proposals/kubelet-auth.md)
- Automated builds
    - [Docker Hub](https://docs.docker.com/docker-hub/builds/)
    - [Quay](https://tectonic.com/quay-enterprise/docs/latest/build-support.html)
- [Quay.io](https://quay.io/) & [Clair](https://coreos.com/blog/vulnerability-analysis-for-containers/)
- [Vault](https://www.vaultproject.io/)

### Scaling & Resilience

- [Federation](https://github.com/kubernetes/kubernetes/blob/master/docs/proposals/federation.md)
- [etcd v3 API storage backend](https://github.com/kubernetes/kubernetes/issues/22448)