---
title: TiKV MVCC In-Memory Engine
summary: インメモリエンジンの適用シナリオと動作原理、およびMVCCバージョンのクエリを高速化するためにインメモリエンジンを使用する方法を学びます。
---

# TiKV MVCC インメモリエンジン {#tikv-mvcc-in-memory-engine}

TiKV MVCC インメモリ エンジン (IME) は、主に多数の MVCC 履歴バージョンをスキャンする必要があるクエリを高速化するために使用されます。つまり、 [スキャンされたバージョンの総数（ `total_keys` ）は、処理されたバージョン数（ `processed_keys` ）よりもはるかに多い。](/analyze-slow-queries.md#obsolete-mvcc-versions-and-excessive-keys) 。

TiKV MVCCインメモリエンジンは、以下のシナリオに適しています。

-   頻繁に更新または削除されるレコードを照会する必要があるアプリケーション。
-   TiDBに履歴バージョンをより長い期間（例えば24時間）保持するために、 [`tidb_gc_life_time`](/garbage-collection-configuration.md#garbage-collection-configuration)調整する必要があるアプリケーション。

## 実施原則 {#implementation-principles}

TiKV MVCCインメモリエンジンは、最新の書き込み済みMVCCバージョンをメモリにキャッシュし、TiDBとは独立したMVCC GCメカニズムを実装しています。これにより、メモリ内のMVCCバージョンに対して高速なGCを実行でき、クエリ中にスキャンされるバージョンの数を削減することで、リクエストのレイテンシーを低減し、CPUオーバーヘッドを削減します。

以下の図は、TiKVがMVCCバージョンをどのように整理しているかを示しています。

![IME caches recent versions to reduce CPU overhead](/media/tikv-ime-data-organization.png)

前述の図は、それぞれ9つのMVCCバージョンを含む2行のレコードを示しています。インメモリエンジンを有効にした場合と無効にした場合の動作比較は以下のとおりです。

-   左側（インメモリエンジンが無効になっている場合）：テーブルレコードは、主キーに基づいて昇順でRocksDBに格納され、同じ行のすべてのMVCCバージョンが隣接して配置されます。
-   右側（インメモリエンジン有効）：RocksDB内のデータは左側のデータと同じですが、インメモリエンジンは2つの行それぞれについて最新の2つのMVCCバージョンをキャッシュします。
-   TiKVが範囲`[k1, k2]` 、開始タイムスタンプ`8`のスキャン要求を処理する場合：
    -   インメモリエンジン（左図）がない場合、11個のMVCCバージョンを処理する必要がある。
    -   インメモリエンジン（右図）では、処理するMVCCバージョンは4つだけなので、リクエストのレイテンシーとCPU消費量が削減されます。
-   TiKVが範囲`[k1, k2]` 、開始タイムスタンプ`7`のスキャン要求を処理する場合：
    -   メモリ内エンジン（右図）に必要な履歴バージョンが欠落しているため、キャッシュが無効になり、TiKVはRocksDBからデータを読み込むようにフォールバックします。

## 使用法 {#usage}

TiKV MVCC インメモリエンジン (IME) を有効にするには、 [TiKV構成](/tikv-configuration-file.md#in-memory-engine-new-in-v850)を調整して TiKV を再起動する必要があります。設定の詳細は以下のとおりです。

```toml
[in-memory-engine]
# This parameter is the switch for the in-memory engine feature, which is disabled by default. You can set it to true to enable it.
# It is recommended to configure at least 8 GiB of memory for the TiKV node, with 32 GiB or more for optimal performance.
# If the available memory for the TiKV node is insufficient, the in-memory engine will not be enabled even if this configuration item is set to true. In such cases, check the TiKV log file for messages containing "in-memory engine is disabled because" to learn why the in-memory engine is not enabled.
enable = false

# This parameter controls the memory size available to the in-memory engine.
# The default value is `min(the system memory * 10%, 5 GiB)`. You can manually adjust the configuration to use more memory.
# You can manually adjust this configuration to allocate more memory.
# Note: When the in-memory engine is enabled, block-cache.capacity automatically decreases by 10%.
capacity = "5GiB"

# This parameter controls the time interval for the in-memory engine to GC the cached MVCC versions.
# The default value is 3 minutes, representing that GC is performed every 3 minutes on the cached MVCC versions.
# Decreasing the value of this parameter can increase the GC frequency, reduce the number of MVCC versions, but will increase CPU consumption for GC and increase the probability of in-memory engine cache miss.
gc-run-interval = "3m"

# This parameter controls the threshold for the in-memory engine to select and load Regions based on MVCC read amplification.
# The default value is 10, indicating that if reading a single row in a Region requires processing more than 10 MVCC versions, this Region might be loaded into the in-memory engine.
mvcc-amplification-threshold = 10
```

> **注記：**
>
> -   インメモリエンジンはデフォルトでは無効になっています。有効にした後は、TiKVを再起動する必要があります。
> -   `enable`を除き、その他の設定項目はすべて動的に調整可能です。

### 自動読み込み {#automatic-loading}

インメモリエンジンを有効にすると、TiKVはリージョンの読み取りトラフィックとMVCC増幅に基づいて、ロードするリージョンを自動的に選択します。具体的な手順は次のとおりです。

1.  リージョンは、最近の`next` （RocksDB Iterator next API）および`prev` （RocksDB Iterator prev API）の呼び出し回数に基づいてソートされます。
2.  領域は、 `mvcc-amplification-threshold`構成パラメータを使用してフィルタリングされます。デフォルト値は`10`です。MVCC 増幅は、( `next` + `prev` ) / `processed_keys`として計算されるリード増幅を測定します。
3.  MVCC増幅が著しい上位N個の領域がロードされる。ここでNはメモリ推定に基づいて決定される。

インメモリエンジンは定期的にリージョンを削除します。そのプロセスは以下のとおりです。

1.  インメモリエンジンは、読み取りトラフィックが少ない、またはMVCC増幅率が低い領域を削除します。
2.  メモリ使用率が`capacity`の90%に達し、新しいリージョンをロードする必要がある場合、インメモリエンジンは読み取りトラフィックに基づいてリージョンを選択および削除します。

## 互換性 {#compatibility}

-   [BR](/br/br-use-overview.md) ：インメモリエンジンはBRと併用できます。ただし、 BRリストア中は、リストア処理に関係するリージョンはインメモリエンジンから削除されます。BRBRが完了した後、対応するリージョンがホットスポットとして残っている場合は、インメモリエンジンによって自動的にロードされます。
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) ：インメモリエンジンはTiDB Lightningと併用できます。ただし、 TiDB Lightningが物理インポートモードで動作する場合、復元プロセスに関係するリージョンはインメモリエンジンから削除されます。物理インポートが完了すると、対応するリージョンがホットスポットとして残っている場合、それらはインメモリエンジンによって自動的にロードされます。
-   [Follower Read](/develop/dev-guide-use-follower-read.md)と[ステイル読み取り](/develop/dev-guide-use-stale-read.md) ：インメモリエンジンは、これら2つの機能と併用できます。ただし、インメモリエンジンはLeader上のコプロセッサ要求のみを高速化でき、Follower Readとステイル読み取り操作を高速化することはできません。
-   [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) ：インメモリエンジンはFlashbackと併用できます。ただし、Flashbackはインメモリエンジンのキャッシュを無効化します。Flashback処理が完了すると、インメモリエンジンはホットスポット領域を自動的にロードします。

## FAQ {#faq}

### インメモリエンジンは書き込みレイテンシーを低減し、書き込みスループットを向上させることができるか？ {#can-the-in-memory-engine-reduce-write-latency-and-increase-write-throughput}

いいえ。インメモリエンジンは、多数のMVCCバージョンをスキャンする読み取り要求のみを高速化できます。

### インメモリエンジンが私のシナリオを改善できるかどうかを判断するにはどうすればよいでしょうか？ {#how-to-determine-if-the-in-memory-engine-can-improve-my-scenario}

`Total_keys` `Process_keys`よりはるかに大きい低速クエリが存在するかどうかを確認するには、次のSQL文を実行してください。

```sql
SELECT
    Time,
    DB,
    Index_names,
    Process_keys,
    Total_keys,
    CONCAT(
        LEFT(REGEXP_REPLACE(Query, '\\s+', ' '), 20),
        '...',
        RIGHT(REGEXP_REPLACE(Query, '\\s+', ' '), 10)
    ) as Query,
    Query_time,
    Cop_time,
    Process_time
FROM
    INFORMATION_SCHEMA.SLOW_QUERY
WHERE
    Is_internal = 0
    AND Cop_time > 1
    AND Process_keys > 0
    AND Total_keys / Process_keys >= 10
    AND Time >= NOW() - INTERVAL 10 MINUTE
ORDER BY Total_keys DESC
LIMIT 5;
```

例：

以下の結果は、 `db1.tbl1`テーブルに深刻な MVCC 増幅を伴うクエリが存在することを示しています。TiKV は 1358517 個の MVCC バージョンを処理し、2 つのバージョンのみを返します。

    +----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
    | Time                       | DB  | Index_names       | Process_keys | Total_keys | Query                             | Query_time         | Cop_time           | Process_time       |
    +----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
    | 2024-11-18 11:56:10.303228 | db1 | [tbl1:some_index] |            2 |    1358517 |  SELECT * FROM tbl1 ... LIMIT 1 ; | 1.2581352350000001 |         1.25651062 |        1.251837479 |
    | 2024-11-18 11:56:11.556257 | db1 | [tbl1:some_index] |            2 |    1358231 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.252694002 |        1.251129038 |        1.240532546 |
    | 2024-11-18 12:00:10.553331 | db1 | [tbl1:some_index] |            2 |    1342914 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.473941872 | 1.4720495900000001 | 1.3666103170000001 |
    | 2024-11-18 12:01:52.122548 | db1 | [tbl1:some_index] |            2 |    1128064 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.058942591 |        1.056853228 |        1.023483875 |
    | 2024-11-18 12:01:52.107951 | db1 | [tbl1:some_index] |            2 |    1128064 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.044847031 |        1.042546122 |        0.934768555 |
    +----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
    5 rows in set (1.26 sec)

### TiKV MVCCのインメモリエンジンが有効になっているかどうかを確認するにはどうすればよいですか？ {#how-can-i-check-whether-the-tikv-mvcc-in-memory-engine-is-enabled}

TiKVの設定は、 [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)ステートメントを使用して確認できます。3の値が`in-memory-engine.enable` `true`場合、TiKV MVCCインメモリエンジンが有効になっていることを意味します。

```sql
SHOW CONFIG WHERE Type='tikv' AND Name LIKE 'in-memory-engine\.%';
```

    +------+-----------------+-----------------------------------------------+---------+
    | Type | Instance        | Name                                          | Value   |
    +------+-----------------+-----------------------------------------------+---------+
    | tikv | 127.0.0.1:20160 | in-memory-engine.capacity                     | 5GiB    |
    | tikv | 127.0.0.1:20160 | in-memory-engine.cross-check-interval         | 0s      |
    | tikv | 127.0.0.1:20160 | in-memory-engine.enable                       | true    |
    | tikv | 127.0.0.1:20160 | in-memory-engine.evict-threshold              | 4920MiB |
    | tikv | 127.0.0.1:20160 | in-memory-engine.gc-run-interval              | 3m      |
    | tikv | 127.0.0.1:20160 | in-memory-engine.load-evict-interval          | 5m      |
    | tikv | 127.0.0.1:20160 | in-memory-engine.mvcc-amplification-threshold | 10      |
    | tikv | 127.0.0.1:20160 | in-memory-engine.stop-load-threshold          | 4208MiB |
    +------+-----------------+-----------------------------------------------+---------+
    8 rows in set (0.00 sec)

### TiKV MVCCのインメモリエンジンを監視するにはどうすればよいですか？ {#how-can-i-monitor-the-tikv-mvcc-in-memory-engine}

Grafanaの**TiKV-Details**ダッシュボードのセクション[**インメモリエンジン**](/grafana-tikv-dashboard.md#in-memory-engine)を確認してください。
