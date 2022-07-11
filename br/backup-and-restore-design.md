---
title: BR Design Principles
summary: Learn about the design details of BR.
---

# BRの設計原則 {#br-design-principles}

このドキュメントでは、アーキテクチャとバックアップファイルを含む、バックアップと復元（BR）の設計原則について説明します。

## BRアーキテクチャ {#br-architecture}

BRは、バックアップまたは復元コマンドを各TiKVノードに送信します。コマンドを受信した後、TiKVは対応するバックアップまたは復元操作を実行します。

各TiKVノードには、バックアップ操作で生成されたバックアップファイルが保存され、復元中に保存されたバックアップファイルが読み取られるパスがあります。

![br-arch](/media/br-arch.png)

## バックアップファイル {#backup-files}

このセクションでは、BRによって生成されるバックアップファイルの設計について説明します。

### バックアップファイルの種類 {#types-of-backup-files}

BRは、次のタイプのバックアップファイルを生成できます。

-   `SST`ファイル：TiKVノードがバックアップするデータを保存します。
-   `backupmeta`ファイル：バックアップファイルの数、キー範囲、サイズ、ハッシュ（sha256）値など、バックアップ操作のメタデータを格納します。
-   `backup.lock`ファイル：複数のバックアップ操作で同じディレクトリにデータが保存されないようにします。

### SSTファイルの命名形式 {#naming-format-of-sst-files}

SSTファイルは`storeID_regionID_regionEpoch_keyHash_cf`の形式で名前が付けられます。形式のフィールドは次のように説明されます。

-   `storeID`はTiKVノードIDです。
-   `regionID`はリージョンIDです。
-   `regionEpoch`はリージョンのバージョン番号です。
-   `keyHash`は、範囲のstartKeyのハッシュ（sha256）値であり、キーの一意性を保証します。
-   `cf`はRocksDBのカラムファミリーを示します（デフォルトでは`default`または`write` ）。

### SSTファイルの保存形式 {#storage-format-of-sst-files}

-   SSTファイルの保存形式の詳細については、 [RocksdbBlockBasedTable形式](https://github.com/facebook/rocksdb/wiki/Rocksdb-BlockBasedTable-Format)を参照してください。
-   SSTファイルのバックアップデータのエンコード形式の詳細については、 [テーブルデータのKey-Valueへのマッピング](/tidb-computing.md#mapping-of-table-data-to-key-value)を参照してください。
