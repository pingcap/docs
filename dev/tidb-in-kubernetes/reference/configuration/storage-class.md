---
title: Storage Class Configuration in Kubernetes Local PV Configuration
summary: Learn how to Configure PV (Persistent Volume).
category: reference
aliases: ['/docs/dev/tidb-in-kubernetes/reference/configuration/local-pv/']
---

# Persistent Volume Configuration in Kubernetes

TiDB cluster components such as PD, TiKV, TiDB monitoring, TiDB-Binlog and `tidb-backup` require PV (Persiststent Volume). For PV in Kubernetes, see [PersistentVolume (PV)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). Kubernetes offers a variety of [storage classes](https://kubernetes.io/docs/concepts/storage/volumes/), which are mainly divided into two parts:

- Network storage

    The storage medium is not on the current node, but is mounted to the node through the network. Generally, there are redundant replicas to guarantee high availability. When the node fails, the corresponding netowrk storage can be re-mounted to other nodes for further use.

- Local storage

    The storage medium is on the current node which typically provides lower latency than netowrk storage. However, without redundant replicas, once the node fails, data can be lost. If it is an IDC server, data can be restored to a certain extent. If it is a virtual macine using the local disk on the public cloud, data **cannot** be retrieved after the node fails.

PV is created automatically by the system administrator or volume provisioner. PV and Pod are associated via [PersistentVolumeClaim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims). Users apply for using PV through PVC instead of creating PV directly. The corresponding volume provisioner creates a PV that meets the requirements of PVC and then binds the PV to the PVC.

> **Warning:**
>
> For data security, don't delete PV unless you are familiar with volume provisioner.

## Recommended Storage Class in TiDB Clusters

TiKV uses Raft to replicate data. When a node fails, PD automatically schedules data to fill the missing data copies, and TiKV requires low read and write latency, so local SSD is strongly recommended in production environment.

PD also uses Raft to replicate data. PD is not an I/O-intensive application, but a database for storing cluster meta information, so a local SAS disk or network SSD storage such as EBS General Purpose SSD (gp2) volumes on AWS and SSD persistent disks on GCP can meet the requirements.

To ensure availability, it is recommended to use network storage because TiDB monitoring, TiDB-Binlog and `tidb-backup` components do not have redundant replicas. Pump and Drainer components of TiDB Binlog are I/O-intensive applications that require low read and write latency, so high-performance network storage such as EBS Provisioned IOPS SSD (io1) volumes on AWS and SSD persistent disks on GCP is recommended.

When deploying TiDB clusters or `tidb-backup` with TiDB Operator, you can set the storage class of components that require persistent storage via the corresponding `storageClassName` in the `values.yaml` configuration file. The default storage class is `local-storage`.

## Network PV Configuration

Kubernetes 1.11 and above supports [Resizing Persistent Volumes using Kubernetes](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/), but users need to enable volume expansion for the corresponding `StorageClass`.

{{< copyable "shell-regular" >}}

```shell
kubectl patch storageclass <storage-class-name> -p '{"allowVolumeExpansion": true}'
```

After the volume expansion is enabled, expand PV using the following method:

1. Edit the PersistentVolumeClaim (PVC) object

    Suppose the PVC is 10 Gi and now we need to expand it to 100 Gi.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pvc -n <namespace> <pvc-name> -p '{"spec": {"resources": {"requests": {"storage": "100Gi"}}}'
    ```

2. View the PV size

    After the expansion, the size displayed by `kubectl get pvc -n <namespace> <pvc-name>` is still the initial one, but viewing the PV size shows that it has been expanded to the expected size.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pv | grep <pvc-name>
    ```

## Local PV Configuration

Kubernetes currently supports statically allocated local storage. To create a local storage object, use the `local-volume-provisioner` program in [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) project. The procedures are as follows:

1. Pre-allocate local storage in TiKV cluster nodes. See the [operation document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md) provided by Kubernetes for reference.

2. Install the `local-volume-provisioner` program. See the [Helm installation procedure](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/helm) for reference.

For more information, refer to [Kubernetes local storage](https://kubernetes.io/docs/concepts/storage/volumes/#local) and [local-static-provisioner document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview).

### Best Practices

- The path of local PV is the unique identifier of local storage on the node. To avoid conflict, it is recommended to use the UUID of the device to generate a unique path.
- For IO isolation, a whole physical disk per volume is recommended.
- For capacity isolation, a separate partition per volume is recommended.

Refer to [Best Practices](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md) for more information with local PV in Kubernetes.

## Data Security

In general, after the PVC is used up and deleted, the PV bound to it is reclaimed and placed in the resource pool for scheduling by the provisioner. To avoid accidental data loss, you can globally configure `StorageClass`'s reclaim policy to `Retain` or only change a single PV's reclaim policy to `Retain`. In `Retain` mode, PV is not automatically reclaimed.

- Global configuration

    The `StorageClass` reclaim policy cannot be modified once it is created, so it can only be set at creation time. If it is not set when created, you can create another `StorageClass` of the same provisioner. For example, the default reclaim policy of `StorageClass` on Google Kubernetes Engine (GKE) is `Delete`. You can create another `StorageClass` named `pd-standard` with reclaim policy as `Retain`, and change the `storageClassName` of the corresponding component to `pd-standard` when creating TiDB clusters.

    {{< copyable "" >}}

    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: pd-standard
    parameters:
       type: pd-standard
    provisioner: kubernetes.io/gce-pd
    reclaimPolicy: Retain
    volumeBindingMode: Immediate
    ```

- Configure a single PV

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

> **Note:**
>
> By default, TiDB Operator automatically changes the PV recliam policy of PD and TiKV to `Retain` to ensure data security.

{{< copyable "shell-regular" >}}

```shell
kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

Refer to [Change the Reclaim Policy of a PersistentVolume](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/) for more information about the reclaim policy of a PV.