---
title: TiCDC Data Integrity Validation
summary: Introduce the implementation principle and usage of the TiCDC data integrity validation feature.
---

# TiCDC Data Integrity Validation

Starting from v7.1.0, TiCDC introduces the data integrity validation feature, which uses a checksum algorithm to validate the integrity of single-row data. This feature helps verify whether any error occurs in the process of writing data from TiDB, synchronizing it through TiCDC, and then writing it to a Kafka cluster. The data integrity validation feature only supports changefeeds that use Kafka as the downstream and currently supports the Avro protocol.

## Implementation principles

After you enable the checksum integrity validation feature for single-row data, TiDB uses the CRC32 algorithm to calculate the checksum of a row and writes it to TiKV along with the data. TiCDC reads the data from TiKV and recalculates the checksum using the same algorithm. If the two checksums are equal, it indicates that the data is accurate during the transmission from TiDB to TiCDC.

TiCDC then encodes the data into a specific format and sends it to Kafka. After the Kafka Consumer reads data, it calculates a new checksum using the same algorithm as TiDB. If the new checksum is equal to the checksum in the data, it indicates that the data is accurate during the transmission from TiCDC to the Kafka Consumer.

## Enable the feature

TiCDC disables data integrity validation by default. To enable it, perform the following steps:

1. Enable the checksum integrity validation feature for single-row data in the upstream TiDB cluster by setting the [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) system variable:

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = ON;
    ```

    This configuration only takes effect for newly created sessions, so you need to reconnect to TiDB.

2. In the configuration file specified by the `--config` parameter when creating a changefeed, add the following configurations:

    ```toml
    [integrity]
    integrity-check-level = "correctness"
    corruption-handle-level = "warn"
    ```

3. When using Avro as the data encoding format, you need to set [`enable-tidb-extension=true`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka), [`avro-decimal-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka), and [`avro-bigint-unsigned-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka) in the [`sink-uri`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka). The following is an example:

    ```shell
    cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
    ```

    With the preceding configuration, each message written to Kafka by the Changefeed will include the corresponding data's checksum. You can verify data consistency based on these checksum values.

## Disable the feature

TiCDC disables data integrity validation by default. To disable this feature after enabling it, perform the following steps:

1. Follow the `Pause Task -> Modify Configuration -> Resume Task` process described in [Update task configuration](/ticdc/ticdc-manage-changefeed.md#update-task-configuration) and remove all `[integrity]` configurations in the configuration file specified by the `--config` parameter of the Changefeed.

2. Execute the following SQL statement in the upstream TiDB to disable the checksum integrity validation feature ([`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)):

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = OFF;
    ```

    The preceding configuration only takes effect for newly created sessions. After all clients writing to TiDB have reconnected, the messages written by Changefeed to Kafka will no longer include the checksum for the corresponding data.
