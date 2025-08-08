---
title: Use Physical Import Mode
summary: TiDB Lightningの物理インポート モードを使用する方法を学習します。
---

# 物理インポートモードを使用する {#use-physical-import-mode}

このドキュメントでは、構成ファイルの作成、パフォーマンスのチューニング、ディスク クォータの構成など、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)使用方法を紹介します。

物理インポートモードには制限事項があります。物理インポートモードを使用する前に、必ず[制限事項](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations)お読みください。

## 物理インポートモードの設定と使用 {#configure-and-use-the-physical-import-mode}

物理インポート モードを使用してデータのインポートを実行するには、次の構成ファイルを使用できます。

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

[conflict]
# Starting from v7.3.0, a new version of strategy is introduced to handle conflicting data. The default value is "". Starting from v8.0.0, TiDB Lightning optimizes the conflict strategy for both physical and logical import modes.
# - "": TiDB Lightning does not detect or handle conflicting data. If the source file contains conflicting primary or unique key records, the subsequent step reports an error.
# - "error": when detecting conflicting primary or unique key records in the imported data, TiDB Lightning terminates the import and reports an error.
# - "replace": when encountering conflicting primary or unique key records, TiDB Lightning retains the latest data and overwrites the old data.
#              The conflicting data are recorded in the `lightning_task_info.conflict_view` view of the target TiDB cluster.
#              In the `lightning_task_info.conflict_view` view, if the `is_precheck_conflict` field for a row is `0`, it means that the conflicting data recorded in that row is detected by postprocess conflict detection; if the `is_precheck_conflict` field for a row is `1`, it means that conflicting data recorded in that row is detected by pre-import conflict detection.
#              You can manually insert the correct records into the target table based on your application requirements. Note that the target TiKV must be v5.2.0 or later versions.
strategy = ""
# Controls whether to enable pre-import conflict detection, which checks conflicts in data before importing it to TiDB. The default value is false, indicating that TiDB Lightning only checks conflicts after the import. If you set it to true, TiDB Lightning checks conflicts both before and after the import. This parameter can be used only in the physical import mode. In scenarios where the number of conflict records is greater than 1,000,000, it is recommended to set `precheck-conflict-before-import = true` for better performance in conflict detection. In other scenarios, it is recommended to disable it.
# precheck-conflict-before-import = false
# threshold = 10000
# Starting from v8.1.0, there is no need to configure `max-record-rows` manually, because TiDB Lightning automatically assigns the value of `max-record-rows` with the value of `threshold`, regardless of the user input. `max-record-rows` will be deprecated in a future release.
# max-record-rows = 10000

[tikv-importer]
# Import mode. "local" means using the physical import mode.
backend = "local"

# The `duplicate-resolution` parameter is deprecated starting from v8.0.0 and will be removed in a future release. For more information, see <https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode-usage#the-old-version-of-conflict-detection-deprecated-in-v800>.
# If you set `duplicate-resolution = 'none'` and do not set `conflict.strategy`, TiDB Lightning will automatically assign `""` to `conflict.strategy`. 
# If you set `duplicate-resolution = 'remove'` and do not set `conflict.strategy`, TiDB Lightning will automatically assign "replace" to `conflict.strategy` and enable the new version of conflict detection. 
# The method to resolve the conflicting data.
duplicate-resolution = 'none'

# The directory of local KV sorting.
sorted-kv-dir = "./some-dir"

# Limits the bandwidth in which TiDB Lightning writes data into each TiKV
# node in the physical import mode. 0 by default, which means no limit.
# store-write-bwlimit = "128MiB"

# Specifies whether Physical Import Mode adds indexes via SQL. The default value is `false`, which means that TiDB Lightning will encode both row data and index data into KV pairs and import them into TiKV together. This mechanism is consistent with that of the historical versions. If you set it to `true`, it means that TiDB Lightning adds indexes via SQL after importing the row data.
# The benefit of adding indexes via SQL is that you can separately import data and import indexes, and import data more quickly. After the data is imported, even if the indexes fail to be added, it does not affect the consistency of the imported data.
# add-index-by-sql = false

