# Running Containers and Exposing Services II

 - more on labels and selectors
   - from (ingress)/port->service->pod
 - delete by selectors

## Basic Concepts in Kubernetes II

### Namespaces

The Kubernetes documentation call Namespaces "virtual clusters" and in a way namespaces do separate the cluster into separate environments. However, namespaces do not bring isolation of resources by default. They only make sure that resources in a certain namespaces by default talk to resources in the same namespace.

They are a great way of keeping your clusters orderly as you can group your deployments (and connected resources) in separate environments. For example you could have a `monitoring` namespace, which holds all your monitoring tools.

You could also create a namespace for a project you're currently working on. A namespace also makes it very easy to clean up after yourself. For example, you could create a `myapp-test` namespace to test out some things you are working on and once you are done, you can delete everything with a single

`kubectl delete namespace myapp-test`

Another use case for namespaces is separating environments like dev, testing, QA, pre-prod, and prod (more on that later).

### Node Selectors

In some cases you want to schedule pods to specific nodes. This might be because you want specific pods to run on the same host and be able to communicate faster or because you have a policy of e.g. running frontends on separate machines than backends. You could also have labeled nodes based on the technologies they support, for example if you have nodes with SSDs and others with HDDs.

In these cases you can use Node Selectors to let your pods be scheduled to a specific set of nodes.

For this you need to first assign labels to your pods. You can do this on a per node basis or give a group of pods the same label.

You then use the `nodeSelector` field in the Pod specification to select the nodes you want the pod(s) to be scheduled to.

### Config Maps

### Secrets

### Daemonsets 

### Jobs

### Scheduled Jobs


## Further Reading

- [Understanding Basic Kubernetes Concepts IV - Secrets and ConfigMaps](https://blog.giantswarm.io/understanding-basic-kubernetes-concepts-iv-secrets-and-configmaps/)
- [Understanding Basic Kubernetes Concepts V - Daemon Sets and Jobs](https://blog.giantswarm.io/understanding-basic-kubernetes-concepts-v-daemon-sets-and-jobs/)
- [Namespaces Reference Documentation](http://kubernetes.io/docs/user-guide/namespaces/)
- [Node Selectors Reference Documentation](http://kubernetes.io/docs/user-guide/node-selection/)
- [ConfigMaps Reference Documentation](http://kubernetes.io/docs/user-guide/configmap/)
- [Secrets Reference Documentation](http://kubernetes.io/docs/user-guide/secrets/)
- [Daemon Sets Reference Documentation](http://kubernetes.io/docs/admin/daemons/)
- [Jobs Reference Documentation](http://kubernetes.io/docs/user-guide/jobs/)
- [Scheduled Jobs Reference Documentation](http://kubernetes.io/docs/user-guide/scheduled-jobs/)