---
title: Introduction to Statistics
summary: 統計がテーブルレベルおよび列レベルの情報を収集する方法を学習します。
---

# 統計入門 {#introduction-to-statistics}

TiDB は、統計情報をオプティマイザへの入力として使用し、SQL ステートメントの各プラン ステップで処理される行数を推定します。オプティマイザは、 [インデックスアクセス](/choose-index.md)とテーブル結合のシーケンスを含む、使用可能な各プラン選択のコストを推定し、使用可能な各プランのコストを生成します。次に、オプティマイザは、全体的なコストが最も低い実行プランを選択します。

## 統計を収集する {#collect-statistics}

### 自動更新 {#automatic-update}

[`INSERT`](/sql-statements/sql-statement-insert.md) 、 [`DELETE`](/sql-statements/sql-statement-delete.md) 、または[`UPDATE`](/sql-statements/sql-statement-update.md)ステートメントの場合、TiDB は統計内の行数と変更された行数を自動的に更新します。

<CustomContent platform="tidb">

TiDB は定期的に更新情報を保持し、更新サイクルは 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)です。デフォルト値は`stats-lease`で、 `3s`です。値を`0`に指定すると、TiDB は統計の更新を自動的に停止します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB は 60 秒ごとに更新情報を保持します。

</CustomContent>

