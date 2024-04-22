---
title: TiDB Snapshot Backup and Restore Command Manual
summary: このドキュメントは、TiDBのスナップショットのバックアップと復元コマンドについて説明しています。バックアップにはクラスターのスナップショットやデータベース、テーブルのバックアップが含まれます。さらに、統計のバックアップや暗号化されたバックアップデータの復元も可能です。また、テーブルフィルターを使用して複数のテーブルをバックアップおよび復元することもできます。
---

# TiDB スナップショットのバックアップおよび復元コマンド マニュアル {#tidb-snapshot-backup-and-restore-command-manual}

このドキュメントでは、次のようなアプリケーション シナリオに従って、TiDB スナップショットのバックアップと復元のコマンドについて説明します。

-   [クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)
-   [データベースまたはテーブルをバックアップする](#back-up-a-database-or-a-table)
    -   [データベースをバックアップする](#back-up-a-database)
    -   [テーブルをバックアップする](#back-up-a-table)
    -   [テーブルフィルターを使用して複数のテーブルをバックアップする](#back-up-multiple-tables-with-table-filter)
-   [統計のバックアップ](#back-up-statistics)
-   [バックアップデータを暗号化する](#encrypt-the-backup-data)
-   [クラスターのスナップショットを復元する](#restore-cluster-snapshots)
-   [データベースまたはテーブルを復元する](#restore-a-database-or-a-table)
    -   [データベースを復元する](#restore-a-database)
    -   [テーブルを復元する](#restore-a-table)
    -   [テーブルフィルターを使用して複数のテーブルを復元する](#restore-multiple-tables-with-table-filter)
    -   [`mysql`スキーマから実行プランのバインディングを復元する](#restore-execution-plan-bindings-from-the-mysql-schema)
-   [暗号化されたスナップショットを復元する](#restore-encrypted-snapshots)

スナップショットのバックアップと復元の詳細については、以下を参照してください。

-   [スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)
-   [バックアップと復元の使用例](/br/backup-and-restore-use-cases.md)

## クラスターのスナップショットをバックアップする {#back-up-cluster-snapshots}

`br backup full`コマンドを使用して、TiDB クラスターの最新または指定したスナップショットをバックアップできます。コマンドの詳細については、 `br backup full --help`コマンドを実行してください。

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

前述のコマンドでは次のようになります。

-   `--backupts` : スナップショットの時点。形式は[TSO](/glossary.md#tso)またはタイムスタンプ ( `400036290571534337`や`2018-05-11 01:42:23`など) です。このスナップショットのデータがガベージ コレクションされた場合、 `br backup`コマンドはエラーを返し、「br」は終了します。このパラメータを指定しないままにすると、 `br`バックアップ開始時刻に対応するスナップショットを選択します。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度。単位は MiB/s です。
-   `--log-file` : `br`ログが書き込まれる対象ファイル。

> **注記：**
>
> BRツールはすでに GC への自己適応をサポートしています。 PD の`safePoint`に`backupTS` (デフォルトでは最新の PD タイムスタンプ) を自動的に登録して、バックアップ中に TiDB の GC セーフ ポイントが先に進まないようにし、GC 構成を手動で設定する必要がなくなります。

バックアップ中、以下に示すように、進行状況バーがターミナルに表示されます。進行状況バーが 100% まで進むと、バックアップは完了です。

```shell
Full Backup <---------/................................................> 17.12%.
```

## データベースまたはテーブルをバックアップする {#back-up-a-database-or-a-table}

バックアップと復元 (BR) は、クラスター スナップショットまたは増分データ バックアップからの指定されたデータベースまたはテーブルの部分データのバックアップをサポートします。この機能を使用すると、スナップショット バックアップと増分データ バックアップから不要なデータをフィルタリングして除外し、ビジネス クリティカルなデータのみをバックアップできます。

### データベースをバックアップする {#back-up-a-database}

クラスター内のデータベースをバックアップするには、 `br backup db`コマンドを実行します。

次の例では、 `test`データベースを Amazon S3 にバックアップします。

```shell
br backup db \
    --pd "${PD_IP}:2379" \
    --db test \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

前述のコマンドでは、 `--db`​​データベース名を指定し、その他のパラメータは[TiDB クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)と同じです。

### テーブルをバックアップする {#back-up-a-table}

クラスター内のテーブルをバックアップするには、 `br backup table`コマンドを実行します。

次の例では、 `test.usertable`テーブルを Amazon S3 にバックアップします。

```shell
br backup table \
    --pd "${PD_IP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

前述のコマンドでは、 `--db`と`--table`にそれぞれデータベース名とテーブル名を指定し、その他のパラメータは[TiDB クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)と同じです。

### テーブルフィルターを使用して複数のテーブルをバックアップする {#back-up-multiple-tables-with-table-filter}

より多くの条件を使用して複数のテーブルをバックアップするには、 `br backup full`コマンドを実行し、 `--filter`または`-f`で[テーブルフィルター](/table-filter.md)を指定します。

次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルを Amazon S3 にバックアップします。

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## 統計のバックアップ {#back-up-statistics}

TiDB v7.5.0 以降、 `br`コマンドライン ツールには`--ignore-stats`パラメータが導入されています。このパラメータを`false`に設定すると、 `br`コマンドライン ツールは列、インデックス、テーブルの統計のバックアップと復元をサポートします。この場合、バックアップから復元された TiDB データベースの統計収集タスクを手動で実行したり、自動収集タスクの完了を待つ必要はありません。この機能により、データベースのメンテナンス作業が簡素化され、クエリのパフォーマンスが向上します。

このパラメーターを`false`に設定しない場合、 `br`コマンドライン ツールはデフォルト設定`--ignore-stats=true`を使用します。これは、データのバックアップ中に統計がバックアップされないことを意味します。

以下は、クラスターのスナップショット データをバックアップし、 `--ignore-stats=false`を使用してテーブル統計をバックアップする例です。

```shell
br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ignore-stats=false
```

前述の構成でデータをバックアップした後、データを復元すると、バックアップにテーブル統計が含まれている場合、 `br`コマンド ライン ツールによってテーブル統計が自動的に復元されます。

```shell
br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log
```

バックアップおよび復元機能でデータをバックアップすると、統計が`backupmeta`のファイル内に JSON 形式で保存されます。データを復元するとき、統計情報が JSON 形式でクラスターにロードされます。詳細については、 [負荷統計](/sql-statements/sql-statement-load-stats.md)を参照してください。

## バックアップデータを暗号化する {#encrypt-the-backup-data}

> **警告：**
>
> これは実験的機能です。本番環境で使用することはお勧めできません。

BR は、バックアップ[Amazon S3 にバックアップするときにstorage側で](/br/backup-and-restore-storages.md#amazon-s3-server-side-encryption)でのバックアップ データの暗号化をサポートします。必要に応じてどちらかの暗号化方式を選択できます。

TiDB v5.3.0 以降、次のパラメータを構成することでバックアップ データを暗号化できます。

-   `--crypter.method` : 暗号化アルゴリズム。 `aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`のいずれかです。デフォルト値は`plaintext`で、データが暗号化されないことを示します。
-   `--crypter.key` : 16 進文字列形式の暗号化キー。アルゴリズム`aes128-ctr`場合は 128 ビット (16 バイト) の鍵、アルゴリズム`aes192-ctr`の場合は 24 バイトの鍵、アルゴリズム`aes256-ctr`の場合は 32 バイトの鍵です。
-   `--crypter.key-file` : キーファイル。 `crypter.key`を渡さずに、キーが保存されているファイル パスをパラメータとして直接渡すことができます。

以下は例です。

```shell
br backup full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **注記：**
>
> -   キーを紛失すると、バックアップ データをクラスターに復元できなくなります。
> -   暗号化機能は、 `br`および TiDB クラスター v5.3.0 以降のバージョンで使用する必要があります。暗号化されたバックアップ データは、v5.3.0 より前のクラスターでは復元できません。

## クラスターのスナップショットを復元する {#restore-cluster-snapshots}

`br restore full`コマンドを実行すると、TiDB クラスターのスナップショットを復元できます。

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --with-sys-table \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file restorefull.log
```

前述のコマンドでは次のようになります。

-   `--with-sys-table` : BR は、アカウント権限データ、SQL バインディング、統計など、**一部のシステム テーブルのデータ**を復元します ( [統計のバックアップ](/br/br-snapshot-manual.md#back-up-statistics)を参照)。ただし、統計テーブル ( `mysql.stat_*` ) とシステム変数テーブル ( `mysql.tidb`および`mysql.global_variables` ) は復元されません。詳細については、 [`mysql`スキーマ内のテーブルを復元する](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)を参照してください。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度。単位は MiB/s です。
-   `--log-file` : `br`ログが書き込まれる対象ファイル。

復元中、以下に示すように進行状況バーがターミナルに表示されます。進行状況バーが 100% まで進むと、復元タスクは完了します。 `br` 、復元されたデータを検証してデータのセキュリティを確保します。

```shell
Full Restore <---------/...............................................> 17.12%.
```

## データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

`br`を使用すると、指定したデータベースまたはテーブルの部分データをバックアップ データから復元できます。この機能を使用すると、復元中に不要なデータを除外できます。

### データベースを復元する {#restore-a-database}

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。

次の例では、バックアップ データから`test`データベースをターゲット クラスターに復元します。

```shell
br restore db \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_db.log
```

前述のコマンドでは、 `--db`​​復元するデータベースの名前を指定し、その他のパラメータは[TiDB クラスターのスナップショットを復元する](#restore-cluster-snapshots)と同じです。

> **注記：**
>
> バックアップデータをリストアする場合、バックアップコマンドの`--db`で指定したデータベース名と`-- db`で指定したデータベース名は同じである必要があります。そうしないと、復元は失敗します。これは、バックアップデータのメタファイル（ `backupmeta`ファイル）にデータベース名が記録されており、同じ名前のデータベースにしかデータをリストアできないためです。推奨される方法は、バックアップ データを別のクラスター内の同じ名前のデータベースに復元することです。

### テーブルを復元する {#restore-a-table}

単一のテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。

次の例では、 `test.usertable`テーブルを Amazon S3 からターゲットクラスターに復元します。

```shell
br restore table \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_table.log
```

前述のコマンドでは、 `--table`に復元するテーブルの名前を指定し、その他のパラメータは[データベースを復元する](#restore-a-database)と同じです。

### テーブルフィルターを使用して複数のテーブルを復元する {#restore-multiple-tables-with-table-filter}

より複雑なフィルター ルールを使用して複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 [テーブルフィルター](/table-filter.md)に`--filter`または`-f`を指定します。

次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルを Amazon S3 からターゲット クラスターに復元します。

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restorefull.log
```

### <code>mysql</code>スキーマから実行プランのバインディングを復元する {#restore-execution-plan-bindings-from-the-code-mysql-code-schema}

クラスターの実行プラン バインディングを復元するには、 `--with-sys-table`オプションと、復元するスキーマを指定する`--filter`オプションを含む`br restore full` `mysql` `-f`実行します。

以下は`mysql.bind_info`テーブルを復元する例です。

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'mysql.bind_info' \
    --with-sys-table \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_system_table.log
```

復元が完了したら、実行プランのバインド情報を[`SHOW GLOBAL BINDINGS`](/sql-statements/sql-statement-show-bindings.md)で確認できます。

```sql
SHOW GLOBAL BINDINGS;
```

復元後の実行プラン バインディングの動的読み込みはまだ最適化中です (関連する問題は[#46527](https://github.com/pingcap/tidb/issues/46527)と[#46528](https://github.com/pingcap/tidb/issues/46528)です)。復元後に実行計画バインディングを手動で再ロードする必要があります。

```sql
-- Ensure that the mysql.bind_info table has only one record for builtin_pseudo_sql_for_bind_lock. If there are more records, you need to manually delete them.
SELECT count(*) FROM mysql.bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock';
DELETE FROM bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock' LIMIT 1;

-- Force to reload the binding information.
ADMIN RELOAD BINDINGS;
```

## 暗号化されたスナップショットを復元する {#restore-encrypted-snapshots}

> **警告：**
>
> これは実験的機能です。本番環境で使用することはお勧めできません。

バックアップ データを暗号化した後、データを復元するには、対応する復号化パラメータを渡す必要があります。復号化アルゴリズムとキーが正しいことを確認してください。復号化アルゴリズムまたはキーが間違っている場合、データを復元することはできません。以下は例です。

```shell
br restore full\
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```
