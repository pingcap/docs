---
title: Handle Failed DDL Statements in TiDB Data Migration
summary: TiDB データ移行ツールを使用してデータを移行するときに、失敗した DDL ステートメントを処理する方法を学習します。
---

# TiDB データ移行で失敗した DDL ステートメントを処理する {#handle-failed-ddl-statements-in-tidb-data-migration}

このドキュメントでは、TiDB データ移行 (DM) ツールを使用してデータを移行するときに、失敗した DDL ステートメントを処理する方法について説明します。

現在、TiDBはMySQLのすべての構文と完全に互換性があるわけではありません（ [TiDBでサポートされているDDL文](/mysql-compatibility.md#ddl-operations)参照）。そのため、DMがMySQLからTiDBにデータを移行する際に、TiDBが対応するDDL文をサポートしていない場合、エラーが発生し、移行プロセスが中断される可能性があります。この場合、DMの`binlog`コマンドを使用して移行を再開できます。

## 制限 {#restrictions}

次の状況ではこのコマンドを使用しないでください。

-   実際の本番環境では、失敗した DDL ステートメントが下流の TiDB でスキップされることは許容されません。
-   失敗した DDL ステートメントを他の DDL ステートメントに置き換えることはできません。
-   その他の DDL ステートメントをダウンストリーム TiDB に挿入してはなりません。

たとえば、 `DROP PRIMARY KEY` 。このシナリオでは、新しいテーブル スキーマを使用してダウンストリームに新しいテーブルを作成し (DDL ステートメントを実行した後)、すべてのデータをこの新しいテーブルに再インポートすることしかできません。

## サポートされているシナリオ {#supported-scenarios}

移行中に、TiDB でサポートされていない DDL ステートメントがアップストリームで実行され、ダウンストリームに移行され、その結果、移行タスクが中断されます。

-   この DDL ステートメントがダウンストリーム TiDB でスキップされることが許容される場合は、 `binlog skip <task-name>`使用してこの DDL ステートメントの移行をスキップし、移行を再開できます。
-   この DDL ステートメントを他の DDL ステートメントに置き換えても問題ない場合は、 `binlog replace <task-name>`使用してこの DDL ステートメントを置き換え、移行を再開できます。
-   他の DDL ステートメントがダウンストリーム TiDB に挿入されることが許容される場合は、 `binlog inject <task-name>`使用して他の DDL ステートメントを挿入し、移行を再開できます。

## コマンド {#commands}

dmctl を使用して失敗した DDL ステートメントを手動で処理する場合、よく使用されるコマンドには`query-status`と`binlog`含まれます。

### クエリステータス {#query-status}

`query-status`コマンドは、各 MySQL インスタンス内のサブタスクやリレーユニットなどの現在の状態を問い合わせるために使用されます。詳細については、 [クエリステータス](/dm/dm-query-status.md)参照してください。

### binlog {#binlog}

`binlog`コマンドは、 binlog操作の管理と表示に使用されます。このコマンドは DM v6.0 以降のバージョンでのみサポートされています。それ以前のバージョンでは、 `handle-error`コマンドを使用してください。

`binlog`の使い方は次のとおりです。

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

-   `inject` : 現在のエラーイベントまたは特定のbinlog位置にDDL文を挿入します。binlog位置の指定については、 `-b, --binlog-pos`を参照してください。
-   `list` : 現在のbinlog位置、または現在のbinlog位置以降の有効な`inject` 、 `skip` 、 `replace`各操作をすべてリストします。binlog位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `replace` : 特定のbinlog位置にあるDDL文を別のDDL文に置き換えます。binlog位置の指定については、 `-b, --binlog-pos`を参照してください。
-   `revert` : 指定されたbinlog操作において、前の操作が無効であった場合にのみ、 `inject` 、または`replace` `skip`を元に戻します。binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `skip` : 特定のbinlog位置にあるDDL文をスキップします。binlog位置の指定については、 `-b, --binlog-pos`を参照してください。

`binlog`次のフラグをサポートします:

-   `-b, --binlog-pos` :
    -   タイプ: 文字列。
    -   binlogの位置を指定します。binlogイベントの位置が`binlog-pos`一致すると、操作が実行されます。指定されていない場合、DM は現在失敗した DDL 文に`binlog-pos`自動的に設定します。
    -   形式: `binlog-filename:binlog-pos` 、たとえば`mysql-bin|000001.000003:3270` 。
    -   マイグレーションがエラーを返した後は、 `query-status`で返される`startLocation`の`position`からbinlogの位置を取得できます。マイグレーションがエラーを返す前は、上流の MySQL インスタンスで[`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)を使用してbinlogの位置を取得できます。

-   `-s, --source` :
    -   タイプ: 文字列。
    -   事前設定された操作を実行する MySQL インスタンスを指定します。

## 使用例 {#usage-examples}

### 移行が中断された場合はDDLをスキップする {#skip-ddl-if-the-migration-gets-interrupted}

移行が中断されたときに DDL ステートメントをスキップする必要がある場合は、 `binlog skip`コマンドを実行します。

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

#### シャードマージなしのシナリオ {#non-shard-merge-scenario}

上流のテーブル`db1.tbl1`下流のTiDBに移行する必要があると仮定します。初期のテーブルスキーマは次のとおりです。

```sql
SHOW CREATE TABLE db1.tbl1;
```

```sql
+-------+--------------------------------------------------+
| Table | Create Table                                     |
+-------+--------------------------------------------------+
| tbl1  | CREATE TABLE `tbl1` (
  `c1` int NOT NULL,
  `c2` decimal(11,3) DEFAULT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+-------+--------------------------------------------------+
```

ここで、アップストリームで次の DDL ステートメントが実行され、テーブル スキーマが変更されます (つまり、c2 の DECIMAL(11, 3) が DECIMAL(10, 3) に変更されます)。

```sql
ALTER TABLE db1.tbl1 CHANGE c2 c2 DECIMAL (10, 3);
```

このDDL文はTiDBでサポートされていないため、DMの移行タスクは中断されます。コマンド`query-status <task-name>`を実行すると、次のエラーが表示されます。

    ERROR 8200 (HY000): Unsupported modify column: can't change decimal column precision

実際の本番環境では、このDDL文が下流のTiDBで実行されない（つまり、元のテーブルスキーマが保持される）ことが許容されると仮定します。その場合、 `binlog skip <task-name>`使用してこのDDL文をスキップし、移行を再開できます。手順は以下のとおりです。

1.  `binlog skip <task-name>`実行して、現在失敗している DDL ステートメントをスキップします。

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

2.  タスクのステータスを表示するには、 `query-status <task-name>`実行します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を確認します。</summary>

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

アップストリームにある以下の4つのテーブルを、ダウンストリームにある同じテーブル`` `shard_db`.`shard_table` ``にマージして移行する必要があると仮定します。タスクモードは「悲観的」です。

-   MySQL インスタンス 1 には、 `shard_table_1`と`shard_table_2`テーブルを含む`shard_db_1`スキーマが含まれています。
-   MySQL インスタンス 2 には、 `shard_table_1`と`shard_table_2`テーブルを含む`shard_db_2`スキーマが含まれています。

初期のテーブル スキーマは次のとおりです。

```sql
SHOW CREATE TABLE shard_db.shard_table;
```

```sql
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `shard_table` (
  `id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

次に、すべてのアップストリーム シャード テーブルに対して次の DDL ステートメントを実行して、文字セットを変更します。

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` CHARACTER SET LATIN1 COLLATE LATIN1_DANISH_CI;
```

このDDL文はTiDBでサポートされていないため、DMの移行タスクは中断されます。コマンド`query-status` `shard_db_1`実行すると、MySQLインスタンス1のテーブル`shard_table_1`とMySQLインスタンス`shard_table_1` `shard_db_2`以下のエラーが報告されます。

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }

<!---->

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }

実際の本番環境では、このDDL文が下流のTiDBで実行されない（つまり、元のテーブルスキーマが保持される）ことが許容されると仮定します。その場合、 `binlog skip <task-name>`使用してこのDDL文をスキップし、移行を再開できます。手順は以下のとおりです。

1.  `binlog skip <task-name>`実行して、MySQL インスタンス 1 と 2 で現在失敗している DDL ステートメントをスキップします。

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

2.  `query-status`コマンドを実行すると、MySQL インスタンス 1 の`shard_db_1` `shard_table_2`と MySQL インスタンス 2 `shard_table_2` `shard_db_2`によって報告されたエラーを確認できます。

        {
            "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
            "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
        }

    <!---->

        {
            "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
            "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
        }

3.  `binlog skip <task-name>`再度実行して、MySQL インスタンス 1 と 2 で現在失敗している DDL ステートメントをスキップします。

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

4.  タスクのステータスを表示するには`query-status <task-name>`使用します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を確認します。</summary>

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

    タスクはエラーなしで正常に実行され、4 つの間違った DDL ステートメントはすべてスキップされていることがわかります。

### 移行が中断された場合はDDLを置き換える {#replace-ddl-if-the-migration-gets-interrupted}

移行が中断されたときに DDL ステートメントを置き換える必要がある場合は、 `binlog replace`コマンドを実行します。

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

#### シャードマージなしのシナリオ {#non-shard-merge-scenario}

上流のテーブル`db1.tbl1`下流のTiDBに移行する必要があると仮定します。初期のテーブルスキーマは次のとおりです。

```sql
SHOW CREATE TABLE db1.tbl1;
```

```SQL
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `tbl1` (
  `id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

次に、アップストリームで次の DDL 操作を実行して、UNIQUE 制約を持つ新しい列を追加します。

```sql
ALTER TABLE `db1`.`tbl1` ADD COLUMN new_col INT UNIQUE;
```

このDDL文はTiDBでサポートされていないため、移行タスクは中断されます。コマンド`query-status`を実行すると、次のエラーが表示されます。

    {
        "Message": "cannot track DDL: ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT UNIQUE KEY",
        "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'db1.tbl1'",
    }

このDDL文を2つの同等のDDL文に置き換えることができます。手順は次のとおりです。

1.  間違った DDL ステートメントを次のコマンドで置き換えます。

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

2.  タスクのステータスを表示するには`query-status <task-name>`使用します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を確認します。</summary>

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

    タスクが正常に実行され、間違った DDL ステートメントが正常に実行される新しい DDL ステートメントに置き換えられていることがわかります。

#### シャードマージシナリオ {#shard-merge-scenario}

アップストリームにある以下の4つのテーブルを、ダウンストリームにある同じテーブル`` `shard_db`.`shard_table` ``にマージして移行する必要があると仮定します。タスクモードは「悲観的」です。

-   MySQL インスタンス 1 にはスキーマ`shard_db_1`があり、そこには`shard_table_1`と`shard_table_2` 2 つのテーブルがあります。
-   MySQL インスタンス 2 にはスキーマ`shard_db_2`があり、そこには`shard_table_1`と`shard_table_2` 2 つのテーブルがあります。

初期のテーブル スキーマは次のとおりです。

```sql
SHOW CREATE TABLE shard_db.shard_table;
```

```sql
+-------+-----------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                              |
+-------+-----------------------------------------------------------------------------------------------------------+
| tb    | CREATE TABLE `shard_table` (
  `id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
+-------+-----------------------------------------------------------------------------------------------------------+
```

次に、すべてのアップストリーム シャード テーブルに対して次の DDL 操作を実行し、UNIQUE 制約を持つ新しい列を追加します。

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` ADD COLUMN new_col INT UNIQUE;
```

このDDL文はTiDBでサポートされていないため、移行タスクは中断されます。コマンド`query-status`を実行すると、MySQLインスタンス`shard_table_1` `shard_db_1` MySQLインスタンス2のテーブル`shard_db_2`で以下のエラー`shard_table_1`報告されます。

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
        "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_1.shard_table_1'",
    }

<!---->

    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
        "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_2.shard_table_1'",
    }

このDDL文を2つの同等のDDL文に置き換えることができます。手順は次のとおりです。

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

2.  `query-status <task-name>`使用してタスクのステータス`shard_table_2` `shard_db_1` `shard_table_2` `shard_db_2`された次のエラーを確認できます。

        {
            "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_1`.`shard_table_2`], right DDL sequence should be ..."
        }

    <!---->

        {
            "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_2`.`shard_table_2`], right DDL sequence should be ..."
        }

3.  `handle-error <task-name> replace`再度実行して、MySQL インスタンス 1 と 2 の間違った DDL ステートメントを置き換えます。

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

4.  タスクのステータスを表示するには`query-status <task-name>`使用します。

    ```bash
    » query-status test
    ```

    <details><summary>実行結果を確認します。</summary>

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

    タスクはエラーなしで正常に実行され、4 つの誤った DDL ステートメントがすべて置き換えられていることがわかります。

### その他のコマンド {#other-commands}

`binlog`の他のコマンドの使用方法については、上記の`binlog skip`と`binlog replace`例を参照してください。
