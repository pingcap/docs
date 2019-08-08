---
title: Maintain TiDB Binlog
summary: Learn how to maintain TiDB Binlog of a TiDB cluster in Kubernetes.
category: how-to
---

# Maintain TiDB Binlog

This document describes how to maintain [TiDB Binlog](reference/tidb-binlog-overview.md)  of a TiDB cluster in Kubernetes.

## Prerequisites

- [Deploy TiDB Operator](tidb-in-kubernetes/deploy/tidb-operator.md);
- [Install Helm](tidb-in-kubernetes/reference/tools/in-kubernetes.md#use-helm) and configure it with the official PingCAP chart.

## Enable TiDB Binlog of a TiDB cluster

TiDB Binlog is disabled in the TiDB cluster by default. To create a TiDB cluster with TiDB Binlog enabled or enable  TiDB Binlog in existing TiDB cluster, modify the `values.yaml` file:

* Set `binlog.pump.create` to `true`.
* Set `binlog.drainer.create` to `true`.
* Set `binlog.pump.storageClassName` and `binlog.drainer.storageClassName` to an available `storageClass` in your Kubernetes cluster.
* Set `binlog.drainer.destDBType` to your desired downstream storage as needed, which is explained in details below.

TiDB Binlog supports three types of downstream storage:

* PersistenceVolume: the default downstream storage. You can consider configuring a large PV for `drainer` (by modifying `binlog.drainer.storage`) in this case.
* MySQL compatible databases: enabled by setting `binlog.drainer.destDBType` to `mysql`. Meanwhile, you must configure the address and credential of the target database in `binlog.drainer.mysql`.
* Apache Kafka: enabled by setting `binlog.drainer.destDBType` to `kafka`. Meanwhile, you must configure the zookeeper address and Kafka address of the target cluster in `binlog.drainer.kafka`.

Then, create a new TiDB cluster or update an existing cluster:

* Create a new TiDB cluster with TiDB Binlog enabled:

    {{< copyable "shell-regular" >}}

    ```shell
    helm install pingcap/tidb-cluster --name=<release-name> --namespace=<namespace> --version=<chart-version> -f <values-file>
    ```

* Update a new TiDB cluster to enable TiDB Binlog:

    {{< copyable "shell-regular" >}}

    ```shell
    helm upgrade <release-name> pingcap/tidb-cluster --version=<chart-version> -f <values-file>
    ```

## Deploy Multiple Drainers

By default, only one downstream drainer will be created. You can install the `tidb-drainer` Helm chart to deploy more drainers for a TiDB cluster.

1. Make sure the PingCAP helm repository is up to date:

    {{< copyable "shell-regular" >}}

    ```shell
    helm repo update
    ```

    {{< copyable "shell-regular" >}}

    ```shell
    helm search tidb-drainer -l
    ```

2. Get the default `values.yaml` file to facilitate customization:

    ```shell
    helm inspect values pingcap/tidb-cluster --version=<chartVersion> > values.yaml
    ```

3. Modify the `values.yaml` file to specify the source TiDB cluster and the downstream of the drainer, here is an example:

    ```yaml
    clusterName: example-tidb
    clusterVersion: v3.0.0
    storageClassName: local-storage
    storage: 10Gi
    config: |
      [syncer]
      worker-count = 16
      detect-interval = 10
      disable-dispatch = false
      ignore-schemas = "INFORMATION_SCHEMA,PERFORMANCE_SCHEMA,mysql"
      safe-mode = false
      txn-batch = 20
      db-type = "tidb"
      [syncer.to]
      host = "slave-tidb"
      user = "root"
      password = ""
      port = 4000
    ```

    The `clusterName` and `clusterVersion` must match the desired source TiDB cluster.

    You can refer to [TiDB Binlog Drainer Configurations in Kubernetes](reference/configuration/tidb-drainer.md) for the complete configuration reference.

4. Deploy the drainer:

    {{< copyable "shell-regular" >}}

    ```shell
    helm deploy pingcap/tidb-drainer --name=<release-name> --namespace=<namespace> --version=<chart-version> -f values.yaml
    ```

    > **Note:**
    >
    > This chart must be installed to the same namespace with the source TiDB cluster.