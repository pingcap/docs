---
title: Create a Data Migration Task
summary: Learn how to create a data migration task in TiDB Data Migration.
---

# データ移行タスクの作成 {#create-a-data-migration-task}

`start-task`コマンドを使用して、データ移行タスクを作成できます。データ移行タスクが開始されると、DM [権限と構成を事前チェックします](/dm/dm-precheck.md) .

```bash
help start-task
```

    Starts a task as defined in the configuration file

    Usage:
      dmctl start-task [-s source ...] [--remove-meta] <config-file> [flags]

    Flags:
      -h, --help                help for start-task
          --remove-meta         whether to remove task's meta data
          --start-time string   specify the start time of binlog replication, e.g. '2021-10-21 00:01:00' or 2021-10-21T00:01:00

    Global Flags:
          --config string        Path to config file.
          --master-addr string   Master API server address, this parameter is required when interacting with the dm-master
          --rpc-timeout string   RPC timeout, default is 10m. (default "10m")
      -s, --source strings       MySQL Source ID.
          --ssl-ca string        Path of file that contains list of trusted SSL CAs for connection.
          --ssl-cert string      Path of file that contains X509 certificate in PEM format for connection.
          --ssl-key string       Path of file that contains X509 key in PEM format for connection.
      -V, --version              Prints version and exit.

## 使用例 {#usage-example}

```bash
start-task [ -s "mysql-replica-01"] ./task.yaml
```

## フラグの説明 {#flags-description}

-   `-s` : (オプション) 実行する MySQL ソースを指定します`task.yaml` 。これが設定されている場合、コマンドは MySQL ソース上で指定されたタスクのサブタスクのみを開始します。
-   `config-file` : (必須) `task.yaml`のファイル パスを指定します。
-   `remove-meta` : (オプション) タスクの開始時にタスクの以前のメタデータを削除するかどうかを指定します。
-   `start-time` : (オプション)binlogレプリケーションの開始時刻を指定します。
    -   形式: `'2021-10-21 00:01:00'`または`2021-10-21T00:01:00` 。
    -   増分タスクの場合、このフラグを使用してタスクの大まかな開始点を指定できます。このフラグは、タスク構成ファイル内のbinlogの位置およびダウンストリームチェックポイント内のbinlogの位置よりも優先されます。
    -   タスクにすでにチェックポイントがある場合、このフラグを使用してタスクを開始すると、レプリケーションがチェックポイントを通過するまで、DM は自動的にセーフ モードを有効にします。これは、タスクを以前の位置にリセットすることによって発生するデータ重複エラーを回避するためです。
        -   タスクを以前の位置にリセットすると、その時点のテーブル スキーマが現在の時点のダウンストリームと異なる場合、タスクはエラーを報告する可能性があります。
        -   タスクを後の位置にリセットする場合は、スキップされたbinlogのダウンストリームにダーティなデータが残る可能性があることに注意してください。
    -   より早い開始時刻を指定すると、DM は利用可能な最も早いbinlogの位置から移行を開始します。
    -   遅い開始時刻を指定すると、DM はエラー`start-time {input-time} is too late, no binlog location matches it`を報告します。

## 返された結果 {#returned-results}

```bash
start-task task.yaml
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
