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
-   [`mysql`スキーマのテーブルを復元する](#restore-tables-in-the-mysql-schema)

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

## <code>mysql</code>スキーマのテーブルを復元する {#restore-tables-in-the-code-mysql-code-schema}

BR v5.1.0 以降、フル バックアップを実行すると、BR は**システム テーブル**をバックアップします。 BR v6.2.0 より前のデフォルト構成では、BR はユーザー データのみを復元し、システム テーブル内のデータは復元しません。 BR v6.2.0 以降、バックアップ データにシステム テーブルが含まれている場合、 `--with-sys-table`を構成すると、BR は<strong>一部のシステム テーブルのデータを</strong>復元します。

BR は**、次のシステム テーブルの**データを復元できます。

```
+----------------------------------+
| mysql.columns_priv               |
| mysql.db                         |
| mysql.default_roles              |
| mysql.global_grants              |
| mysql.global_priv                |
| mysql.role_edges                 |
| mysql.tables_priv                |
| mysql.user                       |
+----------------------------------+
```

**BR は、次のシステム テーブルを復元しません**。

-   統計表 ( `mysql.stat_*` )
-   システム変数テーブル ( `mysql.tidb` 、 `mysql.global_variables` )
-   [その他のシステム テーブル](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/systable_restore.go#L31)

システム権限に関連するデータを復元する場合は、次の点に注意してください。

-   BR は、 `user`を`cloud_admin`として、 `host`を`'%'`としてユーザー データを復元しません。このユーザーはTiDB Cloud用に予約されています。 `cloud_admin`に関連するユーザー権限を正しく復元できないため、ご使用の環境で`cloud_admin`という名前のユーザーまたはロールを作成しないでください。
-   BR は、データを復元する前に、ターゲット クラスタ内のシステム テーブルがバックアップ データ内のシステム テーブルと互換性があるかどうかをチェックします。 「互換性がある」とは、次のすべての条件が満たされていることを意味します。

    -   ターゲット クラスタには、バックアップ データと同じシステム テーブルがあります。
    -   対象クラスタのシステム権限テーブル**の列数が**バックアップデータの列数と一致している。列の順序は異なる場合があります。
    -   ターゲット クラスタのシステム権限テーブルの列は、バックアップ データの列と互換性があります。列のデータ型が長さのある型 (int や char など) の場合、ターゲット クラスターの長さはバックアップ データの長さ以上である必要があります。列のデータ型が列挙型の場合、ターゲット クラスターの列挙値は、バックアップ データの列挙値のスーパーセットである必要があります。

ターゲット クラスタが空でない場合、またはターゲット クラスタがバックアップ データと互換性がない場合、BR は次の情報を返します。 `--with-sys-table`を削除すると、システム テーブルの復元をスキップできます。

```
#######################################################################
# the target cluster is not compatible with the backup data,
# br cannot restore system tables.
# you can remove 'with-sys-table' flag to skip restoring system tables
#######################################################################
```

`mysql`スキーマ (システム テーブルではない) でユーザーが作成したテーブルを復元するには、 [テーブル フィルター](/table-filter.md#syntax)を使用して明示的にテーブルを含めることができます。次の例は、BR が通常の復元を実行するときに`mysql.usertable`テーブルを復元する方法を示しています。

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

前のコマンドでは、

-   `-f '*.*'`は、デフォルトのルールをオーバーライドするために使用されます
-   `-f '!mysql.*'`は、特に明記されていない限り、 `mysql`でテーブルを復元しないように BR に指示します。
-   `-f 'mysql.usertable'`は、 `mysql.usertable`を復元する必要があることを示します。

`mysql.usertable`のみを復元する必要がある場合は、次のコマンドを実行します。

{{< copyable "" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --with-sys-table
```

## 復元性能と影響 {#restoration-performance-and-impact}

-   TiDB は、データの復元時に TiKV CPU、ディスク IO、ネットワーク帯域幅、およびその他のリソースを完全に使用します。したがって、実行中のサービスに影響を与えないように、空のクラスターにバックアップ データを復元することをお勧めします。
-   復元速度は、クラスター構成、展開、および実行中のサービスに大きく依存します。通常、復元速度は 100 MB/秒 (TiKV ノードあたり) に達することがあります。

> **ノート：**
>
> 多くのシナリオでのシミュレーション テストに基づき、一部の顧客サイトで検証された前述のテストの結論は、参照に値します。ただし、復元速度はシナリオによって異なる場合があります。したがって、常にテストを実行し、テスト結果を確認する必要があります。
