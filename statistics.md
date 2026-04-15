---
title: Introduction to Statistics
summary: 統計情報がテーブルレベルと列レベルの情報をどのように収集するのかを学びましょう。
---

# 統計入門 {#introduction-to-statistics}

TiDB は、統計情報をオプティマイザへの入力として使用し、SQL ステートメントの各プラン ステップで処理される行数を推定します。オプティマイザは、利用可能な各プランのコストを推定し、[インデックスアクセス](/choose-index.md)やテーブル結合の順序などを含め、利用可能な各プランのコストを算出します。その後、オプティマイザは、全体のコストが最も低い実行プランを選択します。

## 統計情報を収集する {#collect-statistics}

このセクションでは、統計情報を収集する2つの方法、すなわち自動更新と手動収集について説明します。

### 自動更新 {#automatic-update}

[`INSERT`](/sql-statements/sql-statement-insert.md) 、 [`DELETE`](/sql-statements/sql-statement-delete.md) 、または[`UPDATE`](/sql-statements/sql-statement-update.md)文の場合、TiDBは統計情報内の行数と変更された行数を自動的に更新します。

<CustomContent platform="tidb">

TiDB は更新情報を定期的に保持し、更新サイクルは 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)です。 `stats-lease`のデフォルト値は`3s`です。値を`0`と指定すると、TiDB は統計情報の自動更新を停止します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDBは60秒ごとに更新情報を永続化します。

</CustomContent>

TiDBは、テーブルへの変更回数に基づいて、自動的に[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)を実行して該当テーブルの統計情報を収集します。これは、以下のシステム変数によって制御されます。

