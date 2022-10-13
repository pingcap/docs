---
title: Connect Airbyte with TiDB
summary: Learn how to use Airbyte TiDB connector.
---

# Connect Airbyte with TiDB

[Airbyte](https://airbyte.com/) is an open-source data integration engine that helps you consolidate your data in your data warehouses, lakes, and databases. This document shows how to connect Airbyte to TiDB as a source or a destination.

## Deploy Airbyte

Airbyte supports local deployment with only a few easy steps.

1. Install Docker on your workspace.
2. Clone the Airbyte source code.

    ```
    $ git clone https://github.com/airbytehq/airbyte.git
    $ cd airbyte
    ```
   
3. Run the Docker images by docker-compose. 
   
    ```
    $ docker-compose up
    ```

Once see an Airbyte banner, the UI is ready to go at [http://localhost:8000](http://localhost:8000).

![img](/media/tidb-cloud/integration-airbyte-ready.jpg)

## Set TiDB Connector

> For TiDB as the source, here is a step-by-step tutorial about [Using Airbyte to Migrate Data from TiDB Cloud to Snowflake](https://www.pingcap.com/blog/using-airbyte-to-migrate-data-from-tidb-cloud-to-snowflake/).

Conveniently, the steps are the same for setting TiDB as source or as destination。

1. Click **Sources**(or **Destinations**) in the sidebar and choose TiDB type to create a new TiDB connector.
2. Fill in the parameters, such as host, port, database, username, password, and so on.
   
    > **Description of fields**
    > - Host: The host domain of the TiDB
    > - Port: The port of the database
    > - Database: The database that you want to sync the data
    > - Username: The username to access the database
    > - Password: The password of the username

3. Enable **SSL Connection**, and set TLS protocols to "TLSv1.2" or "TLSv1.3" in **JDBC URL Params**.

    > Note:
    > - TiDB Cloud supports TLS connection, you can choose your TLS protocols in "TLSv1.2" and "TLSv1.3". Such as `enabledTLSProtocols=TLSv1.2`.
    > - If you want to disable TLS connection to TiDB Cloud via JDBC, you need to set useSSL to "false" in JDBC URL Params specifically and close SSL Connection. Such as `useSSL=false`.
    > - TiDB Serverless only supports TLS connections.

4. Click **Set up source**(or **destinations**) to complete creating the connector.

![img](/media/tidb-cloud/integration-airbyte-parameters.jpg)

For more details about TiDB connector, you can see [TiDB Source](https://docs.airbyte.com/integrations/sources/tidb) and [TiDB Destination](https://docs.airbyte.com/integrations/destinations/tidb) in Airbyte document.

## Set Connection

After the source and destination have been set up, build the connection and set the configuration. You can use any combination of source and destination, such as TiDB to Snowflake, CSV file to TiDB, etc.

1. Click **Connections** in the sidebar and click **New Connection**.
2. Select the previously established source and destination.
3. Then go into the **Set up** connection panel and pick a name for this connection, such as "source-name <> destination-name".
4. Set **Replication frequency** to "Every 24 hours" which means transforming data once a day.
5. Set **Destination Namespace** to "Custom format" and set **Namespace Custom Format** to "test" which makes all data stored in the test database.
6. Choose the **Sync schema** to "Full refresh | Overwrite".

    > **Tips**
    >   
    > The TiDB connector supports both Incremental and Full Refresh syncs. For Incremental mode, the Airbyte would only read records added to the source since the last sync job. (The first sync using Incremental is equivalent to a Full Refresh). For Full Refresh, the Airbyte would read all records in source and trans to destination in every sync task. The sync mode can be set for every table which is named Namespace in Airbyte individually.

7. Set **Normalization & Transformation** to "Normalized tabular data". This will use default normalization mode, or you can set the dbt file for your job.
8. Click **Set up** connection.
9. Start the sync task and wait a few minutes for the mission completed.

![img](/media/tidb-cloud/integration-airbyte-connection.jpg)

## Limitations

- TiDB connector does not support Change Data Capture(CDC) feature.
- TiDB destination transforms `timestamp` type to `varchar` type in default normalize mode. This is since that Airbyte converts the timestamp type to string during transmission, and TiDB does not support `cast ('2020-07-28 14:50:15+1:00' as timestamp)`.
- For some huge ETL missions, you should raise the parameters of [transaction restrictions](https://docs.pingcap.com/tidb/dev/dev-guide-transaction-restraints) in TiDB.