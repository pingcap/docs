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

TiDB は、各オペレーターのスピルのしきい値を制御する次のシステム変数を提供します。オペレーターのメモリ使用量がしきい値を超えると、 TiFlash はオペレーターのスピルをトリガーします。

-   [`tidb_max_bytes_before_tiflash_external_group_by`](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700)
-   [`tidb_max_bytes_before_tiflash_external_join`](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700)
-   [`tidb_max_bytes_before_tiflash_external_sort`](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)

## 例 {#example}

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

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 29.55 GiB."] [source=MemoryTracker] [thread_id=468]
    ```

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

    ```
    [DEBUG] [MemoryTracker.cpp:69] ["Peak memory usage (total): 12.80 GiB."] [source=MemoryTracker] [thread_id=110]
    ```

## ノート {#notes}

-   ハッシュ集計演算子に`GROUP BY`キーがない場合、スピルはサポートされません。ハッシュ集計演算子に個別の集約関数が含まれている場合でも、スピルはサポートされません。
-   現在、閾値は演算子ごとに計算されています。クエリに 2 つのハッシュ集計演算子が含まれており、しきい値が 10 GiB に設定されている場合、2 つのハッシュ集計演算子は、それぞれのメモリ使用量が 10 GiB を超えた場合にのみデータを流出させます。
-   現在、ハッシュ集計演算子と TopN/Sort 演算子は、復元フェーズ中にマージ集約アルゴリズムとマージ ソート アルゴリズムを使用します。したがって、これら 2 つの演算子は 1 ラウンドのスピルをトリガーするだけです。メモリ需要が非常に高く、復元フェーズ中のメモリ使用量が依然としてしきい値を超えている場合、スピルは再度トリガーされません。
-   現在、ハッシュ結合演算子はパーティションベースのスピル戦略を使用しています。復元フェーズ中のメモリ使用量が依然としてしきい値を超えている場合、スピルは再びトリガーされます。ただし、流出規模を抑えるため、流出回数は３回までに制限されている。復元フェーズ中のメモリ使用量が 3 回目のスピル後もしきい値を超えている場合、スピルは再びトリガーされません。
