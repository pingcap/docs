---
title: TiDB Snapshot Backup and Restore Architecture
summary: Learn about the architecture of TiDB snapshot backup and restore.
---

# TiDB スナップショットのバックアップと復元のアーキテクチャ {#tidb-snapshot-backup-and-restore-architecture}

このドキュメントでは、バックアップと復元 ( BR ) ツールを例として使用して、TiDB スナップショットのバックアップと復元のアーキテクチャとプロセスを紹介します。

## アーキテクチャ {#architecture}

TiDB スナップショットのバックアップと復元のアーキテクチャは次のとおりです。

![BR snapshot backup and restore architecture](/media/br/br-snapshot-arch.png)

## バックアップのプロセス {#process-of-backup}

クラスタ スナップショット バックアップのプロセスは次のとおりです。

![snapshot backup process design](/media/br/br-snapshot-backup-ts.png)

完全なバックアップ プロセスは次のとおりです。

1.  BR は`br backup full`コマンドを受信します。

    -   バックアップ時点とstorageパスを取得します。

2.  BR はバックアップ データをスケジュールします。

    -   **Pause GC** : BR は、 TiDB GC 時間を構成して、バックアップ データが[TiDB GC メカニズム](/garbage-collection-overview.md)クリーンアップされるのを防ぎます。
    -   **Fetch TiKV and リージョン info** : BR はPD にアクセスして、すべての TiKV ノード アドレスと[リージョン](/tidb-storage.md#region)のデータ分布を取得します。
    -   **データのバックアップを TiKV に要求する**: BR はバックアップ要求を作成し、それをすべての TiKV ノードに送信します。バックアップ要求には、バックアップ時点、バックアップするリージョン、およびstorageパスが含まれます。

3.  TiKV はバックアップ リクエストを受け入れ、バックアップ ワーカーを開始します。

4.  TiKV がデータをバックアップします。

    -   **Scan KVs** : バックアップ ワーカーは、リーダーが配置されているリージョンからバックアップ時点に対応するデータを読み取ります。
    -   **Generate SST** : バックアップ ワーカーはデータを SST ファイルに保存し、メモリに保存します。
    -   **Upload SST** : バックアップ ワーカーが SST ファイルをstorageパスにアップロードします。

5.  BR は、各 TiKV ノードからバックアップ結果を受け取ります。

    -   たとえば、TiKV ノードがダウンしているなど、リージョンの変更が原因で一部のデータのバックアップに失敗した場合、 BR はバックアップを再試行します。
    -   バックアップに失敗し、再試行できないデータがある場合、バックアップ タスクは失敗します。
    -   すべてのデータがバックアップされた後、 BR はメタデータをバックアップします。

6.  BR はメタデータをバックアップします。

    -   **スキーマのバックアップ**: BR はテーブル スキーマをバックアップし、テーブル データのチェックサムを計算します。
    -   **メタデータのアップロード**: BR はバックアップ メタデータを生成し、それをstorageパスにアップロードします。バックアップ メタデータには、バックアップ タイムスタンプ、テーブルと対応するバックアップ ファイル、データ チェックサム、およびファイル チェックサムが含まれます。

## 復元のプロセス {#process-of-restore}

クラスター スナップショットの復元のプロセスは次のとおりです。

![snapshot restore process design](/media/br/br-snapshot-restore-ts.png)

完全な復元プロセスは次のとおりです。

1.  BR は`br restore`コマンドを受信します。

    -   復元するデータstorageパスとデータベースまたはテーブルを取得します。
    -   復元するテーブルが存在するかどうか、および復元の要件を満たしているかどうかを確認します。

2.  BR は復元データをスケジュールします。

    -   **リージョンスケジュールの一時停止**: BR はPD に、復元中に自動リージョンスケジューリングを一時停止するよう要求します。
    -   **Restore schema** : BR は、バックアップ データのスキーマと、復元するデータベースとテーブルを取得します。新しく作成されたテーブルの ID は、バックアップ データの ID とは異なる場合があることに注意してください。
    -   **Split &amp; scatter リージョン** : BR は、バックアップ データに基づいてリージョンを割り当てるように PD に要求し (split リージョン)、リージョンがstorageノードに均等に分散されるようにスケジュールします (scatter リージョン)。各リージョンには指定されたデータ範囲があります`[start key, end key)` 。
    -   **TiKV にデータの復元をリクエストする**: BR は復元リクエストを作成し、リージョン分割の結果に従って、対応する TiKV ノードに送信します。復元要求には、復元するデータと書き換え規則が含まれます。

3.  TiKV は復元要求を受け入れ、復元ワーカーを開始します。

    -   復元ワーカーは、復元するために読み取る必要があるバックアップ データを計算します。

4.  TiKV がデータを復元します。

    -   **Download SST** : 復元ワーカーは、対応する SST ファイルをstorageパスからローカル ディレクトリにダウンロードします。
    -   **Rewrite KVs** : 復元ワーカーは、新しいテーブル ID に従って KV データを書き換えます。つまり、 [キー値](/tidb-computing.md#mapping-table-data-to-key-value)の元のテーブル ID を新しいテーブル ID に置き換えます。復元ワーカーも同様にインデックス ID を書き換えます。
    -   **取り込み SST** : 復元ワーカーは、処理された SST ファイルを RocksDB に取り込みます。
    -   **復元結果の報告**: 復元ワーカーは復元結果をBRに報告します。

5.  BR は、各 TiKV ノードから復元結果を受け取ります。

    -   `RegionNotFound`または`EpochNotMatch`が原因で一部のデータの復元に失敗した場合 (たとえば、TiKV ノードがダウンしている場合)、 BRは復元を再試行します。
    -   復元に失敗し、再試行できないデータがある場合、復元タスクは失敗します。
    -   すべてのデータが復元されると、復元タスクは成功します。

## バックアップファイル {#backup-files}

### バックアップファイルの種類 {#types-of-backup-files}

スナップショット バックアップでは、次の種類のファイルが生成されます。

-   `SST`ファイル: TiKV ノードがバックアップするデータを保存します。 `SST`ファイルのサイズはリージョンのサイズと同じです。
-   `backupmeta`ファイル: すべてのバックアップ ファイルの数、各バックアップ ファイルのキー範囲、サイズ、ハッシュ (sha256) 値など、バックアップ タスクのメタデータを保存します。
-   `backup.lock`ファイル: 複数のバックアップ タスクが同じディレクトリにデータを保存するのを防ぎます。

### SST ファイルの命名形式 {#naming-format-of-sst-files}

データが Google Cloud Storage (GCS) または Azure Blob Storage にバックアップされる場合、SST ファイルは`storeID_regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。名前のフィールドは次のように説明されています。

-   `storeID`は TiKV ノード ID です。
-   `regionID`はリージョンID です。
-   `regionEpoch`はリージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値で、ファイルの一意性を保証します。
-   `timestamp`は、TiKV によって生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリーを示します ( `cf`が`default`または`write`のデータのみを復元します)。

データが Amazon S3 またはネットワーク ディスクにバックアップされる場合、SST ファイルは`regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。名前のフィールドは次のように説明されています。

-   `regionID`はリージョンID です。
-   `regionEpoch`はリージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値で、ファイルの一意性を保証します。
-   `timestamp`は、TiKV によって生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf` RocksDB のカラムファミリーを示します ( `cf`が`default`または`write`のデータのみを復元します)。

### SST ファイルの保存形式 {#storage-format-of-sst-files}

-   SST ファイルのstorage形式の詳細については、 [RocksDB BlockBasedTable 形式](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)を参照してください。
-   SST ファイルのバックアップ データのエンコード形式の詳細については、 [テーブル データの Key-Value へのマッピング](/tidb-computing.md#mapping-table-data-to-key-value)を参照してください。

### バックアップファイルの構造 {#structure-of-backup-files}

データを GCS または Azure Blob Storage にバックアップすると、SST ファイル、 `backupmeta`ファイル、および`backup.lock`ファイルが次の構造で同じディレクトリに格納されます。

```
.
└── 20220621
    ├── backupmeta
    |—— backup.lock
    ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    └── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
```

データを Amazon S3 またはネットワーク ディスクにバックアップする場合、SST ファイルは`storeID`に基づくサブディレクトリに保存されます。構造は次のとおりです。

```
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
```

## こちらもご覧ください {#see-also}

-   [TiDB スナップショットのバックアップと復元ガイド](/br/br-snapshot-guide.md)
