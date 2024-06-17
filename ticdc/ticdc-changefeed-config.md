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
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2024-05-24T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.1.0"}
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

```toml
# Specifies the memory quota (in bytes) that can be used in the capture server by the sink manager.
# If the value is exceeded, the overused part will be recycled by the go runtime.
# The default value is `1073741824` (1 GB).
# memory-quota = 1073741824

# Specifies whether the database names and tables in the configuration file are case-sensitive.
# Starting from v6.5.6, v7.1.3, and v7.5.0, the default value changes from true to false.
# This configuration item affects configurations related to filter and sink.
case-sensitive = false

# Specifies whether to enable the Syncpoint feature, which is supported since v6.3.0 and is disabled by default.
# Since v6.4.0, only the changefeed with the SYSTEM_VARIABLES_ADMIN or SUPER privilege can use the TiCDC Syncpoint feature.
# Note: This configuration item only takes effect if the downstream is TiDB.
# enable-sync-point = false

# Specifies the interval at which Syncpoint aligns the upstream and downstream snapshots.
# The format is in h m s. For example, "1h30m30s".
# The default value is "10m" and the minimum value is "30s".
# Note: This configuration item only takes effect if the downstream is TiDB.
# sync-point-interval = "5m"

# Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up.
# The format is in h m s. For example, "24h30m30s".
# The default value is "24h".
# Note: This configuration item only takes effect if the downstream is TiDB.
# sync-point-retention = "1h"

# Starting from v6.5.6, v7.1.3, and v7.5.0, this configuration item specifies the SQL mode used when parsing DDL statements. Multiple modes are separated by commas.
# The default value is the same as the default SQL mode of TiDB.
# sql-mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"

# The duration for which the changefeed is allowed to automatically retry when internal errors or exceptions occur. The default value is 30 minutes.
# The changefeed enters the failed state if internal errors or exceptions occur in the changefeed and persist longer than the duration set by this parameter.
# When the changefeed is in the failed state, you need to restart the changefeed manually for recovery.
# The format of this parameter is "h m s", for example, "1h30m30s".
changefeed-error-stuck-duration = "30m"

[mounter]
# The number of threads with which the mounter decodes KV data. The default value is 16.
# worker-num = 16

[filter]
# Ignores the transaction of specified start_ts.
# ignore-txn-start-ts = [1, 2]

# Filter rules.
# Filter syntax: <https://docs.pingcap.com/tidb/stable/table-filter#syntax>.
rules = ['*.*', '!test.*']

# Event filter rules.
# The detailed syntax is described in <https://docs.pingcap.com/tidb/stable/ticdc-filter>
# The first event filter rule.
# [[filter.event-filters]]
# matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
# ignore-event = ["insert"] # Ignore insert events.
# ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
# ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
# ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
# ignore-update-old-value-expr = "age < 18" # Ignore update DMLs whose old value contains "age < 18".
# ignore-update-new-value-expr = "gender = 'male'" # Ignore update DMLs whose new value contains "gender = 'male'".

# The second event filter rule.
# matcher = ["test.fruit"] # matcher is an allow list, which means this rule only applies to the fruit table in the test database.
# ignore-event = ["drop table", "delete"] # Ignore the `drop table` DDL events and the `delete` DML events.
# ignore-sql = ["^drop table", "alter table"] # Ignore DDL statements that start with `drop table` or contain `alter table`.
# ignore-insert-value-expr = "price > 1000 and origin = 'no where'" # Ignore insert DMLs that contain the conditions "price > 1000" and "origin = 'no where'".

[scheduler]
# Allocate tables to multiple TiCDC nodes for replication on a per-Region basis.
# Note: This configuration item only takes effect on Kafka changefeeds and is not supported on MySQL changefeeds.
# The value is "false" by default. Set it to "true" to enable this feature.
enable-table-across-nodes = false
# When `enable-table-across-nodes` is enabled, there are two allocation modes:
# 1. Allocate tables based on the number of Regions, so that each TiCDC node handles roughly the same number of Regions. If the number of Regions for a table exceeds the value of `region-threshold`, the table will be allocated to multiple nodes for replication. The default value of `region-threshold` is 10000.
# region-threshold = 10000
# 2. Allocate tables based on the write traffic, so that each TiCDC node handles roughly the same number of modified rows. Only when the number of modified rows per minute in a table exceeds the value of `write-key-threshold`, will this allocation take effect.
# write-key-threshold = 30000
# Note:
# * The default value of `write-key-threshold` is 0, which means that the traffic allocation mode is not used by default.
# * You only need to configure one of the two modes. If both `region-threshold` and `write-key-threshold` are configured, TiCDC prioritizes the traffic allocation mode, namely `write-key-threshold`.

[sink]
############ MQ sink configuration items ############
# For the sink of MQ type, you can use dispatchers to configure the event dispatcher.
# Since v6.1.0, TiDB supports two types of event dispatchers: partition and topic. For more information, see <partition and topic link>.
# The matching syntax of matcher is the same as the filter rule syntax. For details about the matcher rules, see <>.
# Note: This configuration item only takes effect if the downstream is MQ.
# Note: When the downstream MQ is Pulsar, if the routing rule for `partition` is not specified as any of `ts`, `index-value`, `table`, or `default`, each Pulsar message will be routed using the string you set as the key.
# For example, if you specify the routing rule for a matcher as the string `code`, then all Pulsar messages that match that matcher will be routed with `code` as the key.
# dispatchers = [
#    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "index-value"},
#    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value", index = "index1"},
#    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
#    {matcher = ['test6.*'], partition = "columns", columns = "['a', 'b']"}
#    {matcher = ['test7.*'], partition = "ts"}
# ]

# column-selectors is introduced in v7.5.0 and only takes effect when the downstream is Kafka.
# column-selectors is used to select specific columns for replication.
# column-selectors = [
#     {matcher = ['test.t1'], columns = ['a', 'b']},
#     {matcher = ['test.*'], columns = ["*", "!b"]},
#     {matcher = ['test1.t1'], columns = ['column*', '!column1']},
#     {matcher = ['test3.t'], columns = ["column?", "!column1"]},
# ]

# The protocol configuration item specifies the protocol format used for encoding messages.
# When the downstream is Kafka, the protocol can be canal-json, avro, debezium, open-protocol, or simple.
# When the downstream is Pulsar, the protocol can only be canal-json.
# When the downstream is a storage service, the protocol can only be canal-json or csv.
# Note: This configuration item only takes effect if the downstream is Kafka, Pulsar, or a storage service.
# protocol = "canal-json"

# Starting from v7.2.0, the `delete-only-output-handle-key-columns` parameter specifies the output of DELETE events. This parameter is valid only for canal-json and open-protocol protocols.
# This parameter is incompatible with `force-replicate`. If both this parameter and `force-replicate` is set to `true`, TiCDC reports an error when creating a changefeed.
# The default value is false, which means outputting all columns. When you set it to true, only primary key columns or unique index columns are output.
# The Avro protocol is not controlled by this parameter and always outputs only the primary key columns or unique index columns.
# The CSV protocol is not controlled by this parameter and always outputs all columns.
delete-only-output-handle-key-columns = false

# Schema registry URL.
# Note: This configuration item only takes effect if the downstream is MQ.
# schema-registry = "http://localhost:80801/subjects/{subject-name}/versions/{version-number}/schema"

# Specifies the number of encoder threads used when encoding data.
# Note: This configuration item only takes effect if the downstream is MQ.
# The default value is 32.
# encoder-concurrency = 32

# Specifies whether to enable kafka-sink-v2 that uses the kafka-go sink library.
# Note: This configuration item is experimental, and only takes effect if the downstream is MQ.
# The default value is false.
# enable-kafka-sink-v2 = false

# Starting from v7.1.0, this configuration item specifies whether to only output the updated columns.
# Note: This configuration item only applies to the MQ downstream using the open-protocol and canal-json.
# The default value is false.
# only-output-updated-columns = false

############ Storage sink configuration items ############
# The following three configuration items are only used when you replicate data to storage sinks and can be ignored when replicating data to MQ or MySQL sinks.
# Row terminator, used for separating two data change events. The default value is an empty string, which means "\r\n" is used.
# terminator = ''
# Date separator type used in the file directory. Value options are `none`, `year`, `month`, and `day`. `day` is the default value and means separating files by day. For more information, see <https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#data-change-records>.
# Note: This configuration item only takes effect if the downstream is a storage service.
date-separator = 'day'
# Whether to use partitions as the separation string. The default value is true, which means that partitions in a table are stored in separate directories. It is recommended that you keep the value as `true` to avoid potential data loss in downstream partitioned tables <https://github.com/pingcap/tiflow/issues/8724>. For usage examples, see <https://docs.pingcap.com/tidb/dev/ticdc-sink-to-cloud-storage#data-change-records)>.
# Note: This configuration item only takes effect if the downstream is a storage service.
enable-partition-separator = true

# Since v6.5.0, TiCDC supports saving data changes to storage services in CSV format. Ignore the following configurations if you replicate data to MQ or MySQL sinks.
# [sink.csv]
# The character used to separate fields in the CSV file. The value must be an ASCII character and defaults to `,`.
# delimiter = ','
# The quotation character used to surround fields in the CSV file. The default value is `"`. If the value is empty, no quotation is used.
# quote = '"'
# The character displayed when a CSV column is null. The default value is `\N`.
# null = '\N'
# Whether to include commit-ts in CSV rows. The default value is false.
# include-commit-ts = false
# The encoding method of binary data, which can be 'base64' or 'hex'. The default value is 'base64'.
# binary-encoding-method = 'base64'
# Whether to output handle key information. The default value is false. 
# This configuration parameter is for internal implementation only, so it is not recommended to set it.
# output-handle-key = false
# Whether to output the value before the row data changes. The default value is false. 
# When it is enabled, the UPDATE event will output two rows of data: the first row is a DELETE event that outputs the data before the change; the second row is an INSERT event that outputs the changed data.
# When it is enabled (setting it to true), the "is-update" column will be added before the column with data changes. This added column is used to identify whether the data change of the current row comes from the UPDATE event or the original INSERT/DELETE event.
# If the data change of the current row comes from the UPDATE event, the value of the "is-update" column is true. Otherwise it is false.
# output-old-value = false

