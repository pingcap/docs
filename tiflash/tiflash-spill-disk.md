---
title: TiFlash Spill to Disk
summary: Learn how TiFlash spills data to disk and how to customize the spill behavior.
---

# TiFlash のディスクへの流出 {#tiflash-spill-to-disk}

このドキュメントでは、 TiFlash が計算中にデータをディスクに書き込む方法を紹介します。

v7.0.0 以降、 TiFlash はメモリ負荷を軽減するために中間データのディスクへのスピルをサポートします。次の演算子がサポートされています。

-   等結合条件を持つハッシュ結合演算子
-   `GROUP BY`キーを持つハッシュ集計演算子
-   ウィンドウ関数の TopN 演算子と並べ替え演算子

## 流出を引き起こす {#trigger-the-spilling}

TiFlash は、データをディスクに書き出すための 2 つのトリガー メカニズムを提供します。

-   オペレーターレベルのスピル: 各オペレーターのデータスピルしきい値を指定することで、 TiFlash がそのオペレーターのデータをいつディスクにスピルするかを制御できます。
-   クエリレベルのスピル: TiFlashノード上のクエリの最大メモリ使用量とスピルのメモリ比率を指定することで、 TiFlash がクエリでサポートされているオペレータのデータを必要に応じてディスクにスピルするタイミングを制御できます。

### オペレーターレベルの流出 {#operator-level-spilling}

v7.0.0 以降、 TiFlash はオペレーター レベルでの自動スピルをサポートします。次のシステム変数を使用して、各オペレーターのデータ流出のしきい値を制御できます。オペレーターのメモリ使用量がしきい値を超えると、 TiFlash はオペレーターに対してスピルをトリガーします。

