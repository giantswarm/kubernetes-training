# Overview

Kubernetes is a platform for managing distributed applications based on the microservices architecture.

## Excourse Distributed Systems & Microservices

### Microservices are ..

> In microservice architectures, applications are built and deployed as simple, highly decoupled, focussed services. They connect to each other over lightweight language agnostic communication mechanisms, which often times means simple HTTP APIs and message queues. Services are built around business capabilities and independently changeable and deployable with only a bare minimum of centralized management. They are polyglot in terms of programming languages, frameworks, and data stores used. Lastly, microservices are resilient, which means they are immutable artifacts that are designed to fail and elastic in scale.

### Core Ideas

- Decoupled Services
- Lightweight Communication
- Polyglot
- Resilience
    - Designed To Fail
    - Elastic in Scale

### Designed To Fail

Availabiliy = MTBF / (MTBF + MTTR)

Focus on minimizing MTTR instead of MTBF

### Further Reading

- [Introduction to Microservice Architectures](https://giantswarm.io/microservices/)
- [The 12-Factor App](https://12factor.net/)

## Architecture

### Kubernetes consists of 5 main components

3 Master Components
- Apiserver
  http://kubernetes.io/docs/admin/kube-apiserver/
- kube-controller-manager
  http://kubernetes.io/docs/admin/kube-controller-manager/
  replication controller, endpoints controller, namespace controller, and serviceaccounts controller.
- kube-scheduler
  http://kubernetes.io/docs/admin/kube-scheduler/

2 Worker/Node Components    
- kube-proxy
  http://kubernetes.io/docs/admin/kube-proxy/
- kubelet
  http://kubernetes.io/docs/admin/kubelet/


Idea: declarative state is constantly compared to running state.


### Reference
- [What is Kubernetes?](http://kubernetes.io/docs/whatisk8s/)
- [Design Principles](https://github.com/kubernetes/kubernetes/blob/master/docs/design/principles.md)
- [Kubernetes Design Overview](https://github.com/kubernetes/kubernetes/blob/master/docs/design/README.md)
- [Kubernetes architecture](https://github.com/kubernetes/kubernetes/blob/master/docs/design/architecture.md)

## Features

FIXME! what do we cover during this workshop?

Feature list as of Kubernetes v1.4 from the [official documentation](http://kubernetes.io/docs/whatisk8s/):
- co-locating helper processes, facilitating composite applications and preserving the one-application-per-container model,
- mounting storage systems,
- distributing secrets,
- application health checking,
- replicating application instances,
- horizontal auto-scaling,
- naming and discovery,
- load balancing,
- rolling updates,
- resource monitoring,
- log access and ingestion,
- support for introspection and debugging, and
- identity and authorization.



## History

- Borg/Omega?
- Paxos/Chubby?
- https://www.researchgate.net/publication/297595470_Borg_Omega_and_Kubernetes
  "Borg, Omega, and Kubernetes" January 2016

## Community

https://github.com/kubernetes/kubernetes

~900 Contributors
from Google, Red Hat, Microsoft, CoreOS, Mesosphere

Release Cycle: about every [three months](https://github.com/kubernetes/features/blob/master/release-1.5/release-1.5.md)

Runs on [RaspberryPi](https://github.com/luxas/kubernetes-on-arm)

## Main reasons

- primitives
- community
- no lock-in
