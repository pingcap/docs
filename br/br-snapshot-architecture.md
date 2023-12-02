---
title: TiDB Snapshot Backup and Restore Architecture
summary: Learn about the architecture of TiDB snapshot backup and restore.
---

# TiDB スナップショットのバックアップおよび復元のアーキテクチャ {#tidb-snapshot-backup-and-restore-architecture}

このドキュメントでは、例としてバックアップ &amp; リストア ( BR ) ツールを使用した TiDB スナップショットのバックアップとリストアのアーキテクチャとプロセスを紹介します。

## アーキテクチャ {#architecture}

TiDB スナップショットのバックアップと復元のアーキテクチャは次のとおりです。

![BR snapshot backup and restore architecture](/media/br/br-snapshot-arch.png)

## バックアップのプロセス {#process-of-backup}

クラスターのスナップショット バックアップのプロセスは次のとおりです。

![snapshot backup process design](/media/br/br-snapshot-backup-ts.png)

完全なバックアップ プロセスは次のとおりです。

1.  BRは`br backup full`コマンドを受信します。

    -   バックアップの時点とstorageのパスを取得します。

2.  BR はデータのバックアップをスケジュールします。

    -   **GC の一時停止**: BR は、バックアップ データが[TiDB GC メカニズム](/garbage-collection-overview.md)によってクリーンアップされないように TiDB GC 時間を設定します。
    -   **TiKV およびリージョン情報の取得**: BR はPD にアクセスして、すべての TiKV ノードのアドレスとデータの[リージョン](/tidb-storage.md#region)を取得します。
    -   **TiKV にデータのバックアップを要求する**: BR はバックアップ要求を作成し、それをすべての TiKV ノードに送信します。バックアップ要求には、バックアップ時点、バックアップ対象のリージョン、およびstorageパスが含まれます。

3.  TiKV はバックアップ要求を受け入れ、バックアップ ワーカーを開始します。

4.  TiKV はデータをバックアップします。

    -   **KV のスキャン**: バックアップ ワーカーは、リーダーが配置されているリージョンからバックアップ時点に対応するデータを読み取ります。
    -   **SST の生成**: バックアップ ワーカーはデータを SST ファイルに保存し、メモリに保存します。
    -   **SST のアップロード**: バックアップ ワーカーは、SST ファイルをstorageパスにアップロードします。

5.  BR は各 TiKV ノードからバックアップ結果を受信します。

    -   TiKV ノードがダウンしているなど、リージョンの変更により一部のデータのバックアップに失敗した場合、 BR はバックアップを再試行します。
    -   バックアップに失敗し、再試行できないデータがある場合、バックアップ タスクは失敗します。
    -   すべてのデータがバックアップされた後、 BR はメタデータをバックアップします。

6.  BR はメタデータをバックアップします。

    -   **スキーマのバックアップ**: BR はテーブル スキーマをバックアップし、テーブル データのチェックサムを計算します。
    -   **メタデータのアップロード**: BR はバックアップ メタデータを生成し、storageパスにアップロードします。バックアップ メタデータには、バックアップ タイムスタンプ、テーブルと対応するバックアップ ファイル、データ チェックサム、ファイル チェックサムが含まれます。

## 復元のプロセス {#process-of-restore}

クラスターのスナップショット復元のプロセスは次のとおりです。

![snapshot restore process design](/media/br/br-snapshot-restore-ts.png)

完全な復元プロセスは次のとおりです。

1.  BRは`br restore`コマンドを受信します。

    -   データstorageパスと復元するデータベースまたはテーブルを取得します。
    -   リストア対象のテーブルが存在するか、リストアの要件を満たしているかを確認します。

2.  BR はデータの復元をスケジュールします。

    -   **リージョンスケジュールの一時停止**: BR は、復元中に自動リージョンスケジュールを一時停止するように PD に要求します。
    -   **スキーマの復元**: BR は、バックアップ データと復元するデータベースおよびテーブルのスキーマを取得します。新規に作成したテーブルのIDはバックアップデータのIDと異なる場合があるので注意してください。
    -   **分割および分散リージョン**: BR は、バックアップ データに基づいて領域を割り当てるように PD に要求し (分割リージョン)、領域がstorageノードに均等に分散されるようにスケジュールします (分散リージョン)。各リージョンには指定されたデータ範囲があります`[start key, end key)` 。
    -   **TiKV にデータの復元を要求する**: BR は復元要求を作成し、リージョン分割の結果に従って対応する TiKV ノードに送信します。復元リクエストには、復元するデータと書き換えルールが含まれます。

3.  TiKV は復元リクエストを受け入れ、復元ワーカーを開始します。

    -   リストア ワーカーは、リストアするために読み取る必要があるバックアップ データを計算します。

4.  TiKV がデータを復元します。

    -   **SST のダウンロード**: リストア ワーカーは、対応する SST ファイルをstorageパスからローカル ディレクトリにダウンロードします。
    -   **KV の書き換え**: 復元ワーカーは、新しいテーブル ID に従って KV データを書き換えます。つまり、 [キーと値](/tidb-computing.md#mapping-table-data-to-key-value)の元のテーブル ID を新しいテーブル ID に置き換えます。復元ワーカーも同様にインデックス ID を書き換えます。
    -   **SSTの取り込み**: リストア ワーカーは、処理された SST ファイルを RocksDB に取り込みます。
    -   **復元結果の報告**: 復元ワーカーは復元結果をBRに報告します。

5.  BR は各 TiKV ノードからリストア結果を受け取ります。

    -   TiKV ノードがダウンしているなど、 `RegionNotFound`または`EpochNotMatch`原因で一部のデータの復元に失敗した場合、 BR は復元を再試行します。
    -   復元に失敗し、再試行できないデータがある場合、復元タスクは失敗します。
    -   すべてのデータが復元されると、復元タスクは成功します。

## バックアップファイル {#backup-files}

### バックアップファイルの種類 {#types-of-backup-files}

スナップショット バックアップでは、次の種類のファイルが生成されます。

-   `SST`ファイル: TiKV ノードがバックアップするデータを保存します。 `SST`ファイルのサイズは、リージョンのサイズと同じです。
-   `backupmeta`ファイル: すべてのバックアップ ファイルの数、各バックアップ ファイルのキー範囲、サイズ、ハッシュ (sha256) 値など、バックアップ タスクのメタデータを保存します。
-   `backup.lock`ファイル: 複数のバックアップ タスクが同じディレクトリにデータを保存することを防ぎます。

### SST ファイルの命名形式 {#naming-format-of-sst-files}

データが Google Cloud Storage (GCS) または Azure Blob Storage にバックアップされる場合、SST ファイルには`storeID_regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。名前のフィールドについては次のように説明します。

-   `storeID`は TiKV ノード ID です。
-   `regionID`はリージョンID です。
-   `regionEpoch`は、リージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値で、ファイルの一意性が保証されます。
-   `timestamp`は、TiKV によって生成された SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリーを示します ( `cf`が`default`または`write`であるデータのみを復元します)。

データが Amazon S3 またはネットワーク ディスクにバックアップされる場合、SST ファイルには`regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。名前のフィールドについては次のように説明します。

-   `regionID`はリージョンID です。
-   `regionEpoch`は、リージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値で、ファイルの一意性が保証されます。
-   `timestamp`は、TiKV によって生成された SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリーを示します ( `cf`が`default`または`write`であるデータのみを復元します)。

### SSTファイルの保存形式 {#storage-format-of-sst-files}

-   SST ファイルのstorage形式については、 [RocksDB BlockBasedTable 形式](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)を参照してください。
-   SSTファイルのバックアップデータのエンコード形式については、 [テーブルデータの Key-Value へのマッピング](/tidb-computing.md#mapping-table-data-to-key-value)を参照してください。

### バックアップファイルの構造 {#structure-of-backup-files}

データを GCS または Azure Blob Storage にバックアップすると、SST ファイル、 `backupmeta`ファイル、および`backup.lock`ファイルが次の構造として同じディレクトリに保存されます。

    .
    └── 20220621
        ├── backupmeta
        |—— backup.lock
        ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        └── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst

データを Amazon S3 またはネットワーク ディスクにバックアップすると、SST ファイルは`storeID`に基づいてサブディレクトリに保存されます。構造は次のとおりです。

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

## こちらも参照 {#see-also}

-   [TiDB スナップショットのバックアップおよび復元ガイド](/br/br-snapshot-guide.md)
