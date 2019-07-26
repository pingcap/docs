---
title: Local PV Configuration
summary: Learn how to manage local PV (Persistent Volume).
category: how-to
---

# Local PV Configuration

TiDB is a database with high availability. Data is stored and replicated on TiKV, the storage layer of TiDB, which can tolerate the inavailability of nodes. TiKV uses local storage with high IOPS and high throughput, such as Local SSDs, to enhance database capacity.

Kubernetes currently supports statically allocated local storage. To create a local storage object, use the `local-volume-provisioner` program in [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) project. The procedures are as follows:

1. Pre-allocate local storage in TiKV cluster nodes. See the [operation document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md) provided by Kubernetes for reference.

2. Install the `local-volume-provisioner` program. See the [Helm installation procedure](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/helm) for reference.

For more information, refer to [Kubernetes local storage](https://kubernetes.io/docs/concepts/storage/volumes/#local) and [local-static-provisioner document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview).

## Data Security

- By default, when a local PV is released, the provisioner will recycle it. You can set the relaimi policy of your storage class to `Retain` to prevent it from being recycled automatically. When confirming that a PV's data can be deleted, modify its reclaim policy to `Delete`. For how to change PV reclaim policy in Kubernetes, please refer to [this doc](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/).

 ## Best Practices

- The path of the local PV is the unique identifier of local storage on the node, it's recommended to utilize the UUID of the device to generate path.
- For IO isolation, a whole disk per volume is recommended.
- For capacity isolation, separate partition per volume is recommended.

Refer to [this doc](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md) for more best practices with local PV in kubernetes.
