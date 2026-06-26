---
title: Kafka - Credentials (Beta)
summary: Create a "Kafka - Credentials" data source to store Kafka connection information for reuse in Kafka Consumer integration tasks.
---

# Kafka - Credentials (Beta)

This page describes how to create a `Kafka - Credentials` data source. This data source stores the broker addresses, authentication method, and connection credentials required to access a Kafka cluster. You can reuse these settings across multiple Kafka Consumer integration tasks.

`Kafka - Credentials` only stores Kafka connection information. It does not consume messages by itself. The actual process of reading Kafka topic messages and writing them to internal object storage is performed by a [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md).

## Use Cases

- Centrally manage Kafka broker addresses and authentication settings
- Reuse the same Kafka connection settings across multiple Kafka Consumer tasks
- Update the Kafka addresses, authentication method, or account information in one place when referenced by multiple tasks

## Create Kafka - Credentials

1. Navigate to **Data** > **Data Sources**, then click **Create Data Source**.
2. Select **Kafka - Credentials** as the service type, then fill in the connection details:

    | Field | Required | Description |
    |-------|----------|-------------|
    | **Name** | Yes | A descriptive name for the data source |
    | **Brokers** | Yes | Kafka broker address list. Separate multiple addresses with commas, for example `broker-1:9092,broker-2:9093,broker-3:9092` |
    | **Authentication** | Yes | Kafka authentication method. Supported options are **None** and **SASL/PLAIN** |
    | **TLS encryption** | No | Whether to enable TLS encryption |
    | **Username** | Required if applicable | Kafka username. Required when **SASL/PLAIN** is selected |
    | **Password** | Required if applicable | Kafka password. Required when **SASL/PLAIN** is selected |

3. Click **Test Connectivity** to validate the connection. If the test succeeds, click **OK** to save the data source.

## Configuration Recommendations

- Create a dedicated Kafka user for the platform instead of sharing an application account.
- Enable **TLS encryption** if your Kafka cluster requires encrypted connections.
- If you select **SASL/PLAIN**, make sure the Kafka user is allowed to read the topics that will be consumed by downstream tasks.
- Run **Test Connectivity** before saving the data source to verify the broker addresses, network access, and authentication settings.

## Next Steps

After creating the data source, you can use it to create a [Kafka Consumer Integration Task (Beta)](/tidb-cloud-lake/guides/integrate-with-kafka.md).
