---
title: Data Check in the Sharding Scenario
summary: シャーディング シナリオでのデータ チェックについて学習します。
---

# シャーディングシナリオにおけるデータチェック {#data-check-in-the-sharding-scenario}

sync-diff-inspector は、シャーディングシナリオにおけるデータチェックをサポートします。1 ツール[TiDBデータ移行](/dm/dm-overview.md)使用して複数の MySQL インスタンスから TiDB にデータを複製する場合、sync-diff-inspector を使用して上流と下流のデータをチェックできます。

上流のシャードテーブルの数が少なく、シャードテーブルの命名規則にパターンがない場合（以下を参照）、 `Datasource config`使用して`table-0`設定し、対応する`rules`設定して、上流データベースと下流データベース間のマッピング関係を持つテーブルを設定できます。この設定方法では、すべてのシャードテーブルを設定する必要があります。

![shard-table-replica-1](/media/shard-table-replica-1.png)

以下は sync-diff-inspector 構成の完全な例です。

```toml
# Diff Configuration.

######################### Global config #########################

# The number of goroutines created to check data. The number of connections between upstream and downstream databases are slightly greater than this value
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables
export-fix-sql = true

# Only compares the table structure instead of the data
check-struct-only = false

######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule2"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test"        # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "table-[1-2]"  # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"         # The name of the schema in the target database
target-table = "table-0"       # The name of the target table

[routes.rule2]
schema-pattern = "test"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "table-3"    # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"       # The name of the schema in the target database
target-table = "table-0"     # The name of the target table

######################### Task config #########################
[task]
    output-dir = "./output"

    source-instances = ["mysql1", "mysql2"]

    target-instance = "tidb0"

    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    target-check-tables = ["test.table-0"]
```

アップストリームのシャード テーブルが多数あり、すべてのシャード テーブルの命名規則に次のようなパターンがある場合は、構成に`table-rules`使用できます。

![shard-table-replica-2](/media/shard-table-replica-2.png)

以下は sync-diff-inspector 構成の完全な例です。

```toml
# Diff Configuration.
######################### Global config #########################

# The number of goroutines created to check data. The number of connections between upstream and downstream databases are slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the table structure instead of the data.
check-struct-only = false

######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "table-*"    # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"       # The name of the schema in the target database
target-table = "table-0"     # The name of the target table

######################### Task config #########################
[task]
    output-dir = "./output"
    source-instances = ["mysql1", "mysql2"]

    target-instance = "tidb0"

    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    target-check-tables = ["test.table-0"]
```

## 注記 {#note}

上流データベースに`test.table-0`存在する場合、下流データベースもこのテーブルを比較します。
