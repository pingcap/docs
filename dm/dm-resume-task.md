---
title: Resume a Data Migration Task
summary: データ移行タスクを再開する方法を学びます。
---

# データ移行タスクを再開する {#resume-a-data-migration-task}

`resume-task`コマンドを使用すると、状態`Paused`にあるデータ移行タスクを再開できます。これは通常、タスクを一時停止させるエラーを処理した後に、データ移行タスクを手動で再開したい場合に使用されます。

```bash
help resume-task
```

    resume a specified paused task

    Usage:
     dmctl resume-task [-s source ...] <task-name | task-file> [flags]

    Flags:
     -h, --help   help for resume-task

    Global Flags:
     -s, --source strings   MySQL Source ID

## 使用例 {#usage-example}

```bash
resume-task [-s "mysql-replica-01"] task-name
```

## フラグの説明 {#flags-description}

-   `-s` : (オプション) 移行タスクのサブタスクを再開するMySQLソースを指定します。設定されている場合、コマンドは指定されたMySQLソースのサブタスクのみを再開します。
-   `task-name | task-file` : (必須) タスク名またはタスク ファイル パスを指定します。

## 返された結果 {#returned-results}

```bash
resume-task test
```

    {
        "op": "Resume",
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