# Starting from v8.0.0, TiCDC supports the Simple message encoding protocol. The following are the configuration parameters for the Simple protocol.
# For more information about the protocol, see <https://docs.pingcap.com/tidb/stable/ticdc-simple-protocol>.
# The following configuration parameters control the sending behavior of bootstrap messages.
# send-bootstrap-interval-in-sec controls the time interval for sending bootstrap messages, in seconds.
# The default value is 120 seconds, which means that a bootstrap message is sent every 120 seconds for each table.
# send-bootstrap-interval-in-sec = 120

# send-bootstrap-in-msg-count controls the message interval for sending bootstrap, in message count.
# The default value is 10000, which means that a bootstrap message is sent every 10000 row changed messages for each table.
# send-bootstrap-in-msg-count = 10000
# Note: If you want to disable the sending of bootstrap messages, set both send-bootstrap-interval-in-sec and send-bootstrap-in-msg-count to 0.

# send-bootstrap-to-all-partition controls whether to send bootstrap messages to all partitions.
# The default value is true, which means that bootstrap messages are sent to all partitions of the corresponding table topic.
# Setting it to false means bootstrap messages are sent to only the first partition of the corresponding table topic.
# send-bootstrap-to-all-partition = true

[sink.kafka-config.codec-config]
# encoding-format controls the encoding format of the Simple protocol messages. Currently, the Simple protocol message supports "json" and "avro" encoding formats.
# The default value is "json".
# encoding-format = "json"

