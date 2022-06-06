---
title: Create a Data Migration Task
summary: Learn how to create a data migration task in TiDB Data Migration.
---

# データ移行タスクを作成する {#create-a-data-migration-task}

`start-task`コマンドを使用して、データ移行タスクを作成できます。データ移行タスクが開始されると、 [特権と構成を事前にチェックします](/dm/dm-precheck.md) 。

{{< copyable "" >}}

```bash
help start-task
```

```
Starts a task as defined in the configuration file
Usage:
  dmctl start-task [-s source ...] [--remove-meta] <config-file> [flags]
Flags:
  -h, --help          Help for start-task
      --remove-meta   Whether to remove task's metadata
Global Flags:
  -s, --source strings   MySQL Source ID
```

## 使用例 {#usage-example}

{{< copyable "" >}}

```bash
start-task [ -s "mysql-replica-01"] ./task.yaml
```

## フラグの説明 {#flags-description}

-   `-s` :(オプション）実行するMySQLソースを指定します`task.yaml` 。設定されている場合、コマンドはMySQLソースで指定されたタスクのサブタスクのみを開始します。
-   `config-file` :(必須） `task.yaml`のファイルパスを指定します。
-   `remove-meta` :(オプション）タスクの開始時にタスクの以前のメタデータを削除するかどうかを指定します。

## 返された結果 {#returned-results}

{{< copyable "" >}}

```bash
start-task task.yaml
```

```
{
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
