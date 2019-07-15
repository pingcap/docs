---
title: Automatic Failover Policies of TiDB Cluster Components on Kubernetes
summary: Learn the automatic failover policies of TiDB cluster components on Kubernetes.
category: how-to
---

# Automatic Failover Policies of TiDB Cluster Components on Kubernetes

Automatic failover means that when some nodes in the TiDB cluster fail, TiDB Operator automatically adds a new node to ensure the high availability of the cluster like the `deployment` behavior that happens in Kubernetes.

TiDB Operator manages Pods based on `StatefulSet`, but `StatefulSet` does not automatically create a new node to replace the original node when some Pod goes down. For this reason, TiDB Operator develops the automatic failover feature and expands the behavior of `StatefulSet`.

The automatic failover feature is disabled by default in TiDB Operator. You can enable it by setting `controllerManager.autoFailover` to `true` in the `charts/tidb-operator/values.yaml` file when deploying TiDB Operator:

```yaml
controllerManager:
 serviceAccount: tidb-controller-manager
 logLevel: 2
 replicas: 1
 resources:
   limits:
     cpu: 250m
     memory: 150Mi
   requests:
     cpu: 80m
     memory: 50Mi
 # autoFailover is whether tidb-operator should auto failover when failure occurs
 autoFailover: true
 # pd failover period default(5m)
 pdFailoverPeriod: 5m
 # tikv failover period default(5m)
 tikvFailoverPeriod: 5m
 # tidb failover period default(5m)
 tidbFailoverPeriod: 5m
```

By default, `pdFailoverPeriod`, `tikvFailoverPeriod` and `tidbFailoverPeriod` are set to be 5 minutes, which is the waiting timeout after confirming the instance failure. After this time, TiDB Operator begins the automatic failover process.

## Implementation principles

There are three components in a TiDB cluster - PD, TiKV and TiDB, each of which has its own automatic failover policy. This section gives an in-depth introduction to the three policies.

### PD automatic failover policy

Assume that there are 3 nodes in a PD cluster, and if a PD node is down over 5 minutes (configurable by modifying `tidbFailoverPeriod`), TiDB Operator makes this node go offline first, and creates a new PD node. At this time, there are 4 Pods existing in the cluster. After the failed PD node gets back to normal, TiDB Operator deletes the newly created node and the number of nodes gets back to 3.

### TiKV automatic failover policy

When a TiKV node fails, its status turns to `Disconnected`. After 30 minutes (configurable by modifying `pd.maxStoreDownTime` when deploying the cluster), it turns to `Down`. After waiting for 5 minutes (configurable by modifying `tikvFailoverPeriod`), TiDB Operator creates a new TiKV node if this TiKV node is still down. When the failed TiKV node gets back to normal, TiDB Operator does not automatically delete the newly created node, and you need to manually drop it and make the number of nodes the same as before. To do that, you can delete the TiKV node from the `status.tikv.failureStores` field of the `TidbCluster` object:

{{< copyable "shell-regular" >}}

```shell
kubectl edit tc -n <namespace> <clusterName>
```

```
...
status
  tikv:
    failureStores:
      "1":
        podName: cluster1-tikv-0
        storeID: "1"
      "2":
        podName: cluster1-tikv-1
        storeID: "2"
...
```

After the `cluster1-tikv-0` node turns back to normal, you can delete it as shown below:

```
...
status
  tikv:
    failureStores:
      "2":
        podName: cluster1-tikv-1
        storeID: "2"
...
```

### TiDB automatic failover policy

When there are 3 nodes in a TiDB cluster, the TiDB automatic failover policy is the same as the `deployment` behavior in Kubernetes. If a TiDB node is down over 5 minutes (configurable by modifying `tidbFailoverPeriod`), TiDB Operator creates a new TiDB node. At this time, there are 4 Pods existing in the cluster. When the failed TiDB node gets back to normal, TiDB Operator deletes the newly created node and the number of nodes gets back to 3.
