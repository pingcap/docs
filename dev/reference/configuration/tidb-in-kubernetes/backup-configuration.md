---
title: TiDB in Kubernetetes Backup Configuration
category: reference
---

# TiDB in Kubernetetes Backup Configuration

`tidb-backup` is a helm chart designed for TiDB cluster backup and restore. This document describes the configuration of this chart.

## Configuration

### `mode`

- Run mode
- Default: "backup"
- Options: `backup` or `restore`

### `clusterName`

- Target cluster name
- Default: "demo"
- The name of the TiDB cluster that data is backed up from or restore to

### `name`

- The backup name
- Default: "fullbackup-${date}", date is the start time of backup, accurate to minute

### `secretName`

- The name of the `Secret`([Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)) which stores the crendential of the target cluster
- Default: "backup-secret"
- You can create the `Secret` by the follwing command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic backup-secret -n ${namespace} --from-literal=user=root --from-literal=password=<password>
    ```

### `storage.className`

- The [StorageClass](https://kubernetes.io/docs/concepts/storage/storage-classes/) used to store the backup data
- Default: "local-storage"
- The backup job has to bound a Persistent Volume (PV) to store the backup data, you have to ensure the `StorageClass` is presented in your Kubernetes cluster.

### `storage.size`

- The storage size of PersistenceVolume
- Default: "100Gi"

### `backupOptions`

- The options that are passed to [`mydumper`](https://github.com/maxbube/mydumper/blob/master/docs/mydumper_usage.rst#options)
- Default: "--chunk-filesize=100"

### `restoreOptions`

- The options that are passed to [`loader`](https://www.pingcap.com/docs-cn/tools/loader/)
- Default: "-t 16"

### `gcp.bucket`

- The name of the GCP bucket used to store backup data
- Default: ""

> **Note:**
>
> Once you set any variables under `gcp` section, the backup data will be uploaded to Google Cloud Storage, namely, you have to keep the configuration intact.

### `gcp.secretName`

- The name of the `Secret` that stores the credential of Google Cloud Storage
- Default: ""
- You can refer to [Google Cloud Documentation](https://cloud.google.com/docs/authentication/production#obtaining_and_providing_service_account_credentials_manually) to download the credential file and create the `Secret` by the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic gcp-backup-secret -n ${namespace} --from-file=./credentials.json
    ```

### `ceph.endpoint`

- The endpoint of ceph object storage
- Default: ""

> **Note:**
>
> Once you set any variables under `ceph` section, the backup data will be uploaded to ceph object storage, namely, you have to keep the configuration intact.

### `ceph.bucket`

- The bucket name of ceph object storage
- Default: ""

### `ceph.secretName`

- The name of the `Secret` that stores the credential of Ceph object store.
- Default: ""
- You can create the `Secret` by the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic ceph-backup-secret -n ${namespace} --from-literal=access_key=<access-key> --from-literal=secret_key=<secret-key>
    ```
