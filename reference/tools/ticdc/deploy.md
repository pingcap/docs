---
title: Deploy and use TiCDC
category: reference
---

# Deploy and use TiCDC

This document introduces how to deploy and use TiCDC to replicate incremental data.

## Step 1: Deploy TiCDC clusters

Suppose that there is a PD node (the client URL is `10.0.10.25:2379`) in the PD cluster that can provide services. To deploy three TiCDC nodes, start the TiCDC cluster using the following commands. If you have specified the same PD address, the newly started TiCDC nodes can automatically be added to the TiCDC cluster.

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --status-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --status-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --status-addr=127.0.0.1:8303
```

## Step 2: Create replication task

To replicate all upstream database tables (except system tables) to the downstream MySQL, use the following command to create the replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/"
```

The parameters in the above command are described as follows:

- `pd`: The URL of the PD client.
- `start-ts`: Specifies the starting TSO of the replication task. If this parameter is not specified or specified as `0`, the current TSO is used as the starting TSO of the replication task.
- `sink-uri`: The sink address. Currently, the address can be configured to `mysql`, `tidb`, or `kafka`. For how to configure sink URI, refer to [Configure Sink URI](/reference/tools/ticdc/sink.md).
- `config`: The configuration of the replication task. Currently, this configuration supports the black & white lists and skipping specific transaction of certain `commit-ts`.

After executing the above command, TiCDC starts to replicate data to the downstream MySQL (`127.0.0.1:3306`) from the specified `start-ts` (`415238226621235200`).

To replicate data to a Kafka cluster, first create the topic in the Kafka cluster (for example, `cdc-test` in the following example is a topic), create partitions, and use the following command to create the replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="kafka://10.0.10.30:9092/cdc-test"
```

After executing the above command, TiCDC starts to replicate data to the downstream Kafka (`10.0.10.30:9092`) from the specified `start-ts`.
