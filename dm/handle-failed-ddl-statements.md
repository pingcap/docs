---
title: Handle Failed DDL Statements in TiDB Data Migration
summary: Learn how to handle failed DDL statements when you're using the TiDB Data Migration tool to migrate data.
---

# TiDB データ移行で失敗した DDL ステートメントを処理する {#handle-failed-ddl-statements-in-tidb-data-migration}

このドキュメントでは、TiDB データ移行 (DM) ツールを使用してデータを移行するときに失敗した DDL ステートメントを処理する方法を紹介します。

現在、TiDB はすべての MySQL 構文と完全に互換性があるわけではありません ( [TiDB によってサポートされる DDL ステートメント](/mysql-compatibility.md#ddl-operations)を参照)。したがって、DM が MySQL から TiDB にデータを移行していて、TiDB が対応する DDL ステートメントをサポートしていない場合、エラーが発生して移行プロセスが中断される可能性があります。この場合、DM の`binlog`コマンドを使用して移行を再開できます。

## 制限 {#restrictions}

次の状況ではこのコマンドを使用しないでください。

-   実際の本番環境では、失敗した DDL ステートメントがダウンストリーム TiDB でスキップされることは受け入れられません。
-   失敗した DDL ステートメントを他の DDL ステートメントで置き換えることはできません。
-   他の DDL ステートメントをダウンストリーム TiDB に挿入しないでください。

たとえば、 `DROP PRIMARY KEY` 。このシナリオでは、(DDL ステートメントの実行後) 新しいテーブル スキーマを使用してダウンストリームに新しいテーブルを作成し、すべてのデータをこの新しいテーブルに再インポートすることのみが可能です。

## サポートされているシナリオ {#supported-scenarios}

移行中に、TiDB でサポートされていない DDL ステートメントが上流で実行され、下流に移行されるため、移行タスクが中断されます。

-   この DDL ステートメントがダウンストリーム TiDB でスキップされることが許容される場合は、 `binlog skip <task-name>`を使用してこの DDL ステートメントの移行をスキップし、移行を再開できます。
-   この DDL ステートメントが他の DDL ステートメントに置き換えられることが許容される場合は、 `binlog replace <task-name>`を使用してこの DDL ステートメントを置き換え、移行を再開できます。
-   他の DDL ステートメントがダウンストリーム TiDB に挿入されることが許容される場合は、 `binlog inject <task-name>`を使用して他の DDL ステートメントを挿入し、移行を再開できます。

## コマンド {#commands}

dmctl を使用して失敗した DDL ステートメントを手動で処理する場合、一般的に使用されるコマンドには`query-status`と`binlog`があります。

### クエリステータス {#query-status}

`query-status`コマンドは、各 MySQL インスタンスのサブタスクや中継ユニットなどの現在のステータスをクエリするために使用されます。詳細は[クエリステータス](/dm/dm-query-status.md)を参照してください。

### binlog {#binlog}

`binlog`コマンドは、 binlog操作を管理および表示するために使用されます。このコマンドは、DM v6.0 以降のバージョンでのみサポートされます。以前のバージョンの場合は、 `handle-error`コマンドを使用します。

`binlog`の使い方は以下の通りです。

```bash
binlog -h
```

    manage or show binlog operations

    Usage:
      dmctl binlog [command]

    Available Commands:
      inject      inject the current error event or a specific binlog position (binlog-pos) with some ddls
      list        list error handle command at binlog position (binlog-pos) or after binlog position (binlog-pos)
      replace     replace the current error event or a specific binlog position (binlog-pos) with some ddls
      revert      revert the current binlog operation or a specific binlog position (binlog-pos) operation
      skip        skip the current error event or a specific binlog position (binlog-pos) event

    Flags:
      -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
      -h, --help                help for binlog

    Global Flags:
      -s, --source strings   MySQL Source ID.

    Use "dmctl binlog [command] --help" for more information about a command.

`binlog`次のサブコマンドをサポートします。

-   `inject` : DDL ステートメントを現在のエラー イベントまたは特定のbinlog位置に挿入します。binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `list` : 現在のbinlog位置または現在のbinlog位置以降の有効な`inject` 、 `skip` 、および`replace`の操作をすべてリストします。binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `replace` : 特定のbinlog位置の DDL ステートメントを別の DDL ステートメントに置き換えます。binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `revert` : 前の操作が有効でない場合にのみ、指定されたbinlog操作で`inject` 、 `skip` 、または`replace`操作を元に戻します。binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `skip` : 特定のbinlog位置で DDL ステートメントをスキップします。binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。

`binlog`次のフラグをサポートします。

-   `-b, --binlog-pos` :
    -   タイプ: 文字列。
    -   binlogの位置を指定します。 binlogイベントの位置が`binlog-pos`一致すると、操作が実行されます。これが指定されていない場合、DM は現在失敗した DDL ステートメントに自動的に`binlog-pos`設定します。
    -   形式: `binlog-filename:binlog-pos` 、たとえば`mysql-bin|000001.000003:3270` 。
    -   移行がエラーを返した後、 `query-status`によって返された`startLocation`分の`position`からbinlogの位置を取得できます。移行でエラーが返される前に、上流の MySQL インスタンスで[`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)を使用してbinlogの位置を取得できます。

-   `-s, --source` :
    -   タイプ: 文字列。
    -   プリセット操作を実行する MySQL インスタンスを指定します。

## 使用例 {#usage-examples}

### 移行が中断された場合は DDL をスキップする {#skip-ddl-if-the-migration-gets-interrupted}

移行が中断されたときに DDL ステートメントをスキップする必要がある場合は、次の`binlog skip`コマンドを実行します。

```bash
binlog skip -h
```

    skip the current error event or a specific binlog position (binlog-pos) event

    Usage:
      dmctl binlog skip <task-name> [flags]

    Flags:
      -h, --help   help for skip

    Global Flags:
      -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
      -s, --source strings      MySQL Source ID.

#### 非シャードマージシナリオ {#non-shard-merge-scenario}

アップストリーム テーブル`db1.tbl1`をダウンストリーム TiDB に移行する必要があると仮定します。初期テーブルのスキーマは次のとおりです。

```sql
SHOW CREATE TABLE db1.tbl1;
```

```sql
+-------+--------------------------------------------------+
| Table | Create Table                                     |
+-------+--------------------------------------------------+
| tbl1  | CREATE TABLE `tbl1` (
  `c1` int(11) NOT NULL,
  `c2` decimal(11,3) DEFAULT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+--------------------------------------------------+
```

ここで、次の DDL ステートメントがアップストリームで実行され、テーブル スキーマが変更されます (つまり、c2 の DECIMAL(11, 3) が DECIMAL(10, 3) に変更されます)。

```sql
ALTER TABLE db1.tbl1 CHANGE c2 c2 DECIMAL (10, 3);
```

この DDL ステートメントは TiDB でサポートされていないため、DM の移行タスクは中断されます。 `query-status <task-name>`コマンドを実行すると、次のエラーが表示されます。

    ERROR 8200 (HY000): Unsupported modify column: can't change decimal column precision

実際の本番環境では、この DDL ステートメントがダウンストリーム TiDB で実行されない (つまり、元のテーブル スキーマが保持される) ことが許容されると想定します。その後、 `binlog skip <task-name>`を使用してこの DDL ステートメントをスキップし、移行を再開できます。手順は次のとおりです。

1.  現在失敗している DDL ステートメントをスキップするには、 `binlog skip <task-name>`を実行します。

    ```bash
    » binlog skip test
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

2.  `query-status <task-name>`を実行してタスクのステータスを表示します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を参照してください。</summary>

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
                            "unresolvedDDLLockID": "",
                            "sync": {
                                "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                                "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                                "blockingDDLs": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "synced": true,
                                "binlogType": "remote",
                                "totalRows": "4",
                                "totalRps": "0",
                                "recentRps": "0"
                            }
                        }
                    ]
                }
            ]
        }

    </details>

    タスクが正常に実行され、間違った DDL がスキップされていることがわかります。

