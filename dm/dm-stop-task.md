---
title: Stop a Data Migration Task
summary: データ移行タスクを停止する方法を学びます。
---

# データ移行タスクを停止する {#stop-a-data-migration-task}

`stop-task`コマンドを使用して、データ移行タスクを停止できます。 `stop-task`と`pause-task`の違いについては、 [データ移行タスクを一時停止する](/dm/dm-pause-task.md)を参照してください。

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

-   `-s` : (オプション) 停止する移行タスクのサブタスクが実行される MySQL ソースを指定します。設定されている場合、指定された MySQL ソースのサブタスクのみが停止されます。
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
