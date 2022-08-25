---
title: Use BR Command-line for Backup and Restoration
summary: Learn how to use the BR command line to back up and restore cluster data.
---

# バックアップと復元に BR コマンドラインを使用する {#use-br-command-line-for-backup-and-restoration}

このドキュメントでは、BR コマンド ラインを使用して TiDBクラスタデータをバックアップおよび復元する方法について説明します。

[BR ツールの概要](/br/backup-and-restore-overview.md) 、特に[利用制限](/br/backup-and-restore-overview.md#usage-restrictions)と[いくつかのヒント](/br/backup-and-restore-overview.md#some-tips)を読んだことを確認してください。

## BR コマンドラインの説明 {#br-command-line-description}

`br`コマンドは、サブコマンド、オプション、およびパラメーターで構成されます。

-   サブコマンド: `-`または`--`のない文字。
-   オプション: `-`または`--`で始まる文字。
-   パラメータ: 直後に続き、サブコマンドまたはオプションに渡される文字。

これは完全な`br`のコマンドです。

{{< copyable "" >}}

```shell
`br backup full --pd "${PDIP}:2379" -s "s3://backup-data/2022-01-30/"`
```

上記のコマンドの説明は次のとおりです。

-   `backup` : `br`のサブコマンド。
-   `full` : `backup`のサブコマンド。
-   `-s` (または`--storage` ): バックアップ ファイルが格納されるパスを指定するオプション。
-   `"s3://backup-data/2022-01-30/"` : `-s`のパラメータ。バックアップ データが Amazon S3 の`backup-data`バケットの`2022-01-30/`ディレクトリに保存されることを示します。
-   `--pd` : Placement Driver (PD) サービス アドレスを指定するオプション。
-   `"${PDIP}:2379"` : `--pd`のパラメーター。

### サブコマンド {#sub-commands}

`br`のコマンドは、サブコマンドの複数のレイヤーで構成されます。現在、BR には次のサブコマンドがあります。

-   `br backup` : TiDBクラスタのデータをバックアップするために使用されます。
-   `br restore` : TiDBクラスタのデータを復元するために使用されます。

上記の各サブコマンドには、操作の範囲を指定する次のサブコマンドが含まれる場合があります。

-   `full` : すべてのクラスタデータのバックアップまたは復元に使用されます。
-   `db` :クラスタの指定されたデータベースのバックアップまたは復元に使用されます。
-   `table` :クラスタの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

### 共通オプション {#common-options}

-   `--pd` : 接続に使用され、PD サーバーのアドレスを指定します。たとえば、 `"${PDIP}:2379"`です。
-   `-h` (または`--help` ): すべてのサブコマンドのヘルプを取得するために使用されます。たとえば、 `br backup --help`です。
-   `-V` (または`--version` ): BR のバージョンを確認するために使用されます。
-   `--ca` : 信頼できる CA 証明書へのパスを PEM 形式で指定します。
-   `--cert` : SSL 証明書へのパスを PEM 形式で指定します。
-   `--key` : SSL 証明書キーへのパスを PEM 形式で指定します。
-   `--status-addr` : BR が Prometheus に統計情報を提供するためのリスニング アドレスを指定します。

## BR コマンドラインを使用してクラスタデータをバックアップする例 {#examples-of-using-br-command-line-to-back-up-cluster-data}

クラスタデータをバックアップするには、 `br backup`コマンドを実行します。 `full`または`table`サブコマンドを追加して、バックアップ操作の範囲 (クラスタ全体または単一のテーブル) を指定できます。

-   [TiDBクラスタのスナップショットをバックアップする](/br/br-usage-backup.md#back-up-tidb-cluster-snapshots)
-   [データベースのバックアップ](/br/br-usage-backup.md#back-up-a-database)
-   [テーブルをバックアップする](/br/br-usage-backup.md#back-up-a-table)
-   [テーブル フィルターを使用して複数のテーブルをバックアップする](/br/br-usage-backup.md#back-up-multiple-tables-with-table-filter)
-   [BR を使用して Amazon S3 にデータをバックアップする](/br/backup-storage-S3.md)
-   [BR を使用して Google Cloud Storage にデータをバックアップする](/br/backup-storage-gcs.md)
-   [BR を使用して Azure Blob Storage 上のデータをバックアップする](/br/backup-storage-azblob.md)
-   [増分データのバックアップ](/br/br-usage-backup.md#back-up-incremental-data)
-   [バックアップ中にデータを暗号化する](/br/br-usage-backup.md#encrypt-backup-data-at-the-backup-end)

## BR コマンドラインを使用してクラスタデータを復元する例 {#examples-of-using-br-command-line-to-restore-cluster-data}

クラスタデータを復元するには、 `br restore`コマンドを実行します。 `full` 、 `db` 、または`table`サブコマンドを追加して、復元の範囲 (クラスタ全体、データベース、または単一のテーブル) を指定できます。

-   [TiDBクラスタのスナップショットを復元する](/br/br-usage-restore.md#restore-tidb-cluster-snapshots)
-   [データベースを復元する](/br/br-usage-restore.md#restore-a-database)
-   [テーブルを復元する](/br/br-usage-restore.md#restore-a-table)
-   [テーブル フィルターを使用して複数のテーブルを復元する](/br/br-usage-restore.md#restore-multiple-tables-with-table-filter)
-   [BR を使用して Amazon S3 にデータを復元する](/br/backup-storage-S3.md)
-   [BR を使用して Google Cloud Storage にデータを復元する](/br/backup-storage-gcs.md)
-   [BR を使用して Azure Blob Storage にデータを復元する](/br/backup-storage-azblob.md)
-   [増分データの復元](/br/br-usage-restore.md#restore-incremental-data)
-   [暗号化されたバックアップ データを復元する](/br/br-usage-restore.md#restore-encrypted-backup-data)
