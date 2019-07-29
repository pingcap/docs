---
title: TiDB FAQs in Kubernetes
summary: Learn about TiDB FAQs in Kubernetes.
category: FAQ
---

# TiDB FAQs in Kubernetes

This document collects frequently asked questions (FAQs) about the TiDB cluster in Kubernetes.

## How to modify time zone settings？

The default time zone setting for each component container of a TiDB cluster in Kubernetes is UTC. To modify this setting, take the steps below based on your cluster status:

* If it is the first time you deploy the cluster:

    In the `values.yaml` file of the TiDB cluster, modify the `timezone` setting. For example, you can set it to `timezone: Asia/Shanghai` before you deploy the TiDB cluster.

* If the cluster is running:

    * In the `values.yaml` file of the TiDB cluster, modify `timezone` settings in the `values.yaml` file of the TiDB cluster. For example, you can set it to `timezone: Asia/Shanghai` and then upgrade the TiDB cluster.
    * Refer to [Time Zone Support](/how-to/configure/time-zone.md) to modify TiDB service time zone settings.

## Can HPA or VPA be configured on TiDB components?

Currently, TiDB cluster does not support HPA (Horizontal Pod Autoscaling) or VPA (Vertical Pod Autoscaling), because it is difficult to achieve autoscaling on applications with state such as database. Autoscaling can not be achieved merely by the monitoring data of CPU and memory.

## What scenarios require manual intervention when I use TiDB Operator to orchestrate TiDB clusters?

Except for the operation of the Kubernetes cluster itself, TiDB Operator has the following two scenarios that might require manual intervention:

* Adjusting the cluster after the auto-failover of TiKV. Detailed reference: [Auto-Failover](tidb-in-kubernetes/maintain/auto-failover.md)
* Maintaining or dropping the specific Kubernetes nodes. Detailed reference: [Maintaining Nodes](tidb-in-kubernetes/maintain/kubernetes-node.md)

## What is the recommended deployment topology when I use TiDB Operator to orchestrate a TiDB cluster on a public cloud?

To achieve high availability and data security, it is recommended for you to deploy at least three Available Zones in a TiDB cluster in a production environment.

For the relationship of deployment topology between TiDB cluster and TiDB services, TiDB Operator supports the following three deployment modes, each of which has its own merits and demerits. Specific selection must be based on actual business needs.

* Deploy TiDB clusters and TiDB services in the same Kubernetes cluster in the same VPC;
* Deploy TiDB clusters and TiDB services in different Kubernetes clusters in the same VPC;
* Deploy TiDB clusters and TiDB services in different Kubernetes clusters in different VPCs.

## Does TiDB Operator supports TiSpark?

TiS Operator does not yet support the automatic orchestration of TiSpark.

If you want to add TiSpark components to TiDB in Kubernetes, you must maintain Spark on your own in **the same** Kubernetes cluster. You must ensure that Spark can access the IP and ports of PD and TiKV instances, and install the TiSpark plugin for Spark. [TiSpark](/reference/tispark.md#deploy-tiSpark-on-the-existing-spark-cluster) offers a detailed guide for you to install the TiSpark plugin.

Refer to [Spark on Kubernetes](http://spark.apache.org/docs/latest/running-on-kubernetes.html) to maintain Spark in Kubernetes.

## How to check the configuration of TiDB cluster?

To check the configuration of the PD, TiKV, and TiDB components of the current cluster, run the following command:

* Check the PD configuration file:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <pdPodName> -n <namespace> -- cat /etc/pd/pd.toml
    ```

* Check the TiKV configuration file:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <tikvPodName> -n <namespace> -- cat /etc/tikv/tikv.toml
    ```

* Check the TiDB configuration file:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl exec -it <tidbPodName> -c tidb -n <namespace> -- cat /etc/tidb/tidb.toml
    ```
