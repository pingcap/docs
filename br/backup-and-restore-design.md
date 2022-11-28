---
title: BR Design Principles
summary: Learn about the design details of BR.
---

# BR の設計原則 {#br-design-principles}

このドキュメントでは、アーキテクチャとバックアップ ファイルを含む、バックアップと復元 (BR) の設計原則について説明します。

## BRアーキテクチャ {#br-architecture}

BR は、各 TiKV ノードにバックアップまたは復元コマンドを送信します。コマンドを受け取った後、TiKV は対応するバックアップまたは復元操作を実行します。

各 TiKV ノードには、バックアップ操作で生成されたバックアップ ファイルが格納されるパスと、復元時に格納されたバックアップ ファイルが読み込まれるパスがあります。

![br-arch](/media/br-arch.png)

## バックアップファイル {#backup-files}

このセクションでは、BR によって生成されるバックアップ ファイルの設計について説明します。

### バックアップファイルの種類 {#types-of-backup-files}

BR は、次の種類のバックアップ ファイルを生成できます。

-   `SST`ファイル: TiKV ノードがバックアップするデータを保存します。
-   `backupmeta`ファイル: バックアップ ファイルの数、キー範囲、サイズ、ハッシュ (sha256) 値など、バックアップ操作のメタデータを格納します。
-   `backup.lock`ファイル: 複数のバックアップ操作でデータが同じディレクトリに保存されるのを防ぎます。

### SST ファイルの命名形式 {#naming-format-of-sst-files}

データが Google Cloud Storage または Azure Blob Storage にバックアップされる場合、SST ファイルは`storeID_regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。フォーマットのフィールドは次のように説明されています。

-   `storeID`は TiKV ノード ID です。
-   `regionID`はリージョンID です。
-   `regionEpoch`はリージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値であり、キーの一意性を保証します。
-   `timestamp`は、TiKV で生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf`は RocksDB のカラムファミリーを示します (デフォルトでは`default`または`write` )。

データが Amazon S3 またはネットワーク ディスクにバックアップされる場合、SST ファイルは`regionID_regionEpoch_keyHash_timestamp_cf`の形式で名前が付けられます。フォーマットのフィールドは次のように説明されています。

-   `regionID`はリージョンID です。
-   `regionEpoch`はリージョンのバージョン番号です。
-   `keyHash`は範囲の startKey のハッシュ (sha256) 値であり、キーの一意性を保証します。
-   `timestamp`は、TiKV で生成されたときの SST ファイルの Unix タイムスタンプです。
-   `cf`は RocksDB のカラムファミリーを示します (デフォルトでは`default`または`write` )。

### SST ファイルの保存形式 {#storage-format-of-sst-files}

-   SST ファイルの保存形式の詳細については、 [Rocksdb BlockBasedTable フォーマット](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)を参照してください。
-   SST ファイルのバックアップ データのエンコード形式の詳細については、 [テーブル データの Key-Value へのマッピング](/tidb-computing.md#mapping-of-table-data-to-key-value)を参照してください。

### バックアップファイルの構造 {#backup-file-structure}

データを Google Cloud Storage または Azure Blob Storage にバックアップすると、SST ファイル、backupmeta ファイル、backup.lock ファイルが次の構造の同じディレクトリに保存されます。

```
.
└── 20220621
    ├── backupmeta
    |—— backup.lock
    ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    ├── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
    └── {storeID}-{regionID}-{regionEpoch}-{keyHash}-{timestamp}-{cf}.sst
```

データを Amazon S3 またはネットワーク ディスクにバックアップすると、SST ファイルは storeID に基づいてサブディレクトリに保存されます。構造は次のとおりです。

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