[sink.open]
# Whether to output the value before the row data changes. The default value is true. When it is disabled, the UPDATE event does not output the "p" field.
# output-old-value = true

[sink.debezium]
# Whether to output the value before the row data changes. The default value is true. When it is disabled, the UPDATE event does not output the "before" field.
# output-old-value = true

# Specifies the replication consistency configurations for a changefeed when using the redo log. For more information, see https://docs.pingcap.com/tidb/stable/ticdc-sink-to-mysql#eventually-consistent-replication-in-disaster-scenarios.
# Note: The consistency-related configuration items only take effect when the downstream is a database and the redo log feature is enabled.
[consistent]
# The data consistency level. Available options are "none" and "eventual". "none" means that the redo log is disabled.
# The default value is "none".
level = "none"
# The max redo log size in MB.
# The default value is 64.
max-log-size = 64
# The flush interval for redo log. The default value is 2000 milliseconds.
flush-interval = 2000
# The storage URI of the redo log.
# The default value is empty.
storage = ""
# Specifies whether to store the redo log in a local file.
# The default value is false.
use-file-backend = false
# The number of encoding and decoding workers in the redo module.
# The default value is 16.
encoding-worker-num = 16
# The number of flushing workers in the redo module.
# The default value is 8.
flush-worker-num = 8
# The behavior to compress redo log files.
# Available options are "" and "lz4". The default value is "", which means no compression.
compression = ""
# The concurrency for uploading a single redo file.
# The default value is 1, which means concurrency is disabled.
flush-concurrency = 1

