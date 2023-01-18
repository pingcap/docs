---
title: Tune TiFlash Performance
summary: Learn how to tune the performance of TiFlash by planning machine resources and tuning TiDB parameters.
---

# TiFlashパフォーマンスの調整 {#tune-tiflash-performance}

このドキュメントでは、マシン リソースを適切に計画し、TiDB パラメータを調整することによって、 TiFlashのパフォーマンスを調整する方法を紹介します。これらの方法に従うことで、 TiFlashクラスターは最適なパフォーマンスを実現できます。

## リソースの計画 {#plan-resources}

マシン リソースを節約し、分離の要件がない場合は、TiKV とTiFlashの両方のデプロイを組み合わせた方法を使用できます。 TiKV とTiFlashにそれぞれ十分なリソースを確保し、ディスクを共有しないことをお勧めします。

## TiDB パラメータを調整する {#tune-tidb-parameters}

このセクションでは、次のような TiDB パラメータを調整してTiFlash のパフォーマンスを向上させる方法について説明します。

-   [MPP モードを強制的に有効にする](#forcibly-enable-the-mpp-mode)
-   [`Join`または<code>Union</code>の前の位置に集約関数をプッシュダウンする](#push-down-aggregate-functions-to-a-position-before-join-or-union)
-   [`Distinct`最適化を有効にする](#enable-distinct-optimization)
-   [`ALTER TABLE ... COMPACT`ステートメントを使用してデータを圧縮する](#compact-data-using-the-alter-table--compact-statement)
-   [シャッフル ハッシュ結合をブロードキャスト ハッシュ結合に置き換える](#replace-shuffled-hash-join-with-broadcast-hash-join)
-   [より大きな実行同時実行数を設定する](#set-a-greater-execution-concurrency)
-   [`tiflash_fine_grained_shuffle_stream_count`構成する](#configure-tiflash_fine_grained_shuffle_stream_count)

### MPP モードを強制的に有効にする {#forcibly-enable-the-mpp-mode}

MPP 実行プランは、分散コンピューティング リソースを十分に活用できるため、バッチ データ クエリの効率が大幅に向上します。オプティマイザーがクエリの MPP 実行プランを生成しない場合は、MPP モードを強制的に有効にすることができます。

変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)は、オプティマイザのコスト見積もりを無視し、クエリの実行に TiFlash の MPP モードを強制的に使用するかどうかを制御します。 MPP モードを強制的に有効にするには、次のコマンドを実行します。

```sql
set @@tidb_enforce_mpp = ON;
```

### <code>Join</code>または<code>Union</code>の前の位置に集約関数をプッシュダウンする {#push-down-aggregate-functions-to-a-position-before-code-join-code-or-code-union-code}

集計操作を`Join`または`Union`の前の位置にプッシュダウンすることで、 `Join`または`Union`操作で処理するデータを減らすことができ、パフォーマンスが向上します。

変数[`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)は、オプティマイザーが集約関数を`Join`または`Union`の前の位置に押し下げる最適化操作を実行するかどうかを制御します。クエリで集計操作が非常に遅い場合は、この変数を`ON`に設定できます。

```sql
set @@tidb_opt_agg_push_down = ON;
```

### <code>Distinct</code>最適化を有効にする {#enable-code-distinct-code-optimization}

TiFlashは、 `Sum`などの`Distinct`列を受け入れる一部の集計関数をサポートしていません。デフォルトでは、集計関数全体が TiDB で計算されます。 `Distinct`最適化を有効にすることで、一部の操作をTiFlashにプッシュダウンできるため、クエリのパフォーマンスが向上します。

クエリで`distinct`操作の集計関数が遅い場合は、 [`tidb_opt_distinct_agg_push_down`](/system-variables.md#tidb_opt_distinct_agg_push_down)変数の値を`ON`に設定することで、 `Distinct` ( `select sum(distinct a) from t`など) の集計関数をコプロセッサーにプッシュ ダウンする最適化操作を有効にできます。

```sql
set @@tidb_opt_distinct_agg_push_down = ON;
```

### <code>ALTER TABLE ... COMPACT</code>ステートメントを使用してデータを圧縮する {#compact-data-using-the-code-alter-table-compact-code-statement}

[`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)ステートメントを実行すると、 TiFlashノード上の特定のテーブルまたはパーティションの圧縮を開始できます。圧縮中に、削除された行のクリーンアップや、更新によって発生した複数のバージョンのデータのマージなど、ノード上の物理データが書き換えられます。これにより、アクセス パフォーマンスが向上し、ディスク使用量が削減されます。以下に例を示します。

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

### シャッフル ハッシュ結合をブロードキャスト ハッシュ結合に置き換える {#replace-shuffled-hash-join-with-broadcast-hash-join}

小さなテーブルでの`Join`操作の場合、ブロードキャスト ハッシュ結合アルゴリズムは大きなテーブルの転送を回避できるため、コンピューティング パフォーマンスが向上します。

-   [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50)変数は、ブロードキャスト ハッシュ結合アルゴリズムを使用するかどうかを制御します。テーブル サイズ (単位: バイト) がこの変数の値より小さい場合、Broadcast Hash Join アルゴリズムが使用されます。それ以外の場合は、Shuffled Hash Join アルゴリズムが使用されます。

    ```sql
    set @@tidb_broadcast_join_threshold_size = 2000000;
    ```

-   [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50)変数は、ブロードキャスト ハッシュ結合アルゴリズムを使用するかどうかも制御します。結合操作のオブジェクトがサブクエリに属している場合、オプティマイザはサブクエリの結果セットのサイズを見積もることができません。この場合、サイズは結果セットの行数によって決まります。サブクエリの推定行数がこの変数の値よりも少ない場合、ブロードキャスト ハッシュ結合アルゴリズムが使用されます。それ以外の場合は、Shuffled Hash Join アルゴリズムが使用されます。

    ```sql
    set @@tidb_broadcast_join_threshold_count = 100000;
    ```

### より大きな実行同時実行数を設定する {#set-a-greater-execution-concurrency}

実行の同時実行数が増えると、 TiFlashがシステムのより多くの CPU リソースを占有できるようになり、クエリのパフォーマンスが向上します。

[`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)変数は、 TiFlashがリクエストを実行する最大同時実行数を設定するために使用されます。単位はスレッドです。

```sql
set @@tidb_max_tiflash_threads = 20;
```

### <code>tiflash_fine_grained_shuffle_stream_count</code>構成する {#configure-code-tiflash-fine-grained-shuffle-stream-count-code}

ファイングレイン シャッフル機能の[`tiflash_fine_grained_shuffle_stream_count`](/system-variables.md#tiflash_fine_grained_shuffle_stream_count-new-in-v620)を構成することにより、ウィンドウ関数を実行するための同時実行性を高めることができます。このようにして、ウィンドウ関数の実行により多くのシステム リソースを占有できるため、クエリのパフォーマンスが向上します。

ウィンドウ関数が実行のためにTiFlashにプッシュされると、この変数を使用してウィンドウ関数実行の同時実行レベルを制御できます。単位はスレッドです。

```sql
set @@tiflash_fine_grained_shuffle_stream_count = 20;
```
