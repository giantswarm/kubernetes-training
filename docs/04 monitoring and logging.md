# Monitoring and Logging Demo

## Prometheus & Grafana for Monitoring

[Prometheus](https://prometheus.io/) is an open-source monitoring solution that includes the gathering of metrics, their storage in an internal time series database as well as querying and alerting based on that data.

It is part of the CNCF and offers a lot of integrations incl. Docker, Kubernetes, etc. and is the leading solution in practice in the ecosystem.

Prometheus can also visualize your data. However, we include another open-source tool, [Grafana](http://grafana.org/), for the visualization part, as it offers a more powerful and flexible way to generate visuals and dashboards.

![Grafana Screenshot](img/grafana_cluster_overview.png)

## Elastic Stack for Logging

The Elastic stack is most prominently know in form of the ELK stack. Here we use the more recent combination of Filebeat, Elasticsearch, and Kibana.

This stack helps you get all logs from your containers into a single searchable data store without having to worry about logs disappearing together with the containers.

With Kibana you get a nice analytics and visualization platform on top.

![Kibana Screenshot](img/kibana.png)

## Twitter Hot URLs Example with Custom Metrics

This Microservices example consists of multiple components working hand in hand but decoupled to collect URLs mentioned on Twitter to create a hotlist of popular URLs.

![THUX Components Overview](img/thux-overview.png)

It offers a prometheus compatible metrics endpoint for custom metrics, which could be used to implement auto-scaling of the resolver workers.