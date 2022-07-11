---
title: Handle Failed DDL Statements
summary: Learn how to handle failed DDL statements when you're using the TiDB Data Migration tool to migrate data.
---

# 失敗したDDLステートメントの処理 {#handle-failed-ddl-statements}

このドキュメントでは、TiDBデータ移行（DM）ツールを使用してデータを移行するときに失敗したDDLステートメントを処理する方法を紹介します。

現在、TiDBはすべてのMySQL構文と完全に互換性があるわけではありません（ [TiDBでサポートされているDDLステートメント](/mysql-compatibility.md#ddl)を参照）。したがって、DMがMySQLからTiDBにデータを移行していて、TiDBが対応するDDLステートメントをサポートしていない場合、エラーが発生して移行プロセスが中断する可能性があります。この場合、DMの`binlog`コマンドを使用して移行を再開できます。

## 制限 {#restrictions}

次の状況では、このコマンドを使用しないでください。

-   実際の実稼働環境では、失敗したDDLステートメントがダウンストリームTiDBでスキップされることは受け入れられません。
-   失敗したDDLステートメントを他のDDLステートメントで置き換えることはできません。
-   他のDDLステートメントをダウンストリームTiDBに挿入しないでください。

たとえば、 `DROP PRIMARY KEY` 。このシナリオでは、（DDLステートメントの実行後に）新しいテーブルスキーマを使用してダウンストリームに新しいテーブルを作成し、すべてのデータをこの新しいテーブルに再インポートすることしかできません。

## サポートされているシナリオ {#supported-scenarios}

移行中、TiDBでサポートされていないDDLステートメントがアップストリームで実行され、ダウンストリームに移行されます。その結果、移行タスクが中断されます。

-   このDDLステートメントがダウンストリームTiDBでスキップされることが許容される場合は、 `binlog skip <task-name>`を使用して、このDDLステートメントの移行をスキップし、移行を再開できます。
-   このDDLステートメントが他のDDLステートメントに置き換えられることが許容される場合は、 `binlog replace <task-name>`を使用してこのDDLステートメントを置き換え、移行を再開できます。
-   他のDDLステートメントがダウンストリームTiDBに挿入されることが許容される場合は、 `binlog inject <task-name>`を使用して他のDDLステートメントを挿入し、移行を再開できます。

## コマンド {#commands}

dmctlを使用して失敗したDDLステートメントを手動で処理する場合、一般的に使用されるコマンドには`query-status`と`binlog`が含まれます。

### クエリステータス {#query-status}

`query-status`コマンドは、各MySQLインスタンスのサブタスクやリレーユニットなどのアイテムの現在のステータスを照会するために使用されます。詳細については、 [クエリステータス](/dm/dm-query-status.md)を参照してください。

### binlog {#binlog}

`binlog`コマンドは、binlog操作を管理および表示するために使用されます。このコマンドは、DMv6.0以降のバージョンでのみサポートされています。以前のバージョンでは、 `handle-error`コマンドを使用します。

`binlog`の使用法は次のとおりです。

```bash
binlog -h
```

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
```

`binlog`は、次のサブコマンドをサポートします。

-   `inject` ：現在のエラーイベントまたは特定のbinlog位置にDDLステートメントを挿入します。 binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `list` ：現在のbinlog位置または現在のbinlog位置の後のすべての有効な`inject` 、および`skip`操作をリストし`replace` 。 binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `replace` ：特定のbinlog位置にあるDDLステートメントを別のDDLステートメントに置き換えます。 binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `revert` ：前の操作が有効にならない場合にのみ、指定された`replace` `inject` `skip`を元に戻します。 binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。
-   `skip` ：特定のbinlog位置でDDLステートメントをスキップします。 binlogの位置を指定するには、 `-b, --binlog-pos`を参照してください。

`binlog`は、次のフラグをサポートします。

-   `-b, --binlog-pos` ：
    -   タイプ：文字列。
    -   binlogの位置を指定します。 binlogイベントの位置が`binlog-pos`に一致すると、操作が実行されます。指定されていない場合、DMは自動的に`binlog-pos`を現在失敗しているDDLステートメントに設定します。
    -   形式： `binlog-filename:binlog-pos` 、たとえば`mysql-bin|000001.000003:3270` 。
    -   移行でエラーが返された後、binlogの位置は`query-status`で返された`startLocation`の`position`から取得できます。移行でエラーが返される前に、アップストリームのMySQLインスタンスで[`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/5.7/en/show-binlog-events.html)を使用してbinlogの位置を取得できます。

