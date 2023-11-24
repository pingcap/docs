---
title: br Command-line Manual
summary: Learn about the description, options, and usage of the br command-line tool.
---

# br コマンドラインマニュアル {#br-command-line-manual}

このドキュメントでは、 `br`のコマンドの定義、コンポーネント、共通オプション、および`br`コマンドを使用してスナップショット バックアップと復元、ログ バックアップとポイントインタイム リカバリ (PITR) を実行する方法について説明します。

## <code>br</code>コマンドラインの説明 {#code-br-code-command-line-description}

`br`コマンドは、サブコマンド、オプション、パラメータで構成されます。サブコマンドは`-`または`--`を除いた文字です。オプションは`-`または`--`で始まる文字です。パラメータは直後に続く文字で、サブコマンドまたはオプションに渡されます。

以下は完全な`br`コマンドです。

```shell
br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-data/snapshot-202209081330/"
```

前述のコマンドの説明は次のとおりです。

-   `backup` : `br`のサブコマンド。
-   `full` : `br backup`のサブコマンド。
-   `-s` (または`--storage` ): バックアップ ファイルが保存されるパスを指定するオプション。 `"s3://backup-data/snapshot-202209081330/"` `-s`のパラメータです。
-   `--pd` : PDサービスアドレスを指定するオプション。 `"${PD_IP}:2379"` `--pd`のパラメータです。

### コマンドとサブコマンド {#commands-and-sub-commands}

`br`コマンドは複数層のサブコマンドで構成されます。現在、br コマンドライン ツールには次のサブコマンドがあります。

-   `br backup` : TiDB クラスターのデータのバックアップに使用されます。
-   `br log` : ログ バックアップ タスクの開始と管理に使用されます。
-   `br restore` : TiDB クラスターのバックアップ データを復元するために使用されます。

`br backup`と`br restore`には次のサブコマンドが含まれます。

-   `full` : すべてのクラスター データのバックアップまたは復元に使用されます。
-   `db` : クラスターの指定されたデータベースのバックアップまたは復元に使用されます。
-   `table` : クラスターの指定されたデータベース内の単一テーブルをバックアップまたは復元するために使用されます。

### 共通オプション {#common-options}

-   `--pd` : PDサービスアドレスを指定します。たとえば、 `"${PD_IP}:2379"` 。
-   `-s` (または`--storage` ): バックアップ ファイルが保存されるパスを指定します。バックアップ データの保存には、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、NFS がサポートされています。詳細については[外部ストレージ サービスの URI 形式](/external-storage-uri.md)を参照してください。
-   `--ca` : 信頼できる CA 証明書へのパスを PEM 形式で指定します。
-   `--cert` : PEM 形式の SSL 証明書へのパスを指定します。
-   `--key` : SSL 証明書キーへのパスを PEM 形式で指定します。
-   `--status-addr` : `br` Prometheus に統計を提供する際に使用するリスニング アドレスを指定します。
-   `--concurrency` : バックアップまたは復元中の同時タスクの数。

## フルバックアップのコマンド {#commands-of-full-backup}

クラスターデータをバックアップするには、 `br backup`コマンドを実行します。 `full`または`table`サブコマンドを追加して、バックアップ操作の範囲 (クラスター全体 ( `full` ) または単一のテーブル ( `table` )) を指定できます。

-   [TiDB クラスターのスナップショットをバックアップする](/br/br-snapshot-manual.md#back-up-cluster-snapshots)
-   [データベースをバックアップする](/br/br-snapshot-manual.md#back-up-a-database)
-   [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)
-   [テーブルフィルターを使用して複数のテーブルをバックアップする](/br/br-snapshot-manual.md#back-up-multiple-tables-with-table-filter)
-   [スナップショットの暗号化](/br/backup-and-restore-storages.md#server-side-encryption)

## ログバックアップのコマンド {#commands-of-log-backup}

ログ バックアップを開始し、ログ バックアップ タスクを管理するには、 `br log`コマンドを実行します。

-   [ログバックアップタスクを開始する](/br/br-pitr-manual.md#start-a-backup-task)
-   [バックアップステータスを問い合わせる](/br/br-pitr-manual.md#query-the-backup-status)
-   [ログバックアップタスクの一時停止と再開](/br/br-pitr-manual.md#pause-and-resume-a-backup-task)
-   [ログバックアップタスクを停止して再開する](/br/br-pitr-manual.md#stop-and-restart-a-backup-task)
-   [バックアップデータをクリーンアップする](/br/br-pitr-manual.md#clean-up-backup-data)
-   [バックアップのメタデータをビュー](/br/br-pitr-manual.md#view-the-backup-metadata)

## バックアップデータを復元するコマンド {#commands-of-restoring-backup-data}

クラスターデータを復元するには、 `br restore`コマンドを実行します。 `full` 、 `db` 、または`table`サブコマンドを追加して、リストアの範囲 (クラスター全体 ( `full` )、単一データベース ( `db` )、または単一テーブル ( `table` )) を指定できます。

-   [ポイントインタイムリカバリ](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)
-   [クラスターのスナップショットを復元する](/br/br-snapshot-manual.md#restore-cluster-snapshots)
-   [データベースを復元する](/br/br-snapshot-manual.md#restore-a-database)
-   [テーブルを復元する](/br/br-snapshot-manual.md#restore-a-table)
-   [テーブルフィルターを使用して複数のテーブルを復元する](/br/br-snapshot-manual.md#restore-multiple-tables-with-table-filter)
-   [暗号化されたスナップショットを復元する](/br/br-snapshot-manual.md#restore-encrypted-snapshots)
