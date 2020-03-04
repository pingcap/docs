---
title: Restore Data From S3-Compatible Storage
summary: Learn how to restore data from the S3-compatible storage.
category: how-to
---

# Restore Data From S3-Compatible Storage

本文描述了将 Kubernetes 上通过 TiDB Operator 备份的数据恢复到 TiDB 集群的操作过程。底层通过使用 [`loader`](/reference/tools/loader.md) 来恢复数据。

本文使用的备份方式基于 TiDB Operator 新版（v1.1 及以上）的 CRD 实现。基于 Helm Charts 实现的备份恢复方式可参考[基于 Helm Charts 实现的 TiDB 集群备份恢复](/tidb-in-kubernetes/maintain/backup-and-restore/charts.md)。

以下示例将兼容 S3 的存储（指定路径）上的备份数据恢复到 TiDB 集群。

This document describes how to restore the TiDB cluster data backed up by TiDB Operator in Kubernetes. For the underlying implementation, [`loader`](/reference/tools/loader.md) is used to perform the restoration.

The restoration method described in this document is implemented based on CustomResourceDefinition (CRD) in TiDB Operator v1.1 or later versions. For the restoration method implemented based on Helm Charts, refer to [Back up and Restore TiDB Cluster Data Based on Helm Charts](/tidb-in-kubernetes/maintain/backup-and-restore/charts.md).

This document shows a use case in which the backup data stored in the specified path on the S3-compatible storage is restored to the TiDB cluster.

## 环境准备

## Prerequisites

1. 下载文件 [`backup-rbac.yaml`](https://github.com/pingcap/tidb-operator/blob/master/manifests/backup/backup-rbac.yaml)，并在 `test2` 这个 namespace 中创建恢复备份所需的 RBAC 资源，所需命令如下：

1. Download [`backup-rbac.yaml`](https://github.com/pingcap/tidb-operator/blob/master/manifests/backup/backup-rbac.yaml) and execute the following command to create the role-based access control (RBAC) resources in the `test2` namespace:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f backup-rbac.yaml -n test2
    ```

2. 创建 `restore-demo2-tidb-secret` secret，该 secret 存放用来访问 TiDB 集群的 root 账号和密钥：

2. Create the `restore-demo2-tidb-secret` secret which stores the root account and password used to access the TiDB cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl create secret generic restore-demo2-tidb-secret --from-literal=user=root --from-literal=password=<password> --namespace=test2
    ```

## Restoration process

1. Create the restore custom resource (CR) and restore the backup data to the TiDB cluster:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl apply -f restore.yaml
    ```

    The `restore.yaml` file has the following content:

    ```yaml
    ---
    apiVersion: pingcap.com/v1alpha1
    kind: Restore
    metadata:
      name: demo2-restore
      namespace: test2
    spec:
      to:
        host: <tidb-host-ip>
        port: <tidb-port>
        user: <tidb-user>
        secretName: restore-demo2-tidb-secret
      s3:
        provider: ceph
        endpoint: http://10.233.2.161
        secretName: ceph-secret
        path: s3://<path-to-backup>
      storageClassName: local-storage
      storageSize: 1Gi
    ```

2. After creating the `Restore` CR, execute the following command to check the restoration status:

    {{< copyable "shell-regular" >}}

     ```shell
     kubectl get rt -n test2 -owide
     ```

以上示例将兼容 S3 的存储（`spec.s3.path` 路径下）中的备份数据恢复到 TiDB 集群 (`spec.to.host`)。有关兼容 S3 的存储的配置项，可以参考 [backup-s3.yaml](/tidb-in-kubernetes/maintain/backup-and-restore/backup-s3.md#备份数据到兼容-s3-的存储)。

In the above example, the backup data stored in the `spec.s3.path` path on the S3-compatible storage is restored to the `spec.to.host` TiDB cluster. For the configuration of the S3-compatible storage, refer to [backup-s3.yaml](/tidb-in-kubernetes/maintain/backup-and-restore/backup-s3.md#ad-hoc-backup-process).

更多 `Restore` CR 字段的详细解释：

More `Restore` CRs are as described follows:

* `.spec.metadata.namespace`: the namespace where the `Restore` CR is located.
* `.spec.to.host`: the accessing address of the TiDB cluster to be restored.
* `.spec.to.port`: the accessing port of the TiDB cluster to be restored.
* `.spec.to.user`: the accessing user of the TiDB cluster to be restored.
* `.spec.to.tidbSecretName`: the secrete of the credential required by the TiDB cluster to be restored.
* `.spec.storageClassName`: the persistent volume (PV) type specified for the restoration. If this item is not specified, the value of the `default-backup-storage-class-name` parameter (`standard` by default, specified when TiDB Operator is started) is used by default.
* `.spec.storageSize`: the PV size specified for the restoration. This value must be greater than size of the backed up TiDB cluster.