テーブルへの変更の数に基づいて、TiDB はそれらのテーブルの統計情報を収集するスケジュールを自動的に[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)設定します。これは、 [`tidb_enable_auto_anlyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)システム変数と次の`tidb_auto_analyze%`の変数によって制御されます。

| システム変数                                                                                                                | デフォルト値        | 説明                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_auto_anlyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                                | 真実            | TiDB が ANALYZE を自動的に実行するかどうかを制御します。                                                                                                                                              |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)                                             | 0.5           | 自動更新の閾値                                                                                                                                                                          |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time)                                   | `00:00 +0000` | TiDBが自動更新を実行できる1日の開始時刻                                                                                                                                                           |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time)                                       | `23:59 +0000` | TiDBが自動更新を実行できる1日の終了時刻                                                                                                                                                           |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)   | `128`         | パーティションテーブルを分析するときに TiDB が自動的に分析するパーティションの数 (つまり、パーティションテーブルの統計を自動的に更新するとき)                                                                                                      |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | `ON`          | 優先キューを有効にして、統計を自動的に収集するタスクをスケジュールするかどうかを制御します。この変数を有効にすると、TiDB は、新しく作成されたインデックスやパーティションが変更されたパーティション テーブルなど、収集する価値の高いテーブルの統計の収集を優先します。さらに、TiDB はヘルス スコアが低いテーブルを優先し、キューの先頭に配置します。 |

テーブル内の変更された行数と`tbl`の行の合計数の比率が`tidb_auto_analyze_ratio`より大きく、現在の時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`間である場合、TiDB はバックグラウンドで`ANALYZE TABLE tbl`ステートメントを実行し、このテーブルの統計を自動的に更新します。

小さなテーブルのデータを変更すると頻繁に自動更新がトリガーされる状況を回避するために、テーブルの行数が 1000 未満の場合、変更によって TiDB の自動更新はトリガーされません。 `SHOW STATS_META`ステートメントを使用して、テーブル内の行数を表示できます。

> **注記：**
>
> 現在、自動更新では、手動`ANALYZE`で入力した設定項目は記録されません。そのため、 `WITH`構文を使用して`ANALYZE`の収集動作を制御する場合は、統計情報を収集するためのスケジュールされたタスクを手動で設定する必要があります。

### 手動収集 {#manual-collection}

現在、TiDB は完全なコレクションとして統計情報を収集します。統計を収集するには、 `ANALYZE TABLE`ステートメントを実行できます。

次の構文を使用して完全なコレクションを実行できます。

-   `TableNameList`内のすべてのテーブルの統計を収集するには:

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `WITH NUM BUCKETS` 、生成されたヒストグラム内のバケットの最大数を指定します。

-   `WITH NUM TOPN`生成される`TOPN`の最大数を指定します。

-   `WITH NUM CMSKETCH DEPTH` CM スケッチの深さを指定します。

-   `WITH NUM CMSKETCH WIDTH` CM スケッチの幅を指定します。

-   `WITH NUM SAMPLES`サンプル数を指定します。

-   `WITH FLOAT_NUM SAMPLERATE`サンプリング レートを指定します。

`WITH NUM SAMPLES`と`WITH FLOAT_NUM SAMPLERATE`サンプルを収集する 2 つの異なるアルゴリズムに対応します。

詳しい説明については[ヒストグラム](#histogram) 、 [トップN](#top-n-values) 、 [CMSketch](#count-min-sketch) (Count-Min Sketch) を参照してください。 `SAMPLES` / `SAMPLERATE`については[収集パフォーマンスの向上](#improve-collection-performance)を参照してください。

オプションを永続化して再利用しやすくする方法については、 [ANALYZE構成を永続化する](#persist-analyze-configurations)参照してください。

## 統計の種類 {#types-of-statistics}

### ヒストグラム {#histogram}

ヒストグラム統計は、間隔述語または範囲述語の選択性を推定するためにオプティマイザによって使用され、統計のバージョン 2 で等号/IN 述語を推定するために列内の異なる値の数を決定するために使用されることもあります ( [統計のバージョン](#versions-of-statistics)を参照)。

ヒストグラムは、データの分布を大まかに表したものです。値の範囲全体を一連のバケットに分割し、バケットに含まれる値の数など、単純なデータを使用して各バケットを説明します。TiDB では、各テーブルの特定の列に対して等深度ヒストグラムが作成されます。等深度ヒストグラムを使用して、間隔クエリを推定できます。

ここで「等深度」とは、各バケットに入る値の数が可能な限り等しくなることを意味します。たとえば、特定のセット {1.6、1.9、1.9、2.0、2.4、2.6、2.7、2.7、2.8、2.9、3.4、3.5} に対して、4 つのバケットを生成するとします。等深度ヒストグラムは次のようになります。[1.6、1.9]、[2.0、2.6]、[2.7、2.8]、[2.9、3.5] の 4 つのバケットが含まれます。バケットの深さは 3 です。

![Equal-depth Histogram Example](/media/statistics-1.png)

ヒストグラムのバケット数の上限を決定するパラメータの詳細については、 [手動収集](#manual-collection)を参照してください。バケット数が多いほどヒストグラムの精度は高くなりますが、精度が高くなるとメモリリソースの使用量が増大します。実際のシナリオに応じて、この数値を適切に調整できます。

### カウントミニマムスケッチ {#count-min-sketch}

> **注記：**
>
> Count-Min スケッチは、統計バージョン 1 では、equal/IN 述語の選択性推定にのみ使用されます。バージョン 2 では、以下で説明するように、衝突を回避するために Count-Min スケッチを管理することが困難なため、他の統計が使用されます。

Count-Min Sketch はハッシュ構造です。等価クエリに`a = 1`または`IN`クエリ (たとえば`a IN (1, 2, 3)` ) が含まれる場合、TiDB はこのデータ構造を使用して推定を行います。

Count-Min Sketch [`EXPLAIN`](/sql-statements/sql-statement-explain.md)ハッシュ構造であるため、ハッシュ衝突が発生する可能性があります。1 文で、等価クエリの推定値が実際の値と大きく異なる場合、大きい値と小さい値が一緒にハッシュされていると考えられます。この場合、ハッシュ衝突を回避するには、次のいずれかの方法を実行します。

-   `WITH NUM TOPN`パラメータを変更します。TiDB は高頻度 (上位 x) データを別々に保存し、その他のデータは Count-Min Sketch に保存します。したがって、大きい値と小さい値が一緒にハッシュされるのを防ぐには、 `WITH NUM TOPN`の値を増やすことができます。TiDB では、デフォルト値は 20 です。最大値は 1024 です。このパラメータの詳細については、 [手動収集](#manual-collection)を参照してください。
-   2 つのパラメータ`WITH NUM CMSKETCH DEPTH`と`WITH NUM CMSKETCH WIDTH`を変更します。どちらもハッシュ バケットの数と衝突確率に影響します。実際のシナリオに応じて 2 つのパラメータの値を適切に増やすと、ハッシュ衝突の確率を下げることができますが、統計のメモリ使用量が高くなります。TiDB では、デフォルト値`WITH NUM CMSKETCH DEPTH`は 5、デフォルト値`WITH NUM CMSKETCH WIDTH`は 2048 です。2 つのパラメータの詳細については、 [手動収集](#manual-collection)を参照してください。

### 上位Nの値 {#top-n-values}

上位 N 値は、列またはインデックス内で上位 N 個出現する値です。上位 N 統計は、頻度統計またはデータ スキューと呼ばれることもあります。

TiDB は、Top-N 値の値と発生回数を記録します。デフォルト値は 20 で、最も頻繁に発生する上位 20 個の値が収集されることを意味します。最大値は 1024 です。収集される値の数を決定するパラメータの詳細については、 [手動収集](#manual-collection)参照してください。

## 選択的統計収集 {#selective-statistics-collection}

### インデックスの統計を収集する {#collect-statistics-on-indexes}

`IndexNameList` in `TableName`のすべてのインデックスの統計を収集するには、次の構文を使用します。

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

`IndexNameList`が空の場合、この構文は`TableName`内のすべてのインデックスの統計を収集します。

> **注記：**
>
> 収集前後の統計情報の一貫性を確保するために、 `tidb_analyze_version`が`2`の場合、この構文はインデックスだけでなく、テーブル全体 (すべての列とインデックスを含む) の統計を収集します。

### いくつかの列の統計を収集する {#collect-statistics-on-some-columns}

ほとんどの場合、オプティマイザは`WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`ステートメントの列の統計のみを使用します。これらの列は`PREDICATE COLUMNS`として参照できます。

テーブルに多数の列がある場合、すべての列の統計を収集すると、大きなオーバーヘッドが発生する可能性があります。オーバーヘッドを削減するには、特定の列（選択した列）のみの統計を収集するか、オプティマイザーが使用する`PREDICATE COLUMNS`のみの統計を収集します。将来再利用できるように列のサブセットの列リストを保持するには、 [列構成の保持](#persist-column-configurations)を参照してください。

> **注記：**
>
> -   述語列の統計の収集は[`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)にのみ適用されます。
> -   TiDB v7.2.0 以降、TiDB では[`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)システム変数も導入され、統計を収集する`ANALYZE`コマンドを実行するときに、統計収集でスキップされる列の種類を示します。システム変数は`tidb_analyze_version = 2`にのみ適用されます。

-   特定の列の統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    構文では、 `ColumnNameList`​​ターゲット列の名前リストを指定します。複数の列を指定する必要がある場合は、列名をコンマ`,`で区切ります。たとえば、 `ANALYZE table t columns a, b` 。この構文では、特定のテーブルの特定の列の統計を収集するだけでなく、インデックス付き列とそのテーブルのすべてのインデックスの統計も同時に収集します。

-   `PREDICATE COLUMNS`の統計を収集するには、次の手順を実行します。

    > **警告：**
    >
    > 現在、 `PREDICATE COLUMNS`の統計収集は実験的機能です。本番環境での使用はお勧めしません。

    1.  TiDB が`PREDICATE COLUMNS`を収集できるようにするには、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定します。

        <CustomContent platform="tidb">

        設定後、TiDB は 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システム テーブルに書き込みます。

        </CustomContent>

        <CustomContent platform="tidb-cloud">

        設定後、TiDB は 300 秒ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システム テーブルに書き込みます。

        </CustomContent>

    2.  ビジネスのクエリ パターンが比較的安定したら、次の構文を使用して`PREDICATE COLUMNS`の統計を収集します。

        ```sql
        ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
        ```

        この構文は、特定のテーブル内の`PREDICATE COLUMNS`の統計を収集するだけでなく、そのテーブル内のインデックス付き列とすべてのインデックスの統計を同時に収集します。

        > **注記：**
        >
        > -   [`mysql.column_stats_usage`](/mysql-schema.md)システム テーブルにそのテーブルに対して記録された`PREDICATE COLUMNS`含まれていない場合、上記の構文は、そのテーブル内のすべての列とすべてのインデックスの統計を収集します。
        > -   コレクションから除外された列 (手動で列をリストするか、 `PREDICATE COLUMNS`使用することで) の統計は上書きされません。新しいタイプの SQL クエリを実行すると、オプティマイザは、そのような列の古い統計 (存在する場合) または列の統計が収集されていない場合は疑似列統計を使用します。 `PREDICATE COLUMNS`を使用する次の ANALYZE では、それらの列の統計が収集されます。

-   すべての列とインデックスの統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

### パーティションの統計を収集する {#collect-statistics-on-partitions}

-   `PartitionNameList` in `TableName`のすべてのパーティションの統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `PartitionNameList` in `TableName`のすべてのパーティションのインデックス統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   テーブル内の一部のパーティションの[いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)だけが必要な場合は、次の構文を使用します。

    > **警告：**
    >
    > 現在、 `PREDICATE COLUMNS`の統計収集は実験的機能です。本番環境での使用はお勧めしません。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

#### 動的プルーニングモードでパーティションテーブルの統計を収集する {#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)でパーティション テーブルにアクセスすると (v6.3.0 以降のデフォルト)、TiDB はテーブル レベルの統計 (GlobalStats と呼ばれる) を収集します。現在、GlobalStats はすべてのパーティションの統計から集計されます。動的プルーニング モードでは、パーティションテーブルの統計の更新によって GlobalStats の更新がトリガーされることがあります。

パーティションが空の場合、または一部のパーティションの列が欠落している場合、コレクションの動作は[`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)変数によって制御されます。

-   GlobalStats 更新がトリガーされ、 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)が`OFF`場合:

    -   一部のパーティションに統計がない場合 (分析されたことのない新しいパーティションなど)、GlobalStats の生成が中断され、パーティションに統計がないことを示す警告メッセージが表示されます。

    -   特定のパーティションに一部の列の統計情報がない場合 (これらのパーティションで分析用に異なる列が指定されている場合)、これらの列の統計情報が集計されるときに GlobalStats の生成が中断され、特定のパーティションに一部の列の統計情報が存在しないことを示す警告メッセージが表示されます。

-   GlobalStats 更新がトリガーされ、 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)が`ON`場合:

    -   一部のパーティションのすべての列または一部の列の統計が欠落している場合、TiDB は GlobalStats を生成するときにこれらの欠落しているパーティションの統計をスキップするため、GlobalStats の生成には影響しません。

動的プルーニング モードでは、パーティションとテーブルの Analyze 構成は同じである必要があります。したがって、 `ANALYZE TABLE TableName PARTITION PartitionNameList`ステートメントの後に`COLUMNS`構成を指定したり、 `WITH`の後に`OPTIONS`構成を指定したりした場合、TiDB はそれらを無視し、警告を返します。

## 収集パフォーマンスの向上 {#improve-collection-performance}

> **注記：**
>
> -   TiDB での`ANALYZE TABLE`の実行時間は、MySQL や InnoDB よりも長くなる可能性があります。InnoDB では少数のページのみがサンプリングされますが、TiDB ではデフォルトで包括的な統計セットが完全に再構築されます。

TiDB は、統計収集のパフォーマンスを向上させる 2 つのオプションを提供します。

-   列のサブセットに関する統計を収集します。 [いくつかの列の統計情報を収集する](#collect-statistics-on-some-columns)を参照してください。
-   サンプリング。

### 統計サンプリング {#statistics-sampling}

サンプリングは、 `ANALYZE`ステートメントの 2 つの別個のオプションを介して実行できます。それぞれが異なる収集アルゴリズムに対応しています。

-   `WITH NUM SAMPLES` 、TiDB のリザーバ サンプリング メソッドで実装されるサンプリング セットのサイズを指定します。テーブルが大きい場合、このメソッドを使用して統計を収集することはお勧めしません。リザーバ サンプリングの中間結果セットには冗長な結果が含まれるため、メモリなどのリソースに余分な負荷がかかります。
-   `WITH FLOAT_NUM SAMPLERATE` 、v5.3.0 で導入されたサンプリング方法です。値の範囲が`(0, 1]`の場合、このパラメータはサンプリング レートを指定します。これは、TiDB のベルヌーイ サンプリングの方法で実装されており、より大きなテーブルのサンプリングに適しており、収集効率とリソース使用率が向上します。

v5.3.0 より前の TiDB では、統計を収集するためにリザーバ サンプリング メソッドが使用されていました。v5.3.0 以降、TiDB バージョン 2 の統計では、デフォルトでベルヌーイ サンプリング メソッドが使用されて統計が収集されます。リザーバ サンプリング メソッドを再利用するには、 `WITH NUM SAMPLES`ステートメントを使用できます。

現在のサンプリング レートは、適応アルゴリズムに基づいて計算されます。 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)を使用して表の行数を観察できる場合は、この行数を使用して 100,000 行に対応するサンプリング レートを計算できます。 この数を観察できない場合は、表の[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)の結果の`APPROXIMATE_KEYS`列のすべての値の合計を別の基準として使用して、サンプリング レートを計算できます。

<CustomContent platform="tidb">

> **注記：**
>
> 通常、 `STATS_META` `APPROXIMATE_KEYS`よりも信頼性が高いです。ただし、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)などの方法でデータをインポートした後、 `STATS_META`の結果は`0`なります。この状況に対処するには、 `STATS_META`の結果が`APPROXIMATE_KEYS`の結果よりもはるかに小さい場合に、 `APPROXIMATE_KEYS`使用してサンプリング レートを計算できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 通常、 `STATS_META` `APPROXIMATE_KEYS`よりも信頼性が高いです。ただし、 TiDB Cloudコンソール ( [サンプルデータのインポート](/tidb-cloud/import-sample-data.md)を参照) からデータをインポートした後、 `STATS_META`の結果は`0`なります。この状況に対処するには、 `STATS_META`の結果が`APPROXIMATE_KEYS`の結果よりもはるかに小さい場合に、 `APPROXIMATE_KEYS`使用してサンプリング レートを計算できます。

</CustomContent>

### 統計情報を収集するためのメモリ割り当て {#the-memory-quota-for-collecting-statistics}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

TiDB v6.1.0 以降では、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)を使用して、TiDB で統計を収集するためのメモリクォータを制御できます。

適切な値`tidb_mem_quota_analyze`を設定するには、クラスターのデータ サイズを考慮してください。デフォルトのサンプリング レートを使用する場合、主な考慮事項は、列の数、列値のサイズ、および TiDB のメモリ構成です。最大値と最小値を構成するときは、次の提案を考慮してください。

> **注記：**
>
> 以下の提案は参考用です。実際のシナリオに基づいて値を設定する必要があります。
>
> -   最小値: TiDB が最も多くの列を持つテーブルから統計を収集する場合の最大メモリ使用量よりも大きくする必要があります。おおよその目安: TiDB がデフォルト設定を使用して 20 列のテーブルから統計を収集する場合、最大メモリ使用量は約 800 MiB です。TiDB がデフォルト設定を使用して 160 列のテーブルから統計を収集する場合、最大メモリ使用量は約 5 GiB です。
> -   最大値: TiDB が統計を収集していない場合は、使用可能なメモリよりも小さくする必要があります。

## ANALYZE構成を永続化する {#persist-analyze-configurations}

v5.4.0 以降、TiDB はいくつかの`ANALYZE`つの構成の永続化をサポートしています。この機能により、将来の統計収集に既存の構成を簡単に再利用できます。

永続性をサポートする`ANALYZE`構成は次のとおりです。

| 構成            | 対応するANALYZE構文                                                                            |
| ------------- | ---------------------------------------------------------------------------------------- |
| ヒストグラムバケットの数  | バケット数                                                                                    |
| トップNの数        | 番号付きトップ                                                                                  |
| サンプル数         | サンプル数                                                                                    |
| サンプリングレート     | FLOATNUM SAMPLERATE 付き                                                                   |
| `ANALYZE`列タイプ | AnalyzeColumnOption ::= ( &#39;すべての列&#39; | &#39;述語列&#39; | &#39;列&#39; ColumnNameList ) |
| `ANALYZE`列目   | ColumnNameList ::= 識別子 ( &#39;,&#39; 識別子 )*                                              |

### ANALYZE構成の永続性を有効にする {#enable-analyze-configuration-persistence}

<CustomContent platform="tidb">

`ANALYZE`構成の永続性機能はデフォルトで有効になっています (システム変数`tidb_analyze_version`は`2`で`tidb_persist_analyze_options`はデフォルトで`ON`です)。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ANALYZE`構成の永続性機能は、デフォルトで無効になっています。この機能を有効にするには、システム変数`tidb_persist_analyze_options`が`ON`であることを確認し、システム変数`tidb_analyze_version`を`2`に設定します。

</CustomContent>

この機能を使用すると、ステートメントを手動で実行するときに、 `ANALYZE`ステートメントで指定された永続性設定を記録できます。記録されると、次に TiDB が統計を自動的に更新するか、これらの設定を指定せずに手動で統計を収集するときに、TiDB は記録された設定に従って統計を収集します。

auto analyze操作に使用される特定のテーブルに保存されている構成を照会するには、次の SQL ステートメントを使用できます。

```sql
SELECT sample_num, sample_rate, buckets, topn, column_choice, column_ids FROM mysql.analyze_options opt JOIN information_schema.tables tbl ON opt.table_id = tbl.tidb_table_id WHERE tbl.table_schema = '{db_name}' AND tbl.table_name = '{table_name}';
```

TiDB は、最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続構成を上書きします。たとえば、 `ANALYZE TABLE t WITH 200 TOPN;`実行すると、 `ANALYZE`ステートメントの上位 200 個の値が設定されます。続いて`ANALYZE TABLE t WITH 0.1 SAMPLERATE;`を実行すると、 `ANALYZE TABLE t WITH 200 TOPN, 0.1 SAMPLERATE;`と同様に、上位 200 個の値と auto `ANALYZE`ステートメントのサンプリング レート 0.1 の両方が設定されます。

### ANALYZE構成の永続性を無効にする {#disable-analyze-configuration-persistence}

`ANALYZE`構成の永続性機能を無効にするには、 `tidb_persist_analyze_options`システム変数を`OFF`に設定します。 `ANALYZE`構成の永続性機能は`tidb_analyze_version = 1`には適用されないため、 `tidb_analyze_version = 1`を設定することでもこの機能を無効にすることができます。

`ANALYZE`構成の永続性機能を無効にした後、TiDB は永続化された構成レコードをクリアしません。したがって、この機能を再度有効にすると、TiDB は以前に記録された永続的な構成を使用して統計を収集し続けます。

> **注記：**
>
> `ANALYZE`構成の永続性機能を再度有効にしたときに、以前に記録された永続性構成が最新のデータに適用できなくなった場合は、 `ANALYZE`ステートメントを手動で実行し、新しい永続性構成を指定する必要があります。

### 列構成の保持 {#persist-column-configurations}

`ANALYZE`ステートメントの列構成 ( `COLUMNS ColumnNameList` 、 `PREDICATE COLUMNS` 、 `ALL COLUMNS`を含む) を永続化する場合は、 `tidb_persist_analyze_options`システム変数の値を`ON`に設定して[構成の永続性を分析する](#persist-analyze-configurations)機能を有効にします。ANALYZE 構成永続化機能を有効にした後、次の操作を実行します。

-   TiDB が自動的に統計を収集する場合、または列構成を指定せずに`ANALYZE`ステートメントを実行して手動で統計を収集する場合、TiDB は統計収集に以前に保持された構成を引き続き使用します。
-   列構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDB は最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続的な構成を上書きします。

統計が収集された`PREDICATE COLUMNS`と列を見つけるには、 [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md)ステートメントを使用します。

次の例では、 `ANALYZE TABLE t PREDICATE COLUMNS;`実行した後、 TiDB は列`b` 、 `c` 、および`d`の統計を収集します。ここで、列`b`は`PREDICATE COLUMN`であり、列`c`と`d`はインデックス列です。

```sql
SET GLOBAL tidb_enable_column_tracking = ON;
Query OK, 0 rows affected (0.00 sec)

CREATE TABLE t (a INT, b INT, c INT, d INT, INDEX idx_c_d(c, d));
Query OK, 0 rows affected (0.00 sec)

-- The optimizer uses the statistics on column b in this query.
SELECT * FROM t WHERE b > 1;
Empty set (0.00 sec)

-- After waiting for a period of time (100 * stats-lease), TiDB writes the collected `PREDICATE COLUMNS` to mysql.column_stats_usage.
-- Specify `last_used_at IS NOT NULL` to show the `PREDICATE COLUMNS` collected by TiDB.
SHOW COLUMN_STATS_USAGE
WHERE db_name = 'test' AND table_name = 't' AND last_used_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at |
+---------+------------+----------------+-------------+---------------------+------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | NULL             |
+---------+------------+----------------+-------------+---------------------+------------------+
1 row in set (0.00 sec)

ANALYZE TABLE t PREDICATE COLUMNS;
Query OK, 0 rows affected, 1 warning (0.03 sec)

-- Specify `last_analyzed_at IS NOT NULL` to show the columns for which statistics have been collected.
SHOW COLUMN_STATS_USAGE
WHERE db_name = 'test' AND table_name = 't' AND last_analyzed_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+---------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at    |
+---------+------------+----------------+-------------+---------------------+---------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | 2022-01-05 17:23:06 |
| test    | t          |                | c           | NULL                | 2022-01-05 17:23:06 |
| test    | t          |                | d           | NULL                | 2022-01-05 17:23:06 |
+---------+------------+----------------+-------------+---------------------+---------------------+
3 rows in set (0.00 sec)
```

## 統計のバージョン {#versions-of-statistics}

[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)変数は、TiDB によって収集される統計を制御します。現在、 `tidb_analyze_version = 1`と`tidb_analyze_version = 2` 2 つのバージョンの統計がサポートされています。

-   TiDB Self-Hosted の場合、この変数のデフォルト値は、v5.3.0 以降で`1`から`2`に変更されます。
-   TiDB Cloudの場合、この変数のデフォルト値は、v6.5.0 以降で`1`から`2`に変更されます。
-   クラスターが以前のバージョンからアップグレードされた場合、アップグレード後もデフォルト値`tidb_analyze_version`は変更されません。

バージョン 2 が推奨されており、最終的にはバージョン 1 を完全に置き換えるために引き続き機能強化される予定です。バージョン 1 と比較すると、バージョン 2 では、より大規模なデータ ボリュームに対して収集される多くの統計の精度が向上しています。また、バージョン 2 では、述語選択性の推定のために Count-Min スケッチ統計を収集する必要がなくなり、選択した列のみの自動収集もサポートされるようになったため、収集パフォーマンスが向上しています ( [いくつかの列の統計情報を収集する](#collect-statistics-on-some-columns)を参照)。

次の表は、オプティマイザーの推定で使用するために各バージョンで収集される情報を示しています。

| 情報          | バージョン 1                            | バージョン2                         |
| ----------- | ---------------------------------- | ------------------------------ |
| 表内の行の総数     | √                                  | √                              |
| 等号/IN述語推定   | √ (カラム/ インデックス トップ N と カウント最小スケッチ) | √ (カラム/ インデックス トップ N と ヒストグラム) |
| 範囲述語推定      | √ (カラム/ インデックス トップ N と ヒストグラム)     | √ (カラム/ インデックス トップ N と ヒストグラム) |
| `NULL`述語推定  | √                                  | √                              |
| 列の平均長さ      | √                                  | √                              |
| インデックスの平均長さ | √                                  | √                              |

### 統計バージョンを切り替える {#switch-between-statistics-versions}

すべてのテーブル/インデックス (およびパーティション) が同じバージョンの統計収集を利用するようにすることをお勧めします。バージョン 2 が推奨されますが、使用中のバージョンで問題が発生したなどの正当な理由がない限り、あるバージョンから別のバージョンに切り替えることはお勧めしません。バージョン間の切り替えでは、すべてのテーブルが新しいバージョンで分析されるまで統計が利用できない期間が発生する可能性があり、統計が利用できない場合はオプティマイザー プランの選択に悪影響を与える可能性があります。

切り替えの正当な理由の例としては、バージョン 1 では、Count-Min スケッチ統計を収集するときにハッシュ衝突が原因で、equal/IN 述語の推定が不正確になる可能性があることが挙げられます。解決策は[カウントミニマムスケッチ](#count-min-sketch)セクションに記載されています。または、 `tidb_analyze_version = 2`を設定して、すべてのオブジェクトで`ANALYZE`を再実行することも解決策です。バージョン 2 の初期リリースでは、 `ANALYZE`後にメモリオーバーフローが発生するリスクがありました。この問題は解決されていますが、当初は、 `set tidb_analyze_version = 1`を設定して、すべてのオブジェクトで`ANALYZE`を再実行するという解決策がありました。

バージョン間の切り替え`ANALYZE`準備するには:

-   `ANALYZE`ステートメントを手動で実行する場合は、分析対象のすべてのテーブルを手動で分析します。

    ```sql
    SELECT DISTINCT(CONCAT('ANALYZE TABLE ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables JOIN mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 2;
    ```

-   自動分析が有効になっているため、TiDB が`ANALYZE`ステートメントを自動的に実行する場合は、 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)ステートメントを生成する次のステートメントを実行します。

    ```sql
    SELECT DISTINCT(CONCAT('DROP STATS ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables ON mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 2;
    ```

-   前のステートメントの結果が長すぎてコピーして貼り付けることができない場合は、結果を一時テキスト ファイルにエクスポートし、次のようにファイルから実行することができます。

    ```sql
    SELECT DISTINCT ... INTO OUTFILE '/tmp/sql.txt';
    mysql -h ${TiDB_IP} -u user -P ${TIDB_PORT} ... < '/tmp/sql.txt'
    ```

## 統計情報をビュー {#view-statistics}

次のステートメントを使用して、 `ANALYZE`ステータスと統計情報を表示できます。

### <code>ANALYZE</code>状態 {#code-analyze-code-state}

`ANALYZE`ステートメントを実行すると、 [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)を使用して`ANALYZE`の現在の状態を表示できます。

TiDB v6.1.0 以降では、 `SHOW ANALYZE STATUS`ステートメントはクラスター レベルのタスクの表示をサポートします。TiDB を再起動した後でも、このステートメントを使用して再起動前のタスク レコードを表示できます。TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンス レベルのタスクのみを表示でき、タスク レコードは TiDB の再起動後にクリアされます。

`SHOW ANALYZE STATUS`最新のタスク レコードのみを表示します。TiDB v6.1.0 以降では、システム テーブル`mysql.analyze_jobs`を通じて過去 7 日間の履歴タスクを表示できます。

[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)が設定され、TiDB のバックグラウンドで実行されている自動`ANALYZE`タスクがこのしきい値を超えるメモリを使用すると、タスクは再試行されます。 `SHOW ANALYZE STATUS`ステートメントの出力で、失敗したタスクと再試行されたタスクを確認できます。

[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)が 0 より大きく、TiDB のバックグラウンドで実行されている自動`ANALYZE`タスクにこのしきい値を超える時間がかかる場合、タスクは終了します。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

### テーブルのメタデータ {#metadata-of-tables}

[`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)ステートメントを使用すると、行の合計数と更新された行の数を表示できます。

### テーブルの健全性状態 {#health-state-of-tables}

[`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを使用すると、テーブルの正常性状態を確認し、統計の精度を大まかに見積もることができます。 `modify_count` &gt;= `row_count`の場合、正常性状態は 0 です。 `modify_count` &lt; `row_count`の場合、正常性状態は (1 - `modify_count` / `row_count` ) * 100 です。

### 列のメタデータ {#metadata-of-columns}

[`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md)ステートメントを使用すると、すべての列の異なる値の数と`NULL`の数を表示できます。

### ヒストグラムのバケット {#buckets-of-histogram}

[ `SHOW STATS_BUCKETS` ](/sql-statements/sql-statement-show-stats-buckets.md ステートメントを使用して、ヒストグラムの各バケットを表示できます。

### トップN情報 {#top-n-information}

[`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md)ステートメントを使用すると、TiDB によって現在収集されている Top-N 情報を表示できます。

## 統計情報を削除 {#delete-statistics}

統計を削除するには、 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)ステートメントを実行します。

## 負荷統計 {#load-statistics}

> **注記：**
>
> [TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは読み込み統計は利用できません。

デフォルトでは、列統計のサイズに応じて、TiDB は次のように異なる方法で統計をロードします。

-   メモリを少量しか消費しない統計 (count、distinctCount、nullCount など) の場合、列データが更新されている限り、TiDB は対応する統計をメモリに自動的にロードし、SQL 最適化ステージで使用します。
-   大量のメモリを消費する統計 (ヒストグラム、TopN、Count-Min Sketch など) の場合、SQL 実行のパフォーマンスを確保するために、TiDB はオンデマンドで統計を非同期的にロードします。ヒストグラムを例に挙げると、TiDB は、オプティマイザがその列のヒストグラム統計を使用する場合にのみ、その列のヒストグラム統計をメモリにロードします。オンデマンドの非同期統計のロードは、SQL 実行のパフォーマンスには影響しませんが、SQL 最適化に不完全な統計を提供する可能性があります。

v5.4.0 以降、TiDB では統計の同期ロード機能が導入されています。この機能により、SQL ステートメントを実行するときに、TiDB は大規模な統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリにメモリにロードできるようになり、SQL 最適化の統計の完全性が向上します。

この機能を有効にするには、 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)システム変数の値を、SQL 最適化が完全な列統計を同期的にロードするまで待機できる最大タイムアウト (ミリ秒単位) に設定します。この変数のデフォルト値は`100`で、この機能が有効であることを示します。

<CustomContent platform="tidb">

統計の同期読み込み機能を有効にした後、次のように機能をさらに構成できます。

-   SQL 最適化の待機時間がタイムアウトに達したときの TiDB の動作を制御するには、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更します。この変数のデフォルト値は`ON`で、タイムアウト後、SQL 最適化プロセスではどの列でもヒストグラム、TopN、または CMSketch 統計が使用されないことを示します。この変数が`OFF`に設定されている場合、タイムアウト後、SQL 実行は失敗します。
-   同期ロード統計機能が同時に処理できる列の最大数を指定するには、TiDB 構成ファイルの[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)オプションの値を変更します。デフォルト値は`5`です。
-   同期的にロードする統計機能がキャッシュできる列リクエストの最大数を指定するには、TiDB 構成ファイルの[`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)オプションの値を変更します。デフォルト値は`1000`です。

TiDB の起動時に、初期統計が完全にロードされる前に実行される SQL ステートメントの実行プランが最適ではない場合があり、パフォーマンスの問題が発生します。このような問題を回避するために、TiDB v7.1.0 では構成パラメータ[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が導入されています。このオプションを使用すると、起動時に統計の初期化が完了した後にのみ TiDB がサービスを提供するかどうかを制御できます。v7.2.0 以降では、このパラメータはデフォルトで有効になっています。

v7.1.0 以降、TiDB では軽量統計の初期化に[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)導入されています。

-   `lite-init-stats`の値が`true`の場合、統計の初期化では、インデックスまたは列のヒストグラム、TopN、または Count-Min Sketch がメモリにロードされません。
-   `lite-init-stats`の値が`false`の場合、統計の初期化では、インデックスと主キーのヒストグラム、TopN、Count-Min Sketch がメモリにロードされますが、主キー以外の列のヒストグラム、TopN、Count-Min Sketch はメモリにロードされません。オプティマイザーが特定のインデックスまたは列のヒストグラム、TopN、Count-Min Sketch を必要とする場合、必要な統計が同期的または非同期的にメモリにロードされます。

デフォルト値`lite-init-stats`は`true`で、軽量統計の初期化を有効にすることを意味します。 `lite-init-stats`から`true`に設定すると、統計の初期化が高速化され、不要な統計の読み込みが回避されるため、TiDB のメモリ使用量が削減されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

統計の同期ロード機能を有効にした後、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更することで、SQL 最適化の待機時間がタイムアウトに達したときの TiDB の動作を制御できます。この変数のデフォルト値は`ON`で、タイムアウト後、SQL 最適化プロセスはどの列でもヒストグラム、TopN、または CMSketch 統計を使用しないことを示します。この変数が`OFF`に設定されている場合、タイムアウト後、SQL 実行は失敗します。

</CustomContent>

## 輸入と輸出の統計 {#import-and-export-statistics}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

### 輸出統計 {#export-statistics}

統計をエクスポートするためのインターフェースは次のとおりです。

-   `${db_name}`データベース内の`${table_name}`テーブルの JSON 形式の統計を取得するには:

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}

    例えば：

    ```shell
    curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json
    ```

-   特定の時間における`${db_name}`データベース内の`${table_name}`テーブルの JSON 形式の統計を取得するには:

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}

### 輸入統計 {#import-statistics}

> **注記：**
>
> MySQL クライアントを起動するときは、 `--local-infile=1`オプションを使用します。

通常、インポートされた統計は、エクスポート インターフェイスを使用して取得された JSON ファイルを参照します。

統計の読み込みは[`LOAD STATS`](/sql-statements/sql-statement-load-stats.md)ステートメントで実行できます。

例えば：

```sql
LOAD STATS 'file_name'
```

`file_name`はインポートする統計のファイル名です。

## ロック統計 {#lock-statistics}

v6.5.0 以降、TiDB は統計のロックをサポートしています。テーブルまたはパーティションの統計がロックされると、テーブルの統計は変更できなくなり、テーブルに対して`ANALYZE`ステートメントを実行することもできなくなります。例:

テーブル`t`を作成し、そこにデータを挿入します。テーブル`t`の統計がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

```sql
mysql> CREATE TABLE t(a INT, b INT);
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                                                                               |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

テーブル`t`の統計をロックし、 `ANALYZE`を実行します。警告メッセージは、 `ANALYZE`ステートメントがテーブル`t`をスキップしたことを示します。

```sql
mysql> LOCK STATS t;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 2 warnings (0.00 sec)

mysql> SHOW WARNINGS;
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                 |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t                                                                                                       |
+---------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

表`t`および`ANALYZE`の統計のロックを解除すると、再度正常に実行できます。

```sql
mysql> UNLOCK STATS t;
Query OK, 0 rows affected (0.01 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> SHOW WARNINGS;
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                 |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t, reason to use this rate is "use min(1, 110000/8) as the sample-rate=1" |
+-------+------+-----------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

さらに、 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)使用してパーティションの統計をロックすることもできます。例:

パーティション テーブル`t`を作成し、そこにデータを挿入します。パーティション`p1`の統計がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

```sql
mysql> CREATE TABLE t(a INT, b INT) PARTITION BY RANGE (a) (PARTITION p0 VALUES LESS THAN (10), PARTITION p1 VALUES LESS THAN (20), PARTITION p2 VALUES LESS THAN (30));
Query OK, 0 rows affected (0.03 sec)

mysql> INSERT INTO t VALUES (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 6 warning (0.02 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                                                                                              |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p0, reason to use this rate is "Row count in stats_meta is much smaller compared with the row count got by PD, use min(1, 15000/4) as the sample-rate=1" |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
| Warning | 1105 | disable dynamic pruning due to t has no global stats                                                                                                                                                                                 |
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p2, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1"                                                                 |
+---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
6 rows in set (0.01 sec)
```

パーティション`p1`の統計をロックし、 `ANALYZE`を実行します。警告メッセージは、 `ANALYZE`ステートメントがパーティション`p1`をスキップしたことを示します。

```sql
mysql> LOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> SHOW STATS_LOCKED;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          | p1             | locked |
+---------+------------+----------------+--------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 2 warnings (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                                              |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
| Warning | 1105 | skip analyze locked table: test.t partition (p1)                                                                                                                     |
+---------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
2 rows in set (0.00 sec)
```

パーティション`p1`と`ANALYZE`の統計情報のロック解除を再度正常に実行できます。

```sql
mysql> UNLOCK STATS t PARTITION p1;
Query OK, 0 rows affected (0.00 sec)

mysql> ANALYZE TABLE t PARTITION p1;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Level | Code | Message                                                                                                                                                              |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t's partition p1, reason to use this rate is "TiDB assumes that the table is empty, use sample-rate=1" |
+-------+------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### 統計情報のロックの動作 {#behaviors-of-locking-statistics}

-   パーティションテーブルの統計をロックすると、パーティションテーブルのすべてのパーティションの統計がロックされます。
-   テーブルまたはパーティションを切り捨てると、テーブルまたはパーティションの統計ロックが解除されます。

次の表は、統計のロックの動作を示しています。

|                                    | テーブル全体を削除する | テーブル全体を切り捨てる                             | パーティションを切り捨てる                                | 新しいパーティションを作成する        | パーティションを削除する                                     | パーティションを再編成する                                   | パーティションを交換する                                 |
| ---------------------------------- | ----------- | ---------------------------------------- | -------------------------------------------- | ---------------------- | ------------------------------------------------ | ----------------------------------------------- | -------------------------------------------- |
| パーティションテーブルがロックされている               | ロックが無効です    | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。 | /                                            | /                      | /                                                | /                                               | /                                            |
| パーティションテーブルとテーブル全体がロックされている        | ロックが無効です    | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。 | 古いパーティションのロック情報は無効であり、新しいパーティションは自動的にロックされます | 新しいパーティションは自動的にロックされます | 削除されたパーティションのロック情報はクリアされ、テーブル全体のロックは引き続き有効になります。 | 削除されたパーティションのロック情報はクリアされ、新しいパーティションは自動的にロックされます | ロック情報は交換されたテーブルに転送され、新しいパーティションは自動的にロックされます。 |
| パーティションテーブルで、一部のパーティションのみがロックされている | ロックが無効です    | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。 | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。     | /                      | 削除されたパーティションのロック情報はクリアされます                       | 削除されたパーティションのロック情報はクリアされます                      | ロック情報は交換テーブルに転送される                           |

## <code>ANALYZE</code>タスクと同時実行を管理する {#manage-code-analyze-code-tasks-and-concurrency}

### バックグラウンドの<code>ANALYZE</code>タスクを終了する {#terminate-background-code-analyze-code-tasks}

TiDB v6.0 以降、TiDB は`KILL`ステートメントを使用してバックグラウンドで実行されている`ANALYZE`タスクを終了することをサポートしています。バックグラウンドで実行されている`ANALYZE`タスクが大量のリソースを消費し、アプリケーションに影響を与えていることがわかった場合は、次の手順を実行して`ANALYZE`タスクを終了できます。

1.  次の SQL ステートメントを実行します。

    ```sql
    SHOW ANALYZE STATUS
    ```

    結果の`instance`列目と`process_id`列目を確認すると、TiDB インスタンスのアドレスとバックグラウンド`ANALYZE`タスクのタスク`ID`を取得できます。

2.  バックグラウンドで実行されている`ANALYZE`タスクを終了します。

    <CustomContent platform="tidb">

    -   [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が`true` (デフォルトでは`true` ) の場合、 `KILL TIDB ${id};`ステートメントを直接実行できます。ここで、 `${id}`前の手順で取得されたバックグラウンド`ANALYZE`タスクの`ID`です。
    -   `enable-global-kill`が`false`の場合、クライアントを使用して、バックエンド`ANALYZE`タスクを実行している TiDB インスタンスに接続してから、 `KILL TIDB ${id};`ステートメントを実行する必要があります。クライアントを使用して別の TiDB インスタンスに接続した場合、またはクライアントと TiDB クラスターの間にプロキシがある場合、 `KILL`ステートメントはバックグラウンド`ANALYZE`タスクを終了できません。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    `ANALYZE`タスクを終了するには、 `KILL TIDB ${id};`ステートメントを実行します。ここで、 `${id}`前の手順で取得したバックグラウンド`ANALYZE`タスクの`ID`です。

    </CustomContent>

`KILL`ステートメントの詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

### <code>ANALYZE</code>同時実行を制御する {#control-code-analyze-code-concurrency}

`ANALYZE`ステートメントを実行すると、システム変数を使用して同時実行性を調整し、システムへの影響を制御できます。

関連するシステム変数の関係を以下に示します。

![analyze\_concurrency](/media/analyze_concurrency.png)

`tidb_build_stats_concurrency` 、 `tidb_build_sampling_stats_concurrency` 、 `tidb_analyze_partition_concurrency` 、上の図に示すように、上流と下流の関係にあります。実際の合計同時実行数は、 `tidb_build_stats_concurrency` * ( `tidb_build_sampling_stats_concurrency` + `tidb_analyze_partition_concurrency` ) です。これらの変数を変更するときは、それぞれの値を同時に考慮する必要があります。 `tidb_analyze_partition_concurrency` 、 `tidb_build_sampling_stats_concurrency` 、 `tidb_build_stats_concurrency`の順に 1 つずつ調整し、システムへの影響を観察することをお勧めします。これら 3 つの変数の値が大きいほど、システムのリソース オーバーヘッドが大きくなります。

#### <code>tidb_build_stats_concurrency</code> {#code-tidb-build-stats-concurrency-code}

`ANALYZE`ステートメントを実行すると、タスクは複数の小さなタスクに分割されます。各タスクは、1 つの列またはインデックスの統計情報のみを処理します。 [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)変数を使用して、同時実行される小さなタスクの数を制御できます。デフォルト値は`2`です。v7.4.0 以前のバージョンでは、デフォルト値は`4`です。

#### <code>tidb_build_sampling_stats_concurrency</code> {#code-tidb-build-sampling-stats-concurrency-code}

通常の列を分析する場合、 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)使用してサンプリング タスクの実行の同時実行を制御できます。デフォルト値は`2`です。

#### <code>tidb_analyze_partition_concurrency</code> {#code-tidb-analyze-partition-concurrency-code}

`ANALYZE`ステートメントを実行する場合、 [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)使用して、パーティションテーブルの統計の読み取りと書き込みの同時実行を制御できます。デフォルト値は`2`です。v7.4.0 以前のバージョンの場合、デフォルト値は`1`です。

#### <code>tidb_distsql_scan_concurrency</code> {#code-tidb-distsql-scan-concurrency-code}

通常の列を分析する場合、 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)変数を使用して、一度に読み取るリージョンの数を制御できます。デフォルト値は`15`です。値を変更するとクエリのパフォーマンスに影響することに注意してください。値を慎重に調整してください。

#### <code>tidb_index_serial_scan_concurrency</code> {#code-tidb-index-serial-scan-concurrency-code}

インデックス列を分析する場合、 [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)変数を使用して、一度に読み取るリージョンの数を制御できます。デフォルト値は`1`です。値を変更するとクエリのパフォーマンスに影響することに注意してください。値を慎重に調整してください。

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [ロード統計](/sql-statements/sql-statement-load-stats.md)
-   [ドロップ統計](/sql-statements/sql-statement-drop-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報のロックを解除](/sql-statements/sql-statement-unlock-stats.md)
-   [STATS_LOCKED を表示](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [ロード統計](/sql-statements/sql-statement-load-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報のロックを解除](/sql-statements/sql-statement-unlock-stats.md)
-   [STATS_LOCKED を表示](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>
