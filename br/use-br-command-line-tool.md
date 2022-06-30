---
title: Use BR Command-line for Backup and Restoration
summary: Learn how to use the BR command line to back up and restore cluster data.
---

# バックアップと復元にBRコマンドラインを使用する {#use-br-command-line-for-backup-and-restoration}

このドキュメントでは、BRコマンドラインを使用してTiDBクラスタデータをバックアップおよび復元する方法について説明します。

[BRツールの概要](/br/backup-and-restore-overview.md) 、特に[使用制限](/br/backup-and-restore-overview.md#usage-restrictions)と[いくつかのヒント](/br/backup-and-restore-overview.md#some-tips)を読んだことを確認してください。

## BRコマンドラインの説明 {#br-command-line-description}

`br`コマンドは、サブコマンド、オプション、およびパラメーターで構成されます。

-   サブコマンド： `-`または`--`のない文字。
-   オプション： `-`または`--`で始まる文字。
-   パラメーター：直後に続き、サブコマンドまたはオプションに渡される文字。

これは完全な`br`のコマンドです。

{{< copyable "" >}}

```shell
`br backup full --pd "${PDIP}:2379" -s "s3://backup-data/2022-01-30/"`
```

上記のコマンドの説明は次のとおりです。

-   `backup` ： `br`のサブコマンド。
-   `full` ： `backup`のサブコマンド。
-   `-s` （または`--storage` ）：バックアップファイルが保存されるパスを指定するオプション。
-   `"s3://backup-data/2022-01-30/"` ：パラメータ`-s`これは、バックアップデータがAmazonS3の`backup-data`バケットの`2022-01-30/`ディレクトリに保存されていることを示します。
-   `--pd` ：配置ドライバー（PD）サービスアドレスを指定するオプション。
-   `"${PDIP}:2379"` ： `--pd`のパラメータ。

### サブコマンド {#sub-commands}

`br`のコマンドは、サブコマンドの複数のレイヤーで構成されます。現在、BRには次のサブコマンドがあります。

-   `br backup` ：TiDBクラスタのデータをバックアップするために使用されます。
-   `br restore` ：TiDBクラスタのデータを復元するために使用されます。

上記の各サブコマンドには、操作の範囲を指定するための次のサブコマンドが含まれている場合があります。

-   `full` ：すべてのクラスタデータをバックアップまたは復元するために使用されます。
-   `db` ：クラスタの指定されたデータベースをバックアップまたは復元するために使用されます。
-   `table` ：クラスタの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

### 一般的なオプション {#common-options}

-   `--pd` ：接続に使用され、PDサーバーアドレスを指定します。たとえば、 `"${PDIP}:2379"` 。
-   `-h` （または`--help` ）：すべてのサブコマンドのヘルプを取得するために使用されます。たとえば、 `br backup --help` 。
-   `-V` （または`--version` ）：BRのバージョンを確認するために使用されます。
-   `--ca` ：信頼できるCA証明書へのパスをPEM形式で指定します。
-   `--cert` ：SSL証明書へのパスをPEM形式で指定します。
-   `--key` ：SSL証明書キーへのパスをPEM形式で指定します。
-   `--status-addr` ：BRがPrometheusに統計を提供するためのリスニングアドレスを指定します。

## BRコマンドラインを使用してクラスタデータをバックアップする例 {#examples-of-using-br-command-line-to-back-up-cluster-data}

クラスタデータをバックアップするには、 `br backup`コマンドを実行します。 `full`または`table`サブコマンドを追加して、バックアップ操作の範囲（クラスタ全体または単一のテーブル）を指定できます。

-   [TiDBクラスタスナップショットをバックアップします](/br/br-usage-backup.md#back-up-tidb-cluster-snapshots)
-   [データベースをバックアップする](/br/br-usage-backup.md#back-up-a-database)
-   [テーブルをバックアップする](/br/br-usage-backup.md#back-up-a-table)
-   [テーブルフィルターを使用して複数のテーブルをバックアップする](/br/br-usage-backup.md#back-up-multiple-tables-with-table-filter)
-   [BRを使用してAmazonS3でデータをバックアップする](/br/backup-storage-S3.md)
-   [BRを使用してGoogleCloudStorageにデータをバックアップする](/br/backup-storage-gcs.md)
-   [BRを使用してAzureBlobStorageのデータをバックアップする](/br/backup-storage-azblob.md)
-   [インクリメンタルデータをバックアップする](/br/br-usage-backup.md#back-up-incremental-data)
-   [バックアップ中にデータを暗号化する](/br/br-usage-backup.md#encrypt-backup-data-at-the-backup-end)

## BRコマンドラインを使用してクラスタデータを復元する例 {#examples-of-using-br-command-line-to-restore-cluster-data}

クラスタデータを復元するには、 `br restore`コマンドを実行します。 `full` 、または`db`サブコマンドを追加して、復元の範囲（クラスタ全体、データベース、または単一のテーブル）を指定でき`table` 。

-   [TiDBクラスタスナップショットを復元する](/br/br-usage-restore.md#restore-tidb-cluster-snapshots)
-   [データベースを復元する](/br/br-usage-restore.md#restore-a-database)
-   [テーブルを復元する](/br/br-usage-restore.md#restore-a-table)
-   [テーブルフィルターを使用して複数のテーブルを復元する](/br/br-usage-restore.md#restore-multiple-tables-with-table-filter)
-   [BRを使用してAmazonS3でデータを復元する](/br/backup-storage-S3.md)
-   [BRを使用してGoogleCloudStorageのデータを復元する](/br/backup-storage-gcs.md)
-   [BRを使用してAzureBlobStorageのデータを復元する](/br/backup-storage-azblob.md)
-   [増分データを復元する](/br/br-usage-restore.md#restore-incremental-data)
-   [暗号化されたバックアップデータを復元する](/br/br-usage-restore.md#restore-encrypted-backup-data)
