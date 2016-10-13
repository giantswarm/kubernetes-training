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

- isolation by namespaces
- isolation by clusters (federation as bonus)
- switching namespaces
- switching clusters
- keeping different configmaps and secrets per env