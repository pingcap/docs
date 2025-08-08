---
title: TiDB Snapshot Backup and Restore Architecture
summary: TiDBスナップショットのバックアップと復元アーキテクチャでは、バックアップと復元（BR）ツールを使用したプロセスについて説明します。アーキテクチャには、バックアップと復元のプロセス、バックアップファイルの種類、命名形式、storage形式、バックアップファイルの構造が含まれます。バックアッププロセスには、スケジュール設定、データのバックアップ、メタデータのバックアップが含まれます。復元プロセスには、スケジュール設定、スキーマの復元、リージョンの割り当て、データの復元、レポート作成が含まれます。バックアップファイルの種類には、SST、backupmeta、backup.lockファイルなどがあります。SSTファイルの命名形式とstorage形式について詳しく説明します。詳細については、TiDBスナップショットのバックアップと復元ガイドを参照してください。
---

# TiDB スナップショットのバックアップと復元のアーキテクチャ {#tidb-snapshot-backup-and-restore-architecture}

このドキュメントでは、バックアップとリストア ( BR ) ツールを例として、TiDB スナップショットのバックアップとリストアのアーキテクチャとプロセスについて説明します。

## アーキテクチャ {#architecture}

TiDB スナップショットのバックアップと復元のアーキテクチャは次のとおりです。

![BR snapshot backup and restore architecture](/media/br/br-snapshot-arch.png)

## バックアップのプロセス {#process-of-backup}

クラスター スナップショット バックアップのプロセスは次のとおりです。

![snapshot backup process design](/media/br/br-snapshot-backup-ts.png)

完全なバックアッププロセスは次のとおりです。

1.  BRは`br backup full`コマンドを受信します。

    -   バックアップの時点とstorageパスを取得します。

