---
title: Use Physical Import Mode
summary: Learn how to use the physical import mode in TiDB Lightning.
---

# 物理インポート モードを使用する {#use-physical-import-mode}

このドキュメントでは、構成ファイルの作成、パフォーマンスのチューニング、ディスク クォータの構成など、 TiDB Lightningで[物理インポート モード](/tidb-lightning/tidb-lightning-physical-import-mode.md)を使用する方法を紹介します。

## 物理インポート モードの構成と使用 {#configure-and-use-the-physical-import-mode}

次の構成ファイルを使用して、物理インポート モードを使用してデータ インポートを実行できます。

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
# Import mode. "local" means using the physical import mode.
backend = "local"

# The method to resolve the conflicting data.
duplicate-resolution = 'remove'

# The directory of local KV sorting.
sorted-kv-dir = "./some-dir"

# Limits the bandwidth in which TiDB Lightning writes data into each TiKV
# node in the physical import mode. 0 by default, which means no limit.
# store-write-bwlimit = "128MiB"

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

完全な構成ファイルについては、 [構成ファイルとコマンド ライン パラメータ](/tidb-lightning/tidb-lightning-configuration.md)を参照してください。

## 競合の検出 {#conflict-detection}

競合するデータとは、PK/UK 列のデータが同じである 2 つ以上のレコードを指します。データ ソースに競合するデータが含まれている場合、テーブル内の実際の行数は、一意のインデックスを使用したクエリによって返される合計行数とは異なります。

TiDB Lightning は、競合するデータを検出するための 3 つの戦略を提供します。

-   `record` : 競合するレコードのみをターゲット TiDB の`lightning_task_info.conflict_error_v1`テーブルに記録します。ターゲット TiKV の必要なバージョンは v5.2.0 以降のバージョンであることに注意してください。それ以外の場合は、&#39;none&#39; にフォールバックします。
-   `remove` (推奨): `record`戦略のように、競合するすべてのレコードを記録します。ただし、競合するすべてのレコードをターゲット テーブルから削除して、ターゲット TiDB で一貫した状態を確保します。
-   `none` : 重複レコードを検出しません。 `none` 3 つの戦略で最高のパフォーマンスを発揮しますが、ターゲット TiDB でデータの一貫性が失われる可能性があります。

v5.3 より前では、Lightning は競合検出をサポートしていません。競合するデータがある場合、インポート プロセスはチェックサム ステップで失敗します。競合検出が有効になっている場合、戦略`record`または`remove`に関係なく、競合するデータがある場合、Lightning はチェックサム手順をスキップします (常に失敗するため)。

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

インポート中に Lightning が競合するデータを検出した場合、次のように`lightning_task_info.conflict_error_v1`テーブルをクエリできます。

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

保持する必要があるレコードを手動で識別し、これらのレコードをテーブルに挿入できます。

## テーブル レベルでスケジューリングを一時停止する {#pause-scheduling-on-the-table-level}

v6.2.0 以降、 TiDB Lightning はオンライン アプリケーションへのデータ インポートの影響を制限するメカニズムを実装しています。新しいメカニズムにより、 TiDB Lightning はグローバル スケジューリングを一時停止しませんが、ターゲット テーブル データを格納するリージョンのスケジューリングのみを一時停止します。これにより、インポートによるオンライン アプリケーションへの影響が大幅に軽減されます。

<Note>
TiDB Lightning は、既にデータが含まれているテーブルへのデータのインポートをサポートしていません。
</Note>

TiDB クラスターは v6.1.0 以降のバージョンである必要があります。以前のバージョンでは、 TiDB Lightning は古い動作を維持しており、スケジューリングがグローバルに一時停止し、インポート中にオンライン アプリケーションに深刻な影響を与えます。

デフォルトでは、 TiDB Lightning は可能な限り最小の範囲でクラスターのスケジューリングを一時停止します。ただし、既定の構成では、クラスターのパフォーマンスは依然として高速インポートの影響を受ける可能性があります。これを回避するには、次のオプションを構成して、クラスターのパフォーマンスに影響を与える可能性のあるインポート速度やその他の要因を制御できます。

```toml
[tikv-importer]
# Limits the bandwidth in which TiDB Lightning writes data into each TiKV node in the physical import mode.
store-write-bwlimit = "128MiB"

[tidb]
# Use smaller concurrency to reduce the impact of Checksum and Analyze on the transaction latency.
distsql-scan-concurrency = 3

[cron]
# Prevent TiKV from switching to import mode.
switch-mode = '0'
```

TPCC を使用してオンライン アプリケーションをシミュレートし、 TiDB Lightningを使用して TiDB クラスターにデータをインポートすることにより、TPCC の結果に対するデータ インポートの影響を測定できます。テスト結果は次のとおりです。

| 同時実行 | TPM     | P99     | P90     | 平均      |
| ---- | ------- | ------- | ------- | ------- |
| 1    | 20%~30% | 60%~80% | 30%~50% | 30%~40% |
| 8    | 15%~25% | 70%~80% | 35%~45% | 20%~35% |
| 16   | 20%~25% | 55%~85% | 35%~40% | 20%~30% |
| 64   | 大きな影響なし |         |         |         |
| 256  | 大きな影響なし |         |         |         |

前の表のパーセンテージは、データ インポートが TPCC の結果に与える影響を示しています。

-   TPM 列の数値は、TPM の減少率を示します。
-   P99、P90、および AVG 列の場合、数値はレイテンシーの増加のパーセンテージを示します。

テスト結果は、同時実行数が小さいほど、TPCC の結果に対するデータ インポートの影響が大きくなることを示しています。同時実行数が 64 以上の場合、TPCC の結果に対するデータ インポートの影響は無視できます。

