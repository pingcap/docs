---
title: Use BR to Restore Cluster Data
summary: Learn how to restore data using BR commands
---

# BR を使用してクラスタデータを復元する {#use-br-to-restore-cluster-data}

このドキュメントでは、次のシナリオで TiDB クラスター データを復元する方法について説明します。

-   [TiDB クラスターのスナップショットを復元する](#restore-tidb-cluster-snapshots)
-   [データベースを復元する](#restore-a-database)
-   [テーブルを復元する](#restore-a-table)
-   [テーブル フィルターを使用して複数のテーブルを復元する](#restore-multiple-tables-with-table-filter)
-   [外部ストレージからバックアップ データを復元する](#restore-backup-data-from-external-storage)
-   [増分データの復元](#restore-incremental-data)
-   [暗号化されたバックアップ データを復元する](#restore-encrypted-backup-data)
-   [`mysql`スキーマで作成されたテーブルを復元する](#restore-tables-created-in-the-mysql-schema)

バックアップ ツールと復元ツールに慣れていない場合は、次のドキュメントを読んで、これらのツールの使用原理と方法を完全に理解することをお勧めします。

-   [BRの概要](/br/backup-and-restore-overview.md)
-   [バックアップと復元に BR コマンドラインを使用する](/br/use-br-command-line-tool.md)

Dumpling、CSV ファイル、または Amazon Auroraによって生成された Apache Parquet ファイルによってエクスポートされたデータを復元する必要がある場合は、 TiDB Lightningを使用してデータをインポートし、復元を実装できます。詳細については、 [TiDB Lightningを使用して完全なデータを復元する](/backup-and-restore-using-dumpling-lightning.md#use-tidb-lightning-to-restore-full-data)を参照してください。

## TiDB クラスターのスナップショットを復元する {#restore-tidb-cluster-snapshots}

BR は、空のクラスターでのスナップショット バックアップの復元をサポートし、スナップショットのバックアップ時にターゲット クラスターを最新の状態に復元します。

例: Amazon S3 の`backup-data`バケットの`2022-01-30/`ディレクトリから`2022-01-30 07:42:23`で生成されたスナップショットをターゲット クラスタに復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
```

前のコマンドでは、

-   `--ratelimit` :**各 TiKV**が復元タスクを実行する最大速度 (単位: MiB/s)
-   `--log-file` BR ロギングの対象ファイル

復元中は、以下に示すように、進行状況バーがターミナルに表示されます。プログレス バーが 100% まで進むと、復元は完了です。データのセキュリティを確保するために、BR は復元されたデータに対してチェックを実行します。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

## データベースまたはテーブルを復元する {#restore-a-database-or-a-table}

BR は、指定されたデータベースまたはテーブルの部分データをバックアップ データから復元することをサポートします。この機能を使用すると、不要なデータを除外して、特定のデータベースまたはテーブルのみをバックアップできます。

### データベースを復元する {#restore-a-database}

データベースをクラスターに復元するには、 `br restore db`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore db --help`コマンドを実行します。

例: Amazon S3 の`backup-data`バケットの`db-test/2022-01-30/`ディレクトリから`test`データベースをターゲット クラスタに復元します。

{{< copyable "" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://backup-data/db-test/2022-01-30/" \
    --log-file restore_db.log
```

上記のコマンドで、 `--db`は復元するデータベースの名前を指定し、その他のパラメーターは[TiDB クラスターのスナップショットを復元する](#restore-tidb-cluster-snapshots)と同じです。

> **ノート：**
>
> バックアップデータを復元する場合、 `--db`で指定したデータベース名は、バックアップコマンドの`-- db`で指定したデータベース名と同じでなければなりません。そうしないと、復元は失敗します。これは、バックアップ データのメタファイル ( `backupmeta`ファイル) にデータベース名が記録されており、同じ名前のデータベースにしかデータを復元できないためです。推奨される方法は、バックアップ データを別のクラスター内の同じ名前のデータベースに復元することです。

### テーブルを復元する {#restore-a-table}

1 つのテーブルをクラスターに復元するには、 `br restore table`コマンドを実行します。このコマンドのヘルプを表示するには、 `br restore table --help`コマンドを実行します。

例: `test`を復元します。 `usertable` Amazon S3 の`backup-data`バケット内の`table-db-usertable/2022-01-30/`ディレクトリからターゲット クラスタへ。

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

上記のコマンドで、 `--table`は復元するテーブルの名前を指定し、その他のパラメーターは[TiDB クラスターのスナップショットを復元する](#restore-tidb-cluster-snapshots)と同じです。

### テーブル フィルターを使用して複数のテーブルを復元する {#restore-multiple-tables-with-table-filter}

複数の基準で複数のテーブルを復元するには、 `br restore full`コマンドを実行し、 `--filter`または`-f`で[テーブル フィルター](/table-filter.md)を指定します。

例: Amazon S3 の`backup-data`バケットの`table-filter/2022-01-30/`ディレクトリから`db*.tbl*`テーブルに一致するデータをターゲット クラスタに復元します。

{{< copyable "" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://backup-data/table-filter/2022-01-30/"  \
    --log-file restorefull.log
```

## 外部ストレージからバックアップ データを復元する {#restore-backup-data-from-external-storage}

BR は、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS、またはその他の S3 互換ファイル ストレージ サービスへのデータの復元をサポートしています。詳細については、次のドキュメントを参照してください。

-   [BR を使用して Amazon S3 にデータを復元する](/br/backup-storage-S3.md)
-   [BR を使用して Google Cloud Storage にデータを復元する](/br/backup-storage-gcs.md)
-   [BR を使用して Azure Blob Storage にデータを復元する](/br/backup-storage-azblob.md)

## 増分データの復元 {#restore-incremental-data}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

増分データの復元は、BR を使用した完全なデータの復元に似ています。増分データを復元する場合は、 `last backup ts`より前にバックアップされたすべてのデータがターゲット クラスターに復元されていることを確認してください。また、増分復元では ts データが更新されるため、復元中に他の書き込みが行われないようにする必要があります。そうしないと、競合が発生する可能性があります。

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://backup-data/2022-01-30/incr"  \
    --ratelimit 128 \
    --log-file restorefull.log
```

## 暗号化されたバックアップ データを復元する {#restore-encrypted-backup-data}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

バックアップ データを暗号化したら、対応する復号化パラメータを渡してデータを復元する必要があります。復号化アルゴリズムとキーが正しいことを確認してください。復号化アルゴリズムまたはキーが正しくない場合、データは復元できません。

{{< copyable "" >}}

```shell
br restore full\
    --pd ${PDIP}:2379 \
    --storage "s3://backup-data/2022-01-30/" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

## <code>mysql</code>スキーマで作成されたテーブルを復元する {#restore-tables-created-in-the-code-mysql-code-schema}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することはお勧めし**ません**。

BR は、デフォルトで`mysql`スキーマで作成されたテーブルをバックアップします。 BR を使用してデータを復元する場合、 `mysql`スキーマで作成されたテーブルはデフォルトでは復元されません。これらのテーブルを復元するには、 [テーブル フィルター](/table-filter.md#syntax)を使用して明示的に含めることができます。次の例では、 `mysql`スキーマで作成された`mysql.usertable`を復元します。このコマンドは、他のデータとともに`mysql.usertable`を復元します。

{{< copyable "" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

前のコマンドでは、

-   `-f '*.*'`は、デフォルトのルールをオーバーライドするために使用されます
-   `-f '!mysql.*'`は、特に明記されていない限り、 `mysql`でテーブルを復元しないように BR に指示します。
-   `-f 'mysql.usertable'`は、 `mysql.usertable`を復元する必要があることを示します。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを実行します。

{{< copyable "" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **警告：**
>
> BR を使用してシステム テーブル ( `mysql.tidb`など) をバックアップできますが、 --filter 設定を使用して復元を実行しても、BR は次のシステム テーブルを無視します。
>
> -   統計情報表 ( `mysql.stat_*` )
> -   システム変数テーブル ( `mysql.tidb` 、 `mysql.global_variables` )
> -   ユーザー情報テーブル ( `mysql.user`や`mysql.columns_priv`など)
> -   [その他のシステム テーブル](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)
>
> システム テーブルを復元するときに、互換性の問題が発生する場合があります。したがって、実稼働環境でシステム テーブルを復元することは避けてください。

## 復元性能と影響 {#restoration-performance-and-impact}

-   TiDB は、データの復元時に TiKV CPU、ディスク IO、ネットワーク帯域幅、およびその他のリソースを完全に使用します。したがって、実行中のサービスに影響を与えないように、空のクラスターにバックアップ データを復元することをお勧めします。
-   復元速度は、クラスター構成、展開、および実行中のサービスに大きく依存します。通常、復元速度は 100 MB/秒 (TiKV ノードあたり) に達することがあります。

> **ノート：**
>
> 多くのシナリオでのシミュレーション テストに基づき、一部の顧客サイトで検証された前述のテストの結論は、参照に値します。ただし、復元速度はシナリオによって異なる場合があります。したがって、常にテストを実行し、テスト結果を確認する必要があります。
