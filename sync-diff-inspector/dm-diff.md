---
title: Data Check in the DM Replication Scenario
summary: データ チェックを実行するために、DM-master` から特定の `task-name` 構成を設定する方法について説明します。
---

# DM レプリケーション シナリオにおけるデータ チェック {#data-check-in-the-dm-replication-scenario}

[TiDB データ移行](/dm/dm-overview.md)などのレプリケーション ツールを使用する場合、レプリケーション処理の前後でデータの整合性を確認する必要があります`DM-master`から特定の`task-name`構成を設定して、データ チェックを実行できます。

以下は簡単な設定例です。完全な設定については[Sync-diff-inspector ユーザーガイド](/sync-diff-inspector/sync-diff-inspector-overview.md)を参照してください。

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

この例では、dm-task = &quot;test&quot; に設定されており、&quot;test&quot; タスクの下にある hb_test スキーマのすべてのテーブルをチェックします。DM レプリケーション後のデータの一貫性を確認するために、アップストリーム データベースとダウンストリーム データベース間のスキーマの定期的なマッチングが自動的に取得されます。
