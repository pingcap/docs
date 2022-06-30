---
title: Use BR to Restore Cluster Data
summary: Learn how to restore data using BR commands
---

# BRを使用してクラスターデータを復元する {#use-br-to-restore-cluster-data}

このドキュメントでは、次のシナリオでBRを使用してクラスタデータを復元する方法について説明します。

-   [TiDBクラスタスナップショットを復元する](#restore-tidb-cluster-snapshots)
-   [データベースを復元する](#restore-a-database)
-   [テーブルを復元する](#restore-a-table)
-   [テーブルフィルターを使用して複数のテーブルを復元する](#restore-multiple-tables-with-table-filter)
-   [外部ストレージからバックアップデータを復元する](#restore-backup-data-from-external-storage)
-   [増分データを復元する](#restore-incremental-data)
-   [暗号化されたバックアップデータを復元する](#restore-encrypted-backup-data)
-   [`mysql`スキーマで作成されたテーブルを復元します](#restore-tables-created-in-the-mysql-schema)

Backup＆Restore（BR）に精通していない場合は、次のドキュメントを読んで、BRの使用原則と方法を完全に理解することをお勧めします。

-   [BRの概要](/br/backup-and-restore-overview.md)
-   [バックアップと復元にBRコマンドラインを使用する](/br/use-br-command-line-tool.md)

## TiDBクラスタスナップショットを復元する {#restore-tidb-cluster-snapshots}

BRは、スナップショットのバックアップ時にターゲットクラスタを最新の状態に復元するために、空のクラスタでのスナップショットバックアップの復元をサポートしています。

例： `2022-01-30 07:42:23`で生成されたスナップショットをAmazonS3の`backup-data`バケットの`2022-01-30/`ディレクトリからターゲットクラスタに復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
```

上記のコマンドでは、

-   `--ratelimit` ：復元タスクを実行するための**各TiKV**の最大速度（単位：MiB / s）
-   `--log-file`ロギングのターゲットファイル

復元中は、以下に示すように、ターミナルにプログレスバーが表示されます。プログレスバーが100％に進むと、復元が完了します。データのセキュリティを確保するために、BRは復元されたデータのチェックを実行します。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

## データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

BRは、バックアップデータからの指定されたデータベースまたはテーブルの部分データの復元をサポートします。この機能を使用すると、不要なデータを除外して、特定のデータベースまたはテーブルのみをバックアップできます。

### データベースを復元する {#restore-a-database}

データベースをクラスタに復元するには、 `br restore db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore db --help`コマンドを実行します。

例：AmazonS3の`backup-data`バケットの`db-test/2022-01-30/`ディレクトリからターゲットクラスタに`test`データベースを復元します。

{{< copyable "" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --log-file restore_db.log
```

上記のコマンドで、 `--db`は復元するデータベースの名前を指定し、その他のパラメーターは[TiDBクラスタスナップショットを復元する](#restore-tidb-cluster-snapshots)のパラメーターと同じです。

> **ノート：**
>
> バックアップデータを復元する場合、 `--db`で指定されたデータベース名は、backupコマンドで`-- db`で指定されたデータベース名と同じである必要があります。そうしないと、復元は失敗します。これは、バックアップデータのメタファイル（ `backupmeta`ファイル）にデータベース名が記録されており、同じ名前のデータベースにしかデータを復元できないためです。推奨される方法は、バックアップデータを別のクラスタの同じ名前のデータベースに復元することです。

### テーブルを復元する {#restore-a-table}

単一のテーブルをクラスタに復元するには、 `br restore table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore table --help`コマンドを実行します。

例：復元`test` 。 `table-db-usertable/2022-01-30/`の`backup-data`バケットの`usertable`ディレクトリからターゲットクラスタへ。

{{< copyable "" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://backup-data/table-db-usertable/2022-01-30/" \
    --log-file restore_table.log
```

上記のコマンドで、 `--table`は復元するテーブルの名前を指定し、その他のパラメーターは[TiDBクラスタスナップショットを復元する](#restore-tidb-cluster-snapshots)のパラメーターと同じです。

### テーブルフィルターを使用して複数のテーブルを復元する {#restore-multiple-tables-with-table-filter}

より多くの基準で複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 `--filter`または`-f`で[テーブルフィルター](/table-filter.md)を指定します。

例：AmazonS3の`backup-data`バケットの`table-filter/2022-01-30/`ディレクトリからターゲットクラスタに`db*.tbl*`テーブルに一致するデータを復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/"  \
    --log-file restorefull.log
```

## 外部ストレージからバックアップデータを復元する {#restore-backup-data-from-external-storage}

BRは、Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、NFS、またはその他のS3互換のファイルストレージサービスへのデータの復元をサポートしています。詳細については、次のドキュメントを参照してください。

-   [BRを使用してAmazonS3でデータを復元する](/br/backup-storage-S3.md)
-   [BRを使用してGoogleCloudStorageのデータを復元する](/br/backup-storage-gcs.md)
-   [BRを使用してAzureBlobStorageのデータを復元する](/br/backup-storage-azblob.md)

## 増分データを復元する {#restore-incremental-data}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

インクリメンタルデータの復元は、BRを使用した完全なデータの復元に似ています。インクリメンタルデータを復元するときは、 `last backup ts`がターゲットクラスタに復元される前にバックアップされたすべてのデータを確認してください。また、増分復元はtsデータを更新するため、復元中に他の書き込みがないことを確認する必要があります。そうしないと、競合が発生する可能性があります。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/incr"  \
    --ratelimit 128 \
    --log-file restorefull.log
```

## 暗号化されたバックアップデータを復元する {#restore-encrypted-backup-data}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

バックアップデータを暗号化した後、対応する復号化パラメータを渡してデータを復元する必要があります。復号化アルゴリズムとキーが正しいことを確認してください。復号化アルゴリズムまたはキーが正しくない場合、データを復元できません。

{{< copyable "" >}}

```shell
br restore full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

## <code>mysql</code>スキーマで作成されたテーブルを復元します {#restore-tables-created-in-the-code-mysql-code-schema}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

BRは、デフォルトで`mysql`スキーマで作成されたテーブルをバックアップします。 BRを使用してデータを復元する場合、 `mysql`スキーマで作成されたテーブルはデフォルトでは復元されません。これらのテーブルを復元するには、 [テーブルフィルター](/table-filter.md#syntax)を使用して明示的に含めることができます。次の例では、 `mysql`スキーマで作成された`mysql.usertable`を復元します。このコマンドは、他のデータとともに`mysql.usertable`を復元します。

{{< copyable "" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

上記のコマンドでは、

-   `-f '*.*'`はデフォルトのルールを上書きするために使用されます
-   `-f '!mysql.*'`は、特に明記されていない限り、BRに`mysql`のテーブルを復元しないように指示します。
-   `-f 'mysql.usertable'`は、 `mysql.usertable`を復元する必要があることを示します。

`mysql.usertable`を復元するだけでよい場合は、次のコマンドを実行します。

{{< copyable "" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **警告：**
>
> BRを使用してシステムテーブル（ `mysql.tidb`など）をバックアップできますが、-filter設定を使用して復元を実行した場合でも、BRは次のシステムテーブルを無視します。
>
> -   統計情報表（ `mysql.stat_*` ）
> -   システム変数`mysql.global_variables` `mysql.tidb`
> -   ユーザー情報テーブル（ `mysql.user`や`mysql.columns_priv`など）
> -   [その他のシステムテーブル](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)
>
> システムテーブルを復元するときに、互換性の問題が発生する可能性があります。したがって、実稼働環境でシステムテーブルを復元することは避けてください。

## 復元のパフォーマンスと影響 {#restoration-performance-and-impact}

-   TiDBは、データを復元するときにTiKV CPU、ディスクIO、ネットワーク帯域幅、およびその他のリソースを完全に使用します。したがって、実行中のサービスに影響を与えないように、空のクラスタでバックアップデータを復元することをお勧めします。
-   復元速度は、cluserの構成、展開、および実行中のサービスに大きく依存します。通常、復元速度は100 MB / s（TiKVノードあたり）に達する可能性があります。

> **ノート：**
>
> 多くのシナリオでのシミュレーションテストに基づいており、一部の顧客サイトで検証された前述のテストの結論は、参照する価値があります。ただし、復元速度はシナリオによって異なる場合があります。したがって、常にテストを実行し、テスト結果を確認する必要があります。
