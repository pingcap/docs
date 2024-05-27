---
title: br Command-line Manual
summary: br コマンドライン ツールは、TiDB クラスターのスナップショット バックアップ、ログ バックアップ、およびポイントインタイム リカバリ (PITR) に使用されます。サブコマンド、オプション、およびパラメーターで構成され、PD サービス アドレスの `--pd` やstorageパスの `-s` などの共通オプションがあります。サブコマンドには、それぞれ特定の機能を持つ `tiup br backup`、`tiup br log`、および `tiup br restore` が含まれます。バックアップ コマンドには `full`、`db`、および `table` オプションが含まれ、ログ バックアップ コマンドと復元コマンドには、バックアップ操作を管理するためのさまざまなタスクがあります。
---

# br コマンドラインマニュアル {#br-command-line-manual}

このドキュメントでは、 `br`のコマンドの定義、コンポーネント、共通オプション、および`br`コマンドを使用してスナップショットのバックアップと復元、ログのバックアップとポイントインタイムリカバリ (PITR) を実行する方法について説明します。

## <code>br</code>コマンドラインの説明 {#code-br-code-command-line-description}

`br`コマンドは、サブコマンド、オプション、およびパラメータで構成されます。サブコマンドは、 `-`または`--`のない文字です。オプションは、 `-`または`--`で始まる文字です。パラメータは、直後に続き、サブコマンドまたはオプションに渡される文字です。

以下は完全な`br`コマンドです。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-data/snapshot-202209081330/"
```

上記のコマンドの説明は次のとおりです。

-   `backup` : `tiup br`のサブコマンド。
-   `full` : `tiup br backup`のサブコマンド。
-   `-s` (または`--storage` ): バックアップ ファイルが保存されるパスを指定するオプション。4 `"s3://backup-data/snapshot-202209081330/"` `-s`のパラメーターです。
-   `--pd` : PD サービス アドレスを指定するオプション。2 `"${PD_IP}:2379"` `--pd`のパラメーターです。

### コマンドとサブコマンド {#commands-and-sub-commands}

`tiup br`コマンドは、複数のサブコマンドのレイヤーで構成されます。現在、br コマンドライン ツールには次のサブコマンドがあります。

-   `tiup br backup` : TiDB クラスターのデータをバックアップするために使用されます。
-   `tiup br log` : ログ バックアップ タスクを開始および管理するために使用されます。
-   `tiup br restore` : TiDB クラスターのバックアップ データを復元するために使用されます。

`tiup br backup`と`tiup br restore`次のサブコマンドが含まれます。

-   `full` : すべてのクラスター データをバックアップまたは復元するために使用されます。
-   `db` : クラスターの指定されたデータベースをバックアップまたは復元するために使用されます。
-   `table` : クラスターの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

### 共通オプション {#common-options}

-   `--pd` : PD サービス アドレスを指定します。たとえば、 `"${PD_IP}:2379"` 。
-   `-s` (または`--storage` ): バックアップ ファイルが保存されるパスを指定します。バックアップ データの保存には、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS がサポートされています。詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)を参照してください。
-   `--ca` : PEM 形式の信頼された CA 証明書へのパスを指定します。
-   `--cert` : PEM 形式の SSL 証明書へのパスを指定します。
-   `--key` : PEM 形式の SSL 証明書キーへのパスを指定します。
-   `--status-addr` : `br` Prometheus に統計情報を提供するリスニング アドレスを指定します。
-   `--concurrency` : バックアップまたは復元中の同時タスクの数。
-   `--compression` ：バックアップ ファイルの生成に使用する圧縮アルゴリズムを決定します。 `lz4` 、 `snappy` 、 `zstd`をサポートしており、デフォルトは`zstd`です (通常は変更する必要はありません)。さまざまな圧縮アルゴリズムの選択に関するガイダンスについては、 [このドキュメント](https://github.com/EighteenZi/rocksdb_wiki/blob/master/Compression.md)を参照してください。
-   `--compression-level` ：バックアップ用に選択した圧縮アルゴリズムに対応する圧縮レベルを設定します。 `zstd`のデフォルトの圧縮レベルは 3 です。ほとんどの場合、このオプションを設定する必要はありません。

## フルバックアップのコマンド {#commands-of-full-backup}

クラスターデータをバックアップするには、 `tiup br backup`コマンドを実行します。3 または`full`サブコマンドを追加して、バックアップ操作の範囲`table`クラスター全体 ( `full` ) または単一のテーブル ( `table` )）を指定できます。

-   [TiDB クラスターのスナップショットをバックアップする](/br/br-snapshot-manual.md#back-up-cluster-snapshots)
-   [データベースをバックアップする](/br/br-snapshot-manual.md#back-up-a-database)
-   [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)
-   [テーブルフィルターを使用して複数のテーブルをバックアップする](/br/br-snapshot-manual.md#back-up-multiple-tables-with-table-filter)
-   [スナップショットを暗号化する](/br/backup-and-restore-storages.md#server-side-encryption)

## ログバックアップのコマンド {#commands-of-log-backup}

ログ バックアップを開始し、ログ バックアップ タスクを管理するには、 `tiup br log`コマンドを実行します。

-   [ログバックアップタスクを開始する](/br/br-pitr-manual.md#start-a-backup-task)
-   [バックアップステータスを照会する](/br/br-pitr-manual.md#query-the-backup-status)
-   [ログバックアップタスクを一時停止して再開する](/br/br-pitr-manual.md#pause-and-resume-a-backup-task)
-   [ログバックアップタスクを停止して再開する](/br/br-pitr-manual.md#stop-and-restart-a-backup-task)
-   [バックアップデータをクリーンアップする](/br/br-pitr-manual.md#clean-up-backup-data)
-   [バックアップメタデータをビュー](/br/br-pitr-manual.md#view-the-backup-metadata)

## バックアップデータを復元するコマンド {#commands-of-restoring-backup-data}

クラスターデータを復元するには、 `tiup br restore`コマンドを実行します。 `full` 、 `db` 、または`table`サブコマンドを追加して、復元の範囲（クラスター全体 ( `full` )、単一のデータベース ( `db` )、または単一のテーブル ( `table` )）を指定できます。

-   [ポイントインタイムリカバリ](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)
-   [クラスタースナップショットを復元する](/br/br-snapshot-manual.md#restore-cluster-snapshots)
-   [データベースを復元する](/br/br-snapshot-manual.md#restore-a-database)
-   [テーブルを復元する](/br/br-snapshot-manual.md#restore-a-table)
-   [テーブルフィルターを使用して複数のテーブルを復元する](/br/br-snapshot-manual.md#restore-multiple-tables-with-table-filter)
-   [暗号化されたスナップショットを復元する](/br/br-snapshot-manual.md#restore-encrypted-snapshots)
