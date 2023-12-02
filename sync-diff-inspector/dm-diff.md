---
title: Data Check in the DM Replication Scenario
summary: Learn about how to set a specific `task-name` configuration from `DM-master` to perform a data check.
---

# DM レプリケーション シナリオでのデータ チェック {#data-check-in-the-dm-replication-scenario}

[TiDB データ移行](/dm/dm-overview.md)などのレプリケーション ツールを使用する場合は、レプリケーション プロセスの前後でデータの整合性をチェックする必要があります。 `DM-master`の中から特定の`task-name`設定を設定してデータチェックを実行できます。

以下に簡単な構成例を示します。完全な構成については、 [Sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。

```toml
# Diff Configuration.

######################### Global config #########################

# The number of goroutines created to check data. The number of connections between upstream and downstream databases are slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the table structure instead of the data.
check-struct-only = false

# The IP address of dm-master and the format is "http://127.0.0.1:8261".
dm-addr = "http://127.0.0.1:8261"

# Specifies the `task-name` of DM.
dm-task = "test"

######################### Task config #########################
[task]
    output-dir = "./output"

    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    target-check-tables = ["hb_test.*"]
```

この例は dm-task = &quot;test&quot; で構成されており、&quot;test&quot; タスクの下の hb_test スキーマのすべてのテーブルをチェックします。 DM レプリケーション後のデータの整合性を検証するために、アップストリーム データベースとダウンストリーム データベース間のスキーマの定期的な一致を自動的に取得します。