#### シャードマージシナリオ {#shard-merge-scenario}

アップストリームの次の 4 つのテーブルをマージして、ダウンストリームの 1 つの同じテーブル`` `shard_db`.`shard_table` ``に移行する必要があるとします。タスクモードは「悲観的」です。

-   MySQL インスタンス 1 には、 `shard_table_1`と`shard_table_2`テーブルを含む`shard_db_1`スキーマが含まれています。
-   MySQL インスタンス 2 には、 `shard_table_1`と`shard_table_2`テーブルを含む`shard_db_2`スキーマが含まれています。

初期テーブルのスキーマは次のとおりです。

```sql
SHOW CREATE TABLE shard_db.shard_table;
```

```sql
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `shard_table` (
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

ここで、上流のすべてのシャードテーブルに対して次の DDL ステートメントを実行して、文字セットを変更します。

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` CHARACTER SET LATIN1 COLLATE LATIN1_DANISH_CI;
```

この DDL ステートメントは TiDB でサポートされていないため、DM の移行タスクは中断されます。 `query-status`コマンドを実行すると、 `shard_db_1`によって報告される次のエラーが表示されます。 `shard_table_1` MySQL インスタンスのテーブル 1 と`shard_db_2` 。 `shard_table_1` MySQL インスタンス 2 のテーブル:

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }

<!---->

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }

実際の本番環境では、この DDL ステートメントがダウンストリーム TiDB で実行されない (つまり、元のテーブル スキーマが保持される) ことが許容されると想定します。その後、 `binlog skip <task-name>`を使用してこの DDL ステートメントをスキップし、移行を再開できます。手順は次のとおりです。

1.  `binlog skip <task-name>`を実行して、MySQL インスタンス 1 および 2 で現在失敗している DDL ステートメントをスキップします。

    ```bash
    » binlog skip test
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
                },
                {
                    "result": true,
                    "msg": "",
                    "source": "mysql-replica-02",
                    "worker": "worker2"
                }
            ]
        }

