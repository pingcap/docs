---
title: TiCDC Data Integrity Validation for Single-Row Data
summary: Introduce the implementation principle and usage of the TiCDC data integrity validation feature.
---

# TiCDC Data Integrity Validation for Single-Row Data

Starting from v7.1.0, TiCDC introduces the data integrity validation feature, which uses a checksum algorithm to validate the integrity of single-row data. This feature helps verify whether any error occurs in the process of writing data from TiDB, replicating it through TiCDC, and then writing it to a Kafka cluster. The data integrity validation feature only supports changefeeds that use Kafka as the downstream and currently supports the Avro protocol.

## Implementation principles

After you enable the checksum integrity validation feature for single-row data, TiDB uses the CRC32 algorithm to calculate the checksum of a row and writes it to TiKV along with the data. TiCDC reads the data from TiKV and recalculates the checksum using the same algorithm. If the two checksums are equal, it indicates that the data is consistent during the transmission from TiDB to TiCDC.

TiCDC then encodes the data into a specific format and sends it to Kafka. After the Kafka Consumer reads data, it calculates a new checksum using the same algorithm as TiDB. If the new checksum is equal to the checksum in the data, it indicates that the data is consistent during the transmission from TiCDC to the Kafka Consumer.

For more information about the algorithm of the checksum, see [Algorithm for checksum calculation](#algorithm-for-checksum-calculation).

## Enable the feature

TiCDC disables data integrity validation by default. To enable it, perform the following steps:

1. Enable the checksum integrity validation feature for single-row data in the upstream TiDB cluster by setting the [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) system variable:

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = ON;
    ```

    This configuration only takes effect for newly created sessions, so you need to reconnect to TiDB.

2. In the [configuration file](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) specified by the `--config` parameter when you create a changefeed, add the following configurations:

    ```toml
    [integrity]
    integrity-check-level = "correctness"
    corruption-handle-level = "warn"
    ```

3. When using Avro as the data encoding format, you need to set [`enable-tidb-extension=true`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) in the [`sink-uri`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka). To prevent numerical precision loss during network transmission, which can cause checksum validation failures, you also need to set [`avro-decimal-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) and [`avro-bigint-unsigned-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka). The following is an example:

    ```shell
    cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-checksum" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
    ```

    With the preceding configuration, each message written to Kafka by the changefeed will include the corresponding data's checksum. You can verify data consistency based on these checksum values.

    > **Note:**
    >
    > For existing changefeeds, if `avro-decimal-handling-mode` and `avro-bigint-unsigned-handling-mode` are not set, enabling the checksum validation feature might cause schema compatibility issues. To resolve this issue, you can modify the compatibility type of the Schema Registry to `NONE`. For more details, see [Schema Registry](https://docs.confluent.io/platform/current/schema-registry/fundamentals/avro.html#no-compatibility-checking).

## Disable the feature

TiCDC disables data integrity validation by default. To disable this feature after enabling it, perform the following steps:

1. Follow the `Pause Task -> Modify Configuration -> Resume Task` process described in [Update task configuration](/ticdc/ticdc-manage-changefeed.md#update-task-configuration) and remove all `[integrity]` configurations in the configuration file specified by the `--config` parameter of the changefeed.

    ```toml
    [integrity]
    integrity-check-level = "none"
    corruption-handle-level = "warn"
    ```

2. Execute the following SQL statement in the upstream TiDB to disable the checksum integrity validation feature ([`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)):

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = OFF;
    ```

    The preceding configuration only takes effect for newly created sessions. After all clients writing to TiDB have reconnected, the messages written by changefeed to Kafka will no longer include the checksum for the corresponding data.

## Algorithm for checksum calculation

The pseudocode for the checksum calculation algorithm is as follows:

```
fn checksum(columns) {
    let result = 0
    for column in sort_by_schema_order(columns) {
        result = crc32.update(result, encode(column))
    }
    return result
}
```

* `columns` should be sorted by column ID. In the Avro schema, fields are already sorted by column ID, so you can directly use the order in `columns`.

* The `encode(column)` function encodes the column value into bytes. Encoding rules vary based on the data type of the column. The specific rules are as follows:

    * TINYINT, SMALLINT, INT, BIGINT, MEDIUMINT, and YEAR types are converted to UINT64 and encoded in little-endian. For example, the number `0x0123456789abcdef` is encoded as `hex'0x0123456789abcdef'`.
    * FLOAT and DOUBLE types are converted to DOUBLE and then encoded as UINT64 in IEEE754 format.
    * BIT, ENUM, and SET types are converted to UINT64.

        * BIT type is converted to UINT64 in binary format.
        * ENUM and SET types are converted to their corresponding INT values in UINT64. For example, if the data value of a `SET('a','b','c')` type column is `'a,c'`, the value is encoded as `0b101`, which is `5`.

    * TIMESTAMP, DATE, DURATION, DATETIME, JSON, and DECIMAL types are converted to STRING and then encoded as bytes.
    * CHAR、VARCHAR、VARSTRING、STRING、TEXT、BLOB（(including TINY, MEDIUM, and LONG) are encoded as bytes.

    * NULL and GEOMETRY types are excluded from the checksum calculation and this function returns empty bytes.

## Golang based Avro message consumption and checksum verification

TiCDC provides a checksum calculation and validation program based on the avro decoder, which you can refer to implement your owner version. The main part is the [NextRowChangedEvent](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L100). It works in the following steps：

1. Assuming the message is received from the kafka, and set as the key and value. Decode the key and value to get the decoded data and schema. The specific process can refer to [`decodeKey`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L395) and [`decodeValue`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L419).
2. Rebuild the data content of the `RowChangedEvent` using the decoded key, value, and schema. For details, see the [`assembleEvent`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L176). It works in the following steps：

    1. The schema has all the `fields`, and traverse each element `field` in `fields` to construct the corresponding column. The `fields` are already sorted by column ID.
    2. Rebuild the MySQL Type of each column using the type information contained in `field`, and identify the Handle Key column through `keyMap`, and then set the corresponding flag.
    3. The value in `valueMap` needs to be converted through [`getColumnValue`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L299), since when value for nullable columns is encoded as map, so we need to get the specific value from the map. If the column is of type `mysql.TypeEnum` or `mysql.TypeSet`, it also needs to be mapped to its numeric representation.
    4. All column data is obtained after traversing all `fields`. For Delete events, the decoded columns are set to `PreColumns`; for Insert and Update events, the decoded columns are set to `Columns`.

The Checksum calculation and verification steps is as follows:

1. Get the expected checksum value by call the [`extractExpectedChecksum`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L281). If the method returns `false`, it means that the event does not need to be checksum verified because the upstream does not send the checksum. This may happen when TiCDC has enabled the checksum but TiDB has not enabled this feature, or the current event occurs before the checksum verification feature is enabled, etc.
2. Calculate the checksum by call the [`calculateChecksum`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L461). It traverses all the columns that have been rebuilt before. Use the [`buildChecksumBytes`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L482) method to encode the value of each column into a byte slice by using the corresponding MySQL Type, and then use the byte slice to update the checksum value.
3. Compare the expected checksum and the calculated checksum by call the [`verifyChecksum`](https://github.com/pingcap/tiflow/blob/eb04aecaf8e61f7f9d67597c2d2ef1f44583dd79/pkg/sink/codec/avro/decoder.go#L444). If they are not equal, the checksum verification fails and the data may be corrupted.

> **Note:**
>
> - After enabling the checksum validation feature, DECIMAL and UNSIGNED BIGINT types data will be converted to string types. Therefore, in the downstream consumer code, you need to convert them back to their corresponding numerical types before calculating checksum values.
> - Delete event only encode the Handle Key column, and the checksum is calculated based on all columns. Therefore, the Delete event does not participate in the checksum validation.
