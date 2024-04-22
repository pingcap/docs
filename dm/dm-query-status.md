---
title: Query Task Status in TiDB Data Migration
summary: このドキュメントは、TiDBデータ移行中のタスクステータスのクエリ方法について説明しています。`query-status`コマンドを使用してタスクのステータスとDMのサブタスクのステータスを問い合わせることができます。成功したクエリ結果には、タスク名、タスクステータス、およびソースが含まれます。また、サブタスクのステータスについても説明されています。
---

# TiDB データ移行でのタスク ステータスのクエリ {#query-task-status-in-tidb-data-migration}

このドキュメントでは、 `query-status`コマンドを使用してタスクのステータスと DM のサブタスクのステータスを問い合わせる方法を紹介します。

## クエリ結果 {#query-result}

次の手順で`query-status`を使用することをお勧めします。

1.  実行中の各タスクが通常の状態であるかどうかを確認するには、 `query-status`使用します。
2.  タスクでエラーが発生した場合は、 `query-status <taskName>`コマンドを使用して詳細なエラー情報を確認します。このコマンドの`<taskName>`エラーが発生したタスクの名前を示します。

成功したクエリ結果は次のとおりです。

```bash
» query-status
```

```json
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "test",
            "taskStatus": "Running",
            "sources": [
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

クエリ結果の一部のフィールドは次のように説明されます。

-   `result` : クエリが成功したかどうか。
-   `msg` : クエリが失敗した場合に返されるエラー メッセージ。
-   `tasks` : 移行タスクのリスト。各タスクには次のフィールドが含まれます。
    -   `taskName` : タスクの名前。
    -   `taskStatus` : タスクのステータス。 `taskStatus`の詳しい説明は[タスクのステータス](#task-status)を参照してください。
    -   `sources` : アップストリーム MySQL データベースのリスト。

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

```json
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": null
            },
            "subTaskStatus": [
                {
                    "name": "test",
                    "stage": "Running",
                    "unit": "Sync",
                    "result": null,
                    "unresolvedDDLLockID": "test-`test`.`t_target`",
                    "sync": {
                        "masterBinlog": "(bin.000001, 3234)",
                        "masterBinlogGtid": "c0149e17-dff1-11e8-b6a8-0242ac110004:1-14",
                        "syncerBinlog": "(bin.000001, 2525)",
                        "syncerBinlogGtid": "",
                        "blockingDDLs": [
                            "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                        ],
                        "unresolvedGroups": [
                            {
                                "target": "`test`.`t_target`",
                                "DDLs": [
                                    "USE `test`; ALTER TABLE `test`.`t_target` DROP COLUMN `age`;"
                                ],
                                "firstPos": "(bin|000001.000001, 3130)",
                                "synced": [
                                    "`test`.`t2`"
                                    "`test`.`t3`"
                                    "`test`.`t1`"
                                ],
                                "unsynced": [
                                ]
                            }
                        ],
                        "synced": false,
                        "totalRows": "12",
                        "totalRps": "1",
                        "recentRps": "1"
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
                    "load": {
                        "finishedBytes": "115",
                        "totalBytes": "452",
                        "progress": "25.44 %",
                        "bps": "2734"
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
                    "result": {
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
                    "dump": {
                        "totalTables": "10",
                        "completedTables": "3",
                        "finishedBytes": "2542",
                        "finishedRows": "32",
                        "estimateTotalRows": "563",
                        "progress": "30.52 %",
                        "bps": "445"
                    }
                }
            ]
        },
    ]
}
```

返された結果の一部のフィールドは次のように説明されます。

-   `result` : クエリが成功したかどうか。
-   `msg` : クエリが失敗した場合に返されるエラー メッセージ。
-   `sources` : アップストリーム MySQL インスタンスのリスト。各ソースには次のフィールドが含まれます。
    -   `result`
    -   `msg`
    -   `sourceStatus` : 上流の MySQL データベースの情報。
    -   `subTaskStatus` : 上流の MySQL データベースのすべてのサブタスクの情報。各サブタスクには次のフィールドが含まれる場合があります。
        -   `name` : サブタスクの名前。
        -   `stage` : サブタスクのステータス。 「sources」の「subTaskStatus」の「stage」の状態説明と状態切り替え関係については、 [サブタスクのステータス](#subtask-status)を参照してください。
        -   `unit` : 「チェック」、「ダンプ」、「ロード」、「同期」を含む DM の処理単位。
        -   `result` : サブタスクが失敗した場合にエラー情報を表示します。
        -   `unresolvedDDLLockID` : 異常な状態でシャーディング DDL ロックを手動で処理するために使用されるシャーディング DDL ロック ID。 「sources」の「subTaskStatus」の「unresolvedDDLLockID」の操作詳細については、 [シャーディング DDL ロックを手動で処理する](/dm/manually-handling-sharding-ddl-locks.md)を参照してください。
        -   `sync` : `Sync`プロセッシングユニットのレプリケーション情報。この情報は、現在の処理ユニットと同じコンポーネントに関するものです。
            -   `masterBinlog` : 上流データベース内のbinlogの位置。
            -   `masterBinlogGtid` : 上流データベースの GTID 情報。
            -   `syncerBinlog` : `Sync`処理ユニットで複製されたbinlogの位置。
            -   `syncerBinlogGtid` : GTID を使用してレプリケートされたbinlogの位置。
            -   `blockingDDLs` : 現在ブロックされている DDL リスト。この DM ワーカーのすべての上流テーブルが「同期」ステータスにある場合にのみ空ではありません。この場合、実行されるシャーディング DDL ステートメント、またはスキップされるシャーディング DDL ステートメントを示します。
            -   `unresolvedGroups` : 解決されていないシャーディング グループ。各グループには次のフィールドが含まれます。
                -   `target` : レプリケートされるダウンストリーム データベース テーブル。
                -   `DDLs` : DDL ステートメントのリスト。
                -   `firstPos` : シャーディング DDL ステートメントの開始位置。
                -   `synced` : 実行されたシャーディング DDL ステートメントが`Sync`ユニットによって読み取られた上流シャーディング テーブル。
                -   `unsynced` : このシャーディング DDL ステートメントを実行していない上流テーブル。レプリケーションを完了していない上流テーブルがある場合、 `blockingDDLs`は空になります。
            -   `synced` : 増分レプリケーションがアップストリームに追いつき、アップストリームと同じbinlog位置を持つかどうか。セーブ ポイントは`Sync`バックグラウンドではリアルタイムで更新されないため、 `synced`の`false`は必ずしもレプリケーションの遅延が発生することを意味するわけではありません。
            -   `totalRows` : このサブタスクでレプリケートされる行の合計数。
            -   `totalRps` : このサブタスクで 1 秒あたりにレプリケートされる行の数。
            -   `recentRps` : 最後の 1 秒間にこのサブタスクでレプリケートされた行の数。
        -   `load` : `Load`プロセッシングユニットのレプリケーション情報。
            -   `finishedBytes` : ロードされたバイト数。
            -   `totalBytes` : ロードする必要がある合計バイト数。
            -   `progress` : ロードプロセスの進行状況。
            -   `bps` : フルロードの速度。
        -   `dump` : `Dump`プロセッシングユニットのレプリケーション情報。
            -   `totalTables` : ダンプするテーブルの数。
            -   `completedTables` : ダンプされたテーブルの数。
            -   `finishedBytes` : ダンプされたバイト数。
            -   `finishedRows` : ダンプされた行の数。
            -   `estimateTotalRows` : ダンプされる推定行数。
            -   `progress` : ダンププロセスの進行状況。
            -   `bps` : ダンプ速度 (バイト/秒)。

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
