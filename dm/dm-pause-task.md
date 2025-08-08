---
title: Pause a Data Migration Task
summary: TiDB データ移行でデータ移行タスクを一時停止する方法を学習します。
---

# データ移行タスクを一時停止する {#pause-a-data-migration-task}

`pause-task`コマンドを使用して、データ移行タスクを一時停止できます。

`pause-task` `stop-task`次の点で異なります:

-   `pause-task`移行タスクを一時停止するだけです。タスクのステータス情報（メモリに保持されている）は`query-status`で照会できます。4 `stop-task`移行タスクを終了し、このタスクに関連するすべての情報をメモリから削除します。つまり、 `query-status`使用してステータス情報を照会することはできません。「チェックポイント」のような`dm_meta`や、下流に移行済みのデータは削除されません。
-   `pause-task`実行して移行タスクを一時停止した場合、同じ名前の新しいタスクを開始することはできません。また、一時停止したタスクは既に存在するため、そのタスクのリレーログを削除することもできません`stop-task`実行してタスクを停止した場合、同じ名前の新しいタスクを開始できます。また、停止したタスクは既に存在しないため、そのタスクのリレーログを削除することができます。
-   `pause-task`は通常、トラブルシューティングのためにタスクを一時停止するために使用され、 `stop-task`は移行タスクを永続的に削除するか、 `start-task`と連携して構成情報を更新するために使用されます。

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

-   `-s` : (オプション) 移行タスクのサブタスクを一時停止するMySQLソースを指定します。設定されている場合、このコマンドは指定されたMySQLソースのサブタスクのみを一時停止します。
-   `task-name| task-file` : (必須) タスク名またはタスク ファイル パスを指定します。

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
