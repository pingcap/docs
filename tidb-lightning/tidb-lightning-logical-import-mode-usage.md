---
title: Use Logical Import Mode
summary: TiDB Lightningの論理インポート モードを使用する方法を学習します。
---

# 論理インポートモードを使用する {#use-logical-import-mode}

このドキュメントでは、設定ファイルの記述やパフォーマンスのチューニングなど、 TiDB Lightningの[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)使用方法を紹介します。

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

競合データとは、PK 列または UK 列に同じデータを持つ 2 つ以上のレコードを指します。論理インポート モードでは、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)構成項目を設定することで、競合データの処理戦略を構成できます。この戦略に基づいて、 TiDB Lightning は異なる SQL ステートメントでデータをインポートします。

| 戦略          | 競合するデータのデフォルトの動作                                                                | 対応するSQL文                                                                                                                  |
| :---------- | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| `"replace"` | 既存のデータを新しいデータに置き換えます。                                                           | `REPLACE INTO ...`                                                                                                        |
| `"ignore"`  | 既存のデータを保持し、新しいデータを無視します。                                                        | `conflict.max-record-rows`が0より大きい場合は`INSERT INTO`が使用され、 `conflict.max-record-rows`が`0`の場合は`INSERT IGNORE INTO ...`使用されます。 |
| `"error"`   | インポートを一時停止し、エラーを報告します。                                                          | `INSERT INTO ...`                                                                                                         |
| `""`        | TiDB Lightning は競合するデータを検出または処理しません。主キーと一意キーが競合するデータが存在する場合、後続のステップでエラーが報告されます。 | なし                                                                                                                        |

戦略が`"error"`の場合、競合するデータによってエラーが発生すると、インポート タスクが直接終了します。戦略が`"replace"`または`"ignore"`場合、 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)設定することで、最大許容競合数を制御できます。デフォルト値は`9223372036854775807`で、ほぼすべてのエラーが許容されることを意味します。

戦略が`"ignore"`の場合、競合するデータは下流の`conflict_records`テーブルに記録されます。詳細については[エラーレポート](/tidb-lightning/tidb-lightning-error-resolution.md#error-report)参照してください。この場合、 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を設定することでレコードを制限でき、制限を超える競合データはスキップされて記録されません。デフォルト値は`100`です。

## パフォーマンスチューニング {#performance-tuning}

-   論理インポート モードでは、 TiDB Lightningのパフォーマンスは、ターゲット TiDB クラスターの書き込みパフォーマンスに大きく依存します。クラスターがパフォーマンスのボトルネックになった場合は、 [高度な同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)を参照してください。

-   ターゲット TiDB クラスターが書き込みボトルネックに遭遇しない場合は、 TiDB Lightning構成で値`region-concurrency`を増やすことを検討してください。デフォルト値`region-concurrency`は CPU コアの数です`region-concurrency`の意味は、物理インポート モードと論理インポート モードでは異なります。論理インポート モードでは、 `region-concurrency`書き込み同時実行数です。

    構成例:

    ```toml
    [lightning]
    region-concurrency = 32
    ```

-   ターゲット TiDB クラスター内の構成項目`raftstore.apply-pool-size`と`raftstore.store-pool-size`を調整すると、インポート速度が向上する可能性があります。
