---
title: Stop a Data Migration Task
summary: データ移行タスクを停止する方法を学びます。
---

# データ移行タスクを停止する {#stop-a-data-migration-task}

`stop-task`コマンドを使用してデータ移行タスクを停止できます。3 と`stop-task` `pause-task`違いについては、 [データ移行タスクを一時停止する](/dm/dm-pause-task.md)を参照してください。

```bash
help stop-task
```

    stop a specified task

    Usage:
     dmctl stop-task [-s source ...] <task-name | task-file> [flags]

    Flags:
     -h, --help   help for stop-task

    Global Flags:
     -s, --source strings   MySQL Source ID

## 使用例 {#usage-example}

```bash
stop-task [-s "mysql-replica-01"]  task-name
```

## フラグの説明 {#flags-description}

-   `-s` : (オプション) 停止する移行タスクのサブタスクが実行されるMySQLソースを指定します。このパラメータが設定されている場合、指定されたMySQLソース上のサブタスクのみが停止されます。
-   `task-name | task-file` : (必須) タスク名またはタスク ファイル パスを指定します。

## 返された結果 {#returned-results}

```bash
stop-task test
```

    {
        "op": "Stop",
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

> **注記：**
>
> `stop-task`コマンドで移行タスクを停止した後、 [`query-status`](/dm/dm-query-status.md)を実行してもタスクは表示されなくなります。ただし、このタスクのチェックポイントやその他の関連情報は`dm_meta`データベースに保持されます。
>
> -   移行タスクを最初からやり直すには、 [`start-task`](/dm/dm-create-task.md)コマンドを実行するときに`--remove-meta`オプションを追加します。
> -   移行タスクを完全に削除するには、タスク名をプレフィックスとして使用する 4 つのテーブルを`dm_meta`データベースから手動で削除します。
