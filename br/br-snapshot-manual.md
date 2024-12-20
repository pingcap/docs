---
title: TiDB Snapshot Backup and Restore Command Manual
summary: TiDB スナップショット バックアップおよび復元コマンド マニュアルでは、クラスター スナップショット、データベース、およびテーブルをバックアップおよび復元するためのコマンドについて説明しています。また、バックアップ データの暗号化と暗号化されたスナップショットの復元についても説明しています。BR ツールはGC への自己適応をサポートし、統計のバックアップと復元のための --ignore-stats パラメータを導入しています。また、バックアップ データの暗号化と、指定されたデータベースまたはテーブルの部分的なデータの復元もサポートしています。
---

# TiDB スナップショットのバックアップと復元コマンド マニュアル {#tidb-snapshot-backup-and-restore-command-manual}

このドキュメントでは、次のようなアプリケーション シナリオに応じて、TiDB スナップショットのバックアップと復元のコマンドについて説明します。

-   [クラスタースナップショットをバックアップする](#back-up-cluster-snapshots)
-   [データベースまたはテーブルをバックアップする](#back-up-a-database-or-a-table)
    -   [データベースをバックアップする](#back-up-a-database)
    -   [テーブルをバックアップする](#back-up-a-table)
    -   [テーブルフィルターを使用して複数のテーブルをバックアップする](#back-up-multiple-tables-with-table-filter)
-   [統計のバックアップ](#back-up-statistics)
-   [バックアップデータを暗号化する](#encrypt-the-backup-data)
-   [クラスタースナップショットを復元する](#restore-cluster-snapshots)
-   [データベースまたはテーブルを復元する](#restore-a-database-or-a-table)
    -   [データベースを復元する](#restore-a-database)
    -   [テーブルを復元する](#restore-a-table)
    -   [テーブルフィルターを使用して複数のテーブルを復元する](#restore-multiple-tables-with-table-filter)
    -   [`mysql`スキーマから実行プランバインディングを復元する](#restore-execution-plan-bindings-from-the-mysql-schema)
-   [暗号化されたスナップショットを復元する](#restore-encrypted-snapshots)

スナップショットのバックアップと復元の詳細については、以下を参照してください。

-   [スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)
-   [バックアップと復元のユースケース](/br/backup-and-restore-use-cases.md)

## クラスタースナップショットをバックアップする {#back-up-cluster-snapshots}

`tiup br backup full`コマンドを使用して、TiDB クラスターの最新または指定されたスナップショットをバックアップできます。コマンドの詳細については、 `tiup br backup full --help`コマンドを実行してください。

```shell
tiup br backup full \
    --pd "${PD_IP}:2379" \
    --backupts '2024-06-28 13:30:00 +08:00' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

上記のコマンドでは、

-   `--backupts` : スナップショットの時点。形式は[TSO](/tso.md)または`400036290571534337`や`2024-06-28 13:30:00 +08:00`などのタイムスタンプです。このスナップショットのデータがガベージ コレクションされた場合、 `tiup br backup`コマンドはエラーを返し、&#39;br&#39; は終了します。このパラメータを指定しない場合、 `br`バックアップ開始時刻に対応するスナップショットを選択します。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV あたりの**最大速度。単位は MiB/s です。
-   `--log-file` : `br`ログが書き込まれる対象ファイル。

> **注記：**
>
> -   v8.5.0 以降、 BRツールは、バックアップ パフォーマンスを向上させるために、フル バックアップ中のテーブル レベルのチェックサム計算をデフォルトで無効にします ( `--checksum=false` )。
> -   BRツールは、GC への自己適応をすでにサポートしています。バックアップ中に TiDB の GC セーフ ポイントが前進しないように、 `backupTS` (デフォルトでは最新の PD タイムスタンプ) を PD の`safePoint`に自動的に登録し、GC 構成を手動で設定する必要がなくなります。

バックアップ中は、以下のようにターミナルに進行状況バーが表示されます。進行状況バーが 100% に進むと、バックアップが完了します。

```shell
Full Backup <---------/................................................> 17.12%.
```

## データベースまたはテーブルをバックアップする {#back-up-a-database-or-a-table}

バックアップと復元 (BR) は、クラスター スナップショットまたは増分データ バックアップから、指定されたデータベースまたはテーブルの部分的なデータのバックアップをサポートします。この機能を使用すると、スナップショット バックアップと増分データ バックアップから不要なデータを除外し、ビジネスに不可欠なデータのみをバックアップできます。

### データベースをバックアップする {#back-up-a-database}

クラスター内のデータベースをバックアップするには、 `tiup br backup db`コマンドを実行します。

次の例では、 `test`データベースを Amazon S3 にバックアップします。

```shell
tiup br backup db \
    --pd "${PD_IP}:2379" \
    --db test \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

上記のコマンドでは、 `--db`データベース名を指定し、その他のパラメータは[TiDB クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)と同じです。

### テーブルをバックアップする {#back-up-a-table}

クラスター内のテーブルをバックアップするには、 `tiup br backup table`コマンドを実行します。

次の例では、 `test.usertable`テーブルを Amazon S3 にバックアップします。

```shell
tiup br backup table \
    --pd "${PD_IP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

上記のコマンドでは、 `--db`と`--table`それぞれデータベース名とテーブル名を指定し、その他のパラメータは[TiDB クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)と同じです。

### テーブルフィルターを使用して複数のテーブルをバックアップする {#back-up-multiple-tables-with-table-filter}

より多くの条件で複数のテーブルをバックアップするには、 `tiup br backup full`コマンドを実行し、 [テーブルフィルター](/table-filter.md) `--filter`または`-f`で指定します。

次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルを Amazon S3 にバックアップします。

```shell
tiup br backup full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## 統計のバックアップ {#back-up-statistics}

TiDB v7.5.0 以降、 `br`コマンドライン ツールに`--ignore-stats`パラメータが導入されました。このパラメータを`false`に設定すると、 `br`コマンドライン ツールは列、インデックス、およびテーブルの統計のバックアップをサポートします。この場合、バックアップから復元された TiDB データベースの統計収集タスクを手動で実行したり、自動収集タスクの完了を待ったりする必要はありません。この機能により、データベースのメンテナンス作業が簡素化され、クエリのパフォーマンスが向上します。

このパラメータを`false`に設定しない場合、 `br`コマンドライン ツールはデフォルト設定の`--ignore-stats=true`使用します。つまり、データのバックアップ中に統計はバックアップされません。

以下は、クラスター スナップショット データをバックアップし、テーブル統計を`--ignore-stats=false`でバックアップする例です。

```shell
tiup br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ignore-stats=false
```

上記の構成でデータをバックアップした後、データを復元すると、バックアップにテーブル統計が含まれている場合、 `br`コマンドライン ツールはテーブル統計を自動的に復元します (v8.0.0 以降、 `br`コマンドライン ツールは、バックアップ統計を復元するかどうかを制御する`--load-stats`パラメーターを導入しました。デフォルトの動作では、バックアップ統計が復元されます。ほとんどの場合、これを`false`に設定する必要はありません)。

```shell
tiup br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log
```

バックアップと復元機能では、データをバックアップするときに、統計情報を JSON 形式で`backupmeta`ファイル内に保存します。データを復元するときに、統計情報を JSON 形式でクラスターに読み込みます。詳細については、 [ロード統計](/sql-statements/sql-statement-load-stats.md)参照してください。

## バックアップデータを暗号化する {#encrypt-the-backup-data}

BR はバックアップ側でのバックアップデータの暗号化と[Amazon S3にバックアップする際のstorage側](/br/backup-and-restore-storages.md#amazon-s3-server-side-encryption)サポートしています。必要に応じていずれかの暗号化方法を選択できます。

TiDB v5.3.0 以降では、次のパラメータを設定することでバックアップ データを暗号化できます。

-   `--crypter.method` : 暗号化アルゴリズム。 `aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`になります。デフォルト値は`plaintext`で、データが暗号化されていないことを示します。
-   `--crypter.key` : 16 進文字列形式の暗号化キー。アルゴリズム`aes128-ctr`の場合は 128 ビット (16 バイト) のキー、アルゴリズム`aes192-ctr`の場合は 24 バイトのキー、アルゴリズム`aes256-ctr`の場合は 32 バイトのキーです。
-   `--crypter.key-file` : キー ファイル`crypter.key`を渡さずに、キーが保存されているファイル パスをパラメーターとして直接渡すことができます。

次に例を示します。

```shell
tiup br backup full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **注記：**
>
> -   キーが失われると、バックアップ データをクラスターに復元できなくなります。
> -   暗号化機能は、 `br`および TiDB クラスター v5.3.0 以降のバージョンで使用する必要があります。暗号化されたバックアップ データは、v5.3.0 より前のクラスターでは復元できません。

## クラスタースナップショットを復元する {#restore-cluster-snapshots}

`tiup br restore full`コマンドを実行すると、TiDB クラスターのスナップショットを復元できます。

```shell
tiup br restore full \
    --pd "${PD_IP}:2379" \
    --with-sys-table \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file restorefull.log
```

上記のコマンドでは、

-   `--with-sys-table` : BR は、アカウント権限データ、SQL バインディング、統計情報など、**一部のシステム テーブルのデータを**復元します ( [統計のバックアップ](/br/br-snapshot-manual.md#back-up-statistics)を参照)。ただし、統計テーブル ( `mysql.stat_*` ) とシステム変数テーブル ( `mysql.tidb`と`mysql.global_variables` ) は復元されません。詳細については、 [`mysql`スキーマ内のテーブルを復元する](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)参照してください。
-   `--ratelimit` : 復元タスクを実行する**TiKV あたりの**最大速度。単位は MiB/s です。
-   `--log-file` : `br`ログが書き込まれる対象ファイル。

復元中は、以下のようにターミナルに進行状況バーが表示されます。進行状況バーが 100% に進むと、復元タスクは完了です。 `br` 、復元されたデータを検証して、データのセキュリティを確保します。

```shell
Full Restore <---------/...............................................> 17.12%.
```

## データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

`br`使用すると、バックアップ データから指定されたデータベースまたはテーブルの部分的なデータを復元できます。この機能を使用すると、復元中に不要なデータを除外できます。

### データベースを復元する {#restore-a-database}

データベースをクラスターに復元するには、 `tiup br restore db`コマンドを実行します。

次の例では、バックアップ データから`test`データベースをターゲット クラスターに復元します。

```shell
tiup br restore db \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_db.log
```

上記のコマンドでは、 `--db`復元するデータベースの名前を指定し、その他のパラメータは[TiDB クラスターのスナップショットを復元する](#restore-cluster-snapshots)と同じです。

> **注記：**
>
> バックアップデータをリストアする場合、 `--db`で指定したデータベース名は、バックアップコマンドの`-- db`で指定したデータベース名と同じである必要があります。そうでない場合、リストアは失敗します。これは、バックアップデータのメタファイル ( `backupmeta`ファイル) にデータベース名が記録されており、同じ名前のデータベースにしかデータをリストアできないためです。推奨される方法は、バックアップデータを別のクラスター内の同じ名前のデータベースにリストアすることです。

### テーブルを復元する {#restore-a-table}

単一のテーブルをクラスターに復元するには、 `tiup br restore table`コマンドを実行します。

次の例では、Amazon S3 から`test.usertable`テーブルをターゲット クラスターに復元します。

```shell
tiup br restore table \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_table.log
```

上記のコマンドでは、 `--table`復元するテーブルの名前を指定し、その他のパラメータは[データベースを復元する](#restore-a-database)と同じです。

### テーブルフィルターを使用して複数のテーブルを復元する {#restore-multiple-tables-with-table-filter}

より複雑なフィルター ルールを使用して複数のテーブルを復元するには、 `tiup br restore full`コマンドを実行し、 [テーブルフィルター](/table-filter.md) `--filter`または`-f`で指定します。

次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルを Amazon S3 からターゲット クラスターに復元します。

```shell
tiup br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restorefull.log
```

### <code>mysql</code>スキーマから実行プランバインディングを復元する {#restore-execution-plan-bindings-from-the-code-mysql-code-schema}

クラスターの実行プラン バインディングを復元するには、 `--with-sys-table`オプションと、復元する`mysql`スキーマを指定する`--filter`または`-f`オプションを含む`tiup br restore full`コマンドを実行します。

以下は`mysql.bind_info`テーブルを復元する例です。

```shell
tiup br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'mysql.bind_info' \
    --with-sys-table \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_system_table.log
```

復元が完了したら、実行プランのバインディング情報を[`SHOW GLOBAL BINDINGS`](/sql-statements/sql-statement-show-bindings.md)で確認できます。

```sql
SHOW GLOBAL BINDINGS;
```

復元後の実行プラン バインディングの動的読み込みはまだ最適化中です (関連する問題は[＃46527](https://github.com/pingcap/tidb/issues/46527)と[＃46528](https://github.com/pingcap/tidb/issues/46528)です)。復元後に実行プラン バインディングを手動で再読み込みする必要があります。

```sql
-- Ensure that the mysql.bind_info table has only one record for builtin_pseudo_sql_for_bind_lock. If there are more records, you need to manually delete them.
SELECT count(*) FROM mysql.bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock';
DELETE FROM bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock' LIMIT 1;

-- Force to reload the binding information.
ADMIN RELOAD BINDINGS;
```

## 暗号化されたスナップショットを復元する {#restore-encrypted-snapshots}

バックアップ データを暗号化した後、データを復元するには、対応する復号化パラメータを渡す必要があります。復号化アルゴリズムとキーが正しいことを確認してください。復号化アルゴリズムまたはキーが正しくない場合、データを復元することはできません。次に例を示します。

```shell
tiup br restore full\
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```
