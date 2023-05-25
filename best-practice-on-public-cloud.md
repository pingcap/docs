---
title: Best Practice On Public Cloud
summary: This document introduces the best practice for TiDB to deploy on public cloud
---

# Introduction

Public cloud infrastructure has gained significant popularity as a preferred choice for deploying and managing TiDB. However, deploying TiDB on the cloud requires careful consideration of several factors, such as performance tuning, cost optimization, reliability and scability. This document will cover various topics such as dedicated disk for Raft-Engine, IO throughput limitation, cost optimization for cross-AZ traffic, mitigation of GCP live migration event and PD server tuning on a large cluster. By following these best practices, you can ensure that your TiDB deployment on public cloud is optimized for performance, cost, reliability and scability.

# Improve the TiKV Write Performance and Stability

## Dedicated Disk for Raft-Engine
As with traditional databases, the Raft-Engine in TiKV plays a critical role similar to that of a write-ahead log (WAL). When deploying TiDB on a public cloud, it is important to ensure that the Raft engine has a dedicated disk to achieve optimal performance and stability. Below `iostat` shows the IO character on a TiKV node with write heavy workload.

```
Device            r/s     rkB/s       w/s     wkB/s      f/s  aqu-sz  %util
sdb           1649.00 209030.67   1293.33 304644.00    13.33    5.09  48.37
sdd           1033.00   4132.00   1141.33  31685.33   571.00    0.94 100.00
```

Device sdb is for KV RocksDB; sdd is to restore Raft-Engine log. There is much higher `f/s` for sdd, `f/s` means the number of flush requests completed per second for the device. For Raft-Engine, when one write in a batch is marked synchronous, the batch leader will call fdatasync() after writing. This way, buffered data is guaranteed to be flushed out onto the storage. By deploying a dedicated volume for Raft-Engine, TiKV is able to reduce the the average queue length of the requests and make sure the write latency is optimal and stable.

Different cloud providers offer different types of disks with varying performance characteristics, such as IOPS and MBPS. Therefore, it is important to choose the appropriate disk type and size based on the workload and the cloud provider being used.

### Chose proper disk for Raft-Engine on different public cloud

This section covers best practices for choosing proper disks for Raft-Engine on different public clouds. Depending on performance requirements, two types of recommended disks are available on different public clouds.

#### Middle Range Disk
For middle-range disks, the following recommendations are suggested for different public clouds:

