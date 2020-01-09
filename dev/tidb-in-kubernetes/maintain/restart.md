---
title: Restart TiDB Cluster in Kubernetes
summary: Learn how to restart the TiDB cluster in the Kubernetes cluster.
category: how-to
---

# Restart TiDB Cluster in Kubernetes

This document describes how to forcibly restart the TiDB cluster in the Kubernetes cluster, including restarting a Pod, restarting all Pods of a component, and restarting all Pods of the TiDB cluster.

> **Note:**
>
> TiDB Operator v1.0.x only supports restarting the Pod in a forcible way.
>
> - If the PD Pod being restarted is the PD Leader, its leadership does not automatically shift, causing the PD service to pause momentarily.
> - If the TiKV Pod being restarted contains a Region Leader of the TiKV cluster, its leadership does not automatically shift, causing the request for accessing the corresponding data to fail.
> - Restarting the TiDB Pod causes the request for accessing this Pod to fail.

## Forcibly restart a Pod

Execute the following command to forcibly restart a Pod:

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> <pod-name>
```

## Forcibly restart all Pods of a component

Execute the following command to check the Pod list of a component:

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n <namespace> -l app.kubernetes.io/component=<component-name>
```

Execute the following command to forcibly restart all Pods of a component:

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> -l app.kubernetes.io/component=<component-name>
```

> **Note:**
>
> + Replace `<component-name>` in the above commands with `pd`, `tidb`, or `tikv` to forcibly restart all Pods of the `PD`, `TiDB`, or `TiKV` component.
> + Replace `<namespace>` in the above commands with your own namespace.

## Forcibly restart all Pods of the TiDB cluster

Execute the following command to check the Pod list of the TiDB cluster (including `monitor` and `discovery`):

{{< copyable "shell-regular" >}}

```shell
kubectl get pod -n <namespace> -l  app.kubernetes.io/instance=<tidb-cluster-name>
```

Execute the following command to forcibly restart all Pods of the TiDB cluster (including `monitor` and `discovery`):

{{< copyable "shell-regular" >}}

```shell
kubectl delete pod -n <namespace> -l  app.kubernetes.io/instance=<tidb-cluster-name>
```

> **Note:**
>
> Replace `<namespace>` and `<tidb-cluster-name>` in the above commands with your own namespace and TiDB cluster name.
