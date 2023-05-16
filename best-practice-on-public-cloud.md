---
title: Best Practice On Public Cloud
summary: This document introduces the best practice for TiDB to deploy on public cloud
---

# Introduction

Public cloud has become an increasingly popular option for deploying and managing databases, offering a range of benefits such as flexibility, scalability, and ease of management. However, deploying TiDB on the cloud requires careful consideration of several factors, such as performance tuning, cost optimization, and reliability. This document will cover various topics such as dedicated disk for raft-engine, cost optimization for cross-AZ traffic, and mitigation of GCP live migration event. By following these best practices, you can ensure that your TiDB deployment on public cloud is optimized for performance, cost, and reliability.

# Improve the TiKV Write Performance and Stability

## Dedicated Disk for Raft-Engine
As with traditional databases, the raft-engine in TiKV plays a critical role similar to that of a write-ahead log (WAL). When deploying TiDB on a public cloud, it is important to ensure that the Raft engine has a dedicated disk to achieve optimal performance and stability. Different cloud providers offer different types of disks with varying performance characteristics, such as IOPS and MBPS. Therefore, it is important to choose the appropriate disk type and size based on the workload and the cloud provider being used.

### middle range disk
- On AWS, it is recommended to use the gp3 volumes, it offers minimum 3000 IOPS and 125 MB/s throughput, which is usually good enough for the raft-engine.

- On GCP, The IOPS and MBPS are dependent on the disk size. 

- On Azure, The IOPS and MBPS are also dependent on the disk size.

### high range disk

- AWS: io2 volumes, disk size, IOPS and MBPS can be provisioned.
- GCP: Extreme persistent disks, disk size, IOPS and MBPS can be provisioned, it's only available on 64c+ instances
- Azure: Ultra SSD, disk size, IOPS and MBPS can be provisioned.

### Example 1, Run a social network workload on AWS
With 20GB gp3 dedicated raft-engine disk, for a write intensive social network application workload, qps is up by 17.5%, avg latency of insert statement down by 18.7%, p99 latency of insert statement down by 45.6%, and the estimated cost is increased by only 0.4%. AWS provide 3000 IOPS and 125 MBPS/s for a 20GB gp3 volume.

| Item | shared raft-engine disk|dedicated raft-engine disk| diff(%) |
| ------------- | ------------- |------------- |------------- |
| QPS (K/s)| 8.0 | 9.4 | 17.5| 
| AVG Insert Latency (ms)| 11.3 | 9.2 | -18.7 |
| P99 Insert Latency (ms)| 29.4 | 16.0 | -45.6|

### Example 2, Run TPC-C/SYSBench workload on AZure
By using a 32G ultra disk for raft-engine on Azure, 

- For sysbench oltp_read_write,  QPS up by 17.8%, avg latency is down by 15.6%.
- For TPC-C, QPS up by 27.6%, avg latency down by 23.1%

| Item | Workload | shared raft-engine disk|dedicated raft-engine disk| diff(%) |
| ------------- | ------------- | ------------- |------------- |------------- |
| QPS (K/s) | Sysbench - oltp_read_write | 60.7 | 71.5 | 17.8| 
| QPS (K/s) | TPC-C | 23.9 | 30.5 | 27.6| 
| AVG Latency (ms)| Sysbench - oltp_read_write |  4.5 | 3.8 | -15.6 |
| AVG Latency (ms)| TPC-C |  3.9 | 3.0 | -23.1 |

### Example 3, how to attach a dedicated ps-ssd disk for raft-engine on TiKV manifest

Here is a example for a cluster deployed by TiDB Operator on GCP, attach an additional disk with 512GB PD-SSD volumne, and change the `raft-engine.dir` to store raft-engine logs to this specific disk.

```
tikv:
    config: |
      [raft-engine]
        dir = "/var/lib/raft-pv-ssd/raft-engine"
        enable = true
        enable-log-recycle = true
    requests:
      storage: 4Ti
    storageClassName: pd-ssd
    storageVolumes:
    - mountPath: /var/lib/raft-pv-ssd
      name: raft-pv-ssd
      storageSize: 512Gi
```


## Reduce Compaction IO Flow
In addition to choosing the appropriate disk type and size, it is also important to tune TiKV's compaction settings to optimize performance. If the total number of compaction pending bytes grows over time and flow control is triggered, indicating that TiKV doesn't have enough resources to keep up with the foreground write flow. In this case, if the bottleneck is the IO throughput limit on the cloud disk,  increasing the compression level and reducing the IO throughput can help improve performance. For example, below config increase all the compression level of the defaultcf column family to reduce the compaction flow IO throughput.

```
[rocksdb.defaultcf]
compression-per-level = ["zstd", "zstd", "zstd", "zstd", "zstd", "zstd", "zstd"]
```

# Cost Optimization for Cross-AZ
Deploying TiDB across multiple availability zones (AZs) can lead to increased costs due to cross-AZ data transfer fees. To optimize costs, it is important to reduce cross-AZ network traffic.

One way to reduce cross-AZ read traffic is to use the [Follower Read feature](https://docs.pingcap.com/tidb/dev/follower-read), which allows TiDB prefers to select a replica in the same availability zone. This feature can be enabled setting tidb_replica_read variable to `closest-replicas` or `closest-adaptive`. 

To reduce cross-AZ write traffic For TiDB/TiKV instance, gRPC compression feature can be enabled to compress data before transmitting it across the network. Additionally, TiFlash's data exchange compression feature can also be enabled to further reduce data transmission overhead. Below is the configuration example to enable gzip grp compression type for both TiDB and TiKV.

```
server_configs:
  tidb:
    tikv-client.grpc-compression-type: gzip
  tikv:
    server.grpc-compression-type: gzip
```

To reduce network traffic caused by the data shuffle of the TiFlash MPP tasks, it's recommended to deploy multiple TiFlash instance at the same availability zones (AZs).
Since v6.6.0, TiFlash support [compression exchange](https://docs.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression) to reduce the network traffic caused by MPP data shuffle.


# Mitigation of GCP Live Migration Event
GCP's Live Migration feature allows VMs to be migrated between hosts without downtime. It's not a rarely occured maintenance event. During the event, the impacted VMs is slow performance or event instance pauses.
To mitigate the performance penalty from GCP's live migration event, TiDB provide a [watching script](https://github.com/PingCAP-QE/tidb-google-maintenance) based off of Google's own metadata [example](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/metadata/main.py). The scripts are deployed on TiDB, TiKV, and PD nodes, to detect maintenance events. During maintenance events, below appropriate actions can be taken, be noted that only TiDB Cluster deployed by [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/tidb-operator-overview) is supported:
- TiDB: Put the TiDB offline by cordon the TiDB node and delete the TiDB pod (the node pool of TiDB instance MUST be set to auto-scale, the cordon node is expected to be reclaimed by auto-scaler)
- TiKV: Ecivt leaders on TiKV store during maintenance.
- PD: Resign leader if the current PD instance is the PD leader

# Conclusion
Optimizing TiDB deployments on a public cloud involves choosing the appropriate disk type and size, tuning TiKV's compaction settings, reducing cross-AZ read and write traffic, and utilizing cloud provider-specific features such as GCP Live Migration. By following these best practices, TiDB deployments can achieve optimal performance and cost-efficiency.



