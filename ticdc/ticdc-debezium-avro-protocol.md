# TiCDC Debezium Avro Protocol

TiCDC Debezium Avro protocol combines Debezium-style change event semantics with Confluent Avro wire format.

In this protocol, TiCDC still produces Debezium envelope fields such as `before`, `after`, `source`, `op`, and `ts_ms`, but message bytes are encoded in Avro binary and schema ids are managed by Schema Registry.

Compared with `protocol=debezium`, `protocol=debezium-avro` is better suited for downstream systems that already use Avro deserializers and Schema Registry.

## Use Debezium Avro

When you use Kafka as the downstream sink, specify `protocol=debezium-avro` in `sink-uri`, and provide the Schema Registry endpoint.

The configuration example is as follows:

```shell
cdc cli changefeed create \
  --server=http://127.0.0.1:8300 \
  --changefeed-id="kafka-debezium-avro" \
  --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=debezium-avro&avro-decimal-handling-mode=precise&avro-bigint-unsigned-handling-mode=string" \
  --schema-registry=http://127.0.0.1:8081 \
  --config changefeed_config.toml
```

The value of `--schema-registry` supports the `https` protocol and `username:password` authentication. The username and password must be URL-encoded. For example, `--schema-registry=https://username:password@schema-registry-uri.com`.

> **Note:**
>
> Debezium Avro uses Schema Registry topic-name subject behavior. One Kafka topic should contain data for only one table. You need to configure topic dispatchers to route each table to an independent topic.

