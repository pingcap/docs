---
title: Handle Sharding DDL Locks Manually in DM
summary: Learn how to handle sharding DDL locks manually in DM.
---

# DMでシャーディングDDLロックを手動で処理する {#handle-sharding-ddl-locks-manually-in-dm}

DMは、シャーディングDDLロックを使用して、操作が正しい順序で実行されるようにします。このロックメカニズムは、ほとんどの場合、シャーディングDDLロックを自動的に解決しますが、一部の異常なシナリオでは、 `shard-ddl-lock`コマンドを使用して異常なDDLロックを手動で処理する必要があります。

> **ノート：**
>
> -   このドキュメントは、ペシミスティックコーディネーションモードでのシャーディングDDLロックの処理にのみ適用されます。
> -   このドキュメントの「コマンドの使用法」セクションのコマンドは、対話型モードです。コマンドラインモードでは、エラーレポートを回避するために、エスケープ文字を追加する必要があります。
> -   コマンドによってもたらされる可能性のある影響を完全に認識していて、それらを受け入れることができる場合を除いて、 `shard-ddl-lock unlock`を使用しないでください。
> -   異常なDDLロックを手動で処理する前に、 [シャードマージの原則](/dm/feature-shard-merge-pessimistic.md#principles)をすでに読んでいることを確認してください。

## 指示 {#command}

### <code>shard-ddl-lock</code> {#code-shard-ddl-lock-code}

このコマンドを使用して、DDLロックを表示し、DMマスターに指定されたDDLロックを解放するように要求できます。このコマンドは、DMv6.0以降でのみサポートされています。以前のバージョンでは、 `show-ddl-locks`および`unlock-ddl-locks`コマンドを使用する必要があります。

```bash
shard-ddl-lock -h
```

```
maintain or show shard-ddl locks information
Usage:
  dmctl shard-ddl-lock [task] [flags]
  dmctl shard-ddl-lock [command]
Available Commands:
  unlock      Unlock un-resolved DDL locks forcely
Flags:
  -h, --help   help for shard-ddl-lock
Global Flags:
  -s, --source strings   MySQL Source ID.
Use "dmctl shard-ddl-lock [command] --help" for more information about a command.
```

#### 引数の説明 {#arguments-description}

-   `shard-ddl-lock [task] [flags]` ：現在のDMマスターのDDLロック情報を表示します。

<!---->

-   `shard-ddl-lock [command]` ：指定されたDDLロックを解放するようにDMマスターに要求します。 `[command]`は値として`unlock`のみを受け入れます。

## 使用例 {#usage-examples}

### <code>shard-ddl-lock [task] [flags]</code> {#code-shard-ddl-lock-task-flags-code}

`shard-ddl-lock [task] [flags]`を使用して、現在のDMマスターのDDLロック情報を表示できます。例えば：

```bash
shard-ddl-lock test
```

<details><summary>期待される出力</summary>

```
{
    "result": true,                                        # The result of the query for the lock information.
    "msg": "",                                             # The additional message for the failure to query the lock information or other descriptive information (for example, the lock task does not exist).
    "locks": [                                             # The existing lock information list.
        {
            "ID": "test-`shard_db`.`shard_table`",         # The lock ID, which is made up of the current task name and the schema/table information corresponding to the DDL.
            "task": "test",                                # The name of the task to which the lock belongs.
            "mode": "pessimistic"                          # The shard DDL mode. Can be set to "pessimistic" or "optimistic".
            "owner": "mysql-replica-01",                   # The owner of the lock (the ID of the first source that encounters this DDL operation in the pessimistic mode), which is always empty in the optimistic mode.
            "DDLs": [                                      # The list of DDL operations corresponding to the lock in the pessimistic mode, which is always empty in the optimistic mode.
                "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` DROP COLUMN `c2`;"
            ],
            "synced": [                                    # The list of sources that have received all sharding DDL events in the corresponding MySQL instance.
                "mysql-replica-01"
            ],
            "unsynced": [                                  # The list of sources that have not yet received all sharding DDL events in the corresponding MySQL instance.
                "mysql-replica-02"
            ]
        }
    ]
}
```

</details>

### <code>shard-ddl-lock unlock</code> {#code-shard-ddl-lock-unlock-code}

このコマンドは、所有者にDDLステートメントの実行を要求し、所有者ではない他のすべてのDMワーカーにDDLステートメントをスキップするように要求し、 `DM-master`のロック情報を削除するなど、指定されたDDLロックのロックを解除するように`DM-master`をアクティブに要求します。

> **ノート：**
>
> 現在、 `shard-ddl-lock unlock`は`pessimistic`モードのロックに対してのみ有効です。

```bash
shard-ddl-lock unlock -h
```

```
Unlock un-resolved DDL locks forcely

