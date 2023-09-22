---
title: Use Physical Import Mode
summary: Learn how to use the physical import mode in TiDB Lightning.
---

# 物理インポートモードを使用する {#use-physical-import-mode}

このドキュメントでは、構成ファイルの作成、パフォーマンスのチューニング、ディスク クォータの構成など、 TiDB Lightningの[物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)の使用方法を紹介します。

物理インポート モードには制限があります。物理インポートモードを使用する前に、必ず[制限事項](/tidb-lightning/tidb-lightning-physical-import-mode.md#limitations)をお読みください。

## 物理インポート モードを構成して使用する {#configure-and-use-the-physical-import-mode}

以下の設定ファイルを使用すると、物理インポートモードでデータインポートを実行できます。

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
# Import mode. "local" means using the physical import mode.
backend = "local"

# The method to resolve the conflicting data.
duplicate-resolution = 'remove'

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
# Required. The address of any pd-server from the cluster.
pd-addr = "172.16.31.4:2379"
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

完全な構成ファイルについては、 [設定ファイルとコマンドラインパラメータ](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合の検出 {#conflict-detection}

競合するデータとは、同じ PK/UK 列データを持つ 2 つ以上のレコードを指します。データ ソースに競合するデータが含まれている場合、テーブル内の実際の行数は、一意のインデックスを使用したクエリによって返される合計行数と異なります。

TiDB Lightning は、競合するデータを検出するための 3 つの戦略を提供します。

-   `remove` (推奨): 競合するレコードをすべて記録し、ターゲット テーブルから削除して、ターゲット TiDB 内の一貫した状態を確保します。
-   `none` : 重複レコードを検出しません。 `none` 2 つの戦略の中で最高のパフォーマンスを示しますが、ターゲット TiDB でデータの不整合が生じる可能性があります。

v5.3 より前のTiDB Lightning は競合検出をサポートしていません。競合するデータがある場合、インポート プロセスはチェックサム ステップで失敗します。競合検出が有効になっている場合、競合するデータがある場合、 TiDB Lightning はチェックサム ステップをスキップします (チェックサム ステップは常に失敗するため)。

`order_line`テーブルに次のスキーマがあるとします。

```sql
CREATE TABLE IF NOT EXISTS `order_line` (
  `ol_o_id` int(11) NOT NULL,
  `ol_d_id` int(11) NOT NULL,
  `ol_w_id` int(11) NOT NULL,
  `ol_number` int(11) NOT NULL,
  `ol_i_id` int(11) NOT NULL,
  `ol_supply_w_id` int(11) DEFAULT NULL,
  `ol_delivery_d` datetime DEFAULT NULL,
  `ol_quantity` int(11) DEFAULT NULL,
  `ol_amount` decimal(6,2) DEFAULT NULL,
  `ol_dist_info` char(24) DEFAULT NULL,
  PRIMARY KEY (`ol_w_id`,`ol_d_id`,`ol_o_id`,`ol_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

Lightning がインポート中に競合するデータを検出した場合は、次のように`lightning_task_info.conflict_error_v1`テーブルをクエリできます。

```sql
mysql> select table_name,index_name,key_data,row_data from conflict_error_v1 limit 10;
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

保持する必要があるレコードを手動で特定し、これらのレコードをテーブルに挿入できます。

## インポート中のスケジュール一時停止の範囲 {#scope-of-pausing-scheduling-during-import}

v6.2.0 以降、 TiDB Lightning は、オンライン アプリケーションへのデータ インポートの影響を制限するメカニズムを実装します。新しいメカニズムにより、 TiDB Lightning はグローバル スケジューリングを一時停止せず、ターゲット テーブル データを保存するリージョンのスケジューリングのみを一時停止します。これにより、オンライン アプリケーションに対するインポートの影響が大幅に軽減されます。

v7.1.0 以降、 TiDB Lightningパラメータ[`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md)を使用して、スケジュールの一時停止の範囲を制御できます。デフォルト値は`"table"`です。これは、ターゲット テーブル データを保存するリージョンに対してのみスケジュールが一時停止されることを意味します。クラスター内にビジネス トラフィックがない場合は、インポート中の他のスケジュールによる干渉を避けるために、このパラメーターを`"global"`に設定することをお勧めします。

<Note>

TiDB Lightning は、既にデータが含まれているテーブルへのデータのインポートをサポートしていません。

TiDB クラスターは v6.1.0 以降のバージョンである必要があります。以前のバージョンの場合、 TiDB Lightning は古い動作を維持しており、これによりスケジュールがグローバルに一時停止され、インポート中にオンライン アプリケーションに重大な影響が与えられます。

</Note>

デフォルトでは、 TiDB Lightning はクラスターのスケジューリングを可能な限り最小限の範囲で一時停止します。ただし、デフォルト構成では、クラスターのパフォーマンスが高速インポートの影響を受ける可能性があります。これを回避するには、次のオプションを構成して、クラスターのパフォーマンスに影響を与える可能性のあるインポート速度やその他の要因を制御できます。

```toml
[tikv-importer]
# Limits the bandwidth in which TiDB Lightning writes data into each TiKV node in the physical import mode.
store-write-bwlimit = "128MiB"

[tidb]
# Use smaller concurrency to reduce the impact of Checksum and Analyze on the transaction latency.
distsql-scan-concurrency = 3
```

## 性能調整 {#performance-tuning}

**物理インポート モードのインポート パフォーマンスを向上させる最も直接的かつ効果的な方法は次のとおりです。**

-   **Lightning がデプロイされているノードのハードウェア (特に`sorted-key-dir`の CPU とstorageデバイス) をアップグレードします。**
-   **水平方向のスケーリングを実現するには、<a href="/tidb-lightning/tidb-lightning-distributed-import.md">平行インポート</a>機能を使用します。**

TiDB Lightning は、物理インポート モードでのインポート パフォーマンスに影響を与えるいくつかの同時実行関連の構成を提供します。ただし、長年の経験から、次の 4 つの設定項目はデフォルト値のままにすることをお勧めします。 4 つの構成項目を調整しても、パフォーマンスは大幅に向上しません。

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

インポート中、各テーブルはインデックスを格納する 1 つの「インデックス エンジン」と行データを格納する複数の「データ エンジン」に分割されます。

`index-concurrency`インデックス エンジンの最大同時実行性を制御します。 `index-concurrency`を調整するときは、CPU が完全に活用されるように`index-concurrency * the number of source files of each table > region-concurrency`を調整してください。通常、比率は 1.5 ～ 2 の間です`index-concurrency`を大きすぎたり、2 (デフォルト) より低く設定したりしないでください。 `index-concurrency`が大きすぎると、構築されるパイプラインが多すぎて、インデックス エンジンのインポート ステージが蓄積されてしまいます。

`table-concurrency`についても同様です。 CPU が最大限に活用されるようにするには、 `table-concurrency * the number of source files of each table > region-concurrency`を確認してください。推奨値は約`region-concurrency * 4 / the number of source files of each table`であり、4 以上です。

テーブルが大きい場合、Lightning はテーブルを 100 GiB の複数のバッチに分割します。同時実行性は`table-concurrency`によって制御されます。

`index-concurrency`と`table-concurrency`はインポート速度にほとんど影響しません。デフォルト値のままにすることができます。

`io-concurrency`ファイル読み取りの同時実行性を制御します。デフォルト値は 5 です。常に 5 つのハンドルのみが読み取り操作を実行します。通常、ファイルの読み取り速度はボトルネックではないため、この構成はデフォルト値のままにして問題ありません。

ファイルデータが読み取られた後、Lightning はローカルでのデータのエンコードや並べ替えなどの後処理を行う必要があります。これらの操作の同時実行性は`region-concurrency`によって制御されます。デフォルト値は CPU コアの数です。この設定はデフォルト値のままにすることができます。 Lightning を他のコンポーネントとは別のサーバーにデプロイすることをお勧めします。 Lightning を他のコンポーネントと一緒にデプロイする必要がある場合は、負荷に応じて`region-concurrency`の値を下げる必要があります。

TiKV の[`num-threads`](/tikv-configuration-file.md#num-threads)構成もパフォーマンスに影響を与える可能性があります。新しいクラスターの場合は、CPU コアの数を`num-threads`に設定することをお勧めします。

## ディスク クォータの構成<span class="version-mark">v6.2.0 の新機能</span> {#configure-disk-quota-span-class-version-mark-new-in-v6-2-0-span}

物理インポート モードでデータをインポートすると、 TiDB Lightning はローカル ディスク上に多数の一時ファイルを作成し、元のデータをエンコード、並べ替え、分割します。ローカル ディスク容量が不十分な場合、 TiDB Lightning はエラーを報告し、書き込み失敗のために終了します。

この状況を回避するには、 TiDB Lightningのディスク クォータを構成します。一時ファイルのサイズがディスク クォータを超えると、 TiDB Lightning はソース データの読み取りと一時ファイルの書き込みプロセスを一時停止します。 TiDB Lightning は、ソートされたキーと値のペアを TiKV に優先的に書き込みます。ローカル一時ファイルを削除した後、 TiDB Lightning はインポート プロセスを続行します。

ディスク クォータを有効にするには、次の構成を構成ファイルに追加します。

```toml
[tikv-importer]
# MaxInt64 by default, which is 9223372036854775807 bytes.
disk-quota = "10GB"
backend = "local"

[cron]
# The interval of checking disk quota. 60 seconds by default.
check-disk-quota = "30s"
```

`disk-quota` TiDB Lightningによって使用されるstorageスペースを制限します。デフォルト値は MaxInt64、つまり 9223372036854775807 バイトです。この値は、インポートに必要なディスク容量よりもはるかに大きいため、デフォルト値のままにすることは、ディスク クォータを設定しないことと同じです。

`check-disk-quota`はディスク クォータをチェックする間隔です。デフォルト値は 60 秒です。 TiDB Lightning はディスク クォータをチェックするときに、関連するデータの排他ロックを取得し、すべてのインポート スレッドをブロックします。したがって、 TiDB Lightning が書き込みのたびにディスク クォータをチェックすると、書き込み効率が大幅に低下します (シングル スレッド書き込みと同じくらい遅くなります)。効率的な書き込みを実現するために、毎回の書き込み前にディスク クォータはチェックされません。代わりに、 TiDB Lightning はすべてのインポート スレッドを一時停止し、 `check-disk-quota`間隔ごとにディスク クォータをチェックします。つまり、値`check-disk-quota`が大きな値に設定されている場合、 TiDB Lightningによって使用されるディスク容量が設定したディスク クォータを超える可能性があり、その結果、ディスク クォータが無効になります。したがって、 `check-disk-quota`の値を小さい値に設定することをお勧めします。この項目の具体的な値は、 TiDB Lightningが実行されている環境によって決まります。異なる環境では、 TiDB Lightning は異なる速度で一時ファイルを書き込みます。理論的には、速度が速いほど、 `check-disk-quota`の値は小さくする必要があります。
