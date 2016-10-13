#  Rolling Updates & Multiple Environments

## Rolling Updates

### Deployment Updates

Rolling updates to pods can be done through updates of their respective deployment. If there are more than one replica in the deployment, a rolling update will be initiated. Kubernetes monitors the update and automatically stop and stops a rollout if the health the new/updated pods fail.

### How to update

There are several ways to update a Deployment.

- Edit the deployment manifest
    - locally/git + `kubectl apply -f <manifest-file>`
    - `kubectl edit deployment <deployment-name>`
- Set a new image
    - `kubectl set image deployment <deployment-name> <container-name>=<image>:<tag>`

### Checking on updates

While the update is running you can check the status with

`kubectl rollout status deployment <deployment-name>`

Once it is done you can check the deployment:

`kubectl get deployment <deployment-name>`

`kubectl describe deployment <deployment-name>`

### Deployment Audit Log

You can check the revisions of a deployment in the audit log (also called rollout history).

`kubectl rollout history deployment <deployment-name>`

For further details on what has actually changed in a specific revision

`kubectl rollout history deployment <deployment-name> --revision=2`

You can adjust the length of the history with [`.spec.revisionHistoryLimit`](http://kubernetes.io/docs/user-guide/deployments/#revision-history-limit).

### Rolling Back

Rolling back to the previous version is easy.

`kubectl rollout undo deployment <deployment-name>`

You can also roll back to a specific former revision.

`kubectl rollout undo deployment <deployment-name> --revision=2`

### Update Strategies

By default a rolling update strategy will be attached to your deployment. You can, however, also define the update strategy manually.

Your strategy type can be either `RollingUpdate` or `Recreate`. The latter kills all existing pods before creating new ones. The former does a rolling update with two variables that again can be manually defined:

- `maxUnavailable`
    - Defines the number (or percentage) of Pods that can be unavailable during the update process. 
- `maxSurge`
    - Specifies the maximum number (or percentage) of Pods that can be created above the desired number of Pods.

By tweaking these variables you can adjust the rolling update strategy to your sepcific needs.

You can additionally sepcify a field called `minReadySeconds`, which defines the minimum number of seconds for which a newly created Pod should be ready without any of its containers crashing, for it to be considered available. By default this is set to `0`. Setting this to a higher number will slow down your update process, but might be useful to make sure your rollout is actually stable.

### Blue/Green & Canary Deployments

You can work with `kubectl rollout pause` and `kubectl rollout resume`, however, that is not very sophisticated. The currently recommended way is to use a second Deployment (with usually fewer replicas), which is identical to the first Deployment, but has a different deployment name and updated image(s). As your pods are still labeled the same, your service will include them in its selector by default and route traffic to the new pods as soon as they're deployed.

Once you're confident that your new release is working as intended you can update your first Deployment and remove the second one again.

## Multiple Environments

### Multiple Environments & Isolation

When talking about multiple environments, there are many variables implied that need clarfication before choosing a fitting solution.

The first variable is the number of environment types needed, as in dev, testing, QA, pre-prod, prod, etc.

The second variable is if there are multiple teams and if these teams need separate environments.

However, these two variables only define the number of environments. On top of that the organization needs to decide on what level of isolation between environments is desired or in bigger organizations even required by compliance & security.

### Separating Environments in Kubernetes

The most native way of separating environments in Kubernetes is using Namespaces. However, there's also the option to use completely separate clusters if isolation requirements are high.

### Isolation by Namespaces

Namespaces bring a certain level of isolation by default. They separate all resources created in them, but only on a soft level. That is, resources like for example pods are not blocked from using resources like for example services from other namespaces. They can access services in other namespaces through their FQDN on DNS or also through accessing the Kubernetes API.

If a real isolation is wanted it needs to be enforced with a combination of network policies as wellas authorization and admission rules. All of these concepts are available in Kubernetes 1.4 already. However, some of them are still being actively worked on and might change and improve in future releases.

### Isolation by clusters
 

 (federation as bonus)

### Switching between environments
- switching namespaces
- switching clusters

### Configuration and Secrets help
- keeping different configmaps and secrets per env