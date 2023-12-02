---
title: Use Logical Import Mode
summary: Learn how to use the logical import mode in TiDB Lightning.
---

# 論理インポートモードを使用する {#use-logical-import-mode}

このドキュメントでは、設定ファイルの作成やパフォーマンスのチューニングなど、 TiDB Lightningの[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)の使用方法を紹介します。

## 論理インポート モードを構成して使用する {#configure-and-use-the-logical-import-mode}

次の構成ファイルを介して論理インポート モードを使用してデータをインポートできます。

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

完全な構成ファイルについては、 [TiDB Lightningコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合の検出 {#conflict-detection}

競合するデータとは、PK 列または UK 列に同じデータを持つ 2 つ以上のレコードを指します。論理インポートモードでは、設定項目[`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を設定することで、競合するデータを処理するための戦略を設定できます。戦略に基づいて、 TiDB Lightning はさまざまな SQL ステートメントを使用してデータをインポートします。

| 戦略          | 競合するデータのデフォルトの動作                                                                    | 対応するSQL文                 |
| :---------- | :---------------------------------------------------------------------------------- | :----------------------- |
| `"replace"` | 既存のデータを新しいデータに置き換えます。                                                               | `REPLACE INTO ...`       |
| `"ignore"`  | 既存のデータを保持し、新しいデータを無視します。                                                            | `INSERT IGNORE INTO ...` |
| `"error"`   | インポートを一時停止し、エラーを報告します。                                                              | `INSERT INTO ...`        |
| `""`        | TiDB Lightning は、競合するデータを検出したり処理したりしません。主キーと一意キーが競合するデータが存在する場合、後続のステップでエラーが報告されます。 | なし                       |

戦略が`"error"`の場合、データの競合によってエラーが発生すると、インポート タスクが直接終了します。戦略が`"replace"`または`"ignore"`の場合、 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を構成することで最大許容競合を制御できます。デフォルト値は`9223372036854775807`で、ほとんどすべてのエラーが許容されることを意味します。

ストラテジが`"ignore"`の場合、下流`conflict_records`テーブルには矛盾するデータが記録されます。詳細については、 [エラーレポート](/tidb-lightning/tidb-lightning-error-resolution.md#error-report)を参照してください。この場合、 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を設定することでレコードを制限でき、制限を超える競合するデータはスキップされ、記録されません。デフォルト値は`100`です。

## 性能調整 {#performance-tuning}

-   論理インポート モードでは、 TiDB Lightningのパフォーマンスはターゲット TiDB クラスターの書き込みパフォーマンスに大きく依存します。クラスターがパフォーマンスのボトルネックに達した場合は、 [高度な同時書き込みのベスト プラクティス](/best-practices/high-concurrency-best-practices.md)を参照してください。

-   ターゲット TiDB クラスターが書き込みボトルネックに遭遇しない場合は、 TiDB Lightning構成の値`region-concurrency`を増やすことを検討してください。デフォルト値の`region-concurrency`は CPU コアの数です。 `region-concurrency`の意味は、物理インポートモードと論理インポートモードで異なります。論理インポート モードでは、書き込み同時実行数は`region-concurrency`です。

    構成例:

    ```toml
    [lightning]
    region-concurrency = 32
    ```

-   ターゲット TiDB クラスターの`raftstore.apply-pool-size`および`raftstore.store-pool-size`構成項目を調整すると、インポート速度が向上する可能性があります。