-   `-s, --source` ：
    -   タイプ：文字列。
    -   プリセット操作を実行するMySQLインスタンスを指定します。

## 使用例 {#usage-examples}

### 移行が中断された場合はDDLをスキップします {#skip-ddl-if-the-migration-gets-interrupted}

移行が中断されたときにDDLステートメントをスキップする必要がある場合は、次の`binlog skip`コマンドを実行します。

```bash
binlog skip -h
```

```
skip the current error event or a specific binlog position (binlog-pos) event

Usage:
  dmctl binlog skip <task-name> [flags]

Flags:
  -h, --help   help for skip

Global Flags:
  -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
  -s, --source strings      MySQL Source ID.
```

#### 非シャードマージシナリオ {#non-shard-merge-scenario}

アップストリームテーブル`db1.tbl1`をダウンストリームTiDBに移行する必要があると想定します。初期テーブルスキーマは次のとおりです。

{{< copyable "" >}}

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

ここで、次のDDLステートメントがアップストリームで実行され、テーブルスキーマが変更されます（つまり、c2のDECIMAL（11、3）がDECIMAL（10、3）に変更されます）。

{{< copyable "" >}}

```sql
ALTER TABLE db1.tbl1 CHANGE c2 c2 DECIMAL (10, 3);
```

このDDLステートメントはTiDBでサポートされていないため、DMの移行タスクが中断されます。 `query-status <task-name>`コマンドを実行すると、次のエラーが表示されます。

```
ERROR 8200 (HY000): Unsupported modify column: can't change decimal column precision
```

実際の実稼働環境では、このDDLステートメントがダウンストリームTiDBで実行されない（つまり、元のテーブルスキーマが保持される）ことが許容できると想定します。次に、 `binlog skip <task-name>`を使用してこのDDLステートメントをスキップし、移行を再開できます。手順は次のとおりです。

1.  `binlog skip <task-name>`を実行して、現在失敗しているDDLステートメントをスキップします。

    {{< copyable "" >}}

    ```bash
    » binlog skip test
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

2.  `query-status <task-name>`を実行して、タスクのステータスを表示します。

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary>実行結果をご覧ください。</summary>

    ```
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
                            "totalEvents": "4",
                            "totalTps": "0",
                            "recentTps": "0",
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    タスクが正常に実行され、間違ったDDLがスキップされていることがわかります。

#### シャードマージシナリオ {#shard-merge-scenario}

アップストリームの次の4つのテーブルを、ダウンストリームの1つの同じテーブル`` `shard_db`.`shard_table` ``にマージして移行する必要があると想定します。タスクモードは「悲観的」です。

-   MySQLインスタンス1には、 `shard_table_1`つと`shard_table_2`のテーブルを含む`shard_db_1`のスキーマが含まれています。
-   MySQLインスタンス2には、 `shard_table_1`つと`shard_table_2`のテーブルを含む`shard_db_2`のスキーマが含まれています。

初期テーブルスキーマは次のとおりです。

{{< copyable "" >}}

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

次に、すべてのアップストリームシャードテーブルに対して次のDDLステートメントを実行して、文字セットを変更します。

{{< copyable "" >}}

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` CHARACTER SET LATIN1 COLLATE LATIN1_DANISH_CI;
```

このDDLステートメントはTiDBでサポートされていないため、DMの移行タスクが中断されます。 `query-status`コマンドを実行すると、 `shard_db_1`によって報告された次のエラーが表示されます。 MySQLインスタンス1および`shard_db_2`の`shard_table_1`テーブル。 MySQLインスタンス2の`shard_table_1`テーブル：

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
    "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
}
```

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
    "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
}
```

実際の実稼働環境では、このDDLステートメントがダウンストリームTiDBで実行されない（つまり、元のテーブルスキーマが保持される）ことが許容できると想定します。次に、 `binlog skip <task-name>`を使用してこのDDLステートメントをスキップし、移行を再開できます。手順は次のとおりです。