- On AWS, it is recommended to use [gp3](https://aws.amazon.com/ebs/general-purpose/) volumes. These volumes offer free 3000 IOPS and 125 MB/s throughput, regardless of the volume size allocated. This is usually sufficient for the Raft-Engine.

- On GCP, it is recommended to use [pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/) volumes. The IOPS and MBPS are dependent on the disk size allocated. To meet the performance requirement, it's recommended to allocate 200GB space for Raft-Engine. Although, Raft-Engine doesn't need this large space, it can provide the necessary performance.

- On Azure, it is recommended to use  [Premium SSD v2](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#premium-ssd-v2) volumes. Similar to AWS, it provides free 3000 IOPS and 125 MB/s throughput regardless of volume size allocated, which is usually sufficient for Raft-Engine.

#### High End Disk
If even lower latency is required for Raft-Engine, high-end disks are available. Here are the recommendations for different public clouds:

- On AWS, it is recommended to use [io2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html) volumes. Disk size and IOPS can be provisioned according to the requirement.

- On GCP, [pd-extreme](https://cloud.google.com/compute/docs/disks#disk-types/) is recommended. Disk size, IOPS and MBPS can be provisioned, but it's only available on 64c+ instances.

- On Azure, [Ultra disk](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks) is recommended. Disk size, IOPS, and MBPS can be provisioned according to the requirement.

### Example 1, Run a social network workload on AWS
With 20GB [gp3](https://aws.amazon.com/ebs/general-purpose/) dedicated Raft-Engine disk, for a write intensive social network application workload, qps increases by 17.5%, avg latency of insert statement decreases by 18.7%, p99 latency of insert statement decreases by 45.6%, and the estimated cost is increased by only 0.4%. AWS provide 3000 IOPS and 125 MBPS/s for a 20GB [gp3](https://aws.amazon.com/ebs/general-purpose/) volume.

| Item | shared Raft-Engine disk|dedicated Raft-Engine disk| diff(%) |
| ------------- | ------------- |------------- |------------- |
| QPS (K/s)| 8.0 | 9.4 | 17.5| 
| AVG Insert Latency (ms)| 11.3 | 9.2 | -18.7 |
| P99 Insert Latency (ms)| 29.4 | 16.0 | -45.6|

### Example 2, Run TPC-C/SYSBench workload on AZure
By using a 32G Ultra disk for Raft-Engine on Azure:

- For sysbench oltp_read_write,  QPS up by 17.8%, avg latency is down by 15.6%.
- For TPC-C, QPS up by 27.6%, avg latency down by 23.1%

| Item | Workload | shared Raft-Engine disk|dedicated Raft-Engine disk| diff(%) |
| ------------- | ------------- | ------------- |------------- |------------- |
| QPS (K/s) | Sysbench - oltp_read_write | 60.7 | 71.5 | 17.8| 
| QPS (K/s) | TPC-C | 23.9 | 30.5 | 27.6| 
| AVG Latency (ms)| Sysbench - oltp_read_write |  4.5 | 3.8 | -15.6 |
| AVG Latency (ms)| TPC-C |  3.9 | 3.0 | -23.1 |

### Example 3, how to attach a dedicated pd-ssd disk on Google Cloud for Raft-Engine on TiKV manifest

Here is a example for a cluster deployed by TiDB Operator on Google Cloud, attach an additional disk with 512GB [pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/) volumne, and change the `raft-engine.dir` to store Raft-Engine logs to this specific disk.

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


## Reduce Compaction IO Flow In KV RocksDB
As the storage engine of TiKV, [RocksDB](https://rocksdb.org/) is used to store user data. The write amplification for RocksDB can be high and the workload may be bottlenecked on disk throughput. This is not uncommon because the provisioned IO throughput on cloud ebs is usually limited due to cost reason. Under this situation, the total number of compaction pending bytes will grow over time and flow control is triggered, indicating that TiKV doesn't have enough disk bandwith to keep up with the foreground write flow. In this case, to mitigate the bottleneck of disk throughput, increasing the compression level for the RocksDB and reducing the disk throughput can help improve performance. For example, below config increase all the compression level of the default column family to zstd.

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


# Mitigation of Live Migration Maintenance Events on Google Cloud

Google Cloud's [Live Migration feature](https://cloud.google.com/compute/docs/instances/live-migration-process) enables VMs to be seamlessly migrated between hosts without causing downtime. However, these migration events are not rarely occured and can have an huge impact on the performance of VMs, including those running in a TiDB Cluster. During the event, the impacted VMs will performan much slower and impact the query proccsing response time in TiDB Cluster.

To mitigate the performance penalty from GCP's live migration event, TiDB provide a [watching script](https://github.com/PingCAP-QE/tidb-google-maintenance) based on the Google's own metadata [example](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/metadata/main.py). The scripts are deployed on TiDB, TiKV, and PD nodes, to detect maintenance events. During maintenance events, below appropriate actions can be taken:
- TiDB: Put the TiDB offline by cordon the TiDB node and delete the TiDB pod (the node pool of TiDB instance MUST be set to auto-scale, and be set to TiDB dedicated. Other pods running on the node would be interrupted when the node is cordon. The cordon node is expected to be reclaimed by auto-scaler)
- TiKV: Ecivt leaders on TiKV store during maintenance.
- PD: Resign leader if the current PD instance is the PD leader

It is worth emphasizing that this monitoring script is specifically tailored for TiDB Clusters deployed using the [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/tidb-operator-overview), which offers enhanced management functionalities for TiDB in Kubernetes environments.

The purpose of the watching script is to detect maintenance events initiated by Google Cloud. When such events are detected, appropriate actions can be taken to minimize disruption and optimize the cluster's behavior. It's important to note that this watching script is specifically designed for TiDB Clusters deployed using the TiDB Operator, which provides additional management capabilities for TiDB in Kubernetes environments.

By utilizing the watching script and taking necessary actions during maintenance events, TiDB clusters can better handle GCP's live migration events and ensure smoother operations with minimal impact on query processing and response times.

# PD Tuning with large deployment cluster

In a TiDB Cluster, the architecture relies on a single active PD (Placement Driver) server to handle crucial tasks such as serving the TSO (Timestamp Oracle) and other requests. However, this single point of active architecture can potentially limit the scalability of TiDB clusters.

## Sympotoms of PD limiration
The example showcases a large cluster deployment consisting of three PD servers, each equipped with 56 CPUs. In the below graphs, it is observed that when the query per second (QPS) exceeds 1 million and the TSO (Timestamp Oracle) requests per second surpass 162,000, the CPU utilization reaches approximately 4,600%. This high CPU utilization indicates that the PD leader is experiencing significant load and is running out of available CPU resources.

![pd-server-cpu](/media/performance/public-cloud-best-practice/baseline_cpu.png)
![pd-server-metrics](/media/performance/public-cloud-best-practice/baseline_metrics.png)

## PD Tuning

To address the high CPU utilization issue in the PD server, the following tuning adjustments can be made to the PD configuration:

### PD Configuration
`tso-update-physical-interval`: This parameter controls the interval at which the PD server updates the physical TSO batch. By reducing the value, the PD server can allocate TSO batches more frequently, reducing the waiting time for the next allocation.
```
tso-update-physical-interval = "10ms" # default: 50ms
```

### TiDB Global Variable
In addition to the PD configuration, adjusting a TiDB global variable can further optimize the TSO client's behavior. Enable the TSO client batch wait feature by setting `tidb_tso_client_batch_max_wait_time` to a non-zero value.

```
set global tidb_tso_client_batch_max_wait_time = 2; # default: 0
```

### TiKV Configuration
To reduce the number of regions and alleviate the heartbeat overhead on the system, it is recommended to increase the region size in the TiKV configuration from 96MB to 256MB.

```
[coprocessor]
  region-split-size = "256MB"
```

## After Tuning

Following the implementation of these tuning changes, the effects are observed in the graphs below:

- The TSO requests per second have decreased to 64,800.
- The CPU utilization has reduced significantly from approximately 4,600% to 1,400%.
- The P999 value of "PD server TSO handle time" has decreased from 2ms to 0.5ms.

These improvements indicate that the tuning adjustments have successfully reduced the CPU utilization of the PD server while maintaining stable TSO handling performance.

![pd-server-cpu](/media/performance/public-cloud-best-practice/after_tuning_cpu.png)
![pd-server-metrics](/media/performance/public-cloud-best-practice/after_tuning_metrics.png)


# Conclusion
By adhering to these best practices, TiDB deployments on the public cloud can achieve exceptional performance, cost efficiency, reliability and scability. The selection of the right dedicated disk type and size ensures optimal storage performance for Raft-Engine. Tuning TiKV's compaction settings improves resource utilization and reduces IO throughput. Minimizing cross-AZ read traffic helps optimize costs. Leveraging notification and taking proper actions mitigates performance impact during maintenance events. Tuning PD server addresses scalability bottleneck on a single active PD server.

In conclusion, Whether you are deploying TiDB on AWS, GCP, Azure, or any other public cloud provider, these best practices provide a solid foundation for success. 