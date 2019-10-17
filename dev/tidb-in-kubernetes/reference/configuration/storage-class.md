---
title: Persistent Storage Class Configuration in Kubernetes
summary: Learn how to Configure local PVs and network PVs.
category: reference
aliases: ['/docs/dev/tidb-in-kubernetes/reference/configuration/local-pv/']
---

# Persistent Storage Class Configuration in Kubernetes

TiDB cluster components such as PD, TiKV, TiDB monitoring, TiDB Binlog and `tidb-backup` require the persistent storage of data. To persist the data in Kubernetes, you need to use [PersistentVolume (PV)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/). Kubernetes supports several types of [storage classes](https://kubernetes.io/docs/concepts/storage/volumes/), which are mainly divided into two parts:

- Network storage

    The network storage medium is not on the current node, but is mounted to the node through the network. Generally, there are redundant replicas to guarantee high availability. When the node fails, the corresponding network storage can be re-mounted to another node for further use.

- Local storage

    The local storage medium is on the current node, and typically can provide lower latency than the network storage. Because there are no redundant replicas, once the node fails, data might be lost. If it is an IDC server, data can be restored to a certain extent. If it is a virtual machine using the local disk on the public cloud, data **cannot** be retrieved after the node fails.

PVs are created automatically by the system administrator or volume provisioner. PVs and Pods are bound by[PersistentVolumeClaim (PVC)](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims). Users request for using a PV through a PVC instead of creating a PV directly. The corresponding volume provisioner creates a PV that meets the requirements of PVC and then binds the PV to the PVC.

> **Warning:**
>
> For data security, do not delete a PV in any case unless you are familiar with volume provisioners.

## Recommended storage class for TiDB clusters

TiKV uses the Raft protocol to replicate data. When a node fails, PD automatically schedules data to fill the missing data replicas; TiKV requires low read and write latency, so local SSD storage is strongly recommended in the production environment.

PD also uses Raft to replicate data. PD is not an I/O-intensive application, but a database for storing cluster meta information, so a local SAS disk or network SSD storage such as EBS General Purpose SSD (gp2) volumes on AWS or SSD persistent disks on GCP can meet the requirements.

To ensure availability, it is recommended to use network storage for components such as TiDB monitoring, TiDB Binlog and `tidb-backup` because they do not have redundant replicas. TiDB Binlog's Pump and Drainer components are I/O-intensive applications that require low read and write latency, so it is recommended to use high-performance network storage such as EBS Provisioned IOPS SSD (io1) volumes on AWS or SSD persistent disks on GCP.

When deploying TiDB clusters or `tidb-backup` with TiDB Operator, you can set the storage class for the components that require persistent storage via the corresponding `storageClassName` in the `values.yaml` configuration file. The storage class by default is `local-storage`.

## Network PV configuration

Kubernetes 1.11 and later versions support [dynamic expansion of network PV](https://kubernetes.io/blog/2018/07/12/resizing-persistent-volumes-using-kubernetes/), but you need to enable dynamic volume expansion for the corresponding `StorageClass`.

{{< copyable "shell-regular" >}}

```shell
kubectl patch storageclass <storage-class-name> -p '{"allowVolumeExpansion": true}'
```

After the dynamic volume expansion is enabled, expand the PV using the following method:

1. Edit the PersistentVolumeClaim (PVC) object

    Suppose the PVC is 10 Gi and now we need to expand it to 100 Gi.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pvc -n <namespace> <pvc-name> -p '{"spec": {"resources": {"requests": {"storage": "100Gi"}}}'
    ```

2. View the size of the PV

    After the expansion, the size displayed by `kubectl get pvc -n <namespace> <pvc-name>` is still the original one, but the size of the PV viewed by the following command shows that it has been expanded to the expected size.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl get pv | grep <pvc-name>
    ```

## Local PV configuration

Kubernetes currently supports statically allocated local storage. To create a local storage object, use the `local-volume-provisioner` program in [local-static-provisioner](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner) project. The procedures are as follows:

1. Pre-allocate local storage in TiKV cluster nodes. See the [operation document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/operations.md) provided by Kubernetes for reference.

2. Install the `local-volume-provisioner` program. See the [Helm installation procedure](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/tree/master/helm) for reference.

For more information, refer to [Kubernetes local storage](https://kubernetes.io/docs/concepts/storage/volumes/#local) and [local-static-provisioner document](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner#overview).

### Best practices

- The path of a local PV is the unique identifier for the local volume. To avoid conflicts, it is recommended to use the UUID of the device to generate a unique path.
- For I/O isolation, a dedicated physical disk per volume is recommended to ensure hardware-based isolation.
- For capacity isolation, a dedicated partition per volume is recommended.

Refer to [Best Practices](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner/blob/master/docs/best-practices.md) for more information on local PV in Kubernetes.

## Data security

In general, after a PVC is no longer used and deleted, the PV bound to it is reclaimed and placed in the resource pool for scheduling by the provisioner. To avoid accidental data loss, you can globally configure `StorageClass`'s reclaim policy to `Retain` or only change a single PV's reclaim policy to `Retain`. Once in the `Retain` mode, a PV cannot be automatically reclaimed.

- Configure globally:

    The `StorageClass`'s reclaim policy cannot be modified once it is created, so it can only be set at creation time. If it is not set when created, you can create another `StorageClass` of the same provisioner. For example, the default reclaim policy of `StorageClass` on Google Kubernetes Engine (GKE) is `Delete`. You can create another `StorageClass` named `pd-standard` with its reclaim policy as `Retain`, and change the `storageClassName` of the corresponding component to `pd-standard` when creating a TiDB cluster.

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

- Configure a single PV:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

> **Note:**
>
> By default, TiDB Operator automatically changes the PV reclaim policy of PD and TiKV to `Retain` to ensure data security.

When the PV reclaim policy is `Retain`, if the data of a PV can be deleted, you need to set the reclaim policy to `Delete`. In this case, as long as the corresponding PVC is deleted, the PV is automatically deleted and reclaimed.

{{< copyable "shell-regular" >}}

```shell
kubectl patch pv <pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Delete"}}'
```

Refer to [Change the Reclaim Policy of a PersistentVolume](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy/) for more information about the reclaim policy of a PV.