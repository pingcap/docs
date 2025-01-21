---
title: CLI and Configuration Parameters of TiCDC Changefeeds
summary: Learn the definitions of CLI and configuration parameters of TiCDC changefeeds.
---

# CLI and Configuration Parameters of TiCDC Changefeeds

## Changefeed CLI parameters

This section introduces the command-line parameters of TiCDC changefeeds by illustrating how to create a replication (changefeed) task:

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2024-12-05T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.5.0"}
```

- `--changefeed-id`: The ID of the replication task. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the replication task. Configure `--sink-uri` according to the following format. Currently, the scheme supports `mysql`, `tidb`, and `kafka`.

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    When the sink URI contains special characters such as `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`, you need to escape the special characters, for example, in [URI Encoder](https://www.urlencoder.org/).

- `--start-ts`: Specifies the starting TSO of the changefeed. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.
- `--target-ts`: Specifies the ending TSO of the changefeed. To this TSO, the TiCDC cluster stops pulling data. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: Specifies the configuration file of the changefeed.

## Changefeed configuration parameters

This section introduces the configuration of a replication task.

### `memory-quota`

- Specifies the memory quota (in bytes) that can be used in the capture server by the sink manager. If the value is exceeded, the overused part will be recycled by the go runtime.
- Default value: `1073741824` (1 GiB)

### `case-sensitive`

- Specifies whether the database names and tables in the configuration file are case-sensitive. Starting from v6.5.6, v7.1.3, and v7.5.0, the default value changes from `true` to `false`.
- This configuration item affects configurations related to filter and sink.
- Default value: `false`

### `force-replicate`

- Specifies whether to forcibly [replicate tables without a valid index](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index).
- Default value: `false`

### `enable-sync-point` <span class="version-mark">New in v6.3.0</span>

- Specifies whether to enable the Syncpoint feature, which is supported starting from v6.3.0 and is disabled by default.
- Starting from v6.4.0, only the changefeed with the `SYSTEM_VARIABLES_ADMIN` or `SUPER` privilege can use the TiCDC Syncpoint feature.
- This configuration item only takes effect if the downstream is TiDB.
- Default value: `false`

### `sync-point-interval`

- Specifies the interval at which Syncpoint aligns the upstream and downstream snapshots.
- This configuration item only takes effect if the downstream is TiDB.
- The format is `"h m s"`. For example, `"1h30m30s"`.
- Default value: `"10m"`
- Minimum value: `"30s"`

### `sync-point-retention`

- Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up.
- This configuration item only takes effect if the downstream is TiDB.
- The format is `"h m s"`. For example, `"24h30m30s"`.
- Default value: `"24h"`

### `sql-mode` <span class="version-mark">New in v6.5.6, v7.1.3, and v7.5.0</span>

- Specifies the [SQL mode](/sql-mode.md) used when parsing DDL statements. Multiple modes are separated by commas.
- Default value: `"ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"`, which is the same as the default SQL mode of TiDB

### `bdr-mode`

- To set up BDR (Bidirectional replication) clusters using TiCDC, modify this parameter to `true` and set the TiDB clusters to BDR mode. For more information, see [Bidirectional Replication](/ticdc/ticdc-bidirectional-replication.md#bidirectional-replication).
- Default value: `false`, indicating that bi-directional replication (BDR) mode is not enabled

### `changefeed-error-stuck-duration`

- Specifies the duration for which the changefeed is allowed to automatically retry when internal errors or exceptions occur.
- The changefeed enters the failed state if internal errors or exceptions occur in the changefeed and persist longer than the duration set by this parameter.
- When the changefeed is in the failed state, you need to restart the changefeed manually for recovery.
- The format is `"h m s"`. For example, `"1h30m30s"`.
- Default value: `"30m"`

### mounter

#### `worker-num`

- Specifies the number of threads with which the mounter decodes KV data.
- Default value: `16`

### filter

#### `ignore-txn-start-ts`

- Ignores the transaction of specified start_ts.

<!-- Example: `[1, 2]` -->

#### `rules`

- Specifies the filter rules. For more information, see [Syntax](/table-filter.md#syntax).

<!-- Example: `['*.*', '!test.*']` -->

#### filter.event-filters

For more information, see [Event filter rules](/ticdc/ticdc-filter.md#event-filter-rules).

##### `matcher`

- `matcher` is an allow list. `matcher = ["test.worker"]` means this rule only applies to the `worker` table in the `test` database.

##### `ignore-event`

- `ignore-event = ["insert"]` ignores `INSERT` events. 
- `ignore-event = ["drop table", "delete"]` ignores the `DROP TABLE` DDL events and the `DELETE` DML events. Note that when a value in the clustered index column is updated in TiDB, TiCDC splits an `UPDATE` event into `DELETE` and `INSERT` events. TiCDC cannot identify such events as `UPDATE` events and thus cannot correctly filter out such events.

##### `ignore-sql`

- `ignore-sql = ["^drop", "add column"]` ignores DDLs that start with `DROP` or contain `ADD COLUMN`.

##### `ignore-delete-value-expr`

- `ignore-delete-value-expr = "name = 'john'"` ignores `DELETE` DMLs that contain the condition `name = 'john'`.

##### `ignore-insert-value-expr`

- `ignore-insert-value-expr = "id >= 100"` ignores `INSERT` DMLs that contain the condition `id >= 100`

##### `ignore-update-old-value-expr`

- `ignore-update-old-value-expr = "age < 18"` ignores `UPDATE` DMLs whose old value contains `age < 18`

##### `ignore-update-new-value-expr`

- `ignore-update-new-value-expr = "gender = 'male'"` ignores `UPDATE` DMLs whose new value contains `gender = 'male'`

### scheduler

#### `enable-table-across-nodes`

- Allocate tables to multiple TiCDC nodes for replication on a per-Region basis.
- This configuration item only takes effect on Kafka changefeeds and is not supported on MySQL changefeeds.
- When `enable-table-across-nodes` is enabled, there are two allocation modes:

    1. Allocate tables based on the number of Regions, so that each TiCDC node handles roughly the same number of Regions. If the number of Regions for a table exceeds the value of [`region-threshold`](#region-threshold), the table will be allocated to multiple nodes for replication. The default value of `region-threshold` is `10000`.
    2. Allocate tables based on the write traffic, so that each TiCDC node handles roughly the same number of modified rows. Only when the number of modified rows per minute in a table exceeds the value of [`write-key-threshold`](#write-key-threshold), will this allocation take effect.

  You only need to configure one of the two modes. If both `region-threshold` and `write-key-threshold` are configured, TiCDC prioritizes the traffic allocation mode, namely `write-key-threshold`.

- The value is `false` by default. Set it to `true` to enable this feature.
- Default value: `false`

#### `region-threshold`

- Default value: `10000`

#### `write-key-threshold`

- Default value: `0`, which means that the traffic allocation mode is not used by default

### sink

<!-- MQ sink configuration items -->

#### `dispatchers`

- For the sink of MQ type, you can use dispatchers to configure the event dispatcher.
- Starting from v6.1.0, TiDB supports two types of event dispatchers: partition and topic.
- The matching syntax of matcher is the same as the filter rule syntax.
- This configuration item only takes effect if the downstream is MQ.
- When the downstream MQ is Pulsar, if the routing rule for `partition` is not specified as any of `ts`, `index-value`, `table`, or `default`, each Pulsar message will be routed using the string you set as the key. For example, if you specify the routing rule for a matcher as the string `code`, then all Pulsar messages that match that matcher will be routed with `code` as the key.

#### `column-selectors` <span class="version-mark">New in v7.5.0</span>

- Selects specific columns for replication. This only takes effect when the downstream is Kafka.

#### `protocol`

- Specifies the protocol format used for encoding messages.
- This configuration item only takes effect if the downstream is Kafka, Pulsar, or a storage service.
- When the downstream is Kafka, the protocol can be canal-json, avro, debezium, open-protocol, or simple.
- When the downstream is Pulsar, the protocol can only be canal-json.
- When the downstream is a storage service, the protocol can only be canal-json or csv.

<!-- Example: `"canal-json"` -->

#### `delete-only-output-handle-key-columns` <span class="version-mark">New in v7.2.0</span>

- Specifies the output of DELETE events. This parameter is valid only for canal-json and open-protocol protocols.
- This parameter is incompatible with `force-replicate`. If both this parameter and `force-replicate` are set to `true`, TiCDC reports an error when creating a changefeed.
- The Avro protocol is not controlled by this parameter and always outputs only the primary key columns or unique index columns.
- The CSV protocol is not controlled by this parameter and always outputs all columns.
- Default value: `false`, which means outputting all columns
- When you set it to `true`, only primary key columns or unique index columns are output.

#### `schema-registry`

- Specifies the schema registry URL.
- This configuration item only takes effect if the downstream is MQ.

<!-- Example: `"http://localhost:80801/subjects/{subject-name}/versions/{version-number}/schema"` -->

#### `encoder-concurrency`

- Specifies the number of encoder threads used when encoding data.
- This configuration item only takes effect if the downstream is MQ.
- Default value: `32`

#### `enable-kafka-sink-v2`

> **Warning:**
>
> This configuration is an experimental feature. It is not recommended to use it in production environments.

- Specifies whether to enable kafka-sink-v2 that uses the kafka-go sink library.
- This configuration item only takes effect if the downstream is MQ.
- Default value: `false`

#### `only-output-updated-columns` <span class="version-mark">New in v7.1.0</span>

- Specifies whether to only output the updated columns.
- This configuration item only applies to the MQ downstream using the open-protocol and canal-json.
- Default value: `false`

<!-- Storage sink configuration items -->

#### `terminator`

- This configuration item is only used when you replicate data to storage sinks and can be ignored when replicating data to MQ or MySQL sinks.
- Specifies the row terminator, used for separating two data change events.
- Default value: `""`, which means `\r\n` is used

#### `date-separator`

- Specifies the date separator type used in the file directory. For more information, see [Data change records](/ticdc/ticdc-sink-to-cloud-storage.md#data-change-records).
- This configuration item only takes effect if the downstream is a storage service.
- Default value: `day`, which means separating files by day
- Value options: `none`, `year`, `month`, `day`

#### `enable-partition-separator`

- Controls whether to use partitions as the separation string.
- This configuration item only takes effect if the downstream is a storage service.
- Default value: `true`, which means that partitions in a table are stored in separate directories
- Note that this configuration will be deprecated in future versions and will be forcibly set to `true`. It is recommended to keep this configuration at its default value to avoid potential data loss in downstream partitioned tables. For more information, see [Issue #11979](https://github.com/pingcap/tiflow/issues/11979). For usage examples, see [Data change records](/ticdc/ticdc-sink-to-cloud-storage.md#data-change-records).

#### `debezium-disable-schema`

- Controls whether to disable the output of schema information.
- Default value: `false`, which means enabling the output of schema information
- This parameter only takes effect when the sink type is MQ and the output protocol is Debezium.

#### sink.csv <span class="version-mark">New in v6.5.0</span>

Starting from v6.5.0, TiCDC supports saving data changes to storage services in CSV format. Ignore the following configurations if you replicate data to MQ or MySQL sinks.

##### `delimiter`

- Specifies the character used to separate fields in the CSV file. The value must be an ASCII character.
- Default value: `,`

##### `quote`

- Specifies the quotation character used to surround fields in the CSV file. If the value is empty, no quotation is used.
- Default value: `"`