```toml
[sink]
dispatchers = [
  {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

## Definition of the data format

TiCDC converts a DML event into a Kafka event. The key and value are encoded as Debezium-model payloads over Avro wire format.

### Wire format

Each Kafka message is encoded as:

```text
[magic byte][schema id][avro binary payload]
```

### Key data format

The key contains only primary key columns or unique index columns.

The following JSON is the Debezium Connect schema model used before Avro binary encoding.

```json
{
  "schema": {
    "type": "struct",
    "optional": false,
    "name": "{{ClusterID}}.{{SchemaName}}.{{TableName}}Key",
    "fields": [
      {
        "field": "id",
        "type": "int64",
        "optional": false
      }
    ]
  },
  "payload": {
    "id": 1
  }
}
```

#### Avro record naming (key)

When TiCDC converts this key schema to Avro and registers it in Schema Registry:

- `connect.name` keeps the full logical name: `{{ClusterID}}.{{SchemaName}}.{{TableName}}Key`
- Avro `name` becomes: `{{TableName}}Key`
- Avro `namespace` becomes: `{{ClusterID}}.{{SchemaName}}`

All parts are sanitized to Avro-compatible identifiers.

### Value data format

The value is a Debezium envelope and includes `before`, `after`, `source`, `op`, and `ts_ms`.

The following JSON is the Debezium Connect schema model used before Avro binary encoding.

```json
{
  "schema": {
    "type": "struct",
    "optional": false,
    "name": "{{ClusterID}}.{{SchemaName}}.{{TableName}}Envelope",
    "version": 1,
    "fields": [
      {
        "field": "before",
        "type": "struct",
        "optional": true,
        "name": "{{ClusterID}}.{{SchemaName}}.{{TableName}}Value",
        "fields": [
          {{RowFields}}
        ]
      },
      {
        "field": "after",
        "type": "struct",
        "optional": true,
        "name": "{{ClusterID}}.{{SchemaName}}.{{TableName}}Value",
        "fields": [
          {{RowFields}}
        ]
      },
      {
        "field": "source",
        "type": "struct",
        "optional": false,
        "name": "{{ClusterID}}.{{SchemaName}}.Source",
        "fields": [
          ...
        ]
      },
      {
        "field": "op",
        "type": "string",
        "optional": false
      },
      {
        "field": "ts_ms",
        "type": "int64",
        "optional": false
      }
    ]
  },
  "payload": {
    "source": {
      "version": "2.4.0.Final",
      "connector": "TiCDC",
      "name": "default",
      "ts_ms": 1707103832263,
      "snapshot": null,
      "db": "test",
      "table": "t2",
      "server_id": 0,
      "file": "",
      "pos": 0,
      "row": 0,
      "gtid": null,
      "query": null,
      "thread": null,
      "commit_ts": 447507027004751877,
      "cluster_id": "default"
    },
    "ts_ms": 1707103832957,
    "op": "c",
    "before": null,
    "after": {
      "{{ClusterID}}.{{SchemaName}}.{{TableName}}": {
        "id": 1,
        "name": "Alice"
      }
    }
  }
}
```

#### Avro record naming (value)

For value-related records, TiCDC applies the same conversion rule:

- Envelope `connect.name`: `{{ClusterID}}.{{SchemaName}}.{{TableName}}Envelope`
- Envelope Avro `name`: `{{TableName}}Envelope`
- Envelope Avro `namespace`: `{{ClusterID}}.{{SchemaName}}`

Nested row records follow the same pattern (for example, `{{TableName}}` under the same namespace).

Debezium Avro encodes DML event types as follows:

- For insert events, `op = "c"`, `before = null`, and `after` contains new row data.
- For update events, `op = "u"`, and `after` contains updated row data. If old value output is enabled, `before` is included.
- For delete events, `op = "d"`, `after = null`, and `before` contains deleted row data.

## Configuration

The following parameters affect Debezium Avro:

| Parameter                            | Description                                                                                                           | Default   |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------- | --------- |
| `protocol=debezium-avro`             | Enables the Debezium Avro protocol                                                                                    | N/A       |
| `schema-registry`                    | Confluent Schema Registry URL                                                                                         | Required  |
| `enable-tidb-extension`              | Adds TiDB-specific metadata such as `tidb_type`, and enables internal watermark / DDL encoding paths when used with `avro-enable-watermark` | `false`   |
| `avro-decimal-handling-mode`         | Decimal handling mode, `precise` or `string`                                                                          | `precise` |
| `avro-bigint-unsigned-handling-mode` | Unsigned BIGINT handling mode, `long` or `string`                                                                     | `long`    |
| `avro-enable-watermark`              | Enables watermark / DDL messages for internal testing                                                                 | `false`   |

The `debezium-output-old-value` setting is controlled by sink configuration and decides whether update events include old row values in `before`.

`enable-tidb-extension` is optional in normal Debezium Avro scenarios. Base Debezium envelope fields are available without it.

### Constraints

- Debezium Avro requires a Schema Registry endpoint.
- A Kafka topic should carry one table schema.
- `force-replicate` must be disabled when using Avro or Debezium Avro.

## DDL events and schema changes

Debezium Avro does not rely on downstream DDL event consumption. When table schema changes, TiCDC generates and registers new schemas through Schema Registry during DML processing.

If schema compatibility checks fail in Schema Registry, changefeed enters an error state.

For operational details, read:

- [TiCDC Avro Protocol - DDL events and schema changes](/ticdc/ticdc-avro-protocol.md#ddl-events-and-schema-changes)

## Data type mapping

Debezium Avro follows Debezium-style type semantics, with TiCDC-specific behavior controlled by Avro options such as decimal and unsigned bigint handling.

For exact type mapping details and differences, see:

- [TiCDC Debezium Protocol - Data type mapping](/ticdc/ticdc-debezium.md#data-type-mapping)

## Consumer implementation

Use Confluent-compatible Avro deserializers and Schema Registry APIs to decode message payloads.

Reference:

- [TiCDC Avro Protocol - Consumer implementation](/ticdc/ticdc-avro-protocol.md#consumer-implementation)

## Compatibility

Schema evolution compatibility is determined by Schema Registry policy. Incompatible schema changes can stop the changefeed.

Reference:

- [TiCDC Avro Protocol - Compatibility](/ticdc/ticdc-avro-protocol.md#compatibility)