| システム変数                                                                                                                | デフォルト値         | 説明                                                                                                                                                                                |
| --------------------------------------------------------------------------------------------------------------------- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)                     | `1`            | TiDBクラスタ内における自動分析操作の並行処理。                                                                                                                                                         |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time)                                       | `23:59 +0000`  | TiDBが自動更新を実行できる1日の終了時刻。                                                                                                                                                           |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)   | `8192`         | TiDBがパーティションテーブルを分析する際（つまり、パーティションテーブルの統計情報を自動的に更新する際）に自動的に分析するパーティションの数。                                                                                                         |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)                                             | `0.5`          | 自動更新のしきい値。                                                                                                                                                                        |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time)                                   | `00:00 +0000`  | TiDBが自動更新を実行できる開始時刻（1日のうち）。                                                                                                                                                       |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                               | `ON`           | TiDB が`ANALYZE`を自動的に実行するかどうかを制御します。                                                                                                                                               |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | `ON`           | 統計情報の自動収集タスクをスケジュールするための優先度キューを有効にするかどうかを制御します。この変数を有効にすると、TiDB は、新しく作成されたインデックスやパーティションが変更されたパーティションテーブルなど、収集する価値の高いテーブルの統計情報の収集を優先します。さらに、TiDB は健全性スコアの低いテーブルを優先し、キューの先頭に配置します。 |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840)                                 | `ON`           | 対応するTiDBインスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                         |
| [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                           | `43200` （12時間） | 自動`ANALYZE`タスクの最大実行時間。単位は秒です。                                                                                                                                                     |

テーブル内の`tbl`の変更された行数と総行数の比率が`tidb_auto_analyze_ratio`より大きく、かつ現在時刻が`tidb_auto_analyze_start_time`と`tidb_auto_analyze_end_time`の間である場合、TiDB はバックグラウンドで`ANALYZE TABLE tbl`ステートメントを実行して、このテーブルの統計情報を自動的に更新します。

小さなテーブルのデータを変更すると、自動更新が頻繁にトリガーされる状況を避けるため、TiDB では、テーブルの行数が 1000 行未満の場合、変更によって自動更新がトリガーされません。テーブルの行数を確認するには、 `SHOW STATS_META`ステートメントを使用できます。

> **注記：**
>
> 現在、自動更新では`ANALYZE`で手動で入力された構成項目は記録されません。そのため、 [`WITH`](/sql-statements/sql-statement-analyze-table.md)構文を使用して`ANALYZE`の収集動作を制御する場合は、統計情報を収集するためのスケジュール済みタスクを手動で設定する必要があります。

### 手動収集 {#manual-collection}

現在、TiDB は統計情報を完全なコレクションとして収集します。統計情報を収集するには、 `ANALYZE TABLE`ステートメントを実行してください。

以下の構文を使用すると、完全なデータ収集を実行できます。

-   `TableNameList`内のすべてのテーブルの統計情報を収集するには：

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `WITH NUM BUCKETS`生成されるヒストグラムのバケットの最大数を指定します。

-   `WITH NUM TOPN`生成される`TOPN`の最大数を指定します。

-   `WITH NUM CMSKETCH DEPTH` CM スケッチの深さを指定します。

-   `WITH NUM CMSKETCH WIDTH` CM スケッチの幅を指定します。

-   `WITH NUM SAMPLES`サンプル数を指定します。

-   `WITH FLOAT_NUM SAMPLERATE`はサンプリングレートを指定します。

`WITH NUM SAMPLES`と`WITH FLOAT_NUM SAMPLERATE`は、サンプルを収集する2つの異なるアルゴリズムに対応しています。

詳細な説明については、[ヒストグラム](#histogram)、[トップN](#top-n) 、 [CMSketch](#count-min-sketch) (Count-Min Sketch) を参照してください。 `SAMPLES` / `SAMPLERATE`については、[収集パフォーマンスを向上させる](#improve-collection-performance)ください。

再利用を容易にするためにオプションを永続化する方法については、 [`ANALYZE`構成を永続化する](#persist-analyze-configurations)を参照してください。

## 統計の種類 {#types-of-statistics}

このセクションでは、ヒストグラム、カウントミニスケッチ、トップNという3種類の統計について説明します。

### ヒストグラム {#histogram}

ヒストグラム統計は、オプティマイザが区間または範囲述語の選択性を推定するために使用され、また、統計のバージョン 2 で等号/IN 述語を推定するために列内の異なる値の数を決定するためにも使用される場合があります (統計[統計のバージョン](#versions-of-statistics)を参照)。

ヒストグラムは、データの分布を近似的に表現したものです。値の全範囲を複数のバケットに分割し、各バケットに含まれる値の数など、単純なデータを用いて各バケットを記述します。TiDBでは、各テーブルの特定の列に対して等深ヒストグラムが作成されます。この等深ヒストグラムは、区間クエリの推定に利用できます。

ここで「等深」とは、各バケットに入る値の数が可能な限り均等になることを意味します。たとえば、与えられたセット {1.6, 1.9, 1.9, 2.0, 2.4, 2.6, 2.7, 2.7, 2.8, 2.9, 3.4, 3.5} に対して、4 つのバケットを生成したいとします。等深ヒストグラムは次のようになります。これには [1.6, 1.9]、[2.0, 2.6]、[2.7, 2.8]、[2.9, 3.5] の 4 つのバケットが含まれます。バケットの深さは 3 です。

![Equal-depth Histogram Example](/media/statistics-1.png)

ヒストグラムのバケット数の上限を決定するパラメータの詳細については[手動収集](#manual-collection)を参照してください。 バケット数が多いほどヒストグラムの精度は高くなりますが、精度が高いほどメモリリソースの使用量が増加します。実際の状況に応じて、この数値を適切に調整してください。

### カウントミニスケッチ {#count-min-sketch}

> **注記：**
>
> 統計バージョン1では、Count-Min Sketchは等号/IN述語選択性の推定にのみ使用されます。バージョン2では、後述するようにCount-Min Sketchの管理に課題があるため、代わりにヒストグラム統計が使用されます。

Count-Min Sketch はハッシュ構造です。 `a = 1`や`IN`クエリ (例えば`a IN (1, 2, 3)` ) のような等価性クエリを処理する際、TiDB はこのデータ構造を使用して推定を行います。

Count-Min Sketch はハッシュ構造であるため、ハッシュ衝突が発生する可能性があります。EXPLAIN [`EXPLAIN`](/sql-statements/sql-statement-explain.md)において、同等のクエリの推定値が実際の値から大きく乖離する場合、より大きな値とより小さな値がハッシュ化されているとみなすことができます。この場合、ハッシュ衝突を回避するために、以下のいずれかの方法を取ることができます。

-   `WITH NUM TOPN`パラメータを変更します。TiDB は、高頻度 (上位 x) のデータを別々に格納し、その他のデータは Count-Min Sketch に格納します。そのため、より大きな値とより小さな値が一緒にハッシュ化されるのを防ぐには、 `WITH NUM TOPN`の値を増やすことができます。TiDB では、デフォルト値は 20 です。最大値は 1024 です。このパラメータの詳細については、 を参照[手動収集](#manual-collection)てください。
-   `WITH NUM CMSKETCH DEPTH`と`WITH NUM CMSKETCH WIDTH`の 2 つのパラメータを変更します。どちらもハッシュ バケットの数と衝突確率に影響します。実際のシナリオに応じて 2 つのパラメータの値を適切に増やすことでハッシュ衝突の確率を減らすことができますが、統計情報のメモリ使用量が増加します。TiDB では、 `WITH NUM CMSKETCH DEPTH`のデフォルト値は 5、 `WITH NUM CMSKETCH WIDTH`のデフォルト値は 2048 です。2 つのパラメータの詳細については、 を参照[手動収集](#manual-collection)てください。

### トップN {#top-n}

トップN値とは、列またはインデックス内で出現頻度が最も高いN個の値のことです。トップN統計は、頻度統計またはデータスキューと呼ばれることもあります。

TiDB は上位 N 個の値とその出現回数を記録します。ここでは`N`は`WITH NUM TOPN`パラメータによって制御されます。デフォルト値は 20 で、これは最も頻繁に出現する上位 20 個の値が収集されることを意味します。最大値は 1024 です。パラメータの詳細については、 を参照[手動収集](#manual-collection)てください。

## 選択的統計収集 {#selective-statistics-collection}

このセクションでは、統計データを選択的に収集する方法について説明します。

### 指標に関する統計情報を収集する {#collect-statistics-on-indexes}

`IndexNameList` `TableName`内のすべてのインデックスに関する統計情報を収集するには、次の構文を使用します。

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

`IndexNameList`が空の場合、この構文は`TableName`内のすべてのインデックスに関する統計情報を収集します。

> **注記：**
>
> 収集の前後の統計情報が一貫していることを保証するために、 `tidb_analyze_version`が`2`の場合、この構文はインデックス付き列とすべてのインデックスに関する統計情報を収集します。

### いくつかの列の統計情報を収集する {#collect-statistics-on-some-columns}

TiDB が SQL ステートメントを実行する際、オプティマイザはほとんどの場合、一部の列のみの統計情報を使用します。たとえば、 `WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`句に現れる列などです。これらの列は述語列と呼ばれます。

テーブルに多数の列がある場合、すべての列の統計情報を収集すると、大きなオーバーヘッドが発生する可能性があります。オーバーヘッドを削減するには、オプティマイザで使用する特定の列（選択した列）または`PREDICATE COLUMNS`のみの統計情報を収集できます。列のサブセットの列リストを将来再利用するために保持するには、[列構成を保持する](#persist-column-configurations)参照してください。

> **注記：**
>
> -   述語列に関する統計情報の収集は、 [`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)の場合にのみ適用されます。
> -   TiDB v7.2.0 以降、TiDB では、統計情報を収集するために`ANALYZE`コマンドを実行する際に、統計収集からスキップされる列の種類を示すシステム変数[`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)が導入されました。このシステム変数は`tidb_analyze_version = 2`にのみ適用されます。

-   特定の列に関する統計情報を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    構文では、 `ColumnNameList`対象列の名前リストを指定します。複数の列を指定する必要がある場合は、列名をカンマ`,`で区切ります。たとえば、 `ANALYZE table t columns a, b`のように指定します。この構文では、特定のテーブルの特定の列に関する統計情報を収集するだけでなく、そのテーブルのインデックス付き列とすべてのインデックスに関する統計情報も同時に収集します。

-   `PREDICATE COLUMNS`に関する統計情報を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    <CustomContent platform="tidb">

    TiDB は常に`PREDICATE COLUMNS`情報を 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに[`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables)システム テーブルに書き込みます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    TiDB は常に`PREDICATE COLUMNS`情報を[`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables)システム テーブルに 300 秒ごとに書き込みます。

    </CustomContent>

    この構文は、特定のテーブル内の`PREDICATE COLUMNS`に関する統計情報を収集するだけでなく、そのテーブル内のインデックス付き列とすべてのインデックスに関する統計情報も同時に収集します。

    > **注記：**
    >
    > -   [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables)システム テーブルにそのテーブルに対して`PREDICATE COLUMNS`が記録されていない場合、上記の構文は、そのテーブルのインデックス付き列とすべてのインデックスに関する統計情報を収集します。
    > -   手動で列をリストアップするか、 `PREDICATE COLUMNS`を使用して収集対象から除外した列の統計情報は上書きされません。新しいタイプの SQL クエリを実行すると、オプティマイザは、そのような列に古い統計情報が存在する場合はそれを使用し、統計情報が収集されたことがない列の場合は擬似列統計情報を使用します。 `PREDICATE COLUMNS`を使用した次の ANALYZE で、これらの列の統計情報が収集されます。

-   すべての列とインデックスに関する統計情報を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

### パーティションに関する統計情報を収集する {#collect-statistics-on-partitions}

-   `PartitionNameList`内の`TableName`内のすべてのパーティションに関する統計情報を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `PartitionNameList` `TableName`のすべてのパーティションのインデックス統計情報を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   テーブル内のいくつかのパーティションの[いくつかの列の統計情報を収集する](/statistics.md#collect-statistics-on-some-columns)必要がある場合は、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

#### 動的プルーニングモードでパーティションテーブルの統計情報を収集する {#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

TiDB は、パーティション分割されたテーブルに、パーティション [動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)(v6.3.0 以降はデフォルト) でアクセスする場合、テーブルレベルの統計情報、つまりパーティション分割されたテーブルのグローバル統計情報を収集します。現在、グローバル統計情報は、すべてのパーティションの統計情報を集計したものです。動的プルーニングモードでは、テーブルのいずれかのパーティションの統計情報が更新されると、そのテーブルのグローバル統計情報も更新される可能性があります。

一部のパーティションの統計情報が空の場合、または一部のパーティションで一部の列の統計情報が欠落している場合、収集動作は[`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)変数によって制御されます。

-   グローバル統計の更新がトリガーされ、 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)が`OFF`の場合：

    -   一部のパーティションに統計情報がない場合（例えば、これまで分析されたことのない新しいパーティションなど）、グローバル統計情報の生成は中断され、パーティションに統計情報が存在しないことを示す警告メッセージが表示されます。

    -   特定のパーティションで一部の列の統計情報が存在しない場合（これらのパーティションでは、分析対象として異なる列が指定されています）、これらの列の統計情報が集計される際にグローバル統計情報の生成が中断され、特定のパーティションで一部の列の統計情報が存在しないことを示す警告メッセージが表示されます。

-   グローバル統計の更新がトリガーされ、 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)が`ON`の場合：

    -   一部のパーティションで、すべての列または一部の列の統計情報が欠落している場合、TiDB はグローバル統計情報の生成時にこれらの欠落したパーティション統計情報をスキップするため、グローバル統計情報の生成には影響しません。

動的プルーニングモードでは、パーティションとテーブルの`ANALYZE`構成は同じである必要があります。したがって、 `COLUMNS`ステートメントの後に`ANALYZE TABLE TableName PARTITION PartitionNameList` }構成を指定した場合、または`OPTIONS`の後に`WITH` }構成を指定した場合、TiDBはそれらを無視して警告を返します。

## 収集パフォーマンスを向上させる {#improve-collection-performance}

> **注記：**
>
> -   TiDB での`ANALYZE TABLE`の実行時間は、MySQL や InnoDB よりも長くなる可能性があります。InnoDB では少数のページのみがサンプリングされますが、TiDB ではデフォルトで包括的な統計情報が完全に再構築されます。

TiDBは、統計情報の収集パフォーマンスを向上させるための2つのオプションを提供します。

-   列のサブセットに関する統計を収集します。[いくつかの列に関する統計情報を収集する](#collect-statistics-on-some-columns)ご覧ください。
-   サンプリング。

### 統計サンプリング {#statistics-sampling}

サンプリングは`ANALYZE`ステートメントの 2 つのオプションで利用可能であり、それぞれ異なる収集アルゴリズムに対応しています。

-   `WITH NUM SAMPLES` TiDB のリザーバーサンプリング方式で実装されているサンプリングセットのサイズを指定します。テーブルが大きい場合、この方式を使用して統計情報を収集することは推奨されません。リザーバーサンプリングの中間結果セットには冗長な結果が含まれるため、メモリなどのリソースに余分な負荷がかかります。
-   `WITH FLOAT_NUM SAMPLERATE`は、v5.3.0 で導入されたサンプリング方法です。値の範囲`(0, 1]`を指定することで、サンプリングレートを設定できます。TiDB ではベルヌーイサンプリング方式で実装されており、大規模なテーブルのサンプリングに適しており、収集効率とリソース使用量の面で優れたパフォーマンスを発揮します。

バージョン5.3.0より前は、TiDBはリザーバーサンプリング方式を使用して統計情報を収集していました。バージョン5.3.0以降、TiDBバージョン2の統計情報は、デフォルトでベルヌーイサンプリング方式を使用して統計情報を収集します。リザーバーサンプリング方式を再利用するには、 `WITH NUM SAMPLES`ステートメントを使用できます。

現在のサンプリングレートは、適応アルゴリズムに基づいて計算されます。SHOW [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)を使用してテーブルの行数を確認できる場合は、その行数を使用して 100,000 行に対応するサンプリングレートを計算できます。この行数を確認できない場合は、テーブルの[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)の結果にある`APPROXIMATE_KEYS`列のすべての値の合計を、サンプリングレートを計算するための別の参照値として使用できます。

> **注記：**
>
> 通常、 `STATS_META` `APPROXIMATE_KEYS`よりも信頼性が高いです。ただし、 `STATS_META`の結果が`APPROXIMATE_KEYS`の結果よりもはるかに小さい場合は、 `APPROXIMATE_KEYS`を使用してサンプリングレートを計算することをお勧めします。

### 統計情報を収集するためのメモリ割り当て {#the-memory-quota-for-collecting-statistics}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

TiDB v6.1.0以降では、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)を使用して、TiDBで統計情報を収集するためのメモリ割り当てを制御できます。

`tidb_mem_quota_analyze`の適切な値を設定するには、クラスタのデータサイズを考慮してください。デフォルトのサンプリングレートを使用する場合、主な考慮事項は、列数、列値のサイズ、および TiDB のメモリ構成です。最大値と最小値を設定する際には、次の提案を参考にしてください。

> **注記：**
>
> 以下の提案は参考情報です。実際の状況に基づいて値を設定する必要があります。

-   最小値：TiDBが列数が最も多いテーブルから統計情報を収集する際の最大メモリ使用量よりも大きくする必要があります。目安として、デフォルト設定で20列のテーブルから統計情報を収集する場合、最大メモリ使用量は約800 MiBです。また、デフォルト設定で160列のテーブルから統計情報を収集する場合、最大メモリ使用量は約5 GiBです。
-   最大値：TiDBが統計情報を収集していないときは、利用可能なメモリよりも小さくする必要があります。

## ANALYZE構成を永続化する {#persist-analyze-configurations}

バージョン5.4.0以降、TiDBは一部の`ANALYZE`設定の永続化をサポートしています。この機能により、既存の設定を今後の統計情報収集に簡単に再利用できます。

永続性をサポートする`ANALYZE`構成は以下のとおりです。

| 設定            | 対応するANALYZE構文                                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------ |
| ヒストグラムのバケット数  | `WITH NUM BUCKETS`                                                                                                 |
| トップNの数        | `WITH NUM TOPN`                                                                                                    |
| サンプル数         | `WITH NUM SAMPLES`                                                                                                 |
| サンプリングレート     | `WITH FLOATNUM SAMPLERATE`                                                                                         |
| `ANALYZE`列タイプ | AnalyzeColumnOption ::= ( &#39;ALL COLUMNS&#39; | &#39;PREDICATE COLUMNS&#39; | &#39;COLUMNS&#39; ColumnNameList ) |
| `ANALYZE`列    | ColumnNameList ::= Identifier ( &#39;,&#39; Identifier )*                                                          |

### ANALYZE構成の永続性を有効にする {#enable-analyze-configuration-persistence}

<CustomContent platform="tidb">

`ANALYZE`構成永続化機能はデフォルトで有効になっています (システム変数`tidb_analyze_version`はデフォルトで`2`であり、 `tidb_persist_analyze_options`はデフォルトで`ON`です)。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ANALYZE`構成永続化機能は、デフォルトでは無効になっています。この機能を有効にするには、システム変数`tidb_persist_analyze_options`が`ON`であることを確認し、システム変数`tidb_analyze_version`を`2`に設定してください。

</CustomContent>

この機能を使用すると、 `ANALYZE`ステートメントを手動で実行する際に、そのステートメントで指定された永続化構成を記録できます。一度記録すると、次回 TiDB が統計情報を自動的に更新する場合、またはこれらの構成を指定せずに手動で統計情報を収集する場合、TiDB は記録された構成に従って統計情報を収集します。

auto analyze操作に使用される特定のテーブルに保持されている構成を照会するには、次の SQL ステートメントを使用できます。

```sql
SELECT sample_num, sample_rate, buckets, topn, column_choice, column_ids FROM mysql.analyze_options opt JOIN information_schema.tables tbl ON opt.table_id = tbl.tidb_table_id WHERE tbl.table_schema = '{db_name}' AND tbl.table_name = '{table_name}';
```

TiDB は、最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続構成を上書きします。たとえば、 `ANALYZE TABLE t WITH 200 TOPN;`実行すると、 `ANALYZE`ステートメントの上位 200 個の値が設定されます。その後、 `ANALYZE TABLE t WITH 0.1 SAMPLERATE;`を実行すると、 `ANALYZE`と同様に、自動`ANALYZE TABLE t WITH 200 TOPN, 0.1 SAMPLERATE;` 。

### ANALYZE構成の永続化を無効にする {#disable-analyze-configuration-persistence}

`ANALYZE`構成永続化機能を無効にするには、 `tidb_persist_analyze_options`システム変数を`OFF`に設定します。 `ANALYZE`構成永続化機能は`tidb_analyze_version = 1`には適用されないため、 `tidb_analyze_version = 1`を設定することでもこの機能を無効にできます。

`ANALYZE`構成永続化機能を無効にした後も、TiDBは永続化された構成レコードをクリアしません。そのため、この機能を再度有効にすると、TiDBは以前に記録された永続化構成を使用して統計情報の収集を継続します。

> **注記：**
>
> `ANALYZE`構成永続化機能を再度有効にする場合、以前に記録された永続化構成が最新のデータに適用できなくなった場合は、 `ANALYZE`ステートメントを手動で実行し、新しい永続化構成を指定する必要があります。

### 列構成を保持する {#persist-column-configurations}

`ANALYZE`ステートメント ( `COLUMNS ColumnNameList` 、{{B-PLACEHOLDER-2-PLACEHOLDER- `PREDICATE COLUMNS`を含む) の列構成を永続化する場合は、 `tidb_persist_analyze_options` `ALL COLUMNS`変数の値を`ON`に設定して[構成の永続性を分析する](#persist-analyze-configurations)機能を有効にします。 ANALYZE 構成永続化機能を有効にした後:

-   TiDB が統計情報を自動的に収集する場合、または列構成を指定せずに`ANALYZE`ステートメントを実行して手動で統計情報を収集する場合、TiDB は統計情報の収集に以前に保持された構成を引き続き使用します。
-   列構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDB は最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続構成を上書きします。

`PREDICATE COLUMNS`および統計情報が収集された列を特定するには、 [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md)ステートメントを使用します。

次の例では、 `ANALYZE TABLE t PREDICATE COLUMNS;`を実行した後、TiDB は列`b` 、 `c` 、および`d`の統計情報を収集します。ここで、列`b`は`PREDICATE COLUMN`であり、列`c`および`d`はインデックス列です。

```sql
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

> **警告：**
>
> v8.5.6 以降、統計バージョン 1 ( `tidb_analyze_version = 1` ) は非推奨となり、将来のリリースでは削除される予定です。統計バージョン 2 ( `tidb_analyze_version = 2` ) および[統計バージョン1を使用している既存のオブジェクトをバージョン2に移行する](#switch-between-statistics-versions)ことをお勧めします。

[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)変数は、TiDB によって収集される統計情報を制御します。現在、TiDB は`tidb_analyze_version = 1`と`tidb_analyze_version = 2` 2 つの統計バージョンをサポートしています。

-   TiDB Self-Managedの場合、v5.3.0以降、この変数のデフォルト値が`1`から`2`に変更されます。
-   TiDB Cloudの場合、v6.5.0 以降、この変数のデフォルト値が`1`から`2`に変更されます。
-   クラスターを以前のバージョンからアップグレードした場合、 `tidb_analyze_version`のデフォルト値はアップグレード後も変更されません。

バージョン2は推奨される統計バージョンです。バージョン1と比較して、バージョン2ではデータ量が多い場合の多くの統計情報の精度が向上しています。また、バージョン2ではCount-Minスケッチ統計情報を収集する必要がなくなったため、収集パフォーマンスも向上しています。

以下の表は、最適化推定に使用するために各バージョンで収集された情報の一覧です。

| 情報         | バージョン1                     | バージョン2                   |
| ---------- | -------------------------- | ------------------------ |
| テーブル内の行の総数 | ⎷                          | ⎷                        |
| 等しい/IN述語推定 | ⎷（カラム／インデックス上位N件と最小件数スケッチ） | ⎷（カラム／インデックス上位N件とヒストグラム） |
| 範囲述語推定     | ⎷（カラム／インデックス上位N件とヒストグラム）   | ⎷（カラム／インデックス上位N件とヒストグラム） |
| `NULL`述語推定 | ⎷                          | ⎷                        |
| 列の平均長さ     | ⎷                          | ⎷                        |
| インデックスの平均長 | ⎷                          | ⎷                        |

### 統計バージョンの切り替え {#switch-between-statistics-versions}

すべてのテーブル、インデックス、パーティションで同じ統計バージョンを使用することをお勧めします。クラスタでまだ統計バージョン1を使用している場合は、できるだけ早く統計バージョン2に移行してください。テーブル、インデックス、パーティションなどのオブジェクトに対してバージョン2の統計が収集されるまで、TiDBはそのオブジェクトに対して既存のバージョン1の統計を引き続き使用します。

移行の主な理由の1つは、Count-Min Sketchでハッシュ衝突が発生する可能性があるため、バージョン1ではequal/IN述語の推定値が不正確になる可能性があることです。詳細については、[カウントミニスケッチ](#count-min-sketch)参照してください。この問題を回避するには、 `tidb_analyze_version = 2`を設定し、すべてのオブジェクトで`ANALYZE`を再実行してください。

統計バージョン1から統計バージョン2への移行準備として、 `ANALYZE`を準備します。

-   `ANALYZE`ステートメントを手動で実行する場合は、分析対象のすべてのテーブルを手動で分析します。

    ```sql
    SELECT DISTINCT(CONCAT('ANALYZE TABLE ', table_schema, '.', table_name, ';'))
    FROM information_schema.tables JOIN mysql.stats_histograms
    ON table_id = tidb_table_id
    WHERE stats_ver = 1;
    ```

-   自動分析が有効になっているため、TiDB が`ANALYZE`ステートメントを自動的に実行する場合、 `tidb_analyze_version = 2`を設定すると、TiDB は後続の自動分析を通じて統計情報をバージョン 2 に徐々に更新します。オブジェクトに対してバージョン 2 の統計情報が収集されるまでは、TiDB は既存のバージョン 1 の統計情報を引き続き使用できます。重要なオブジェクトの移行を高速化するには、それらのオブジェクトに対して`ANALYZE`を手動で実行してください。

-   前述のステートメントの結果が長すぎてコピー＆ペーストできない場合は、結果を一時的なテキストファイルにエクスポートし、そのファイルから次のように実行できます。

    ```sql
    SELECT DISTINCT ... INTO OUTFILE '/tmp/sql.txt';
    mysql -h ${TiDB_IP} -u user -P ${TIDB_PORT} ... < '/tmp/sql.txt'
    ```

## 統計情報をビュー {#view-statistics}

`ANALYZE`の状態と統計情報は、以下のステートメントを使用して表示できます。

### 状態<code>ANALYZE</code> {#code-analyze-code-state}

`ANALYZE`ステートメントを実行すると、 [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)を使用して`ANALYZE`の現在の状態を表示できます。

TiDB v6.1.0 以降では、 `SHOW ANALYZE STATUS`ステートメントでクラスタレベルのタスクを表示できるようになりました。TiDB を再起動した後でも、このステートメントを使用すれば再起動前のタスクレコードを表示できます。TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントではインスタンスレベルのタスクしか表示できず、TiDB の再起動後にタスクレコードはクリアされていました。

`SHOW ANALYZE STATUS`には、最新のタスク記録のみが表示されます。TiDB v6.1.0 以降では、システムテーブル`mysql.analyze_jobs`を通じて、過去 7 日間の履歴タスクを表示できます。

[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)が設定されていて、TiDB のバックグラウンドで実行されている自動タスク`ANALYZE`このしきい値を超えるメモリを使用している場合、タスクは再試行されます。失敗したタスクと再試行されたタスクは`SHOW ANALYZE STATUS`ステートメントの出力で確認できます。

[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)が 0 より大きく、TiDB のバックグラウンドで実行されている自動`ANALYZE`タスクがこのしきい値を超える時間がかかった場合、タスクは終了します。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

### テーブルのメタデータ {#metadata-of-tables}

[`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)ステートメントを使用すると、行の総数と更新された行の数を表示できます。

### テーブルの健康状態 {#health-state-of-tables}

[`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを使用すると、テーブルの健全性状態を確認し、統計情報の精度を概算できます。 `modify_count` &gt;= `row_count`の場合、健全性状態は 0 です。 `modify_count` &lt; `row_count`の場合、健全性状態は (1 - `modify_count` / `row_count` ) * 100 です。

### 列のメタデータ {#metadata-of-columns}

[`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md)ステートメントを使用すると、すべての列における異なる値の数と`NULL`の数を表示できます。

### ヒストグラムのバケット {#buckets-of-histogram}

[`SHOW STATS_BUCKETS`](/sql-statements/sql-statement-show-stats-buckets.md)ステートメントを使用すると、ヒストグラムの各バケットを表示できます。

### トップN情報 {#top-n-information}

[`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md)ステートメントを使用すると、TiDB が現在収集しているトップ N 情報を表示できます。

## 統計情報を削除する {#delete-statistics}

統計情報を削除するには、[`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)ステートメントを実行します。

## 負荷統計 {#load-statistics}

> **注記：**
>
> [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスでは、ロード統計情報は利用できません。

デフォルトでは、列統計のサイズに応じて、TiDB は次のように異なる方法で統計情報をロードします。

-   メモリ使用量が少ない統計情報（count、distinctCount、nullCountなど）については、列データが更新される限り、TiDBは対応する統計情報を自動的にメモリにロードし、SQL最適化段階で使用します。
-   メモリを大量に消費する統計情報（ヒストグラム、TopN、Count-Min Sketchなど）については、SQL実行のパフォーマンスを確保するため、TiDBは必要に応じて非同期で統計情報をロードします。ヒストグラムを例にとると、TiDBはオプティマイザがその列のヒストグラム統計情報を使用する場合にのみ、その列のヒストグラム統計情報をメモリにロードします。オンデマンドの非同期統計情報ロードはSQL実行のパフォーマンスには影響しませんが、SQL最適化に必要な統計情報が不完全になる可能性があります。

TiDBはバージョン5.4.0以降、統計情報の同期読み込み機能を導入しました。この機能により、SQL文の実行時に、ヒストグラム、TopN、Count-Min Sketch統計情報などの大規模な統計情報をメモリに同期的に読み込むことが可能になり、SQL最適化のための統計情報の網羅性が向上します。

この機能を有効にするには、 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)システム変数の値を、SQL 最適化が完全な列統計情報を同期的にロードするために待機できる最大時間 (ミリ秒単位) に設定します。この変数のデフォルト値は`100`で、この機能が有効になっていることを示します。

<CustomContent platform="tidb">

同期的に統計情報を読み込む機能を有効にした後、以下のようにさらに設定を行うことができます。

-   SQL最適化の待機時間がタイムアウトに達したときのTiDBの動作を制御するには、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更します。この変数のデフォルト値は`ON`で、タイムアウト後、SQL最適化プロセスではどの列に対してもヒストグラム、TopN、またはCMSketch統計情報を使用しないことを示します。この変数を`OFF`に設定すると、タイムアウト後にSQLの実行が失敗します。
-   同期的に統計情報をロードする機能が同時に処理できる列の最大数を指定するには、TiDB 設定ファイルの[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)オプションの値を変更します。v8.2.0 以降、このオプションのデフォルト値は`0`であり、これは TiDB がサーバー構成に基づいて同時実行数を自動的に調整することを示しています。
-   同期的に統計情報をロードする機能がキャッシュできる列リクエストの最大数を指定するには、TiDB 設定ファイルの[`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)オプションの値を変更します。デフォルト値は`1000`です。

TiDBの起動時、初期統計情報が完全にロードされる前に実行されるSQL文は、最適とは言えない実行プランとなり、パフォーマンスの問題を引き起こす可能性があります。このような問題を回避するため、TiDB v7.1.0では設定パラメータ[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が導入されました。このオプションを使用すると、起動時に統計情報の初期化が完了した後にのみTiDBがサービスを提供するかどうかを制御できます。v7.2.0以降、このパラメータはデフォルトで有効になっています。

バージョン7.1.0以降、TiDBは軽量な統計情報初期化のための[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)を導入しました。

-   `lite-init-stats`の値が`true`の場合、統計初期化では、インデックスまたは列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。
-   `lite-init-stats`の値が`false`の場合、統計情報の初期化では、インデックスと主キーのヒストグラム、TopN、および Count-Min Sketch がメモリにロードされますが、主キー以外の列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。オプティマイザが特定のインデックスまたは列のヒストグラム、TopN、および Count-Min Sketch を必要とする場合、必要な統計情報が同期または非同期でメモリにロードされます。

`lite-init-stats`のデフォルト値は`true`で、これは軽量統計初期化を有効にすることを意味します。 `lite-init-stats`を`true`に設定すると、不要な統計の読み込みを回避することで、統計初期化が高速化され、TiDB のメモリ使用量が削減されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

同期的に統計情報を読み込む機能を有効にした後、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更することで、SQL 最適化の待機時間がタイムアウトに達したときの TiDB の動作を制御できます。この変数のデフォルト値は`ON`で、タイムアウト後には、SQL 最適化プロセスでどの列に対してもヒストグラム、TopN、または CMSketch 統計情報が使用されないことを示しています。この変数を`OFF`に設定すると、タイムアウト後に SQL の実行が失敗します。

</CustomContent>

## 輸出入統計 {#export-and-import-statistics}

このセクションでは、統計情報のエクスポートとインポートの方法について説明します。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

### 輸出統計 {#export-statistics}

統計情報をエクスポートするためのインターフェースは以下のとおりです。

-   `${table_name}`データベース内の`${db_name}`テーブルの JSON 形式の統計情報を取得するには：

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}

    例えば：

    ```shell
    curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json
    ```

-   `${table_name}` `${db_name}`テーブルの特定の時刻における JSON 形式の統計情報を取得するには：

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}

### 輸入統計 {#import-statistics}

> **注記：**
>
> MySQLクライアントを起動する際には、 `--local-infile=1`オプションを使用してください。

一般的に、インポートされる統計情報は、エクスポートインターフェースを使用して取得したJSONファイルを指します。

統計情報の読み込みは[`LOAD STATS`](/sql-statements/sql-statement-load-stats.md)ステートメントを使用して行うことができます。

例えば：

```sql
LOAD STATS 'file_name';
```

`file_name`は、インポートする統計データのファイル名です。

## ロック統計 {#lock-statistics}

TiDBはv6.5.0以降、統計情報のロックをサポートしています。テーブルまたはパーティションの統計情報がロックされると、テーブルの統計情報を変更したり、 `ANALYZE`ステートメントをテーブル上で実行したりすることはできません。例：

テーブル`t`を作成し、データを挿入します。テーブル`t`の統計情報がロックされていない場合、 `ANALYZE`ステートメントを正常に実行できます。

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

テーブル`t`の統計情報をロックし、 `ANALYZE`を実行します。警告メッセージには、 `ANALYZE`ステートメントがテーブル`t`をスキップしたことが示されています。

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

テーブル`t`と`ANALYZE`の統計情報をロック解除して、再度実行できます。

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

さらに、[`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)を使用してパーティションの統計情報をロックすることもできます。例:

パーティションテーブル`t`を作成し、そこにデータを挿入します。パーティション`p1`の統計情報がロックされていない場合、 `ANALYZE`ステートメントを正常に実行できます。

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

パーティション`p1`の統計情報をロックし、 `ANALYZE`を実行します。警告メッセージには、 `ANALYZE`ステートメントがパーティション`p1`をスキップしたことが示されています。

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

### ロック統計の挙動 {#behaviors-of-locking-statistics}

-   パーティションテーブルの統計情報をロックすると、そのパーティションテーブル上のすべてのパーティションの統計情報がロックされます。
-   テーブルまたはパーティションを切り捨てると、そのテーブルまたはパーティションにかかっていた統計ロックが解除されます。

以下の表は、ロック統計の動作について説明しています。

|                                     | テーブル全体を削除します | テーブル全体を切り捨てる                               | パーティションを切り詰める                                | 新しいパーティションを作成する        | パーティションを削除する                                     | パーティションを再編成する                                    | パーティションを交換する                              |
| ----------------------------------- | ------------ | ------------------------------------------ | -------------------------------------------- | ---------------------- | ------------------------------------------------ | ------------------------------------------------ | ----------------------------------------- |
| パーティションテーブルがロックされています               | ロックが無効です     | TiDBが古いテーブルを削除するため、ロック情報も削除され、ロックは無効になります。 | /                                            | /                      | /                                                | /                                                | /                                         |
| パーティションテーブルと、テーブル全体がロックされています       | ロックが無効です     | TiDBが古いテーブルを削除するため、ロック情報も削除され、ロックは無効になります。 | 古いパーティションロック情報は無効であり、新しいパーティションは自動的にロックされます。 | 新しいパーティションは自動的にロックされます | 削除されたパーティションのロック情報はクリアされ、テーブル全体のロックは引き続き有効になります。 | 削除されたパーティションのロック情報がクリアされ、新しいパーティションが自動的にロックされます。 | ロック情報は交換テーブルに転送され、新しいパーティションは自動的にロックされます。 |
| パーティションテーブルで、一部のパーティションのみがロックされている。 | ロックが無効です     | TiDBが古いテーブルを削除するため、ロック情報も削除され、ロックは無効になります。 | TiDBが古いテーブルを削除するため、ロック情報も削除され、ロックは無効になります。   | /                      | 削除されたパーティションロック情報はクリアされます                        | 削除されたパーティションロック情報はクリアされます                        | ロック情報は交換テーブルに転送されます                       |

## <code>ANALYZE</code>タスクと並行処理を管理する {#manage-code-analyze-code-tasks-and-concurrency}

このセクションでは、バックグラウンド`ANALYZE`タスクを終了し、 `ANALYZE`の同時実行を制御する方法について説明します。

### バックグラウンドの<code>ANALYZE</code>タスクを終了します {#terminate-background-code-analyze-code-tasks}

TiDB v6.0以降、TiDBは`KILL`ステートメントを使用して、バックグラウンドで実行中の`ANALYZE`タスクを終了することをサポートしています。バックグラウンドで実行中の`ANALYZE`タスクが多くのリソースを消費し、アプリケーションに影響を与えている場合は、次の手順で`ANALYZE`タスクを終了できます。

1.  以下のSQL文を実行してください。

    ```sql
    SHOW ANALYZE STATUS
    ```

    結果の`instance`列と`process_id`列を確認することで、TiDB インスタンス アドレスと、バックグラウンド`ID`タスクのタスク`ANALYZE`を取得できます。

2.  バックグラウンドで実行されている`ANALYZE`タスクを終了します。

    <CustomContent platform="tidb">

    -   [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が`true` (デフォルトでは`true` ) の場合、 `KILL TIDB ${id};`ステートメントを直接実行できます。ここで、 `${id}`は、前の手順で取得したバックグラウンド`ID`タスクの`ANALYZE`です。
    -   `enable-global-kill`が`false`の場合、クライアントを使用してバックエンドの`ANALYZE`タスクを実行している TiDB インスタンスに接続し、 `KILL TIDB ${id};`ステートメントを実行する必要があります。クライアントを使用して別の TiDB インスタンスに接続する場合、またはクライアントと TiDB クラスタの間にプロキシがある場合、 `KILL`ステートメントではバックグラウンド`ANALYZE`タスクを終了できません。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    `ANALYZE`タスクを終了するには、 `KILL TIDB ${id};`ステートメントを実行します。ここで、 `${id}`は、前の手順で取得したバックグラウンド`ID`タスクの`ANALYZE`です。

    </CustomContent>

`KILL`ステートメントの詳細については、[`KILL`](/sql-statements/sql-statement-kill.md)参照してください。

### 制御<code>ANALYZE</code>並行性 {#control-code-analyze-code-concurrency}

`ANALYZE`ステートメントを実行すると、システム変数を使用して同時実行性を調整し、システムへの影響を制御できます。

関連するシステム変数間の関係を以下に示します。

![analyze\_concurrency](/media/analyze_concurrency.png)

`tidb_build_stats_concurrency` 、 `tidb_build_sampling_stats_concurrency` 、および`tidb_analyze_partition_concurrency`は、前述の図に示すように、上流-下流の関係にあります。実際の合計同時実行数は、 `tidb_build_stats_concurrency` * ( `tidb_build_sampling_stats_concurrency` + `tidb_analyze_partition_concurrency` ) です。これらの変数を変更する場合は、それぞれの値を同時に考慮する必要があります。 `tidb_analyze_partition_concurrency` 、 `tidb_build_sampling_stats_concurrency` 、 `tidb_build_stats_concurrency`の順に1つずつ調整し、システムへの影響を確認することをお勧めします。これら3つの変数の値が大きいほど、システムのリソースオーバーヘッドが大きくなります。

#### <code>tidb_build_stats_concurrency</code> {#code-tidb-build-stats-concurrency-code}

`ANALYZE`ステートメントを実行すると、タスクは複数の小さなタスクに分割されます。各タスクは、1 つの列またはインデックスの統計情報のみを処理します。tidb_build_stats_concurrency 変数を使用して、同時実行される小さなタスクの数を制御できます。 [`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)値は`2`です。v7.4.0 以前のバージョンでは、デフォルト値は`4`です。

#### <code>tidb_build_sampling_stats_concurrency</code> {#code-tidb-build-sampling-stats-concurrency-code}

通常の列を分析する場合、 [`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)を使用して、サンプリング タスクの実行の同時実行を制御できます。デフォルト値は`2`です。

#### <code>tidb_analyze_partition_concurrency</code> {#code-tidb-analyze-partition-concurrency-code}

`ANALYZE`ステートメントを実行する際に、 [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)を使用して、パーティションテーブルの統計情報の読み取りと書き込みの同時実行を制御できます。デフォルト値は`2`です。v7.4.0 以前のバージョンでは、デフォルト値は`1`です。

#### <code>tidb_distsql_scan_concurrency</code> {#code-tidb-distsql-scan-concurrency-code}

通常の列を分析する場合、 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)変数を使用して、一度に読み込むリージョンの数を制御できます。デフォルト値は`15`です。値を変更するとクエリのパフォーマンスに影響するため、慎重に調整してください。

#### <code>tidb_index_serial_scan_concurrency</code> {#code-tidb-index-serial-scan-concurrency-code}

インデックス列を分析する際、 [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)変数を使用して、一度に読み込むリージョンの数を制御できます。デフォルト値は`1`です。この値を変更するとクエリのパフォーマンスに影響するため、慎重に調整してください。

## 関連項目 {#see-also}

<CustomContent platform="tidb">

-   [ロード統計](/sql-statements/sql-statement-load-stats.md)
-   [ドロップ統計](/sql-statements/sql-statement-drop-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報をアンロックする](/sql-statements/sql-statement-unlock-stats.md)
-   [統計情報ロックを表示](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [ロード統計](/sql-statements/sql-statement-load-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報をアンロックする](/sql-statements/sql-statement-unlock-stats.md)
-   [統計情報ロックを表示](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>