Usage:
  dmctl shard-ddl-lock unlock <lock-id> [flags]

Flags:
  -a, --action string     accept skip/exec values which means whether to skip or execute ddls (default "skip")
  -d, --database string   database name of the table
  -f, --force-remove      force to remove DDL lock
  -h, --help              help for unlock
  -o, --owner string      source to replace the default owner
  -t, --table string      table name

Global Flags:
  -s, --source strings   MySQL Source ID.
```

`shard-ddl-lock unlock`は次の引数を受け入れます。

-   `-o, --owner` ：

    -   国旗;ストリング;オプション
    -   指定されていない場合、このコマンドはデフォルトの所有者（ `shard-ddl-lock`の結果の所有者）にDDLステートメントの実行を要求します。指定されている場合、このコマンドはMySQLソース（デフォルトの所有者の代替）にDDLステートメントの実行を要求します。
    -   元の所有者がクラスタから既に削除されていない限り、新しい所有者を指定しないでください。

-   `-f, --force-remove` ：

    -   国旗;ブール値;オプション
    -   指定されていない場合、このコマンドは、所有者がDDLステートメントの実行に成功した場合にのみロック情報を削除します。指定されている場合、このコマンドは、所有者がDDLステートメントの実行に失敗した場合でも、ロック情報を強制的に削除します（これを実行した後は、ロックを再度照会したり操作したりすることはできません）。

-   `lock-id` ：

    -   非フラグ;ストリング;必要
    -   ロックを解除する必要のあるDDLロックのIDを指定します（ `shard-ddl-lock`の結果の`ID` ）。

以下は、 `shard-ddl-lock unlock`コマンドの例です。

{{< copyable "" >}}

```bash
shard-ddl-lock unlock test-`shard_db`.`shard_table`
```

```
{
    "result": true,                                        # The result of the unlocking operation.
    "msg": "",                                             # The additional message for the failure to unlock the lock.
}
```

## サポートされているシナリオ {#supported-scenarios}

現在、 `shard-ddl-lock unlock`コマンドは、次の2つの異常なシナリオでのシャーディングDDLロックの処理のみをサポートしています。

### シナリオ1：一部のMySQLソースが削除されます {#scenario-1-some-mysql-sources-are-removed}

#### 異常なロックの理由 {#the-reason-for-the-abnormal-lock}

`DM-master`がシャーディングDDLロックのロックを自動的に解除しようとする前に、すべてのMySQLソースがシャーディングDDLイベントを受信する必要があります（詳細については、 [シャードマージの原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください）。シャーディングDDLイベントがすでに移行プロセスにあり、一部のMySQLソースが削除されて再ロードされない場合（これらのMySQLソースはアプリケーションの要求に応じて削除されます）、シャーディングDDLロックを自動的に移行およびロック解除することはできません。すべてのDMワーカーがDDLイベントを受信できるわけではないためです。

> **ノート：**
>
> シャーディングDDLイベントを移行していないときに、一部のDMワーカーをオフラインにする必要がある場合は、 `stop-task`を使用して実行中のタスクを最初に停止し、DMワーカーをオフラインにし、対応する構成情報をから削除することをお勧めします。タスク構成ファイルを作成し、最後に`start-task`と新しいタスク構成を使用して移行タスクを再開します。

#### 手動ソリューション {#manual-solution}

アップストリームに2つのインスタンス`MySQL-1` （ `mysql-replica-01` ）と`MySQL-2` （ `mysql-replica-02` ）があり、2つのテーブル`shard_db_1`があるとします。 `shard_table_1`と`shard_db_1` 。 `MySQL-1`の`shard_table_2`と2つのテーブル`shard_db_2` 。 `shard_table_1`と`shard_db_2` 。 `MySQL-2`の`shard_table_2` 。次に、4つのテーブルをマージし、それらをテーブル`shard_db`に移行する必要があります。ダウンストリームTiDBで`shard_table` 。

初期のテーブル構造は次のとおりです。

```sql
SHOW CREATE TABLE shard_db_1.shard_table_1;
+---------------+------------------------------------------+
| Table         | Create Table                             |
+---------------+------------------------------------------+
| shard_table_1 | CREATE TABLE `shard_table_1` (
  `c1` int(11) NOT NULL,
  PRIMARY KEY (`c1`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 |
+---------------+------------------------------------------+
```

次のDDL操作は、テーブル構造を変更するためにアップストリームのシャーディングされたテーブルで実行されます。

```sql
ALTER TABLE shard_db_*.shard_table_* ADD COLUMN c2 INT;
```

MySQLとDMの操作プロセスは次のとおりです。

1.  対応するDDL操作は、テーブル構造を変更するために`mysql-replica-01`の2つのシャーディングされたテーブルで実行されます。

    ```sql
    ALTER TABLE shard_db_1.shard_table_1 ADD COLUMN c2 INT;
    ```

    ```sql
    ALTER TABLE shard_db_1.shard_table_2 ADD COLUMN c2 INT;
    ```

2.  DM-workerは、 `mysql-replica-01`の2つのシャーディングテーブルの受信したDDL情報をDM-masterに送信し、DM-masterは対応するDDLロックを作成します。

3.  `shard-ddl-lock`を使用して、現在のDDLロックの情報を確認します。

    ```bash
    » shard-ddl-lock test
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "mode": "pessimistic"
                "owner": "mysql-replica-01",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "mysql-replica-01"
                ],
                "unsynced": [
                    "mysql-replica-02"
                ]
            }
        ]
    }
    ```

4.  アプリケーションの需要により、 `mysql-replica-02`に対応するデータをダウンストリームTiDBに移行する必要がなくなり、 `mysql-replica-02`が削除されます。

5.  IDが``test-`shard_db`.`shard_table` ``対`DM-master`のロックは、 `mysql-replica-02`のDDL情報を受信できません。

    -   返される結果`unsynced`には、常に`shard-ddl-lock`の情報が含まれてい`mysql-replica-02` 。

6.  `shard-ddl-lock unlock`を使用して`DM-master`を要求し、DDLロックをアクティブにロック解除します。

    -   DDLロックの所有者がオフラインになった場合は、パラメーター`--owner`を使用して、DDLを実行するための新しい所有者として別のDMワーカーを指定できます。
    -   いずれかのMySQLソースがエラーを報告した場合、 `result`は`false`に設定されます。この時点で、各MySQLソースのエラーが許容可能であり、期待範囲内であるかどうかを注意深く確認する必要があります。

        {{< copyable "" >}}

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": ""
        ```

