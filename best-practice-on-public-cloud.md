---
title: Best Practice On Public Cloud
summary: This document introduces the best practice for TiDB to deploy on public cloud
---

# Introduction

Public cloud has become an increasingly popular option for deploying and managing databases, offering a range of benefits such as flexibility, scalability, and ease of management. However, deploying TiDB on the cloud requires careful consideration of several factors, such as performance tuning, cost optimization, and reliability. This document will cover various topics such as dedicated disk for raft-engine, cost optimization for cross-AZ traffic, and mitigation of GCP live migration event. By following these best practices, you can ensure that your TiDB deployment on public cloud is optimized for performance, cost, and reliability.


# Dedicated Disk for Raft-Engine
When deploying TiDB on a public cloud, it is important to ensure that the Raft engine has a dedicated disk to achieve optimal performance. Different cloud providers offer different types of disks with varying performance characteristics, such as IOPS and MBPS. Therefore, it is important to choose the appropriate disk type and size based on the workload and the cloud provider being used.

For example, on AWS, it is recommended to use the gp3 disk type with a minimum of 20GB, and IOPS and MBPS can be specified depending on the workload. On GCP, the PD-SSD disk type is recommended, and the IOPS and MBPS are dependent on the disk size. On Azure, the SSD Premium disk type is recommended, and the IOPS and MBPS are also dependent on the disk size.

In addition to choosing the appropriate disk type and size, it is also important to tune TiKV's compaction settings to optimize performance. The total number of compaction pending bytes can grow over time, indicating that TiKV doesn't have enough resources to keep up with the foreground write flow. In this case, increasing the compression level and reducing the IO throughput can help improve performance. For example, below config increase all the compression level of the defaultcf column family to reduce the compaction flow IO throughput.

```
[rocksdb.defaultcf]
compression-per-level = ["zstd", "zstd", "zstd", "zstd", "zstd", "zstd", "zstd"]
```

# Cost Optimization for Cross-AZ
Deploying TiDB across multiple availability zones (AZs) can lead to increased costs due to cross-AZ data transfer fees. To optimize costs, it is important to reduce cross-AZ read and write traffic.

One way to reduce cross-AZ read traffic is to use the Follower Read feature, which allows TiDB to read data from the follower replicas that are geographically closer to the user. This feature can be enabled by setting the tidb_followers and tidb_max_delta_schema_count variables appropriately.

To reduce cross-AZ write traffic, TiKV's gRPC compression feature can be enabled to compress data before transmitting it across the network. Additionally, TiFlash's data exchange compression feature can also be enabled to further reduce data transmission overhead.

# mitigation of GCP Live Migration Event
GCP's Live Migration feature allows VMs to be migrated between hosts without downtime. To take advantage of this feature for TiDB deployments, a maintenance watching script can be set up to detect maintenance events on TiDB, TiKV, and PD nodes. During maintenance events, appropriate actions can be taken, such as putting TiDB offline by cordon the TiDB node, evicting leaders on TiKV store, or resigning leader if the current PD instance is the PD leader. An additional container can be added to run the maintenance watching script.

# Conclusion
Optimizing TiDB deployments on a public cloud involves choosing the appropriate disk type and size, tuning TiKV's compaction settings, reducing cross-AZ read and write traffic, and utilizing cloud provider-specific features such as GCP Live Migration. By following these best practices, TiDB deployments can achieve optimal performance and cost-efficiency.