1.  `binlog skip <task-name>`を実行して、MySQLインスタンス1および2で現在失敗しているDDLステートメントをスキップします。

    {{< copyable "" >}}

    ```bash
    » binlog skip test
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
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

2.  `query-status`コマンドを実行すると、 `shard_db_1`によって報告されたエラーを確認できます。 MySQLインスタンス1および`shard_db_2`の`shard_table_2`テーブル。 MySQLインスタンス2の`shard_table_2`テーブル：

    ```
    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }
    ```

    ```
    {
        "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_2` CHARACTER SET UTF8 COLLATE UTF8_UNICODE_CI",
        "RawCause": "[ddl:8200]Unsupported modify charset from latin1 to utf8"
    }
    ```

3.  MySQLインスタンス1および2で現在失敗しているDDLステートメントをスキップするには、もう一度`binlog skip <task-name>`を実行します。

    {{< copyable "" >}}

    ```bash
    » handle-error test skip
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
            },
            {
                "result": true,
                "msg": "",
                "source": "mysql-replica-02",
                "worker": "worker2"
            }
        ]
    }
    ```

4.  `query-status <task-name>`を使用して、タスクのステータスを表示します。

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary>実行結果をご覧ください。</summary>

    ```
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
                            "totalEvents": "4",
                            "totalTps": "0",
                            "recentTps": "0",
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote"
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
                            "totalEvents": "4",
                            "totalTps": "0",
                            "recentTps": "0",
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    タスクがエラーなしで正常に実行され、4つの間違ったDDLステートメントがすべてスキップされていることがわかります。

### 移行が中断された場合は、DDLを置き換えます {#replace-ddl-if-the-migration-gets-interrupted}

移行が中断されたときにDDLステートメントを置き換える必要がある場合は、次の`binlog replace`コマンドを実行します。

```bash
binlog replace -h
```

```
replace the current error event or a specific binlog position (binlog-pos) with some ddls

Usage:
  dmctl binlog replace <task-name> <replace-sql1> <replace-sql2>... [flags]

Flags:
  -h, --help   help for replace

Global Flags:
  -b, --binlog-pos string   position used to match binlog event if matched the binlog operation will be applied. The format like "mysql-bin|000001.000003:3270"
  -s, --source strings      MySQL Source ID.
```

#### 非シャードマージシナリオ {#non-shard-merge-scenario}

アップストリームテーブル`db1.tbl1`をダウンストリームTiDBに移行する必要があると想定します。初期テーブルスキーマは次のとおりです。

{{< copyable "" >}}

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

次に、アップストリームで次のDDL操作を実行して、UNIQUE制約を持つ新しい列を追加します。

{{< copyable "" >}}

```sql
ALTER TABLE `db1`.`tbl1` ADD COLUMN new_col INT UNIQUE;
```

このDDLステートメントはTiDBでサポートされていないため、移行タスクは中断されます。 `query-status`コマンドを実行すると、次のエラーが表示されます。

```
{
    "Message": "cannot track DDL: ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT UNIQUE KEY",
    "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'db1.tbl1'",
}
```

このDDLステートメントを2つの同等のDDLステートメントに置き換えることができます。手順は次のとおりです。

1.  間違ったDDLステートメントを次のコマンドに置き換えます。

    {{< copyable "" >}}

    ```bash
    » binlog replace test "ALTER TABLE `db1`.`tbl1` ADD COLUMN `new_col` INT;ALTER TABLE `db1`.`tbl1` ADD UNIQUE(`new_col`)";
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

2.  `query-status <task-name>`を使用して、タスクのステータスを表示します。

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary>実行結果をご覧ください。</summary>

    ```
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
                            "totalEvents": "4",
                            "totalTps": "0",
                            "recentTps": "0",
                            "masterBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "masterBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-10",
                            "syncerBinlog": "(DESKTOP-T561TSO-bin.000001, 2388)",
                            "syncerBinlogGtid": "143bdef3-dd4a-11ea-8b00-00155de45f57:1-4",
                            "blockingDDLs": [
                            ],
                            "unresolvedGroups": [
                            ],
                            "synced": true,
                            "binlogType": "remote"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    タスクが正常に実行され、間違ったDDLステートメントが正常に実行される新しいDDLステートメントに置き換えられていることがわかります。

#### シャードマージシナリオ {#shard-merge-scenario}

