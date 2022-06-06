---
title: Query Status
summary: Learn how to query the status of a data replication task.
---

# クエリステータス {#query-status}

このドキュメントでは、 `query-status`コマンドを使用してタスクステータスとDMのサブタスクステータスを照会する方法を紹介します。

## クエリ結果 {#query-result}

{{< copyable "" >}}

```bash
» query-status
```

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
```

`tasks`セクションの`taskStatus`の詳細については、 [タスクステータス](#task-status)を参照してください。

次の手順で`query-status`を使用することをお勧めします。

1.  `query-status`を使用して、進行中の各タスクが正常な状態にあるかどうかを確認します。
2.  タスクでエラーが発生した場合は、 `query-status <taskName>`コマンドを使用して詳細なエラー情報を確認してください。このコマンドの`<taskName>`は、エラーが発生したタスクの名前を示します。

## タスクステータス {#task-status}

DM移行タスクのステータスは、DM-workerに割り当てられた各サブタスクのステータスによって異なります。サブタスクステータスの詳細については、 [サブタスクのステータス](#subtask-status)を参照してください。次の表は、サブタスクのステータスがタスクのステータスとどのように関連しているかを示しています。

| タスクのサブタスクステータス                                                                   | タスクステータス                                       |
| :------------------------------------------------------------------------------- | :--------------------------------------------- |
| 1つのサブタスクが`paused`状態にあり、エラー情報が返されます。                                              | `Error - Some error occurred in subtask`       |
| 同期フェーズの`Stopped`つのサブタスクは`Running`状態ですが、そのリレー処理ユニットは実行されて`Paused`ません（ `Error`状態）。 | `Error - Relay status is Error/Paused/Stopped` |
| 1つのサブタスクは`Paused`状態であり、エラー情報は返されません。                                             | `Paused`                                       |
| すべてのサブタスクは`New`状態です。                                                             | `New`                                          |
| すべてのサブタスクは`Finished`状態です。                                                        | `Finished`                                     |
| すべてのサブタスクは`Stopped`状態です。                                                         | `Stopped`                                      |
| その他の状況                                                                           | `Running`                                      |

## 詳細なクエリ結果 {#detailed-query-result}

{{< copyable "" >}}

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
                        "totalEvents": "12",    # The total number of binlog events that are replicated in this subtask.
                        "totalTps": "1",        # The number of binlog events that are replicated in this subtask per second.
                        "recentTps": "1",       # The number of binlog events that are replicated in this subtask in the last one second.
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
                                                # upstream. The save point is not refreshed in real time in the `Sync` background, so "false" of "synced"
                                                # does not always mean a replication delay exits.
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
                        "finishedBytes": "115", # The number of bytes that have been loaded.
                        "totalBytes": "452",    # The total number of bytes that need to be loaded.
                        "progress": "25.44 %"   # The progress of the loading process.
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
                        "progress": "0.00 %"
                    }
                }
            ]
        }
    ]
}

```

「sources」の「subTaskStatus」の「stage」のステータスの説明とステータススイッチの関係については、 [サブタスクステータス](#subtask-status)を参照してください。

「sources」の「subTaskStatus」の「unresolvedDDLLockID」の操作内容は[シャーディングDDLロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。

## サブタスクのステータス {#subtask-status}

### ステータスの説明 {#status-description}

-   `New` ：

    -   初期状態。
    -   サブタスクでエラーが発生しない場合は、 `Running`に切り替えられます。それ以外の場合は`Paused`に切り替えられます。

-   `Running` ：通常の実行状態。

-   `Paused` ：

    -   一時停止ステータス。
    -   サブタスクでエラーが発生した場合は、 `Paused`に切り替えられます。
    -   サブタスクが`Running`ステータスのときに`pause-task`を実行すると、タスクは`Paused`に切り替わります。
    -   サブタスクがこのステータスの場合、 `resume-task`コマンドを実行してタスクを再開できます。

-   `Stopped` ：

    -   停止状態。
    -   サブタスクが`Running`または`Paused`ステータスのときに`stop-task`を実行すると、タスクは`Stopped`に切り替わります。
    -   サブタスクがこのステータスの場合、 `resume-task`を使用してタスクを再開することはできません。

-   `Finished` ：

    -   終了したサブタスクのステータス。
    -   フルレプリケーションサブタスクが正常に終了した場合にのみ、タスクはこのステータスに切り替わります。

### ステータススイッチ図 {#status-switch-diagram}

```
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
```