2.  `query-status`コマンドを実行すると、 `shard_db_1`によって報告されたエラーが表示されます。 `shard_table_2` MySQL インスタンスのテーブル 1 と`shard_db_2` 。 `shard_table_2` MySQL インスタンス 2 のテーブル:

        {
            "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
            "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
        }

    <!---->

        {
            "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
            "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
        }

3.  `binlog skip <task-name>`を再度実行して、MySQL インスタンス 1 および 2 で現在失敗している DDL ステートメントをスキップします。

    ```bash
    » handle-error test skip
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
                },
                {
                    "result": true,
                    "msg": "",
                    "source": "mysql-replica-02",
                    "worker": "worker2"
                }
            ]
        }

4.  タスクのステータスを表示するには`query-status <task-name>`を使用します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を参照してください。</summary>

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
                            "unresolvedDDLLockID": "",
                            "sync": {
                                "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                                "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                                "blockingDDLs": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "synced": true,
                                "binlogType": "remote",
                                "totalRows": "4",
                                "totalRps": "0",
                                "recentRps": "0"
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
                            "unit": "Sync",
                            "result": null,
                            "unresolvedDDLLockID": "",
                            "sync": {
                                "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                                "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                                "blockingDDLs": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "synced": true,
                                "binlogType": "remote",
                                "totalRows": "4",
                                "totalRps": "0",
                                "recentRps": "0"
                            }
                        }
                    ]
                }
            ]
        }

    </details>

    タスクがエラーなしで正常に実行され、4 つの間違った DDL ステートメントがすべてスキップされていることがわかります。

### 移行が中断された場合は DDL を置き換えます {#replace-ddl-if-the-migration-gets-interrupted}

移行が中断されたときに DDL ステートメントを置き換える必要がある場合は、次のコマンド`binlog replace`を実行します。

```bash
binlog replace -h
```

    replace the current error event or a specific binlog position (binlog-pos) with some ddls

    Usage:
      dmctl binlog replace <task-name> <replace-sql1> <replace-sql2>... [flags]

    Flags:
      -h, --help   help for replace

    Global Flags:
      -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
      -s, --source strings      MySQL Source ID.

#### 非シャードマージシナリオ {#non-shard-merge-scenario}

アップストリーム テーブル`db1.tbl1`をダウンストリーム TiDB に移行する必要があると仮定します。初期テーブルのスキーマは次のとおりです。

```sql
SHOW CREATE TABLE db1.tbl1;
```

```SQL
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `tbl1` (
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

ここで、アップストリームで次の DDL 操作を実行して、UNIQUE 制約を持つ新しい列を追加します。

```sql
ALTER TABLE `db1`.`tbl1` ADD COLUMN new_col INT UNIQUE;
```

この DDL ステートメントは TiDB でサポートされていないため、移行タスクは中断されます。 `query-status`コマンドを実行すると、次のエラーが表示されます。

    {
        "Message": "cannot track DDL: ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT UNIQUE KEY",
        "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'db1.tbl1'",
    }

この DDL ステートメントは、2 つの同等の DDL ステートメントに置き換えることができます。手順は次のとおりです。

1.  間違った DDL ステートメントを次のコマンドに置き換えます。

    ```bash
    » binlog replace test "ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT;ALTER TABLE `db1`.`tbl1` ADD UNIQUE(`new_col`)";
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

2.  タスクのステータスを表示するには`query-status <task-name>`を使用します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を参照してください。</summary>

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
                            "unresolvedDDLLockID": "",
                            "sync": {
                                "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                                "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                                "blockingDDLs": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "synced": true,
                                "binlogType": "remote",
                                "totalRows": "4",
                                "totalRps": "0",
                                "recentRps": "0"
                            }
                        }
                    ]
                }
            ]
        }

    </details>

    タスクが正常に実行され、間違った DDL ステートメントが新しい DDL ステートメントに置き換えられ、正常に実行されることがわかります。

#### シャードマージシナリオ {#shard-merge-scenario}

アップストリームの次の 4 つのテーブルをマージして、ダウンストリームの 1 つの同じテーブル`` `shard_db`.`shard_table` ``に移行する必要があるとします。タスクモードは「悲観的」です。

-   MySQL インスタンス 1 には、2 つのテーブル`shard_table_1`および`shard_table_2`を持つスキーマ`shard_db_1`があります。
-   MySQL インスタンス 2 には、2 つのテーブル`shard_table_1`および`shard_table_2`を持つスキーマ`shard_db_2`があります。

初期テーブルのスキーマは次のとおりです。

```sql
SHOW CREATE TABLE shard_db.shard_table;
```

```sql
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `shard_table` (
  `id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

ここで、上流のすべてのシャードテーブルに対して次の DDL 操作を実行して、UNIQUE 制約を持つ新しい列を追加します。

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` ADD COLUMN new_col INT UNIQUE;
```

この DDL ステートメントは TiDB でサポートされていないため、移行タスクは中断されます。 `query-status`コマンドを実行すると、 `shard_db_1`によって報告される次のエラーが表示されます。 `shard_table_1` MySQL インスタンスのテーブル 1 と`shard_db_2` 。 `shard_table_1` MySQL インスタンス 2 のテーブル:

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
        "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_1.shard_table_1'",
    }

<!---->

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
        "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_2.shard_table_1'",
    }

この DDL ステートメントは、2 つの同等の DDL ステートメントに置き換えることができます。手順は次のとおりです。

1.  次のコマンドを使用して、MySQL インスタンス 1 と MySQL インスタンス 2 の間違った DDL ステートメントをそれぞれ置き換えます。

    ```bash
    » binlog replace test -s mysql-replica-01 "ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_1`.`shard_table_1` ADD UNIQUE(`new_col`)";
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

    ```bash
    » binlog replace test -s mysql-replica-02 "ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_2`.`shard_table_1` ADD UNIQUE(`new_col`)";
    ```

        {
            "result": true,
            "msg": "",
            "sources": [
                {
                    "result": true,
                    "msg": "",
                    "source": "mysql-replica-02",
                    "worker": "worker2"
                }
            ]
        }

2.  `query-status <task-name>`を使用してタスクのステータスを表示すると、 `shard_db_1`によって報告される次のエラーが表示されます。 `shard_table_2` MySQL インスタンスのテーブル 1 と`shard_db_2` 。 `shard_table_2` MySQL インスタンス 2 のテーブル:

        {
            "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_1`.`shard_table_2`], right DDL sequence should be ..."
        }

    <!---->

        {
            "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_2`.`shard_table_2`], right DDL sequence should be ..."
        }

