---
title: Deploy TiDB in Kubernetes Using kind
summary: Learn how to deploy a TiDB cluster in Kubernetes using kind.
category: how-to
---

# Deploy TiDB in Kubernetes Using kind

This tutorial shows how to deploy the [TiDB Operator](https://github.com/pingcap/tidb-operator) and a TiDB cluster in Kubernetes on your laptop (Linux or macOS) using [kind](https://kind.sigs.k8s.io/).

kind is a tool for running local Kubernetes clusters using Docker container as cluster nodes. It is developed for testing local Kubernetes clusters, initially targeting the conformance tests. The cluster version depends on the node image that your kind version uses, but you can specify the image to be used for the nodes and choose any other published version. Refer to [Docker hub](https://hub.docker.com/r/kindest/node/tags) to see available tags.

> **Warning:**
>
> This deployment is for testing only. DO NOT USE in production!

## Prerequisites

Before deployment, make sure the following requirements are satisfied:

- Resources requirement: CPU 2+, Memory 4G+

    > **Note:**
    >
    > For macOS, you need to allocate 2+ CPU and 4G+ Memory to Docker. For details, see [Docker for Mac configuration](https://docs.docker.com/docker-for-mac/#advanced).

- [Docker](https://docs.docker.com/install/): version >= 17.03

- [Helm Client](https://github.com/helm/helm/blob/master/docs/install.md#installing-the-helm-client): version >= 2.9.0 and < 3.0.0

- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl): version >= 1.10, 1.13 or later recommended

    > **Note:**
    >
    > The output might vary slightly for different versions of `kubectl`.

- [kind](https://kind.sigs.k8s.io/docs/user/quick-start/): version >= 0.4.0
- The value of [net.ipv4.ip_forward](https://linuxconfig.org/how-to-turn-on-off-ip-forwarding-in-linux) should be set to 1

## Step 1: Create a Kubernetes cluster using kind

First, make sure that the Docker is running. Then, you can create a local Kubernetes cluster with the script in our repository. Follow the steps below:

1. Clone the code:

    {{< copyable "shell-regular" >}}

    ``` shell
    git clone --depth=1 https://github.com/pingcap/tidb-operator && \
    cd tidb-operator
    ```

2. Run the script and create a local Kubernetes cluster:

    {{< copyable "shell-regular" >}}

    ``` shell
    hack/kind-cluster-build.sh
    ```

    > **Note:**
    >
    > In this script, the Kubernetes version defaults to v1.12.8, and the Kubernetes cluster starts with six nodes and  for each node the mount count set to 9. You can configure these items in startup options.
    >
    > {{< copyable "shell-regular" >}}
    >
    > ```shell
    > hack/kind-cluster-build.sh --nodeNum 2 --k8sVersion v1.14.6 --volumeNum 3
    > ```

3. Execute the following command to set the default configuration files of kubectl to `kube-config`, so as to connect the local Kubernetes cluster.

    {{< copyable "shell-regular" >}}

    ```shell
    export KUBECONFIG="$(kind get kubeconfig-path)"
    ```

4. You can verify whether the Kubernetes cluster is on and running by using the following command:

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl cluster-info
    ```

    The response should be like this:

    ``` shell
    Kubernetes master is running at https://127.0.0.1:50295
    KubeDNS is running at https://127.0.0.1:50295/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
    ```

5. Check the `storageClass` of the cluster:

    {{< copyable "shell-regular" >}}

    ``` shell
    kubectl get storageClass
    ```

    The response should be like this:

    ``` shell
    NAME                 PROVISIONER                    AGE
    local-storage        kubernetes.io/no-provisioner   7m50s
    standard (default)   kubernetes.io/host-path        8m29s
    ```

## Step 2: Install TiDB Operator in the Kubernetes

Refer steps in [Deploy TiDB Operator](/dev/tidb-in-kubernetes/deploy/tidb-operator.md#install-tidb-operator).

## Step 3: Deploy a TiDB cluster in the Kubernetes cluster

Refer steps in [Deploy TiDB on General Kubernetes](/dev/tidb-in-kubernetes/deploy/general-kubernetes.md#deploy-tidb-cluster).

## Access the database and monitor dashboards

Refer the steps in [](/dev/tidb-in-kubernetes/monitor/tidb-in-kubernetes.md#view-the-monitoring-dashboard).

## Destroy the TiDB and Kubernetes cluster

To destroy the local TiDB cluster, refer the steps in [Destroy TiDB Clusters in Kubernetes](/dev/tidb-in-kubernetes/maintain/destroy-tidb-cluster.md).

To destroy the Kubernetes cluster, execute the following command:

{{< copyable "shell-regular" >}}

``` shell
kind delete cluster
```