[integrity]
# Whether to enable the checksum validation for single-row data. The default value is "none", which means to disable the feature. Value options are "none" and "correctness".
integrity-check-level = "none"
# Specifies the log level of the Changefeed when the checksum validation for single-row data fails. The default value is "warn". Value options are "warn" and "error".
corruption-handle-level = "warn"

# The following configuration items only take effect when the downstream is Kafka.
[sink.kafka-config]
# The mechanism of Kafka SASL authentication. The default value is empty, indicating that SASL authentication is not used.
sasl-mechanism = "OAUTHBEARER"
# The client-id in the Kafka SASL OAUTHBEARER authentication. The default value is empty. This parameter is required when the OAUTHBEARER authentication is used.
sasl-oauth-client-id = "producer-kafka"
# The client-secret in the Kafka SASL OAUTHBEARER authentication. The default value is empty. This parameter is required when the OAUTHBEARER authentication is used.
sasl-oauth-client-secret = "cHJvZHVjZXIta2Fma2E="
# The token-url in the Kafka SASL OAUTHBEARER authentication to obtain the token. The default value is empty. This parameter is required when the OAUTHBEARER authentication is used.
sasl-oauth-token-url = "http://127.0.0.1:4444/oauth2/token"
# The scopes in the Kafka SASL OAUTHBEARER authentication. The default value is empty. This parameter is optional when the OAUTHBEARER authentication is used.
sasl-oauth-scopes = ["producer.kafka", "consumer.kafka"]
# The grant-type in the Kafka SASL OAUTHBEARER authentication. The default value is "client_credentials". This parameter is optional when the OAUTHBEARER authentication is used.
sasl-oauth-grant-type = "client_credentials"
# The audience in the Kafka SASL OAUTHBEARER authentication. The default value is empty. This parameter is optional when the OAUTHBEARER authentication is used.
sasl-oauth-audience = "kafka"
# The following configuration is only required when using Avro as the protocol and AWS Glue Schema Registry:
# Please refer to the section "Integrate TiCDC with AWS Glue Schema Registry" in the document "Sync Data to Kafka": https://docs.pingcap.com/tidb/dev/ticdc-sink-to-kafka#integrate-ticdc-with-aws-glue-schema-registry
# [sink.kafka-config.glue-schema-registry-config]
# region="us-west-1"  
# registry-name="ticdc-test"
# access-key="xxxx"
# secret-access-key="xxxx"
# token="xxxx"

