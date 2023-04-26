---
title: Handle Sharding DDL Locks Manually in DM
summary: Learn how to handle sharding DDL locks manually in DM.
---

# DM でシャーディング DDL ロックを手動で処理する {#handle-sharding-ddl-locks-manually-in-dm}

DM はシャーディング DDL ロックを使用して、操作が正しい順序で実行されるようにします。このロック メカニズムは、ほとんどの場合、シャーディング DDL ロックを自動的に解決しますが、一部の異常なシナリオでは、 `shard-ddl-lock`コマンドを使用して異常な DDL ロックを手動で処理する必要があります。

> **ノート：**
>
> -   このドキュメントは、悲観的調整モードでの DDL ロックのシャーディングの処理にのみ適用されます。
> -   このドキュメントのコマンド使用セクションのコマンドは、インタラクティブ モードです。コマンドライン モードでは、エラー レポートを回避するためにエスケープ文字を追加する必要があります。
> -   コマンドによってもたらされる可能性のある影響を完全に認識しており、それを受け入れることができる場合を除き、 `shard-ddl-lock unlock`を使用しないでください。
> -   異常な DDL ロックを手動で処理する前に、DM [シャード マージの原則](/dm/feature-shard-merge-pessimistic.md#principles)を既に読んでいることを確認してください。

## 指図 {#command}

### <code>shard-ddl-lock</code> {#code-shard-ddl-lock-code}

このコマンドを使用して、DDL ロックを表示し、指定された DDL ロックを解放するよう DM マスターに要求できます。このコマンドは、DM v6.0 以降でのみサポートされています。以前のバージョンでは、 `show-ddl-locks`および`unlock-ddl-locks`コマンドを使用する必要があります。

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

-   `shard-ddl-lock [task] [flags]` : 現在の DM マスターの DDL ロック情報を表示します。

<!---->

-   `shard-ddl-lock [command]` : 指定された DDL ロックの解放を DM マスターに要求します。 `[command]`値として`unlock`のみを受け入れます。

## 使用例 {#usage-examples}

### <code>shard-ddl-lock [task] [flags]</code> {#code-shard-ddl-lock-task-flags-code}

`shard-ddl-lock [task] [flags]`を使用して、現在の DM マスターの DDL ロック情報を表示できます。例えば：

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

このコマンドは、所有者に DDL ステートメントを実行するように要求する、所有者ではない他のすべての DM-worker に DDL ステートメントをスキップするように要求する、および`DM-master`ロック情報を削除するなど、指定された DDL ロックのロックを解除するように`DM-master`アクティブに要求します。

> **ノート：**
>
> 現在、 `shard-ddl-lock unlock` `pessimistic`モードのロックに対してのみ有効です。

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

`shard-ddl-lock unlock`次の引数を受け入れます。

-   `-o, --owner` :

    -   国旗;弦;オプション
    -   指定されていない場合、このコマンドは、デフォルトの所有者 ( `shard-ddl-lock`の結果の所有者) が DDL ステートメントを実行するように要求します。指定されている場合、このコマンドは MySQL ソース (デフォルトの所有者の代替) に DDL ステートメントを実行するように要求します。
    -   元の所有者がクラスターから既に削除されていない限り、新しい所有者を指定しないでください。

-   `-f, --force-remove` :

    -   国旗;ブール値;オプション
    -   指定されていない場合、このコマンドは所有者が DDL ステートメントの実行に成功した場合にのみロック情報を削除します。これが指定されている場合、このコマンドは、所有者が DDL ステートメントの実行に失敗した場合でも、ロック情報を強制的に削除します (これを実行した後は、再度ロックを照会したり操作したりすることはできません)。

-   `lock-id` :

    -   非フラグ;弦;必要
    -   ロックを解除する必要がある DDL ロックの ID ( `shard-ddl-lock`の結果の`ID` ) を指定します。

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

## サポートされるシナリオ {#supported-scenarios}

現在、 `shard-ddl-lock unlock`コマンドは、次の 2 つの異常なシナリオでのシャーディング DDL ロックの処理のみをサポートしています。

### シナリオ 1: 一部の MySQL ソースが削除される {#scenario-1-some-mysql-sources-are-removed}

#### ロック異常の原因 {#the-reason-for-the-abnormal-lock}

`DM-master`がシャーディング DDL ロックの自動ロック解除を試行する前に、すべての MySQL ソースがシャーディング DDL イベントを受信する必要があります (詳細については、 [シャード マージの原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください)。シャーディング DDL イベントがすでに移行プロセスにあり、一部の MySQL ソースが削除されて再ロードされない場合 (これらの MySQL ソースはアプリケーションの要求に従って削除されています)、シャーディング DDL ロックを自動的に移行してロック解除することはできません。すべての DM ワーカーが DDL イベントを受信できるわけではないためです。

> **ノート：**
>
> シャーディング DDL イベントを移行していないときに一部の DM-worker をオフラインにする必要がある場合は、 `stop-task`を使用して実行中のタスクを最初に停止し、DM-worker をオフラインにして、対応する構成情報をタスク構成ファイルを削除し、最後に`start-task`と新しいタスク構成を使用して移行タスクを再開します。

#### 手動ソリューション {#manual-solution}

上流に`MySQL-1` ( `mysql-replica-01` ) と`MySQL-2` ( `mysql-replica-02` ) の 2 つのインスタンスがあり、2 つのテーブル`shard_db_1`があるとします。 `shard_table_1`および`shard_db_1` 。 `MySQL-1`の`shard_table_2`と 2 つのテーブル`shard_db_2` 。 `shard_table_1`および`shard_db_2` 。 `MySQL-2`中`shard_table_2` 。ここで、4 つのテーブルをマージしてテーブルに移行する必要があります`shard_db` 。ダウンストリーム TiDB の`shard_table` 。

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

次の DDL 操作がアップストリームのシャード テーブルで実行され、テーブル構造が変更されます。

```sql
ALTER TABLE shard_db_*.shard_table_* ADD COLUMN c2 INT;
```

MySQL と DM の操作プロセスは次のとおりです。

1.  対応する DDL 操作が`mysql-replica-01`の 2 つのシャード テーブルに対して実行され、テーブル構造が変更されます。

    ```sql
    ALTER TABLE shard_db_1.shard_table_1 ADD COLUMN c2 INT;
    ```

    ```sql
    ALTER TABLE shard_db_1.shard_table_2 ADD COLUMN c2 INT;
    ```

2.  DM-worker は受信した`mysql-replica-01`の 2 つのシャード テーブルの DDL 情報を DM-master に送信し、DM-master は対応する DDL ロックを作成します。

3.  `shard-ddl-lock`を使用して、現在の DDL ロックの情報を確認します。

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

4.  アプリケーションの需要により、 `mysql-replica-02`に対応するデータを下流の TiDB に移行する必要がなくなり、 `mysql-replica-02`が削除されます。

5.  ID が``test-`shard_db`.`shard_table` `` on `DM-master`ロックは、 `mysql-replica-02`の DDL 情報を受け取ることができません。

    -   返された結果`unsynced` by `shard-ddl-lock`には、常に`mysql-replica-02`の情報が含まれています。

6.  `shard-ddl-lock unlock`を使用して`DM-master`要求し、DDL ロックをアクティブにロック解除します。

    -   DDL ロックの所有者がオフラインになった場合、パラメーター`--owner`を使用して、DDL を実行する新しい所有者として別の DM-worker を指定できます。
    -   いずれかの MySQL ソースがエラーを報告した場合、 `result` `false`に設定されます。この時点で、各 MySQL ソースのエラーが許容可能であり、想定内であるかどうかを慎重に確認する必要があります。

        {{< copyable "" >}}

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        ```

        ```
        {
            "result": true,
            "msg": ""
        ```

7.  `shard-ddl-lock`使用して、DDL ロックが正常にロック解除されたかどうかを確認します。

    ```bash
    » shard-ddl-lock test
    {
        "result": true,
        "msg": "no DDL lock exists",
        "locks": [
        ]
    }
    ```

8.  下流の TiDB でテーブル構造が正常に変更されているかどうかを確認します。

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

9.  `query-status`使用して、移行タスクが正常かどうかを確認します。

#### 影響 {#impact}

`shard-ddl-lock unlock`を使用して手動でロックを解除した後、タスク構成情報に含まれるオフラインの MySQL ソースを処理しないと、次のシャーディング DDL イベントが受信されたときにロックが自動的に移行されない可能性があります。

したがって、DDL ロックを手動でロック解除した後、次の操作を実行する必要があります。

1.  実行中のタスクを停止するには、 `stop-task`を使用します。
2.  タスク構成ファイルを更新し、オフライン MySQL ソースの関連情報を構成ファイルから削除します。
3.  `start-task`と新しいタスク構成ファイルを使用して、タスクを再開します。

> **ノート：**
>
> `shard-ddl-lock unlock`を実行した後、オフラインになった MySQL ソースが再ロードされ、DM-worker が分割されたテーブルのデータを移行しようとすると、データと下流のテーブル構造の間で一致エラーが発生する可能性があります。

### シナリオ 2: 一部の DM-worker が異常停止するか、DDL ロック解除プロセス中にネットワーク障害が発生する {#scenario-2-some-dm-workers-stop-abnormally-or-the-network-failure-occurs-during-the-ddl-unlocking-process}

#### ロック異常の原因 {#the-reason-for-the-abnormal-lock}

`DM-master`がすべての DM-worker の DDL イベントを受信した後、自動的に`unlock DDL lock`を実行するには、主に次の手順が含まれます。

1.  ロックの所有者に DDL を実行し、対応するシャード テーブルのチェックポイントを更新するよう依頼します。
2.  所有者が DDL を正常に実行した後、 `DM-master`に保存されている DDL ロック情報を削除します。
3.  所有者以外のすべての非所有者に、DDL をスキップして、所有者が DDL を正常に実行した後、対応するシャード テーブルのチェックポイントを更新するように依頼します。
4.  DM マスターは、すべての所有者または非所有者の操作が成功した後、対応する DDL ロック情報を削除します。

現在、上記のロック解除プロセスはアトミックではありません。非所有者が DDL 操作を正常にスキップすると、非所有者が配置されている DM-worker が異常停止するか、下流の TiDB でネットワーク異常が発生し、チェックポイントの更新が失敗する可能性があります。

非所有者に対応する MySQL ソースがデータ移行を復元すると、非所有者は DM マスターに、例外が発生する前に調整されていた DDL 操作を再調整するように要求しようとし、他のソースから対応する DDL 操作を受け取ることはありません。 MySQL ソース。これにより、DDL 操作によって、対応するロックが自動的にロック解除される可能性があります。

#### 手動ソリューション {#manual-solution}

ここで、アップストリームとダウンストリームのテーブル構造が同じであり、テーブルのマージと移行に対する要求が[一部の MySQL ソースが削除されました](#scenario-1-some-mysql-sources-are-removed)の手動ソリューションと同じであるとします。

`DM-master`が自動的にロック解除プロセスを実行すると、所有者 ( `mysql-replica-01` ) は DDL を正常に実行し、移行プロセスを続行します。ただし、非所有者 ( `mysql-replica-02` ) に DDL 操作をスキップするように要求するプロセスでは、対応する DM-worker が再起動されたため、DM-worker が DDL 操作をスキップした後、チェックポイントの更新に失敗します。

`mysql-replica-02`の復元に対応するデータ移行サブタスクの後、DM マスターに新しいロックが作成されますが、他の MySQL ソースは DDL 操作を実行またはスキップしており、後続の移行を実行しています。

操作プロセスは次のとおりです。

1.  `shard-ddl-lock`を使用して、DDL の対応するロックが`DM-master`に存在するかどうかを確認します。

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

2.  `shard-ddl-lock`を使用して`DM-master`にロック解除を依頼します。

    -   ロック解除処理中に、所有者は再びダウンストリームへの DDL 操作を実行しようとします (再起動前の元の所有者はダウンストリームへの DDL 操作を 1 回実行しています)。 DDL 操作を複数回実行できることを確認してください。

        ```bash
        shard-ddl-lock unlock test-`shard_db`.`shard_table`
        {
            "result": true,
            "msg": "",
        }
        ```

3.  `shard-ddl-lock`を使用して、DDL ロックが正常にロック解除されたかどうかを確認します。

4.  `query-status`使用して、移行タスクが正常かどうかを確認します。

#### 影響 {#impact}

手動でロックを解除した後、次のシャーディング DDL を自動的に正常に移行できます。
