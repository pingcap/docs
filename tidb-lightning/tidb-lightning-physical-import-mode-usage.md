---
title: Use Physical Import Mode
summary: TiDB Lightningの物理インポートモードの使い方を学びましょう。
---

# 物理インポートモードを使用する {#use-physical-import-mode}

このドキュメントでは、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)の使用方法について説明します。具体的には、設定ファイルの作成、パフォーマンスのチューニング、ディスククォータの設定などが含まれます。

物理インポート モードには制限があります。物理インポートモードを使用する前に、 [制限事項](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations)必ずお読みください。

## 物理インポートモードを設定して使用する {#configure-and-use-the-physical-import-mode}

物理インポートモードを使用してデータインポートを実行するには、以下の設定ファイルを使用できます。

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

競合データとは、主キーまたは一意キー列のデータが同じレコードが2つ以上存在する状態を指します。データソースに競合データが含まれており、競合検出機能が有効になっていない場合、テーブルの実際の行数は、一意インデックスを使用したクエリによって返される行の総数と異なります。

競合検出には2つのバージョンがあります。

-   `conflict`設定項目によって制御される、新しいバージョンの競合検出。
-   `tikv-importer.duplicate-resolution`設定項目によって制御される、競合検出の旧バージョン（v8.0.0 で非推奨となり、将来のリリースで削除されます）。

### 衝突検出の新しいバージョン {#the-new-version-of-conflict-detection}

設定値の意味は以下のとおりです。

| 戦略          | 競合するデータのデフォルト動作                                                                            | 対応するSQL文           |
| :---------- | :----------------------------------------------------------------------------------------- | :----------------- |
| `"replace"` | 最新のデータを保持し、古いデータを上書きする                                                                     | `REPLACE INTO ...` |
| `"error"`   | インポートを終了し、エラーを報告します。                                                                       | `INSERT INTO ...`  |
| `""`        | TiDB Lightningは、競合するデータを検出したり処理したりしません。主キーと一意キーが競合するデータが存在する場合、後続のチェックサム計算ステップでエラーが報告されます。 | なし                 |

> **Note:**
>
> TiDB Lightningの内部実装と制限により、物理インポートモードでの競合検出結果は、SQLベースのインポート結果と異なる場合があります。

