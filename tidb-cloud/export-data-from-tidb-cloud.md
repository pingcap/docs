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
    tiup install dumpling:v6.1.1
    ```

4. Export your data using Dumpling from TiDB. You can export data in the following formats:

    <SimpleTab>

    <div label="Serverless Tier">

    ```shell
    tiup dumpling:v6.1.1 -h ${tidb-endpoint} -P ${port} -u ${user} -p ${password} --ca=${cert_path} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql
    ```

    </div>
    <div label="Dedicated Tier">

    ```shell
    tiup dumpling:v6.1.1 -h ${tidb-endpoint} -P ${port} -u ${user} -p ${password} -F 67108864MiB -t 4 -o ${export_dir} --filetype sql
    ```

    </div>

    Parameters are described as follows:

    - `-h` or `--host`: The TiDB cluster endpoint.
    - `--ca`: The CA root path. Refer to [Secure Connections to Serverless Tier Clusters](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md#where-is-the-ca-root-path-on-my-system).
    - `--filetype`: The exported file type. The default value is `sql`. You can choose from `sql` and `csv`.

    For more information about Dumpling options, see [Dumpling option list](/dumpling-overview.md#option-list-of-dumpling).

    The minimum permissions required are as follows:

    - `SELECT`
    - `RELOAD`
    - `LOCK TABLES`
    - `REPLICATION CLIENT`
