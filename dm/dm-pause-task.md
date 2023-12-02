---
title: Pause a Data Migration Task
summary: Learn how to pause a data migration task in TiDB Data Migration.
---

# データ移行タスクを一時停止する {#pause-a-data-migration-task}

`pause-task`コマンドを使用すると、データ移行タスクを一時停止できます。

`pause-task`次の点で`stop-task`と異なります。

-   `pause-task`移行タスクのみを一時停止します。 `query-status`を使用して、タスクのステータス情報 (メモリに保持されている) を照会できます。 `stop-task`移行タスクを終了し、このタスクに関連するすべての情報をメモリから削除します。これは、ステータス情報のクエリに`query-status`を使用できないことを意味します。 `dm_meta` 「チェックポイント」など、ダウンストリームに移行されたデータは削除されません。
-   `pause-task`を実行して移行タスクを一時停止した場合、このタスクは存在するため、同じ名前で新しいタスクを開始することはできません。また、一時停止したタスクのリレー ログを削除することもできません。 `stop-task`を実行してタスクを停止すると、同じ名前で新しいタスクを開始でき、停止したタスクのリレー ログは削除されます。このタスクは存在しなくなったためです。
-   通常`pause-task`トラブルシューティングのためにタスクを一時停止するために使用され、 `stop-task`は移行タスクを永久に削除するか、 `start-task`と連携して構成情報を更新するために使用されます。

```bash
help pause-task
```

    pause a specified running task

    Usage:
     dmctl pause-task [-s source ...] <task-name | task-file> [flags]

    Flags:
     -h, --help   help for pause-task

    Global Flags:
     -s, --source strings   MySQL Source ID

## 使用例 {#usage-example}

```bash
pause-task [-s "mysql-replica-01"] task-name
```

## フラグの説明 {#flags-description}

-   `-s` : (オプション) 移行タスクのサブタスクを一時停止する MySQL ソースを指定します。設定されている場合、このコマンドは、指定された MySQL ソースのサブタスクのみを一時停止します。
-   `task-name| task-file` : (必須) タスク名またはタスク ファイルのパスを指定します。

## 返された結果 {#returned-results}

```bash
pause-task test
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
