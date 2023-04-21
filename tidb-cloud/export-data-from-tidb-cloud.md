---
title: Export Data from TiDB
summary: This page has instructions for exporting data from your TiDB cluster in TiDB Cloud.
---

# Export Data from TiDB

This page describes how to export data from your cluster in TiDB Cloud.

TiDB does not lock in your data. Sometimes you still want to be able to migrate data from TiDB to other data platforms. Because TiDB is highly compatible with MySQL, any export tool suitable for MySQL can also be used for TiDB.

You can use the tool [Dumpling](/dumpling-overview.md) for data export.

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding `profile` file. You need to modify `.bash_profile` in following command to the path of your `profile` file.

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. Install Dumpling.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install dumpling
    ```

4. Export your data using Dumpling from TiDB.

    You can get the following connection parameters `${tidb_endpoint}`, `${port}`, and `${user}` from the connection string in the [**Connect**](/tidb-cloud/connect-via-standard-connection.md) dialog.

    <SimpleTab>

    <div label="Serverless Tier">

    ```shell
    tiup dumpling -h ${tidb_endpoint} -P 4000 -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql --consistency none
    ```

   > **Note:**
   >
   > To export Serverless Tier cluster data, you must ensure that the Dumpling version is at least v6.5.0. If your Dumpling version is v6.5.0, you also need to set `--ca=${ca_path}` in the command. To find the CA root path on your system, see [TLS Connections to Serverless Tier](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#root-certificate-default-path).

    </div>
    <div label="Dedicated Tier">

    ```shell
    tiup dumpling:v6.5.2 -h ${tidb_endpoint} -P ${port} -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql
    ```

    </div>
    </SimpleTab>

    Options are described as follows:

    - `-h`: The TiDB cluster endpoint.
    - `-P`: The TiDB cluster port.
    - `-u`: The TiDB cluster user.
    - `-p`: The TiDB cluster password.
    - `-F`: The maximum size of a single file.
    - `-o`: The export directory.
    - `--filetype`: The exported file type. The default value is `sql`. You can choose from `sql` and `csv`.
    - `--consistency`: The data consistency. The default value is `auto`. For Serverless Tier, you must set it to `none`.

    For more information about Dumpling options, see [Dumpling option list](/dumpling-overview.md#option-list-of-dumpling).

    The minimum permissions required are as follows:

    - `SELECT`
    - `RELOAD`
    - `LOCK TABLES`
    - `REPLICATION CLIENT`

After exporting data using Dumpling, you can import the data to MySQL compatible databases by using [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview).
