---
title: Stop a Data Migration Task
summary: Learn how to stop a data migration task.
---

# データ移行タスクを停止する {#stop-a-data-migration-task}

`stop-task`コマンドを使用して、データ移行タスクを停止できます。 `stop-task`と`pause-task`の違いについては、 [データ移行タスクを一時停止します](/dm/dm-pause-task.md)を参照してください。

{{< copyable "" >}}

```bash
help stop-task
```

```
stop a specified task

Usage:
 dmctl stop-task [-s source ...] <task-name | task-file> [flags]

Flags:
 -h, --help   help for stop-task

Global Flags:
 -s, --source strings   MySQL Source ID
```

## 使用例 {#usage-example}

{{< copyable "" >}}

```bash
stop-task [-s "mysql-replica-01"]  task-name
```

## フラグの説明 {#flags-description}

-   `-s` :(オプション）移行タスク（停止する）のサブタスクが実行されるMySQLソースを指定します。設定されている場合、指定されたMySQLソースのサブタスクのみが停止されます。
-   `task-name | task-file` :(必須）タスク名またはタスクファイルのパスを指定します。

## 返された結果 {#returned-results}

{{< copyable "" >}}

```bash
stop-task test
```

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
```