3.  `handle-error <task-name> replace`を再度実行して、MySQL インスタンス 1 および 2 の間違った DDL ステートメントを置き換えます。

    ```bash
    » binlog replace test -s mysql-replica-01 "ALTER TABLE `shard_db_1`.`shard_table_2` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_1`.`shard_table_2` ADD UNIQUE(`new_col`)";
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

    ```bash
    » binlog replace test -s mysql-replica-02 "ALTER TABLE `shard_db_2`.`shard_table_2` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_2`.`shard_table_2` ADD UNIQUE(`new_col`)";
    ```

        {
            "result": true,
            "msg": "",
            "sources": [
                {
                    "result": true,
                    "msg": "",
                    "source": "mysql-replica-02",
                    "worker": "worker2"
                }
            ]
        }

4.  タスクのステータスを表示するには`query-status <task-name>`を使用します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を参照してください。</summary>

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
                            "unresolvedDDLLockID": "",
                            "sync": {
                                "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                                "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                                "blockingDDLs": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "synced": true,
                                "binlogType": "remote",
                                "totalRows": "4",
                                "totalRps": "0",
                                "recentRps": "0"
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
                            "unit": "Sync",
                            "result": null,
                            "unresolvedDDLLockID": "",
                            "sync": {
                                "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                                "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                                "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                                "blockingDDLs": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "unresolvedGroups": [
                                ],
                                "synced": try,
                                "binlogType": "remote",
                                "totalRows": "4",
                                "totalRps": "0",
                                "recentRps": "0"
                            }
                        }
                    ]
                }
            ]
        }

    </details>

    タスクがエラーなしで正常に実行され、4 つの間違った DDL ステートメントがすべて置き換えられていることがわかります。

### その他のコマンド {#other-commands}

`binlog`の他のコマンドの使用方法については、上記の`binlog skip`と`binlog replace`例を参照してください。
