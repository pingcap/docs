---
title: TiDB Binlog Drainer Configurations in Kubernetes
summary: Learn the configurations of a TiDB Binlog Drainer in Kubernetes.
category: reference
---

# TiDB Binlog Drainer Configurations in Kubernetes

This document introduces the configuration parameters of a TiDB Binlog drainer in Kubernetes.

## Configuration parameters

The following table contains all the available configuration parameters of the `tidb-drainer` chart, refer to [use helm](tidb-in-kubernetes/reference/tools/in-kubernetes.md#use-helm) to learn how to configure these parameters.

| Parameter | Description | Default Value |
| :----- | :---- | :----- |
| `clusterName` | The name of source TiDB cluster | `demo` |
| `clusterVersion` | The version of source TiDB cluster | `v3.0.1` |
| `baseImage` | The base image of TiDB Binlog | `pingcap/tidb-binlog` |
| `imagePullPolicy` | The pulling policy of the image | `IfNotPresent` |
| `logLevel` | The log level of drainer process | `info` |
| `storageClassName` | The `storageClass` used by drainer. `storageClassName` refers to a type of storage provided by the Kubernetes cluster, which might map to a level of service quality, a backup policy, or to any policy determined by the cluster administrator. Detailed reference: [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `storage` | The storage limit of drainer Pod, note that you should set larger size if the `db-type` is set to `pb` | `10Gi` |
| `disableDetect` |  Whether disable the casuality detection | `false` |
| `initialCommitTs` |  Used to initial checkpoint ff the drainer does not have any checkpoint | `0` |
| `config` | The configuration file passed to drainer. Detailed reference: [drainer.toml](https://github.com/pingcap/tidb-binlog/blob/master/cmd/drainer/drainer.toml) | (see below) |
| `resources` | The resource limits and requests of the drainer pod | `{}` |
| `nodeSelector` | Ensures that drainer Pod are only scheduled to the node with the specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tolerations` | Applies to drainer Pod, allowing the Pods to be scheduled to the nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `affinity` | Defines scheduling policies and preferences of the drainer Pod. Detailed reference:[affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |

The default value of `config` is:

```toml
[syncer]
worker-count = 16
detect-interval = 10
disable-dispatch = false
ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"
safe-mode = false
txn-batch = 20
db-type = "pb"
[syncer.to]
dir = "/data/pb"
compression = "gzip"
```