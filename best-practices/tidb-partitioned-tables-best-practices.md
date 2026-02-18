---
title: Best Practices for Using TiDB Partitioned Tables
summary: TiDB パーティション テーブルを使用してパフォーマンスを向上させ、データ管理を簡素化し、大規模なデータセットを効率的に処理するためのベスト プラクティスを学習します。
aliases: ['/ja/tidb/stable/tidb-partitioned-tables-best-practices/','/ja/tidb/dev/tidb-partitioned-tables-best-practices/']
---

# TiDB パーティションテーブルの使用に関するベストプラクティス {#best-practices-for-using-tidb-partitioned-tables}

このガイドでは、TiDB でパーティション テーブルを使用してパフォーマンスを向上させ、データ管理を簡素化し、大規模なデータセットを効率的に処理する方法について説明します。

TiDBのパーティションテーブルは、大規模データセットの管理、クエリ効率の向上、一括データ削除の容易化、書き込みホットスポット問題の緩和など、多用途なアプローチを提供します。データを論理セグメントに分割することで、TiDBはパーティションプルーニングを活用し、クエリ実行時に不要なデータをスキップします。これにより、リソース消費が削減され、特に大規模データセットを扱うオンライン分析処理（OLAP）ワークロードにおいてパフォーマンスが向上します。