# The following parameters take effect only when the downstream is Pulsar.
[sink.pulsar-config]
# Authentication on the Pulsar server is done using a token. Specify the value of the token.
authentication-token = "xxxxxxxxxxxxx"
# When you use a token for Pulsar server authentication, specify the path to the file where the token is located.
token-from-file="/data/pulsar/token-file.txt"
# Pulsar uses the basic account and password to authenticate the identity. Specify the account.
basic-user-name="root"
# Pulsar uses the basic account and password to authenticate the identity. Specify the password.
basic-password="password"
# The certificate path for Pulsar TLS encrypted authentication.
auth-tls-certificate-path="/data/pulsar/certificate"
# The private key path for Pulsar TLS encrypted authentication.
auth-tls-private-key-path="/data/pulsar/certificate.key"
# Path to trusted certificate file of the Pulsar TLS encrypted authentication.
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
# Pulsar oauth2 issuer-url. For more information, see the Pulsar website: https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication
oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
# Pulsar oauth2 audience
oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
# Pulsar oauth2 private-key
oauth2.oauth2-private-key="/data/pulsar/privateKey"
# Pulsar oauth2 client-id
oauth2.oauth2-client-id="0Xx...Yyxeny"
# Pulsar oauth2 oauth2-scope
oauth2.oauth2-scope="xxxx"
# The number of cached Pulsar producers in TiCDC. The value is 10240 by default. Each Pulsar producer corresponds to one topic. If the number of topics you need to replicate is larger than the default value, you need to increase the number.
pulsar-producer-cache-size=10240
# Pulsar data compression method. No compression is used by default. Optional values are "lz4", "zlib", and "zstd".
compression-type=""
# The timeout for the Pulsar client to establish a TCP connection with the server. The value is 5 seconds by default.
connection-timeout=5
# The timeout for Pulsar clients to initiate operations such as creating and subscribing to a topic. The value is 30 seconds by default.
operation-timeout=30
# The maximum number of messages in a single batch for a Pulsar producer to send. The value is 1000 by default.
batching-max-messages=1000
# The interval at which Pulsar producer messages are saved for batching. The value is 10 milliseconds by default.
batching-max-publish-delay=10
# The timeout for a Pulsar producer to send a message. The value is 30 seconds by default.
send-timeout=30

[sink.cloud-storage-config]
# The concurrency for saving data changes to the downstream cloud storage. 
# The default value is 16.
worker-count = 16
# The interval for saving data changes to the downstream cloud storage.
# The default value is "2s".
flush-interval = "2s"
# A data change file is saved to the cloud storage when the number of bytes in this file exceeds `file-size`.
# The default value is 67108864 (this is, 64 MiB).
file-size = 67108864
# The duration to retain files, which takes effect only when `date-separator` is configured as `day`. Assume that `file-expiration-days = 1` and `file-cleanup-cron-spec = "0 0 0 * * *"`, then TiCDC performs daily cleanup at 00:00:00 for files saved beyond 24 hours. For example, at 00:00:00 on 2023/12/02, TiCDC cleans up files generated before 2023/12/01, while files generated on 2023/12/01 remain unaffected.
# The default value is 0, which means file cleanup is disabled. 
file-expiration-days = 0
# The running cycle of the scheduled cleanup task, compatible with the crontab configuration, with a format of `<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`
# The default value is "0 0 2 * * *", which means that the cleanup task is executed every day at 2 AM.
file-cleanup-cron-spec = "0 0 2 * * *"
# The concurrency for uploading a single file.
# The default value is 1, which means concurrency is disabled.
flush-concurrency = 1
```