戦略が`"error"`で競合データが検出された場合、 TiDB Lightning はエラーを報告してインポートを終了します。戦略が`"replace"`の場合、競合データは[競合エラー](/tidb-lightning/tidb-lightning-error-resolution.md#conflict-errors)として扱われます。conflict.threshold [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)値が`0`より大きい場合、 TiDB Lightning は指定された数の競合エラーを許容します。デフォルト値は`9223372036854775807`で、これはほぼすべてのエラーが許容されることを意味します。詳細については、を参照してください。 [エラー解決](/tidb-lightning/tidb-lightning-error-resolution.md)。

新しいバージョンの競合検出機能には、以下の制限事項があります。

-   TiDB Lightning はインポート前に、すべてのデータを読み込んでエンコードすることで、競合する可能性のあるデータを事前チェックします。検出処理中、 TiDB Lightningは`tikv-importer.sorted-kv-dir`を使用して一時ファイルを保存します。検出が完了すると、 TiDB Lightning はインポートフェーズのために結果を保持します。これにより、処理時間、ディスク容量、およびデータ読み取りのための API リクエストに余分なオーバーヘッドが発生します。
-   新しいバージョンの競合検出は単一ノードでのみ機能し、並列インポートや`disk-quota`パラメーターが有効になっているシナリオには適用されません。

新しいバージョンの競合検出では`precheck-conflict-before-import`パラメータを使用して、インポート前の競合検出を有効にするかどうかを制御します。元のデータに競合データが多く含まれている場合、インポート前後の競合検出にかかる合計時間は、旧バージョンよりも短くなります。そのため、競合レコードの割合が 1% 以上で、ローカルディスクの空き容量が十分な場合は、インポート前の競合検出を有効にすることをお勧めします。

### 旧バージョンの競合検出機能（v8.0.0で非推奨） {#the-old-version-of-conflict-detection-deprecated-in-v800}

バージョン 8.0.0 以降、競合検出の旧バージョン ( `tikv-importer.duplicate-resolution` ) は非推奨となります。 `tikv-importer.duplicate-resolution`パラメータは今後のリリースで削除されます。 `tikv-importer.duplicate-resolution`が`remove`であり、 `conflict.strategy`が設定されていない場合、 TiDB Lightning は`conflict.strategy`の値`"replace"` 。 `tikv-importer.duplicate-resolution`と`conflict.strategy`は同時に設定できません。同時に設定するとエラーが発生しますのでご注意ください。

-   バージョン v7.3.0 から v7.6.0 の間では、 `tikv-importer.duplicate-resolution`空文字列でない場合、 TiDB Lightning は古いバージョンの競合検出を有効にします。
-   TiDB Lightningは、v7.2.0以前のバージョンでは、古いバージョンの競合検出のみをサポートしています。

旧バージョンの競合検出では、 TiDB Lightningは2つの戦略を提供していました。

-   `remove` (推奨): ターゲット TiDB の一貫した状態を確保するために、ターゲット テーブルから競合するすべてのレコードを記録して削除します。
-   `none` : 重複レコードを検出しません。 `none` 2 つの戦略の中で最も優れたパフォーマンスを発揮しますが、ターゲット TiDB のデータに不整合が生じる可能性があります。

バージョン5.3より前のTiDB Lightningは、競合検出をサポートしていません。競合データが存在する場合、インポート処理はチェックサムの段階で失敗します。競合検出が有効になっている場合、競合データが存在すると、 TiDB Lightningはチェックサムの段階をスキップします（常に失敗するため）。

`order_line`テーブルに以下のスキーマがあるとします。

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

Lightning がインポート中に競合するデータを検出した場合、次のように`lightning_task_info.conflict_error_v3`テーブルをクエリできます。

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

保持する必要のあるレコードを手動で特定し、それらのレコードをテーブルに挿入することができます。

## インポート中のスケジュール一時停止の範囲 {#scope-of-pausing-scheduling-during-import}

バージョン6.2.0以降、 TiDB Lightningはデータインポートがオンラインアプリケーションに与える影響を制限するメカニズムを実装しました。この新しいメカニズムにより、 TiDB Lightningはグローバルスケジューリングを一時停止するのではなく、対象テーブルデータが格納されているリージョンのみのスケジューリングを一時停止します。これにより、インポートがオンラインアプリケーションに与える影響が大幅に軽減されます。

バージョン7.1.0以降では、 TiDB Lightningパラメータ[`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)を使用して、スケジューリングの一時停止範囲を制御できます。デフォルト値は`"table"`で、これは対象テーブルデータを格納するリージョンのみのスケジューリングが一時停止されることを意味します。クラスタに業務トラフィックがない場合は、インポート中に他のスケジューリングによる干渉を避けるため、このパラメータを`"global"`に設定することをお勧めします。

<Note>

TiDB Lightningは、既にデータが含まれているテーブルへのデータインポートをサポートしていません。

TiDBクラスタはv6.1.0以降のバージョンである必要があります。それ以前のバージョンでは、 TiDB Lightningは従来の動作を維持し、グローバルなスケジューリングを一時停止するため、インポート中にオンラインアプリケーションに深刻な影響を与えます。

</Note>

TiDB Lightning はデフォルトでは、可能な限り最小限の時間だけクラスタのスケジューリングを一時停止します。しかし、デフォルト設定では、高速インポートによってクラスタのパフォーマンスが影響を受ける可能性があります。これを回避するには、インポート速度やクラスタのパフォーマンスに影響を与える可能性のあるその他の要因を制御するために、次のオプションを設定できます。

```toml
[tikv-importer]
# Limits the bandwidth in which TiDB Lightning writes data into each TiKV node in the physical import mode.
store-write-bwlimit = "128MiB"

[tidb]
# Use smaller concurrency to reduce the impact of Checksum and Analyze on the transaction latency.
distsql-scan-concurrency = 3
```

TPCCを使用してオンラインアプリケーションをシミュレートし、 TiDB Lightningを使用してTiDBクラスタにデータをインポートすることで、データインポートがTPCCの結果に与える影響を測定できます。テスト結果は以下のとおりです。

| 並行処理 | TPM     | P99     | P90     | 平均      |
| ---- | ------- | ------- | ------- | ------- |
| 1    | 20%～30% | 60%～80% | 30%～50% | 30%～40% |
| 8    | 15%～25% | 70%～80% | 35%～45% | 20%～35% |
| 16   | 20%～25% | 55%～85% | 35%～40% | 20%～30% |
| 64   | 重大な影響なし |         |         |         |
| 256  | 重大な影響なし |         |         |         |

前述の表のパーセンテージは、データインポートがTPCCの結果に与える影響を示しています。

-   TPMの列の数値は、TPMの減少率（パーセント）を示しています。
-   P99、P90、およびAVG列の数値は、レイテンシーの増加率を示しています。

テスト結果によると、同時実行数が少ないほど、データインポートがTPCCの結果に与える影響は大きくなる。同時実行数が64以上の場合、データインポートがTPCCの結果に与える影響はごくわずかである。

したがって、TiDBクラスタにレイテンシに敏感なアプリケーションがあり、かつ同時実行数が少ない場合は、 TiDB Lightningを使用してクラスタにデータをインポートし**ないこと**を強くお勧めします。これは、オンラインアプリケーションに大きな影響を与える可能性があります。

## パフォーマンスチューニング {#performance-tuning}

**物理インポートモードのインポートパフォーマンスを向上させるための最も直接的かつ効果的な方法は以下のとおりです。**

-   **Lightningがデプロイされているノードのハードウェア、特にCPUと`sorted-key-dir`のストレージデバイスをアップグレードしてください。**
-   **<a href="/tidb-lightning/tidb-lightning-distributed-import.md">並列インポート</a>機能を使用して、水平方向のスケーリングを実現します。**

TiDB Lightningは、物理インポートモードでのインポートパフォーマンスに影響を与える同時実行性関連の設定項目をいくつか提供しています。しかし、長年の経験から、以下の4つの設定項目はデフォルト値のままにしておくことをお勧めします。これらの設定項目を調整しても、パフォーマンスが大幅に向上することはありません。

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

インポート処理中、各テーブルはインデックスを格納するための「インデックスエンジン」1つと、行データを格納するための複数の「データエンジン」に分割されます。

`index-concurrency`インデックス エンジンの最大同時実行数を制御します。 `index-concurrency`を調整する際は、CPU が最大限に活用されるように`index-concurrency * the number of source files of each table > region-concurrency`も必ず調整してください。比率は通常 1.5 ～ 2 です。 `index-concurrency`を高く設定しすぎたり、2 (デフォルト値) より低く設定したりしないでください。 `index-concurrency`高すぎると、パイプラインが多数構築され、インデックス エンジンのインポート ステージが滞留します。

`table-concurrency`についても同様です。 `table-concurrency * the number of source files of each table > region-concurrency`がCPUをフル活用していることを確認してください。推奨値は`region-concurrency * 4 / the number of source files of each table`前後で、4を下回らないようにしてください。

テーブルが大きい場合、Lightning はテーブルを 100 GiB の複数のバッチに分割します。同時実行は`table-concurrency`によって制御されます。

`index-concurrency`と`table-concurrency`はインポート速度にほとんど影響を与えません。デフォルト値のままで問題ありません。

`io-concurrency`ファイル読み取りの同時実行数を制御します。デフォルト値は 5 です。常に 5 つのハンドルのみが読み取り操作を実行します。ファイル読み取り速度は通常ボトルネックにならないため、この設定はデフォルト値のままにしておくことができます。

ファイルデータが読み込まれた後、Lightning はデータのエンコードやローカルでのソートなどの後処理を行う必要があります。これらの操作の同時実行は`region-concurrency`によって制御されます。デフォルト値は CPU コア数です。この設定はデフォルト値のままにしておくことができます。Lightning は他のコンポーネントとは別のサーバーにデプロイすることをお勧めします。Lightning を他のコンポーネントと一緒にデプロイする必要がある場合は、負荷に応じて`region-concurrency`の値を下げる必要があります。

TiKV の[`num-threads`](/tikv-configuration-file.md#num-threads)設定もパフォーマンスに影響を与える可能性があります。新しいクラスターの場合は、 `num-threads` CPU コア数に設定することをお勧めします。

## ディスククォータの設定<span class="version-mark">（v6.2.0の新機能）</span> {#configure-disk-quota-new-in-v620}

物理インポートモードでデータをインポートする場合、 TiDB Lightning は元のデータをエンコード、ソート、分割するために、ローカルディスク上に多数の一時ファイルを作成します。ローカルディスクの空き容量が不足すると、書き込みエラーが発生し、 TiDB Lightning はエラーを報告して終了します。

この状況を回避するには、 TiDB Lightningのディスククォータを設定できます。一時ファイルのサイズがディスククォータを超えると、 TiDB Lightning はソースデータの読み込みと一時ファイルの書き込み処理を一時停止します。TiDB Lightning は、ソートされたキーと値のペアを TiKV に書き込むことを優先します。ローカルの一時ファイルを削除した後、 TiDB Lightning はインポート処理を再開します。

ディスククォータを有効にするには、設定ファイルに次の設定を追加してください。

```toml
[tikv-importer]
# MaxInt64 by default, which is 9223372036854775807 bytes.
disk-quota = "10GB"
backend = "local"

[cron]
# The interval of checking disk quota. 60 seconds by default.
check-disk-quota = "30s"
```

`disk-quota` TiDB Lightningが使用するストレージ容量を制限します。デフォルト値は MaxInt64 で、9223372036854775807 バイトです。この値はインポートに必要なディスク容量よりもはるかに大きいため、デフォルト値のままにしておくことは、ディスククォータを設定しないことと同じです。

`check-disk-quota`は、ディスククォータをチェックする間隔です。デフォルト値は 60 秒です。TiDB Lightning がディスククォータをチェックすると、関連データに対して排他ロックを取得し、すべてのインポートスレッドをブロックします。そのため、 TiDB Lightning が書き込みの前に毎回ディスククォータをチェックすると、書き込み効率が大幅に低下します (シングルスレッド書き込みと同じくらい遅くなります)。効率的な書き込みを実現するために、ディスククォータは書き込みの前に毎回チェックされません。代わりに、 TiDB Lightning はすべてのインポートスレッドを一時停止し、 `check-disk-quota`間隔ごとにディスククォータをチェックします。つまり、 `check-disk-quota`の値を大きな値に設定すると、 TiDB Lightningが使用するディスク領域が設定したディスククォータを超える可能性があり、ディスククォータが無効になります。したがって、 `check-disk-quota`の値は小さい値に設定することをお勧めします。この項目の具体的な値は、 TiDB Lightningが実行される環境によって決まります。TiDB Lightning は、環境によって一時ファイルの書き込み速度が異なります。理論的には、書き込み速度が速いほど、 `check-disk-quota`の値は小さくする必要があります。
