---
title: TiDB Snapshot Backup and Restore Command Manual
summary: Learn about the commands of TiDB snapshot backup and restore.
---

# TiDB スナップショットのバックアップと復元コマンド マニュアル {#tidb-snapshot-backup-and-restore-command-manual}

このドキュメントでは、次のようなアプリケーション シナリオに従って、TiDB スナップショットのバックアップと復元のコマンドについて説明します。

-   [クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)
-   [データベースのバックアップ](#back-up-a-database)
-   [テーブルをバックアップする](#back-up-a-table)
-   [テーブル フィルターを使用して複数のテーブルをバックアップする](#back-up-multiple-tables-with-table-filter)
-   [バックアップ データを暗号化する](#encrypt-the-backup-data)
-   [クラスターのスナップショットを復元する](#restore-cluster-snapshots)
-   [データベースを復元する](#restore-a-database)
-   [テーブルを復元する](#restore-a-table)
-   [テーブル フィルターを使用して複数のテーブルを復元する](#restore-multiple-tables-with-table-filter)
-   [暗号化されたスナップショットを復元する](#restore-encrypted-snapshots)

スナップショットのバックアップと復元の詳細については、次を参照してください。

-   [スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)
-   [バックアップと復元の使用例](/br/backup-and-restore-use-cases.md)

## クラスターのスナップショットをバックアップする {#back-up-cluster-snapshots}

`br backup full`コマンドを使用して、TiDB クラスターの最新または指定されたスナップショットをバックアップできます。コマンドの詳細については、 `br backup full --help`コマンドを実行してください。

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

前述のコマンドでは:

-   `--backupts` : スナップショットの時点。形式は[TSO](/glossary.md#tso)またはタイムスタンプ ( `400036290571534337`や`2018-05-11 01:42:23`など) にすることができます。このスナップショットのデータがガベージ コレクションされている場合、 `br backup`コマンドはエラーを返し、&#39;br&#39; は終了します。このパラメーターを指定しない場合、 `br`バックアップの開始時刻に対応するスナップショットを選択します。
-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度。単位は MiB/s です。
-   `--log-file` : `br`ログが書き込まれる対象ファイル。

> **ノート：**
>
> BRツールは、GC への自己適応を既にサポートしています。 `backupTS` (デフォルトでは最新の PD タイムスタンプ) を PD の`safePoint`に自動的に登録して、バックアップ中に TiDB の GC セーフ ポイントが前に移動しないようにするため、手動で GC 構成を設定する必要がなくなります。

バックアップ中は、以下に示すように、進行状況バーがターミナルに表示されます。プログレス バーが 100% まで進むと、バックアップは完了です。

```shell
Full Backup <---------/................................................> 17.12%.
```

## データベースまたはテーブルのバックアップ {#back-up-a-database-or-a-table}

バックアップと復元 (BR) は、クラスター スナップショットまたは増分データ バックアップから、指定されたデータベースまたはテーブルの部分的なデータのバックアップをサポートします。この機能を使用すると、スナップショット バックアップと増分データ バックアップから不要なデータを除外し、ビジネス クリティカルなデータのみをバックアップできます。

### データベースのバックアップ {#back-up-a-database}

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

上記のコマンドで、 `--db`データベース名を指定し、他のパラメーターは[TiDB クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)と同じです。

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

上記のコマンドで、 `--db`と`--table`それぞれデータベース名とテーブル名を指定し、その他のパラメーターは[TiDB クラスターのスナップショットをバックアップする](#back-up-cluster-snapshots)と同じです。

### テーブル フィルターを使用して複数のテーブルをバックアップする {#back-up-multiple-tables-with-table-filter}

複数の基準で複数のテーブルをバックアップするには、 `br backup full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)を指定します。

次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルを Amazon S3 にバックアップします。

```shell
br backup full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## バックアップ データを暗号化する {#encrypt-the-backup-data}

> **警告：**
>
> これは実験的機能です。本番環境で使用することはお勧めしません。

BR は、バックアップ[Amazon S3にバックアップする際のstorage側](/br/backup-and-restore-storages.md#amazon-s3-server-side-encryption)でのバックアップ データの暗号化をサポートしています。必要に応じて、いずれかの暗号化方式を選択できます。

TiDB v5.3.0 以降、次のパラメータを設定することでバックアップ データを暗号化できます。

-   `--crypter.method` : 暗号化アルゴリズム。 `aes128-ctr` 、 `aes192-ctr` 、または`aes256-ctr`のいずれかです。デフォルト値は`plaintext`で、データが暗号化されていないことを示します。
-   `--crypter.key` : 16 進文字列形式の暗号化キー。アルゴリズム`aes128-ctr`では 128 ビット (16 バイト) の鍵、アルゴリズム`aes192-ctr`では 24 バイトの鍵、アルゴリズム`aes256-ctr`では 32 バイトの鍵です。
-   `--crypter.key-file` : 鍵ファイル。 `crypter.key` .

次に例を示します。

```shell
br backup full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **ノート：**
>
> -   キーを紛失すると、バックアップ データをクラスタに復元できなくなります。
> -   暗号化機能は、 `br`および TiDB クラスター v5.3.0 以降のバージョンで使用する必要があります。暗号化されたバックアップ データは、v5.3.0 より前のクラスターでは復元できません。

## クラスターのスナップショットを復元する {#restore-cluster-snapshots}

`br restore full`コマンドを実行して、TiDB クラスターのスナップショットを復元できます。

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file restorefull.log
```

前述のコマンドでは:

-   `--ratelimit` : バックアップ タスクを実行する**TiKV ごとの**最大速度。単位は MiB/s です。
-   `--log-file` : `br`ログが書き込まれるターゲット ファイル。

復元中は、以下に示すように進行状況バーがターミナルに表示されます。プログレス バーが 100% まで進むと、復元タスクは完了です。 `br` 、復元されたデータを検証して、データのセキュリティを確保します。

```shell
Full Restore <---------/...............................................> 17.12%.
```

## データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

`br`を使用して、指定したデータベースまたはテーブルの部分データをバックアップ データから復元できます。この機能により、復元中に不要なデータを除外できます。

### データベースを復元する {#restore-a-database}

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。

次の例では、 `test`データベースをバックアップ データからターゲット クラスターに復元します。

```shell
br restore db \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_db.log
```

上記のコマンドで、 `--db`復元するデータベースの名前を指定し、その他のパラメーターは[TiDB クラスターのスナップショットを復元する](#restore-cluster-snapshots)と同じです。

> **ノート：**
>
> バックアップデータを復元する場合、 `--db`で指定したデータベース名は、バックアップコマンドの`-- db`で指定したデータベース名と同じでなければなりません。そうしないと、復元は失敗します。これは、バックアップ データのメタファイル ( `backupmeta`ファイル) にデータベース名が記録されており、同じ名前のデータベースにしかデータを復元できないためです。推奨される方法は、バックアップ データを別のクラスター内の同じ名前のデータベースに復元することです。

### テーブルを復元する {#restore-a-table}

1 つのテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。

次の例では、 `test.usertable`テーブルを Amazon S3 からターゲット クラスターに復元します。

```shell
br restore table \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_table.log
```

上記のコマンドで、 `--table`復元するテーブルの名前を指定し、その他のパラメーターは[データベースを復元する](#restore-a-database)と同じです。

### テーブル フィルターを使用して複数のテーブルを復元する {#restore-multiple-tables-with-table-filter}

より複雑なフィルタ ルールを使用して複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)指定します。

次の例では、 `db*.tbl*`フィルター ルールに一致するテーブルを Amazon S3 からターゲット クラスターに復元します。

```shell
br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restorefull.log
```

## 暗号化されたスナップショットを復元する {#restore-encrypted-snapshots}

> **警告：**
>
> これは実験的機能です。本番環境で使用することはお勧めしません。

バックアップ データを暗号化したら、対応する復号化パラメータを渡してデータを復元する必要があります。復号化アルゴリズムとキーが正しいことを確認してください。復号化アルゴリズムまたはキーが正しくない場合、データは復元できません。次に例を示します。

```shell
br restore full\
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```
