---
title: Use Physical Import Mode
summary: Learn how to use the physical import mode in TiDB Lightning.
---

# 物理インポート モードを使用する {#use-physical-import-mode}

このドキュメントでは、設定ファイルの記述やパフォーマンスのチューニングなど、 TiDB Lightningでの物理インポート モードの使用方法を紹介します。

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
# tidb-lightning import the TiDB library, and generates some logs.
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

### 競合の検出 {#conflict-detection}

競合するデータとは、PK/UK 列のデータが同じである 2 つ以上のレコードを指します。データ ソースに競合するデータが含まれている場合、テーブル内の実際の行数は、一意のインデックスを使用したクエリによって返される合計行数とは異なります。

TiDB Lightningは、競合するデータを検出するための 3 つの戦略を提供します。

-   `record` : 競合するレコードのみをターゲット TiDB の`lightning_task_info.conflict_error_v1`テーブルに記録します。ターゲット TiKV の必要なバージョンは v5.2.0 以降のバージョンであることに注意してください。それ以外の場合は、&#39;none&#39; にフォールバックします。
-   `remove` (推奨): `record`戦略のように、競合するすべてのレコードを記録します。ただし、競合するすべてのレコードをターゲット テーブルから削除して、ターゲット TiDB で一貫した状態を確保します。
-   `none` : 重複レコードを検出しません。 `none`は 3 つの戦略で最高のパフォーマンスを発揮しますが、ターゲット TiDB でデータの一貫性が失われる可能性があります。

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

## 性能調整 {#performance-tuning}

**物理インポート モードのインポート パフォーマンスを向上させる最も直接的で効果的な方法は、次のとおりです。**

-   **Lightning がデプロイされているノードのハードウェア、特に CPU と`sorted-key-dir`のストレージ デバイスをアップグレードします。**
-   **<a href="/tidb-lightning/tidb-lightning-distributed-import.md">並行インポート</a>機能を使用して、水平スケーリングを実現します。**

Lightning には、物理インポートモードのインポートパフォーマンスに影響を与える同時実行関連の設定がいくつか用意されています。ただし、長年の経験から、次の 4 つの構成項目はデフォルト値のままにしておくことをお勧めします。 4 つの構成項目を調整しても、パフォーマンスが大幅に向上するわけではありません。

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

`index-concurrency`は、インデックス エンジンの最大同時実行数を制御します。 `index-concurrency`を調整するときは、CPU が完全に使用されるように`index-concurrency * the number of source files of each table > region-concurrency`を確認してください。比率は通常 1.5 ～ 2 です`index-concurrency`を高く設定しすぎたり、2 より低く設定したりしないでください (デフォルト)。 `index-concurrency`が高すぎると、構築されるパイプラインが多すぎて、インデックス エンジンのインポート ステージが積み重なってしまいます。

`table-concurrency`についても同様です。 CPU が完全に使用されていることを確認するために`table-concurrency * the number of source files of each table > region-concurrency`を確認してください。推奨値は約`region-concurrency * 4 / the number of source files of each table`で、4 以上です。

テーブルが大きい場合、Lightning はテーブルを 100 GiB の複数のバッチに分割します。同時実行性は`table-concurrency`によって制御されます。

`index-concurrency`と`table-concurrency`はインポート速度にほとんど影響しません。デフォルト値のままにしておくことができます。

`io-concurrency`は、ファイル読み取りの並行性を制御します。デフォルト値は 5 です。常に、5 つのハンドルのみが読み取り操作を実行しています。通常、ファイルの読み取り速度はボトルネックにはならないため、この構成はデフォルト値のままにしておくことができます。

ファイルデータが読み取られた後、Lightning はデータのエンコードやローカルでの並べ替えなどの後処理を行う必要があります。これらの操作の並行性は`region-concurrency`によって制御されます。デフォルト値は CPU コアの数です。この構成はデフォルト値のままにしておくことができます。他のコンポーネントとは別のサーバーに Lightning をデプロイすることをお勧めします。 Lightning を他のコンポーネントと一緒にデプロイする必要がある場合は、負荷に応じて`region-concurrency`の値を下げる必要があります。

TiKV の[`num-threads`](/tikv-configuration-file.md#num-threads)構成もパフォーマンスに影響を与える可能性があります。新しいクラスターの場合、CPU コアの数に`num-threads`を設定することをお勧めします。
