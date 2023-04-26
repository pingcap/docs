---
title: br Command-line Manual
summary: Learn about the description, options, and usage of the br command-line tool.
---

# br コマンドラインマニュアル {#br-command-line-manual}

このドキュメントでは、 `br`コマンドの定義、コンポーネント、共通オプション、および`br`コマンドを使用してスナップショット バックアップと復元、およびログ バックアップとポイント イン タイム リカバリ (PITR) を実行する方法について説明します。

## <code>br</code>コマンドラインの説明 {#code-br-code-command-line-description}

`br`コマンドは、サブコマンド、オプション、およびパラメーターで構成されます。サブコマンドは`-`または`--`を除いた文字です。オプションは`-`または`--`で始まる文字です。パラメータは、直後に続く文字で、サブコマンドまたはオプションに渡されます。

以下は完全な`br`コマンドです。

```shell
br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-data/snapshot-202209081330/"
```

上記のコマンドの説明は次のとおりです。

-   `backup` : `br`のサブコマンド。
-   `full` : `br backup`のサブコマンド。
-   `-s` (または`--storage` ): バックアップ ファイルが格納されるパスを指定するオプション。 `"s3://backup-data/snapshot-202209081330/"` `-s`のパラメータです。
-   `--pd` : PD サービス アドレスを指定するオプション。 `"${PD_IP}:2379"` `--pd`のパラメータです。

### コマンドとサブコマンド {#commands-and-sub-commands}

`br`コマンドは、サブコマンドの複数のレイヤーで構成されます。現在、br コマンドライン ツールには次のサブコマンドがあります。

-   `br backup` : TiDB クラスターのデータをバックアップするために使用されます。
-   `br log` : ログ バックアップ タスクの開始と管理に使用されます。
-   `br restore` : TiDB クラスターのバックアップ データを復元するために使用されます。

`br backup`と`br restore`には、次のサブコマンドが含まれます。

-   `full` : すべてのクラスター データのバックアップまたは復元に使用されます。
-   `db` : クラスターの指定されたデータベースのバックアップまたは復元に使用されます。
-   `table` : クラスターの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

### 共通オプション {#common-options}

-   `--pd` : PD サービス アドレスを指定します。たとえば、 `"${PD_IP}:2379"`です。
-   `-s` (または`--storage` ): バックアップ ファイルが格納されるパスを指定します。バックアップ データの保存には、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、および NFS がサポートされています。詳細については、 [バックアップ ストレージの URL 形式](/br/backup-and-restore-storages.md#url-format)を参照してください。
-   `--ca` : 信頼できる CA 証明書へのパスを PEM 形式で指定します。
-   `--cert` : SSL 証明書へのパスを PEM 形式で指定します。
-   `--key` : SSL 証明書キーへのパスを PEM 形式で指定します。
-   `--status-addr` : `br` Prometheus に統計を提供するためのリスニング アドレスを指定します。

## フルバックアップのコマンド {#commands-of-full-backup}

クラスター データをバックアップするには、 `br backup`コマンドを実行します。 `full`または`table`サブコマンドを追加して、バックアップ操作の範囲 (クラスター全体 ( `full` ) または単一のテーブル ( `table` )) を指定できます。

-   [TiDB クラスターのスナップショットをバックアップする](/br/br-snapshot-manual.md#back-up-cluster-snapshots)
-   [データベースのバックアップ](/br/br-snapshot-manual.md#back-up-a-database)
-   [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)
-   [テーブル フィルターを使用して複数のテーブルをバックアップする](/br/br-snapshot-manual.md#back-up-multiple-tables-with-table-filter)
-   [スナップショットを暗号化する](/br/backup-and-restore-storages.md#server-side-encryption)

## ログバックアップのコマンド {#commands-of-log-backup}

ログ バックアップを開始し、ログ バックアップ タスクを管理するには、 `br log`コマンドを実行します。

-   [ログ バックアップ タスクを開始する](/br/br-pitr-manual.md#start-a-backup-task)
-   [バックアップ ステータスのクエリ](/br/br-pitr-manual.md#query-the-backup-status)
-   [ログ バックアップ タスクの一時停止と再開](/br/br-pitr-manual.md#pause-and-resume-a-backup-task)
-   [ログ バックアップ タスクを停止して再開する](/br/br-pitr-manual.md#stop-and-restart-a-backup-task)
-   [バックアップ データのクリーンアップ](/br/br-pitr-manual.md#clean-up-backup-data)
-   [バックアップ メタデータをビュー](/br/br-pitr-manual.md#view-the-backup-metadata)

## バックアップデータを復元するコマンド {#commands-of-restoring-backup-data}

クラスター データを復元するには、 `br restore`コマンドを実行します。 `full` 、 `db` 、または`table`サブコマンドを追加して、復元の範囲 (クラスター全体 ( `full` )、単一データベース ( `db` )、または単一テーブル ( `table` )) を指定できます。

-   [ポイントインタイム リカバリ](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)
-   [クラスターのスナップショットを復元する](/br/br-snapshot-manual.md#restore-cluster-snapshots)
-   [データベースを復元する](/br/br-snapshot-manual.md#restore-a-database)
-   [テーブルを復元する](/br/br-snapshot-manual.md#restore-a-table)
-   [テーブル フィルターを使用して複数のテーブルを復元する](/br/br-snapshot-manual.md#restore-multiple-tables-with-table-filter)
-   [暗号化されたスナップショットを復元する](/br/br-snapshot-manual.md#restore-encrypted-snapshots)