一般的なユースケースとしては、 [範囲分割](/partitioned-table.md#range-partitioning)とローカルインデックスを組み合わせて、 [`ALTER TABLE ... DROP PARTITION`](/sql-statements/sql-statement-alter-table.md)などの操作で履歴データを効率的にクリーンアップすることが挙げられます。この方法では、古いデータがほぼ瞬時に削除され、パーティションキーによるフィルタリング時に高いクエリ効率が維持されます。ただし、パーティション化されていないテーブルからパーティション化されたテーブルに移行した後、パーティションキーフィルターがないクエリなど、パーティションプルーニングのメリットを享受できないクエリでは、パフォーマンスが低下する可能性があります。このような場合、 [グローバルインデックス](/partitioned-table.md#global-indexes)使用してすべてのパーティションに統一されたインデックス構造を提供することで、パフォーマンスへの影響を軽減できます。

もう1つのシナリオは、ハッシュまたはキーパーティショニングを使用して書き込みホットスポットの問題に対処することです。特に、 [`AUTO_INCREMENT`](/auto-increment.md) IDを使用するワークロードでは、シーケンシャルな挿入によって特定のTiKVリージョンに過負荷がかかる可能性があります。書き込みをパーティションに分散させることでワークロードのバランスを取ることができますが、レンジパーティショニングと同様に、パーティションプルーニング条件のないクエリではパフォーマンスが低下する可能性があります。このような状況では、グローバルインデックスが役立ちます。

パーティショニングには明らかなメリットがありますが、課題も生じます。例えば、新しく作成されたレンジパーティションは一時的なホットスポットを生み出す可能性があります。この問題に対処するため、TiDBは自動または手動によるリージョン事前分割をサポートし、データ分散のバランスを取り、ボトルネックを回避します。

このドキュメントでは、クエリの最適化、データのクリーンアップ、書き込みのスケーラビリティ、インデックス管理など、TiDBのパーティションテーブルを様々な観点から検証します。また、詳細なシナリオとベストプラクティスを通して、TiDBにおけるパーティションテーブル設計の最適化とパフォーマンスチューニングの実践的なガイダンスを提供します。

> **注記：**
>
> 基礎を学ぶには、パーティション プルーニング、インデックス タイプ、パーティション分割方法などの主要な概念について説明している[パーティショニング](/partitioned-table.md)参照してください。

## クエリ効率の向上 {#improve-query-efficiency}

このセクションでは、次の方法でクエリ効率を向上させる方法について説明します。

-   [パーティションプルーニング](#partition-pruning)
-   [セカンダリインデックスのクエリパフォーマンス](#query-performance-on-secondary-indexes-non-partitioned-tables-vs-local-indexes-vs-global-indexes)

### パーティションプルーニング {#partition-pruning}

パーティションプルーニングは、パーティションテーブルへのクエリ実行時にTiDBがスキャンするデータ量を削減する最適化手法です。TiDBはすべてのパーティションをスキャンするのではなく、クエリフィルタ条件を評価して一致するデータを含む可能性のあるパーティションを特定し、それらのパーティションのみをスキャンします。このアプローチにより、I/Oと計算のオーバーヘッドが削減され、クエリパフォーマンスが大幅に向上します。

パーティションプルーニングは、クエリ述語がパーティション戦略と一致している場合に最も効果的です。典型的な使用例は次のとおりです。

-   時系列データ クエリ: データが時間範囲 (たとえば、日次または月次) でパーティション分割されている場合、特定の時間ウィンドウに限定されたクエリでは、関連のないパーティションをすぐにスキップできます。
-   マルチテナントまたはカテゴリベースのデータセット: テナント ID またはカテゴリ別にパーティション分割することで、クエリをパーティションの小さなサブセットに集中させることができます。
-   ハイブリッドトランザクションおよび分析処理（HTAP）：特にレンジパーティショニングにおいて、TiDBはTiFlash上​​の分析ワークロードにパーティションプルーニングを適用できます。この最適化により、無関係なパーティションがスキップされ、大規模なデータセットにおけるテーブル全体のスキャンが回避されます。

その他の使用例については、 [パーティションプルーニング](/partition-pruning.md)参照してください。

### セカンダリ インデックスのクエリ パフォーマンス: 非パーティション テーブルとローカル インデックスとグローバル インデックスの比較 {#query-performance-on-secondary-indexes-non-partitioned-tables-vs-local-indexes-vs-global-indexes}

TiDBでは、パーティションテーブルはデフォルトでローカルインデックスを使用し、各パーティションが独自のインデックスセットを保持します。一方、グローバルインデックスは、テーブル全体を1つのインデックスでカバーし、すべてのパーティションにまたがる行を追跡します。

複数のパーティションのデータにアクセスするクエリでは、一般的にグローバルインデックスの方がパフォーマンスが向上します。これは、ローカルインデックスを使用するクエリでは、関連するパーティションごとに個別のインデックス参照が必要になるのに対し、グローバルインデックスを使用するクエリでは、テーブル全体に対して単一の参照を実行するためです。

#### テスト済みのテーブルタイプ {#tested-table-types}

このテストでは、次のテーブル構成間でのクエリ パフォーマンスを比較します。

-   パーティションテーブル
-   ローカルインデックスを持つパーティションテーブル
-   グローバルインデックスを持つパーティションテーブル

#### テストセットアップ {#test-setup}

テストでは次の構成を使用します。

-   パーティションテーブルには、 `date`列で定義された 365 個の範囲パーティションが含まれています。
-   ワークロードは、各インデックス キーが複数の行と一致する大量の OLTP クエリ パターンをシミュレートします。
-   このテストでは、さまざまなパーティション数も評価し、パーティションの粒度がクエリのレイテンシーとインデックスの効率にどのように影響するかを測定します。

#### スキーマ {#schema}

この例では次のスキーマが使用されています。

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (`date`)(
  PARTITION `fa_2024001` VALUES LESS THAN (2025001),
  PARTITION `fa_2024002` VALUES LESS THAN (2025002),
  PARTITION `fa_2024003` VALUES LESS THAN (2025003),
  ...
  PARTITION `fa_2024365` VALUES LESS THAN (2025365)
);
```

#### SQL {#sql}

次のSQL文は、パーティションキー（ `date` ）を含めずにセカンダリインデックス（ `sid` ）をフィルタリングします。

```sql
SELECT `fa`.*
FROM `fa`
WHERE `fa`.`sid` IN (
  1696271179344,
  1696317134004,
  1696181972136,
  ...
  1696159221765
);
```

このクエリ パターンが代表的なものである理由は次のとおりです。

-   パーティション キーのないセカンダリ インデックスをフィルターします。
-   プルーニングが不足しているため、各パーティションのローカル インデックス検索がトリガーされます。
-   パーティション化されたテーブルに対して、大幅に多くのテーブル検索タスクが生成されます。

#### テスト結果 {#test-results}

次の表は、365 個の範囲パーティションを持つテーブルから 400 行を返すクエリの結果を示しています。

| コンフィグレーション                | 平均クエリ時間 | タスクの収集（インデックススキャン） | 警官タスク（テーブル検索） | 警官の合計タスク |
| ------------------------- | ------- | ------------------ | ------------- | -------- |
| パーティションテーブル               | 12.6ミリ秒 | 72                 | 79            | 151      |
| ローカルインデックスを持つパーティションテーブル  | 108ミリ秒  | 600                | 375           | 975      |
| グローバルインデックスを持つパーティションテーブル | 14.8ミリ秒 | 69                 | 383           | 452      |

-   **非パーティションテーブル**：最小限のタスクで最高のパフォーマンスを提供します。ほとんどのOLTPワークロードに適しています。
-   **グローバル インデックスを持つパーティション テーブル**: インデックス スキャンの効率は向上しますが、多くの行が一致する場合、テーブル検索のコストは依然として高くなります。
-   **ローカル インデックスを持つパーティション テーブル**: クエリ条件にパーティション キーが含まれていない場合、ローカル インデックス クエリはすべてのパーティションをスキャンします。

> **注記：**
>
> -   **平均クエリ時間**は`statement_summary`ビューから取得されます。
> -   **COP タスクの**メトリックは実行プランから派生します。

#### 実行計画の例 {#execution-plan-examples}

次の例は、各構成の実行プランを示しています。

<details><summary><b>パーティションテーブル</b></summary>

    | id                        | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory   | disk |
    |---------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|----------|------|
    | IndexLookUp_7             | 398.73  | 787052.13 | 400     | root      |                                      | time:11.5ms, loops:2, index_task:{total_time:3.34ms, fetch_handle:3.34ms, build:600ns, wait:2.86µs}, table_task:{total_time:7.55ms, num:1, concurrency:5}, next:{wait_index:3.49ms, wait_table_lookup_build:492.5µs, wait_table_lookup_resp:7.05ms} |  | 706.7 KB | N/A  |
    | IndexRangeScan_5(Build)   | 398.73  | 90633.86  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:3.16ms, loops:3, cop_task:{num:72, max:780.4µs, min:394.2µs, avg:566.7µs, p95:748µs, max_proc_keys:20, p95_proc_keys:10, tot_proc:3.66ms, tot_wait:18.6ms, copr_cache_hit_ratio:0.00, build_task_duration:94µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:72, total_time:40.1ms}}, tikv_task:{proc max:1ms, min:0s, avg:27.8µs, p80:0s, p95:0s, iters:72, tasks:72}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:480, get_snapshot_time:17.7ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:160}}}, time_detail:{total_process_time:3.66ms, total_wait_time:18.6ms, total_kv_read_wall_time:2ms, tikv_wall_time:27.4ms} | range:[1696125963161,1696125963161], …, [1696317134004,1696317134004], keep order:false | N/A | N/A |
    | TableRowIDScan_6(Probe)   | 398.73  | 166072.78 | 400     | cop[tikv] | table:fa                             | time:7.01ms, loops:2, cop_task:{num:79, max:4.98ms, min:0s, avg:514.9µs, p95:3.75ms, max_proc_keys:10, p95_proc_keys:5, tot_proc:15ms, tot_wait:21.4ms, copr_cache_hit_ratio:0.00, build_task_duration:341.2µs, max_distsql_concurrency:1, max_extra_concurrency:7, store_batch_num:62}, rpc_info:{Cop:{num_rpc:17, total_time:40.5ms}}, tikv_task:{proc max:0s, min:0s, avg:0s, p80:0s, p95:0s, iters:79, tasks:79}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:20.8ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1600}}}, time_detail:{total_process_time:15ms, total_wait_time:21.4ms, tikv_wall_time:10.9ms} | keep order:false | N/A | N/A |

</details>

<details><summary><b>グローバルインデックスを持つパーティションテーブル</b></summary>

    | id                     | estRows | estCost   | actRows | task      | access object                                   | execution info | operator info | memory   | disk |
    |------------------------|---------|-----------|---------|-----------|-------------------------------------------------|----------------|---------------|----------|------|
    | IndexLookUp_8          | 398.73  | 786959.21 | 400     | root      | partition:all                                   | time:12.8ms, loops:2, index_task:{total_time:2.71ms, fetch_handle:2.71ms, build:528ns, wait:3.23µs}, table_task:{total_time:9.03ms, num:1, concurrency:5}, next:{wait_index:3.27ms, wait_table_lookup_build:1.49ms, wait_table_lookup_resp:7.53ms} |  | 693.9 KB | N/A  |
    | IndexRangeScan_5(Build)| 398.73  | 102593.43 | 400     | cop[tikv] | table:fa, index:index_fa_on_sid_global(sid, id)| time:2.49ms, loops:3, cop_task:{num:69, max:997µs, min:213.8µs, avg:469.8µs, p95:986.6µs, max_proc_keys:15, p95_proc_keys:10, tot_proc:13.4ms, tot_wait:1.52ms, copr_cache_hit_ratio:0.00, build_task_duration:498.4µs, max_distsql_concurrency:15}, rpc_info:{Cop:{num_rpc:69, total_time:31.8ms}}, tikv_task:{proc max:1ms, min:0s, avg:101.4µs, p80:0s, p95:1ms, iters:69, tasks:69}, scan_detail:{total_process_keys:400, total_process_keys_size:31200, total_keys:480, get_snapshot_time:679.9µs, rocksdb:{key_skipped_count:400, block:{cache_hit_count:189, read_count:54, read_byte:347.7 KB, read_time:6.17ms}}}, time_detail:{total_process_time:13.4ms, total_wait_time:1.52ms, total_kv_read_wall_time:7ms, tikv_wall_time:19.3ms} | range:[1696125963161,1696125963161], …, keep order:false, stats:partial[...] | N/A | N/A |
    | TableRowIDScan_6(Probe)| 398.73  | 165221.64 | 400     | cop[tikv] | table:fa                                        | time:7.47ms, loops:2, cop_task:{num:383, max:4.07ms, min:0s, avg:488.5µs, p95:2.59ms, max_proc_keys:2, p95_proc_keys:1, tot_proc:203.3ms, tot_wait:429.5ms, copr_cache_hit_ratio:0.00, build_task_duration:1.3ms, max_distsql_concurrency:1, max_extra_concurrency:31, store_batch_num:305}, rpc_info:{Cop:{num_rpc:78, total_time:186.3ms}}, tikv_task:{proc max:3ms, min:0s, avg:517µs, p80:1ms, p95:1ms, iters:383, tasks:383}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:2.99ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:1601, read_count:799, read_byte:10.1 MB, read_time:131.6ms}}}, time_detail:{total_process_time:203.3ms, total_suspend_time:6.31ms, total_wait_time:429.5ms, total_kv_read_wall_time:198ms, tikv_wall_time:163ms} | keep order:false, stats:partial[...] | N/A | N/A |

</details>

<details><summary><b>ローカルインデックスを持つパーティションテーブル</b></summary>

    | id                     | estRows | estCost   | actRows | task      | access object                        | execution info | operator info | memory  | disk  |
    |------------------------|---------|-----------|---------|-----------|--------------------------------------|----------------|---------------|---------|-------|
    | IndexLookUp_7          | 398.73  | 784450.63 | 400     | root      | partition:all                        | time:290.8ms, loops:2, index_task:{total_time:103.6ms, fetch_handle:7.74ms, build:133.2µs, wait:95.7ms}, table_task:{total_time:551.1ms, num:217, concurrency:5}, next:{wait_index:179.6ms, wait_table_lookup_build:391µs, wait_table_lookup_resp:109.5ms} |  | 4.30 MB | N/A  |
    | IndexRangeScan_5(Build)| 398.73  | 90633.73  | 400     | cop[tikv] | table:fa, index:index_fa_on_sid(sid) | time:10.8ms, loops:800, cop_task:{num:600, max:65.6ms, min:1.02ms, avg:22.2ms, p95:45.1ms, max_proc_keys:5, p95_proc_keys:3, tot_proc:6.81s, tot_wait:4.77s, copr_cache_hit_ratio:0.00, build_task_duration:172.8ms, max_distsql_concurrency:3}, rpc_info:{Cop:{num_rpc:600, total_time:13.3s}}, tikv_task:{proc max:54ms, min:0s, avg:13.9ms, p80:20ms, p95:30ms, iters:600, tasks:600}, scan_detail:{total_process_keys:400, total_process_keys_size:22800, total_keys:29680, get_snapshot_time:2.47s, rocksdb:{key_skipped_count:400, block:{cache_hit_count:117580, read_count:29437, read_byte:104.9 MB, read_time:3.24s}}}, time_detail:{total_process_time:6.81s, total_suspend_time:1.51s, total_wait_time:4.77s, total_kv_read_wall_time:8.31s, tikv_wall_time:13.2s}} | range:[1696125963161,...,1696317134004], keep order:false, stats:partial[...] | N/A | N/A |
    | TableRowIDScan_6(Probe)| 398.73  | 165221.49 | 400     | cop[tikv] | table:fa                             | time:514ms, loops:434, cop_task:{num:375, max:31.6ms, min:0s, avg:1.33ms, p95:1.67ms, max_proc_keys:2, p95_proc_keys:2, tot_proc:220.7ms, tot_wait:242.2ms, copr_cache_hit_ratio:0.00, build_task_duration:27.8ms, max_distsql_concurrency:1, max_extra_concurrency:1, store_batch_num:69}, rpc_info:{Cop:{num_rpc:306, total_time:495.5ms}}, tikv_task:{proc max:6ms, min:0s, avg:597.3µs, p80:1ms, p95:1ms, iters:375, tasks:375}, scan_detail:{total_process_keys:400, total_process_keys_size:489856, total_keys:800, get_snapshot_time:158.3ms, rocksdb:{key_skipped_count:400, block:{cache_hit_count:3197, read_count:803, read_byte:10.2 MB, read_time:113.5ms}}}, time_detail:{total_process_time:220.7ms, total_suspend_time:5.39ms, total_wait_time:242.2ms, total_kv_read_wall_time:224ms, tikv_wall_time:430.5ms}} | keep order:false, stats:partial[...] | N/A | N/A |

</details>

#### パーティションテーブルにグローバルインデックスを作成する {#create-a-global-index-on-a-partitioned-table}

次のいずれかの方法を使用して、パーティションテーブルにグローバル インデックスを作成できます。

> **注記：**
>
> -   TiDB v8.5.3以前のバージョンでは、一意の列に対してのみグローバルインデックスを作成できました。v8.5.4以降では、一意でない列に対してもグローバルインデックスを作成できます。この制限は、将来のLTSバージョンで解除される予定です。
> -   一意でないグローバル インデックスの場合は、 `ADD UNIQUE INDEX`ではなく`ADD INDEX`使用します。
> -   `GLOBAL`キーワードを明示的に指定する必要があります。

##### オプション1: <code>ALTER TABLE</code>を使用する {#option-1-use-code-alter-table-code}

既存のパーティションテーブルにグローバルインデックスを追加するには、 `ALTER TABLE`使用します。

```sql
ALTER TABLE <table_name>
ADD UNIQUE INDEX <index_name> (col1, col2) GLOBAL;
```

##### オプション2: テーブル作成時にインデックスを定義する {#option-2-define-the-index-at-table-creation}

テーブルを作成するときにグローバル インデックスを作成するには、 `CREATE TABLE`ステートメントでグローバル インデックスをインラインで定義します。

```sql
CREATE TABLE t (
  id BIGINT NOT NULL,
  col1 VARCHAR(50),
  col2 VARCHAR(50),
  -- other columns...
  UNIQUE GLOBAL INDEX idx_col1_col2 (col1, col2)
)
PARTITION BY RANGE (id) (
  PARTITION p0 VALUES LESS THAN (10000),
  PARTITION p1 VALUES LESS THAN (20000),
  PARTITION pMax VALUES LESS THAN MAXVALUE
);
```

#### パフォーマンス概要 {#performance-summary}

TiDB パーティション テーブルのパフォーマンス オーバーヘッドは、パーティションの数とインデックスの種類によって異なります。

-   **パーティション数**：パーティション数が増えるとパフォーマンスが低下します。パーティション数が少ない場合は影響は無視できるかもしれませんが、ワークロードによって異なります。
-   **ローカルインデックス**：クエリに有効なパーティションプルーニング条件が含まれていない場合、パーティション数が直接的に[リモート プロシージャ コール (RPC)](https://docs.pingcap.com/tidb/stable/glossary/#remote-procedure-call-rpc)の数を決定します。つまり、パーティション数が増えると、通常、RPCが増加し、レイテンシーが増加します。
-   **グローバルインデックス**：パフォーマンスは、関連するパーティションの数と、テーブル参照を必要とする行数の両方に依存します。データが複数のリージョンに分散されている非常に大きなテーブルの場合、グローバルインデックスを介してデータにアクセスすると、パーティションテーブルと同等のパフォーマンスが得られます。これは、どちらのシナリオでも複数のリージョン間RPCが使用されるためです。

#### 推奨事項 {#recommendations}

TiDB でパーティション テーブルとインデックスを設計するときは、次のガイドラインに従います。

-   パーティションテーブルは必要な場合にのみ使用してください。ほとんどのOLTPワークロードでは、適切にインデックスが設定されたパーティションテーブルの方がパフォーマンスが向上し、管理が簡単になります。
-   すべてのクエリに、少数のパーティションに一致する有効なパーティション プルーニング条件が含まれている場合は、ローカル インデックスを使用します。
-   効果的なパーティション プルーニング条件がなく、多数のパーティションに一致する重要なクエリには、グローバル インデックスを使用します。
-   DDL 操作の効率 (高速`DROP PARTITION`など) が優先され、潜在的なパフォーマンスへの影響が許容できる場合にのみ、ローカル インデックスを使用します。

## 一括データ削除を容易にする {#facilitate-bulk-data-deletion}

TiDBでは、 [TTL (存続時間)](/time-to-live.md)使用するか、パーティションを手動で削除することで履歴データを削除できます。どちらの方法でもデータは削除されますが、パフォーマンス特性は大きく異なります。以下のテスト結果から、パーティションを削除する方が一般的に高速で消費リソースも少なく、大規模なデータセットや頻繁なデータパージにはより適した選択肢であることがわかります。

### TTLと<code>DROP PARTITION</code>の違い {#differences-between-ttl-and-code-drop-partition-code}

-   TTL: データの経過時間に基づいて自動的にデータを削除します。この方法は、時間の経過とともに行を段階的にスキャンして削除するため、処理速度が低下する可能性があります。
-   `DROP PARTITION` : 1回の操作でパーティション全体を削除します。この方法は、特に大規模なデータセットの場合、通常、はるかに高速です。

#### テストケース {#test-case}

このテストでは、TTL と`DROP PARTITION`のパフォーマンスを比較します。

-   TTL 構成: 10 分ごとに実行されます。
-   パーティション構成: 10 分ごとに 1 つのパーティションを削除します。
-   ワークロード: 50 および 100 の同時スレッドによるバックグラウンド書き込みワークロード。

テストでは、実行時間、システム リソースの使用量、および削除された行の合計数を測定します。

#### 調査結果 {#findings}

> **注記：**
>
> このセクションで説明するパフォーマンス上の利点は、グローバル インデックスのないパーティション テーブルにのみ適用されます。

TTL パフォーマンスに関する調査結果は次のとおりです。

-   スレッドが 50 個の場合、各 TTL ジョブには 8 ～ 10 分かかり、700 万～ 1,100 万行が削除されます。
-   100 スレッドの場合、TTL は最大 2,000 万行を処理できますが、実行時間は 15 ～ 30 分に増加し、変動も大きくなります。
-   負荷が高い場合、TTL ジョブは追加のスキャンと削除のオーバーヘッドにより全体的な QPS を低下させます。

`DROP PARTITION`パフォーマンスに関する調査結果は次のとおりです。

-   `ALTER TABLE ... DROP PARTITION`ステートメントは、パーティション全体をほぼ即座に削除します。
-   この操作はメタデータ レベルで実行されるため、最小限のリソースしか使用されません。
-   `DROP PARTITION` 、特に大規模な履歴データセットの場合、TTL よりも高速で予測可能です。

#### TiDBでTTLと<code>DROP PARTITION</code>使用する {#use-ttl-and-code-drop-partition-code-in-tidb}

以下の例では匿名化されたテーブル構造を使用しています。TTLの詳細については、 [TTL（Time to Live）を使用して定期的にデータを削除する](/time-to-live.md)参照してください。

次の例は、TTL 対応のテーブル スキーマを示しています。

```sql
CREATE TABLE `ad_cache` (
  `session_id` varchar(255) NOT NULL,
  `external_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `cache_data` mediumblob DEFAULT NULL,
  `data_version` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`session_id`, `external_id`, `create_time`, `id_suffix`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
TTL=`expire_time` + INTERVAL 0 DAY TTL_ENABLE='ON'
TTL_JOB_INTERVAL='10m';
```

次の例は、Range INTERVAL パーティション化を使用するパーティションテーブルを示しています。

```sql
CREATE TABLE `ad_cache` (
  `session_id` varchar(255) NOT NULL,
  `external_id` varbinary(255) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_suffix` bigint(20) NOT NULL,
  `expire_time` timestamp NULL DEFAULT NULL,
  `cache_data` mediumblob DEFAULT NULL,
  `data_version` int(11) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (
    `session_id`, `external_id`,
    `create_time`, `id_suffix`
  ) NONCLUSTERED
)
SHARD_ROW_ID_BITS=7
PRE_SPLIT_REGIONS=2
PARTITION BY RANGE COLUMNS (create_time)
INTERVAL (10 MINUTE)
FIRST PARTITION LESS THAN ('2025-02-19 18:00:00')
...
LAST PARTITION LESS THAN ('2025-02-19 20:00:00');
```

`FIRST PARTITION`と`LAST PARTITION`定期的に更新するには、次のようなDDL文を実行します。これらの文は古いパーティションを削除し、新しいパーティションを作成します。

```sql
ALTER TABLE ad_cache FIRST PARTITION LESS THAN ("${nextTimestamp}");
ALTER TABLE ad_cache LAST PARTITION LESS THAN ("${nextTimestamp}");
```

#### 推奨事項 {#recommendations}

-   大規模なデータクリーンアップや時間ベースのデータクリーンアップには、パーティション分割テーブル（パーティション番号`DROP PARTITION`を使用してください。このアプローチにより、パフォーマンスが向上し、システムへの影響が軽減され、操作が簡素化されます。
-   きめ細かいデータクリーンアップやバックグラウンドデータクリーンアップにはTTLを使用してください。TTLは、書き込みスループットが高いワークロードや、大量のデータを迅速に削除するワークロードには適していません。

### パーティション削除の効率: ローカルインデックスとグローバルインデックス {#partition-drop-efficiency-local-indexes-vs-global-indexes}

グローバルインデックスを持つパーティションテーブルの場合、 `DROP PARTITION`などのDDL操作は、グローバルインデックスエントリを同期的に更新する必要があります。これらの更新`REORGANIZE PARTITION` `TRUNCATE PARTITION` DDL実行時間が大幅に増加する可能性があります。

このセクションでは、グローバルインデックスを持つテーブルでは、ローカルインデックスを持つテーブルよりも`DROP PARTITION`大幅に遅くなることを示しています。パーティションテーブルを設計する際には、この動作を考慮してください。

#### テストケース {#test-case}

このテストでは、365個のパーティションと約10億行を持つテーブルを作成します。グローバルインデックスとローカルインデックスを使用した場合の`DROP PARTITION`を比較します。

| インデックスタイプ   | ドロップパーティション期間 |
| ----------- | ------------- |
| グローバルインデックス | 76.02秒        |
| ローカルインデックス  | 0.52秒         |

#### 調査結果 {#findings}

グローバルインデックスを持つテーブルでパーティションを削除すると**76.02秒**かかりますが、ローカルインデックスを持つテーブルで同じ操作を行うとわずか**0.52秒**しかかかりません。この差は、グローバルインデックスはすべてのパーティションにまたがるため、追加のインデックス更新が必要になるのに対し、ローカルインデックスはパーティションデータと共に削除されるためです。

パーティションを削除するには、次の SQL ステートメントを使用できます。

```sql
ALTER TABLE A DROP PARTITION A_2024363;
```

#### 推奨事項 {#recommendations}

-   パーティションテーブルでグローバル インデックスが使用される場合、 `DROP PARTITION` 、 `TRUNCATE PARTITION` 、 `REORGANIZE PARTITION`などの DDL 操作の実行時間が長くなることが予想されます。
-   パーティションを頻繁に削除し、パフォーマンスへの影響を最小限に抑える必要がある場合は、ローカル インデックスを使用して、より高速で効率的なパーティション管理を実現します。

## ホットスポットの問題を軽減する {#mitigate-hotspot-issues}

TiDB では、読み取りまたは書き込みトラフィックが[地域](/tidb-storage.md#region)に不均等に分散されている場合にホットスポットが発生します。ホットスポットは、次のような場合によく発生します。

-   単調に増加する主キー ( `AUTO_INCREMENT`主キーと`AUTO_ID_CACHE=1`など)。
-   デフォルト値が`CURRENT_TIMESTAMP`である datetime 列のセカンダリ インデックス。

TiDBは新しい行とインデックスエントリを「右端」のリージョンに追加します。時間が経つにつれて、この動作は次のような問題を引き起こす可能性があります。

-   単一のリージョンが書き込みワークロードの大部分を処理し、他のリージョンは十分に活用されないままになります。
-   読み取りおよび書き込みのレイテンシーが増加し、全体的なスループットが低下します。
-   TiKV ノードを追加しても、ボトルネックが単一のリージョンに残るため、パフォーマンスはほとんど向上しません。

これらの問題を軽減するには、パーティションテーブルを使用できます。プライマリキーにハッシュまたはキーによるパーティション分割を適用することで、TiDB は挿入操作を複数のパーティションとリージョンに分散し、単一のリージョンにおけるホットスポットの競合を軽減します。

> **注記：**
>
> このセクションでは、読み取りおよび書き込みホットスポットを軽減するための例として、パーティションテーブルを使用します。TiDB は、 [`AUTO_INCREMENT`](/auto-increment.md)や[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)などのホットスポット軽減のための追加機能も提供しています。
>
> 特定のシナリオでパーティションテーブルを使用する場合は、パーティション境界を維持するために`merge_option=deny`設定してください。詳細については[問題 #58128](https://github.com/pingcap/tidb/issues/58128)参照してください。

### パーティショニングの仕組み {#how-partitioning-works}

TiDBはテーブルデータとインデックスをリージョンに保存します。各リージョンは連続した範囲の行キーをカバーします。テーブルが`AUTO_INCREMENT`主キーまたは単調に増加する日付時刻インデックスを使用している場合、書き込みワークロードの分散はテーブルがパーティション分割されているかどうかによって異なります。

**パーティション化されていないテーブル**

パーティションテーブルでは、新しい行は常に最大のキー値を持ち、同じ「最後の」リージョンに書き込まれます。この単一のリージョンは、1つのTiKVノードによって処理されるため、書き込みのボトルネックになる可能性があります。

**ハッシュまたはキーでパーティション分割されたテーブル**

-   TiDB は、主キーまたはインデックス列にハッシュ関数またはキー関数を適用して、テーブルとそのインデックスを複数のパーティションに分割します。
-   各パーティションには独自のリージョン セットがあり、通常は異なる TiKV ノードに分散されます。
-   挿入操作は複数のリージョンに並行して分散され、ワー​​クロードのバランスと書き込みスループットが向上します。

### パーティショニングを使用する場合 {#when-to-use-partitioning}

主キーが[`AUTO_INCREMENT`](/auto-increment.md)テーブルに大量の一括挿入が行われ、書き込みホットスポットが発生する場合は、主キーにハッシュまたはキーのパーティション分割を適用して、書き込みワークロードをより均等に分散します。

次の SQL ステートメントは、主キーに基づいて 16 個のパーティションを持つテーブルを作成します。

```sql
CREATE TABLE server_info (
  id bigint NOT NULL AUTO_INCREMENT,
  serial_no varchar(100) DEFAULT NULL,
  device_name varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  device_type varchar(50) DEFAULT NULL,
  modified_ts timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id) /*T![clustered_index] CLUSTERED */,
  KEY idx_serial_no (serial_no),
  KEY idx_modified_ts (modified_ts)
) /*T![auto_id_cache] AUTO_ID_CACHE=1 */
PARTITION BY KEY (id) PARTITIONS 16;
```

### 利点 {#benefits}

パーティション化されたテーブルには次のような利点があります。

-   **バランスの取れた書き込みワークロード**: ホットスポットが複数のパーティションとリージョンに分散され、競合が軽減され、挿入パフォーマンスが向上します。
-   **パーティション プルーニングによるクエリ パフォーマンスの向上**: パーティション キーでフィルターするクエリの場合、TiDB は無関係なパーティションをスキップし、スキャンされるデータを削減して、クエリのレイテンシーを改善します。

### 制限事項 {#limitations}

パーティション テーブルを使用する前に、次の制限を考慮してください。

-   パーティションテーブルをパーティションテーブルに変換すると、TiDB によってパーティションごとに個別のリージョンが作成されるため、リージョンの合計数が増加します。

-   パーティションキーでフィルタリングしないクエリでは、パーティションプルーニングを使用できません。TiDBはすべてのパーティションをスキャンするか、すべてのパーティションにわたってインデックス検索を実行する必要があるため、コプロセッサタスクの数が増加し、パフォーマンスが低下する可能性があります。

    たとえば、次のクエリではパーティション キー ( `id` ) が使用されていないため、パフォーマンスが低下する可能性があります。

    ```sql
    SELECT * FROM server_info WHERE `serial_no` = ?;
    ```

-   パーティションキーを使用しないクエリのスキャンオーバーヘッドを削減するには、グローバルインデックスを作成する必要があります。グローバルインデックスは`DROP PARTITION`操作を遅くする可能性がありますが、ハッシュおよびキーパーティションテーブルは`DROP PARTITION`サポートしていません。したがって、これらのパーティションはほとんど切り捨てられないため、グローバルインデックスは実用的なソリューションです。例：

    ```sql
    ALTER TABLE server_info ADD UNIQUE INDEX(serial_no, id) GLOBAL;
    ```

## パーティション管理の課題 {#partition-management-challenges}

新しいレンジパーティションは、TiDBでホットスポット問題を引き起こす可能性があります。このセクションでは、一般的なシナリオと緩和策について説明します。

### ホットスポットを読む {#read-hotspots}

範囲パーティション化されたテーブルでは、クエリがパーティション キーでデータをフィルター処理しない場合、新しい空のパーティションが読み取りホットスポットになる可能性があります。

**根本的な原因：**

デフォルトでは、TiDB はテーブルを作成すると、各パーティションに対して空のリージョンを作成します。一定期間データが書き込まれない場合、TiDB は複数の空のパーティションのリージョンを 1 つのリージョンにマージすることがあります。

**インパクト：**

クエリがパーティションキーでフィルタリングされていない場合、TiDBはすべてのパーティションをスキャンします。これは実行プランでは`partition:all`と表示されます。その結果、複数の空のパーティションを保持する単一のリージョンが繰り返しスキャンされ、読み取りホットスポットが発生します。

### ホットスポットを書き込む {#write-hotspots}

時間ベースの列をパーティション キーとして使用すると、トラフィックが新しいパーティションに移行したときに書き込みホットスポットが発生する可能性があります。

**根本的な原因：**

TiDBでは、新しく作成されたパーティションは、最初は1つのTiKVノード上に1つのリージョンを持ちます。リージョンが分割されデータが再分配されるまで、すべての書き込みはこの単一のリージョンに送られます。この間、TiKVノードはアプリケーションからの書き込みとリージョン分割タスクの両方を処理する必要があります。

新しいパーティションへの初期書き込みトラフィックが非常に多い場合、TiKVノードには、リージョンを迅速に分割して分散させるのに十分なリソース（CPUやI/O容量など）がない可能性があります。その結果、書き込みは同じノードに予想よりも長く集中したままになります。

**インパクト：**

この不均衡により、TiKV ノードでフロー制御がトリガーされ、QPS が急激に低下し、書き込みレイテンシーが増加し、CPU 使用率が高くなり、クラスター全体のパフォーマンスが低下する可能性があります。

### パーティションテーブルの種類の比較 {#comparison-of-partitioned-table-types}

次の表は、非クラスター化パーティション テーブル、クラスター化パーティション テーブル、およびクラスター化非パーティション テーブルを比較したものです。

| テーブルタイプ              | リージョンの事前分割 | 読み取りパフォーマンス  | 書き込みスケーラビリティ | パーティションごとのデータクリーンアップ |
| -------------------- | ---------- | ------------ | ------------ | -------------------- |
| 非クラスタ化パーティションテーブル    | 自動         | 下位（追加の検索が必要） | 高い           | サポートされている            |
| クラスター化されたパーティションテーブル | マニュアル      | 高（検索回数が少ない）  | 高（手動管理あり）    | サポートされている            |
| クラスタ化された非パーティションテーブル | 該当なし       | 高い           | 安定した         | サポートされていません          |

### 非クラスタ化パーティションテーブルのソリューション {#solutions-for-non-clustered-partitioned-tables}

#### 利点 {#advantages}

-   [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)で構成された非クラスター化パーティションテーブルに新しいパーティションを作成すると、TiDB によってリージョンが自動的に事前分割され、手作業の労力が大幅に削減されます。
-   運用オーバーヘッドは低いです。

#### デメリット {#disadvantages}

**Point Get**または**Table Range Scan**を使用するクエリでは追加のテーブル検索が必要となり、読み取りパフォーマンスが低下する可能性があります。

#### 適切なシナリオ {#suitable-scenarios}

低レイテンシの読み取りよりも書き込みのスケーラビリティと操作のシンプルさが重要な場合は、クラスター化されていないパーティション テーブルを使用します。

#### ベストプラクティス {#best-practices}

新しい範囲パーティションによって発生するホットスポットの問題を軽減するには、次の手順に従います。

##### ステップ1. <code>SHARD_ROW_ID_BITS</code>と<code>PRE_SPLIT_REGIONS</code>を使用する {#step-1-use-code-shard-row-id-bits-code-and-code-pre-split-regions-code}

リージョンを事前に分割するために、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)でパーティションテーブルを作成します。

**要件：**

-   `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`以下でなければなりません。
-   各パーティションは`2^(PRE_SPLIT_REGIONS)`リージョンに事前に分割されます。

```sql
CREATE TABLE employees (
  id INT NOT NULL,
  fname VARCHAR(30),
  lname VARCHAR(30),
  hired DATE NOT NULL DEFAULT '1970-01-01',
  separated DATE DEFAULT '9999-12-31',
  job_code INT,
  store_id INT,
  PRIMARY KEY (`id`,`hired`) NONCLUSTERED,
  KEY `idx_employees_on_store_id` (`store_id`)
) SHARD_ROW_ID_BITS = 2 PRE_SPLIT_REGIONS = 2
PARTITION BY RANGE ( YEAR(hired) ) (
  PARTITION p0 VALUES LESS THAN (1991),
  PARTITION p1 VALUES LESS THAN (1996),
  PARTITION p2 VALUES LESS THAN (2001),
  PARTITION p3 VALUES LESS THAN (2006)
);
```

##### ステップ2. <code>merge_option=deny</code>属性を追加する {#step-2-add-the-code-merge-option-deny-code-attribute}

空のリージョンがマージされないようにするには、テーブルレベルまたはパーティションレベルで[`merge_option=deny`](/table-attributes.md#control-the-region-merge-behavior-using-table-attributes)属性を追加します。パーティションを削除しても、TiDB は削除されたパーティションに属するリージョンをマージします。

```sql
-- Table level
ALTER TABLE employees ATTRIBUTES 'merge_option=deny';
-- Partition level
ALTER TABLE employees PARTITION `p3` ATTRIBUTES 'merge_option=deny';
```

##### ステップ3. ビジネスデータに基づいて分割境界を決定する {#step-3-determine-split-boundaries-based-on-business-data}

テーブル作成時やパーティション追加時のホットスポットを回避するには、大量の書き込みが始まる前にリージョンを事前分割してください。効果的な事前分割を行うには、実際のビジネスデータ分布に基づいてリージョン分割の下限と上限を設定してください。境界を過度に広く設定することは避けてください。TiKVノード間での効率的なデータ分散が妨げられ、事前分割の目的が達成されない可能性があります。

既存の本番データから最小値と最大値を特定し、書き込みが事前に割り当てられた異なるリージョンに送信されるようにします。次のクエリは、既存のデータ範囲を取得する例を示しています。

```sql
SELECT MIN(id), MAX(id) FROM employees;
```

-   テーブルに履歴データがない場合、ビジネス要件と予想されるデータ範囲に基づいて最小値と最大値を推定します。
-   複合主キーまたは複合インデックスの場合は、分割境界を定義するために左端の列のみを使用します。
-   左端の列が文字列の場合は、データが均等に分散されるように、その長さと値の分散を考慮してください。

##### ステップ4. 領域を事前に分割して散布する {#step-4-pre-split-and-scatter-regions}

一般的な方法としては、TiKVノードの数に合わせてリージョン数を分割するか、TiKVノードの数の2倍に分割することが挙げられます。これにより、開始時からクラスター全体にデータがより均等に分散されます。

##### ステップ5. 必要に応じてプライマリインデックスとセカンダリインデックスの領域を分割する {#step-5-split-regions-for-primary-and-secondary-indexes-if-needed}

パーティションテーブル内のすべてのパーティションの主キーのリージョンを分割するには、次の SQL ステートメントを使用します。

```sql
SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "1970-01-01") AND (100000, "9999-12-31") REGIONS <number_of_regions>;
```

この例では、各パーティションの主キー範囲を指定された境界内の`<number_of_regions>`リージョンに分割します。

パーティションテーブル内のすべてのパーティションのセカンダリ インデックスの領域を分割するには、次の SQL ステートメントを使用します。

```sql
SPLIT PARTITION TABLE employees INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <number_of_regions>;
```

##### （オプション）ステップ6. 新しいパーティションを追加するときに手動で領域を分割する {#optional-step-6-manually-split-regions-when-adding-a-new-partition}

パーティションを追加するときに、主キーとインデックスのリージョンを手動で分割できます。

```sql
ALTER TABLE employees ADD PARTITION (PARTITION p4 VALUES LESS THAN (2011));

SHOW TABLE employees PARTITION (p4) regions;

SPLIT PARTITION TABLE employees INDEX `PRIMARY` BETWEEN (1, "2006-01-01") AND (100000, "2011-01-01") REGIONS <number_of_regions>;

SPLIT PARTITION TABLE employees PARTITION (p4) INDEX `idx_employees_on_store_id` BETWEEN (1) AND (1000) REGIONS <number_of_regions>;

SHOW TABLE employees PARTITION (p4) regions;
```

### クラスター化されたパーティションテーブルのソリューション {#solutions-for-clustered-partitioned-tables}

#### 利点 {#advantages}

**Point Get**または**Table Range Scan**を使用するクエリでは追加の検索は必要ないため、読み取りパフォーマンスが向上します。

#### デメリット {#disadvantages}

新しいパーティションを作成するときは、リージョンを手動で分割する必要があり、操作の複雑さが増します。

#### 適切なシナリオ {#suitable-scenarios}

低レイテンシのポイントクエリが重要であり、手動でリージョン分割を管理できる場合は、クラスター化されたパーティションテーブルを使用します。

#### ベストプラクティス {#best-practices}

新しい範囲パーティションによって発生するホットスポットの問題を軽減するには、 [非クラスタ化パーティションテーブルのベストプラクティス](#best-practices)手順に従います。

### クラスタ化された非パーティションテーブルのソリューション {#solutions-for-clustered-non-partitioned-tables}

#### 利点 {#advantages}

-   新しい範囲パーティションによるホットスポットのリスクはありません。
-   ポイントおよび範囲クエリの読み取りパフォーマンスが良好です。

#### デメリット {#disadvantages}

`DROP PARTITION`使用して大量の履歴データを効率的に削除することはできません。

#### 適切なシナリオ {#suitable-scenarios}

安定したパフォーマンスが必要で、パーティションベースのデータライフサイクル管理が必要ない場合は、クラスター化された非パーティションテーブルを使用します。

## パーティション化されたテーブルとパーティション化されていないテーブル間の変換 {#convert-between-partitioned-and-non-partitioned-tables}

1億2000万行のような大規模なテーブルでは、パフォーマンスチューニングやスキーマの再設計のために、パーティション化されたスキーマとパーティション化されていないスキーマ間の変換が必要になる場合があります。TiDBは以下のアプローチをサポートしています。

-   [パイプラインDML](/pipelined-dml.md) : `INSERT INTO ... SELECT ...`
-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) : `IMPORT INTO ... FROM SELECT ...`
-   [オンラインDDL](/dm/feature-online-ddl.md) : `ALTER TABLE`を使用した直接スキーマ変換

このセクションでは、両方の変換方向についてこれらの方法の効率と影響を比較し、ベスト プラクティスの推奨事項を示します。

### パーティションテーブルスキーマ: <code>fa</code> {#partitioned-table-schema-code-fa-code}

```sql
CREATE TABLE `fa` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE (`date`)
(PARTITION `fa_2024001` VALUES LESS THAN (2025001),
PARTITION `fa_2024002` VALUES LESS THAN (2025002),
PARTITION `fa_2024003` VALUES LESS THAN (2025003),
...
PARTITION `fa_2024365` VALUES LESS THAN (2025365));
```

### 非パーティションテーブルスキーマ: <code>fa_new</code> {#non-partitioned-table-schema-code-fa-new-code}

```sql
CREATE TABLE `fa_new` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint(20) NOT NULL,
  `sid` bigint(20) DEFAULT NULL,
  `user_id` bigint NOT NULL,
  `date` int NOT NULL,
  PRIMARY KEY (`id`,`date`) /*T![clustered_index] CLUSTERED */,
  KEY `index_fa_on_sid` (`sid`),
  KEY `index_fa_on_account_id` (`account_id`),
  KEY `index_fa_on_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

これらの例は、パーティションテーブルを非パーティションテーブルに変換する方法を示しています。非パーティションテーブルをパーティションテーブルに変換する場合も、同じ方法が適用されます。

### 方法 1: パイプライン DML <code>INSERT INTO ... SELECT</code> {#method-1-pipelined-dml-code-insert-into-select-code}

```sql
SET tidb_dml_type = "bulk";
SET tidb_mem_quota_query = 0;
SET tidb_enable_mutation_checker = OFF;
INSERT INTO fa_new SELECT * FROM fa;
-- 120 million rows copied in 58m 42s
```

### 方法 2: <code>IMPORT INTO ... FROM SELECT</code> {#method-2-code-import-into-from-select-code}

```sql
IMPORT INTO fa_new FROM SELECT * FROM fa WITH thread = 32, disable_precheck;
```

    Query OK, 120000000 rows affected, 1 warning (16 min 49.90 sec)
    Records: 120000000, ID: c1d04eec-fb49-49bb-af92-bf3d6e2d3d87

### 方法3: オンラインDDL {#method-3-online-ddl}

次の SQL ステートメントは、パーティションテーブルを非パーティションテーブルに変換します。

```sql
SET @@global.tidb_ddl_REORGANIZE_worker_cnt = 16;
SET @@global.tidb_ddl_REORGANIZE_batch_size = 4096;
ALTER TABLE fa REMOVE PARTITIONING;
-- Actual time: 170m 12.024s (approximately 2h 50m)
```

次の SQL ステートメントは、パーティションテーブルをパーティションテーブルに変換します。

```sql
SET @@global.tidb_ddl_REORGANIZE_worker_cnt = 16;
SET @@global.tidb_ddl_REORGANIZE_batch_size = 4096;
ALTER TABLE fa_new PARTITION BY RANGE (`date`)
(PARTITION `fa_2024001` VALUES LESS THAN (2025001),
PARTITION `fa_2024002` VALUES LESS THAN (2025002),
...
PARTITION `fa_2024365` VALUES LESS THAN (2025365),
PARTITION `fa_2024366` VALUES LESS THAN (2025366));

Query OK, 0 rows affected, 1 warning (2 hours 31 min 57.05 sec)
```

### 調査結果 {#findings}

次の表は、1 億 2000 万行のテーブルに対して各方法でかかった時間を示しています。

| 方法                                            | 所要時間   |
| --------------------------------------------- | ------ |
| 方法1：パイプラインDML（ `INSERT INTO ... SELECT ...` ） | 58分42秒 |
| 方法2： `IMPORT INTO ... FROM SELECT ...`        | 16分59秒 |
| 方法3: オンラインDDL（パーティションテーブルから非パーティションテーブルへ）     | 2時間50分 |
| 方法3: オンラインDDL（非パーティションテーブルからパーティションテーブルへ）     | 2時間31分 |