##### `null`

- Specifies the character displayed when a CSV column is NULL.
- Default value: `\N`

##### `include-commit-ts`

- Controls whether to include commit-ts in CSV rows.
- Default value: `false`

##### `binary-encoding-method`

- Specifies the encoding method of binary data.
- Default value: `base64`
- Value option: `base64`, `hex`

##### `output-handle-key`

- Controls whether to output handle key information. This configuration parameter is for internal implementation only, so it is not recommended to set it.
- Default value: `false`

##### `output-old-value`

- Controls whether to output the value before the row data changes. The default value is false. 
- When it is enabled (setting it to `true`), the `UPDATE` event will output two rows of data: the first row is a `DELETE` event that outputs the data before the change; the second row is an `INSERT` event that outputs the changed data.
- When it is enabled, the `"is-update"` column will be added before the column with data changes. This added column is used to identify whether the data change of the current row comes from the `UPDATE` event or the original `INSERT` or `DELETE` event. If the data change of the current row comes from the `UPDATE` event, the value of the `"is-update"` column is `true`. Otherwise, it is `false`.
- Default value: `false`

Starting from v8.0.0, TiCDC supports the Simple message encoding protocol. The following are the configuration parameters for the Simple protocol. For more information about the protocol, see [TiCDC Simple Protocol](/ticdc/ticdc-simple-protocol.md).

