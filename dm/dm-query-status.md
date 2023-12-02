---
title: Query Task Status in TiDB Data Migration
summary: Learn how to query the status of a data replication task.
---

# TiDB データ移行でのタスク ステータスのクエリ {#query-task-status-in-tidb-data-migration}

このドキュメントでは、 `query-status`コマンドを使用してタスクのステータスと DM のサブタスクのステータスを問い合わせる方法を紹介します。

## クエリ結果 {#query-result}

```bash
» query-status
```

    {
        "result": true,     # Whether the query is successful.
        "msg": "",          # Describes the reason for the unsuccessful query.
        "tasks": [          # Migration task list.
            {
                "taskName": "test",         # The task name.
                "taskStatus": "Running",    # The status of the task.
                "sources": [                # The upstream MySQL list.
                    "mysql-replica-01",
                    "mysql-replica-02"
                ]
            },
            {
                "taskName": "test2",
                "taskStatus": "Paused",
                "sources": [
                    "mysql-replica-01",
                    "mysql-replica-02"
                ]
            }
        ]
    }

`tasks`の`taskStatus`の詳しい説明は[タスクのステータス](#task-status)を参照してください。

次の手順で`query-status`を使用することをお勧めします。

1.  実行中の各タスクが通常の状態であるかどうかを確認するには、 `query-status`使用します。
2.  タスクでエラーが発生した場合は、 `query-status <taskName>`コマンドを使用して詳細なエラー情報を確認します。このコマンドの`<taskName>`エラーが発生したタスクの名前を示します。

## タスクのステータス {#task-status}

DM 移行タスクのステータスは、DM ワーカーに割り当てられた各サブタスクのステータスによって異なります。サブタスクのステータスの詳細については、 [サブタスクのステータス](#subtask-status)を参照してください。次の表は、サブタスクのステータスとタスクのステータスの関係を示しています。

| タスク内のサブタスクのステータス                                                                            | タスクのステータス                                      |
| :------------------------------------------------------------------------------------------ | :--------------------------------------------- |
| 1 つのサブタスクが`paused`状態にあり、エラー情報が返されます。                                                        | `Error - Some error occurred in subtask`       |
| 同期フェーズの 1 つのサブタスクは`Running`状態ですが、そのリレー処理ユニットは実行されていません ( `Error` / `Paused` / `Stopped`状態)。 | `Error - Relay status is Error/Paused/Stopped` |
| 1 つのサブタスクは`Paused`状態にあり、エラー情報は返されません。                                                       | `Paused`                                       |
| すべてのサブタスクは`New`状態になります。                                                                     | `New`                                          |
| すべてのサブタスクは`Finished`状態になります。                                                                | `Finished`                                     |
| すべてのサブタスクは`Stopped`状態になります。                                                                 | `Stopped`                                      |
| その他の状況                                                                                      | `Running`                                      |

## 詳細なクエリ結果 {#detailed-query-result}

```bash
» query-status test
```

```
» query-status
{
    "result": true,     # Whether the query is successful.
    "msg": "",          # Describes the cause for the unsuccessful query.
    "sources": [                            # The upstream MySQL list.
        {
            "result": true,
            "msg": "",
            "sourceStatus": {                   # The information of the upstream MySQL databases.
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [              # The information of all subtasks of upstream MySQL databases.
                {
                    "name": "test",         # The name of the subtask.
                    "stage": "Running",     # The running status of the subtask, including "New", "Running", "Paused", "Stopped", and "Finished".
                    "unit": "Sync",         # The processing unit of DM, including "Check", "Dump", "Load", and "Sync".
                    "result": null,         # Displays the error information if a subtask fails.
                    "unresolvedDDLLockID": "test-`test`.`t_target`",    # The sharding DDL lock ID, used for manually handling the sharding DDL
                                                                        # lock in the abnormal condition.
                    "sync": {                   # The replication information of the `Sync` processing unit. This information is about the
                                                # same component with the current processing unit.
                        "masterBinlog": "(bin.000001, 3234)",                               # The binlog position in the upstream database.
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # The GTID information in the upstream database.
                        "syncerBinlog": "(bin.000001, 2525)",                               # The position of the binlog that has been replicated
                                                                                            # in the `Sync` processing unit.
                        "syncerBinlogGtid": "",                                             # The binlog position replicated using GTID.
                        "blockingDDLs": [       # The DDL list that is blocked currently. It is not empty only when all the upstream tables of this
                                                # DM-worker are in the "synced" status. In this case, it indicates the sharding DDL statements to be executed or that are skipped.
                            "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                        ],
                        "unresolvedGroups": [   # The sharding group that is not resolved.
                            {
                                "target": "`test`.`t_target`",                  # The downstream database table to be replicated.
                                "DDLs": [
                                    "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                                ],
                                "firstPos": "(bin|000001.000001, 3130)",        # The starting position of the sharding DDL statement.
                                "synced": [                                     # The upstream sharded table whose executed sharding DDL statement has been read by the `Sync` unit.
                                    "`test`.`t2`"
                                    "`test`.`t3`"
                                    "`test`.`t1`"
                                ],
                                "unsynced": [                                   # The upstream table that has not executed this sharding DDL
                                                                                # statement. If any upstream tables have not finished replication,
                                                                                # `blockingDDLs` is empty.
                                ]
                            }
                        ],
                        "synced": false         # Whether the incremental replication catches up with the upstream and has the same binlog position as that in the
                                                # upstream. The save point is not refreshed in real time in the `Sync` background, so `false` of `synced`
                                                # does not always mean a replication delay exits.
                        "totalRows": "12",      # The total number of rows that are replicated in this subtask.
                        "totalRps": "1",        # The number of rows that are replicated in this subtask per second.
                        "recentRps": "1"        # The number of rows that are replicated in this subtask in the last second.
                    }
                }
            ]
        },
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-02",
                "worker": "worker2",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Load",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "load": {                   # The replication information of the `Load` processing unit.
                        "finishedBytes": "115",          # The number of bytes that have been loaded.
                        "totalBytes": "452",               # The total number of bytes that need to be loaded.
                        "progress": "25.44 %",         # The progress of the loading process.
                        "bps": "2734"                        # The speed of the full loading.
                    }
                }
            ]
        },
        {
            "result": true,
            "sourceStatus": {
                "source": "mysql-replica-03",
                "worker": "worker3",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Paused",
                    "unit": "Load",
                    "result": {                 # The error example.
                        "isCanceled": false,
                        "errors": [
                            {
                                "Type": "ExecSQL",
                                "msg": "Error 1062: Duplicate entry '1155173304420532225' for key 'PRIMARY'\n/home/jenkins/workspace/build_dm/go/src/github.com/pingcap/tidb-enterprise-tools/loader/db.go:160: \n/home/jenkins/workspace/build_dm/go/src/github.com/pingcap/tidb-enterprise-tools/loader/db.go:105: \n/home/jenkins/workspace/build_dm/go/src/github.com/pingcap/tidb-enterprise-tools/loader/loader.go:138: file test.t1.sql"
                            }
                        ],
                        "detail": null
                    },
                    "unresolvedDDLLockID": "",
                    "load": {
                        "finishedBytes": "0",
                        "totalBytes": "156",
                        "progress": "0.00 %",
                        "bps": "0"
                    }
                }
            ]
        },
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-04",
                "worker": "worker4",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Dump",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "dump": {                        # The replication information of the `Dump` processing unit.
                        "totalTables": "10",         # The number of tables to be dumped.
                        "completedTables": "3",      # The number of tables that have been dumped.
                        "finishedBytes": "2542",     # The number of bytes that have been dumped.
                        "finishedRows": "32",        # The number of rows that have been dumped.
                        "estimateTotalRows": "563",  # The estimated number of rows to be dumped.
                        "progress": "30.52 %",       # The progress of the dumping process.
                        "bps": "445"                 # The dumping speed.
                    }
                }
            ]
        },
    ]
}

```

「sources」の「subTaskStatus」の「stage」の状態説明と状態切り替え関係については、 [サブタスクのステータス](#subtask-status)を参照してください。

「sources」の「subTaskStatus」の「unresolvedDDLLockID」の操作詳細については、 [シャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。

## サブタスクのステータス {#subtask-status}

### ステータスの説明 {#status-description}

-   `New` :

    -   初期状態。
    -   サブタスクでエラーが発生しない場合は、 `Running`に切り替えられます。それ以外の場合は`Paused`に切り替えられます。

-   `Running` : 通常の動作状態。

-   `Paused` :

    -   一時停止状態。
    -   サブタスクでエラーが発生した場合、サブタスクは`Paused`に切り替わります。
    -   サブタスクが`Running`ステータスにあるときに`pause-task`を実行すると、タスクは`Paused`に切り替わります。
    -   サブタスクがこのステータスの場合、 `resume-task`コマンドを実行してタスクを再開できます。

-   `Stopped` :

    -   停止状態。
    -   サブタスクが`Running`または`Paused`ステータスにあるときに`stop-task`実行すると、タスクは`Stopped`に切り替わります。
    -   サブタスクがこのステータスの場合、 `resume-task`を使用してタスクを再開することはできません。

-   `Finished` :

    -   完了したサブタスクのステータス。
    -   フルレプリケーションサブタスクが正常に終了した場合のみ、この状態に切り替わります。

### ステータススイッチ図 {#status-switch-diagram}

                                             error occurs
                                New --------------------------------|
                                 |                                  |
                                 |           resume-task            |
                                 |  |----------------------------|  |
                                 |  |                            |  |
                                 |  |                            |  |
                                 v  v        error occurs        |  v
      Finished <-------------- Running -----------------------> Paused
                                 ^  |        or pause-task       |
                                 |  |                            |
                      start task |  | stop task                  |
                                 |  |                            |
                                 |  v        stop task           |
                               Stopped <-------------------------|
