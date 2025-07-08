---
title: 将数据复制到 Kafka
summary: 学习如何使用 TiCDC 将数据复制到 Apache Kafka。
---

# 将数据复制到 Kafka

本文档描述了如何创建一个 changefeed，将增量数据复制到 Apache Kafka，使用 TiCDC。

## 创建复制任务

通过运行以下命令创建一个复制任务：

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="kafka://127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"kafka://127.0.0.1:9092,127.0.0.1:9093,127.0.0.1:9094/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1","opts":{},"create-time":"2023-11-28T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":false,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--server`: TiCDC 集群中任意 TiCDC 服务器的地址。
- `--changefeed-id`: 复制任务的 ID。格式必须符合 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` 正则表达式。如果未指定此 ID，TiCDC 会自动生成一个 UUID（版本 4 格式）作为 ID。
- `--sink-uri`: 复制任务的下游地址。详情请参见 [使用 `kafka` 配置 sink URI](#configure-sink-uri-for-kafka)。
- `--start-ts`: 指定 changefeed 的起始 TSO。从此 TSO 开始，TiCDC 集群开始拉取数据。默认值为当前时间。
- `--target-ts`: 指定 changefeed 的结束 TSO。到此 TSO，TiCDC 集群停止拉取数据。默认值为空，表示 TiCDC 不会自动停止拉取数据。
- `--config`: 指定 changefeed 配置文件。详情请参见 [TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

## 支持的 Kafka 版本

下表显示了每个 TiCDC 版本支持的最低 Kafka 版本：

| TiCDC 版本            | 最低支持的 Kafka 版本 |
|:---------------------|:---------------------|
| TiCDC >= v8.1.0      | 2.1.0                |
| v7.6.0 <= TiCDC < v8.1.0 | 2.4.0            |
| v7.5.2 <= TiCDC < v8.0.0 | 2.1.0            |
| v7.5.0 <= TiCDC < v7.5.2 | 2.4.0            |
| v6.5.0 <= TiCDC < v7.5.0 | 2.1.0            |
| v6.1.0 <= TiCDC < v6.5.0 | 2.0.0            |

## 配置 Kafka 的 sink URI

Sink URI 用于指定 TiCDC 目标系统的连接信息。格式如下：

```shell
[scheme]://[host]:[port][/path]?[query_parameters]
```

> **Tip:**
> 
> 如果下游 Kafka 有多个主机或端口，可以在 sink URI 中配置多个 `[host]:[port]`。例如：
>
> ```shell
> [scheme]://[host]:[port],[host]:[port],[host]:[port][/path]?[query_parameters]
> ```

示例配置：

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=canal-json&kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
```

以下是 Kafka sink URI 参数及其说明：