The following configuration parameters control the sending behavior of bootstrap messages.

#### `send-bootstrap-interval-in-sec`

- Controls the time interval for sending bootstrap messages, in seconds.
- Default value: `120`, which means that a bootstrap message is sent every 120 seconds for each table
- Unit: Seconds

#### `send-bootstrap-in-msg-count`

- Controls the message interval for sending bootstrap, in message count.
- Default value: `10000`, which means that a bootstrap message is sent every 10000 row changed messages for each table
- If you want to disable the sending of bootstrap messages, set both [`send-bootstrap-interval-in-sec`](#send-bootstrap-interval-in-sec) and `send-bootstrap-in-msg-count` to `0`.

#### `send-bootstrap-to-all-partition`

- Controls whether to send bootstrap messages to all partitions.
- Setting it to `false` means bootstrap messages are sent to only the first partition of the corresponding table topic.
- Default value: `true`, which means that bootstrap messages are sent to all partitions of the corresponding table topic

#### sink.kafka-config.codec-config

##### `encoding-format`

- Controls the encoding format of the Simple protocol messages. Currently, the Simple protocol message supports `json` and `avro` encoding formats.
- Default value: `json`
- Value options: `json`, `avro`

#### sink.open

##### `output-old-value`

- Controls whether to output the value before the row data changes. The default value is true. When it is disabled, the `UPDATE` event does not output the "p" field.
- Default value: `true`

#### sink.debezium

##### `output-old-value`

- Controls whether to output the value before the row data changes. The default value is true. When it is disabled, the `UPDATE` event does not output the "before" field.
- Default value: `true`

### consistent

Specifies the replication consistency configurations for a changefeed when using the redo log. For more information, see [Eventually consistent replication in disaster scenarios](/ticdc/ticdc-sink-to-mysql.md#eventually-consistent-replication-in-disaster-scenarios).

Note: The consistency-related configuration items only take effect when the downstream is a database and the redo log feature is enabled.

#### `level`

- The data consistency level. `"none"` means that the redo log is disabled.
- Default value: `"none"`
- Value options: `"none"`, `"eventual"`

#### `max-log-size`

- The max redo log size.
- Default value: `64`
- Unit: MiB

#### `flush-interval`

- The flush interval for redo log.
- Default value: `2000`
- Unit: milliseconds

#### `storage`

- The storage URI of the redo log.
- Default value: `""`

#### `use-file-backend`

- Specifies whether to store the redo log in a local file.
- Default value: `false`

#### `encoding-worker-num`

- The number of encoding and decoding workers in the redo module.
- Default value: `16`

#### `flush-worker-num`

- The number of flushing workers in the redo module.
- Default value: `8`

#### `compression`

- The behavior to compress redo log files.
- Default value: `""`, which means no compression
- Value options: `""`, `"lz4"`

#### `flush-concurrency`

- The concurrency for uploading a single redo file.
- Default value: `1`, which means concurrency is disabled

### integrity

#### `integrity-check-level`

- Controls whether to enable the checksum validation for single-row data.
- Default value: `"none"`, which means to disable the feature
- Value options: `"none"`, `"correctness"`

#### `corruption-handle-level`

- Specifies the log level of the changefeed when the checksum validation for single-row data fails.
- Default value: `"warn"` 
- Value options: `"warn"`, `"error"`

### sink.kafka-config

The following configuration items only take effect when the downstream is Kafka.

#### `sasl-mechanism`

- Specifies the mechanism of Kafka SASL authentication.
- Default value: `""`, indicating that SASL authentication is not used

<!-- Example: `OAUTHBEARER` -->

#### `sasl-oauth-client-id`

- Specifies the client-id in the Kafka SASL OAUTHBEARER authentication. This parameter is required when the OAUTHBEARER authentication is used.
- Default value: `""`

#### `sasl-oauth-client-secret`

- Specifies the client-secret in the Kafka SASL OAUTHBEARER authentication. This parameter is required when the OAUTHBEARER authentication is used.
- Default value: `""`

#### `sasl-oauth-token-url`

- Specifies the token-url in the Kafka SASL OAUTHBEARER authentication to obtain the token. This parameter is required when the OAUTHBEARER authentication is used.
- Default value: `""`

#### `sasl-oauth-scopes`

- Specifies the scopes in the Kafka SASL OAUTHBEARER authentication. This parameter is optional when the OAUTHBEARER authentication is used.
- Default value: `""`

#### `sasl-oauth-grant-type`

- Specifies the grant-type in the Kafka SASL OAUTHBEARER authentication. This parameter is optional when the OAUTHBEARER authentication is used.
- Default value: `"client_credentials"`

#### `sasl-oauth-audience`

- Specifies the audience in the Kafka SASL OAUTHBEARER authentication. This parameter is optional when the OAUTHBEARER authentication is used.
- Default value: `""`

<!-- Example: `"kafka"` -->

#### `output-raw-change-event`

- Controls whether to output the original data change event. For more information, see [Control whether to split primary or unique key `UPDATE` events](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events).
- Default value: `false`

### sink.kafka-config.glue-schema-registry-config

The following configuration is only required when using Avro as the protocol and AWS Glue Schema Registry:

```toml
region="us-west-1"
registry-name="ticdc-test"
access-key="xxxx"
secret-access-key="xxxx"
token="xxxx"
```

For more information, see [Integrate TiCDC with AWS Glue Schema Registry](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-aws-glue-schema-registry).

### sink.pulsar-config

The following parameters take effect only when the downstream is Pulsar.

#### `authentication-token`

- Authentication on the Pulsar server is done using a token. Specify the value of the token.

#### `token-from-file`

- When you use a token for Pulsar server authentication, specify the path to the file where the token is located.

#### `basic-user-name`

- Pulsar uses the basic account and password to authenticate the identity. Specify the account.

#### `basic-password`

- Pulsar uses the basic account and password to authenticate the identity. Specify the password.

#### `auth-tls-certificate-path`

- Specifies the certificate path for Pulsar TLS encrypted authentication.

#### `auth-tls-private-key-path`

- Specifies the private key path for Pulsar TLS encrypted authentication.

#### `tls-trust-certs-file-path`

- Specifies the path to trusted certificate file of the Pulsar TLS encrypted authentication.

#### `oauth2.oauth2-issuer-url`

- Pulsar oauth2 issuer-url.
- For more information, see [Pulsar documentation website](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication).

#### `oauth2.oauth2-audience`

- Pulsar oauth2 audience.
- For more information, see the [Pulsar website](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication).

#### `oauth2.oauth2-private-key`

- Pulsar oauth2 private-key.
- For more information, see the [Pulsar website](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication).

#### `oauth2.oauth2-client-id`

- Pulsar oauth2 client-id
- For more information, see the [Pulsar website](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication).

#### `oauth2.oauth2-scope`

- Pulsar oauth2 oauth2-scope.
- For more information, see the [Pulsar website](https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication).

#### `pulsar-producer-cache-size`

- Specifies the number of cached Pulsar producers in TiCDC. Each Pulsar producer corresponds to one topic. If the number of topics you need to replicate is larger than the default value, you need to increase the number.
- Default value: `10240`

#### `compression-type`

- Pulsar data compression method. 
- Default value: `""`, which means no compression is used
- Value options: `"lz4"`, `"zlib"`, `"zstd"`

#### `connection-timeout`

- The timeout for the Pulsar client to establish a TCP connection with the server.
- Default value: `5` (seconds)

#### `operation-timeout`

- The timeout for Pulsar clients to initiate operations such as creating and subscribing to a topic.
- Default value: `30` (seconds)

#### `batching-max-messages`

- The maximum number of messages in a single batch for a Pulsar producer to send.
- Default value: `1000`

#### `batching-max-publish-delay`

- The interval at which Pulsar producer messages are saved for batching.
- Default value: `10` (milliseconds)

#### `send-timeout`

- The timeout for a Pulsar producer to send a message.
- Default value: `30` (seconds)

#### `output-raw-change-event`

- Controls whether to output the original data change event. For more information, see [Control whether to split primary or unique key `UPDATE` events](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events).
- Default value: `false`

### sink.cloud-storage-config

#### `worker-count`

- The concurrency for saving data changes to the downstream cloud storage.
- Default value: `16`

#### `flush-interval`

- The interval for saving data changes to the downstream cloud storage.
- Default value: `"2s"`

#### `file-size`

- A data change file is saved to the cloud storage when the number of bytes in this file exceeds `file-size`.
- Default value: `67108864`, that is 64 MiB

#### `file-expiration-days`

- The duration to retain files, which takes effect only when `date-separator` is configured as `day`.
- Default value: `0`, which means file cleanup is disabled
- Assume that `file-expiration-days = 1` and `file-cleanup-cron-spec = "0 0 0 * * *"`, then TiCDC performs daily cleanup at 00:00:00 for files saved beyond 24 hours. For example, at 00:00:00 on 2023/12/02, TiCDC cleans up files generated before 2023/12/01, while files generated on 2023/12/01 remain unaffected.

#### `file-cleanup-cron-spec`

- The running cycle of the scheduled cleanup task, compatible with the crontab configuration.
- The format is `<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`
- Default value: `"0 0 2 * * *"`, which means that the cleanup task is executed every day at 2 AM

#### `flush-concurrency`

- The concurrency for uploading a single file.
- Default value: `1`, which means concurrency is disabled

#### `output-raw-change-event`

- Controls whether to output the original data change event. For more information, see [Control whether to split primary or unique key `UPDATE` events](/ticdc/ticdc-split-update-behavior.md#control-whether-to-split-primary-or-unique-key-update-events).
- Default value: `false`