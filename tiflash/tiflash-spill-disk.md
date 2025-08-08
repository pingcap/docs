---
title: TiFlash Spill to Disk
summary: TiFlash がデータをディスクに書き出す方法と、書き出し動作をカスタマイズする方法について説明します。
---

# TiFlashディスクへの書き込み {#tiflash-spill-to-disk}

このドキュメントでは、 TiFlash が計算中にデータをディスクに書き出す方法について説明します。

バージョン7.0.0以降、 TiFlashはメモリ負荷を軽減するために中間データをディスクに書き出す機能をサポートしています。以下の演算子がサポートされています。

-   等価結合条件を持つハッシュ結合演算子
-   `GROUP BY`キーを持つハッシュ集計演算子
-   TopN演算子とウィンドウ関数のソート演算子

## こぼれを誘発する {#trigger-the-spilling}

TiFlash は、データをディスクに書き出すための 2 つのトリガー メカニズムを提供します。

-   オペレータ レベルのスピル: 各オペレータのデータ スピルしきい値を指定することにより、 TiFlash がそのオペレータのデータをディスクにスピルするタイミングを制御できます。
-   クエリ レベルのスピル: TiFlashノードでのクエリの最大メモリ使用量とスピルのメモリ比率を指定することにより、 TiFlash がクエリでサポートされている演算子のデータを必要に応じてディスクにスピルするタイミングを制御できます。

### オペレータレベルのスピル {#operator-level-spilling}

バージョン7.0.0以降、 TiFlashはオペレータレベルでの自動スピルをサポートしています。以下のシステム変数を使用して、各オペレータのデータスピルのしきい値を制御できます。オペレータのメモリ使用量がしきい値を超えると、 TiFlashはそのオペレータのスピルをトリガーします。

-   [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700)
-   [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
-   [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)

#### 例 {#example}

この例では、ハッシュ集計演算子のスピルを示すために、大量のメモリを消費する SQL ステートメントを構築します。

1.  環境を準備します。2ノードのTiFlashクラスターを作成し、TPCH-100データをインポートします。

2.  以下のステートメントを実行してください。これらのステートメントは、 `GROUP BY`キーのハッシュ集計演算子のメモリ使用量を制限しません。

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

4.  次のステートメントを実行します。このステートメントは、キーが`GROUP BY`ハッシュ集計子のメモリ使用量を10737418240（10 GiB）に制限します。

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

5.  TiFlashのログを見ると、 `tidb_max_bytes_before_tiflash_external_group_by`設定するとTiFlash が中間結果のスピルをトリガーし、クエリで使用されるメモリが大幅に削減されることがわかります。

        [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]

### クエリレベルのスピル {#query-level-spilling}

TiFlash v7.4.0以降、クエリレベルでの自動スピルをサポートしています。この機能は、以下のシステム変数を使用して制御できます。

-   [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) : TiFlashノードでのクエリの最大メモリ使用量を制限します。
-   [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) : データの流出をトリガーするメモリ比率を制御します。

`tiflash_mem_quota_query_per_node`と`tiflash_query_spill_ratio`両方が 0 より大きい値に設定されている場合、クエリのメモリ使用量が`tiflash_mem_quota_query_per_node * tiflash_query_spill_ratio`超えると、 TiFlash はクエリでサポートされている演算子のスピルを自動的にトリガーします。

#### 例 {#example}

この例では、クエリ レベルのスピルを示すために大量のメモリを消費する SQL ステートメントを構築します。

1.  環境を準備します。2ノードのTiFlashクラスターを作成し、TPCH-100データをインポートします。

2.  以下のステートメントを実行してください。これらのステートメントは、クエリのメモリ使用量や、キーが`GROUP BY`ハッシュ集計演算子のメモリ使用量を制限しません。

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

4.  以下のステートメントを実行します。これらのステートメントは、 TiFlashノード上のクエリの最大メモリ使用量を5GiBに制限します。

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

5.  TiFlashのログから、クエリ レベルのスピルを構成すると、 TiFlash中間結果のスピルがトリガーされ、クエリで使用されるメモリが大幅に削減されることがわかります。

        [DEBUG] [MemoryTracker.cpp:101] ["Peak memory usage (for query): 3.94 GiB."] [source=MemoryTracker] [thread_id=1547]

## 注記 {#notes}

-   ハッシュ集計演算子に`GROUP BY`キーがない場合、スピルはサポートされません。ハッシュ集計子に独自の集計関数が含まれている場合でも、スピルはサポートされません。
-   現在、演算子レベルのスピルのしきい値は各演算子ごとに個別に計算されます。2つのハッシュ集計演算子を含むクエリの場合、クエリレベルのスピルが設定されておらず、集計演算子のしきい値が10 GiBに設定されている場合、2つのハッシュ集計演算子は、それぞれのメモリ使用量が10 GiBを超えた場合にのみデータをスピルします。
-   現在、ハッシュ集計演算子とTopN/Sort演算子は、リストアフェーズでマージ集計アルゴリズムとマージソートアルゴリズムを使用しています。そのため、これら2つの演算子はスピルを1ラウンドのみトリガーします。メモリ需要が非常に高く、リストアフェーズ中のメモリ使用量が依然としてしきい値を超えている場合、スピルは再度トリガーされません。
-   現在、ハッシュ結合演算子はパーティションベースのスピル戦略を使用しています。リストアフェーズ中のメモリ使用量が依然としてしきい値を超える場合、スピルは再度トリガーされます。ただし、スピルの規模を制御するため、スピルの回数は3回に制限されています。3回目のスピル後もリストアフェーズ中のメモリ使用量が依然としてしきい値を超える場合、スピルは再度トリガーされません。
-   クエリ レベルのスピルが設定されている場合 (つまり、 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740)と[`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)両方が 0 より大きい場合)、 TiFlash は個々の演算子のスピルしきい値を無視し、クエリ レベルのスピルしきい値に基づいてクエリ内の関連する演算子のスピルを自動的にトリガーします。
-   クエリレベルのスピルが設定されている場合でも、クエリで使用される演算子がスピルをサポートしていない場合、そのクエリの中間計算結果はディスクにスピルできません。この場合、そのクエリのメモリ使用量が関連するしきい値を超えると、 TiFlashはエラーを返し、クエリを終了します。
-   クエリ レベルのスピルが構成されていて、クエリにスピルをサポートする演算子が含まれている場合でも、次のいずれかのシナリオでメモリしきい値を超えたためにクエリからエラーが返される可能性があります。

    -   クエリ内のその他の非スピル演算子はメモリを大量に消費します。
    -   スピル演算子は、タイムリーにディスクにスピルしません。

    スピル演算子が時間内にディスクにスピルしない状況に対処するには、メモリしきい値エラーを回避するために[`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740)減らすことを試してください。
