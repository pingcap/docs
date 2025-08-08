---
title: br Command-line Manual
summary: br` コマンドラインツールは、TiDB クラスターのスナップショットバックアップ、ログバックアップ、およびポイントインタイムリカバリ (PITR) に使用されます。サブコマンド、オプション、およびパラメータで構成されており、PD サービスアドレスの `--pd` やstorageパスの `-s` などの共通オプションがあります。サブコマンドには、それぞれ特定の機能を持つ `tiup br backup`、`tiup br log`、`tiup br restore` などがあります。バックアップコマンドには `full`、`db`、`table` オプションがあり、ログバックアップおよびリストアコマンドには、バックアップ操作を管理するためのさまざまなタスクがあります。
---

# br コマンドラインマニュアル {#br-command-line-manual}

このドキュメントでは、 `br`コマンドの定義、コンポーネント、共通オプション、および`br`コマンドを使用してスナップショットのバックアップと復元、ログのバックアップとポイントインタイムリカバリ (PITR) を実行する方法について説明します。

## <code>br</code>コマンドラインの説明 {#code-br-code-command-line-description}

`br`コマンドは、サブコマンド、オプション、パラメータで構成されます。サブコマンドとは、 `-`または`--`含まない文字です。オプションとは、 `-`または`--`で始まる文字です。パラメータとは、サブコマンドまたはオプションの直後に続く文字で、サブコマンドまたはオプションに渡されます。

以下は完全な`br`コマンドです。

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-data/snapshot-202209081330/"
```

上記のコマンドの説明は次のとおりです。

-   `backup` : `tiup br`のサブコマンド。
-   `full` : `tiup br backup`のサブコマンド。
-   `-s` (または`--storage` ): バックアップ ファイルが保存されるパスを指定するオプション。4 は`"s3://backup-data/snapshot-202209081330/"` `-s`パラメーターです。
-   `--pd` : PD サービス アドレスを指定するオプション`"${PD_IP}:2379"`は`--pd`のパラメーターです。

### コマンドとサブコマンド {#commands-and-sub-commands}

`tiup br`コマンドは複数のサブコマンドの階層で構成されています。現在、br コマンドラインツールには以下のサブコマンドがあります。

-   `tiup br backup` : TiDB クラスターのデータをバックアップするために使用されます。
-   `tiup br log` : ログ バックアップ タスクの開始と管理に使用されます。
-   `tiup br restore` : TiDB クラスターのバックアップ データを復元するために使用されます。
-   `tiup br debug` : バックアップ メタデータの解析、バックアップ データのチェックなどに使用されます。

`tiup br backup`および`tiup br restore`は次のサブコマンドが含まれます。

-   `full` : すべてのクラスター データをバックアップまたは復元するために使用されます。
-   `db` : クラスターの指定されたデータベースをバックアップまたは復元するために使用されます。
-   `table` : クラスターの指定されたデータベース内の単一のテーブルをバックアップまたは復元するために使用されます。

`tiup br debug`には次のサブコマンドが含まれます。

