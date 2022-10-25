---
title: Use Airbyte to Extract, Load and Transform Data
summary: Learn how to use Airbyte TiDB connector.
---

# Use Airbyte to Extract, Load and Transform Data

[Airbyte](https://airbyte.com/) is an open-source data integration engine to build Extract, Load, Transform (ELT) pipelines and consolidate your data in your data warehouses, data lakes, and databases. This document shows how to connect Airbyte to TiDB as a source or a destination.

## Deploy Airbyte

Airbyte supports local deployment with only a few steps.

1. Install [Docker](https://www.docker.com/products/docker-desktop) on your workspace.

2. Clone the Airbyte source code.

    ```shell
    $ git clone https://github.com/airbytehq/airbyte.git
    $ cd airbyte
    ```

3. Run the Docker images by docker-compose.

    ```shell
    $ docker-compose up
    ```

Once you see an Airbyte banner, you can go to [http://localhost:8000](http://localhost:8000) to visit the UI.

![img](/media/tidb-cloud/integration-airbyte-ready.jpg)

## Set the TiDB connector

If you use TiDB as the source, see a step-by-step tutorial about [Using Airbyte to Migrate Data from TiDB Cloud to Snowflake](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/).

Conveniently, the steps are the same for setting TiDB as the source and the destination.

1. Click **Sources** or **Destinations** in the sidebar and choose TiDB type to create a new TiDB connector.

2. Fill in the following parameters.

    - Host: The host domain of TiDB
    - Port: The port of the database
    - Database: The database that you want to sync the data
    - Username: The username to access the database
    - Password: The password of the username

3. Enable **SSL Connection**, and set TLS protocols to **TLSv1.2** or **TLSv1.3** in **JDBC URL Params**.

    > Note:
    >
    > - TiDB Cloud supports TLS connection. You can choose your TLS protocols in **TLSv1.2** and **TLSv1.3**, for example, `enabledTLSProtocols=TLSv1.2`.
    > - If you want to disable TLS connection to TiDB Cloud via JDBC, you need to set useSSL to `false` in JDBC URL Params specifically and close SSL connection, for example, `useSSL=false`.
    > - TiDB Serverless Tier only supports TLS connections.

4. Click **Set up source** or **destinations** to complete creating the connector.

![img](/media/tidb-cloud/integration-airbyte-parameters.jpg)

For more details about the TiDB connector, see [TiDB Source](https://docs.airbyte.com/integrations/sources/tidb) and [TiDB Destination](https://docs.airbyte.com/integrations/destinations/tidb).

## Set up the connection

After setting up the source and destination, you can build and configure the connection. You can use any combination of sources and destinations, such as TiDB to Snowflake, and CSV file to TiDB.

The following steps use TiDB as source and destination. Other connectors may have different parameters.

1. Click **Connections** in the sidebar and then click **New Connection**.
2. Select the previously established source and destination.
3. Go to the **Set up** connection panel and create a name for the connection, such as "${source_name} - ${destination-name}".
4. Set **Replication frequency** to **Every 24 hours** which means the connection replicates data once a day.
5. Set **Destination Namespace** to **Custom format** and set **Namespace Custom Format** to **test** to store all data in the `test` database.
6. Choose the **Sync schema** to **Full refresh | Overwrite**.

    > **Tips**
    >
    > The TiDB connector supports both Incremental and Full Refresh syncs. In Incremental mode, Airbyte only reads records added to the source since the last sync job. The first sync using Incremental mode is equivalent to Full Refresh mode. In Full Refresh mode, Airbyte reads all records in the source and replicates to the destination in every sync task. You can set the sync mode for every table named **Namespace** in Airbyte individually.

7. Set **Normalization & Transformation** to **Normalized tabular data** to use the default normalization mode, or you can set the dbt file for your job.
8. Click **Set up connection**.
9. Start the sync task and wait a few minutes for the mission to finish.

![img](/media/tidb-cloud/integration-airbyte-connection.jpg)

## Limitations

- The TiDB connector does not support the Change Data Capture (CDC) feature.
- TiDB destination converts the `timestamp` type to the `varchar` type in default normalization mode. It happens because Airbyte converts the timestamp type to string during transmission, and TiDB does not support `cast ('2020-07-28 14:50:15+1:00' as timestamp)`.
- For some large ETL missions, you need to increase the parameters of [transaction restrictions](/develop/dev-guide-transaction-restraints.md#large-transaction-restrictions) in TiDB.
