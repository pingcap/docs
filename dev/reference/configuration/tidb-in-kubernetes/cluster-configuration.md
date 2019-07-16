---
title: TiDB Cluster Configuration on Kubernetes
summary: Learn the configuration of TiDB cluster on Kubernetes.
category: reference
---

# TiDB Cluster Configuration in Kubernetes

This document introduces the following items of a TiDB cluster in Kubernetes:

+ The parameters for configuration
+ The configuration of resources
+ The configuration of disaster recovery

## Parameters for configuration

TiDB Operator deploys and manages TiDB clusters using Helm. The configuration items for the deployment of TiDB cluster are listed in the table below.

The `charts/tidb-cluster/values.yaml` file of `tidb-cluster` provides the basic configuration by default with which you could quickly start a TiDB cluster. However, if you need special configuration or are deploying in a production environment, you need to manually configure the corresponding parameters according to the table below.

> **Note:**
>
> In the following table, `values.yaml` refers to `charts/tidb-cluster/values.yaml`.

| Parameter | Description | Default Value |
| :----- | :---- | :----- |
| `rbac.create` | Whether to enable the RBAC of Kubernetes | `true` |
| `clusterName` | TiDB cluster name. This variable is unset by default. `tidb-cluster` directly replaces this parameter with `RealeaseName` when the cluster is being installed. | `nil` |
| `extraLabels` | The custom labels attached to TiDB cluster. See: [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) | `{}` |
| `schedulerName` | The scheduler used by TiDB cluster | `tidb-scheduler` |
| `timezone` | The default timezone used by TiDB cluster | `UTC` |
| `pvReclaimPolicy` | The reclaim policy for PV (Persistent Volume) used by TiDB cluster | `Retain` |
| `services[0].name` | The name of the service that TiDB cluster exposes | `nil` |
| `services[0].type` | The type of service that TiDB cluster exposes (selected from `ClusterIP`, `NodePort` and `LoadBalancer`) | `nil` |
| `discovery.image` | The image of PD's Service Discovery Component in a TiDB cluster. This component is used to provide service discovery for each PD instance to coordinate the starting sequence when the PD cluster is started for the first time. | `pingcap/tidb-operator:v1.0.0-beta.3` |
| `discovery.imagePullPolicy` | The pulling policy for the image of PD's Service Discovery Component | `IfNotPresent` |
| `discovery.resoureces.limits.cpu` | The limit of the image of PD's Service Discovery Component on CPU resource | `250m` |
| `discovery.resoureces.limits.memory` | The limit of the image of PD's Service Discovery Component on memory resource  | `150Mi` |
| `discovery.resoureces.requests.cpu` | The image of PD's Service Discovery Component's request for CPU resource  | `80m` |
| `discovery.resoureces.requests.memory` | The image of PD's Service Discovery Component's request for memory resource | `50Mi` |
| `enableConfigMapRollout` | Whether to enable the automatic rolling update of TiDB cluster. If enabled, TiDB cluster automatically updates the corresponding components when the `ConfigMap` of this cluster changes. This configuration is only supported in `tidb-operator` v1.0 and later versions. | `false` |
| `pd.config` | The configuration of PD. Check [this link](https://github.com/pingcap/pd/blob/master/conf/config.toml) for the file of the default PD configuration (by choosing the tag of the corresponding PD version). You can see [this document](https://pingcap.com/docs-cn/v3.0/reference/configuration/pd-server/configuration-file/) for the detailed description of the configuration parameters (by choosing the corresponding document version). Here you only need to **modify the configuration based on the format of the configuration file**.  | If the version of TiDB Operator is v1.0.0-beta.3 or earlier, the default value is <br>`nil`<br>If the version of TiDB Operator is later than v1.0.0-beta.3, the default value is <br>`[log]`<br>`level = "info"`<br>`[replication]`<br>`location-labels = ["region", "zone", "rack", "host"]`.<br>Example of configuration:<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`[log]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`level = "info"`<br>&nbsp;&nbsp;&nbsp;&nbsp;`[replication]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`location-labels = ["region", "zone", "rack", "host"]` |
| `pd.replicas` | The number of Pods in PD | `3` |
| `pd.image` | PD image | `pingcap/pd:v3.0.0-rc.1` |
| `pd.imagePullPolicy` | The pulling policy for PD image | `IfNotPresent` |
| `pd.logLevel` | The log level of PD<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure the parameter via `pd.config`: <br>`[log]`<br>`level = "info"` | `info` |
| `pd.storageClassName` | The `storageClass` used by PD. `storageClassName` refers to a type of storage provided by the Kubernetes cluster, which might map to a level of service quality, a backup policy, or to any policy determined by the cluster administrator. Detailed reference: [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `pd.maxStoreDownTime` | This parameter indicates how soon a store node is marked as `down` after it is disconnected. When the state changes to `down`, the store node starts migrating data to other store nodes.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `pd.config`:<br>`[schedule]`<br>`max-store-down-time = "30m"`  | `30m` |
| `pd.maxReplicas` | The number of data replica in the TiDB cluster<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `pd.config`:<br>`[replication]`<br>`max-replicas = 3` | `3` |
| `pd.resources.limits.cpu` | The limit on CPU resource per PD Pod | `nil` |
| `pd.resources.limits.memory` | The limit on memory resource per PD Pod | `nil` |
| `pd.resources.limits.storage` | The limit on storage per PD Pod | `nil` |
| `pd.resources.requests.cpu` | Each PD Pod's request for CPU resource | `nil` |
| `pd.resources.requests.memory` | Each PD Pod's request for memory resource | `nil` |
| `pd.resources.requests.storage` | Each PD Pod's request for storage | `1Gi` |
| `pd.affinity` | This parameter defines PD's scheduling rules and preferences. Detailed reference: [affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |
| `pd.nodeSelector` | This parameter ensures that PD Pods are only scheduled to the node with specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `pd.tolerations` | This parameter applies to PD Pods, allowing PD Pods to be scheduled to the nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `pd.annotations` | This parameter adds a specific `annotations` for PD Pods. | `{}` |
| `tikv.config` | The configuration of TiKV. Check [this link](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) for the file of the default TiKV configuration (by choosing the tag of the corresponding TiKV version). You can see [this document](https://pingcap.com/docs-cn/v3.0/reference/configuration/tikv-server/configuration-file/) for the detailed description of the configuration parameters (by choosing the corresponding document version). Here you only need to **modify the configuration based on the format of the configuration file**. | If the version of TiDB Operator is v1.0.0-beta.3 or ealier, the default value is<br>`nil`<br>If the version of TiDB Operator is later than v1.0.0-beta.3, the default value is<br>`log-level = "info"`<br>Example of configuration:<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`log-level = "info"` |
| `tikv.replicas` | The number of Pods in TiKV | `3` |
| `tikv.image` | TiKV image | `pingcap/tikv:v3.0.0-rc.1` |
| `tikv.imagePullPolicy` | The pulling policy for TiKV image | `IfNotPresent` |
| `tikv.logLevel` | The level of TiKV logs<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`log-level = "info"` | `info` |
| `tikv.storageClassName` | The `storageClass` used by TiKV. `storageClassName` refers to a type of storage provided by the Kubernetes cluster, which might map to a level of service quality, a backup policy, or to any policy determined by the cluster administrator. Detailed reference: [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `tikv.syncLog` | `SyncLog` means whether to enable the raft log synchronization. Enabling this feature ensures that data will not be lost when power is off.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[raftstore]`<br>`sync-log = true`  | `true` |
| `tikv.grpcConcurrency` | This parameter configures the thread pool size of the gRPC server.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[server]`<br>`grpc-concurrency = 4` | `4` |
| `tikv.resources.limits.cpu` | The limit on CPU resource per TiKV Pod | `nil` |
| `tikv.resources.limits.memory` | The limit on memory resource per TiKV Pod | `nil` |
| `tikv.resources.limits.storage` | The limit on storage per TiKV Pod | `nil` |
| `tikv.resources.requests.cpu` | Each TiKV Pod's request for CPU resource | `nil` |
| `tikv.resources.requests.memory` | Each TiKV Pod's request for memory resource | `nil` |
| `tikv.resources.requests.storage` | Each TiKV Pod's request for storage | `10Gi` |
| `tikv.affinity` | This parameter defines TiKV's scheduling rules and preferences. Detailed reference:[affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |
| `tikv.nodeSelector` | This parameter ensures that TiKV Pods are only scheduled to the node with specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tikv.tolerations` | This parameter applies to TiKV Pods, allowing TiKV Pods to be scheduled to the nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `tikv.annotations` | This parameter adds a specific `annotations` for TiKV Pods. | `{}` |
| `tikv.storeLabels` | The labels that specifies the information of TiKV location. PD schedules the copy of the TiKV data based on these labels, the priority of which is decremented in the order of these labels themselves. For example, `["zone","rack"]` means that data copies are preferentially scheduled to TiKV on different `zone`. If the number of `zone` is not enough, these data copies are scheduled to TiKV on different `rack`. If this parameter is not specified, the system sets `["region", "zone", "rack", "host"]` as the default values. The premise that these labels take effect is that they are also included in the Kubernetes Nodes. Note that the lable name is currently not supported to include `/`. | `nil` |
| `tikv.defaultcfBlockCacheSize` | This parameter specifies the size of block cache which is used to cache uncompressed blocks. Larger block cache settings speed up reads. It is recommended to set the parameter to 30%-50% of the value of `tikv.resources.limits.memory`.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[rocksdb.defaultcf]`<br>`block-cache-size = "1GB"`<br>From TiKV v3.0.0 on, you do not need to configure  `[rocksdb.defaultcf].block-cache-size` and `[rocksdb.writecf].block-cache-size`. Instead, configure `[storage.block-cache].capacity`.   | `1GB` |
| `tikv.writecfBlockCacheSize` | The parameter specifies the size of writecf block cache. It is recommended to set the parameter to 10%-30% of the value of `tikv.resources.limits.memory`.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[rocksdb.writecf]`<br>`block-cache-size = "256MB"`<br>From TiKV v3.0.0 on, you do not need to configure `[rocksdb.defaultcf].block-cache-size` and `[rocksdb.writecf].block-cache-size`. Instead, configure `[storage.block-cache].capacity`.   | `256MB` |
| `tikv.readpoolStorageConcurrency` | The size of thread pool for high priority, normal priority or low priority operations in the TiKV storage<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[readpool.storage]`<br>`high-concurrency = 4`<br>`normal-concurrency = 4`<br>`low-concurrency = 4` | `4` |
| `tikv.readpoolCoprocessorConcurrency` | If `tikv.resources.limits.cpu` is greater than `8`, set the value of `tikv.readpoolCoprocessorConcurrency` to `tikv.resources.limits.cpu` * 0.8<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[readpool.coprocessor]`<br>`high-concurrency = 8`<br>`normal-concurrency = 8`<br>`low-concurrency = 8`  | `8` |
| `tikv.storageSchedulerWorkerPoolSize` | The worker pool size of TiKV scheduler. This size must be increased in the case of rewriting but be smaller than the total CPU core.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tikv.config`:<br>`[storage]`<br>`scheduler-worker-pool-size = 4`  | `4` |
| `tidb.config` | The configuration of TiDB. Check [this link](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) for the file of the default TiDB configuration (by choosing the tag of the corresponding TiDB version). You can see [this document](https://pingcap.com/docs-cn/v3.0/reference/configuration/tidb-server/configuration-file/) for the detailed description of the configuration parameters (by choosing the corresponding document version). Here you only need to **modify the configuration based on the format of the configuration file**.  | If the version of TiDB Operator is v1.0.0-beta.3 or ealier, the default value is<br>`nil`<br>If the version of TiDB Operator is later than v1.0.0-beta.3, the default value is<br>`[log]`<br>`level = "info"`<br>Example of configuration:<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`[log]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`level = "info"` |
| `tidb.replicas` | The number of Pods in TiDB | `2` |
| `tidb.image` | TiDB image | `pingcap/tidb:v3.0.0-rc.1` |
| `tidb.imagePullPolicy` | The pulling policy for TiDB image | `IfNotPresent` |
| `tidb.logLevel` | The level of TiDB logs<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[log]`<br>`level = "info"`  | `info` |
| `tidb.resources.limits.cpu` | The limit on CPU resource per TiDB Pod | `nil` |
| `tidb.resources.limits.memory` | The limit on memory resource per TiDB Pod | `nil` |
| `tidb.resources.requests.cpu` | Each TiDB Pod's request for CPU resource | `nil` |
| `tidb.resources.requests.memory` | Each TiDB Pod's request for memory resource | `nil` |
| `tidb.passwordSecretName`| The name of the `Secret` that stores the TiDB username and password. The `Secret` can create a secret with this command: `kubectl create secret generic tidb secret--from literal=root=<root password>--namespace=<namespace>`. If the parameter is unset, TiDB root password is empty. | `nil` |
| `tidb.initSql`| The initialization script that will be executed after a TiDB cluster is successfully started. | `nil` |
| `tidb.affinity` | This parameter defines TiDB's scheduling rules and preferences. Detailed reference: [affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |
| `tidb.nodeSelector` | This parameter ensures that TiDB Pods are only scheduled to the node with specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tidb.tolerations` | This parameter applies to TiDB Pods, allowing TiDB Pods to be scheduled to nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `tidb.annotations` | This parameter adds a specific `annotations` for TiDB Pods. | `{}` |
| `tidb.maxFailoverCount` | The maximum number of failovers for TiDB. Assuming the number is `3`, that is, failovers of up to `3` TiDB instances are supported at the same time. | `3` |
| `tidb.service.type` | The type of service that TiDB cluster exposes | `Nodeport` |
| `tidb.service.externalTrafficPolicy` | This parameter indicates whether this Service routes external traffic to a node-local or cluster-wide endpoint. There are two options available: `Cluster`(by default) and `Local`. `Cluster` obscures the client source IP and some traffic needs to hop twice among nodes for the intended node, but with a good overall load distribution. `Local` preserves the client source IP and avoids a second hop for the LoadBalancer and `Nodeport` type services, but risks potentially imbalanced traffic distribution. Detailed reference: [External LoadBalancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip) | `nil` |
| `tidb.service.loadBalancerIP` | This parameter specifies the IP of LoadBalancer. Some cloud providers allow you to specify `loadBalancerIP`. In these cases, the LoadBalancer will be created using the user-specified `loadBalancerIP`. If the `loadBalancerIP` field is not specified, the LoadBalancer will be set using the temporary IP address. If `loadBalancerIP` is specified but the cloud provider does not support this feature, the `loadbalancerIP` field you set will be ignored.| `nil` |
| `tidb.service.mysqlNodePort` | The mysql `NodePort` that TiDB Service exposes |  |
| `tidb.service.exposeStatus` | The port that indicates the expose status of TiDB Service | `true` |
| `tidb.service.statusNodePort` | The `NodePort` exposed through specifying the status of TiDB Service |  |
| `tidb.separateSlowLog` | Whether to run in sidebar mode the `SlowLog` of TiDB exported via independent container | If the version of TiDB Operator is v1.0.0-beta.3 or ealier, the default value is `false`.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, the default value is `true`.  |
| `tidb.slowLogTailer.image` | The image of TiDB's `slowLogTailer`. `slowLogTailer` is a container of sidecar type, used to export the `SlowLog` of TiDB. This configuration only takes effect when `tidb.separateSlowLog`=`true`. | `busybox:1.26.2` |
| `tidb.slowLogTailer.resources.limits.cpu` | The limit on CPU resource per TiDB Pod's `slowLogTailer` | `100m` |
| `tidb.slowLogTailer.resources.limits.memory` | The limit on memory resource per TiDB Pod's `slowLogTailer` | `50Mi` |
| `tidb.slowLogTailer.resources.requests.cpu` | The request of each TiDB Pod's `slowLogTailer` for CPU resource | `20m` |
| `tidb.slowLogTailer.resources.requests.memory` | The request of each TiDB Pod's `slowLogTailer` for memory resource | `5Mi` |
| `tidb.plugin.enable` | Whether to enable TiDB plugin | `false` |
| `tidb.plugin.directory` | This parameter specifies the directory where the TiDB plugin is located. | `/plugins` |
| `tidb.plugin.list` | This parameter specifies a list of plugins loaded on TiDB. The naming rules of Plugin ID: plugin name-version. For example: 'conn_limit-1'. | `[]` |
| `tidb.preparedPlanCacheEnabled` | Whether to enable TiDB's prepared plan cache<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[prepared-plan-cache]`<br>`enabled = false` | `false` |
| `tidb.preparedPlanCacheCapacity` | The cache capacity of TiDB's prepared plan<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[prepared-plan-cache]`<br>`capacity = 100`  | `100` |
| `tidb.txnLocalLatchesEnabled` | Whether to enable the memory lock for transaction. It is recommended to enable the lock when there are many conflicts among local transactions.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[txn-local-latches]`<br>`enabled = false` | `false` |
| `tidb.txnLocalLatchesCapacity` |  The capacity of the local latch of a transaction<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[txn-local-latches]`<br>`capacity = 10240000` | `10240000` |
| `tidb.tokenLimit` | The restrictions on TiDB to execute concurrent sessions<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`token-limit = 1000` | `1000` |
| `tidb.memQuotaQuery` | The memory quota for TiDB queries, which is 32GB by default.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`mem-quota-query = 34359738368` | `34359738368` |
| `tidb.txnEntryCountLimit` | The limit on the number of entries in a transaction. If TiKV is used as the storage, the entry represents a key-value pair. **Warning:** Do not set this value too large. Otherwise, it might have a big impact on the TiKV cluster. Set this parameter carefully.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[performance]`<br>`txn-entry-count-limit = 300000` | `300000` |
| `tidb.txnTotalSizeLimit` | The limit on byte size for each entry in a transaction. If TiKV is used as the storage, the entry represents a key-value pair. **Warning:** Do not set this value too large. Otherwise, it might have a big impact on the TiKV cluster. Set this parameter carefully.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[performance]`<br>`txn-total-size-limit = 104857600` | `104857600` |
| `tidb.enableBatchDml` | This parameter enables batch submission for DML.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`enable-batch-dml = false` | `false` |
| `tidb.checkMb4ValueInUtf8` | This parameter is used to control whether to check the `mb4` characters when the character set is `utf8`.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`check-mb4-value-in-utf8 = true` | `true` |
| `tidb.treatOldVersionUtf8AsUtf8mb4` | This parameter is used for upgrading compatibility. After it is set to `true`, `utf8` character set in the old table is treated as `utf8mb4`.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`treat-old-version-utf8-as-utf8mb4 = true` | `true` |
| `tidb.lease` | The lease time of TiDB Schema lease. It is highly risky to change this parameter. Therefore, it is not recommended to do so unless you know exactly what might be happening.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`lease = "45s"`  | `45s` |
| `tidb.maxProcs` | The maximum available CPU cores. `0` represents the number of CPU on the machine or Pod.<br>If the version of TiDB Operator is later than v1.0.0-beta.3, you can configure this parameter via `tidb.config`:<br>`[performance]`<br>`max-procs = 0` | `0` |

## Description of resource configuration

Before deploying a TiDB cluster, it is necessary to configure the resource for each components of the cluster according to actual needs. `requests` and `limits` are the resource configuration items listed in the table above. They respectively refer to the minimum requirement for and maximum limit on resources. `limits` must be greater than or equal to `request`. It is recommended to set `limits` to be greater than or equal to `requests`, which ensures that the service achieves Guaranteed-level QoS.

PD, TiKV and TiDB are the core service components of a TiDB cluster. In a production environment, their resource configuration must be made manually according to component needs. Detailed reference: [Hardware Recommendations](dev/how-to/deploy/hardware-recommendations.md). In a testing environment, you can directly use the default configuration in the `values.yaml` file without any manual setting.

## Description of configuration for disaster recovery

TiDB is a distributed database. Its disaster recovery must ensure that when any physical topology node fails, not only the service is unaffected, but also the data is complete and available. The two configurations of disaster recovery are specified separately as follows.

### The disaster recovery of TiDB service

The disaster recovery of TiDB service is essentially based on Kubernetes' scheduling capabilities. To optimize scheduling, TiDB Operator provides a custom scheduler that guarantees the disaster recovery of the TiDB service at the host level through the specified scheduling algorithm. Currently, TiDB Cluster uses this scheduler as the default scheduler which is configured through the item `schedulerName` in the above table.

Disaster recovery at other levels (such as rack, zone, region) are guaranteed by Affinity's `PodAntiAffinity`. Through `PodAntiAffinity`, you can try to avoid the situation where different instances of the same component are deployed on the same physical topology node. In this way, disaster recovery is achieved. Detailed user guide for Affinity: [Affinity & AntiAffinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity).

The following is an example of a typical disaster recovery setup:

{{< copyable "shell-regular" >}}

```shell
affinity:
 podAntiAffinity:
   preferredDuringSchedulingIgnoredDuringExecution:
   # this term work when the nodes have the label named region
   - weight: 10
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "region"
       namespaces:
       - <helm namespace>
   # this term work when the nodes have the label named zone
   - weight: 20
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "zone"
       namespaces:
       - <helm namespace>
   # this term work when the nodes have the label named rack
   - weight: 40
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "rack"
       namespaces:
       - <helm namespace>
   # this term work when the nodes have the label named kubernetes.io/hostname
   - weight: 80
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "kubernetes.io/hostname"
       namespaces:
       - <helm namespace>
```

### The disaster recovery of data

The disaster recovery of data is guaranteed by the TiDB cluster's own data scheduling algorithm. TiDB Operator only needs to collect topology information from the nodes where TiKV is running and call PD interface to set this information as the information of TiKV store labels. In this way, the TiDB cluster can schedule data copies based on this information.

Currently, TiDB Operator only identifies a specific number of labels. Therefore, you need to use the following labels to set the topology information of a node:

* `region`: The Region where a node is located
* `zone`: The zone where a node is located
* `rack`: The rack where a node is located
* `kubernetes.io/hostname`: The host name of a node

You can label a node with the following command:

{{< copyable "shell-regular" >}}

```shell
$ kubectl label node <nodeName> region=<regionName> zone=<zoneName> rack=<rackName> kubernetes.io/hostname=<hostName>
```

The labels in the above command are not to be set all at once. Instead, they are to be selected according to actual situation.
