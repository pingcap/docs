---
title: Manage TiCDC Cluster and Replication Tasks
summary: Learn how to manage a TiCDC cluster and replication tasks.
aliases: ['/docs/dev/ticdc/manage-ticdc/','/docs/dev/reference/tools/ticdc/manage/']
---

# Manage TiCDC Cluster and Replication Tasks

This document describes how to upgrade TiCDC cluster and modify the configuration of TiCDC cluster using TiUP, and how to manage the TiCDC cluster and replication tasks using the command-line tool `cdc cli`.

You can also use the HTTP interface (the TiCDC OpenAPI feature) to manage the TiCDC cluster and replication tasks. For details, see [TiCDC OpenAPI](/ticdc/ticdc-open-api.md).

## Upgrade TiCDC using TiUP

This section introduces how to upgrade the TiCDC cluster using TiUP. In the following example, assume that you need to upgrade TiCDC and the entire TiDB cluster to v6.2.0.

{{< copyable "shell-regular" >}}

```shell
tiup update --self && \
tiup update --all && \
tiup cluster upgrade <cluster-name> v6.2.0
```

### Notes for upgrade

* The `changefeed` configuration has changed in TiCDC v4.0.2. See [Compatibility notes for the configuration file](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file) for details.
* If you encounter any issues, see [Upgrade TiDB using TiUP - FAQ](/upgrade-tidb-using-tiup.md#faq).

## Modify TiCDC configuration using TiUP

This section introduces how to modify the configuration of TiCDC cluster using the  [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) command of TiUP. The following example changes the value of `gc-ttl` from the default `86400` to `3600`, namely, one hour.

First, execute the following command. You need to replace `<cluster-name>` with your actual cluster name.

{{< copyable "shell-regular" >}}

```shell
tiup cluster edit-config <cluster-name>
```

Then, enter the vi editor page and modify the `cdc` configuraion under [`server-configs`](/tiup/tiup-cluster-topology-reference.md#server_configs). The configuration is shown below:

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
    gc-ttl: 3600
```

After the modification, execute the `tiup cluster reload -R cdc` command to reload the configuration.

## Use TLS

For details about using encrypted data transmission (TLS), see [Enable TLS Between TiDB Components](/enable-tls-between-components.md).

## Use `cdc cli` to manage cluster status and data replication task

This section introduces how to use `cdc cli` to manage a TiCDC cluster and data replication tasks. `cdc cli` is the `cli` sub-command executed using the `cdc` binary. The following description assumes that:

- `cli` commands are executed directly using the `cdc` binary;
- TiCDC listens on `10.0.10.25` and the port is `8300`.

> **Note:**
>
> The IP address and port that TiCDC listens on correspond to the `advertise-client-urls` parameter specified during the `cdc-server` startup. Starting from TiCDC v6.2.0, the `cdc cli` command can directly interact with TiCDC server via TiCDC Open API. You can specify the address of TiCDC server using the `--server` parameter. `--pd` is deprecated and no longer recommended.

If you deploy TiCDC using TiUP, replace `cdc cli` in the following commands with `tiup ctl cdc`.

### Manage TiCDC service progress (`capture`)

- Query the `capture` list:

    ```shell
    cdc cli capture list --server=http://10.0.10.25:8300
    ```

    ```json
    [
      {
        "id": "806e3a1b-0e31-477f-9dd6-f3f2c570abdd",
        "is-owner": true,
        "address": "127.0.0.1:8300"
      },
      {
        "id": "ea2a4203-56fe-43a6-b442-7b295f458ebc",
        "is-owner": false,
        "address": "127.0.0.1:8301"
      }
    ]
    ```

    - `id`: The ID of the service process.
    - `is-owner`: Indicates whether the service process is the owner node.
    - `address`: The address via which the service process provides interface to the outside.

### Manage replication tasks (`changefeed`)

#### State transfer of replication tasks

The state of a replication task represents the running status of the replication task. During the running of TiCDC, replication tasks might fail with errors, be manually paused, resumed, or reach the specified `TargetTs`. These behaviors can lead to the change of the replication task state. This section describes the states of TiCDC replication tasks and the transfer relationships between states.

![TiCDC state transfer](/media/ticdc/ticdc-state-transfer.png)

The states in the above state transfer diagram are described as follows:

- `Normal`: The replication task runs normally and the checkpoint-ts proceeds normally.
- `Stopped`: The replication task is stopped, because the user manually pauses the changefeed. The changefeed in this state blocks GC operations.
- `Error`: The replication task returns an error. The replication cannot continue due to some recoverable errors. The changefeed in this state keeps trying to resume until the state transfers to `Normal`. The changefeed in this state blocks GC operations.
- `Finished`: The replication task is finished and has reached the preset `TargetTs`. The changefeed in this state does not block GC operations.
- `Failed`: The replication task fails. Due to some unrecoverable errors, the replication task cannot resume and cannot be recovered. The changefeed in this state does not block GC operations.

The numbers in the above state transfer diagram are described as follows.

- ① Execute the `changefeed pause` command
- ② Execute the `changefeed resume` command to resume the replication task
- ③ Recoverable errors occur during the `changefeed` operation, and the operation is resumed automatically.
- ④ Execute the `changefeed resume` command to resume the replication task
- ⑤ Recoverable errors occur during the `changefeed` operation
- ⑥ `changefeed` has reached the preset `TargetTs`, and the replication is automatically stopped.
- ⑦ `changefeed` suspended longer than the duration specified by `gc-ttl`, and cannot be resumed.
- ⑧ `changefeed` experienced an unrecoverable error when trying to execute automatic recovery.

#### Create a replication task

Execute the following commands to create a replication task:

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":true,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--changefeed-id`: The ID of the replication task. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the replication task. Configure `--sink-uri` according to the following format. Currently, the scheme supports `mysql`/`tidb`/`kafka`/`pulsar`/`s3`/`local`.

    {{< copyable "" >}}

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    When a URI contains special characters, you need to process these special characters using URL encoding.

- `--start-ts`: Specifies the starting TSO of the `changefeed`. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.
- `--target-ts`: Specifies the ending TSO of the `changefeed`. To this TSO, the TiCDC cluster stops pulling data. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--sort-engine`: Specifies the sorting engine for the `changefeed`. Because TiDB and TiKV adopt distributed architectures, TiCDC must sort the data changes before writing them to the sink. This option supports `unified` (by default)/`memory`/`file`.

    - `unified`: When `unified` is used, TiCDC prefers data sorting in memory. If the memory is insufficient, TiCDC automatically uses the disk to store the temporary data. This is the default value of `--sort-engine`.
    - `memory`: Sorts data changes in memory. This option is **deprecated**. It is **NOT recommended** to use it in **any** situation.
    - `file`: Entirely uses the disk to store the temporary data. This option is **deprecated**. It is **NOT recommended** to use it in **any** situation.

- `--config`: Specifies the configuration file of the `changefeed`.
- `sort-dir`: Specifies the temporary file directory used by the sorting engine. **Note that this option is not supported since TiDB v4.0.13, v5.0.3 and v5.1.0. Do not use it any more**.

#### Configure sink URI with `mysql`/`tidb`

Sample configuration:

{{< copyable "shell-regular" >}}

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000&transaction-atomicity=table"
```

The following are descriptions of parameters and parameter values that can be configured for the sink URI with `mysql`/`tidb`:

| Parameter/Parameter Value    | Description                                             |
| :------------ | :------------------------------------------------ |
| `root`        | The username of the downstream database                              |
| `123456`       | The password of the downstream database                                      |
| `127.0.0.1`    | The IP address of the downstream database                               |
| `3306`         | The port for the downstream data                                 |
| `worker-count` | The number of SQL statements that can be concurrently executed to the downstream (optional, `16` by default)       |
| `max-txn-row`  | The size of a transaction batch that can be executed to the downstream (optional, `256` by default) |
| `ssl-ca` | The path of the CA certificate file needed to connect to the downstream MySQL instance (optional)  |
| `ssl-cert` | The path of the certificate file needed to connect to the downstream MySQL instance (optional) |
| `ssl-key` | The path of the certificate key file needed to connect to the downstream MySQL instance (optional) |
| `time-zone` | The time zone used when connecting to the downstream MySQL instance, which is effective since v4.0.8. This is an optional parameter. If this parameter is not specified, the time zone of TiCDC service processes is used. If this parameter is set to an empty value, no time zone is specified when TiCDC connects to the downstream MySQL instance and the default time zone of the downstream is used. |
| `transaction-atomicity`  |  The atomicity level of a transaction. This is an optional parameter, with the default value of `table`. When the value is `table`, TiCDC ensures the atomicity of a single-table transaction. When the value is `none`, TiCDC splits the single-table transaction.  |

#### Configure sink URI with `kafka`

Sample configuration:

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

The following are descriptions of parameters and parameter values that can be configured for the sink URI with `kafka`:

| Parameter/Parameter Value               | Description                                                        |
| :------------------ | :------------------------------------------------------------ |
| `127.0.0.1`          | The IP address of the downstream Kafka services                                 |
| `9092`               | The port for the downstream Kafka                                          |
| `topic-name` | Variable. The name of the Kafka topic |
| `kafka-version`      | The version of the downstream Kafka (optional, `2.4.0` by default. Currently, the earliest supported Kafka version is `0.11.0.2` and the latest one is `2.7.0`. This value needs to be consistent with the actual version of the downstream Kafka)                      |
| `kafka-client-id`    | Specifies the Kafka client ID of the replication task (optional. `TiCDC_sarama_producer_replication ID` by default) |
| `partition-num`      | The number of the downstream Kafka partitions (optional. The value must be **no greater than** the actual number of partitions; otherwise, the replication task cannot be created successfully. `3` by default) |
| `max-message-bytes`  | The maximum size of data that is sent to Kafka broker each time (optional, `10MB` by default). From v5.0.6 and v4.0.6, the default value has changed from 64MB and 256MB to 10MB. |
| `replication-factor` | The number of Kafka message replicas that can be saved (optional, `1` by default)                       |
| `protocol` | The protocol with which messages are output to Kafka. The value options are `canal-json`, `open-protocol`, `canal`, `avro` and `maxwell`.   |
| `auto-create-topic` | Determines whether TiCDC creates the topic automatically when the `topic-name` passed in does not exist in the Kafka cluster (optional, `true` by default) |
| `enable-tidb-extension` | Optional. `false` by default. When the output protocol is `canal-json`, if the value is `true`, TiCDC sends Resolved events and adds the TiDB extension field to the Kafka message. From v6.1.0, this parameter is also applicable to the `avro` protocol. If the value is `true`, TiCDC adds three TiDB extension fields to the Kafka message. |
| `max-batch-size` | New in v4.0.9. If the message protocol supports outputting multiple data changes to one Kafka message, this parameter specifies the maximum number of data changes in one Kafka message. It currently takes effect only when Kafka's `protocol` is `open-protocol`. (optional, `16` by default) |
| `enable-tls` | Whether to use TLS to connect to the downstream Kafka instance (optional, `false` by default) |
| `ca` | The path of the CA certificate file needed to connect to the downstream Kafka instance (optional)  |
| `cert` | The path of the certificate file needed to connect to the downstream Kafka instance (optional) |
| `key` | The path of the certificate key file needed to connect to the downstream Kafka instance (optional) |
| `sasl-user` | The identity (authcid) of SASL/PLAIN or SASL/SCRAM authentication needed to connect to the downstream Kafka instance (optional) |
| `sasl-password` | The password of SASL/PLAIN or SASL/SCRAM authentication needed to connect to the downstream Kafka instance (optional) |
| `sasl-mechanism` | The name of SASL authentication needed to connect to the downstream Kafka instance. The value can be `plain`, `scram-sha-256`, `scram-sha-512`, or `gssapi`. |
| `sasl-gssapi-auth-type` | The gssapi authentication type. Values can be `user` or `keytab` (optional) |
| `sasl-gssapi-keytab-path` | The gssapi keytab path (optional)|
| `sasl-gssapi-kerberos-config-path` | The gssapi kerberos configuration path (optional) |
| `sasl-gssapi-service-name` | The gssapi service name (optional) |
| `sasl-gssapi-user` | The user name of gssapi authentication (optional) |
| `sasl-gssapi-password` | The password of gssapi authentication (optional)  |
| `sasl-gssapi-realm` | The gssapi realm name (optional) |
| `sasl-gssapi-disable-pafxfast` | Whether to disable the gssapi PA-FX-FAST (optional) |
| `dial-timeout` | The timeout in establishing a connection with the downstream Kafka. The default value is `10s` |
| `read-timeout` | The timeout in getting a response returned by the downstream Kafka. The default value is `10s` |
| `write-timeout` | The timeout in sending a request to the downstream Kafka. The default value is `10s` |
| `avro-decimal-handling-mode` | Only effective with the `avro` protocol. Determines how Avro handles the DECIMAL field. The value can be `string` or `precise`, indicating either mapping the DECIMAL field to a string or a precise floating number.  |
| `avro-bigint-unsigned-handling-mode` | Only effective with the `avro` protocol. Determines how Avro handles the BIGINT UNSIGNED field. The value can be `string` or `long`, indicating either mapping the BIGINT UNSIGNED field to a 64-bit signed number or a string.  |

Best practices:

* It is recommended that you create your own Kafka Topic. At a minimum, you need to set the maximum amount of data of each message that the Topic can send to the Kafka broker, and the number of downstream Kafka partitions. When you create a changefeed, these two settings correspond to `max-message-bytes` and `partition-num`, respectively.
* If you create a changefeed with a Topic that does not yet exist, TiCDC will try to create the Topic using the `partition-num` and `replication-factor` parameters. It is recommended that you specify these parameters explicitly.
* In most cases, it is recommended to use the `canal-json` protocol.

> **Note:**
>
> When `protocol` is `open-protocol`, TiCDC tries to avoid generating messages that exceed `max-message-bytes` in length. However, if a row is so large that a single change alone exceeds `max-message-bytes` in length, to avoid silent failure, TiCDC tries to output this message and prints a warning in the log.

#### TiCDC uses the authentication and authorization of Kafka

The following are examples when using Kafka SASL authentication:

- SASL/PLAIN

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
    ```

- SASL/SCRAM

    SCRAM-SHA-256 and SCRAM-SHA-512 are similar to the PLAIN method. You just need to specify `sasl-mechanism` as the corresponding authentication method.

- SASL/GSSAPI

    SASL/GSSAPI `user` authentication:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
    ```

    Values of `sasl-gssapi-user` and `sasl-gssapi-realm` are related to the [principle](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html) specified in kerberos. For example, if the principle is set as `alice/for-kafka@example.com`, then `sasl-gssapi-user` and `sasl-gssapi-realm` are specified as `alice/for-kafka` and `example.com` respectively.

    SASL/GSSAPI `keytab` authentication:

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
    ```

    For more information about SASL/GSSAPI authentication methods, see [Configuring GSSAPI](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html).

- TLS/SSL encryption

    If the Kafka broker has TLS/SSL encryption enabled, you need to add the `-enable-tls=true` parameter to `--sink-uri`. If you want to use self-signed certificates, you also need to specify `ca`, `cert` and `key` in `--sink-uri`.

- ACL authorization

    The minimum set of permissions required for TiCDC to function properly is as follows.

    - The `Create` and `Write` permissions for the Topic [resource type](https://docs.confluent.io/platform/current/kafka/authorization.html#resources).
    - The `DescribeConfigs` permission for the Cluster resource type.

#### Integrate TiCDC with Kafka Connect (Confluent Platform)

To use the [data connectors](https://docs.confluent.io/current/connect/managing/connectors.html) provided by Confluent to stream data to relational or non-relational databases, you need to use the `avro` protocol and provide a URL for [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) in `schema-registry`.

Sample configuration:

{{< copyable "shell-regular" >}}

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --schema-registry="http://127.0.0.1:8081" --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

For detailed integration guide, see [Quick Start Guide on Integrating TiDB with Confluent Platform](/ticdc/integrate-confluent-using-ticdc.md).

#### Configure sink URI with `pulsar`

> **Warning:**
>
> This is still an experimental feature. Do **NOT** use it in a production environment.

Sample configuration:

{{< copyable "shell-regular" >}}

```shell
--sink-uri="pulsar://127.0.0.1:6650/topic-name?connectionTimeout=2s"
```

The following are descriptions of parameters that can be configured for the sink URI with `pulsar`:

| Parameter  | Description                                            |
| :------------------ | :------------------------------------------------------------ |
| `connectionTimeout` | The timeout for establishing a connection to the downstream Pulsar, which is optional and defaults to 30 (seconds) |
| `operationTimeout` | The timeout for performing an operation on the downstream Pulsar, which is optional and defaults to 30 (seconds) |
| `tlsTrustCertsFilePath` | The path of the CA certificate file needed to connect to the downstream Pulsar instance (optional) |
| `tlsAllowInsecureConnection` | Determines whether to allow unencrypted connection after TLS is enabled (optional) |
| `tlsValidateHostname` |  Determines whether to verify the host name of the certificate from the downstream Pulsar (optional) |
| `maxConnectionsPerBroker` | The maximum number of connections allowed to a single downstream Pulsar broker, which is optional and defaults to 1 |
| `auth.tls` | Uses the TLS mode to verify the downstream Pulsar (optional). For example, `auth=tls&auth.tlsCertFile=/path/to/cert&auth.tlsKeyFile=/path/to/key`. |
| `auth.token` | Uses the token mode to verify the downstream Pulsar (optional). For example, `auth=token&auth.token=secret-token` or `auth=token&auth.file=path/to/secret-token-file`. |
| `name` | The name of Pulsar producer in TiCDC (optional) |
| `protocol` | The protocol with which messages are output to Pulsar. The value options are `canal-json`, `open-protocol`, `canal`, `avro`, and `maxwell`. |
| `maxPendingMessages` | Sets the maximum size of the pending message queue, which is optional and defaults to 1000. For example, pending for the confirmation message from Pulsar. |
| `disableBatching` |  Disables automatically sending messages in batches (optional) |
| `batchingMaxPublishDelay` | Sets the duration within which the messages sent are batched (default: 10ms) |
| `compressionType` | Sets the compression algorithm used for sending messages (optional). The value options are `NONE`, `LZ4`, `ZLIB`, and `ZSTD`. (`NONE` by default) |
| `hashingScheme` | The hash algorithm used for choosing the partition to which a message is sent (optional). The value options are `JavaStringHash` (default) and `Murmur3`. |
| `properties.*` | The customized properties added to the Pulsar producer in TiCDC (optional). For example, `properties.location=Hangzhou`. |

For more parameters of Pulsar, see [pulsar-client-go ClientOptions](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ClientOptions) and [pulsar-client-go ProducerOptions](https://godoc.org/github.com/apache/pulsar-client-go/pulsar#ProducerOptions).

#### Use the task configuration file

For more replication configuration (for example, specify replicating a single table), see [Task configuration file](#task-configuration-file).

You can use a configuration file to create a replication task in the following way:

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --config changefeed.toml
```

In the command above, `changefeed.toml` is the configuration file for the replication task.

#### Query the replication task list

Execute the following command to query the replication task list:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --server=http://10.0.10.25:8300
```

```shell
[{
    "id": "simple-replication-task",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

- `checkpoint` indicates that TiCDC has already replicated data before this time point to the downstream.
- `state` indicates the state of the replication task.
    - `normal`: The replication task runs normally.
    - `stopped`: The replication task is stopped (manually paused).
    - `error`: The replication task is stopped (by an error).
    - `removed`: The replication task is removed. Tasks of this state are displayed only when you have specified the `--all` option. To see these tasks when this option is not specified, execute the `changefeed query` command.
    - `finished`: The replication task is finished (data is replicated to the `target-ts`). Tasks of this state are displayed only when you have specified the `--all` option. To see these tasks when this option is not specified, execute the `changefeed query` command.

#### Query a specific replication task

To query a specific replication task, execute the `changefeed query` command. The query result includes the task information and the task state. You can specify the `--simple` or `-s` argument to simplify the query result that will only include the basic replication state and the checkpoint information. If you do not specify this argument, detailed task configuration, replication states, and replication table information are output.

```shell
cdc cli changefeed query -s --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```
{
 "state": "normal",
 "tso": 419035700154597378,
 "checkpoint": "2020-08-27 10:12:19.579",
 "error": null
}
```

In the command and result above:

+ `state` is the replication state of the current `changefeed`. Each state must be consistent with the state in `changefeed list`.
+ `tso` represents the largest transaction TSO in the current `changefeed` that has been successfully replicated to the downstream.
+ `checkpoint` represents the corresponding time of the largest transaction TSO in the current `changefeed` that has been successfully replicated to the downstream.
+ `error` records whether an error has occurred in the current `changefeed`.

```shell
cdc cli changefeed query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task
```

```
{
  "info": {
    "sink-uri": "mysql://127.0.0.1:3306/?max-txn-row=20\u0026worker-number=4",
    "opts": {},
    "create-time": "2020-08-27T10:33:41.687983832+08:00",
    "start-ts": 419036036249681921,
    "target-ts": 0,
    "admin-job-type": 0,
    "sort-engine": "unified",
    "sort-dir": ".",
    "config": {
      "case-sensitive": true,
      "enable-old-value": false,
      "filter": {
        "rules": [
          "*.*"
        ],
        "ignore-txn-start-ts": null,
        "ddl-allow-list": null
      },
      "mounter": {
        "worker-num": 16
      },
      "sink": {
        "dispatchers": null,
      },
      "scheduler": {
        "type": "table-number",
        "polling-time": -1
      }
    },
    "state": "normal",
    "history": null,
    "error": null
  },
  "status": {
    "resolved-ts": 419036036249681921,
    "checkpoint-ts": 419036036249681921,
    "admin-job-type": 0
  },
  "count": 0,
  "task-status": [
    {
      "capture-id": "97173367-75dc-490c-ae2d-4e990f90da0f",
      "status": {
        "tables": {
          "47": {
            "start-ts": 419036036249681921
          }
        },
        "operation": null,
        "admin-job-type": 0
      }
    }
  ]
}
```

In the command and result above:

- `info` is the replication configuration of the queried `changefeed`.
- `status` is the replication state of the queried `changefeed`.
    - `resolved-ts`: The largest transaction `TS` in the current `changefeed`. Note that this `TS` has been successfully sent from TiKV to TiCDC.
    - `checkpoint-ts`: The largest transaction `TS` in the current `changefeed`. Note that this `TS` has been successfully written to the downstream.
    - `admin-job-type`: The status of a `changefeed`:
        - `0`: The state is normal.
        - `1`: The task is paused. When the task is paused, all replicated `processor`s exit. The configuration and the replication status of the task are retained, so you can resume the task from `checkpiont-ts`.
        - `2`: The task is resumed. The replication task resumes from `checkpoint-ts`.
        - `3`: The task is removed. When the task is removed, all replicated `processor`s are ended, and the configuration information of the replication task is cleared up. Only the replication status is retained for later queries.
- `task-status` indicates the state of each replication sub-task in the queried `changefeed`.

#### Pause a replication task

Execute the following command to pause a replication task:

```shell
cdc cli changefeed pause --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

In the above command:

- `--changefeed-id=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to pause.

#### Resume a replication task

Execute the following command to resume a paused replication task:

```shell
cdc cli changefeed resume --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

- `--changefeed-id=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to resume.
- `--overwrite-checkpoint-ts`: starting from v6.2.0, you can specify the starting TSO of resuming the replication task. TiCDC starts pulling data from the specified TSO. The argument accepts `now` or a specific TSO (such as 434873584621453313). The specified TSO must be in the range of (GC safe point, CurrentTSO]. If this argument is not specified, TiCDC replicates data from the current `checkpoint-ts` by default.
- `--no-confirm`: when the replication is resumed, you do not need to confirm the related information. Defaults to `false`.

> **Note:**
>
> - If the TSO specified in `--overwrite-checkpoint-ts` (`t2`) is larger than the current checkpoint TSO in the changefeed (`t1`), data between `t1` and `t2` will not be replicated to the downstream. This causes data loss. You can obtain `t1` by running `cdc cli changefeed query`.
> - If the TSO specified in `--overwrite-checkpoint-ts` (`t2`) is smaller than the current checkpoint TSO in the changefeed (`t1`), TiCDC pulls data from an old time point (`t2`), which might cause data duplication (for example, if the downstream is MQ sink).

#### Remove a replication task

Execute the following command to remove a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed remove --server=http://10.0.10.25:8300 --changefeed-id simple-replication-task
```

In the above command:

- `--changefeed-id=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to remove.

### Update task configuration

Starting from v4.0.4, TiCDC supports modifying the configuration of the replication task (not dynamically). To modify the `changefeed` configuration, pause the task, modify the configuration, and then resume the task.

```shell
cdc cli changefeed pause -c test-cf --server=http://10.0.10.25:8300
cdc cli changefeed update -c test-cf --server=http://10.0.10.25:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
cdc cli changefeed resume -c test-cf --server=http://10.0.10.25:8300
```

Currently, you can modify the following configuration items:

- `sink-uri` of the `changefeed`.
- The `changefeed` configuration file and all configuration items in the file.
- Whether to use the file sorting feature and the sorting directory.
- The `target-ts` of the `changefeed`.

### Manage processing units of replication sub-tasks (`processor`)

- Query the `processor` list:

    ```shell
    cdc cli processor list --server=http://10.0.10.25:8300
    ```

    ```json
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "simple-replication-task"
            }
    ]
    ```

- Query a specific `changefeed` which corresponds to the status of a specific replication task:

    ```shell
    cdc cli processor query --server=http://10.0.10.25:8300 --changefeed-id=simple-replication-task --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```json
    {
      "status": {
        "tables": {
          "56": {    # ID of the replication table, corresponding to tidb_table_id of a table in TiDB
            "start-ts": 417474117955485702
          }
        },
        "operation": null,
        "admin-job-type": 0
      },
      "position": {
        "checkpoint-ts": 417474143881789441,
        "resolved-ts": 417474143881789441,
        "count": 0
      }
    }
    ```

    In the command above:

    - `status.tables`: Each key number represents the ID of the replication table, corresponding to `tidb_table_id` of a table in TiDB.
    - `resolved-ts`: The largest TSO among the sorted data in the current processor.
    - `checkpoint-ts`: The largest TSO that has been successfully written to the downstream in the current processor.

## Task configuration file

This section introduces the configuration of a replication task.

```toml
# Specifies whether the database names and tables in the configuration file are case-sensitive.
# The default value is true.
# This configuration item affects configurations related to filter and sink.
case-sensitive = true

# Specifies whether to output the old value. New in v4.0.5. Since v5.0, the default value is `true`.
enable-old-value = true

# Specifies whether to enable the Syncpoint feature, which is supported since v6.3.0.
enable-sync-point = true

# Specifies the interval at which Syncpoint aligns the upstream and downstream snapshots.
# The format is in h m s. For example, "1h30m30s".
# The default value is "10m" and the minimum value is "30s".
sync-point-interval = "5m"

# Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up.
# The format is in h m s. For example, "24h30m30s".
# The default value is "24h".
sync-point-retention = "1h"

[filter]
# Ignores the transaction of specified start_ts.
ignore-txn-start-ts = [1, 2]

# Filter rules.
# Filter syntax: https://docs.pingcap.com/tidb/stable/table-filter#syntax.
rules = ['*.*', '!test.*']

# Event filter rules.
# The detailed syntax is described in the event filter rules section.
# The first event filter rule.
[[filter.event-filters]]
matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
ignore-event = ["insert"] # Ignore insert events.
ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
ignore-update-old-value-expr = "age < 18" # Ignore update DMLs whose old value contains "age < 18".
ignore-update-new-value-expr = "gender = 'male'" # Ignore update DMLs whose new value contains "gender = 'male'".

# The second event filter rule.
matcher = ["test.fruit"] # matcher is an allow list, which means this rule only applies to the fruit table in the test database.
ignore-event = ["drop table"] # Ignore drop table events.
ignore-sql = ["delete"] # Ignore delete DMLs.
ignore-insert-value-expr = "price > 1000 and origin = 'no where'" # Ignore insert DMLs that contain the conditions "price > 1000" and "origin = 'no where'".

[sink]
# For the sink of MQ type, you can use dispatchers to configure the event dispatcher.
# Since v6.1, TiDB supports two types of event dispatchers: partition and topic. For more information, see the following section.
# The matching syntax of matcher is the same as the filter rule syntax. For details about the matcher rules, see the following section.

dispatchers = [
    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
    {matcher = ['test6.*'], partition = "ts"}
]
# For the sink of MQ type, you can specify the protocol format of the message.
# Currently the following protocols are supported: canal-json, open-protocol, canal, avro, and maxwell.
protocol = "canal-json"
```

### Event filter rules <span class="version-mark">New in v6.2.0</span>

Starting in v6.2.0, TiCDC supports event filter. You can configure event filter rules to filter out the DML and DDL events that meet the specified conditions.

The following is an example of event filter rules:

```toml
[filter]
# The event filter rules must be under the `[filter]` configuration. You can configure multiple event filters at the same time.

[[filter.event-filters]]
matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
ignore-event = ["insert"] # Ignore insert events.
ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
ignore-update-old-value-expr = "age < 18 or name = 'lili'" # Ignore update DMLs whose old value contains "age < 18" or "name = 'lili'".
ignore-update-new-value-expr = "gender = 'male' and age > 18" # Ignore update DMLs whose new value contains "gender = 'male'" and "age > 18".
```

The event filter rules must be under the `[filter]` configuration. For detailed configuration, refer to [Task configuration file](#task-configuration-file).

Description of configuration parameters :

- `matcher`: the database and table that this event filter rule applies to. The syntax is the same as [table filter](/table-filter.md).
- `ignore-event`: the event type to be ignored. This parameter accepts an array of strings. You can configure multiple event types. Currently, the following event types are supported:

| Event           | Type | Alias | Description         |
| --------------- | ---- | -|--------------------------|
| all dml         |      | |Matches all DML events       |
| all ddl         |      | |Matches all DDL events         |
| insert          | DML  | |Matches `insert` DML event      |
| update          | DML  | |Matches `update` DML event      |
| delete          | DML  | |Matches `delete` DML event      |
| create schema   | DDL  | create database |Matches `create database` event |
| drop schema     | DDL  | drop database  |Matches `drop database` event |
| create table    | DDL  | |Matches `create table` event    |
| drop table      | DDL  | |Matches `drop table` event      |
| rename table    | DDL  | |Matches `rename table` event    |
| truncate table  | DDL  | |Matches `truncate table` event  |
| alter table     | DDL  | |Matches `alter table` event, including all clauses of `alter table`, `create index` and `drop index`   |
| add table partition    | DDL  | |Matches `add table partition` event     |
| drop table partition    | DDL  | |Matches `drop table partition` event     |
| truncate table partition    | DDL  | |Matches `truncate table partition` event     |
| create view     | DDL  | |Matches `create view`event     |
| drop view     | DDL  | |Matches `drop view` event     |

- `ignore-sql`: the DDL statements to be ignored. This parameter accepts an array of strings, in which you can configure multiple regular expressions. This rule only applies to DDL events.
- `ignore-delete-value-expr`: this parameter accepts a SQL expression. This rule only applies to delete DML events with the specified value.
- `ignore-insert-value-expr`: this parameter accepts a SQL expression. This rule only applies to insert DML events with the specified value.
- `ignore-update-old-value-expr`: this parameter accepts a SQL expression. This rule only applies to update DML events whose old value contains the specified value.
- `ignore-update-new-value-expr`: this parameter accepts a SQL expression. This rule only applies to update DML events whose new value contains the specified value.

> **Note:**
>
> - When TiDB updates a value in the column of the clustered index, TiDB splits an `UPDATE` event into a `DELETE` event and an `INSERT` event. TiCDC does not identify such events as an `UPDATE` event and thus cannot correctly filter out such events.
> - When you configure a SQL expression, make sure all tables that matches `matcher` contain all the columns specified in the SQL expression. Otherwise, the replication task cannot be created. In addition, if the table schema changes during the replication, which results in a table no longer containing a required column, the replication task fails and cannot be resumed automatically. In such a situation, you must manually modify the configuration and resume the task.

### Notes for compatibility

* In TiCDC v4.0.0, `ignore-txn-commit-ts` is removed and `ignore-txn-start-ts` is added, which uses start_ts to filter transactions.
* In TiCDC v4.0.2, `db-dbs`/`db-tables`/`ignore-dbs`/`ignore-tables` are removed and `rules` is added, which uses new filter rules for databases and tables. For detailed filter syntax, see [Table Filter](/table-filter.md).
* In TiCDC v6.1.0, `mounter` is removed. If you configure `mounter`, TiCDC does not report an error, but the configuration does not take effect.

## Customize the rules for Topic and Partition dispatchers of Kafka Sink

### Matcher rules

In the example of the previous section:

- For the tables that match the matcher rule, they are dispatched according to the policy specified by the corresponding topic expression. For example, the `test3.aa` table is dispatched according to "Topic expression 2"; the `test5.aa` table is dispatched according to "Topic expression 3".
- For a table that matches multiple matcher rules, it is dispatched according to the first matching topic expression. For example, the `test1.aa` table is distributed according to "Topic expression 1".
- For tables that do not match any matcher rule, the corresponding data change events are sent to the default topic specified in `--sink-uri`. For example, the `test10.aa` table is sent to the default topic.
- For tables that match the matcher rule but do not specify a topic dispatcher, the corresponding data changes are sent to the default topic specified in `--sink-uri`. For example, the `test6.aa` table is sent to the default topic.

### Topic dispatchers

You can use topic = "xxx" to specify a Topic dispatcher and use topic expressions to implement flexible topic dispatching policies. It is recommended that the total number of topics be less than 1000.

The format of the Topic expression is `[prefix]{schema}[middle][{table}][suffix]`.

- `prefix`: optional. Indicates the prefix of the Topic Name.
- `{schema}`: required. Used to match the schema name.
- `middle`: optional. Indicates the delimiter between schema name and table name.
- `{table}`: optional. Used to match the table name.
- `suffix`: optional. Indicates the suffix of the Topic Name.

`prefix`, `middle` and `suffix` can only include the following characters: `a-z`, `A-Z`, `0-9`, `.`, `_` and `-`. `{schema}` and `{table}` are both lowercase. Placeholders such as `{Schema}` and `{TABLE}` are invalid.

Some examples:

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - The data change events corresponding to `test1.table1` are sent to the topic named `hello_test1_table1`.
    - The data change events corresponding to `test2.table2` are sent to the topic named `hello_test2_table2`.
- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - The data change events corresponding to all tables in `test3` are sent to the topic named `hello_test3_world`.
    - The data change events corresponding to all tables in `test4` are sent to the topic named `hello_test4_world`.
- `matcher = ['*.*'], topic = "{schema}_{table}"`
    - All tables listened by TiCDC are dispatched to separate topics according to the "schema_table" rule. For example, for the `test.account` table, TiCDC dispatches its data change log to a Topic named `test_account`.

### Dispatch DDL events

#### Schema-level DDLs

DDLs that are not related to a specific table are called schema-level DDLs, such as `create database` and `drop database`. The events corresponding to schema-level DDLs are sent to the default topic specified in `--sink-uri`.

#### Table-level DDLs

DDLs that are related to a specific table are called table-level DDLs, such as `alter table` and `create table`. The events corresponding to table-level DDLs are sent to the corresponding topic according to dispatcher configurations.

For example, for a dispatcher like `matcher = ['test.*'], topic = {schema}_{table}`, DDL events are dispatched as follows:

- If a single table is involved in the DDL event, the DDL event is sent to the corresponding topic as is. For example, for the DDL event `drop table test.table1`, the event is sent to the topic named `test_table1`.
- If multiple tables are involved in the DDL event (`rename table` / `drop table` / `drop view` may involve multiple tables), the DDL event is split into multiple events and sent to the corresponding topics. For example, for the DDL event `rename table test.table1 to test.table10, test.table2 to test.table20`, the event `rename table test.table1 to test.table10` is sent to the topic named `test_table1` and the event `rename table test.table2 to test.table20` is sent to the topic named `test.table2`.

### Partition dispatchers

You can use `partition = "xxx"` to specify a partition dispatcher. It supports four dispatchers: default, ts, index-value, and table. The dispatcher rules are as follows:

- default: When multiple unique indexes (including the primary key) exist or the Old Value feature is enabled, events are dispatched in the table mode. When only one unique index (or the primary key) exists, events are dispatched in the index-value mode.
- ts: Use the commitTs of the row change to hash and dispatch events.
- index-value: Use the value of the primary key or the unique index of the table to hash and dispatch events.
- table: Use the schema name of the table and the table name to hash and dispatch events.

> **Note:**
>
>
> Since v6.1, to clarify the meaning of the configuration, the configuration used to specify the partition dispatcher has been changed from `dispatcher` to `partition`, with `partition` being an alias for `dispatcher`. For example, the following two rules are exactly equivalent.
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "ts"},
>    {matcher = ['*.*'], partition = "ts"},
> ]
> ```
>
> However, `dispatcher` and `partition` cannot appear in the same rule. For example, the following rule is invalid.
>
> ```
> {matcher = ['*.*'], dispatcher = "ts", partition = "table"},
> ```

## Output the historical value of a Row Changed Event <span class="version-mark">New in v4.0.5</span>

In the default configuration, the Row Changed Event of TiCDC Open Protocol output in a replication task only contains the changed value, not the value before the change. Therefore, the output value cannot be used by the consumer ends of TiCDC Open Protocol as the historical value of a Row Changed Event.

Starting from v4.0.5, TiCDC supports outputting the historical value of a Row Changed Event. To enable this feature, specify the following configuration in the `changefeed` configuration file at the root level:

{{< copyable "" >}}

```toml
enable-old-value = true
```

This feature is enabled by default since v5.0. To learn the output format of the TiCDC Open Protocol after this feature is enabled, see [TiCDC Open Protocol - Row Changed Event](/ticdc/ticdc-open-protocol.md#row-changed-event).

## Replicate tables with the new framework for collations enabled

Starting from v4.0.15, v5.0.4, v5.1.1 and v5.2.0, TiCDC supports tables that have enabled [new framework for collations](/character-set-and-collation.md#new-framework-for-collations).

## Replicate tables without a valid index

Since v4.0.8, TiCDC supports replicating tables that have no valid index by modifying the task configuration. To enable this feature, configure in the `changefeed` configuration file as follows:

{{< copyable "" >}}

```toml
enable-old-value = true
force-replicate = true
```

> **Warning:**
>
> For tables without a valid index, operations such as `INSERT` and `REPLACE` are not reentrant, so there is a risk of data redundancy. TiCDC guarantees that data is distributed only at least once during the replication process. Therefore, enabling this feature to replicate tables without a valid index will definitely cause data redundancy. If you do not accept data redundancy, it is recommended to add an effective index, such as adding a primary key column with the `AUTO RANDOM` attribute.

## Unified Sorter

Unified sorter is the sorting engine in TiCDC. It can mitigate OOM problems caused by the following scenarios:

+ The data replication task in TiCDC is paused for a long time, during which a large amount of incremental data is accumulated and needs to be replicated.
+ The data replication task is started from an early timestamp so it becomes necessary to replicate a large amount of incremental data.

For the changefeeds created using `cdc cli` after v4.0.13, Unified Sorter is enabled by default; for the changefeeds that have existed before v4.0.13, the previous configuration is used.

To check whether or not the Unified Sorter feature is enabled on a changefeed, you can execute the following example command (assuming the IP address of the PD instance is `http://10.0.10.25:2379`):

```shell
cdc cli --server="http://10.0.10.25:8300" changefeed query --changefeed-id=simple-replication-task | grep 'sort-engine'
```

In the output of the above command, if the value of `sort-engine` is "unified", it means that Unified Sorter is enabled on the changefeed.

> **Note:**
>
> + If your servers use mechanical hard drives or other storage devices that have high latency or limited bandwidth, the performance of Unified Sorter will be affected significantly.
> + By default, Unified Sorter uses `data_dir` to store temporary files. It is recommended to ensure that the free disk space is greater than or equal to 500 GiB. For production environments, it is recommended to ensure that the free disk space on each node is greater than (the maximum `checkpoint-ts` delay allowed by the business) * (upstream write traffic at business peak hours). In addition, if you plan to replicate a large amount of historical data after `changefeed` is created, make sure that the free space on each node is greater than the amount of replicated data.

## Eventually consistent replication in disaster scenarios

Starting from v5.3.0, TiCDC supports backing up incremental data from an upstream TiDB cluster to S3 storage or an NFS file system of a downstream cluster. When the upstream cluster encounters a disaster and becomes unavailable, TiCDC can restore the downstream data to the recent eventually consistent state. This is the eventually consistent replication capability provided by TiCDC. With this capability, you can switch applications to the downstream cluster quickly, avoiding long-time downtime and improving service continuity.

Currently, TiCDC can replicate incremental data from a TiDB cluster to another TiDB cluster or a MySQL-compatible database system (including Aurora, MySQL, and MariaDB). In case the upstream cluster crashes, TiCDC can restore data in the downstream cluster within 5 minutes, given the conditions that before the disaster the replication status of TiCDC is normal and the replication lag is small. It allows data loss of 10s at most, that is, RTO <= 5 min, and P95 RPO <= 10s.

TiCDC replication lag increases in the following scenarios:

- The TPS increases significantly in a short time
- Large or long transactions occur in the upstream
- The TiKV or TiCDC cluster in the upstream is reloaded or upgraded
- Time-consuming DDL statements, such as `add index`, are executed in the upstream
- The PD is configured with aggressive scheduling strategies, resulting in frequent transfer of Region leaders, or frequent Region merge or Region split

### Prerequisites

- Prepare a highly available Amazon S3 storage or NFS system for storing TiCDC's real-time incremental data backup files. These files can be accessed in case of an primary cluster disaster.
- Enable this feature for changefeeds that need to have eventual consistency in disaster scenarios. To enable it, you can add the following configuration to the changefeed configuration file.

```toml
[consistent]
# Consistency level. Options include:
# - none: the default value. In a non-disaster scenario, eventual consistency is only guaranteed if and only if finished-ts is specified.
# - eventual: Uses redo log to guarantee eventual consistency in case of the primary cluster disasters.
level = "eventual"

# Individual redo log file size, in MiB. By default, it's 64. It is recommended to be no more than 128.
max-log-size = 64

# The interval for flushing or uploading redo logs to S3, in milliseconds. By default, it's 1000. The recommended range is 500-2000.
flush-interval = 1000

# Form of storing redo log, including nfs (NFS directory) and S3 (uploading to S3).
storage = "s3://logbucket/test-changefeed?endpoint=http://$S3_ENDPOINT/"
```

### Disaster recovery

When a disaster happens in the primary cluster, you need to recover manually in the secondary cluster by running the `cdc redo` command. The recovery process is as follows.

1. Ensure that all the TiCDC processes have exited. This is to prevent the primary cluster from resuming service during data recovery and prevent TiCDC from restarting data synchronization.
2. Use cdc binary for data recovery. Run the following command:

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

In this command:

- `tmp-dir`: Specifies the temporary directory for downloading TiCDC incremental data backup files.
- `storage`: Specifies the address for storing the TiCDC incremental data backup files, either an Amazon S3 storage or an NFS directory.
- `sink-uri`: Specifies the secondary cluster address to restore the data to. Scheme can only be `mysql`.