-   [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700)
-   [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
-   [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)

#### 例 {#example}

この例では、ハッシュ集計演算子の流出を示すために、大量のメモリを消費する SQL ステートメントを構築します。

1.  環境を準備します。 2 つのノードでTiFlashクラスターを作成し、TPCH-100 データをインポートします。

2.  次のステートメントを実行します。これらのステートメントは、 `GROUP BY`キーによるハッシュ集計演算子のメモリ使用量を制限しません。

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 0;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

3.  TiFlashのログから、クエリは単一のTiFlashノードで 29.55 GiB のメモリを消費する必要があることがわかります。

        [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]

4.  次のステートメントを実行します。このステートメントは、キーが`GROUP BY`ハッシュ集計演算子のメモリ使用量を 10737418240 (10 GiB) に制限します。

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 10737418240;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

5.  TiFlashのログから、 `tidb_max_bytes_before_tiflash_external_group_by`を設定すると、 TiFlash が中間結果の流出をトリガーし、クエリで使用されるメモリが大幅に削減されることがわかります。

        [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]

### クエリレベルのスピル {#query-level-spilling}

v7.4.0 以降、 TiFlash はクエリ レベルでの自動スピルをサポートします。この機能は、次のシステム変数を使用して制御できます。

-   [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) : TiFlashノード上のクエリの最大メモリ使用量を制限します。
-   [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) : データの流出を引き起こすメモリ比率を制御します。

`tiflash_mem_quota_query_per_node`と`tiflash_query_spill_ratio`の両方が 0 より大きい値に設定されている場合、クエリのメモリ使用量が`tiflash_mem_quota_query_per_node * tiflash_query_spill_ratio`を超えると、 TiFlash はクエリでサポートされている演算子のスピルを自動的にトリガーします。

#### 例 {#example}

この例では、クエリ レベルの流出を示すために、大量のメモリを消費する SQL ステートメントを構築します。

1.  環境を準備します。 2 つのノードでTiFlashクラスターを作成し、TPCH-100 データをインポートします。

2.  次のステートメントを実行します。これらのステートメントは、クエリのメモリ使用量や`GROUP BY`キーによるハッシュ集計演算子のメモリ使用量を制限しません。

    ```sql
    SET tidb_max_bytes_before_tiflash_external_group_by = 0;
    SET tiflash_mem_quota_query_per_node = 0;
    SET tiflash_query_spill_ratio = 0;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

3.  TiFlashのログから、クエリが単一のTiFlashノードで 29.55 GiB のメモリを消費していることがわかります。

        [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]

4.  次のステートメントを実行します。これらのステートメントは、 TiFlashノード上のクエリの最大メモリ使用量を 5 GiB に制限します。

    ```sql
    SET tiflash_mem_quota_query_per_node = 5368709120;
    SET tiflash_query_spill_ratio = 0.7;
    SELECT
      l_orderkey,
      MAX(L_COMMENT),
      MAX(L_SHIPMODE),
      MAX(L_SHIPINSTRUCT),
      MAX(L_SHIPDATE),
      MAX(L_EXTENDEDPRICE)
    FROM lineitem
    GROUP BY l_orderkey
    HAVING SUM(l_quantity) > 314;
    ```

5.  TiFlashのログから、クエリ レベルのスピルを構成することにより、 TiFlash が中間結果のスピルをトリガーし、クエリによって使用されるメモリが大幅に削減されることがわかります。

        [DEBUG] [MemoryTracker.cpp:101] ["Peak memory usage (for query): 3.94 GiB."] [source=MemoryTracker] [thread_id=1547]

## ノート {#notes}

-   ハッシュ集計演算子に`GROUP BY`キーがない場合、スピルはサポートされません。ハッシュ集計演算子に個別の集約関数が含まれている場合でも、スピルはサポートされません。
-   現在、オペレーターレベルの流出のしきい値はオペレーターごとに個別に計算されます。 2 つのハッシュ集計演算子を含むクエリの場合、クエリレベルのスピルが構成されておらず、集約演算子のしきい値が 10 GiB に設定されている場合、2 つのハッシュ集計演算子は、それぞれのメモリ使用量が 10 GiB を超えた場合にのみデータをスピルします。
-   現在、ハッシュ集計演算子と TopN/Sort 演算子は、復元フェーズ中にマージ集約アルゴリズムとマージ ソート アルゴリズムを使用します。したがって、これら 2 つの演算子は 1 ラウンドのスピルをトリガーするだけです。メモリ需要が非常に高く、復元フェーズ中のメモリ使用量が依然としてしきい値を超えている場合、スピルは再度トリガーされません。
-   現在、ハッシュ結合演算子はパーティションベースのスピル戦略を使用しています。復元フェーズ中のメモリ使用量が依然としてしきい値を超えている場合、スピルは再びトリガーされます。ただし、流出規模を抑えるため、流出回数は３回までに制限されている。復元フェーズ中のメモリ使用量が 3 回目のスピル後もしきい値を超えている場合、スピルは再びトリガーされません。
-   クエリ レベルのスピルが設定されている場合 (つまり、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)と[`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)の両方が 0 より大きい場合)、 TiFlash は個々の演算子のスピルしきい値を無視し、クエリ レベルのスピルしきい値に基づいて、クエリ内の関連演算子のスピルを自動的にトリガーします。
-   クエリ レベルのスピルが構成されている場合でも、クエリで使用される演算子のいずれもスピルをサポートしていない場合、そのクエリの中間計算結果をディスクにスピルすることはできません。この場合、そのクエリのメモリ使用量が関連するしきい値を超えると、 TiFlash はエラーを返し、クエリを終了します。
-   クエリ レベルのスピルが構成されており、クエリにスピルをサポートする演算子が含まれている場合でも、次のいずれかのシナリオでメモリしきい値を超過するため、クエリはエラーを返す可能性があります。

    -   クエリ内の他の非スピル演算子はメモリを大量に消費します。
    -   スピル演算子は、タイムリーにディスクにスピルしません。

    スピル演算子が時間内にディスクにスピルしない状況に対処するには、 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)減らしてメモリしきい値エラーを回避してみてください。