| 参数/参数值 | 描述 |
| :------------------ | :------------------------------------------------------------ |
| `host` | 下游 Kafka 服务的 IP 地址。 |
| `port` | 下游 Kafka 的端口。 |
| `topic-name` | 变量。Kafka 主题的名称。 |
| `protocol` | 输出到 Kafka 的消息协议。可选值包括 [`canal-json`](/ticdc/ticdc-canal-json.md)、[`open-protocol`](/ticdc/ticdc-open-protocol.md)、[`avro`](/ticdc/ticdc-avro-protocol.md)、[`debezium`](/ticdc/ticdc-debezium.md) 和 [`simple`](/ticdc/ticdc-simple-protocol.md)。 |
| `kafka-version` | 下游 Kafka 的版本。此值需与实际的 Kafka 版本保持一致。 |
| `kafka-client-id` | 指定复制任务的 Kafka 客户端 ID（可选，默认为 `TiCDC_sarama_producer_replication ID`）。 |
| `partition-num` | 下游 Kafka 分区的数量（可选，值不能大于实际的分区数，否则无法成功创建复制任务，默认为 `3`）。 |
| `max-message-bytes` | 每次发送到 Kafka broker 的最大数据大小（可选，默认为 `10MB`，从 v5.0.6 和 v4.0.6 起，默认值由 `64MB` 和 `256MB` 改为 `10MB`）。 |
| `replication-factor` | Kafka 消息副本的数量（可选，默认为 `1`，此值必须大于等于 Kafka 中 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 的值）。 |
| `required-acks` | 在 `Produce` 请求中使用的参数，通知 broker 在响应之前需要收到的副本确认数。可选值包括 `0`（`NoResponse`：无响应，只提供 `TCP ACK`）、`1`（`WaitForLocal`：仅在本地提交成功后响应）和 `-1`（`WaitForAll`：所有副本成功提交后响应。可以通过 Kafka 的 [`min.insync.replicas`](https://kafka.apache.org/33/documentation.html#brokerconfigs_min.insync.replicas) 配置项设置最小副本数）。）（可选，默认值为 `-1`）。 |
| `compression` | 发送消息时使用的压缩算法（可选，值包括 `none`、`lz4`、`gzip`、`snappy` 和 `zstd`，默认为 `none`）。注意，Snappy 压缩文件必须符合 [官方 Snappy 格式](https://github.com/google/snappy)，不支持其他变体。 |
| `auto-create-topic` | 决定当传入的 `topic-name` 在 Kafka 集群中不存在时，TiCDC 是否自动创建主题（可选，默认为 `true`）。 |
| `enable-tidb-extension` | 可选，默认为 `false`。当输出协议为 `canal-json` 时，如果值为 `true`，TiCDC 会发送 [WATERMARK 事件](/ticdc/ticdc-canal-json.md#watermark-event) 并在 Kafka 消息中添加 [TiDB 扩展字段](/ticdc/ticdc-canal-json.md#tidb-extension-field)。从 v6.1.0 起，此参数也适用于 `avro` 协议。若值为 `true`，TiCDC 会在 Kafka 消息中添加 [三个 TiDB 扩展字段](/ticdc/ticdc-avro-protocol.md#tidb-extension-fields)。 |
| `max-batch-size` | 在 v4.0.9 中新增。若消息协议支持将多个数据变更输出到一条 Kafka 消息，此参数指定一条 Kafka 消息中的最大数据变更数。目前仅在 Kafka 的 `protocol` 为 `open-protocol` 时生效（可选，默认为 `16`）。 |
| `enable-tls` | 是否使用 TLS 连接到下游 Kafka 实例（可选，默认为 `false`）。 |
| `ca` | 连接到下游 Kafka 实例所需的 CA 证书文件路径（可选）。 |
| `cert` | 连接到下游 Kafka 实例所需的证书文件路径（可选）。 |
| `key` | 连接到下游 Kafka 实例所需的证书密钥文件路径（可选）。 |
| `insecure-skip-verify` | 连接到下游 Kafka 实例时是否跳过证书验证（可选，默认为 `false`）。 |
| `sasl-user` | 连接到下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 认证的身份（authcid）（可选）。 |
| `sasl-password` | 连接到下游 Kafka 实例所需的 SASL/PLAIN 或 SASL/SCRAM 认证的密码（可选，若包含特殊字符需进行 URL 编码）。 |
| `sasl-mechanism` | 连接到下游 Kafka 实例所需的 SASL 认证机制。值可以是 `plain`、`scram-sha-256`、`scram-sha-512` 或 `gssapi`。 |
| `sasl-gssapi-auth-type` | gssapi 认证类型。值可以是 `user` 或 `keytab`（可选）。 |
| `sasl-gssapi-kerberos-config-path` | gssapi Kerberos 配置路径（可选）。 |
| `sasl-gssapi-service-name` | gssapi 服务名（可选）。 |
| `sasl-gssapi-user` | gssapi 认证的用户名（可选）。 |
| `sasl-gssapi-password` | gssapi 认证的密码（可选，若包含特殊字符需进行 URL 编码）。 |
| `sasl-gssapi-realm` | gssapi 领域名（可选）。 |
| `sasl-gssapi-disable-pafxfast` | 是否禁用 gssapi 的 PA-FX-FAST（可选）。 |
| `dial-timeout` | 建立与下游 Kafka 连接的超时时间，默认值为 `10s`。 |
| `read-timeout` | 获取下游 Kafka 返回响应的超时时间，默认值为 `10s`。 |
| `write-timeout` | 发送请求到下游 Kafka 的超时时间，默认值为 `10s`。 |
| `avro-decimal-handling-mode` | 仅在 `avro` 协议下有效。决定 Avro 如何处理 DECIMAL 字段。值可以是 `string` 或 `precise`，表示将 DECIMAL 字段映射为字符串或精确浮点数。 |
| `avro-bigint-unsigned-handling-mode` | 仅在 `avro` 协议下有效。决定 Avro 如何处理 BIGINT UNSIGNED 字段。值可以是 `string` 或 `long`，表示将 BIGINT UNSIGNED 字段映射为 64 位有符号数或字符串。 |

### 最佳实践

* 建议你自己创建 Kafka 主题。至少需要设置每个主题能向 Kafka broker 发送的最大数据量，以及下游 Kafka 分区的数量。当你创建 changefeed 时，这两个设置分别对应 `max-message-bytes` 和 `partition-num`。
* 如果你用不存在的主题创建 changefeed，TiCDC 会尝试使用 `partition-num` 和 `replication-factor` 参数自动创建主题。建议你显式指定这些参数。
* 在大多数情况下，建议使用 `canal-json` 协议。

> **Note:**
>
> 当 `protocol` 为 `open-protocol` 时，TiCDC 会将多个事件编码到一条 Kafka 消息中，避免生成超过 `max-message-bytes` 指定长度的消息。
> 如果单个行变更事件的编码结果超过 `max-message-bytes`，changefeed 会报错并打印日志。

### TiCDC 使用 Kafka 的认证和授权

以下是使用 Kafka SASL 认证的示例：

- SASL/PLAIN

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-user=alice-user&sasl-password=alice-secret&sasl-mechanism=plain"
  ```

- SASL/SCRAM

  SCRAM-SHA-256 和 SCRAM-SHA-512 类似于 PLAIN 方法，只需将 `sasl-mechanism` 指定为对应的认证方式。

- SASL/GSSAPI

  SASL/GSSAPI `user` 认证：

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=user&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-password=alice-secret&sasl-gssapi-realm=example.com"
  ```

  `sasl-gssapi-user` 和 `sasl-gssapi-realm` 的值与在 Kerberos 中指定的 [principle](https://web.mit.edu/kerberos/krb5-1.5/krb5-1.5.4/doc/krb5-user/What-is-a-Kerberos-Principal_003f.html) 相关。例如，如果 principle 设置为 `alice/for-kafka@example.com`，那么 `sasl-gssapi-user` 和 `sasl-gssapi-realm` 分别为 `alice/for-kafka` 和 `example.com`。

  SASL/GSSAPI `keytab` 认证：

  ```shell
  --sink-uri="kafka://127.0.0.1:9092/topic-name?kafka-version=2.4.0&sasl-mechanism=gssapi&sasl-gssapi-auth-type=keytab&sasl-gssapi-kerberos-config-path=/etc/krb5.conf&sasl-gssapi-service-name=kafka&sasl-gssapi-user=alice/for-kafka&sasl-gssapi-keytab-path=/var/lib/secret/alice.key&sasl-gssapi-realm=example.com"
  ```

  更多关于 SASL/GSSAPI 认证方式的信息，请参见 [配置 GSSAPI](https://docs.confluent.io/platform/current/kafka/authentication_sasl/authentication_sasl_gssapi.html)。

- TLS/SSL 加密

  如果 Kafka broker 启用了 TLS/SSL 加密，需要在 `--sink-uri` 中添加 `-enable-tls=true` 参数。如果要使用自签名证书，还需要在 `--sink-uri` 中指定 `ca`、`cert` 和 `key`。

- ACL 授权

  TiCDC 正常运行所需的最低权限集如下：

  - Topic [资源类型](https://docs.confluent.io/platform/current/kafka/authorization.html#resources) 的 `Create`、`Write` 和 `Describe` 权限。
  - Cluster 资源类型的 `DescribeConfig` 权限。

  每个权限的使用场景如下：

    | 资源类型 | 操作类型 | 场景 |
    | :-------- | :-------- | :-------- |
    | Cluster | `DescribeConfig` | 获取集群元数据（changefeed 运行中） |
    | Topic | `Describe` | 在启动时尝试创建主题 |
    | Topic | `Create` | 在启动时尝试创建主题 |
    | Topic | `Write` | 发送数据到主题 |

  在创建或启动 changefeed 时，如果 Kafka 主题已存在，可以禁用 `Describe` 和 `Create` 权限。

### 将 TiCDC 集成到 Kafka Connect（Confluent Platform）

若要使用 Confluent 提供的 [数据连接器](https://docs.confluent.io/current/connect/managing/connectors.html) 将数据流式传输到关系型或非关系型数据库，需要使用 [`avro` 协议](/ticdc/ticdc-avro-protocol.md)，并在 `schema-registry` 中提供 [Confluent Schema Registry](https://www.confluent.io/product/confluent-platform/data-compatibility/) 的 URL。

示例配置：

```shell
--sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --schema-registry="http://127.0.0.1:8081" --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

详细的集成指南请参见 [TiDB 与 Confluent Platform 集成快速入门指南](/ticdc/integrate-confluent-using-ticdc.md)。

### 将 TiCDC 与 AWS Glue Schema Registry 集成

从 v7.4.0 起，TiCDC 支持在用户选择 [`Avro` 协议](/ticdc/ticdc-avro-protocol.md) 进行数据复制时，将 Schema Registry 设置为 [AWS Glue Schema Registry](https://docs.aws.amazon.com/glue/latest/dg/schema-registry.html)。配置示例如下：

```shell
./cdc cli changefeed create --server=127.0.0.1:8300 --changefeed-id="kafka-glue-test" --sink-uri="kafka://127.0.0.1:9092/topic-name?&protocol=avro&replication-factor=3" --config changefeed_glue.toml
```

```toml
[sink]
[sink.kafka-config.glue-schema-registry-config]
region="us-west-1"  
registry-name="ticdc-test"
access-key="xxxx"
secret-access-key="xxxx"
token="xxxx"
```

上述配置中，`region` 和 `registry-name` 为必填字段，`access-key`、`secret-access-key` 和 `token` 为可选字段。最佳实践是将 AWS 凭证设置为环境变量或存储在 `~/.aws/credentials` 文件中，而不是在 changefeed 配置文件中设置。

更多信息请参见 [AWS SDK for Go V2 官方文档](https://aws.github.io/aws-sdk-go-v2/docs/configuring-sdk/#specifying-credentials)。

## 自定义 Kafka Sink 的 Topic 和 Partition 分发规则

### Matcher 规则

以下是 `dispatchers` 配置的示例：

```toml
[sink]
dispatchers = [
  {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
  {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
  {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
  {matcher = ['test6.*'], partition = "ts"}
]
```

- 匹配规则的表，将根据对应的主题表达式指定的策略进行分发。例如，`test3.aa` 表将根据 "Topic expression 2" 进行分发；`test5.aa` 表将根据 "Topic expression 3" 进行分发。
- 一个表如果匹配多个 matcher 规则，将根据第一个匹配的主题表达式进行分发。例如，`test1.aa` 表将根据 "Topic expression 1" 进行分发。
- 不匹配任何 matcher 规则的表，其对应的数据变更事件会发送到 `--sink-uri` 中指定的默认主题。例如，`test10.aa` 表会发送到默认主题。
- 匹配规则但未指定主题分发器的表，其对应的数据变更也会发送到 `--sink-uri` 中的默认主题。例如，`test6.aa` 表会发送到默认主题。

### 主题分发器

你可以使用 `topic = "xxx"` 来指定主题分发器，并用主题表达式实现灵活的主题分发策略。建议主题总数少于 1000 个。

主题表达式的格式为 `[prefix]{schema}[middle][{table}][suffix]`。

- `prefix`: 可选。表示主题名称的前缀。
- `{schema}`: 必填。用于匹配 schema 名称。从 v7.1.4 起，此参数为可选。
- `middle`: 可选。表示 schema 名称与 table 名称之间的分隔符。
- `{table}`: 可选。用于匹配 table 名称。
- `suffix`: 可选。表示主题名称的后缀。

`prefix`、`middle` 和 `suffix` 只能包含以下字符：`a-z`、`A-Z`、`0-9`、`.`、`_` 和 `-`。`{schema}` 和 `{table}` 均为小写。像 `{Schema}` 和 `{TABLE}` 这样的占位符无效。

示例：

- `matcher = ['test1.table1', 'test2.table2'], topic = "hello_{schema}_{table}"`
    - `test1.table1` 对应的变更事件会发送到主题 `hello_test1_table1`。
    - `test2.table2` 对应的变更事件会发送到主题 `hello_test2_table2`。
- `matcher = ['test3.*', 'test4.*'], topic = "hello_{schema}_world"`
    - `test3` 中所有表对应的变更事件会发送到主题 `hello_test3_world`。
    - `test4` 中所有表对应的变更事件会发送到主题 `hello_test4_world`。
- `matcher = ['test5.*', 'test6.*'], topic = "hard_code_topic_name"`
    - `test5` 和 `test6` 中所有表对应的变更事件会发送到主题 `hard_code_topic_name`。可以直接指定主题名。
- `matcher = ['*.*'], topic = "{schema}_{table}"`
    - TiCDC 监听的所有表会根据 "schema_table" 规则分发到不同的主题。例如，`test.account` 表的变更日志会分发到主题 `test_account`。

### 分发 DDL 事件

#### Schema 级别的 DDL

不涉及具体表的 DDL（如 `create database` 和 `drop database`）称为 schema 级别的 DDL，相关事件会发送到 `--sink-uri` 中指定的默认主题。

#### 表级别的 DDL

涉及具体表的 DDL（如 `alter table` 和 `create table`）称为表级别的 DDL，相关事件会根据调度器配置发送到对应的主题。

例如，调度器配置为 `matcher = ['test.*'], topic = {schema}_{table}` 时：

- 如果 DDL 事件只涉及单个表，DDL 事件会原样发送到对应的主题。例如，`drop table test.table1` 会发送到主题 `test_table1`。
- 如果涉及多个表（`rename table` / `drop table` / `drop view` 可能涉及多个表），DDL 事件会拆分成多个事件，分别发送到对应的主题。例如，`rename table test.table1 to test.table10, test.table2 to test.table20`，会将 `rename table test.table1 to test.table10` 发送到 `test_table1`，`rename table test.table2 to test.table20` 发送到 `test.table2`。

### 分区分发器

你可以使用 `partition = "xxx"` 来指定分区分发器。支持五种分发器：`default`、`index-value`、`columns`、`table` 和 `ts`。规则如下：

- `default`: 默认使用 `table` 分发规则。通过 schema 名和 table 名计算分区编号，确保来自同一表的数据在同一分区，保证顺序。此规则限制了发送吞吐量，增加消费者不会提升消费速度。
- `index-value`: 使用主键、唯一索引或显式指定的 `index` 计算分区编号，将表数据分布到多个分区。单表数据会在多个分区中，且每个分区内有序。可以通过增加消费者提升速度。
- `columns`: 使用显式指定的列值计算分区编号，将表数据分布到多个分区。单表数据会在多个分区中，且每个分区内有序。可以通过增加消费者提升速度。
- `table`: 使用 schema 名和 table 名计算分区编号。
- `ts`: 使用行变更的 `commitTs` 计算分区编号，将表数据分布到多个分区。单表数据会在多个分区中，且每个分区内有序。可以通过增加消费者提升速度，但可能导致同一数据项的多次变更被发送到不同分区，消费者进度不同，可能引发数据不一致。因此，消费者在消费前需要按 `commitTs` 排序。

以下是 `dispatchers` 配置示例：

```toml
[sink]
dispatchers = [
    {matcher = ['test.*'], partition = "index-value"},
    {matcher = ['test1.*'], partition = "index-value", index = "index1"},
    {matcher = ['test2.*'], partition = "columns", columns = ["id", "a"]},
    {matcher = ['test3.*'], partition = "table"},
]
```

- `test` 数据库中的表使用 `index-value` 分发器，按主键或唯一索引值计算分区编号。若存在主键，则用主键；否则用最短的唯一索引。
- `test1` 数据库中的表使用 `index-value` 分发器，按名为 `index1` 的索引的所有列值计算分区编号。若索引不存在，则报错。注意，`index` 指定的索引必须是唯一索引。
- `test2` 数据库中的表使用 `columns` 分发器，按 `id` 和 `a` 列的值计算分区编号。若任一列不存在，则报错。
- `test3` 数据库中的表使用 `table` 分发器。
- `test4` 数据库中的表使用 `default` 分发器，即 `table`，因为不匹配前述规则。

如果一个表匹配多个分发规则，优先使用第一个匹配的规则。

> **Note:**
>
> 自 v6.1.0 起，为了明确配置的含义，用于指定分区分发器的配置项由 `dispatcher` 改为 `partition`，且 `partition` 为 `dispatcher` 的别名。例如，以下两个规则完全等价：
>
> ```
> [sink]
> dispatchers = [
>    {matcher = ['*.*'], dispatcher = "index-value"},
>    {matcher = ['*.*'], partition = "index-value"},
> ]
> ```
>
> 但 `dispatcher` 和 `partition` 不能同时出现在同一规则中。例如，以下规则无效：
>
> ```
> {matcher = ['*.*'], dispatcher = "index-value", partition = "table"},
> ```

## 列选择器

列选择器功能支持从事件中选择列，只发送与这些列相关的数据变更到下游。

以下是 `column-selectors` 配置示例：

```toml
[sink]
column-selectors = [
    {matcher = ['test.t1'], columns = ['a', 'b']},
    {matcher = ['test.*'], columns = ["*", "!b"]},
    {matcher = ['test1.t1'], columns = ['column*', '!column1']},
    {matcher = ['test3.t'], columns = ["column?", "!column1"]},
]
```

- 表 `test.t1` 只会发送列 `a` 和 `b`。
- `test` 数据库中的所有表（不包括 `t1`）会发送所有列，除了 `b`。
- 表 `test1.t1` 会发送所有以 `column` 开头的列，排除 `column1`。
- 表 `test3.t` 会发送所有长度为 7 个字符、以 `column` 开头的列，排除 `column1`。
- 不匹配任何规则的表，全部列都会被发送。

> **Note:**
>
> 经过 `column-selectors` 规则过滤后，表中的数据必须有主键或唯一键，才能进行复制。否则，创建或运行时 changefeed 会报错。

## 将单个大表的负载扩展到多个 TiCDC 节点

此功能将单个大表的数据复制范围根据数据量和每分钟变更行数拆分成多个范围，使每个范围的数据量和变更行数大致相同。此功能将这些范围分配给多个 TiCDC 节点进行复制，从而多个 TiCDC 节点可以同时复制一个大表。此功能可以解决以下两个问题：

- 单个 TiCDC 节点无法及时复制完大表。
- TiCDC 节点消耗的资源（如 CPU 和内存）分布不均。

> **Warning:**
>
> TiCDC v7.0.0 仅支持在 Kafka changefeed 上扩展大表的负载。

示例配置：

```toml
[scheduler]
# 默认值为 "false"。你可以设置为 "true" 来启用此功能。
enable-table-across-nodes = true
# 启用此功能后，仅对 region 数量大于 `region-threshold` 的表生效。
region-threshold = 100000
# 启用此功能后，仅对每分钟变更行数大于 `write-key-threshold` 的表生效。
# 注意：
# * `write-key-threshold` 的默认值为 0，意味着默认不根据变更行数拆分复制范围。
# * 你可以根据集群负载调整此参数。例如，设置为 30000，表示当表每分钟变更行数超过 30000 时，拆分复制范围。
# * 当同时配置 `region-threshold` 和 `write-key-threshold` 时：
#   TiCDC 会先检查变更行数是否大于 `write-key-threshold`。
#   若不满足，再检查 region 数量是否大于 `region-threshold`。
write-key-threshold = 30000
```

你可以通过以下 SQL 查询表的 region 数量：

```sql
SELECT COUNT(*) FROM INFORMATION_SCHEMA.TIKV_REGION_STATUS WHERE DB_NAME="database1" AND TABLE_NAME="table1" AND IS_INDEX=0;
```

## 处理超出 Kafka 主题限制的消息

Kafka 主题对消息大小有限制，此限制由 [`max.message.bytes`](https://kafka.apache.org/documentation/#topicconfigs_max.message.bytes) 参数控制。如果 TiCDC Kafka sink 发送的数据超过此限制，changefeed 会报错，无法继续复制数据。为解决此问题，TiCDC 增加了 `large-message-handle-option` 配置，并提供以下方案。

目前，此功能支持两种编码协议：Canal-JSON 和 Open Protocol。当使用 Canal-JSON 协议时，必须在 `sink-uri` 中指定 `enable-tidb-extension=true`。

### TiCDC 数据压缩

从 v7.4.0 起，TiCDC Kafka sink 支持在编码后立即压缩数据，并将压缩后的数据大小与消息大小限制进行比较。此功能能有效减少超出大小限制的消息发生。

示例配置如下：

```toml
[sink.kafka-config.large-message-handle]
# 此配置在 v7.4.0 中引入。
# 默认为 "none"，表示禁用压缩功能。
# 可能的值为 "none"、"lz4" 和 "snappy"。默认值为 "none"。
large-message-handle-compression = "none"
```

启用 `large-message-handle-compression` 后，接收的消息会使用指定的压缩协议编码，消费者端需要使用相应的压缩协议解码数据。

此功能不同于 Kafka 生产者的压缩功能：

* `large-message-handle-compression` 指定的压缩算法会压缩单条 Kafka 消息，压缩在与消息大小限制比较之前进行。
* 你也可以在 [`sink-uri`](#configure-sink-uri-for-kafka) 中通过 `compression` 参数配置压缩算法，此压缩算法应用于整个数据请求（包含多条 Kafka 消息）。

如果设置了 `large-message-handle-compression`，TiCDC 在接收消息时会先与消息大小限制比较，超出限制的消息会被压缩。如果同时在 [`sink-uri`](#configure-sink-uri-for-kafka) 中设置了 `compression`，则会在 sink 层再次根据 `sink-uri` 设置压缩整个请求。

两种压缩方法的压缩比计算公式为：`compression ratio = size before compression / size after compression * 100`。

### 仅发送 handle keys

从 v7.3.0 起，TiCDC Kafka sink 支持在消息超出限制时，仅发送 handle keys，从而大幅减小消息体积，避免因消息超出 Kafka 主题限制导致的 changefeed 失败。

Handle Key 指：

* 若待复制表有主键，则主键为 handle key。
* 若无主键但有 NOT NULL 唯一索引，则该唯一索引为 handle key。

示例配置如下：

```toml
[sink.kafka-config.large-message-handle]
# large-message-handle-option 在 v7.3.0 中引入。
# 默认为 "none"。当消息超出限制时，changefeed 会失败。
# 设置为 "handle-key-only" 时，超出限制时只会在数据字段中发送 handle key，若仍超出限制，changefeed 也会失败。
large-message-handle-option = "claim-check"
```

### 仅消费 handle keys 的消息

只含 handle keys 的消息格式如下：

```json
{
    "id": 0,
    "database": "test",
    "table": "tp_int",
    "pkNames": [
        "id"
    ],
    "isDdl": false,
    "type": "INSERT",
    "es": 1639633141221,
    "ts": 1639633142960,
    "sql": "",
    "sqlType": {
        "id": 4
    },
    "mysqlType": {
        "id": "int"
    },
    "data": [
        {
          "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB 扩展字段
        "commitTs": 429918007904436226,  // TiDB TSO 时间戳
        "onlyHandleKey": true
    }
}
```

当 Kafka 消费者收到此消息时，会先检查 `onlyHandleKey` 字段。若存在且为 `true`，表示消息只包含完整数据的 handle key。此时若需获取完整数据，需要向上游 TiDB 查询，并使用 [`tidb_snapshot` 读取历史数据](/read-historical-data.md)。

> **Warning:**
>
> 当 Kafka 消费者处理数据并查询 TiDB 时，数据可能已被 GC 删除。你需要将 TiDB 集群的 [GC 生命周期](/system-variables.md#tidb_gc_life_time-new-in-v50) 设置为更大值，以避免此问题。

### 将大消息发送到外部存储

从 v7.4.0 起，TiCDC Kafka sink 支持在消息超出限制时，将大消息发送到外部存储，同时向 Kafka 发送包含大消息地址的消息，避免因消息超出 Kafka 主题限制导致的 changefeed 失败。

示例配置如下：

```toml
[sink.kafka-config.large-message-handle]
# large-message-handle-option 在 v7.3.0 中引入。
# 默认为 "none"。当消息超出限制时，changefeed 会失败。
# 设置为 "handle-key-only" 时，超出限制时只会在数据字段中发送 handle key，若仍超出限制，changefeed 也会失败。
# 设置为 "claim-check" 时，超出限制的消息会被存储到外部存储中。
large-message-handle-option = "claim-check"
claim-check-storage-uri = "s3://claim-check-bucket"
```

当 `large-message-handle-option` 设置为 `"claim-check"` 时，`claim-check-storage-uri` 必须指向有效的外部存储地址，否则创建 changefeed 会失败。

> **Tip**
>
> 有关 TiCDC 中 Amazon S3、GCS 和 Azure Blob 存储的 URI 格式的更多信息，请参见 [外部存储服务的 URI 格式](/external-storage-uri.md)。

TiCDC 不会清理外部存储中的消息，数据消费者需要自行管理外部存储。

### 从外部存储中消费大消息

Kafka 消费者收到的消息包含外部存储中大消息的地址，消息格式如下：

```json
{
    "id": 0,
    "database": "test",
    "table": "tp_int",
    "pkNames": [
        "id"
    ],
    "isDdl": false,
    "type": "INSERT",
    "es": 1639633141221,
    "ts": 1639633142960,
    "sql": "",
    "sqlType": {
        "id": 4
    },
    "mysqlType": {
        "id": "int"
    },
    "data": [
        {
          "id": "2"
        }
    ],
    "old": null,
    "_tidb": {     // TiDB 扩展字段
        "commitTs": 429918007904436226,  // TiDB TSO 时间戳
        "claimCheckLocation": "s3:/claim-check-bucket/${uuid}.json"
    }
}
```

如果消息中包含 `claimCheckLocation` 字段，Kafka 消费者会根据该字段提供的地址，从 JSON 格式的外部存储中读取大消息数据。消息格式如下：

```json
{
  key: "xxx",
  value: "xxx",
}
```

`key` 和 `value` 字段包含编码后的大消息，应该在 Kafka 消息的对应字段中。消费者可以解析这两部分数据，恢复大消息的内容。