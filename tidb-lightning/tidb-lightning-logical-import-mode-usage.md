---
title: Use Logical Import Mode
summary: TiDB Lightningの論理インポートモードの使い方を学びましょう。
---

# 論理インポートモードを使用する {#use-logical-import-mode}

このドキュメントでは、設定ファイルの作成やパフォーマンスのチューニングなど、 TiDB Lightningでの[論理インポートモード](/tidb-lightning/tidb-lightning-logical-import-mode.md)の使用方法を紹介します。

## 論理インポートモードを設定して使用する {#configure-and-use-the-logical-import-mode}

論理インポートモードを使用するには、以下の設定ファイルを使用します。

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
# The local data source directory or the URI of the external storage. For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/stable/backup-and-restore-storages/#uri-format.
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

完全な設定ファイルについては、 [TiDB Lightning のコンフィグレーション](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合検出 {#conflict-detection}

競合データとは、PK列またはUK列に同じデータを持つレコードが2つ以上存在する状態を指します。論理インポートモードでは、 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)設定項目を設定することで、競合データの処理戦略を構成できます。TiDB Lightningは、この戦略に基づいて、異なるSQLステートメントを使用してデータをインポートします。

| 戦略          | 競合するデータのデフォルト動作                                           | 対応するSQL文                                                                                                             |
| :---------- | :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| `"replace"` | 既存のデータを新しいデータに置き換える。                                      | `REPLACE INTO ...`                                                                                                   |
| `"ignore"`  | 既存のデータを保持し、新しいデータは無視する。                                   | `conflict.threshold`が0より大きい場合は、 `INSERT INTO`が使用されます。 `conflict.threshold`が`0`の場合は、 `INSERT IGNORE INTO ...`が使用されます。 |
| `"error"`   | 競合するデータが検出された場合、インポートを中止します。                              | `INSERT INTO ...`                                                                                                    |
| `""`        | `"error"`に変換されました。これは、競合するデータが検出された場合、インポートを終了することを意味します。 | なし                                                                                                                   |

戦略が`"error"`の場合、競合するデータによって発生したエラーはインポートタスクを直接終了させます。戦略が`"replace"`または`"ignore"`の場合、 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を設定することで許容される競合の最大数を制御できます。デフォルト値は`10000`で、これは 10000 件のエラーが許容されることを意味します。

戦略が`"ignore"`の場合、競合するデータは下流の`conflict_records`テーブルに記録されます。詳細については、 [エラーレポート](/tidb-lightning/tidb-lightning-error-resolution.md#error-report)参照してください。v8.1.0 より前は、 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)を設定することでレコードを制限でき、制限を超える競合データはスキップされ、記録されません。v8.1.0 以降は、TiDB Lightning が[`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)入力に関係なく`max-record-rows`の値に`threshold`の値を自動的に割り当てるため、代わりにTiDB Lightning を設定する必要があります。

## パフォーマンスチューニング {#performance-tuning}

-   論理インポート モードでは、 TiDB Lightningのパフォーマンスはターゲット TiDB クラスターの書き込みパフォーマンスに大きく依存します。クラスターがパフォーマンスのボトルネックに達した場合は、 [高並行書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)を参照してください。

-   対象の TiDB クラスタで書き込みボトルネックが発生しない場合は、 TiDB Lightning構成の`region-concurrency`の値を増やすことを検討してください。 `region-concurrency`のデフォルト値は CPU コア数です。 `region-concurrency`の意味は、物理インポート モードと論理インポート モードで異なります。論理インポート モードでは、 `region-concurrency`は書き込み同時実行数です。

    設定例：

    ```toml
    [lightning]
    region-concurrency = 32
    ```

-   対象の TiDB クラスターで`raftstore.apply-pool-size`および`raftstore.store-pool-size`設定項目を調整すると、インポート速度が向上する可能性があります。