[tidb]
# The information of the target cluster. The address of any tidb-server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. Either plaintext or Base64 encoded.
password = ""
# Required. Table schema information is fetched from TiDB via this status-port.
status-port = 10080
# Required. The address of any pd-server from the cluster. Starting from v7.6.0, TiDB supports setting multiple PD addresses.
pd-addr = "172.16.31.4:2379,56.78.90.12:3456"
# tidb-lightning imports the TiDB library, and generates some logs.
# Set the log level of the TiDB library.
log-level = "error"

[post-restore]
# Specifies whether to perform `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after importing.
# The following options are available:
# - "required" (default): Perform admin checksum after importing. If checksum fails, TiDB Lightning will exit with failure.
# - "optional": Perform admin checksum. If checksum fails, TiDB Lightning will report a WARN log but ignore any error.
# - "off": Do not perform checksum after importing.
# Note that since v4.0.8, the default value has changed from "true" to "required".
#
# Note:
# 1. Checksum failure usually means import exception (data loss or data inconsistency), so it is recommended to always enable Checksum.
# 2. For backward compatibility, bool values "true" and "false" are also allowed for this field.
# "true" is equivalent to "required" and "false" is equivalent to "off".
checksum = "required"

# Specifies whether to perform `ANALYZE TABLE <table>` for each table after checksum is done.
# Options available for this field are the same as `checksum`. However, the default value for this field is "optional".
analyze = "optional"
```

完全な設定ファイルについては、 [設定ファイルとコマンドラインパラメータ](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合検出 {#conflict-detection}

競合データとは、同じ主キーまたは一意キー列データを持つ2つ以上のレコードを指します。データソースに競合データが含まれており、競合検出機能がオンになっていない場合、テーブル内の実際の行数は、一意インデックスを使用したクエリによって返される行数と異なります。

競合検出には 2 つのバージョンがあります。

-   `conflict`構成項目によって制御される、競合検出の新しいバージョン。
-   `tikv-importer.duplicate-resolution`構成項目によって制御される、競合検出の古いバージョン (v8.0.0 で非推奨となり、将来のリリースで削除される予定)。

### 衝突検出の新しいバージョン {#the-new-version-of-conflict-detection}

設定値の意味は次のとおりです。

| 戦略          | 競合データのデフォルトの動作                                                                      | 対応するSQL文           |
| :---------- | :---------------------------------------------------------------------------------- | :----------------- |
| `"replace"` | 最新のデータを保持し、古いデータを上書きする                                                              | `REPLACE INTO ...` |
| `"error"`   | インポートを終了し、エラーを報告します。                                                                | `INSERT INTO ...`  |
| `""`        | TiDB Lightningは競合するデータを検出または処理しません。主キーと一意キーの競合があるデータが存在する場合、後続のチェックサム処理でエラーが報告されます。 | なし                 |

> **注記：**
>
> 物理インポート モードでの競合検出結果は、 TiDB Lightningの内部実装と制限により、SQL ベースのインポートとは異なる場合があります。

戦略が`"error"`場合、競合データが検出されると、 TiDB Lightning はエラーを報告し、インポートを終了します。戦略が`"replace"`場合、競合データは[競合エラー](/tidb-lightning/tidb-lightning-error-resolution.md#conflict-errors)として扱われます。7 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)値が`0`より大きい場合、 TiDB Lightning は指定された数の競合エラーを許容します。デフォルト値は`9223372036854775807`で、ほぼすべてのエラーが許容されます。詳細については、 [エラー解決](/tidb-lightning/tidb-lightning-error-resolution.md)参照してください。

新しいバージョンの競合検出には、次の制限があります。

-   TiDB Lightningは、インポート前にすべてのデータを読み取ってエンコードすることで、潜在的な競合データを事前チェックします。検出プロセス中、 TiDB Lightningは`tikv-importer.sorted-kv-dir`使用して一時ファイルを保存します。検出が完了すると、 TiDB Lightningはインポートフェーズの結果を保持します。これにより、時間消費、ディスク容量の消費、およびデータ読み取りのためのAPIリクエストによる追加のオーバーヘッドが発生します。
-   新しいバージョンの競合検出は単一のノードでのみ機能し、並列インポートや`disk-quota`パラメータが有効になっているシナリオには適用されません。

新しいバージョンの競合検出では、パラメータ`precheck-conflict-before-import`を介してインポート前の競合検出を有効にするかどうかを制御します。元のデータに多くの競合データが含まれている場合、インポート前後の競合検出にかかる合計時間は、以前のバージョンよりも短くなります。したがって、競合レコードの割合が1%以上で、ローカルディスク容量が十分にあるシナリオでは、インポート前の競合検出を有効にすることをお勧めします。

### 競合検出の古いバージョン（v8.0.0 で非推奨） {#the-old-version-of-conflict-detection-deprecated-in-v8-0-0}

v8.0.0以降、古いバージョンの競合検出（ `tikv-importer.duplicate-resolution` ）は非推奨となりました。パラメータ`tikv-importer.duplicate-resolution`は将来のリリースで削除される予定です。 `tikv-importer.duplicate-resolution`が`remove`で、 `conflict.strategy`設定されていない場合、 TiDB Lightningは`conflict.strategy`の値を`"replace"`に割り当てることで、新しいバージョンの競合検出を自動的に有効化します。 `tikv-importer.duplicate-resolution`と`conflict.strategy`同時に設定することはできません。同時に設定するとエラーが発生しますのでご注意ください。

-   v7.3.0 から v7.6.0 までのバージョンでは、 `tikv-importer.duplicate-resolution`空の文字列でない場合、 TiDB Lightning は古いバージョンの競合検出を有効にします。
-   v7.2.0 以前のバージョンでは、 TiDB Lightning は古いバージョンの競合検出のみをサポートします。

競合検出の古いバージョンでは、 TiDB Lightning は次の 2 つの戦略を提供します。

-   `remove` (推奨): ターゲット テーブルからすべての競合レコードを記録して削除し、ターゲット TiDB の一貫した状態を確保します。
-   `none` : 重複レコードを検出しません。2 `none` 2 つの戦略の中でパフォーマンスが最も優れていますが、ターゲット TiDB でデータの不整合が発生する可能性があります。

v5.3より前のTiDB Lightningは競合検出をサポートしていません。競合データが存在する場合、インポートプロセスはチェックサムのステップで失敗します。競合検出を有効にすると、競合データが存在する場合、 TiDB Lightningはチェックサムのステップをスキップします（常に失敗するため）。

`order_line`テーブルに次のスキーマがあるとします。

```sql
CREATE TABLE IF NOT EXISTS `order_line` (
  `ol_o_id` int NOT NULL,
  `ol_d_id` int NOT NULL,
  `ol_w_id` int NOT NULL,
  `ol_number` int NOT NULL,
  `ol_i_id` int NOT NULL,
  `ol_supply_w_id` int DEFAULT NULL,
  `ol_delivery_d` datetime DEFAULT NULL,
  `ol_quantity` int DEFAULT NULL,
  `ol_amount` decimal(6,2) DEFAULT NULL,
  `ol_dist_info` char(24) DEFAULT NULL,
  PRIMARY KEY (`ol_w_id`,`ol_d_id`,`ol_o_id`,`ol_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

Lightning がインポート中に競合するデータを検出した場合は、次のように`lightning_task_info.conflict_error_v3`テーブルをクエリできます。

```sql
mysql> select table_name,index_name,key_data,row_data from conflict_error_v3 limit 10;
+---------------------+------------+----------+-----------------------------------------------------------------------------+
|  table_name         | index_name | key_data | row_data                                                                    |
+---------------------+------------+----------+-----------------------------------------------------------------------------+
| `tpcc`.`order_line` | PRIMARY    | 21829216 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 49931672 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 21829217 | (2677, 10, 10, 12, 76007, 10, NULL, 5, 9644.36, "bHuVoRfidQ0q2rJ6ZC9Hd12E") |
| `tpcc`.`order_line` | PRIMARY    | 49931673 | (2677, 10, 10, 12, 76007, 10, NULL, 5, 9644.36, "bHuVoRfidQ0q2rJ6ZC9Hd12E") |
| `tpcc`.`order_line` | PRIMARY    | 21829218 | (2677, 10, 10, 13, 85618, 10, NULL, 5, 7427.98, "t3rsesgi9rVAKi9tf6an5Rpv") |
| `tpcc`.`order_line` | PRIMARY    | 49931674 | (2677, 10, 10, 13, 85618, 10, NULL, 5, 7427.98, "t3rsesgi9rVAKi9tf6an5Rpv") |
| `tpcc`.`order_line` | PRIMARY    | 21829219 | (2677, 10, 10, 14, 15873, 10, NULL, 5, 133.21, "z1vH0e31tQydJGhfNYNa4ScD")  |
| `tpcc`.`order_line` | PRIMARY    | 49931675 | (2677, 10, 10, 14, 15873, 10, NULL, 5, 133.21, "z1vH0e31tQydJGhfNYNa4ScD")  |
| `tpcc`.`order_line` | PRIMARY    | 21829220 | (2678, 10, 10, 1, 44644, 10, NULL, 5, 8463.76, "TWKJBt5iJA4eF7FIVxnugNmz")  |
| `tpcc`.`order_line` | PRIMARY    | 49931676 | (2678, 10, 10, 1, 44644, 10, NULL, 5, 8463.76, "TWKJBt5iJA4eF7FIVxnugNmz")  |
+---------------------+------------+----------------------------------------------------------------------------------------+
10 rows in set (0.14 sec)
```

保持する必要があるレコードを手動で識別し、これらのレコードをテーブルに挿入できます。

## インポート中にスケジュールを一時停止する範囲 {#scope-of-pausing-scheduling-during-import}

v6.2.0以降、 TiDB Lightningはデータインポートによるオンラインアプリケーションへの影響を制限するメカニズムを実装しました。この新しいメカニズムでは、 TiDB Lightningはグローバルスケジューリングを一時停止するのではなく、ターゲットテーブルデータが格納されているリージョンのスケジューリングのみを一時停止します。これにより、インポートによるオンラインアプリケーションへの影響が大幅に軽減されます。

バージョン7.1.0以降では、 TiDB Lightningパラメータ[`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)を使用して、スケジュールの一時停止範囲を制御できます。デフォルト値は`"table"`で、これはターゲットテーブルデータが格納されているリージョンのみのスケジュールが一時停止されることを意味します。クラスター内にビジネストラフィックがない場合、インポート中に他のスケジュールからの干渉を回避するため、このパラメータを`"global"`に設定することをお勧めします。

<Note>

TiDB Lightning は、すでにデータが含まれているテーブルへのデータのインポートをサポートしていません。

TiDB クラスタは v6.1.0 以降である必要があります。それより前のバージョンの場合、 TiDB Lightning は以前の動作を維持しており、インポート中にスケジュールがグローバルに一時停止され、オンラインアプリケーションに重大な影響を及ぼします。

</Note>

デフォルトでは、 TiDB Lightning はクラスタのスケジュールを可能な限り最小限の範囲で一時停止します。ただし、デフォルト設定では、高速インポートによってクラスタのパフォーマンスが影響を受ける可能性があります。これを回避するには、以下のオプションを設定することで、インポート速度やクラスタのパフォーマンスに影響を与える可能性のあるその他の要因を制御できます。

```toml
[tikv-importer]
# Limits the bandwidth in which TiDB Lightning writes data into each TiKV node in the physical import mode.
store-write-bwlimit = "128MiB"

[tidb]
# Use smaller concurrency to reduce the impact of Checksum and Analyze on the transaction latency.
distsql-scan-concurrency = 3
```

TPCCを使用してオンラインアプリケーションをシミュレートし、 TiDB Lightningを使用してTiDBクラスターにデータをインポートすることで、データインポートがTPCCの結果に与える影響を測定できます。テスト結果は次のとおりです。

| 同時実行性 | TPM     | P99     | P90     | 平均      |
| ----- | ------- | ------- | ------- | ------- |
| 1     | 20%～30% | 60%～80% | 30%～50% | 30%～40% |
| 8     | 15%～25% | 70%～80% | 35%～45% | 20%～35% |
| 16    | 20%～25% | 55%～85% | 35%～40% | 20%～30% |
| 64    | 重大な影響なし |         |         |         |
| 256   | 重大な影響なし |         |         |         |

上の表のパーセンテージは、データのインポートが TPCC の結果に与える影響を示しています。

-   TPM 列の場合、数字は TPM の減少率を示します。
-   P99、P90、AVG 列の場合、数値はレイテンシーの増加率を示します。

テスト結果によると、同時実行数が少ないほど、データインポートがTPCC結果に与える影響は大きくなります。同時実行数が64以上の場合、データインポートがTPCC結果に与える影響はごくわずかです。

したがって、TiDBクラスタにレイテンシの影響を受けやすいアプリケーションがあり、同時実行性が低い場合は、 TiDB Lightningを使用してクラスタにデータをインポート**しないこと**を強くお勧めします。これは、オンラインアプリケーションに重大な影響を与える可能性があります。

## パフォーマンスチューニング {#performance-tuning}

**物理インポート モードのインポート パフォーマンスを向上させる最も直接的かつ効果的な方法は次のとおりです。**

-   **Lightning がデプロイされているノードのハードウェア、特に CPU と`sorted-key-dir`のstorageデバイスをアップグレードします。**
-   **水平方向のスケーリングを実現するには、<a href="/tidb-lightning/tidb-lightning-distributed-import.md">並列インポート</a>機能を使用します。**

TiDB Lightning は、物理インポートモードでのインポートパフォーマンスに影響を与える同時実行関連の設定をいくつか提供しています。ただし、長期的な経験から、以下の 4 つの設定項目はデフォルト値のままにしておくことをお勧めします。これらの設定項目を調整しても、パフォーマンスの大幅な向上は期待できません。

    [lightning]
    # The maximum concurrency of engine files.
    # Each table is split into one "index engine" to store indices, and multiple
    # "data engines" to store row data. These settings control the maximum
    # concurrent number for each type of engines.
    # The two settings controls the maximum concurrency of the two engine files.
    index-concurrency = 2
    table-concurrency = 6

    # The concurrency of data. The default value is the number of logical CPUs.
    region-concurrency =

    # The maximum concurrency of I/O. When the concurrency is too high, the disk
    # cache may be frequently refreshed, causing the cache miss and read speed
    # to slow down. For different storage mediums, this parameter may need to be
    # adjusted to achieve the best performance.
    io-concurrency = 5

インポート中、各テーブルはインデックスを格納するための 1 つの「インデックス エンジン」と、行データを格納するための複数の「データ エンジン」に分割されます。

`index-concurrency`インデックスエンジンの最大同時実行数を制御します。2 `index-concurrency`調整する場合は、CPUを最大限に活用するために`index-concurrency * the number of source files of each table > region-concurrency`に設定してください。この比率は通常 1.5 ～ 2 です。6 `index-concurrency`高く設定しすぎず、2（デフォルト）より低く設定しないでください`index-concurrency`と高く設定しすぎると、パイプラインが過剰に構築され、インデックスエンジンのインポートステージが滞ってしまいます。

`table-concurrency`についても同様です。CPUを最大限に活用するには、 `table-concurrency * the number of source files of each table > region-concurrency`設定してください。推奨値は`region-concurrency * 4 / the number of source files of each table`程度で、4 未満には設定しないでください。

テーブルが大きい場合、Lightning はテーブルを 100 GiB 単位の複数のバッチに分割します。同時実行性は`table-concurrency`で制御されます。

`index-concurrency`と`table-concurrency`インポート速度にほとんど影響しません。デフォルト値のままで問題ありません。

`io-concurrency`ファイル読み取りの同時実行を制御します。デフォルト値は 5 です。常に 5 つのハンドルのみが読み取り操作を実行しています。ファイル読み取り速度は通常ボトルネックにはならないため、この設定はデフォルト値のままで問題ありません。

ファイルデータが読み込まれた後、Lightning はデータのエンコードやローカルでのソートなどの後処理を実行する必要があります。これらの操作の同時実行数は`region-concurrency`で制御されます。デフォルト値は CPU コア数です。この設定はデフォルト値のままで問題ありません。Lightning は他のコンポーネントとは別のサーバーにデプロイすることをお勧めします。Lightning を他のコンポーネントと一緒にデプロイする必要がある場合は、負荷に応じて`region-concurrency`の値を下げる必要があります。

TiKVの[`num-threads`](/tikv-configuration-file.md#num-threads)設定もパフォーマンスに影響を与える可能性があります。新しいクラスターでは、CPUコア数を`num-threads`に設定することをお勧めします。

## ディスククォータの設定<span class="version-mark">v6.2.0 の新機能</span> {#configure-disk-quota-span-class-version-mark-new-in-v6-2-0-span}

物理インポートモードでデータをインポートすると、 TiDB Lightning は元のデータをエンコード、ソート、分割するために、ローカルディスク上に多数の一時ファイルを作成します。ローカルディスクの空き容量が不足すると、 TiDB Lightning は書き込みエラーを報告し、終了します。

このような状況を回避するには、 TiDB Lightningのディスククォータを設定できます。一時ファイルのサイズがディスククォータを超えると、 TiDB Lightning はソースデータの読み取りと一時ファイルの書き込みプロセスを一時停止します。TiDB TiDB Lightning は、ソートされたキーと値のペアを TiKV に書き込むことを優先します。ローカルの一時ファイルを削除した後、 TiDB Lightning はインポートプロセスを続行します。

ディスク クォータを有効にするには、構成ファイルに次の構成を追加します。

```toml
[tikv-importer]
# MaxInt64 by default, which is 9223372036854775807 bytes.
disk-quota = "10GB"
backend = "local"

[cron]
# The interval of checking disk quota. 60 seconds by default.
check-disk-quota = "30s"
```

`disk-quota` TiDB Lightningが使用するstorage容量を制限します。デフォルト値は MaxInt64 で、9223372036854775807 バイトです。この値はインポートに必要なディスク容量よりもはるかに大きいため、デフォルト値のままにしておくとディスククォータを設定していないのと同じになります。

`check-disk-quota`はディスク クォータをチェックする間隔です。デフォルト値は 60 秒です。TiDB TiDB Lightning がディスク クォータをチェックすると、関連データの排他ロックが取得され、すべてのインポート スレッドがブロックされます。そのため、 TiDB Lightning が毎回書き込み前にディスク クォータをチェックすると、書き込み効率が大幅に低下します (シングル スレッド書き込みと同じくらい遅くなります)。効率的な書き込みを実現するために、毎回書き込み前にディスク クォータをチェックするのではなく、 TiDB Lightning はすべてのインポート スレッドを一時停止し、 `check-disk-quota`間隔ごとにディスク クォータをチェックします。つまり、 `check-disk-quota`の値を大きい値に設定すると、 TiDB Lightningが使用するディスク領域が設定したディスク クォータを超え、ディスク クォータが無効になる可能性があります。したがって、 `check-disk-quota`の値は小さい値に設定することをお勧めします。この項目の具体的な値は、 TiDB Lightning が実行されている環境によって決まります。環境が異なると、 TiDB Lightning が一時ファイルを異なる速度で書き込みます。理論的には、速度が速いほど、 `check-disk-quota`の値は小さくなるはずです。