したがって、TiDB クラスターにレイテンシーの影響を受けやすいアプリケーションがあり、同時実行性が低い場合は、 TiDB Lightningを使用してデータをクラスターにインポートし**ないこと**を強くお勧めします。これは、オンライン アプリケーションに重大な影響を与えます。

## 性能調整 {#performance-tuning}

**物理インポート モードのインポート パフォーマンスを向上させる最も直接的で効果的な方法は、次のとおりです。**

-   **Lightning がデプロイされているノードのハードウェア、特に CPU と`sorted-key-dir`のstorageデバイスをアップグレードします。**
-   **<a href="/tidb-lightning/tidb-lightning-distributed-import.md">並行インポート</a>機能を使用して、水平スケーリングを実現します。**

TiDB Lightning は、物理インポート モードでのインポート パフォーマンスに影響を与える、いくつかの同時実行関連の構成を提供します。ただし、長年の経験から、次の 4 つの構成項目はデフォルト値のままにしておくことをお勧めします。 4 つの構成項目を調整しても、パフォーマンスが大幅に向上するわけではありません。

```
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
```

インポート中、各テーブルは、インデックスを格納する 1 つの &quot;インデックス エンジン&quot; と、行データを格納する複数の &quot;データ エンジン&quot; に分割されます。

`index-concurrency`インデックス エンジンの最大同時実行数を制御します。 `index-concurrency`を調整するときは、CPU が完全に使用されるように`index-concurrency * the number of source files of each table > region-concurrency`を確認してください。比率は通常 1.5 ～ 2 です`index-concurrency`を高く設定しすぎたり、2 より低く設定したりしないでください (デフォルト)。 `index-concurrency`が高すぎると、構築されるパイプラインが多すぎて、インデックス エンジンのインポート ステージが積み重なってしまいます。

`table-concurrency`についても同様です。 CPU が完全に使用されていることを確認するために`table-concurrency * the number of source files of each table > region-concurrency`を確認してください。推奨値は約`region-concurrency * 4 / the number of source files of each table`で、4 以上です。

テーブルが大きい場合、Lightning はテーブルを 100 GiB の複数のバッチに分割します。同時実行性は`table-concurrency`によって制御されます。

`index-concurrency`と`table-concurrency`はインポート速度にほとんど影響しません。デフォルト値のままにしておくことができます。

`io-concurrency`ファイル読み取りの並行性を制御します。デフォルト値は 5 です。常に、5 つのハンドルのみが読み取り操作を実行しています。通常、ファイルの読み取り速度はボトルネックにはならないため、この構成はデフォルト値のままにしておくことができます。

ファイルデータが読み取られた後、Lightning はデータのエンコードやローカルでの並べ替えなどの後処理を行う必要があります。これらの操作の並行性は`region-concurrency`によって制御されます。デフォルト値は CPU コアの数です。この構成はデフォルト値のままにしておくことができます。他のコンポーネントとは別のサーバーに Lightning をデプロイすることをお勧めします。 Lightning を他のコンポーネントと一緒にデプロイする必要がある場合は、負荷に応じて`region-concurrency`の値を下げる必要があります。

TiKV の[`num-threads`](/tikv-configuration-file.md#num-threads)構成もパフォーマンスに影響を与える可能性があります。新しいクラスターの場合、CPU コアの数に`num-threads`を設定することをお勧めします。

## ディスク クォータの構成<span class="version-mark">v6.2.0 の新機能</span> {#configure-disk-quota-span-class-version-mark-new-in-v6-2-0-span}

物理インポート モードでデータをインポートすると、 TiDB Lightning はローカル ディスク上に多数の一時ファイルを作成し、元のデータをエンコード、並べ替え、および分割します。ローカル ディスク容量が不足している場合、 TiDB Lightning はエラーを報告し、書き込みの失敗により終了します。

この状況を回避するために、 TiDB Lightningのディスク クォータを構成できます。一時ファイルのサイズがディスク クォータを超えると、 TiDB Lightning はソース データの読み取りと一時ファイルの書き込みのプロセスを一時停止します。 TiDB Lightning は、並べ替えられたキーと値のペアを優先して TiKV に書き込みます。ローカルの一時ファイルを削除した後、 TiDB Lightning はインポート プロセスを続行します。

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

`disk-quota` TiDB Lightningが使用するstorage容量を制限します。デフォルト値は MaxInt64 で、9223372036854775807 バイトです。この値は、インポートに必要なディスク容量よりもはるかに大きいため、デフォルト値のままにしておくことは、ディスク クォータを設定しないことと同じです。

`check-disk-quota`は、ディスク クォータをチェックする間隔です。デフォルト値は 60 秒です。 TiDB Lightning がディスク クォータをチェックすると、関連データの排他ロックが取得され、すべてのインポート スレッドがブロックされます。したがって、 TiDB Lightning がすべての書き込みの前にディスク クォータをチェックすると、書き込み効率が大幅に低下します (シングル スレッドの書き込みと同じくらい遅くなります)。効率的な書き込みを実現するために、すべての書き込みの前にディスク クォータがチェックされるわけではありません。代わりに、 TiDB Lightning はすべてのインポート スレッドを一時停止し、 `check-disk-quota`間隔ごとにディスク クォータをチェックします。つまり、値`check-disk-quota`を大きな値に設定すると、 TiDB Lightningが使用するディスク容量が設定したディスク クォータを超えて、ディスク クォータが無効になる可能性があります。したがって、 `check-disk-quota`の値を小さい値に設定することをお勧めします。この項目の具体的な値は、 TiDB Lightningが実行されている環境によって決まります。さまざまな環境で、 TiDB Lightning はさまざまな速度で一時ファイルを書き込みます。理論的には、速度が速いほど、 `check-disk-quota`の値を小さくする必要があります。
