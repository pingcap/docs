---
title: Resume a Data Migration Task
summary: データ移行タスクを再開するためには、resume-taskコマンドを使用します。このコマンドは、一時停止したタスクを再開する際に使用されます。-sフラグを使用してMySQLソースを指定し、指定したソースのサブタスクのみを再開することも可能です。タスク名またはタスクファイルのパスを指定することで、再開するタスクを指定します。再開後の結果は、opが"Resume"でresultがtrueとなります。
---

# データ移行タスクを再開する {#resume-a-data-migration-task}

`resume-task`コマンドを使用すると、 `Paused`状態のデータ移行タスクを再開できます。これは通常、タスクを一時停止するエラーを処理した後にデータ移行タスクを手動で再開するシナリオで使用されます。

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

-   `-s` : (オプション) 移行タスクのサブタスクを再開する MySQL ソースを指定します。これが設定されている場合、コマンドは指定された MySQL ソースのサブタスクのみを再開します。
-   `task-name | task-file` : (必須) タスク名またはタスク ファイルのパスを指定します。

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
