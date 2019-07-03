---
title: Access TiDB Clusters on Kubernetes
category: how-to
---

# Access TiDB Clusters on Kubernetes

To access TiDB within a Kubernetes cluster, use the TiDB service domain name `<tidbcluster-name>-tidb.<namespace>`.

To access TiDB outside a Kubernetes cluster, you need to expose TiDB service port. To do that, make the following configuration via the `tidb.service` field in the `values.yaml` file in the tidb-cluster Helm chart.

{{< copyable "" >}}

```yaml
tidb:
  service:
    type: NodePort
    # externalTrafficPolicy: Cluster
    # annotations:
    # cloud.google.com/load-balancer-type: Internal
```

## NodePort

Without LoadBalancer, you could expose TiDB service port in the following 2 modes of NodePort:

- `externalTrafficPolicy=Cluster`: All machines in the Kubernetes cluster assign a NodePort to TiDB Pod, which is the default mode.
- `externalTrafficPolicy=Local`: Only those machines running TiDB assign NodePort to TiDB Pod so that you could access local TiDB instances.

    When the `Local` mode is in use, it is recommended to enable the `StableScheduling` feature of tidb-scheduler. Tidb-scheduler tries to schedule the newly added TiDB instances to the existing machines during the upgrade process. With such scheduling, client outside Kubernetes cluster does not need to upgrade configuration after TiDB is restarted.

### See the IP/PORT exposed in NodePort mode

To see the Node Port assigned by Service, use the following commands to obtain the Service object of TiDB:

{{< copyable "shell-regular" >}}

```shell
namespace=<your-tidb-namesapce>
```

{{< copyable "shell-regular" >}}

```shell
release=<your-tidb-release-name>
```

{{< copyable "shell-regular" >}}

```shell
kubectl -n ${namespace} get svc ${release}-tidb -ojsonpath="{.spec.ports[?(@.name=='mysql-client')].nodePort}{'\n'}"
```

You might encounter the following two situations when seeing which nodes' IP can access TiDB service:

- When `externalTrafficPolicy` is configured as `Cluster`, IPs of all nodes can access TiDB.
- When `externalTrafficPolicy` is configured as `Local`, use the following commands to obtain the nodes on which the TiDB instance of the specified cluster is located:

    {{< copyable "shell-regular" >}}

    ```shell
    release=<your-tidb-release-name>
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl -n stability-cluster1 get pods -l "app.kubernetes.io/component=tidb,app.kubernetes.io/instance=${release}" -ojsonpath="{range .items[*]}{.spec.nodeName}{'\n'}{end}"
    ```

## LoadBalancer

If Kubernetes is run in an environment with LoadBalancer, such as GCP/AWS platform, it is recommended to enable the LoadBalancer feature of these cloud platforms.

See [Kubernetes Service Documentation](https://kubernetes.io/docs/concepts/services-networking/service/) to know more about the features of Service and what LoadBalancer in the cloud platform supports.