7.  `shard-ddl-lock`を使用して、DDLロックが正常にロック解除されているかどうかを確認します。

    ```bash
    » shard-ddl-lock test
    {
        "result": true,
        "msg": "no DDL lock exists",
        "locks": [
        ]
    }
    ```

8.  ダウンストリームTiDBでテーブル構造が正常に変更されているかどうかを確認します。

    ```sql
    mysql> SHOW CREATE TABLE shard_db.shard_table;
    +-------------+--------------------------------------------------+
    | Table       | Create Table                                     |
    +-------------+--------------------------------------------------+
    | shard_table | CREATE TABLE `shard_table` (
      `c1` int(11) NOT NULL,
      `c2` int(11) DEFAULT NULL,
      PRIMARY KEY (`c1`)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_bin |
    +-------------+--------------------------------------------------+
    ```

9.  `query-status`を使用して、移行タスクが正常かどうかを確認します。

#### 影響 {#impact}

`shard-ddl-lock unlock`を使用して手動でロックのロックを解除した後、タスク構成情報に含まれるオフラインのMySQLソースを処理しないと、次のシャーディングDDLイベントを受信したときにロックを自動的に移行できない場合があります。

したがって、DDLロックを手動でロック解除した後、次の操作を実行する必要があります。

1.  `stop-task`を使用して、実行中のタスクを停止します。
2.  タスク構成ファイルを更新し、オフラインMySQLソースの関連情報を構成ファイルから削除します。
3.  `start-task`と新しいタスク構成ファイルを使用して、タスクを再開します。

