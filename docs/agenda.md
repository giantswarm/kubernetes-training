# Agenda

Personal notes:

Atm we plan for six sessions each about one hour.

For each session:
  - Overview about keywords. At best present during session on flip chart.
  - Slides plus demo
  - Hands on to reproduce demo
  - Maybe a quiz at end. Just some slides with questions or multiple choice. Maybe also to discuss some edge cases.
  - Flip chart with keywords can be pinned somewhere in room, growing collection.
    Or maybe we could also pin all flip charts in advance, turned reverse. Including times and breaks as a timeline.
      - "Fun" questions like number of open-issues, top contributors/companies, .., maybe also a bit about docker, rkt, etc.

At the end provide sheet for evaluation?


FIXME
  difference/idea between deployment + replicaset ?
FIXME
  what about apply vs. `create --save-config`


Rough path through hands-on:
  - kubectl run/expose to start containers
    - inspect created objects, manifests on Kubernetes
  - show howto start a onetime "debug" container to get view from within the cluster
    - ping againts pod-ip, service-ip
    - deployment vs. job. vs. pod
    - kubectl --show-all
  - kubectl --show-labels
  - kubectl --selectors to match pods. like service does
  - kubectl delete via --selectors

  - add namespace to the mix
  - kubectl delete namespace
  - dns names for services
  - configmap to overwrite hello-world page

    - on monitoring/logging setup
    - inspect from ingress to pods
  - show daemonset
    - node/pod affinity
  - show job

  - add demo-app with custom-metrics
    - maybe also add custom-metrics to hello-world?


09:00
Croissants and coffee, round of introductions.

10:00
Session "Warm up"
  - Idea behind the Kubernetes architecture
    - api for scaling, upgrades, failure tolerance
    - each pod gets own ip
    - loosely coupled components
  - Idea on distributed services, microservices
    - mean time to failure ..
  - History
    - Borg/Omega?
    - Paxos/Chubby?
    - https://www.researchgate.net/publication/297595470_Borg_Omega_and_Kubernetes
      "Borg, Omega, and Kubernetes" January 2016
  - Stakeholder?
    - Google, RedHat, CoreOS, Microsoft, Canonical
  - Organization of development and community
    - GitHub, Slack, SGIs
    - example: sig-livecycle, kubeadm

11:00
Session "Running Containers and Exposing Services I"
  - Minikube
    - start, dashboard, does it work?
  - Pod, ReplicaSet, Deployment
  - Services, Ingress
    - FIXME curl against ip + "from header"?
  - From `kubectl run/expose` to manifests


Hands-on
  - How to run a Docker container in Kubernetes?
  - How to access Docker containers from outside of Kubernetes?


12:00
Session "Running Containers and Exposing Services I"
  - more on labels and selectors
    - from ingress to pod

  - delete by selectors
  - namespaces
    - delete whole namespace
    - slides from thokin on namespaces?
  - [Node affinity](http://kubernetes.io/docs/user-guide/node-selection/#alpha-feature-in-kubernetes-v12-node-affinity)
  - Configmaps, Secrets
  - Daemonsets, Jobs

Hands-on
  -

13:00
Lunch

14:00
Session "Monitoring and Logging"
  - Prometheus/Grafana at first
    - explain Kubernetes discovery addon
    - show some Grafana dashboards
    - FIXME add more templates to dashboards for drill down
      maybe https://github.com/jimmidyson/prometheus-grafana-dashboards
    - explain Job to configure Grafana here
    - explain labels
      - docker/cadvisor/kubernetes
  - FIXME find demo app like "Thux" but without the need of personal api-keys.
    maybe a crawler for news sites that collects the titles of articles to create a word cloud?

15:00
Session "Rolling Updates, multiple Environments"
  - TBD

16:00
Session "Storage and Outlook"

  - Roadmap
    - Current alpha/beta features
    - kubeadm

  - Reuse/Community
    - Helm

  - Storage
    - PetSets
    - StorageClass

  - Security
    - RBAC and restricting access
      https://github.com/TremoloSecurity/wiki/blob/master/kubernetes.md
    - Automated builds on Docker Hub
    - Quay/Clair
    - Vault?

  - Scaling
    - some real numbers?
      - bottlenecks? etcd2?
    - Federation

  - Alternatives
    - Openshift
    - Mesos/Mesosphere
    - Rancher
    - Docker/rkt/systemd-nspawn
      https://tectonic.com/blog/minikube-and-rkt.html
    - CoreOS/Atomic/Ubuntu Core/Rancher OS
