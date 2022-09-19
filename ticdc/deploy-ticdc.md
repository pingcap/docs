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
cdc server --cluster-id=default --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --cluster-id=default --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --cluster-id=default --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

## Description of TiCDC `cdc server` command-line parameters

The following are descriptions of options available in the `cdc server` command:

- `addr`: The listening address of TiCDC, the HTTP API address, and the Prometheus address of the TiCDC service. The default value is `127.0.0.1:8300`.
- `advertise-addr`: The advertised address via which clients access TiCDC. If unspecified, the value is the same as that of `addr`.
- `pd`: A comma-separated list of PD endpoints.
- `config`: The address of the configuration file that TiCDC uses (optional). This option is supported since TiCDC v5.0.0. This option can be used in the TiCDC deployment since TiUP v1.4.0.
- `data-dir`: Specifies the directory that TiCDC uses when it needs to use disks to store files. Unified Sorter uses this directory to store temporary files. It is recommended to ensure that the free disk space for this directory is greater than or equal to 500 GiB. For more details, see [Unified Sorter](/ticdc/manage-ticdc.md#unified-sorter). If you are using TiUP, you can configure `data_dir` in the [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers) section, or directly use the default `data_dir` path in `global`.
- `gc-ttl`: The TTL (Time To Live) of the service level `GC safepoint` in PD set by TiCDC, and the duration that the replication task can suspend, in seconds. The default value is `86400`, which means 24 hours. Note: Suspending of the TiCDC replication task affects the progress of TiCDC GC safepoint, which means that it affects the progress of upstream TiDB GC, as detailed in [Complete Behavior of TiCDC GC safepoint](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint).
- `log-file`: The path to which logs are output when the TiCDC process is running. If this parameter is not specified, logs are written to the standard output (stdout).
- `log-level`: The log level when the TiCDC process is running. The default value is `"info"`.
- `ca`: Specifies the path of the CA certificate file in PEM format for TLS connection (optional).
- `cert`: Specifies the path of the certificate file in PEM format for TLS connection (optional).
- `cert-allowed-cn`: Specifies the path of the common name in PEM format for TLS connection (optional).
- `key`: Specifies the path of the private key file in PEM format for TLS connection (optional).
- `tz`: Time zone used by the TiCDC service. TiCDC uses this time zone when it internally converts time data types such as `TIMESTAMP` or when it replicates data to the downstream. The default is the local time zone in which the process runs. If you specify `time-zone` (in `sink-uri`) and `tz` at the time, the internal TiCDC processes use the time zone specified by `tz`, and the sink uses the time zone specified by `time-zone` for replicating data to the downstream.
- `cluster-id`: (optional) The ID of the TiCDC cluster. The default value is `default`. `cluster-id` is the unique identifier of a TiCDC cluster. TiCDC nodes with the same `cluster-id` belong to the same cluster. The length of a `cluster-id` is 128 characters at most. `cluster-id` must follow the pattern of `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$` and cannot be one of the following: `owner`, `capture`, `task`, `changefeed`, `job`, and `meta`.

## Rolling upgrade TiCDC using TiUP

From v6.3.0, TiCDC supports rolling upgrades using TiUP. This feature helps keep TiCDC replication latency within a stable range without drastic fluctuations. To perform a rolling upgrade, ensure that:

* At least two TiCDC instances are running in the cluster.
* The TiUP version is v1.11.0 or later.

If the preceding conditions are met, you can run the `tiup cluster upgrade` command to perform a rolling upgrade of the cluster:

```shell
tiup cluster upgrade test-cluster ${target-version} --transfer-timeout 600 --force false
```