---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash.
---

# TiFlashパフォーマンスの調整 {#tune-tiflash-performance}

このドキュメントでは、マシン リソースの計画や TiDB パラメータの調整など、 TiFlashのパフォーマンスを調整する方法を紹介します。

## リソースの計画 {#plan-resources}

マシン リソースを節約し、分離の要件がない場合は、TiKV とTiFlashの両方のデプロイを組み合わせた方法を使用できます。 TiKV とTiFlashにそれぞれ十分なリソースを確保し、ディスクを共有しないことをお勧めします。

## TiDB パラメータを調整する {#tune-tidb-parameters}

1.  OLAP/ TiFlash専用の TiDB ノードの場合、このノードの[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)構成項目の値を`80`に増やすことをお勧めします。

    {{< copyable "" >}}

    ```sql
    set @@tidb_distsql_scan_concurrency = 80;
    ```

2.  スーパー バッチ機能を有効にします。

    [`tidb_allow_batch_cop`](/system-variables.md#tidb_allow_batch_cop-new-in-v40)変数を使用して、 TiFlashから読み取るときにリージョンリクエストをマージするかどうかを設定できます。

    クエリに含まれるリージョンの数が比較的多い場合は、この変数を`1`に設定するか ( TiFlashにプッシュ ダウンされる`aggregation`のオペレーターを含むコプロセッサー リクエストに有効)、この変数を`2`に設定してみてください (すべてのコプロセッサー リクエストに有効です)。 TiFlashにプッシュダウン）。

    {{< copyable "" >}}

    ```sql
    set @@tidb_allow_batch_cop = 1;
    ```

3.  `JOIN`や`UNION`などの TiDB 演算子の前に集計関数をプッシュ ダウンする最適化を有効にします。

    [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)変数を使用してオプティマイザを制御し、この最適化を実行できます。クエリで集計操作が非常に遅い場合は、この変数を`1`に設定してみてください。

    {{< copyable "" >}}

    ```sql
    set @@tidb_opt_agg_push_down = 1;
    ```

4.  `JOIN`や`UNION`などの TiDB 演算子の前に`Distinct`を使用して集約関数をプッシュ ダウンする最適化を有効にします。

    [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)変数を使用してオプティマイザを制御し、この最適化を実行できます。クエリで`Distinct`を使用した集計操作が非常に遅い場合は、この変数を`1`に設定してみてください。

    {{< copyable "" >}}

    ```sql
    set @@tidb_opt_distinct_agg_push_down = 1;
    ```