> **ノート：**
>
> `shard-ddl-lock unlock`を実行した後、オフラインになったMySQLソースがリロードされ、DMワーカーがシャーディングされたテーブルのデータを移行しようとすると、データとダウンストリームテーブル構造の間で一致エラーが発生する可能性があります。

### シナリオ2：一部のDMワーカーが異常に停止するか、DDLロック解除プロセス中にネットワーク障害が発生します {#scenario-2-some-dm-workers-stop-abnormally-or-the-network-failure-occurs-during-the-ddl-unlocking-process}

#### 異常なロックの理由 {#the-reason-for-the-abnormal-lock}

`DM-master`がすべてのDMワーカーのDDLイベントを受信した後、自動的に実行される`unlock DDL lock`には、主に次の手順が含まれます。

1.  ロックの所有者にDDLを実行し、対応するシャードテーブルのチェックポイントを更新するように依頼します。
2.  所有者がDDLを正常に実行した後、 `DM-master`に格納されているDDLロック情報を削除します。
3.  所有者がDDLを正常に実行した後、他のすべての非所有者にDDLをスキップし、対応するシャードテーブルのチェックポイントを更新するように依頼します。
4.  DM-masterは、すべての所有者または非所有者の操作が成功した後、対応するDDLロック情報を削除します。

現在、上記のロック解除プロセスはアトミックではありません。非所有者がDDL操作を正常にスキップすると、非所有者がいるDMワーカーが異常に停止するか、ダウンストリームTiDBでネットワーク異常が発生し、チェックポイントの更新が失敗する可能性があります。

非所有者に対応するMySQLソースがデータ移行を復元すると、非所有者は、例外が発生する前に調整されたDDL操作を再調整するようにDMマスターに要求しようとし、他から対応するDDL操作を受信することはありません。 MySQLソース。これにより、DDL操作で対応するロックが自動的にロック解除される可能性があります。

#### 手動ソリューション {#manual-solution}

これで、 [一部のMySQLソースが削除されました](#scenario-1-some-mysql-sources-are-removed)の手動ソリューションと同じアップストリームとダウンストリームのテーブル構造があり、テーブルのマージと移行に対する需要が同じであると仮定します。

`DM-master`が自動的にロック解除プロセスを実行すると、所有者（ `mysql-replica-01` ）はDDLを正常に実行し、移行プロセスを続行します。ただし、非所有者（ `mysql-replica-02` ）にDDL操作のスキップを要求するプロセスでは、対応するDM-workerが再起動されたため、DM-workerがDDL操作をスキップした後、チェックポイントの更新に失敗します。

`mysql-replica-02`の復元に対応するデータ移行サブタスクの後、DMマスターに新しいロックが作成されますが、他のMySQLソースがDDL操作を実行またはスキップし、後続の移行を実行しています。

操作プロセスは次のとおりです。

1.  `shard-ddl-lock`を使用して、対応するDDLのロックが`DM-master`に存在するかどうかを確認します。

    `synced`状態にあるのは`mysql-replica-02`つだけです。

    ```bash
    » shard-ddl-lock
    {
        "result": true,
        "msg": "",
        "locks": [
            {
                "ID": "test-`shard_db`.`shard_table`",
                "task": "test",
                "mode": "pessimistic"
                "owner": "mysql-replica-02",
                "DDLs": [
                    "USE `shard_db`; ALTER TABLE `shard_db`.`shard_table` ADD COLUMN `c2` int(11);"
                ],
                "synced": [
                    "mysql-replica-02"
                ],
                "unsynced": [
                    "mysql-replica-01"
                ]
            }
        ]
    }
    ```

2.  `shard-ddl-lock`を使用して`DM-master`にロックのロックを解除するように依頼します。

    -   ロック解除プロセス中に、所有者はダウンストリームに対してDDL操作を再度実行しようとします（再起動する前の元の所有者は、ダウンストリームに対してDDL操作を1回実行しました）。 DDL操作を複数回実行できることを確認してください。

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        {
            "result": true,
            "msg": "",
        }
        ```

3.  `shard-ddl-lock`を使用して、DDLロックが正常にロック解除されたかどうかを確認します。

4.  `query-status`を使用して、移行タスクが正常かどうかを確認します。

#### 影響 {#impact}

ロックを手動でロック解除した後、次のシャーディングDDLを自動的かつ通常どおりに移行できます。
