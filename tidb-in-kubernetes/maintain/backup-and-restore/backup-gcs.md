---
title: Back up TiDB Cluster Data to GCS
summary: Learn how to back up the TiDB cluster to GCS.
category: how-to
---

# Back up TiDB Cluster Data to GCS

This document describes how to back up the data of the TiDB cluster in Kubernetes to [Google Cloud Storage (GCS)](https://cloud.google.com/storage/docs/). "Backup" in this document refers to full backup (ad-hoc full backup and scheduled full backup). For the underlying implementation, [`mydumper`](/reference/tools/mydumper.md) is used to get the logic backup of the TiDB cluster, and then this backup data is sent to the remote GCS.

The backup method described in this document is implemented based on CustomResourceDefinition (CRD) in TiDB Operator v1.1 or later versions. For the backup method implemented based on Helm Charts, refer to [Back up and Restore TiDB Cluster Data Based on Helm Charts](/tidb-in-kubernetes/maintain/backup-and-restore/charts.md).

## Ad-hoc full backup to GCS

Ad-hoc full backup describes a backup operation by creating a `Backup` custom resource (CR) object. TiDB Operator performs the specific backup operation based on this `Backup` object. If an error occurs during the backup process, TiDB Operator does not retry and you need to handle this error manually.

To better explain how to perform the backup operation, this document shows an example in which the data of the `demo1` TiDB cluster is backed up to the `test1` Kubernetes namespace.

### Prerequisites for ad-hoc backup

1. Download [backup-rbac.yaml](https://github.com/pingcap/tidb-operator/blob/master/manifests/backup/backup-rbac.yaml) and execute the following command to create the role-based access control (RBAC) resources in the `test1` namespace:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-rbac.yaml -n test1
    ```

2. Create the `gcs-secret` secret which stores the credential used to access GCS. The `google-credentials.json` file stores the service account key that you have downloaded from the GCP console. Refer to [GCP documentation](https://cloud.google.com/docs/authentication/getting-started) for details.

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic gcs-secret --from-file=credentials=./google-credentials.json -n test1
    ```

3. Create the `backup-demo1-tidb-secret` secret which stores the root account and password needed to access the TiDB cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-demo1-tidb-secret --from-literal=password=<password> --namespace=test1
    ```

### Ad-hoc backup process

Create the `Backup` CR and back up data to GSC:

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f backup-gcs.yaml
```

The `backup-gcs.yaml` file has the following content:

```yaml
---
apiVersion: pingcap.com/v1alpha1
kind: Backup
metadata:
  name: demo1-backup-gcs
  namespace: test1
spec:
  from:
    host: <tidb-host-ip>
    port: <tidb-port>
    user: <tidb-user>
    secretName: backup-demo1-tidb-secret
  gcs:
    secretName: gcs-secret
    projectId: <your-project-id>
    # location: us-east1
    # storageClass: STANDARD_IA
    # objectAcl: private
    # bucketAcl: private
  storageClassName: local-storage
  storageSize: 10Gi
```

In the above example, all data of the TiDB cluster is exported and backed up to GCS. You can ignore the `location`, `objectAcl`, `bucketAcl`, and `storageClass` items in the GCS configuration.

`projectId` in the configuration is the unique identifier of the user project on GCP. To learn how to get this identifier, refer to the [GCP documentation](https://cloud.google.com/resource-manager/docs/creating-managing-projects).

GCS supports the following `storageClass` types:

* `MULTI_REGIONAL`
* `REGIONAL`
* `NEARLINE`
* `COLDLINE`
* `DURABLE_REDUCED_AVAILABILITY`

If `storageClass` is not configured, `COLDLINE` is used by default. For the detailed description of these storage types, refer to [GCS documentation](https://cloud.google.com/storage/docs/storage-classes).

GCS supports the following object access-control list (ACL) polices:

* `authenticatedRead`
* `bucketOwnerFullControl`
* `bucketOwnerRead`
* `private`
* `projectPrivate`
* `publicRead`

If the object ACL policy is not configured, the `private` policy is used by default. For the detailed description of these access control policies, refer to [GCS documentation](https://cloud.google.com/storage/docs/access-control/lists).

GCS supports the following bucket ACL policies:

* `authenticatedRead`
* `private`
* `projectPrivate`
* `publicRead`
* `publicReadWrite`

If the bucket ACL policy is not configured, the `private` policy is used by default. For the detailed description of these access control policies, refer to [GCS documentation](https://cloud.google.com/storage/docs/access-control/lists).

After creating the `Backup` CR, execute the following command to check the backup status:

{{< copyable "shell-regular" >}}

 ```shell
 kubectl get bk -n test1 -owide
 ```

More `Backup` CRs are as described follows:

* `.spec.metadata.namespace`: the namespace where the `Backup` CR is located.
* `.spec.from.host`: the address of the TiDB cluster to be backed up.
* `.spec.from.port`: the port of the TiDB cluster to be backed up.
* `.spec.from.user`: the accessing user of the TiDB cluster to be backed up.
* `.spec.from.tidbSecretName`: the secrete of the credential needed by the TiDB cluster to be backed up.
* `.spec.storageClassName`: the persistent volume (PV) type specified for the backup operation. If this item is not specified, the value of the `default-backup-storage-class-name` parameter (`standard` by default, specified when TiDB Operator is started) is used by default.
* `.spec.storageSize`: the PV size specified for the backup operation. This value must be greater than size of the TiDB cluster to be backed up.

## Scheduled full backup to GCS

You can set a backup policy to perform scheduled backups of the TiDB cluster, and set a backup retention policy to avoid excessive backup items. A scheduled full backup is described by a custom `BackupSchedule` CR object. A full backup is triggered at each backup time point. Its underlying implementation is the ad-hoc full backup.

### Prerequisites for scheduled backup

The prerequisites for the scheduled backup is the same with the [prerequisites for ad-hoc backup](#prerequisites-for-ad-hoc-backup).

### Scheduled backup process

Create the `BackupSchedule` CR to enable the scheduled full backup to GCS:

{{< copyable "shell-regular" >}}

```shell
kubectl apply -f backup-schedule-gcs.yaml
```

The `backup-gcs.yaml` file has the following content:

```yaml
---
apiVersion: pingcap.com/v1alpha1
kind: BackupSchedule
metadata:
  name: demo1-backup-schedule-gcs
  namespace: test1
spec:
  #maxBackups: 5
  #pause: true
  maxReservedTime: "3h"
  schedule: "*/2 * * * *"
  backupTemplate:
    from:
      host: <tidb-host-ip>
      port: <tidb-port>
      user: <tidb-user>
      secretName: backup-demo1-tidb-secret
    gcs:
      secretName: gcs-secret
      projectId: <your-project-id>
      # location: us-east1
      # storageClass: STANDARD_IA
      # objectAcl: private
      # bucketAcl: private
    storageClassName: local-storage
    storageSize: 10Gi
```

After creating the scheduled full backup, use the following command to check the backup status:

{{< copyable "shell-regular" >}}

```shell
kubectl get bks -n test1 -owide
```

Execute the following command to check all the backup items:

{{< copyable "shell-regular" >}}

 ```shell
 kubectl get bk -l tidb.pingcap.com/backup-schedule=demo1-backup-schedule-gcs -n test1
 ```

From the above example, you can see that the `backupSchedule` configuration consists of two part. One is the unique configuration of `backupSchedule` and the other is `backupTemplate`. `backupTemple` specifies the configuration related to the GCS storage, which is the same with the configuration of the ad-hoc full backup to GCS (refer to [GCS backup process](#ad-hoc-backup-process) for details). The following are the unique configuration items of `backupSchedule`:

+ `.spec.maxBackups`: A backup retention policy, which determines the maximum number of backup items to be retained. When this value is exceeded, the outdated backup items will be deleted. If you set this configuration item to `0`, all backup items are retained.
+ `.spec.maxReservedTime`: A backup retention policy based on time. For example, if you set the value of this configuration to `24h`, backup items only of recent 24 hours are retained. All backup items out of this time are deleted. For the time format, refer to [`func ParseDuration`](https://golang.org/pkg/time/#ParseDuration). If you have set the maximum number of backup items and the longest retention time of backup items at the same time, the latter setting takes effect.
+ `.spec.schedule`: The time scheduling format of Cron. Refer to [Cron](https://en.wikipedia.org/wiki/Cron) for details.
+ `.spec.pause`: `false` by default. If this parameter is set to `true`, the scheduled scheduling is paused. In this situation, the backup operation will not be performed even if the scheduling time is reached. During this pause, the backup [Garbage Collection](/reference/garbage-collection/overview.md) (GC) runs normally. If you change `true` to `false`, the full backup process is restarted.