2.  BR はバックアップ データをスケジュールします。

    -   **GC を一時停止**: BR は、バックアップ データが[TiDB GCメカニズム](/garbage-collection-overview.md)までにクリーンアップされないように TiDB GC 時間を設定します。
    -   **TiKV およびリージョン情報を取得する**: BR はPD にアクセスして、すべての TiKV ノードのアドレスと[リージョン](/tidb-storage.md#region)データ分布を取得します。
    -   **TiKVにデータのバックアップをリクエスト**： BRはバックアップリクエストを作成し、すべてのTiKVノードに送信します。バックアップリクエストには、バックアップの時点、バックアップ対象のリージョン、storageパスが含まれます。

3.  TiKV はバックアップ要求を受け入れ、バックアップ ワーカーを開始します。

4.  TiKV はデータをバックアップします。

    -   **KV のスキャン**: バックアップ ワーカーは、リーダーが存在するリージョンからバックアップ時点に対応するデータを読み取ります。
    -   **SST の生成**: バックアップ ワーカーはデータを SST ファイルに保存し、メモリに格納します。
    -   **SST のアップロード**: バックアップ ワーカーは SST ファイルをstorageパスにアップロードします。

5.  BR は各 TiKV ノードからバックアップ結果を受信します。

    -   リージョンの変更により一部のデータのバックアップに失敗した場合（たとえば、TiKV ノードがダウンしている場合）、 BR はバックアップを再試行します。
    -   バックアップに失敗し、再試行できないデータがある場合、バックアップ タスクは失敗します。
    -   すべてのデータがバックアップされた後、 BR はメタデータをバックアップします。

6.  BR はメタデータをバックアップします。

    -   **スキーマのバックアップ**: BR はテーブル スキーマをバックアップし、テーブル データのチェックサムを計算します。
    -   **メタデータのアップロード**： BRはバックアップメタデータを生成し、storageパスにアップロードします。バックアップメタデータには、バックアップのタイムスタンプ、テーブルと対応するバックアップファイル、データチェックサム、ファイルチェックサムが含まれます。

## 復元のプロセス {#process-of-restore}

クラスター スナップショットの復元プロセスは次のとおりです。

![snapshot restore process design](/media/br/br-snapshot-restore-ts.png)

完全な復元プロセスは次のとおりです。

1.  BRは`br restore`コマンドを受信します。

    -   データstorageパスと復元するデータベースまたはテーブルを取得します。
    -   復元するテーブルが存在するかどうか、また復元の要件を満たしているかどうかを確認します。

2.  BR はデータの復元をスケジュールします。

    -   **リージョンスケジュールの一時停止**: BR は、復元中に自動リージョンスケジュールを一時停止するように PD に要求します。
    -   **復元スキーマ**: BRはバックアップデータと復元対象のデータベースおよびテーブルのスキーマを取得します。新しく作成されたテーブルのIDは、バックアップデータのIDと異なる場合があることに注意してください。
    -   **リージョンの分割と分散**： BRはPDにバックアップデータに基づいてリージョン（リージョンの分割）の割り当てを要求し、storageノードに均等に分散するようにスケジュールを設定します（リージョンの分散）。各リージョンには指定されたデータ範囲`[start key, end key)`あります。
    -   **TiKVにデータの復元をリクエスト**： BRはリージョン分割の結果に基づいて復元リクエストを作成し、対応するTiKVノードに送信します。復元リクエストには、復元するデータと書き換えルールが含まれます。

3.  TiKV は復元要求を受け入れ、復元ワーカーを開始します。

    -   復元ワーカーは、復元するために読み取る必要があるバックアップ データを計算します。

4.  TiKV はデータを復元します。

    -   **SST のダウンロード**: 復元ワーカーは、対応する SST ファイルをstorageパスからローカル ディレクトリにダウンロードします。
    -   **KVの書き換え**：リストアワーカーは新しいテーブルIDに従ってKVデータを書き換えます。つまり、 [キーバリュー](/tidb-computing.md#mapping-table-data-to-key-value)の元のテーブルIDを新しいテーブルIDに置き換えます。リストアワーカーは同様にインデックスIDも書き換えます。
    -   **SSTの取り込み**: 復元ワーカーは処理済みの SST ファイルを RocksDB に取り込みます。
    -   **復元結果の報告**: 復元ワーカーは復元結果をBRに報告します。

5.  BR は各 TiKV ノードから復元結果を受信します。

    -   `RegionNotFound`または`EpochNotMatch`原因で一部のデータの復元に失敗した場合 (たとえば、TiKV ノードがダウンしている場合)、 BR は復元を再試行します。
    -   復元に失敗し、再試行できないデータがある場合、復元タスクは失敗します。
    -   すべてのデータが復元されると、復元タスクは成功します。

## バックアップファイル {#backup-files}

### バックアップファイルの種類 {#types-of-backup-files}

スナップショット バックアップでは、次の種類のファイルが生成されます。

-   `SST`ファイル: TiKV ノードがバックアップしたデータを保存します。2 `SST`のサイズはリージョンのサイズと同じです。
-   `backupmeta`ファイル: すべてのバックアップ ファイルの数、キー範囲、サイズ、各バックアップ ファイルのハッシュ (sha256) 値など、バックアップ タスクのメタデータを保存します。
-   `backup.lock`ファイル: 複数のバックアップ タスクが同じディレクトリにデータを保存するのを防ぎます。

### SSTファイルの命名形式 {#naming-format-of-sst-files}

データがGoogle Cloud Storage（GCS）またはAzure Blob Storageにバックアップされると、SSTファイルは`storeID_regionID_regionEpoch_keyHash_timestamp_cf`という形式で命名されます。名前の各フィールドの説明は以下のとおりです。

-   `storeID`は TiKV ノード ID です。
-   `regionID`はリージョンID です。
-   `regionEpoch`は、リージョンのバージョン番号です。
-   `keyHash`範囲の startKey のハッシュ (sha256) 値であり、ファイルの一意性を保証します。
-   `timestamp`は、TiKV によって生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリーを示します ( `cf`が`default`または`write`データのみを復元します)。

データがAmazon S3またはネットワークディスクにバックアップされると、SSTファイルは`regionID_regionEpoch_keyHash_timestamp_cf`の形式で命名されます。名前の各フィールドの説明は以下のとおりです。

-   `regionID`はリージョンID です。
-   `regionEpoch`は、リージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値であり、ファイルの一意性を保証します。
-   `timestamp`は、TiKV によって生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリーを示します ( `cf`が`default`または`write`データのみを復元します)。

### SSTファイルの保存形式 {#storage-format-of-sst-files}

-   SST ファイルのstorage形式の詳細については、 [RocksDB BlockBasedTable形式](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)参照してください。
-   SST ファイル内のバックアップ データのエンコード形式の詳細については、 [テーブルデータとキー値とのマッピング](/tidb-computing.md#mapping-table-data-to-key-value)参照してください。

### バックアップファイルの構造 {#structure-of-backup-files}

GCS または Azure Blob Storage にデータをバックアップすると、SST ファイル、 `backupmeta`ファイル、および`backup.lock`ファイルは次の構造で同じディレクトリに保存されます。

    .
    └── 20220621
        ├── backupmeta
        |—— backup.lock
        ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        └── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst

Amazon S3 またはネットワークディスクにデータをバックアップすると、SST ファイルは`storeID`に基づいてサブディレクトリに保存されます。構造は次のとおりです。

    .
    └── 20220621
        ├── backupmeta
        |—— backup.lock
        ├── store1
        │   └── {regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        ├── store100
        │   └── {regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        ├── store2
        │   └── {regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        ├── store3
        ├── store4
        └── store5

## 参照 {#see-also}

-   [TiDB スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)
