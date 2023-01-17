---
title: Collect SQL Query Plan Information Using PingCAP Clinic Diag
summary: Learn how to use PingCAP Clinic Diag to collect SQL query plan information on clusters deployed using TiUP.
---

# Collect SQL Query Plan Information Using PingCAP Clinic Diag

Starting from v5.3.0, TiDB introduces the [`PLAN REPLAYER`](/sql-plan-replayer.md) feature to import and export SQL query plan information using a single command, and simplifies troubleshooting hints-related issues. Clinic Diag client (Diag) integrates the `PLAN REPLAYER` feature. You can use Diag to collect SQL query plan information conveniently.

## Description

When you troubleshoot issues in TiDB v4.0 or higher versions, you can use Diag to export the relevant data in the cluster as a ZIP-formatted file and upload it to PingCAP Clinic for technical support quickly. Before using Diag to collect data, you need to provide a SQL statement file for collection. The data collected by Diag includes log information and cluster information in addition to the data collected by the `PLAN REPLAYER` feature. For more information, see [Output](#output).

> **Warning:**
>
> - This is an experimental feature. It is not recommended that you use it in a production environment.
> - This feature **does not support** clusters deployed using TiDB Operator.

## Usage

This section describes how to use Diag to collect SQL query plan information. You need to install Diag first, and then collect data using Diag.

### Install Diag

- You can use the following TiUP command to install Diag. The latest version is installed by default:

    ```bash
    tiup install diag
    ```

- If you have installed Diag, make sure the version is >= **0.7.3**.

    To check the version of Diag, you can use the following command:

    ```bash
    tiup diag --version
    ```

    If the Diag version does not meet the requirement, you can upgrade to the latest version using the following command:

    ```bash
    tiup update diag
    ```

### Full data collection

To collect data, you can use the following `diag collect` command and replace the `<cluster-name>` and `<statement-filepath>` with your actual information:

```bash
diag collect <cluster-name> --profile=tidb-plan-replayer --explain-sql=<statement-filepath>
```

> **Note:**
>
> - Before collecting data using `diag`, you need to specify the `sql-statement` file using the `--explain-sql` option:
>
>     - In the preceding command, the `<statement-filepath>` is the path of the `sql-statement` file.
>     - The `sql-statement` file contains the SQL statements to be collected.
>     - If there are multiple SQL statements to be collected, you can use the `;` to separate them.
>     - Because the preceding `diag` command creates a new session to execute the SQL statements, make sure that the SQL statements in the `sql-statement` file must explicitly specify the database name, such as `SELECT * FROM test.t1`.
>
> - `PLAN REPLAYER` does **not** export data in the tables.
> - Only `EXPLAIN` is executed during data collection and the SQL statements are not executed. Therefore, the impact on the database performance during collection is minimal.

The following is an example of the `sql-statement` file:

```sql
SELECT * FROM test.t1;SELECT * FROM test.t2;
```

#### Output

The output of the collection is as follows:

| Number | Item | Diag collector | Output file |
| :--- | :--- | :--- | :--- |
| 1 | TiDB configuration | `config` | `tidb.toml` |
| 2 | TiDB session variables | `db_vars` | `global_variables.csv`, `mysql.tidb.csv` |
| 3 | TiDB SQL bindings | `sql_bind` | `sql_bind/global_bind.csv` |
| 4 | The table schema in `sql-statement` | `statistics` | `statistics/<db.table>.schema` |
| 5 | The statistics of the table in `sql-statement` | `statistics` | `statistics/<db.table>.json` |
| 6 | The result of `EXPLAIN [ANALYZE] sql-statement` | `explain` | `explain/sql0` |
| 7 | <ul><li>TiDB logs</li><li> TiUP logs of cluster operations</li></ul> | <ul><li>`log`</li><li>`-R=tidb`</li></ul> | `tidb.log`, `tidb_slow_query.log`, `tidb_stdeer.log`, `cluster_audit/$auditfilename` |
| 8 | The cluster information collected by default<ul><li>Basic information of the cluster</li><li>The collection result of Diag</li></ul> | default | `cluster.json`, `meta.yaml`, `$collectid_diag_audit.log` |

### Custom data collection

You can create a customized configuration file to collect part of the data in the preceding [output](#output) table. The following takes `tidb-plan-replayer.toml` as an example:

```toml
name = "tidb-plan-replayer"
version = "0.0.1"
maintainers = [
    "pingcap"
]

# list of data types to collect
collectors = [
    "config",
    "sql_bind",
    "plan_replayer"
]

# list of component roles to collect
roles = [
    "tidb"
]
```

To collect custom data, specify the path to the configuration file using the `--profile` option:

```bash
diag collect <cluster-name> --profile=<profile-filepath> --explain-sql=<statement-filepath>
```

### Import the data into a TiDB cluster

The `plan_replayer.zip` in the collection result can be directly imported into the TiDB cluster using the `PLAN REPLAYER LOAD` statement. For more information, see [Use `PLAN REPLAYER` to import cluster information](/sql-plan-replayer.md#use-plan-replayer-to-import-cluster-information)
