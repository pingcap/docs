---
title: DM Query Status
summary: Learn the query result and subtask status of DM query status.
category: tools
---

# DM Query Status

This document introduces the query result and subtask status of DM query status.

## Query result

```
» query-status
{
    "result": true,     # Whether the query is successful.
    "msg": "",          # Describes the cause for the unsuccessful query.
    "workers": [                            # DM-worker list.
        {
            "result": true,
            "worker": "172.17.0.2:10081",   # The `host:port` information of the DM-worker.
            "msg": "",
            "subTaskStatus": [              # The information of all the subtasks of the DM-worker.
                {
                    "name": "test",         # The name of the subtask.
                    "stage": "Running",     # The running status of the subtask, including "New", "Running", "Paused", "Stopped", and "Finished".
                    "unit": "Sync",         # The processing unit of DM, including "Check", "Dump", "Load", and "Sync".
                    "result": null,         # Displays the error information if a subtask fails.
                    "unresolvedDDLLockID": "test-`test`.`t_target`",    # The sharding DDL lock ID, used for manually handling the sharding DDL 
                                                                        # lock in the abnormal condition.
                    "sync": {                   # The synchronization information of the `Sync` processing unit. This information is about the 
                                                # same component with the current processing unit.
                        "totalEvents": "12",    # The total number of binlog events that are synchronized in this subtask.
                        "totalTps": "1",        # The number of binlog events that are synchronized in this subtask per second.
                        "recentTps": "1",       # The number of binlog events that are synchronized in this subtask in the last one second.
                        "masterBinlog": "(bin.000001, 3234)",                               # The binlog position in the upstream database.
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # The GTID information in the upstream database.
                        "syncerBinlog": "(bin.000001, 2525)",                               # The position of the binlog that has been synchronized
                                                                                            # in the `Sync` processing unit.
                        "syncerBinlogGtid": "",                                             # It is always empty because `Sync` does not use GTID to
                                                                                            # synchronize data.
                        "blockingDDLs": [       # The DDL list that is blocked currently. It is not empty only when all the upstream tables of this 
                                                # DM-worker are "synced". In this case, it indicates the sharding DDL statement to be executed or skipped.
                            "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                        ],
                        "unresolvedGroups": [   # The sharding group that is not resolved.
                            {
                                "target": "`test`.`t_target`",                  # The downstream database table to be synchronized.
                                "DDLs": [
                                    "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                                ],
                                "firstPos": "(bin|000001.000001, 3130)",        # The starting position of the sharding DDL statement.
                                "synced": [                                     # The sharded table of the sharding DDL statement that `Sync` has read.
                                    "`test`.`t2`"
                                    "`test`.`t3`"
                                    "`test`.`t1`"
                                ],
                                "unsynced": [                                   # The upstream table of the sharding DDL statement that has not been
                                                                                # executed. If any upstream tables have not been synchronized completely,  
                                                                                # `blockingDDLs` is empty.
                                ]
                            }
                        ],
                        "synced": false         # Whether the progress of incremental synchronization in the downstream has been the same as that in the 
                                                # upstream. The save point is not refreshed in real time in the `Sync` background, so "false" of "synced" 
                                                # does not always mean a synchronization delay exits.
                    }
                }
            ],
            "relayStatus": {    # The synchronization status of the relay log.
                "masterBinlog": "(bin.000001, 3234)",                               # The binlog position of the upstream database.
                "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",    # The binlog GTID information of the upstream database.
                "relaySubDir": "c0149e17-dff1-11e8-b6a8-0242ac110004.000001",       # The currently used subdirectory of the relay log.
                "relayBinlog": "(bin.000001, 3234)",                                # The position of the binlog that has been pulled to the local storage.
                "relayBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",     # The GTID information of the binlog that has been pulled to the local 
                                                                                    # storage.
                "relayCatchUpMaster": true,     # Whether the progress of synchronizing the relay log in the local storage has been the same as that in 
                                                # the upstream.
                "stage": "Running",             # The status of the `Sync` processing unit of the relay log.
                "result": null
            }
        },
        {
            "result": true,
            "worker": "172.17.0.3:10081",
            "msg": "",
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Load",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "load": {                   # The synchronization information of the `Load` processing unit.
                        "finishedBytes": "115", # The number of bytes that have been imported fully.
                        "totalBytes": "452",    # The total number of bytes that need to be imported.
                        "progress": "25.44 %"   # The progress of the full import.
                    }
                }
            ],
            "relayStatus": {
                "masterBinlog": "(bin.000001, 28507)",
                "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-96",
                "relaySubDir": "c0149e17-dff1-11e8-b6a8-0242ac110004.000001",
                "relayBinlog": "(bin.000001, 28507)",
                "relayBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-96",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
            }
        },
        {
            "result": true,
            "worker": "172.17.0.3:10081",
            "msg": "",
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Load",
                    "result": null,
                    "unresolvedDDLLockID": "",
                    "load": {                   # The synchronization information of the `Load` processing unit.
                        "finishedBytes": "115", # The number of bytes that have been imported fully.
                        "totalBytes": "452",    # The total number of bytes that need to be imported.
                        "progress": "25.44 %"   # The progress of the full import.
                    }
                }
            ],
            "relayStatus": {
                "masterBinlog": "(bin.000001, 28507)",
                "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-96",
                "relaySubDir": "c0149e17-dff1-11e8-b6a8-0242ac110004.000001",
                "relayBinlog": "(bin.000001, 28507)",
                "relayBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-96",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
            }
        }
                {
            "result": true,
            "worker": "172.17.0.6:10081",
            "msg": "",
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
            ],
            "relayStatus": {
                "masterBinlog": "(bin.000001, 1691)",
                "masterBinlogGtid": "97b5142f-e19c-11e8-808c-0242ac110005:1-9",
                "relaySubDir": "97b5142f-e19c-11e8-808c-0242ac110005.000001",
                "relayBinlog": "(bin.000001, 1691)",
                "relayBinlogGtid": "97b5142f-e19c-11e8-808c-0242ac110005:1-9",
                "relayCatchUpMaster": true,
                "stage": "Running",
                "result": null
            }
        }
    ]
}

```

For the status description and status switch relationship of "stage" of "subTaskStatus" of "workers", see [Subtask status](#subtask-status).
For operation details of "unresolvedDDLLockID" of "subTaskStatus" of "workers", see [Troubleshooting Sharding DDL Locks](../tools/troubleshooting-sharding-ddl-locks/).

## Subtask status

### Status description

- `New`: 

    - The initial status. 
    - If the subtask does not encounter an error, it is switched to `Running`; otherwise it is switched to `Paused`.

- `Running`: The normal running status.

- `Paused`: 

    - The paused status. 
    - If the subtask encounters an error, it is switched to `Paused`.
    - If you run `pause-task` when the subtask is in the `Running` status, the task is switched to `Paused`.
    - When the subtask is in this status, you can run the `resume-task` command to resume the task.

- `Stopped`: 

    - The stopped status.
    - If you run `stop-task` when the subtask is in the `Running` or `Paused` status, the task is switched to `Stopped`.
    - When the subtask is in this status, you cannot use `resume-task` to resume the task.

- `Finished`: 

    - The finished subtask status.
    - Only when the full synchronization subtask is finished normally, the task is switched to this status.

### Status switch diagram

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