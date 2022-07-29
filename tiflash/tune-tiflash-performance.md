---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash.
---

# TiFlashのパフォーマンスを調整する {#tune-tiflash-performance}

このドキュメントでは、マシンリソースの計画やTiDBパラメータの調整など、TiFlashのパフォーマンスを調整する方法を紹介します。

## リソースを計画する {#plan-resources}

マシンリソースを節約したいが、分離の要件がない場合は、TiKVとTiFlashの両方の展開を組み合わせた方法を使用できます。 TiKVとTiFlashにそれぞれ十分なリソースを節約し、ディスクを共有しないことをお勧めします。

## TiDBパラメータを調整する {#tune-tidb-parameters}

1.  OLAP / TiFlash専用のTiDBノードの場合、このノードの[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)構成項目の値を`80`に増やすことをお勧めします。

    {{< copyable "" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2.  スーパーバッチ機能を有効にします。

    [`tidb_allow_batch_cop`](/system-variables.md#tidb_allow_batch_cop-new-in-v40)変数を使用して、TiFlashから読み取るときにリージョンリクエストをマージするかどうかを設定できます。

    クエリに関係するリージョンの数が比較的多い場合は、この変数を`1` （TiFlashにプッシュダウンされる`aggregation`のオペレーターを持つコプロセッサー要求に有効）に設定するか、この変数を`2` （すべてのコプロセッサー要求に有効）に設定してみてください。 TiFlashにプッシュダウン）。

    {{< copyable "" >}}

    ```sql
    set @@tidb_allow_batch_cop = 1;
    ```

3.  `JOIN`や`UNION`などのTiDB演算子の前に集計関数をプッシュダウンする最適化を有効にします。

    [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)変数を使用してオプティマイザーを制御し、この最適化を実行できます。クエリで集計操作が非常に遅い場合は、この変数を`1`に設定してみてください。

    {{< copyable "" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

4.  `JOIN`や`UNION`などのTiDB演算子の前に`Distinct`を使用して集計関数をプッシュダウンする最適化を有効にします。

    [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)変数を使用してオプティマイザーを制御し、この最適化を実行できます。クエリで`Distinct`の集計操作が非常に遅い場合は、この変数を`1`に設定してみてください。

    {{< copyable "" >}}

    ```sql
    set @@tidb_opt_distinct_agg_push_down = 1;
    ```