-   `checksum` : (隠しパラメーター) バックアップ データの整合性をオフラインでチェックし、すべてのバックアップ ファイルが[`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)で計算された CRC64 チェックサム結果と一致することを確認するために使用されます。
-   `backupmeta` : バックアップデータファイル間に交差が存在するかどうかを確認するために使用されます。通常、バックアップデータファイルは交差しません。
-   `decode` : 完全バックアップのメタデータファイル`backupmeta` JSON形式に解析するために使用されます。さらに、 `--field`パラメータを使用して特定のフィールドを解析することもできます。
-   `encode` : 完全バックアップの`backupmeta.json`メタデータ ファイルを、データの復元中に使用される protobuf 形式にエンコードするために使用されます。
-   `reset-pd-config-as-default` : (非推奨) データ回復プロセス中に変更された PD 構成をデフォルト構成に復元するために使用されます。
-   `search-log-backup` : ログ バックアップ データ内の特定のキー情報を検索するために使用されます。

### 一般的なオプション {#common-options}

-   `--pd` : PDサービスアドレスを指定します。例： `"${PD_IP}:2379"` 。
-   `-s` （または`--storage` ）: バックアップファイルを保存するパスを指定します。バックアップデータの保存には、Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、NFSがサポートされています。詳細については、 [外部ストレージサービスのURI形式](/external-storage-uri.md)を参照してください。
-   `--ca` : PEM 形式の信頼された CA 証明書へのパスを指定します。
-   `--cert` : PEM 形式の SSL 証明書へのパスを指定します。
-   `--key` : PEM 形式の SSL 証明書キーへのパスを指定します。
-   `--status-addr` : `br` Prometheus に統計を提供するリスニング アドレスを指定します。
-   `--concurrency` : バックアップタスクを複数のリクエストに分割し、同じ TiKV ノードに同時に送信する方法を制御します。このパラメータは主にBRから TiKV へのリクエスト分割の粒度に影響し、全体的なバックアップスループットを直接決定するものではありません。ほとんどの場合、この値を変更する必要はありません。バックアップパフォーマンスを向上させるには、代わりに[`tikv.backup.num-threads`](/tikv-configuration-file.md#num-threads-1)調整する必要があります。
-   `--pitr-concurrency` : ログ復元中の同時タスクの数。
-   `--tikv-max-restore-concurrency` : スナップショット復元中の TiKV ノードあたりの同時タスクの最大数。
-   `--compression` : バックアップファイルの生成に使用する圧縮アルゴリズムを決定します。2、4、6 `lz4`サポートし、デフォルトは`zstd`です（通常は変更する必要`zstd`ありません）。異なる圧縮アルゴリズムの選択に関するガイダンスについては、 [この文書](https://github.com/EighteenZi/rocksdb_wiki/blob/master/Compression.md)を`snappy`してください。
-   `--compression-level` : バックアップに選択した圧縮アルゴリズムに対応する圧縮レベルを設定します。2 `zstd`のデフォルトの圧縮レベルは 3 です。ほとんどの場合、このオプションを設定する必要はありません。

## フルバックアップのコマンド {#commands-of-full-backup}

クラスターデータをバックアップするには、 `tiup br backup`コマンドを実行します。3 または`full` `table`コマンドを追加して、バックアップ操作の範囲（クラスター全体（ `full` ）または単一のテーブル（ `table` ））を指定できます。

-   [TiDB クラスターのスナップショットをバックアップする](/br/br-snapshot-manual.md#back-up-cluster-snapshots)
-   [データベースをバックアップする](/br/br-snapshot-manual.md#back-up-a-database)
-   [テーブルをバックアップする](/br/br-snapshot-manual.md#back-up-a-table)
-   [テーブルフィルターを使用して複数のテーブルをバックアップする](/br/br-snapshot-manual.md#back-up-multiple-tables-with-table-filter)
-   [スナップショットを暗号化する](/br/backup-and-restore-storages.md#server-side-encryption)

## ログバックアップのコマンド {#commands-of-log-backup}

ログ バックアップを開始し、ログ バックアップ タスクを管理するには、 `tiup br log`コマンドを実行します。

-   [ログバックアップタスクを開始する](/br/br-pitr-manual.md#start-a-log-backup-task)
-   [ログバックアップのステータスを照会する](/br/br-pitr-manual.md#query-the-log-backup-status)
-   [ログバックアップタスクを一時停止して再開する](/br/br-pitr-manual.md#pause-and-resume-a-log-backup-task)
-   [ログバックアップタスクを停止して再開する](/br/br-pitr-manual.md#stop-and-restart-a-log-backup-task)
-   [バックアップデータをクリーンアップする](/br/br-pitr-manual.md#clean-up-log-backup-data)
-   [バックアップメタデータをビュー](/br/br-pitr-manual.md#view-the-log-backup-metadata)

## バックアップデータの復元コマンド {#commands-of-restoring-backup-data}

クラスターデータを復元するには、コマンド`tiup br restore`を実行します。サブコマンド`full` 、 `db` 、または`table`を追加して、復元範囲を指定できます。復元範囲は、クラスター全体 ( `full` )、単一のデータベース ( `db` )、または単一のテーブル ( `table` ) です。

-   [ポイントインタイムリカバリ](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)
-   [クラスタースナップショットを復元する](/br/br-snapshot-manual.md#restore-cluster-snapshots)
-   [データベースを復元する](/br/br-snapshot-manual.md#restore-a-database)
-   [テーブルを復元する](/br/br-snapshot-manual.md#restore-a-table)
-   [テーブルフィルターを使用して複数のテーブルを復元する](/br/br-snapshot-manual.md#restore-multiple-tables-with-table-filter)
-   [暗号化されたスナップショットを復元する](/br/br-snapshot-manual.md#restore-encrypted-snapshots)
