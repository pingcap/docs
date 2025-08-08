---
title: TiKV MVCC In-Memory Engine
summary: インメモリ エンジンの適用可能なシナリオと動作原理、およびインメモリ エンジンを使用して MVCC バージョンのクエリを高速化する方法について学習します。
---

# TiKV MVCC インメモリエンジン {#tikv-mvcc-in-memory-engine}

TiKV MVCC インメモリ エンジン (IME) は主に、多数の MVCC 履歴バージョン (つまり[スキャンされたバージョンの合計数 ( `total_keys` ) が、処理されたバージョン数 ( `processed_keys` ) よりもはるかに大きい](/analyze-slow-queries.md#obsolete-mvcc-versions-and-excessive-keys) ) をスキャンする必要があるクエリを高速化するために使用されます。

TiKV MVCC インメモリ エンジンは、次のシナリオに適しています。

-   頻繁に更新または削除されるレコードを照会する必要があるアプリケーション。
-   履歴バージョンを TiDB に長期間 (たとえば、24 時間) 保持するために[`tidb_gc_life_time`](/garbage-collection-configuration.md#garbage-collection-configuration)調整する必要のあるアプリケーション。

## 実施原則 {#implementation-principles}

TiKV MVCCインメモリエンジンは、書き込まれた最新のMVCCバージョンをメモリにキャッシュし、TiDBに依存しないMVCC GCメカニズムを実装します。これにより、メモリ内のMVCCバージョンに対してGCを迅速に実行できるため、クエリ中にスキャンされるバージョン数が削減され、リクエストのレイテンシーとCPUオーバーヘッドが低減されます。

次の図は、TiKV が MVCC バージョンを整理する方法を示しています。

![IME caches recent versions to reduce CPU overhead](/media/tikv-ime-data-organization.png)

上の図は、それぞれ9つのMVCCバージョンを持つ2行のレコードを示しています。インメモリエンジンを有効にした場合と無効にした場合の動作の比較は次のとおりです。

-   左側 (メモリ内エンジンが無効): テーブル レコードは主キーの昇順で RocksDB に保存され、同じ行のすべての MVCC バージョンが互いに隣接しています。
-   右側 (インメモリ エンジンが有効): RocksDB 内のデータは左側のものと同じですが、インメモリ エンジンは 2 つの行ごとに最新の 2 つの MVCC バージョンをキャッシュします。
-   TiKV が範囲`[k1, k2]`および開始タイムスタンプ`8`のスキャン要求を処理する場合:
    -   インメモリ エンジンがない場合 (左)、11 個の MVCC バージョンを処理する必要があります。
    -   インメモリ エンジン (右) では、4 つの MVCC バージョンのみが処理されるため、リクエストのレイテンシーと CPU 消費が削減されます。
-   TiKV が範囲`[k1, k2]`および開始タイムスタンプ`7`のスキャン要求を処理する場合:
    -   必要な履歴バージョンがメモリ内エンジンにないため (右)、キャッシュが無効になり、TiKV は RocksDB からデータを読み取るようになります。

## 使用法 {#usage}

TiKV MVCCインメモリエンジン（IME）を有効にするには、 [TiKV構成](/tikv-configuration-file.md#in-memory-engine-new-in-v850)調整してTiKVを再起動する必要があります。設定の詳細は次のとおりです。

```toml
[in-memory-engine]
# This parameter is the switch for the in-memory engine feature, which is disabled by default. You can set it to true to enable it.
# It is recommended to configure at least 8 GiB of memory for the TiKV node, with 32 GiB or more for optimal performance.
# If the available memory for the TiKV node is insufficient, the in-memory engine will not be enabled even if this configuration item is set to true. In such cases, check the TiKV log file for messages containing "in-memory engine is disabled because" to learn why the in-memory engine is not enabled.
enable = false

# This parameter controls the memory size available to the in-memory engine.
# The default value is 10% of the system memory, and the maximum value is 5 GiB.
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
> -   インメモリエンジンはデフォルトで無効になっています。有効にした後は、TiKVを再起動する必要があります。
> -   `enable`を除き、他のすべての構成項目は動的に調整できます。

### 自動読み込み {#automatic-loading}

インメモリエンジンを有効にすると、TiKVはリージョンの読み取りトラフィックとMVCC増幅に基づいて、ロードするリージョンを自動的に選択します。具体的なプロセスは以下のとおりです。

1.  リージョンは、最近の`next` (RocksDB Iterator next API) と`prev` (RocksDB Iterator prev API) の呼び出し回数に基づいてソートされます。
2.  領域は`mvcc-amplification-threshold`設定パラメータを使用してフィルタリングされます。デフォルト値は`10`です。MVCC増幅はリード増幅を測定し、( `next` + `prev` ) / `processed_keys`として計算されます。
3.  重大な MVCC 増幅を持つ上位 N 個の領域がロードされます。N はメモリ推定に基づいて決定されます。

インメモリエンジンは定期的にリージョンの削除も行います。そのプロセスは以下のとおりです。

1.  インメモリ エンジンは、読み取りトラフィックが少ない、または MVCC 増幅が低い領域を排除します。
2.  メモリ使用量が`capacity`の 90% に達し、新しいリージョンをロードする必要がある場合、インメモリ エンジンは読み取りトラフィックに基づいてリージョンを選択し、排除します。

## 互換性 {#compatibility}

-   [BR](/br/br-use-overview.md) : インメモリエンジンはBRと併用できます。ただし、 BRリストア中は、リストアプロセスに関係するリージョンがBRメモリエンジンから削除されます。BR リストアが完了した後、対応するリージョンがホットスポットとして残っている場合は、インメモリエンジンによって自動的にロードされます。
-   [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) : インメモリエンジンはTiDB Lightningと併用できます。ただし、 TiDB Lightning が物理インポートモードで動作する場合、復元プロセスに関係するリージョンはインメモリエンジンから削除されます。物理インポートが完了すると、対応するリージョンがホットスポットとして残っている場合は、インメモリエンジンによって自動的にロードされます。
-   [Follower Read](/develop/dev-guide-use-follower-read.md)と[ステイル読み取り](/develop/dev-guide-use-stale-read.md) : インメモリエンジンは、これら 2 つの機能と併用できます。ただし、インメモリエンジンはLeader上のコプロセッサ要求のみを高速化でき、Follower Readとステイル読み取り操作を高速化することはできません。
-   [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) : インメモリエンジンはフラッシュバックと併用できます。ただし、フラッシュバックはインメモリエンジンのキャッシュを無効化します。フラッシュバック処理が完了すると、インメモリエンジンはホットスポット領域を自動的にロードします。

## FAQ {#faq}

### インメモリ エンジンは書き込みレイテンシーを削減し、書き込みスループットを向上させることができますか? {#can-the-in-memory-engine-reduce-write-latency-and-increase-write-throughput}

いいえ。インメモリ エンジンは、多数の MVCC バージョンをスキャンする読み取り要求のみを高速化できます。

### インメモリ エンジンによってシナリオを改善できるかどうかを判断するにはどうすればよいですか? {#how-to-determine-if-the-in-memory-engine-can-improve-my-scenario}

次の SQL ステートメントを実行して、 `Total_keys`が`Process_keys`より大幅に大きい遅いクエリがあるかどうかを確認できます。

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

次の結果は、 `db1.tbl1`テーブルに深刻な MVCC 増幅を伴うクエリが存在することを示しています。TiKV は 1358517 個の MVCC バージョンを処理し、2 つのバージョンのみを返します。

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

### TiKV MVCC インメモリ エンジンが有効になっているかどうかを確認するにはどうすればよいですか? {#how-can-i-check-whether-the-tikv-mvcc-in-memory-engine-is-enabled}

[`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md)ステートメントを使用して TiKV の設定を確認できます。3 の値が`in-memory-engine.enable` `true`場合、TiKV MVCC インメモリエンジンが有効になっていることを意味します。

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

### TiKV MVCC インメモリ エンジンを監視するにはどうすればよいですか? {#how-can-i-monitor-the-tikv-mvcc-in-memory-engine}

Grafana の**TiKV-Details**ダッシュボードの[**インメモリエンジン**](/grafana-tikv-dashboard.md#in-memory-engine)セクションを確認できます。
