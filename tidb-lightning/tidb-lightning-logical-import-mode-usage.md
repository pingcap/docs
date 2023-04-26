---
title: Use Logical Import Mode
summary: Learn how to use the logical import mode in TiDB Lightning.
---

# 論理インポート モードを使用する {#use-logical-import-mode}

このドキュメントでは、設定ファイルの記述やパフォーマンスのチューニングなど、 TiDB Lightningでの[論理インポート モード](/tidb-lightning/tidb-lightning-logical-import-mode.md)の使用方法を紹介します。

## 論理インポート モードの構成と使用 {#configure-and-use-the-logical-import-mode}

次の構成ファイルを介して論理インポート モードを使用して、データをインポートできます。

```toml
[lightning]
# log
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14

# Checks the cluster minimum requirements before start.
check-requirements = true

[mydumper]
# The local data source directory or the external storage URL.
data-source-dir = "/data/my_database"

[tikv-importer]
# Import mode. "tidb" means using the logical import mode.
backend = "tidb"

# The operation of inserting duplicate data in the logical import mode.
# - replace: replace existing data with new data
# - ignore: keep existing data and ignore new data
# - error: pause the import and report an error
on-duplicate = "replace"

[tidb]
# The information of the target cluster. The address of any tidb-server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. Either plaintext or Base64 encoded.
password = ""
# tidb-lightning imports the TiDB library, and generates some logs.
# Set the log level of the TiDB library.
log-level = "error"
```

完全な構成ファイルについては、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合の検出 {#conflict-detection}

競合するデータとは、PK または UK 列に同じデータを持つ 2 つ以上のレコードを指します。データ ソースに競合するデータが含まれている場合、テーブル内の実際の行数は、一意のインデックスを使用したクエリによって返される合計行数とは異なります。

論理インポート モードでは、 `on-duplicate`構成アイテムを設定することで、競合するデータを解決するための戦略を構成できます。この戦略に基づいて、 TiDB Lightning はさまざまな SQL ステートメントでデータをインポートします。

| ストラテジー    | 競合するデータのデフォルトの動作         | 対応する SQL ステートメント         |
| :-------- | :----------------------- | :----------------------- |
| `replace` | 既存のデータを新しいデータに置き換える。     | `REPLACE INTO ...`       |
| `ignore`  | 既存のデータを保持し、新しいデータを無視します。 | `INSERT IGNORE INTO ...` |
| `error`   | インポートを一時停止し、エラーを報告します。   | `INSERT INTO ...`        |

## 性能調整 {#performance-tuning}

-   論理インポートモードでは、 TiDB Lightningのパフォーマンスは対象の TiDB クラスターの書き込みパフォーマンスに大きく依存します。クラスターがパフォーマンスのボトルネックに達した場合は、 [高度な同時書き込みのベスト プラクティス](/best-practices/high-concurrency-best-practices.md)を参照してください。

-   ターゲットの TiDB クラスターが書き込みのボトルネックに達しない場合は、 TiDB Lightning構成で値`region-concurrency`を増やすことを検討してください。デフォルト値の`region-concurrency` 、CPU コアの数です。物理インポートモードと論理インポートモードでは、 `region-concurrency`の意味が異なります。論理インポート モードでは、 `region-concurrency`は書き込み同時実行数です。

    構成例:

    ```toml
    [lightning]
    region-concurrency = 32
    ```

-   ターゲットの TiDB クラスターで`raftstore.apply-pool-size`と`raftstore.store-pool-size`構成項目を調整すると、インポート速度が向上する場合があります。
