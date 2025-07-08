---
title: TiCDC Changefeeds 的 CLI 和配置参数
summary: 了解 TiCDC changefeeds 的 CLI 和配置参数的定义。
---

# TiCDC Changefeeds 的 CLI 和配置参数

## Changefeed CLI 参数

本节通过示例说明如何创建复制（changefeed）任务，介绍 TiCDC changefeeds 的命令行参数：

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2024-12-26T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v8.1.2"}
```

- `--changefeed-id`: 复制任务的 ID。格式必须符合 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` 正则表达式。如果未指定此 ID，TiCDC 会自动生成一个 UUID（版本 4 格式）作为 ID。
- `--sink-uri`: 复制任务的下游地址。请根据以下格式配置 `--sink-uri`。目前，支持的 scheme 有 `mysql`、`tidb` 和 `kafka`。

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    当 sink URI 中包含特殊字符如 `! * ' ( ) ; : @ & = + $ , / ? % # [ ]` 时，需要对特殊字符进行转义，例如使用 [URI Encoder](https://www.urlencoder.org/)。

- `--start-ts`: 指定 changefeed 的起始 TSO。从此 TSO 开始，TiCDC 集群开始拉取数据。默认值为当前时间。
- `--target-ts`: 指定 changefeed 的结束 TSO。到此 TSO，TiCDC 集群停止拉取数据。默认为空，表示 TiCDC 不会自动停止拉取数据。
- `--config`: 指定 changefeed 的配置文件。

## Changefeed 配置参数

本节介绍复制任务的配置。

```toml
# 指定捕获服务器中 sink 管理器可用的内存配额（字节数）。
# 超出此值，超用部分将由 go 运行时回收。
# 默认值为 `1073741824`（1 GB）。
# memory-quota = 1073741824

# 指定配置文件中数据库名和表名是否区分大小写。
# 从 v6.5.6、v7.1.3 和 v7.5.0 开始，默认值由 true 改为 false。
# 此配置项影响过滤和 sink 相关的配置。
case-sensitive = false

# 指定是否启用 Syncpoint 功能，该功能自 v6.3.0 起支持，默认为禁用。
# 从 v6.4.0 起，只有具有 SYSTEM_VARIABLES_ADMIN 或 SUPER 权限的 changefeed 才能使用 TiCDC Syncpoint 功能。
# 注意：此配置项仅在下游为 TiDB 时生效。
# enable-sync-point = false

# 指定 Syncpoint 对上游和下游快照进行对齐的间隔时间。
# 格式为 h m s，例如 "1h30m30s"。
# 默认值为 "10m"，最小值为 "30s"。
# 注意：此配置项仅在下游为 TiDB 时生效。
# sync-point-interval = "5m"

# 指定 Syncpoint 在下游表中保留数据的时间长度。超过此时间，数据将被清理。
# 格式为 h m s，例如 "24h30m30s"。
# 默认值为 "24h"。
# 注意：此配置项仅在下游为 TiDB 时生效。
# sync-point-retention = "1h"

# 从 v6.5.6、v7.1.3 和 v7.5.0 起，此配置项指定解析 DDL 语句时使用的 SQL 模式，多个模式用逗号分隔。
# 默认值与 TiDB 的默认 SQL 模式相同。
# sql-mode = "ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION"

# 允许 changefeed 在发生内部错误或异常时自动重试的持续时间。默认值为 30 分钟。
# 如果在此时间内，changefeed 发生内部错误或异常且持续存在，则会进入失败状态。
# 需要手动重启 changefeed 以恢复。
# 格式为 "h m s"，例如 "1h30m30s"。
changefeed-error-stuck-duration = "30m"

# 默认值为 false，表示未启用双向复制（BDR）模式。
# 若要使用 TiCDC 搭建 BDR 集群，请将此参数改为 `true`，并将 TiDB 集群设置为 BDR 模式。
# 详细信息请参见 https://docs.pingcap.com/tidb/stable/ticdc-bidirectional-replication。
# bdr-mode = false

[mounter]
# 解码 KV 数据的线程数，默认值为 16。
# worker-num = 16

[filter]
# 忽略指定 start_ts 的事务。
# ignore-txn-start-ts = [1, 2]

# 过滤规则。
# 过滤语法详见 <https://docs.pingcap.com/tidb/stable/table-filter#syntax>。
rules = ['*.*', '!test.*']

# 事件过滤规则。
# 详细语法见 <https://docs.pingcap.com/tidb/stable/ticdc-filter>
# 第一个事件过滤规则。
# [[filter.event-filters]]
# matcher = ["test.worker"] # matcher 为允许列表，仅对 test 数据库中的 worker 表生效。
# ignore-event = ["insert"] # 忽略 insert 事件。
# ignore-sql = ["^drop", "add column"] # 忽略以 "drop" 开头或包含 "add column" 的 DDL。
# ignore-delete-value-expr = "name = 'john'" # 忽略包含条件 "name = 'john'" 的 delete DML。
# ignore-insert-value-expr = "id >= 100" # 忽略包含条件 "id >= 100" 的 insert DML。
# ignore-update-old-value-expr = "age < 18" # 忽略旧值包含 "age < 18" 的 update DML。
# ignore-update-new-value-expr = "gender = 'male'" # 忽略新值包含 "gender = 'male'" 的 update DML。

# 第二个事件过滤规则。
# matcher = ["test.fruit"] # matcher 为允许列表，仅对 test 数据库中的 fruit 表生效。
# ignore-event = ["drop table", "delete"] # 忽略 `drop table` DDL 事件和 `delete` DML 事件。注意：在 TiDB 中，当聚簇索引列的值被更新时，TiCDC 会将 `UPDATE` 事件拆分为 `DELETE` 和 `INSERT` 事件。TiCDC 无法将此类事件识别为 `UPDATE`，因此无法正确过滤。
# ignore-sql = ["^drop table", "alter table"] # 忽略以 `drop table` 开头或包含 `alter table` 的 DDL 语句。
# ignore-insert-value-expr = "price > 1000 and origin = 'no where'" # 忽略包含条件 "price > 1000" 和 "origin = 'no where'" 的 insert DML。

[scheduler]
# 将表分配到多个 TiCDC 节点进行复制，按区域（Region）划分。
# 注意：此配置项仅在 Kafka changefeed 上生效，不支持 MySQL changefeed。
# 默认为 false。设置为 true 以启用此功能。
enable-table-across-nodes = false
# 当 `enable-table-across-nodes` 被启用时，有两种分配模式：
# 1. 根据 Region 数量分配表，使每个 TiCDC 节点大致处理相同数量的 Region。如果某个表的 Region 数量超过 `region-threshold`，则该表会被分配到多个节点进行复制。`region-threshold` 的默认值为 100000。
# region-threshold = 100000
# 2. 根据写入流量分配表，使每个 TiCDC 节点大致处理相同数量的变更行数。只有当某个表每分钟的变更行数超过 `write-key-threshold` 时，此分配模式才会生效。
# write-key-threshold = 30000
# 说明：
# * `write-key-threshold` 的默认值为 0，表示默认不使用流量分配模式。
# * 只需配置其中一个模式。如果同时配置了 `region-threshold` 和 `write-key-threshold`，TiCDC 会优先采用流量分配模式，即 `write-key-threshold`。

[sink]
############ MQ sink 配置项 ############
# 对于 MQ 类型的 sink，可以使用调度器配置事件调度器。
# 自 v6.1.0 起，TiDB 支持两种事件调度器：partition 和 topic。详细信息请参见 <partition and topic link>。
# matcher 的匹配语法与过滤规则相同。详情请参见 <>。
# 注意：此配置项仅在下游为 MQ 时生效。
# 注意：当下游 MQ 为 Pulsar 时，如果 `partition` 的路由规则未指定为 `ts`、`index-value`、`table` 或 `default`，则每个 Pulsar 消息会使用你设置的字符串作为 key 进行路由。
# 例如，如果你为 matcher 指定路由规则为字符串 `code`，则所有匹配该 matcher 的 Pulsar 消息都将以 `code` 作为 key 进行路由。
# dispatchers = [
#    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "index-value"},
#    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value", index = "index1"},
#    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
#    {matcher = ['test6.*'], partition = "columns", columns = "['a', 'b']"}
#    {matcher = ['test7.*'], partition = "ts"}
# ]

# column-selectors 在 v7.5.0 起引入，仅在下游为 Kafka 时生效。
# 用于选择特定列进行复制。
# column-selectors = [
#     {matcher = ['test.t1'], columns = ['a', 'b']},
#     {matcher = ['test.*'], columns = ["*", "!b"]},
#     {matcher = ['test1.t1'], columns = ['column*', '!column1']},
#     {matcher = ['test3.t'], columns = ["column?", "!column1"]},
# ]

# 协议配置项指定用于编码消息的协议格式。
# 当下游为 Kafka 时，可选值有 canal-json、avro、debezium、open-protocol 或 simple。
# 当下游为 Pulsar 时，仅支持 canal-json。
# 当下游为存储服务时，仅支持 canal-json 或 csv。
# 注意：此配置项仅在下游为 Kafka、Pulsar 或存储服务时生效。
# protocol = "canal-json"

# 从 v7.2.0 起，`delete-only-output-handle-key-columns` 参数指定 DELETE 事件的输出内容。仅在 canal-json 和 open-protocol 协议下有效。
# 此参数与 `force-replicate` 不兼容。如果同时将此参数和 `force-replicate` 设置为 `true`，创建 changefeed 时会报错。
# 默认值为 false，表示输出所有列。设置为 true 时，仅输出主键列或唯一索引列。
# Avro 协议不受此参数控制，始终只输出主键列或唯一索引列。
# CSV 协议不受此参数控制，始终输出所有列。
delete-only-output-handle-key-columns = false

# schema registry URL。
# 注意：此配置项仅在下游为 MQ 时生效。
# schema-registry = "http://localhost:80801/subjects/{subject-name}/versions/{version-number}/schema"

# 指定编码数据时使用的编码器线程数。
# 注意：此配置项仅在下游为 MQ 时生效。
# 默认值为 32。
# encoder-concurrency = 32

# 指定是否启用使用 kafka-go sink 库的 kafka-sink-v2。
# 注意：此配置项为实验性功能，仅在下游为 MQ 时生效。
# 默认值为 false。
# enable-kafka-sink-v2 = false

# 从 v7.1.0 起，此配置项指定是否只输出更新的列。
# 注意：此配置项仅适用于使用 open-protocol 和 canal-json 的 MQ 下游。
# 默认值为 false。
# only-output-updated-columns = false

############ 存储 sink 配置项 ############
# 以下三个配置项仅在将数据复制到存储 sink 时使用，复制到 MQ 或 MySQL sink 时可忽略。
# 行终止符，用于分隔两个数据变更事件。默认值为空字符串，表示使用 "\r\n"。
# terminator = ''
# 文件目录中使用的日期分隔符类型。可选值为 `none`、`year`、`month` 和 `day`。`day` 为默认值，表示按天分隔文件。详细信息请参见 <https://docs.pingcap.com/tidb/stable/ticdc-sink-to-cloud-storage#data-change-records>。
# 注意：此配置项仅在下游为存储服务时生效。
date-separator = 'day'
# 是否使用分区作为分隔字符串。默认值为 true，表示表中的分区存储在不同目录中。建议保持此值为 `true`，以避免下游分区表可能导致的数据丢失 <https://github.com/pingcap/tiflow/issues/8724>。示例请参见 <https://docs.pingcap.com/tidb/dev/ticdc-sink-to-cloud-storage#data-change-records>。
# 注意：此配置项仅在下游为存储服务时生效。
enable-partition-separator = true

# 控制是否禁用输出 schema 信息。默认值为 false，表示启用 schema 信息输出。
# 注意：此参数仅在 sink 类型为 MQ 且输出协议为 Debezium 时生效。
debezium-disable-schema = false

# 从 v6.5.0 起，TiCDC 支持将数据变更保存为 CSV 格式的存储。若复制数据到 MQ 或 MySQL sink，可忽略以下配置。
# [sink.csv]
# 用于分隔 CSV 文件中字段的字符。必须为 ASCII 字符，默认值为 `,`。
# delimiter = ','
# 用于包裹字段的引号字符。默认值为 `"。` 若为空，则不使用引号。
# quote = '"'
# CSV 列为空时显示的字符。默认值为 `\N`。
# null = '\N'
# 是否在 CSV 行中包含 commit-ts。默认值为 false。
# include-commit-ts = false
# 二进制数据的编码方式，可为 'base64' 或 'hex'。默认值为 'base64'。
# binary-encoding-method = 'base64'
# 是否输出 handle key 信息。默认值为 false。
# output-handle-key = false
# 是否输出变更前的行数据值。默认值为 false。
# 当启用时，UPDATE 事件会输出两行数据：第一行为变更前的数据（DELETE 事件），第二行为变更后的数据（INSERT 事件）。
# 启用（设置为 true）后，会在带有数据变更的列前添加 "is-update" 列，用于标识当前行的数据变更是否来自 UPDATE 事件。
# 如果当前行的数据变更来自 UPDATE 事件，"is-update" 列的值为 true，否则为 false。
# output-old-value = false

# 从 v8.0.0 起，TiCDC 支持 Simple 消息编码协议。以下为 Simple 协议的配置参数。
# 详见 <https://docs.pingcap.com/tidb/stable/ticdc-simple-protocol>。
# 以下配置控制引导消息的发送行为。
# send-bootstrap-interval-in-sec 控制发送引导消息的时间间隔（秒）。
# 默认值为 120 秒，即每个表每 120 秒发送一次引导消息。
# send-bootstrap-interval-in-sec = 120

# send-bootstrap-in-msg-count 控制引导消息的发送间隔（消息数）。
# 默认值为 10000，即每个表每 10000 条变更消息发送一次引导消息。
# send-bootstrap-in-msg-count = 10000
# 注意：若要禁用引导消息的发送，将两个参数都设置为 0。

# send-bootstrap-to-all-partition 控制是否将引导消息发送到所有分区。
# 默认值为 true，表示发送到对应表主题的所有分区。
# 设置为 false 时，仅发送到对应表主题的第一个分区。
# send-bootstrap-to-all-partition = true

[sink.kafka-config.codec-config]
# 编码格式控制 Simple 协议消息的编码格式。目前支持 "json" 和 "avro"。
# 默认值为 "json"。
# encoding-format = "json"

[sink.open]
# 是否输出变更前的行数据值。默认值为 true。禁用后，UPDATE 事件不输出 "p" 字段。
# output-old-value = true

[sink.debezium]
# 是否输出变更前的行数据值。默认值为 true。禁用后，UPDATE 事件不输出 "before" 字段。
# output-old-value = true

# 指定使用重做日志（redo log）时的复制一致性配置。详见 https://docs.pingcap.com/tidb/stable/ticdc-sink-to-mysql#eventually-consistent-replication-in-disaster-scenarios。
# 注意：此一致性相关配置项仅在下游为数据库且启用重做日志功能时生效。
[consistent]
# 数据一致性级别。可选值为 "none" 和 "eventual"。 "none" 表示禁用重做日志。
# 默认值为 "none"。
level = "none"
# 最大重做日志大小（MB）。
# 默认值为 64。
max-log-size = 64
# 重做日志的刷新间隔（毫秒），默认值为 2000。
flush-interval = 2000
# 重做日志存储 URI。
# 默认值为空。
storage = ""
# 指定是否将重做日志存储在本地文件中。
# 默认值为 false。
use-file-backend = false
# 重做模块中的编码和解码工作线程数。
# 默认值为 16。
encoding-worker-num = 16
# 重做模块中的刷新工作线程数。
# 默认值为 8。
flush-worker-num = 8
# 压缩重做日志文件的行为（在 v6.5.6、v7.1.3、v7.5.1 和 v7.6.0 中引入）。
# 可选值为空字符串 "" 和 "lz4"。默认值为空，表示不压缩。
compression = ""
# 上传单个重做文件的并发数（在 v6.5.6、v7.1.3、v7.5.1 和 v7.6.0 中引入）。
# 默认值为 1，表示不启用并发。
flush-concurrency = 1

[integrity]
# 是否启用单行数据的校验和验证。默认值为 "none"，表示禁用此功能。可选值为 "none" 和 "correctness"。
integrity-check-level = "none"
# 指定在单行数据校验和验证失败时的日志级别。默认值为 "warn"。可选值为 "warn" 和 "error"。
corruption-handle-level = "warn"

# 以下配置项仅在下游为 Kafka 时生效。
[sink.kafka-config]
# Kafka SASL 认证机制。默认为空，表示不使用 SASL 认证。
sasl-mechanism = "OAUTHBEARER"
# Kafka SASL OAUTHBEARER 认证中的 client-id。默认为空。使用此认证时必须配置。
sasl-oauth-client-id = "producer-kafka"
# Kafka SASL OAUTHBEARER 认证中的 client-secret。默认为空。使用此认证时必须配置。
sasl-oauth-client-secret = "cHJvZHVjZXIta2Fma2E="
# Kafka SASL OAUTHBEARER 认证中的 token-url，用于获取 token。默认为空。使用此认证时必须配置。
sasl-oauth-token-url = "http://127.0.0.1:4444/oauth2/token"
# Kafka SASL OAUTHBEARER 认证中的 scopes。默认为空。使用此认证时为可选。
sasl-oauth-scopes = ["producer.kafka", "consumer.kafka"]
# Kafka SASL OAUTHBEARER 认证中的 grant-type。默认为 "client_credentials"。使用此认证时为可选。
sasl-oauth-grant-type = "client_credentials"
# Kafka SASL OAUTHBEARER 认证中的 audience。默认为空。使用此认证时为可选。
sasl-oauth-audience = "kafka"

# 以下配置项控制是否输出原始数据变更事件。默认值为 false。详见 https://docs.pingcap.com/tidb/v8.1/ticdc-split-update-behavior#control-whether-to-split-primary-or-unique-key-update-events。
# output-raw-change-event = false

# 以下配置仅在使用 Avro 作为协议且启用 AWS Glue Schema Registry 时需要：
# 详见 "Sync Data to Kafka" 文档中的 "Integrate TiCDC with AWS Glue Schema Registry" 部分：https://docs.pingcap.com/tidb/dev/ticdc-sink-to-kafka#integrate-ticdc-with-aws-glue-schema-registry
# [sink.kafka-config.glue-schema-registry-config]
# region="us-west-1"  
# registry-name="ticdc-test"
# access-key="xxxx"
# secret-access-key="xxxx"
# token="xxxx"

# 以下参数仅在下游为 Pulsar 时生效。
[sink.pulsar-config]
# 使用 token 进行 Pulsar 服务器的认证。请指定 token 的值。
authentication-token = "xxxxxxxxxxxxx"
# 使用 token 进行 Pulsar 服务器认证时，指定 token 文件的路径。
token-from-file="/data/pulsar/token-file.txt"
# Pulsar 使用基本账号密码进行身份验证。请指定账号。
basic-user-name="root"
# Pulsar 使用基本账号密码进行身份验证。请指定密码。
basic-password="password"
# Pulsar TLS 加密认证的证书路径。
auth-tls-certificate-path="/data/pulsar/certificate"
# Pulsar TLS 加密认证的私钥路径。
auth-tls-private-key-path="/data/pulsar/certificate.key"
# Pulsar TLS 加密认证的信任证书文件路径。
tls-trust-certs-file-path="/data/pulsar/tls-trust-certs-file"
# Pulsar oauth2 issuer-url。详见 Pulsar 官方文档：https://pulsar.apache.org/docs/2.10.x/client-libraries-go/#tls-encryption-and-authentication
oauth2.oauth2-issuer-url="https://xxxx.auth0.com"
# Pulsar oauth2 audience
oauth2.oauth2-audience="https://xxxx.auth0.com/api/v2/"
# Pulsar oauth2 私钥路径
oauth2.oauth2-private-key="/data/pulsar/privateKey"
# Pulsar oauth2 client-id
oauth2.oauth2-client-id="0Xx...Yyxeny"
# Pulsar oauth2 scope
oauth2.oauth2-scope="xxxx"
# TiCDC 中缓存的 Pulsar 生产者数量，默认值为 10240。每个 Pulsar 生产者对应一个 topic。如果需要复制的 topic 数量超过此值，需要增加。
pulsar-producer-cache-size=10240
# Pulsar 数据压缩方式。默认不压缩。可选值为 "lz4"、"zlib" 和 "zstd"。
compression-type=""
# Pulsar 客户端与服务器建立 TCP 连接的超时时间，默认值为 5 秒。
connection-timeout=5
# Pulsar 客户端发起创建和订阅等操作的超时时间，默认值为 30 秒。
operation-timeout=30
# Pulsar 生产者单次批量发送的最大消息数，默认值为 1000。
batching-max-messages=1000
# Pulsar 生产者批量保存消息的间隔时间（毫秒），默认值为 10 毫秒。
batching-max-publish-delay=10
# Pulsar 生产者发送消息的超时时间（秒），默认值为 30 秒。
send-timeout=30

# 以下配置项控制是否输出原始数据变更事件。默认值为 false。详见 https://docs.pingcap.com/tidb/v8.1/ticdc-split-update-behavior#control-whether-to-split-primary-or-unique-key-update-events。
# output-raw-change-event = false

[sink.cloud-storage-config]
# 将数据变更保存到下游云存储的并发数。
# 默认值为 16。
worker-count = 16
# 保存数据变更到下游云存储的间隔时间。
# 默认值为 "2s"。
flush-interval = "2s"
# 当数据变更文件的字节数超过 `file-size` 时，文件会被保存到云存储中。
# 默认值为 67108864（即 64 MiB）。
file-size = 67108864
# 文件的保留时间，仅在 `date-separator` 设置为 `day` 时生效。假设 `file-expiration-days = 1` 和 `file-cleanup-cron-spec = "0 0 0 * * *"`，则 TiCDC 每天 00:00:00 执行清理，清除超过 24 小时的文件。例如，在 2023/12/02 00:00:00 时，TiCDC 会清理 2023/12/01 之前生成的文件，2023/12/01 生成的文件不受影响。
# 默认值为 0，表示不启用文件清理。
file-expiration-days = 0
# 定期清理任务的运行周期，支持 crontab 格式，格式为 `<Second> <Minute> <Hour> <Day of the month> <Month> <Day of the week (Optional)>`。
# 默认值为 "0 0 2 * * *"，表示每天 2 点执行清理。
file-cleanup-cron-spec = "0 0 2 * * *"
# 上传单个文件的并发数。
# 默认值为 1，表示不启用并发。
flush-concurrency = 1
# 控制是否输出原始数据变更事件。默认值为 false。详见 https://docs.pingcap.com/tidb/v8.1/ticdc-split-update-behavior#control-whether-to-split-primary-or-unique-key-update-events。
# output-raw-change-event = false
```