アップストリームの次の4つのテーブルを、ダウンストリームの1つの同じテーブル`` `shard_db`.`shard_table` ``にマージして移行する必要があると想定します。タスクモードは「悲観的」です。

-   MySQLインスタンス1には、2つのテーブル`shard_table_1`と`shard_table_2`を持つスキーマ`shard_db_1`があります。
-   MySQLインスタンス2には、2つのテーブル`shard_table_1`と`shard_table_2`を持つスキーマ`shard_db_2`があります。

初期テーブルスキーマは次のとおりです。

{{< copyable "" >}}

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

次に、すべてのアップストリームシャードテーブルに対して次のDDL操作を実行して、UNIQUE制約を持つ新しい列を追加します。

{{< copyable "" >}}

```sql
ALTER TABLE `shard_db_*`.`shard_table_*` ADD COLUMN new_col INT UNIQUE;
```

このDDLステートメントはTiDBでサポートされていないため、移行タスクは中断されます。 `query-status`コマンドを実行すると、 `shard_db_1`によって報告された次のエラーが表示されます。 MySQLインスタンス1および`shard_db_2`の`shard_table_1`テーブル。 MySQLインスタンス2の`shard_table_1`テーブル：

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
    "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_1.shard_table_1'",
}
```

```
{
    "Message": "cannot track DDL: ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT UNIQUE KEY",
    "RawCause": "[ddl:8200]unsupported add column 'new_col' constraint UNIQUE KEY when altering 'shard_db_2.shard_table_1'",
}
```

このDDLステートメントを2つの同等のDDLステートメントに置き換えることができます。手順は次のとおりです。

1.  MySQLインスタンス1とMySQLインスタンス2のそれぞれ間違ったDDLステートメントを次のコマンドで置き換えます。

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-01 "ALTER TABLE `shard_db_1`.`shard_table_1` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_1`.`shard_table_1` ADD UNIQUE(`new_col`)";
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

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-02 "ALTER TABLE `shard_db_2`.`shard_table_1` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_2`.`shard_table_1` ADD UNIQUE(`new_col`)";
    ```

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
    ```

2.  `query-status <task-name>`を使用してタスクのステータスを表示すると、 `shard_db_1`によって報告された次のエラーを確認できます。 MySQLインスタンス1および`shard_db_2`の`shard_table_2`テーブル。 MySQLインスタンス2の`shard_table_2`テーブル：

    ```
    {
        "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_1`.`shard_table_2`], right DDL sequence should be ..."
    }
    ```

    ```
    {
        "Message": "detect inconsistent DDL sequence from source ... ddls: [ALTER TABLE `shard_db`.`tb` ADD COLUMN `new_col` INT UNIQUE KEY] source: `shard_db_2`.`shard_table_2`], right DDL sequence should be ..."
    }
    ```

3.  `handle-error <task-name> replace`を再度実行して、MySQLインスタンス1および2の間違ったDDLステートメントを置き換えます。

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-01 "ALTER TABLE `shard_db_1`.`shard_table_2` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_1`.`shard_table_2` ADD UNIQUE(`new_col`)";
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

    {{< copyable "" >}}

    ```bash
    » binlog replace test -s mysql-replica-02 "ALTER TABLE `shard_db_2`.`shard_table_2` ADD COLUMN `new_col` INT;ALTER TABLE `shard_db_2`.`shard_table_2` ADD UNIQUE(`new_col`)";
    ```

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
    ```

4.  `query-status <task-name>`を使用して、タスクのステータスを表示します。

    {{< copyable "" >}}

    ```bash
    » query-status test
    ```

    <details><summary>実行結果をご覧ください。</summary>

    ```
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
                            "totalEvents": "4",
                            "totalTps": "0",
                            "recentTps": "0",
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
                            "binlogType": "remote"
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
                            "totalEvents": "4",
                            "totalTps": "0",
                            "recentTps": "0",
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
                            "binlogType": "remote"
                        }
                    }
                ]
            }
        ]
    }
    ```

    </details>

    タスクがエラーなしで正常に実行され、4つの間違ったDDLステートメントがすべて置き換えられていることがわかります。

### その他のコマンド {#other-commands}

`binlog`の他のコマンドの使用法については、上記の`binlog skip`と`binlog replace`の例を参照してください。
