---
title: Use Logical Import Mode
summary: TiDB Lightningの論理インポート モードを使用する方法を学習します。
---

# 論理インポートモードを使用する {#use-logical-import-mode}

このドキュメントでは、設定ファイルの書き方やパフォーマンスのチューニングなど、 TiDB Lightning[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)の使い方を紹介します。

## 論理インポートモードを設定して使用する {#configure-and-use-the-logical-import-mode}

次の構成ファイルを使用して論理インポート モードを使用してデータをインポートできます。

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
# The local data source directory or the URI of the external storage. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/v6.6/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"

[tikv-importer]
# Import mode. "tidb" means using the logical import mode.
backend = "tidb"

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

完全な設定ファイルについては、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合検出 {#conflict-detection}

競合データとは、PK列またはUK列に同じデータを持つ2つ以上のレコードを指します。論理インポートモードでは、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)設定項目を設定することで、競合データの処理方法を設定できます。TiDB TiDB Lightningは、この処理方法に基づいて、異なるSQL文でデータをインポートします。

| 戦略          | 競合データのデフォルトの動作                                         | 対応するSQL文                                                                                                     |
| :---------- | :----------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `"replace"` | 既存のデータを新しいデータに置き換えます。                                  | `REPLACE INTO ...`                                                                                           |
| `"ignore"`  | 既存のデータを保持し、新しいデータを無視します。                               | `conflict.threshold`が0より大きい場合は`INSERT INTO`使用され、 `conflict.threshold`が`0`の場合は`INSERT IGNORE INTO ...`使用されます。 |
| `"error"`   | 競合するデータが検出された場合はインポートを終了します。                           | `INSERT INTO ...`                                                                                            |
| `""`        | `"error"`に変換されます。これは、競合するデータが検出されるとインポートを終了することを意味します。 | なし                                                                                                           |

戦略が`"error"`場合、データの競合によって発生したエラーはインポートタスクを直ちに終了します。戦略が`"replace"`または`"ignore"`場合、許容される競合の最大数を[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)に設定することで制御できます。デフォルト値は`10000`で、これは10000件のエラーが許容されることを意味します。

戦略が`"ignore"`場合、競合データは下流の`conflict_records`テーブルに記録されます。詳細は[エラーレポート](/tidb-lightning/tidb-lightning-error-resolution.md#error-report)参照してください。v8.1.0 より前では、 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)設定することでレコード数を制限でき、制限を超える競合データはスキップされ、記録されませんでした。v8.1.0 以降では、 TiDB Lightning はユーザー入力に関係なく、 `threshold`の値に`max-record-rows`の値を自動的に割り当てるため、代わりに[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)設定する必要があります。

## パフォーマンスチューニング {#performance-tuning}

-   論理インポートモードでは、 TiDB Lightningのパフォーマンスは、ターゲットTiDBクラスタの書き込みパフォーマンスに大きく依存します。クラスタでパフォーマンスのボトルネックが発生した場合は、 [高同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)を参照してください。

-   ターゲットTiDBクラスタで書き込みボトルネックが発生していない場合は、 TiDB Lightning設定で`region-concurrency`の値を増やすことを検討してください。デフォルト値の`region-concurrency` CPUコア数です。5 `region-concurrency`物理インポートモードと論理インポートモードで意味が異なります。論理インポートモードでは、 `region-concurrency`書き込み同時実行数です。

    構成例:

    ```toml
    [lightning]
    region-concurrency = 32
    ```

-   ターゲット TiDB クラスター内の`raftstore.apply-pool-size`と`raftstore.store-pool-size`構成項目を調整すると、インポート速度が向上する可能性があります。
