---
title: Pause a Data Migration Task
summary: Learn how to pause a data migration task in TiDB Data Migration.
---

# データ移行タスクを一時停止します {#pause-a-data-migration-task}

`pause-task`コマンドを使用して、データ移行タスクを一時停止できます。

`pause-task`は`stop-task`とは次の点で異なります。

-   `pause-task`は、移行タスクを一時停止するだけです。 `query-status`を使用して、タスクのステータス情報（メモリに保持されている）を照会できます。 `stop-task`は移行タスクを終了し、このタスクに関連するすべての情報をメモリから削除します。これは、 `query-status`を使用してステータス情報を照会できないことを意味します。 「チェックポイント」のような`dm_meta`と、ダウンストリームに移行されたデータは削除されません。
-   移行タスクを一時停止するために`pause-task`を実行した場合、同じ名前で新しいタスクを開始することはできません。また、このタスクが存在するため、一時停止したタスクのリレーログを削除することもできません。 `stop-task`を実行してタスクを停止すると、同じ名前で新しいタスクを開始できます。また、このタスクは存在しないため、停止したタスクのリレーログを削除できます。
-   `pause-task`は通常、トラブルシューティングのためにタスクを一時停止するために使用され、 `stop-task`は移行タスクを完全に削除するため、または`start-task`と連携して構成情報を更新するために使用されます。

{{< copyable "" >}}

```bash
help pause-task
```

```
pause a specified running task

Usage:
 dmctl pause-task [-s source ...] <task-name | task-file> [flags]

Flags:
 -h, --help   help for pause-task

Global Flags:
 -s, --source strings   MySQL Source ID
```

## 使用例 {#usage-example}

{{< copyable "" >}}

```bash
pause-task [-s "mysql-replica-01"] task-name
```

## フラグの説明 {#flags-description}

-   `-s` :(オプション）移行タスクのサブタスクを一時停止するMySQLソースを指定します。設定されている場合、このコマンドは指定されたMySQLソースのサブタスクのみを一時停止します。
-   `task-name| task-file` :(必須）タスク名またはタスクファイルのパスを指定します。

## 返された結果 {#returned-results}

{{< copyable "" >}}

```bash
pause-task test
```

```
{
    "op": "Pause",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```
