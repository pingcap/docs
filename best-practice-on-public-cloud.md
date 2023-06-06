---
title: Best Practice On Public Cloud
summary: This document introduces the best practice for TiDB to deploy on public cloud
---

# Best Practice On Public Cloud

Public cloud infrastructure has become an increasingly popular choice for deploying and managing TiDB. However, deploying TiDB on the cloud requires careful consideration of several critical factors, including performance tuning, cost optimization, reliability, and scalability. 

This document aims to cover various essential topics, such as using dedicated disks for Raft-Engine, overcoming IO throughput limitations, optimizing costs for cross-AZ traffic, mitigating GCP live migration events, and fine-tuning the PD server in large clusters. By adhering to these best practices, your TiDB deployment on the public cloud can achieve optimized performance, cost efficiency, reliability, and scalability.

# Improve the TiKV write performance and stability

## Use a dedicated disk for Raft Engine

The [Raft Engine](/glossary.md#raft-engine) in TiKV plays a critical role similar to that of a write-ahead log (WAL) in traditional databases. To achieve optimal performance and stability, it is crucial to allocate a dedicated disk for the Raft Engine when you deploy TiDB on a public cloud. The following `iostat` shows the IO characteristics on a TiKV node with a write-heavy workload.

```
Device            r/s     rkB/s       w/s     wkB/s      f/s  aqu-sz  %util
sdb           1649.00 209030.67   1293.33 304644.00    13.33    5.09  48.37
sdd           1033.00   4132.00   1141.33  31685.33   571.00    0.94 100.00
```

The device `sdb` is used for KV RocksDB, while `sdd` is used to restore Raft Engine logs. Note that `sdd` has a significantly higher `f/s` value, which represents the number of flush requests completed per second for the device. In Raft Engine, when a write in a batch is marked synchronous, the batch leader will call `fdatasync()` after writing, guaranteeing that buffered data is flushed to the storage. By using a dedicated volume for Raft Engine, TiKV reduces the average queue length of requests, thereby ensuring optimal and stable write latency.

Different cloud providers offer various disk types with different performance characteristics, such as IOPS and MBPS. Therefore, it is important to choose an appropriate cloud provider, disk type, and disk size based on your workload.

### Choose appropriate disks for Raft Engine on public clouds

This section outlines best practices for choosing appropriate disks for Raft-Engine on different public clouds. Depending on performance requirements, two types of recommended disks are available.

#### Middle-range disk

The following are recommended middle-range disks for different public clouds:

- On AWS, it is recommended to use [gp3](https://aws.amazon.com/ebs/general-purpose/) volumes. These volumes offer a free allocation of 3000 IOPS and 125 MB/s throughput, irrespective of the volume size. This is usually sufficient for the Raft Engine.

- On GCP, it is recommended to use [pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/) volumes. The IOPS and MBPS vary depending on the allocated disk size. To meet performance requirements, it is recommended to allocate 200 GB for Raft-Engine. Although Raft Engine does not require such a large space, it ensures optimal performance.

- On Azure, it is recommended to use  [Premium SSD v2](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#premium-ssd-v2) volumes. Similar to AWS, they provide a free allocation of 3000 IOPS and 125 MB/s throughput, regardless of the volume size, which is generally adequate for Raft Engine.

#### High-end disk

If you expect an even lower latency for Raft Engine, consider using high-end disks. The following are recommended high-end disks for different public clouds:

- On AWS, [io2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html) is recommended. Disk size and IOPS can be provisioned according to your specific requirements.

- On GCP, [pd-extreme](https://cloud.google.com/compute/docs/disks#disk-types/) is recommended. Disk size, IOPS, and MBPS can be provisioned, but it is only available on 64c+ instances.

- On Azure, [ultra disk](https://learn.microsoft.com/en-us/azure/virtual-machines/disks-types#ultra-disks) is recommended. Disk size, IOPS, and MBPS can be provisioned according to your specific requirements.

### Example 1: Run a social network workload on AWS

AWS offers 3000 IOPS and 125 MBPS/s for a 20GB [gp3](https://aws.amazon.com/ebs/general-purpose/) volume.

By using a dedicated 20GB [gp3](https://aws.amazon.com/ebs/general-purpose/) Raft Engine disk on AWS for a write-intensive social network application workload, the following improvements are observed but the estimated cost only increases by 0.4%:

- a 17.5% increase in QPS (queries per second)
- an 18.7% decrease in average latency for insert statements
- a 45.6% decrease in p99 latency for insert statements.


| Metric | Shared Raft Engine disk | Dedicated Raft Engine disk | Difference (%) |
| ------------- | ------------- |------------- |------------- |
| QPS (K/s)| 8.0 | 9.4 | 17.5| 
| AVG Insert Latency (ms)| 11.3 | 9.2 | -18.7 |
| P99 Insert Latency (ms)| 29.4 | 16.0 | -45.6|

### Example 2: Run TPC-C/SYSBench workload on Azure

By using a dedicated 32GB ultra disk for Raft Engine on Azure, the following improvements are observed:

- Sysbench `oltp_read_write` workload: a 17.8% increase in QPS and a 15.6% decrease in average latency.
- TPC-C workload: a 27.6% increase in QPS and a 23.1% decrease in average latency.

| Metric | Workload | Shared Raft Engine disk | Dedicated Raft Engine disk | Difference (%) |
| ------------- | ------------- | ------------- |------------- |------------- |
| QPS (K/s) | Sysbench `oltp_read_write` | 60.7 | 71.5 | 17.8| 
| QPS (K/s) | TPC-C | 23.9 | 30.5 | 27.6| 
| AVG Latency (ms)| Sysbench `oltp_read_write` |  4.5 | 3.8 | -15.6 |
| AVG Latency (ms)| TPC-C |  3.9 | 3.0 | -23.1 |

### Example 3: Attach a dedicated pd-ssd disk on Google Cloud for Raft Engine on TiKV manifest

The following TiKV configuration example shows how to attach an additional 512GB [pd-ssd](https://cloud.google.com/compute/docs/disks#disk-types/) disk to a cluster on Google Cloud deployed by TiDB Operator, with `raft-engine.dir` configured to store Raft Engine logs to this specific disk.

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


## Reduce compaction IO flow in KV RocksDB

As the storage engine of TiKV, [RocksDB](https://rocksdb.org/) is used to store user data. However, because the provisioned IO throughput on cloud EBS is usually limited due to cost considerations, RocksDB might exhibit high write amplification, and the disk throughput might become the bottleneck for the workload. As a result, the total number of pending compaction bytes grows over time and triggers flow control, which indicates that TiKV lacks sufficient disk bandwidth to keep up with the foreground write flow. 

To alleviate the bottleneck caused by limited disk throughput, you can improve performance by increasing the compression level for RocksDB and reducing the disk throughput. For example, you can refer to the following example to increase all the compression levels of the default column family to `zstd`.

```
[rocksdb.defaultcf]
compression-per-level = ["zstd", "zstd", "zstd", "zstd", "zstd", "zstd", "zstd"]
```

## Optimize cost for cross-AZ network traffic

Deploying TiDB across multiple availability zones (AZs) can lead to increased costs due to cross-AZ data transfer fees. To optimize costs, it is important to reduce cross-AZ network traffic.

To reduce cross-AZ read traffic, you can enable the [Follower Read feature](/follower-read.md), which allows TiDB to prioritize selecting replicas in the same availability zone. To enable this feature, set the `tidb_replica_read` variable to `closest-replicas` or `closest-adaptive`. 

To reduce cross-AZ write traffic in TiKV instances, you can enable the gRPC compression feature, which compresses data before transmitting it over the network. The following configuration example shows how to enable gzip gRPC compression for TiKV.

```
server_configs:
  tikv:
    server.grpc-compression-type: gzip
```

To reduce network traffic caused by the data shuffle of the TiFlash MPP tasks, it's recommended to deploy multiple TiFlash instance at the same availability zones (AZs).
Since v6.6.0, [Compression exchange](https://docs.pingcap.com/tidb/v6.6/explain-mpp#mpp-version-and-exchange-data-compression) is enabled by default to reduce the network traffic caused by MPP data shuffle.


# Mitigation of Live Migration Maintenance Events on Google Cloud

Google Cloud's [Live Migration feature](https://cloud.google.com/compute/docs/instances/live-migration-process) enables VMs to be seamlessly migrated between hosts without causing downtime. However, these migration events are not rarely occured and can have an huge impact on the performance of VMs, including those running in a TiDB Cluster. During the event, the impacted VMs will performan much slower and impact the query proccsing response time in TiDB Cluster.

To mitigate the performance penalty from GCP's live migration event, TiDB provide a [watching script](https://github.com/PingCAP-QE/tidb-google-maintenance) based on the Google's own metadata [example](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/compute/metadata/main.py). The scripts are deployed on TiDB, TiKV, and PD nodes, to detect maintenance events. During maintenance events, below appropriate actions can be taken:
- TiDB: Put the TiDB offline by cordon the TiDB node and delete the TiDB pod (the node pool of TiDB instance MUST be set to auto-scale, and be set to TiDB dedicated. Other pods running on the node would be interrupted when the node is cordon. The cordon node is expected to be reclaimed by auto-scaler)
- TiKV: Ecivt leaders on TiKV store during maintenance.
- PD: Resign leader if the current PD instance is the PD leader

It is worth emphasizing that this watching script is specifically tailored for TiDB Clusters deployed using the [TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/dev/tidb-operator-overview), which offers enhanced management functionalities for TiDB in Kubernetes environments.

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