---
title: Backup and Restore
summary: Learn how to back up and restore the data of TiDB cluster in Kubernetes.
category: how-to
---

# Backup and Restore

## About

This document describes how to backup and restore the data of TiDB cluster in Kubernetes.

TiDB in Kubernetes supports two kinds of backup:

* [Full backup](#full-backup)(scheduled or ad-hoc) via [`mydumper`](https://www.pingcap.com/docs/dev/reference/tools/mydumper/), which helps you to perform a logically backup of a TiDB cluster.
* [Incremental backup](#incremental-backup) via [`TiDB-Binlog`](https://www.pingcap.com/docs/dev/reference/tools/tidb-binlog/overview/), which helps you replicate the data in a TiDB cluster to other databases or back up the data in real time.

Currently, TiDB in Kubernetes only supports automatic [restore operation](#restore) for full backup taken by `mydumper`. Restoring the backup data captured by `TiDB-Binlog` requires manual intervention.

## Full backup

Full backup uses `mydumper` to take a logical backup of a TiDB cluster. The backup job will create a PVC([PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)) to store data.

By default, the backup uses PV ([Persistent Volume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#persistent-volumes)) to store the backup data. You can also store the backup data to [Google Cloud Storage](https://cloud.google.com/storage/) bucket, [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) or [Amazon S3](https://aws.amazon.com/s3/) by changing the configuration. This way the PV temporarily stores backup data before it is placed in object storage. Refer to [TiDB cluster Backup configuration](/reference/configuration/tidb-in-kubernetes/backup-configuration.md) for full configuration guide of backup and restore.

You can either set up a scheduled full backup job or take a full backup in an ad-hoc manner.

### Scheduled full backup

Scheduled full backup is created alongside the TiDB cluster, and it runs periodically like the crontab job.

To configure a scheduled full backup, modify the `scheduledBackup` section in the `values.yaml` file of the TiDB cluster:

* Set `scheduledBackup.create` to `true`.
* Set `scheduledBackup.storageClassName` to the PV storage class name used for backup data.

    > **Note:**
    >
    > You must set the scheduled full backup PV's [reclaim policy](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy) to `Retain` to keep your backup data safe.

* Configure `scheduledBackup.schedule` in the [Cron](https://en.wikipedia.org/wiki/Cron) format to define the scheduling.
* Create a Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the username and password that has the privilege to backup the database:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

* Create a new cluster with the scheduled full backup configured by `helm install`, or enabling scheduled full backup for the existing cluster by `helm upgrade`:

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade <release_name> pingcap/tidb-cluster -f values.yaml --version=<tidb-operator-version>
    ```

### Ad-Hoc full backup

Ad-hoc full backup is encapsulated in another helm chart, `pingcap/tidb-backup`. According to the `mode` in `values.yaml` file, this chart can perform either full backup or restore. We will cover restore operation in the [restore section](#restore) of this document.

Refer to the steps below to create an ad-hoc full backup job:

* Modify the `values.yaml` file:
    * Set `clusterName` to the target TiDB cluster name.
    * Set `mode` to `backup`.
    * Set `storage.className` to the PV storage class name used for backup data.
    * Adjust the `storage.size` according to your database size.

    > **Note:**
    >
    > You must set the ad-hoc full backup PV's [reclaim policy](https://kubernetes.io/docs/tasks/administer-cluster/change-pv-reclaim-policy) to `Retain` to keep your backup data safe.

* Create a Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the username and password that has the privilege to backup the database:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

* Run the following command to create an ad-hoc backup job:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-backup --name=<backup-name> --namespace=<namespace> -f values.yaml --version=<tidb-operator-version>
    ```

### View backups

For backups stored in PV, you can view the PVs by using the following command:

{{< copyable "shell-regular" >}}

```shell
kubectl get pvc -n <namespace> -l app.kubernetes.io/component=backup,pingcap.com/backup-cluster-name=<cluster-name>
```

If you store your backup data to [Google Cloud Storage](https://cloud.google.com/storage/), [Ceph Object Storage](https://ceph.com/ceph-storage/object-storage/) or [Amazon S3](https://aws.amazon.com/s3/), you can view the backups by using the GUI or CLI tool of these storage provider.

## Restore

The helm chart `pingcap/tidb-backup` helps restore a TiDB cluster using backup data. Refer to the steps below to perform a restore operation:

* Modify the `values.yaml` file:
    * Set `clusterName` to the target TiDB cluster name.
    * Set `mode` to `restore`.
    * Set `name` to the backup name you want to restore([view backups](#view-backups) helps you view all the backups available). If the backup is stored in `Google Cloud Storage`, `Ceph Object Storage` or `Amazon S3`, you must configure the corresponding section too (you might continue to use the same configuration you set in the [adhoc full backup](#ad-hoc-full-backup)).
* Create a Kubernetes [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) containing the user and password that has the privilege to restore the database (skip this if you have already created one in the [adhoc full backup](#ad-hoc-full-backup) section):

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n <namespace> --from-literal=user=<user> --from-literal=password=<password>
    ```

* Restore the backup:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-backup --namespace=<namespace> --name=<restore-name> -f values.yaml --version=<tidb-operator-version>
    ```

## Incremental backup

Incremental backup leverages the [TiDB Binlog](https://www.pingcap.com/docs/dev/reference/tools/tidb-binlog/overview/) tool to collect binlog data from TiDB and provide real-time backup and replication to downstream platforms.

Incremental backup is disabled in the TiDB cluster by default. To create a TiDB cluster with incremental backup enabled or enable incremental backup in existing TiDB cluster, modify the `values.yaml` file:

* Set `binlog.pump.create` to `true`.
* Set `binlog.drainer.create` to `true`.
* Set `binlog.pump.storageClassName` and `binlog.drainer.storageClassName` to a proper `storageClass` available in your kubernetes cluster.
* Set `binlog.drainer.destDBType` to your desired downstream, explained in detail below.

Three types of downstream platforms available for incremental backup:

* PersistenceVolume: default downstream. You can consider configuring a large PV for `drainer` (the `binlog.drainer.storage` variable) in this case.
* MySQL compatible database: enabled by setting `binlog.drainer.destDBType` to `mysql`. You must configure the target address and credential in the `binlog.drainer.mysql` section too.
* Apache Kafka: enable by setting `binlog.drainer.destDBType` to `kafka`. You must configure the zookeeper address and Kafka address in the `binlog.drainer.kafka` section too.
