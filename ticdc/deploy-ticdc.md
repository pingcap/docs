---
title: Deploy TiCDC
summary: Learn how to deploy TiCDC and the hardware and software recommendations for deploying and running it.
---

# Deploy TiCDC

This document describes how to deploy a TiCDC cluster and the hardware and software recommendations for deploying and running it. You can either deploy TiCDC along with a new TiDB cluster or add the TiCDC component to an existing TiDB cluster. Generally, it is recommended that you deploy TiCDC using TiUP. In addition, you can also deploy it using binary as needed.

## Software and hardware recommendations

In production environments, the recommendations of software and hardware for TiCDC are as follows:

| Linux OS       | Version         |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 or later versions   |
| CentOS                   | 7.3 or later versions   |

| CPU | Memory | Disk type | Network | Number of TiCDC cluster instances (minimum requirements for production environment) |
| :--- | :--- | :--- | :--- | :--- |
| 16 core+ | 64 GB+ | SSD | 10 Gigabit network card (2 preferred） | 2 |

For more information, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md).

## Deploy a new TiDB cluster that includes TiCDC using TiUP

When you deploy a new TiDB cluster using TiUP, you can also deploy TiCDC at the same time. You only need to add the `cdc_servers` section in the initialization configuration file that TiUP uses to start the TiDB cluster. For detailed operations, see [Edit the initialization configuration file](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file). For detailed configurable fields, see [Configure `cdc_servers` using TiUP](/tiup/tiup-cluster-topology-reference.md#cdc_servers).

## Add TiCDC to an existing TiDB cluster using TiUP

You can also use TiUP to add the TiCDC component to an existing TiDB cluster. Take the following procedures:

1. Make sure that the current TiDB version supports TiCDC; otherwise, you need to upgrade the TiDB cluster to `v4.0.0-rc.1` or later versions. Since v4.0.6, TiCDC has become a feature for general availability (GA). It is recommended that you use v4.0.6 or later versions.

2. To deploy TiCDC, refer to [Scale out a TiCDC cluster](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster).

## Add TiCDC to an existing TiDB cluster using binary (not recommended)

Suppose that the PD cluster has a PD node (the client URL is `10.0.10.25:2379`) that can provide services. If you want to deploy three TiCDC nodes, start the TiCDC cluster by executing the following commands. You only need to specify the same PD address, and the newly started nodes automatically join the TiCDC cluster.

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## Description of TiCDC `cdc server` command-line parameters

The following are descriptions of options available in the `cdc server` command:

<<<<<<< HEAD
- `addr`: The listening address of TiCDC, the HTTP API address, and the Prometheus address of the TiCDC service. The default value is `127.0.0.1:8300`.
- `advertise-addr`: The advertised address via which clients access TiCDC. If unspecified, the value is the same as that of `addr`.
- `pd`: A comma-separated list of PD endpoints.
- `config`: The address of the configuration file that TiCDC uses (optional). This option is supported since TiCDC v5.0.0. This option can be used in the TiCDC deployment since TiUP v1.4.0.
- `data-dir`: Specifies the directory that TiCDC uses when it needs to use disks to store files. Unified Sorter uses this directory to store temporary files. It is recommended to ensure that the free disk space for this directory is greater than or equal to 500 GiB. For more details, see [Unified Sorter](/ticdc/manage-ticdc.md#unified-sorter). If you are using TiUP, you can configure `data_dir` in the [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers) section, or directly use the default `data_dir` path in `global`.
- `gc-ttl`: The TTL (Time To Live) of the service level `GC safepoint` in PD set by TiCDC, and the duration that the replication task can suspend, in seconds. The default value is `86400`, which means 24 hours. Note: Suspending of the TiCDC replication task affects the progress of TiCDC GC safepoint, which means that it affects the progress of upstream TiDB GC, as detailed in [Complete Behavior of TiCDC GC safepoint](/ticdc/troubleshoot-ticdc.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint).
- `log-file`: The path to which logs are output when the TiCDC process is running. If this parameter is not specified, logs are written to the standard output (stdout).
- `log-level`: The log level when the TiCDC process is running. The default value is `"info"`.
- `ca`: Specifies the path of the CA certificate file in PEM format for TLS connection (optional).
- `cert`: Specifies the path of the certificate file in PEM format for TLS connection (optional).
- `cert-allowed-cn`: Specifies the path of the common name in PEM format for TLS connection (optional).
- `key`: Specifies the path of the private key file in PEM format for TLS connection (optional).
- `tz`: Time zone used by the TiCDC service. TiCDC uses this time zone when it internally converts time data types such as `TIMESTAMP` or when it replicates data to the downstream. The default is the local time zone in which the process runs. If you specify `time-zone` (in `sink-uri`) and `tz` at the time, the internal TiCDC processes use the time zone specified by `tz`, and the sink uses the time zone specified by `time-zone` for replicating data to the downstream.
=======
> **Note:**
>
> Before installing TiCDC, ensure that you have [manually configured the SSH mutual trust and sudo without password](/check-before-deployment.md#manually-configure-the-ssh-mutual-trust-and-sudo-without-password) between the TiUP control machine and the TiCDC host.

## Add or scale out TiCDC to an existing TiDB cluster using TiUP

The method of scaling out a TiCDC cluster is similar to that of deploying one. It is recommended to use TiUP to perform the scale-out.

1. Create a `scale-out.yml` file to add the TiCDC node information. The following is an example:

    ```shell
    cdc_servers:
      - host: 10.1.1.1
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.1.1.2
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
      - host: 10.0.1.4:8300
        gc-ttl: 86400
        data_dir: /tidb-data/cdc-8300
    ```

2. Run the scale-out command on the TiUP control machine:

    ```shell
    tiup cluster scale-out <cluster-name> scale-out.yml
    ```

For more use cases, see [Scale out a TiCDC cluster](/scale-tidb-using-tiup.md#scale-out-a-ticdc-cluster).

## Delete or scale in TiCDC from an existing TiDB cluster using TiUP

It is recommended that you use TiUP to scale in TiCDC nodes. The following is the scale-in command:

```shell
tiup cluster scale-in <cluster-name> --node 10.0.1.4:8300
```

For more use cases, see [Scale in a TiCDC cluster](/scale-tidb-using-tiup.md#scale-in-a-ticdc-cluster).

## Upgrade TiCDC using TiUP

You can upgrade TiDB clusters using TiUP, during which TiCDC is upgraded as well. After you execute the upgrade command, TiUP automatically upgrades the TiCDC component. The following is an example:

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> <version> --transfer-timeout 600
```

> **Note:**
>
> In the preceding command, you need to replace `<cluster-name>` and `<version>` with the actual cluster name and cluster version. For example, the version can be v7.0.0.

### Upgrade cautions

When you upgrade a TiCDC cluster, you need to pay attention to the following:

- TiCDC v4.0.2 reconfigured `changefeed`. For details, see [Configuration file compatibility notes](/ticdc/ticdc-compatibility.md#cli-and-configuration-file-compatibility).
- If you encounter any problem during the upgrade, you can refer to [upgrade FAQs](/upgrade-tidb-using-tiup.md#faq) for solutions.
- Since v6.3.0, TiCDC supports rolling upgrade. During the upgrade, the replication latency is stable and does not fluctuate significantly. Rolling upgrade takes effect automatically if the following conditions are met:

- TiCDC is v6.3.0 or later.
    - TiUP is v1.11.3 or later.
    - At least two TiCDC instances are running in the cluster.

## Modify TiCDC cluster configurations using TiUP

This section describes how to use the [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) command to modify the configurations of TiCDC. In the following example, it is assumed that you need to change the default value of `gc-ttl` from `86400` to `172800` (48 hours).

1. Run the `tiup cluster edit-config` command. Replace `<cluster-name>` with the actual cluster name:

   ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. In the vi editor, modify the `cdc` [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs):

    ```shell
    server_configs:
      tidb: {}
      tikv: {}
      pd: {}
      tiflash: {}
      tiflash-learner: {}
      pump: {}
      drainer: {}
      cdc:
        gc-ttl: 172800
    ```

    In the preceding command, `gc-ttl` is set to 48 hours.

3. Run the `tiup cluster reload -R cdc` command to reload the configuration.

## Stop and start TiCDC using TiUP

You can use TiUP to easily stop and start TiCDC nodes. The commands are as follows:

- Stop TiCDC: `tiup cluster stop -R cdc`
- Start TiCDC: `tiup cluster start -R cdc`
- Restart TiCDC: `tiup cluster restart -R cdc`

## Enable TLS for TiCDC

See [Enable TLS Between TiDB Components](/enable-tls-between-components.md).

## View TiCDC status using the command-line tool

Run the following command to view the TiCDC cluster status. Note that you need to replace `v<CLUSTER_VERSION>` with the TiCDC cluster version, such as `v6.5.0`:

```shell
tiup ctl:v<CLUSTER_VERSION> cdc capture list --server=http://10.0.10.25:8300
```

```shell
[
  {
    "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
    "is-owner": true,
    "address": "127.0.0.1:8300",
    "cluster-id": "default"
  },
  {
    "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
    "is-owner": false,
    "address": "127.0.0.1:8301",
    "cluster-id": "default"
  }
]
```

- `id`: Indicates the ID of the service process.
- `is-owner`: Indicates whether the service process is the owner node.
- `address`: Indicates the address via which the service process provides interface to the outside.
- `cluster-id`: Indicates the ID of the TiCDC cluster. The default value is `default`.
>>>>>>> d4713e770 (tiup: fix the scale-out yaml example (#13327))
