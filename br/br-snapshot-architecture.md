---
title: TiDB Snapshot Backup and Restore Architecture
summary: TiDB スナップショット バックアップおよび復元アーキテクチャでは、バックアップと復元 (BR) ツールを使用したプロセスを紹介します。アーキテクチャには、バックアップと復元のプロセス、バックアップ ファイルの種類、命名形式、storage形式、およびバックアップ ファイルの構造が含まれます。バックアップ プロセスには、スケジュール設定、データ バックアップ、およびメタデータ バックアップが含まれます。復元プロセスには、スケジュール設定、スキーマ復元、リージョン割り当て、データ復元、およびレポートが含まれます。バックアップ ファイルの種類には、SST、backupmeta、および backup.lock ファイルが含まれます。SST ファイルの命名形式とstorage形式について詳しく説明します。詳細については、TiDB スナップショット バックアップおよび復元ガイドを参照してください。
---

# TiDB スナップショットのバックアップと復元のアーキテクチャ {#tidb-snapshot-backup-and-restore-architecture}

このドキュメントでは、バックアップと復元 ( BR ) ツールを例として、TiDB スナップショットのバックアップと復元のアーキテクチャとプロセスについて説明します。

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

    -   **GC を一時停止**: BR は、バックアップ データが[TiDB GC メカニズム](/garbage-collection-overview.md)でクリーンアップされるのを防ぐために TiDB GC 時間を設定します。
    -   **TiKV およびリージョン情報を取得する**: BR はPD にアクセスして、すべての TiKV ノードのアドレスと[リージョン](/tidb-storage.md#region)のデータ分布を取得します。
    -   **TiKV にデータのバックアップを要求します**。BRはバックアップ要求を作成し、すべての TiKV ノードに送信します。バックアップ要求には、バックアップの時点、バックアップするリージョン、およびstorageパスが含まれます。

3.  TiKV はバックアップ要求を受け入れ、バックアップ ワーカーを開始します。

4.  TiKV はデータをバックアップします。

    -   **KV のスキャン**: バックアップ ワーカーは、リーダーが配置されているリージョンからバックアップ時点に対応するデータを読み取ります。
    -   **SST の生成**: バックアップ ワーカーはデータを SST ファイルに保存し、メモリに格納します。
    -   **SST のアップロード**: バックアップ ワーカーは SST ファイルをstorageパスにアップロードします。

5.  BR は各 TiKV ノードからバックアップ結果を受信します。

    -   リージョンの変更 (たとえば、TiKV ノードがダウンしている) により一部のデータのバックアップに失敗した場合、 BR はバックアップを再試行します。
    -   バックアップに失敗し、再試行できないデータがある場合、バックアップ タスクは失敗します。
    -   すべてのデータがバックアップされた後、 BR はメタデータをバックアップします。

6.  BR はメタデータをバックアップします。

    -   **スキーマのバックアップ**: BR はテーブル スキーマをバックアップし、テーブル データのチェックサムを計算します。
    -   **メタデータのアップロード**: BR はバックアップ メタデータを生成し、storageパスにアップロードします。バックアップ メタデータには、バックアップのタイムスタンプ、テーブルと対応するバックアップ ファイル、データ チェックサム、およびファイル チェックサムが含まれます。

## 復元のプロセス {#process-of-restore}

クラスター スナップショットの復元のプロセスは次のとおりです。

![snapshot restore process design](/media/br/br-snapshot-restore-ts.png)

完全な復元プロセスは次のとおりです。

1.  BRは`br restore`コマンドを受信します。

    -   データstorageパスと復元するデータベースまたはテーブルを取得します。
    -   復元するテーブルが存在するかどうか、また復元の要件を満たしているかどうかを確認します。

2.  BR はデータの復元をスケジュールします。

    -   **リージョンスケジュールの一時停止**: BR は、復元中に自動リージョンスケジュールを一時停止するように PD に要求します。
    -   **スキーマの復元**: BR は、バックアップ データのスキーマと、復元するデータベースおよびテーブルを取得します。新しく作成されたテーブルの ID は、バックアップ データの ID と異なる場合があることに注意してください。
    -   **リージョンの分割と分散**: BR は、バックアップ データに基づいて PD にリージョンの割り当て (リージョンの分割) を要求し、リージョンがstorageノードに均等に分散されるようにスケジュールします (リージョンの分散)。各リージョンには、指定されたデータ範囲`[start key, end key)`があります。
    -   **TiKV にデータの復元を要求する**: BR は、リージョン分割の結果に応じて復元要求を作成し、対応する TiKV ノードに送信します。復元要求には、復元するデータと書き換えルールが含まれます。

3.  TiKV は復元要求を受け入れ、復元ワーカーを開始します。

    -   復元ワーカーは、復元するために読み取る必要があるバックアップ データを計算します。

4.  TiKV はデータを復元します。

    -   **SST のダウンロード**: 復元ワーカーは、対応する SST ファイルをstorageパスからローカル ディレクトリにダウンロードします。
    -   **KV の書き換え**: リストア ワーカーは新しいテーブル ID に従って KV データを書き換えます。つまり、 [キーバリュー](/tidb-computing.md#mapping-table-data-to-key-value)の元のテーブル ID を新しいテーブル ID に置き換えます。リストア ワーカーは、同じ方法でインデックス ID も書き換えます。
    -   **SSTの取り込み**: 復元ワーカーは処理された SST ファイルを RocksDB に取り込みます。
    -   **復元結果の報告**: 復元ワーカーは復元結果をBRに報告します。

5.  BR は各 TiKV ノードから復元結果を受信します。

    -   `RegionNotFound`または`EpochNotMatch`が原因で一部のデータの復元に失敗した場合 (たとえば、TiKV ノードがダウンしている場合)、 BR は復元を再試行します。
    -   復元に失敗し、再試行できないデータがある場合、復元タスクは失敗します。
    -   すべてのデータが復元されると、復元タスクは成功します。

## バックアップファイル {#backup-files}

### バックアップファイルの種類 {#types-of-backup-files}

スナップショット バックアップでは、次の種類のファイルが生成されます。

-   `SST`ファイル: TiKV ノードがバックアップするデータを保存します。2 ファイルのサイズは`SST`リージョンのサイズと同じです。
-   `backupmeta`ファイル: すべてのバックアップ ファイルの数、キー範囲、サイズ、各バックアップ ファイルのハッシュ (sha256) 値など、バックアップ タスクのメタデータを保存します。
-   `backup.lock`ファイル: 複数のバックアップ タスクが同じディレクトリにデータを保存するのを防ぎます。

### SST ファイルの命名形式 {#naming-format-of-sst-files}

データが Google Cloud Storage (GCS) または Azure Blob Storage にバックアップされると、SST ファイルには`storeID_regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。名前のフィールドの説明は次のとおりです。

-   `storeID` TiKV ノード ID です。
-   `regionID`リージョンID です。
-   `regionEpoch` リージョンのバージョン番号です。
-   `keyHash`範囲の startKey のハッシュ (sha256) 値であり、ファイルの一意性を保証します。
-   `timestamp`は、TiKV によって生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリを示します ( `cf`が`default`または`write`のデータのみを復元します)。

データが Amazon S3 またはネットワーク ディスクにバックアップされると、SST ファイルの名前は`regionID_regionEpoch_keyHash_timestamp_cf`の形式で付けられます。名前のフィールドの説明は次のとおりです。

-   `regionID`リージョンID です。
-   `regionEpoch` リージョンのバージョン番号です。
-   `keyHash`範囲の startKey のハッシュ (sha256) 値であり、ファイルの一意性を保証します。
-   `timestamp`は、TiKV によって生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリを示します ( `cf`が`default`または`write`のデータのみを復元します)。

### SST ファイルの保存形式 {#storage-format-of-sst-files}

-   SSTファイルのstorage形式の詳細については、 [RocksDB BlockBasedTable 形式](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)参照してください。
-   SST ファイル内のバックアップ データのエンコード形式の詳細については、 [テーブルデータからキー値へのマッピング](/tidb-computing.md#mapping-table-data-to-key-value)を参照してください。

### バックアップファイルの構造 {#structure-of-backup-files}

GCS または Azure Blob Storage にデータをバックアップすると、SST ファイル、 `backupmeta`ファイル、および`backup.lock`ファイルは次の構造で同じディレクトリに保存されます。

    .
    └── 20220621
        ├── backupmeta
        |—— backup.lock
        ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
        └── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst

Amazon S3 またはネットワーク ディスクにデータをバックアップすると、SST ファイルは`storeID`に基づいてサブディレクトリに保存されます。構造は次のとおりです。

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
