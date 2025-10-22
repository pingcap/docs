---
title: Introduction to Statistics
summary: 統計がテーブルレベルおよび列レベルの情報を収集する方法を学習します。
---

# 統計入門 {#introduction-to-statistics}

TiDBは、統計情報をオプティマイザへの入力として使用し、SQL文の各プランステップで処理される行数を推定します。オプティマイザは、利用可能な各プランのコスト（ [インデックスアクセス](/choose-index.md)とテーブル結合の順序を含む）を推定し、利用可能な各プランのコストを生成します。そして、全体的なコストが最も低い実行プランを選択します。

## 統計を収集する {#collect-statistics}

このセクションでは、統計を収集する 2 つの方法 (自動更新と手動収集) について説明します。

### 自動更新 {#automatic-update}

[`INSERT`](/sql-statements/sql-statement-insert.md) 、 [`DELETE`](/sql-statements/sql-statement-delete.md) 、または[`UPDATE`](/sql-statements/sql-statement-update.md)ステートメントの場合、TiDB は統計内の行数と変更された行数を自動的に更新します。

<CustomContent platform="tidb">

TiDBは更新情報を定期的に保持し、更新サイクルは20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)です。デフォルト値は`stats-lease`ですが、 `3s`です。値を`0`に指定すると、TiDBは統計情報の更新を自動的に停止します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB は 60 秒ごとに更新情報を保持します。

</CustomContent>

テーブルへの変更回数に基づいて、TiDBは自動的にそのテーブルの統計情報を収集する[`ANALYZE`](/sql-statements/sql-statement-analyze-table.md)を設定します。これは以下のシステム変数によって制御されます。

| システム変数                                                                                                                | デフォルト値         | 説明                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-new-in-v840)                     | `1`            | TiDB クラスター内の自動分析操作の同時実行性。                                                                                                                                                     |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time)                                       | `23:59 +0000`  | TiDB が自動更新を実行できる 1 日の終了時刻。                                                                                                                                                    |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)   | `8192`         | パーティションテーブルを分析するときに TiDB が自動的に分析するパーティションの数 (つまり、パーティションテーブルの統計を自動的に更新するときに)。                                                                                                 |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)                                             | `0.5`          | 自動更新のしきい値。                                                                                                                                                                    |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time)                                   | `00:00 +0000`  | TiDB が自動更新を実行できる 1 日の開始時刻。                                                                                                                                                    |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                               | `ON`           | TiDB が`ANALYZE`自動的に実行するかどうかを制御します。                                                                                                                                            |
| [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-new-in-v800) | `ON`           | 優先キューを有効にして、統計情報の自動収集タスクをスケジュールするかどうかを制御します。この変数を有効にすると、TiDBは、新しく作成されたインデックスやパーティションが変更されたパーティションテーブルなど、収集する価値の高いテーブルの統計情報を優先的に収集します。さらに、TiDBはヘルススコアが低いテーブルを優先し、キューの先頭に配置します。 |
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-new-in-v840)                                 | `ON`           | 対応する TiDB インスタンスが自動統計更新タスクを実行できるかどうかを制御します。                                                                                                                                   |
| [`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                           | `43200` (12時間) | 自動タスク`ANALYZE`の最大実行時間。単位は秒です。                                                                                                                                                 |

テーブル内の変更された行数と`tbl`の行の合計数の比率が`tidb_auto_analyze_ratio`より大きく、現在の時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`間である場合、TiDB はバックグラウンドで`ANALYZE TABLE tbl`ステートメントを実行し、このテーブルの統計を自動的に更新します。

小さなテーブルのデータ変更が頻繁に自動更新をトリガーする状況を回避するため、テーブルの行数が1000行未満の場合は、TiDBでは変更によって自動更新がトリガーされません。テーブルの行数を確認するには、 `SHOW STATS_META`ステートメントを使用します。

> **注記：**
>
> 現在、自動更新では、手動`ANALYZE`で入力された設定項目は記録されません。そのため、 [`WITH`](/sql-statements/sql-statement-analyze-table.md)構文を使用して`ANALYZE`の収集動作を制御する場合は、統計情報を収集するためのスケジュールタスクを手動で設定する必要があります。

### 手動収集 {#manual-collection}

現在、TiDBは完全なコレクションとして統計を収集します。統計を収集するには、 `ANALYZE TABLE`ステートメントを実行できます。

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

`WITH NUM SAMPLES`と`WITH FLOAT_NUM SAMPLERATE` 、サンプルを収集する 2 つの異なるアルゴリズムに対応します。

詳細な説明については`SAMPLERATE` [ヒストグラム](#histogram) （カウント・ミニマムスケッチ） [トップN](#top-n)参照してください。7/ `SAMPLES`については、 [収集パフォーマンスの向上](#improve-collection-performance) [CMSketch](#count-min-sketch)してください。

オプションを永続化して再利用しやすくする方法については、 [`ANALYZE`構成を保持する](#persist-analyze-configurations)参照してください。

## 統計の種類 {#types-of-statistics}

このセクションでは、ヒストグラム、Count-Min Sketch、Top-N の 3 種類の統計について説明します。

### ヒストグラム {#histogram}

ヒストグラム統計は、間隔述語または範囲述語の選択性を推定するためにオプティマイザーによって使用されます。また、統計バージョン 2 の等号/IN 述語の推定のために、列内の個別値の数を決定するために使用される場合もあります ( [統計のバージョン](#versions-of-statistics)を参照)。

ヒストグラムは、データの分布を大まかに表すものです。値の範囲全体を一連のバケットに分割し、各バケットに含まれる値の数などの単純なデータを使用して各バケットを説明します。TiDBでは、各テーブルの特定の列に対して等深度ヒストグラムが作成されます。等深度ヒストグラムは、間隔クエリの推定に使用できます。

ここで「等深度」とは、各バケットに含まれる値の数が可能な限り均等になることを意味します。例えば、{1.6, 1.9, 1.9, 2.0, 2.4, 2.6, 2.7, 2.7, 2.8, 2.9, 3.4, 3.5}という集合に対して、4つのバケットを生成するとします。等深度ヒストグラムは以下のようになります。[1.6, 1.9]、[2.0, 2.6]、[2.7, 2.8]、[2.9, 3.5]という4つのバケットが含まれています。バケットの深度は3です。

![Equal-depth Histogram Example](/media/statistics-1.png)

ヒストグラムのバケット数の上限を決定するパラメータの詳細については、 [手動収集](#manual-collection)を参照してください。バケット数が多いほどヒストグラムの精度は向上しますが、精度向上にはメモリリソースの消費量の増加が伴います。実際のシナリオに応じて、この数値を適切に調整してください。

### カウントミニマムスケッチ {#count-min-sketch}

> **注記：**
>
> Count-Minスケッチは、統計バージョン1ではequal/IN述語選択性推定にのみ使用されます。バージョン2では、後述するようにCount-Minスケッチの衝突回避のための管理が困難であるため、代わりにヒストグラム統計が使用されます。

Count-Min Sketchはハッシュ構造です。1 `a = 1`ような同値クエリや`IN`ようなクエリ（例えば`a IN (1, 2, 3)` ）を処理する際、TiDBはこのデータ構造を用いて推定を行います。

Count-Min Sketchはハッシュ構造であるため、ハッシュ衝突が発生する可能性があります。1 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)のステートメントにおいて、同等のクエリの推定値が実際の値と大きく異なる場合、大きい値と小さい値が一緒にハッシュ化されていると考えられます。この場合、ハッシュ衝突を回避するために、以下のいずれかの方法を実行できます。

-   パラメータ`WITH NUM TOPN`を変更します。TiDB は、高頻度データ（上位 x 値）を別々に保存し、その他のデータは Count-Min Sketch に保存します。そのため、大きな値と小さな値が一緒にハッシュ化されるのを防ぐには、パラメータ`WITH NUM TOPN`の値を増やすことができます。TiDB では、デフォルト値は 20 です。最大値は 1024 です。このパラメータの詳細については、パラメータ[手動収集](#manual-collection)参照してください。
-   2つのパラメータ`WITH NUM CMSKETCH DEPTH`と`WITH NUM CMSKETCH WIDTH`を変更します。どちらもハッシュバケットの数と衝突確率に影響します。実際のシナリオに応じて、2つのパラメータの値を適切に増やすことでハッシュ衝突の確率を下げることができますが、統計情報のメモリ使用量が増加します。TiDBでは、デフォルト値`WITH NUM CMSKETCH DEPTH`は5、デフォルト値`WITH NUM CMSKETCH WIDTH`は2048です。2つのパラメータの詳細については、 [手動収集](#manual-collection)参照してください。

### トップN {#top-n}

上位N値とは、列またはインデックス内で出現頻度が上位N個の値を指します。上位N統計は、頻度統計またはデータスキューとも呼ばれます。

TiDBは、上位N値の値と出現回数を記録します。ここで`N`パラメータ`WITH NUM TOPN`によって制御されます。デフォルト値は20で、これは最も頻度の高い上位20個の値が収集されることを意味します。最大値は1024です。パラメータの詳細については、 [手動収集](#manual-collection)参照してください。

## 選択的統計収集 {#selective-statistics-collection}

このセクションでは、統計を選択的に収集する方法について説明します。

### インデックスの統計を収集する {#collect-statistics-on-indexes}

`IndexNameList` in `TableName`のすべてのインデックスの統計を収集するには、次の構文を使用します。

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

`IndexNameList`が空の場合、この構文は`TableName`内のすべてのインデックスの統計を収集します。

> **注記：**
>
> 収集前後の統計情報の一貫性を確保するために、 `tidb_analyze_version`が`2`場合、この構文はインデックス付き列とすべてのインデックスの統計を収集します。

### いくつかの列の統計を収集する {#collect-statistics-on-some-columns}

TiDBがSQL文を実行する際、オプティマイザはほとんどの場合、列のサブセットのみの統計情報を使用します。例えば、 `WHERE` 、 `JOIN` 、 `ORDER BY` 、 `GROUP BY`節に現れる列などです。これらの列は述語列と呼ばれます。

テーブルに多数の列がある場合、すべての列の統計情報を収集すると大きなオーバーヘッドが発生する可能性があります。オーバーヘッドを軽減するには、特定の列（選択した列）のみの統計を収集するか、オプティマイザで使用する列`PREDICATE COLUMNS`収集することができます。列のサブセットの列リストを永続化して将来再利用できるようにするには、 [列構成を保持する](#persist-column-configurations)参照してください。

> **注記：**
>
> -   述語列の統計の収集は[`tidb_analyze_version = 2`](/system-variables.md#tidb_analyze_version-new-in-v510)にのみ適用されます。
> -   TiDB v7.2.0以降、TiDBは[`tidb_analyze_skip_column_types`](/system-variables.md#tidb_analyze_skip_column_types-new-in-v720)システム変数も導入しました。これは、統計情報を収集する`ANALYZE`コマンドを実行する際に、統計収集からどのタイプの列をスキップするかを示します。このシステム変数は`tidb_analyze_version = 2`にのみ適用されます。

-   特定の列の統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    この構文では、 `ColumnNameList`対象列の名前リストを指定します。複数の列を指定する必要がある場合は、列名をカンマ`,`で区切ります。例： `ANALYZE table t columns a, b` 。この構文は、特定のテーブルの特定の列の統計情報を収集するだけでなく、インデックスが付けられた列とそのテーブル内のすべてのインデックスの統計も同時に収集します。

-   `PREDICATE COLUMNS`の統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    <CustomContent platform="tidb">

    TiDB は常に 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を[`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables)システム テーブルに書き込みます。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    TiDB は常に 300 秒ごとに`PREDICATE COLUMNS`情報を[`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables)システム テーブルに書き込みます。

    </CustomContent>

    この構文では、特定のテーブル内の`PREDICATE COLUMNS`に関する統計を収集するだけでなく、インデックスが付けられた列とそのテーブル内のすべてのインデックスに関する統計も同時に収集します。

    > **注記：**
    >
    > -   [`mysql.column_stats_usage`](/mysql-schema/mysql-schema.md#statistics-system-tables)システム テーブルにそのテーブルに対して記録された`PREDICATE COLUMNS`含まれていない場合、上記の構文は、そのテーブル内のインデックス付き列とすべてのインデックスに関する統計を収集します。
    > -   手動で列をリストするか、 `PREDICATE COLUMNS`使用することで収集から除外された列の統計情報は上書きされません。新しいタイプのSQLクエリを実行する際、オプティマイザは、そのような列に古い統計情報が存在する場合はそれを使用し、統計情報が収集されていない列の場合は擬似列統計情報を使用します。次に`PREDICATE COLUMNS`使用したANALYZEを実行すると、それらの列の統計情報が収集されます。

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

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

#### 動的プルーニングモードでパーティションテーブルの統計を収集する {#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) （v6.3.0以降のデフォルト）でパーティションテーブルにアクセスする場合、TiDBはテーブルレベルの統計、つまりパーティションテーブルのグローバル統計を収集します。現在、グローバル統計はすべてのパーティションの統計から集約されています。動的プルーニングモードでは、テーブルのいずれかのパーティションの統計が更新されると、そのテーブルのグローバル統計も更新される可能性があります。

一部のパーティションの統計が空の場合、または一部のパーティションの一部の列の統計が欠落している場合、コレクションの動作は[`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)変数によって制御されます。

-   グローバル統計の更新がトリガーされ、 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)が`OFF`場合:

    -   一部のパーティションに統計がない場合 (分析されたことのない新しいパーティションなど)、グローバル統計の生成が中断され、パーティションに統計がないことを示す警告メッセージが表示されます。

    -   特定のパーティションに一部の列の統計が存在しない場合 (これらのパーティションでは分析用に異なる列が指定されている)、これらの列の統計を集計するときにグローバル統計の生成が中断され、特定のパーティションに一部の列の統計が存在しないことを示す警告メッセージが表示されます。

-   グローバル統計の更新がトリガーされ、 [`tidb_skip_missing_partition_stats`](/system-variables.md#tidb_skip_missing_partition_stats-new-in-v730)が`ON`場合:

    -   一部のパーティションのすべての列または一部の列の統計が欠落している場合、TiDB はグローバル統計を生成するときにこれらの欠落しているパーティション統計をスキップするため、グローバル統計の生成には影響しません。

動的プルーニングモードでは、パーティションとテーブルの`ANALYZE`構成は同じである必要があります。したがって、 `ANALYZE TABLE TableName PARTITION PartitionNameList`文の後に`COLUMNS`構成を指定した場合、または`WITH`の後に`OPTIONS`構成を指定した場合、TiDB はそれらを無視し、警告を返します。

## 収集パフォーマンスの向上 {#improve-collection-performance}

> **注記：**
>
> -   TiDBにおける`ANALYZE TABLE`実行時間は、MySQLやInnoDBよりも長くなる可能性があります。InnoDBでは少数のページのみがサンプリングされますが、TiDBではデフォルトで包括的な統計セットが完全に再構築されます。

TiDB は、統計収集のパフォーマンスを向上させる 2 つのオプションを提供します。

-   列のサブセットに関する統計情報を収集しています。1 [いくつかの列の統計情報を収集する](#collect-statistics-on-some-columns)参照してください。
-   サンプリング。

### 統計サンプリング {#statistics-sampling}

サンプリングは`ANALYZE`ステートメントの 2 つの別個のオプションを介して実行できます。それぞれが異なる収集アルゴリズムに対応しています。

-   `WITH NUM SAMPLES` 、TiDB のリザーバサンプリング方式で実装されているサンプリングセットのサイズを指定します。テーブルが大きい場合、この方式を使用して統計情報を収集することは推奨されません。リザーバサンプリングの中間結果セットには冗長な結果が含まれるため、メモリなどのリソースにさらなる負荷がかかります。
-   `WITH FLOAT_NUM SAMPLERATE`はバージョン5.3.0で導入されたサンプリング方式です。値の範囲は`(0, 1]`で、このパラメータはサンプリングレートを指定します。これはTiDBのベルヌーイサンプリング方式で実装されており、大規模なテーブルのサンプリングに適しており、収集効率とリソース使用率が向上します。

v5.3.0より前のTiDBでは、統計収集にリザーバサンプリング法が使用されていました。v5.3.0以降、TiDBバージョン2の統計では、デフォルトでベルヌーイサンプリング法が統計収集に使用されます。リザーバサンプリング法を再利用するには、 `WITH NUM SAMPLES`文を使用します。

現在のサンプリングレートは、適応アルゴリズムに基づいて計算されます。表の行数を[`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)で観測できる場合は、その行数を使用して100,000行に対応するサンプリングレートを計算できます。この行数を観測できない場合は、表の[`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)の結果の`APPROXIMATE_KEYS`列目のすべての値の合計を別の基準として使用して、サンプリングレートを計算できます。

> **注記：**
>
> 通常、 `STATS_META` `APPROXIMATE_KEYS`よりも信頼性が高いです。ただし、 `STATS_META`の結果が`APPROXIMATE_KEYS`結果よりもはるかに小さい場合は、 `APPROXIMATE_KEYS`使用してサンプリングレートを計算することをお勧めします。

### 統計情報を収集するためのメモリクォータ {#the-memory-quota-for-collecting-statistics}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

TiDB v6.1.0 以降では、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)使用して、TiDB で統計を収集するためのメモリクォータを制御できます。

適切な値`tidb_mem_quota_analyze`を設定するには、クラスターのデータサイズを考慮してください。デフォルトのサンプリングレートを使用する場合、主な考慮事項は列数、列値のサイズ、およびTiDBのメモリ構成です。最大値と最小値を設定する際には、以下の推奨事項を考慮してください。

> **注記：**
>
> 以下の提案は参考用です。実際のシナリオに基づいて値を設定する必要があります。

-   最小値: TiDBが最も多くの列を持つテーブルから統計情報を収集する場合の最大メモリ使用量よりも大きい値にする必要があります。おおよその目安: TiDBがデフォルト設定で20列のテーブルから統計情報を収集する場合、最大メモリ使用量は約800 MiBです。一方、TiDBがデフォルト設定で160列のテーブルから統計情報を収集する場合、最大メモリ使用量は約5 GiBです。
-   最大値: TiDB が統計を収集していない場合は、使用可能なメモリよりも小さくする必要があります。

## ANALYZE構成を保持する {#persist-analyze-configurations}

v5.4.0以降、TiDBはいくつ`ANALYZE`の設定の永続化をサポートしています。この機能により、既存の設定を将来の統計収集に簡単に再利用できます。

永続性をサポートする`ANALYZE`構成は次のとおりです。

| 構成            | 対応するANALYZE構文                                                                   |
| ------------- | ------------------------------------------------------------------------------- |
| ヒストグラムバケットの数  | `WITH NUM BUCKETS`                                                              |
| トップNの数        | `WITH NUM TOPN`                                                                 |
| サンプル数         | `WITH NUM SAMPLES`                                                              |
| サンプリングレート     | `WITH FLOATNUM SAMPLERATE`                                                      |
| `ANALYZE`列タイプ | AnalyzeColumnOption ::= ( &#39;すべての列&#39; | &#39;述語列&#39; | &#39;列&#39; 列名リスト ) |
| `ANALYZE`列目   | 列名リスト ::= 識別子 ( &#39;,&#39; 識別子 )*                                              |

### ANALYZE構成の永続性を有効にする {#enable-analyze-configuration-persistence}

<CustomContent platform="tidb">

`ANALYZE`構成の永続性機能はデフォルトで有効になっています (システム変数`tidb_analyze_version`は`2`で`tidb_persist_analyze_options`デフォルトで`ON`です)。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ANALYZE`設定の永続性機能はデフォルトで無効になっています。この機能を有効にするには、システム変数`tidb_persist_analyze_options`が`ON`なっていることを確認し、システム変数`tidb_analyze_version`を`2`に設定してください。

</CustomContent>

この機能を使用すると、 `ANALYZE`のステートメントを手動で実行する際に、そのステートメントで指定された永続性設定を記録できます。一度記録すると、次回 TiDB が統計を自動的に更新するとき、またはこれらの設定を指定せずに手動で統計を収集するときに、TiDB は記録された設定に従って統計を収集します。

auto analyze操作に使用される特定のテーブルに保存されている構成を照会するには、次の SQL ステートメントを使用できます。

```sql
SELECT sample_num, sample_rate, buckets, topn, column_choice, column_ids FROM mysql.analyze_options opt JOIN information_schema.tables tbl ON opt.table_id = tbl.tidb_table_id WHERE tbl.table_schema = '{db_name}' AND tbl.table_name = '{table_name}';
```

TiDBは、最新の`ANALYZE`ステートメントで指定された新しい設定を使用して、以前に記録された永続的な設定を上書きします。例えば、 `ANALYZE TABLE t WITH 200 TOPN;`のステートメントを実行すると、 `ANALYZE`ステートメントの上位200個の値が設定されます。その後、 `ANALYZE TABLE t WITH 0.1 SAMPLERATE;`ステートメントを実行すると、上位200個の値と、 `ANALYZE TABLE t WITH 200 TOPN, 0.1 SAMPLERATE;`のステートメントと同様に、auto `ANALYZE`ステートメントのサンプリングレート0.1が設定されます。

### ANALYZE構成の永続性を無効にする {#disable-analyze-configuration-persistence}

`ANALYZE`設定永続性機能を無効にするには、 `tidb_persist_analyze_options`システム変数を`OFF`に設定します。 `ANALYZE`設定永続性機能は`tidb_analyze_version = 1`には適用されないため、 `tidb_analyze_version = 1`設定することでもこの機能を無効にすることができます。

`ANALYZE`設定永続化機能を無効にした後、TiDB は永続化された設定レコードをクリアしません。そのため、この機能を再度有効にすると、TiDB は以前に記録された永続設定を使用して統計情報を収集し続けます。

> **注記：**
>
> `ANALYZE`構成の永続性機能を再度有効にするときに、以前に記録された永続性構成が最新のデータに適用されなくなった場合は、 `ANALYZE`ステートメントを手動で実行し、新しい永続性構成を指定する必要があります。

### 列構成を保持する {#persist-column-configurations}

`ANALYZE`文（ `COLUMNS ColumnNameList` 、 `PREDICATE COLUMNS` 、 `ALL COLUMNS`を含む）の列設定を永続化したい場合は、システム変数`tidb_persist_analyze_options`の値を`ON`に設定して、 [構成の永続性を分析する](#persist-analyze-configurations)機能を有効にします。ANALYZE 設定永続化機能を有効にした後、以下の操作を行います。

-   TiDB が自動的に統計を収集する場合、または列構成を指定せずに`ANALYZE`ステートメントを実行して手動で統計を収集する場合、TiDB は統計収集のために以前に保持された構成を引き続き使用します。
-   列構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDB は最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続的な構成を上書きします。

統計が収集された`PREDICATE COLUMNS`と列を見つけるには、 [`SHOW COLUMN_STATS_USAGE`](/sql-statements/sql-statement-show-column-stats-usage.md)ステートメントを使用します。

次の例では、 `ANALYZE TABLE t PREDICATE COLUMNS;`実行した後、 TiDB は列`b` 、 `c` 、および`d`の統計を収集します。ここで、列`b` `PREDICATE COLUMN`であり、列`c`と`d`インデックス列です。

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

変数[`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)は、TiDB によって収集される統計情報を制御します。現在、統計情報のバージョンは`tidb_analyze_version = 1`と`tidb_analyze_version = 2` 2 つがサポートされています。

-   TiDB Self-Managed の場合、この変数のデフォルト値は、v5.3.0 以降、 `1`から`2`に変更されます。
-   TiDB Cloudの場合、この変数のデフォルト値は、v6.5.0 以降、 `1`から`2`に変更されます。
-   クラスターが以前のバージョンからアップグレードされた場合、アップグレード後もデフォルト値`tidb_analyze_version`は変更されません。

バージョン2が推奨されており、今後も機能強化が続けられ、最終的にはバージョン1を完全に置き換える予定です。バージョン1と比較して、バージョン2では、より大規模なデータ量に対して収集される多くの統計情報の精度が向上しています。また、述語選択性推定のためのCount-Minスケッチ統計情報の収集が不要になり、選択された列のみの自動収集もサポートされるため、収集パフォーマンスも向上しています（ [いくつかの列の統計情報を収集する](#collect-statistics-on-some-columns)参照）。

次の表は、オプティマイザーの推定に使用するために各バージョンで収集される情報を示しています。

| 情報         | バージョン1                                | バージョン2                           |
| ---------- | ------------------------------------- | -------------------------------- |
| 表の行の総数     | ⎷                                     | ⎷                                |
| 等号/IN述語推定  | ⎷ (カラム/ インデックス トップN &amp; カウント最小スケッチ) | ⎷ (カラム/ インデックストップN &amp; ヒストグラム) |
| 範囲述語推定     | ⎷ (カラム/ インデックストップN &amp; ヒストグラム)      | ⎷ (カラム/ インデックストップN &amp; ヒストグラム) |
| `NULL`述語推定 | ⎷                                     | ⎷                                |
| 列の平均長さ     | ⎷                                     | ⎷                                |
| インデックスの平均長 | ⎷                                     | ⎷                                |

### 統計バージョンを切り替える {#switch-between-statistics-versions}

すべてのテーブル／インデックス（およびパーティション）で、同じバージョンの統計情報収集を使用することをお勧めします。バージョン2の使用が推奨されますが、使用中のバージョンで問題が発生したなどの正当な理由がない限り、バージョン間の切り替えは推奨されません。バージョン間の切り替えでは、すべてのテーブルが新しいバージョンで分析されるまで、統計情報が利用できない状態が続く場合があります。統計情報が利用できない場合、オプティマイザのプラン選択に悪影響を与える可能性があります。

切り替えの正当な理由としては、バージョン1では、Count-Minスケッチ統計の収集時にハッシュ衝突が発生するため、equal/IN述語の推定に不正確な点が生じる可能性があることが挙げられます。解決策は[カウントミニマムスケッチ](#count-min-sketch)セクションに記載されています。あるいは、 `tidb_analyze_version = 2`設定してすべてのオブジェクトで`ANALYZE`を再実行することも解決策の一つです。バージョン2の初期リリースでは、 `ANALYZE`後にメモリオーバーフローが発生するリスクがありました。この問題は解決されていますが、当初は`tidb_analyze_version = 1`設定してすべてのオブジェクトで`ANALYZE`再実行するという解決策もありました。

バージョン間の切り替えを準備するには`ANALYZE`

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
    FROM information_schema.tables JOIN mysql.stats_histograms
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

`ANALYZE`ステートメントを実行するときに、 [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md)を使用して`ANALYZE`の現在の状態を表示できます。

TiDB v6.1.0以降、 `SHOW ANALYZE STATUS`ステートメントはクラスターレベルのタスクの表示をサポートします。TiDBの再起動後でも、このステートメントを使用して再起動前のタスクレコードを表示できます。TiDB v6.1.0より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンスレベルのタスクのみを表示でき、タスクレコードはTiDBの再起動後に消去されます。

`SHOW ANALYZE STATUS`最新のタスク記録のみを表示します。TiDB v6.1.0以降では、システムテーブル`mysql.analyze_jobs`を通じて過去7日間のタスク履歴を表示できます。

[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)が設定され、TiDB のバックグラウンドで実行されている自動タスク`ANALYZE`がこのしきい値を超えるメモリを使用すると、タスクは再試行されます。失敗したタスクと再試行されたタスクは、 `SHOW ANALYZE STATUS`ステートメントの出力で確認できます。

[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)が 0 より大きく、TiDB バックグラウンドで実行されている自動`ANALYZE`タスクにこのしきい値を超える時間がかかる場合、タスクは終了します。

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

### テーブルのヘルス状態 {#health-state-of-tables}

[`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md)ステートメントを使用すると、テーブルのヘルス状態を確認し、統計情報の精度を大まかに推定できます。3 &gt;= `row_count` `modify_count`場合、ヘルス状態は 0 です。7 &lt; `row_count`の場合、ヘルス状態は ( `modify_count` - `modify_count` / `row_count` ) * 100 です。

### 列のメタデータ {#metadata-of-columns}

[`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md)ステートメントを使用すると、すべての列の異なる値の数と`NULL`の数を表示できます。

### ヒストグラムのバケット {#buckets-of-histogram}

[`SHOW STATS_BUCKETS`](/sql-statements/sql-statement-show-stats-buckets.md)ステートメントを使用して、ヒストグラムの各バケットを表示できます。

### トップN情報 {#top-n-information}

[`SHOW STATS_TOPN`](/sql-statements/sql-statement-show-stats-topn.md)ステートメントを使用すると、現在 TiDB によって収集されている Top-N 情報を表示できます。

## 統計情報を削除 {#delete-statistics}

統計を削除するには、 [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md)ステートメントを実行します。

## 負荷統計 {#load-statistics}

> **注記：**
>
> ロード統計はクラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

デフォルトでは、列統計のサイズに応じて、TiDB は次のように異なる方法で統計をロードします。

-   メモリ消費量が少ない統計 (count、distinctCount、nullCount など) の場合、列データが更新されている限り、TiDB は対応する統計を SQL 最適化ステージで使用するためにメモリに自動的にロードします。
-   大量のメモリを消費する統計（ヒストグラム、TopN、Count-Min Sketchなど）については、SQL実行のパフォーマンスを確保するため、TiDBはオンデマンドで統計を非同期的に読み込みます。ヒストグラムを例に挙げると、TiDBはオプティマイザーがその列のヒストグラム統計を使用する場合にのみ、その列のヒストグラム統計をメモリに読み込みます。オンデマンドの非同期統計読み込みはSQL実行のパフォーマンスには影響しませんが、SQL最適化に不完全な統計を提供する可能性があります。

v5.4.0以降、TiDBは統計情報の同期ロード機能を導入しました。この機能により、SQL文の実行時に、ヒストグラム、TopN、Count-Min Sketch統計などの大規模な統計情報をメモリに同期ロードできるようになり、SQL最適化における統計情報の完全性が向上します。

この機能を有効にするには、システム変数[`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)の値を、SQL最適化が完全な列統計情報を同期的にロードするまでの最大待機時間（ミリ秒）に設定します。この変数のデフォルト値は`100`で、この機能が有効であることを示します。

<CustomContent platform="tidb">

統計の同期読み込み機能を有効にした後、次のように機能をさらに構成できます。

-   SQL最適化の待機時間がタイムアウトに達した際のTiDBの動作を制御するには、システム変数[`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)の値を変更します。この変数のデフォルト値は`ON`で、タイムアウト後、SQL最適化プロセスはどの列に対してもヒストグラム、TopN、CMSketch統計を使用しません。この変数を`OFF`に設定すると、タイムアウト後にSQL実行が失敗します。
-   同期ロード統計機能で同時に処理できる列の最大数を指定するには、TiDB設定ファイルの[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)オプションの値を変更します。v8.2.0以降、このオプションのデフォルト値は`0`で、TiDBはサーバー設定に基づいて同時実行性を自動的に調整します。
-   同期ロード統計機能がキャッシュできる列リクエストの最大数を指定するには、TiDB設定ファイルの[`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)オプションの値を変更します。デフォルト値は`1000`です。

TiDBの起動時、初期統計情報が完全にロードされる前に実行されるSQL文は、最適ではない実行プランを持つ可能性があり、パフォーマンスの問題を引き起こす可能性があります。このような問題を回避するために、TiDB v7.1.0では設定パラメータ[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v657-and-v710)が導入されました。このオプションを使用すると、起動時に統計情報の初期化が完了した後にのみTiDBがサービスを提供するかどうかを制御できます。v7.2.0以降では、このパラメータはデフォルトで有効になっています。

v7.1.0 以降、TiDB では軽量統計の初期化に[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)導入されています。

-   `lite-init-stats`の値が`true`場合、統計の初期化では、インデックスまたは列のヒストグラム、TopN、または Count-Min Sketch はメモリにロードされません。
-   `lite-init-stats`の値が`false`場合、統計の初期化では、インデックスと主キーのヒストグラム、TopN、Count-Min Sketch がメモリにロードされますが、主キー以外の列のヒストグラム、TopN、Count-Min Sketch はメモリにロードされません。オプティマイザーが特定のインデックスまたは列のヒストグラム、TopN、Count-Min Sketch を必要とする場合、必要な統計は同期的または非同期的にメモリにロードされます。

デフォルト値は`lite-init-stats` `true` 、これは軽量な統計情報の初期化を有効にすることを意味します。5 から`lite-init-stats` `true`設定すると、統計情報の初期化が高速化され、不要な統計情報の読み込みが回避されるため、TiDB のメモリ使用量が削減されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

統計情報の同期ロード機能を有効にすると、システム変数[`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)値を変更することで、SQL最適化の待機時間がタイムアウトに達した際のTiDBの動作を制御できます。この変数のデフォルト値は`ON`で、タイムアウト後、SQL最適化プロセスはどの列に対してもヒストグラム、TopN、CMSketch統計を使用しません。この変数を`OFF`に設定すると、タイムアウト後にSQL実行が失敗します。

</CustomContent>

## 輸出入統計 {#export-and-import-statistics}

このセクションでは、統計をエクスポートおよびインポートする方法について説明します。

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

-   特定の時間における`${db_name}`データベース内の`${table_name}`のテーブルの JSON 形式の統計を取得するには:

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}

### 輸入統計 {#import-statistics}

> **注記：**
>
> MySQL クライアントを起動するときは、 `--local-infile=1`オプションを使用します。

通常、インポートされた統計は、エクスポート インターフェイスを使用して取得された JSON ファイルを参照します。

統計のロードは[`LOAD STATS`](/sql-statements/sql-statement-load-stats.md)ステートメントで実行できます。

例えば：

```sql
LOAD STATS 'file_name';
```

`file_name`はインポートする統計のファイル名です。

## ロック統計 {#lock-statistics}

v6.5.0以降、TiDBは統計情報のロックをサポートしています。テーブルまたはパーティションの統計情報がロックされると、そのテーブルの統計情報を変更できなくなり、そのテーブルに対して`ANALYZE`文を実行することもできなくなります。例えば：

テーブル`t`を作成し、そこにデータを挿入します。テーブル`t`の統計情報がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

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

テーブル`t`の統計情報をロックし、 `ANALYZE`実行します。警告メッセージには、 `ANALYZE`ステートメントがテーブル`t`スキップしたことが示されています。

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

表`t`および`ANALYZE`統計のロックを解除すると、再度正常に実行できるようになります。

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

さらに、 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)使用してパーティションの統計情報をロックすることもできます。例:

パーティションテーブル`t`を作成し、そこにデータを挿入します。パーティション`p1`の統計情報がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

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

パーティション`p1`の統計情報をロックし、 `ANALYZE`実行します。警告メッセージには、 `ANALYZE`ステートメントがパーティション`p1`スキップしたことが示されています。

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

パーティション`p1`と`ANALYZE`統計のロック解除を再度正常に実行できます。

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

|                                    | テーブル全体を削除する | テーブル全体を切り捨てる                             | パーティションを切り捨てる                                | 新しいパーティションを作成する        | パーティションを削除する                                     | パーティションを再編成する                                    | パーティションを交換する                                 |
| ---------------------------------- | ----------- | ---------------------------------------- | -------------------------------------------- | ---------------------- | ------------------------------------------------ | ------------------------------------------------ | -------------------------------------------- |
| パーティションテーブルがロックされている               | ロックが無効です    | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。 | /                                            | /                      | /                                                | /                                                | /                                            |
| パーティションテーブルとテーブル全体がロックされている        | ロックが無効です    | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。 | 古いパーティションのロック情報は無効であり、新しいパーティションは自動的にロックされます | 新しいパーティションは自動的にロックされます | 削除されたパーティションのロック情報はクリアされ、テーブル全体のロックは引き続き有効になります。 | 削除されたパーティションのロック情報はクリアされ、新しいパーティションは自動的にロックされます。 | ロック情報は交換されたテーブルに転送され、新しいパーティションは自動的にロックされます。 |
| パーティションテーブルで、一部のパーティションのみがロックされている | ロックが無効です    | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。 | TiDBは古いテーブルを削除するためロックは無効であり、ロック情報も削除される。     | /                      | 削除されたパーティションのロック情報はクリアされます                       | 削除されたパーティションのロック情報はクリアされます                       | ロック情報は交換テーブルに転送される                           |

## <code>ANALYZE</code>タスクと同時実行を管理する {#manage-code-analyze-code-tasks-and-concurrency}

このセクションでは、バックグラウンド`ANALYZE`タスクを終了し、 `ANALYZE`同時実行を制御する方法について説明します。

### バックグラウンドの<code>ANALYZE</code>タスクを終了する {#terminate-background-code-analyze-code-tasks}

TiDB v6.0以降、TiDBは`KILL`のステートメントを使用して、バックグラウンドで実行されている`ANALYZE`タスクを終了できるようになりました。バックグラウンドで実行されている`ANALYZE`タスクが大量のリソースを消費し、アプリケーションに影響を与える場合は、次の手順で`ANALYZE`タスクを終了できます。

1.  次の SQL ステートメントを実行します。

    ```sql
    SHOW ANALYZE STATUS
    ```

    結果の`instance`列目と`process_id`列目を確認すると、TiDB インスタンスのアドレスと、バックグラウンド`ANALYZE`タスクのタスク`ID`取得できます。

2.  バックグラウンドで実行されている`ANALYZE`タスクを終了します。

    <CustomContent platform="tidb">

    -   [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が`true` (デフォルトでは`true` ) の場合、 `KILL TIDB ${id};`ステートメントを直接実行できます。ここで、 `${id}`前の手順で取得されたバックグラウンド`ANALYZE`タスクの`ID`です。
    -   `enable-global-kill`が`false`場合、クライアントを使用してバックエンド`ANALYZE`タスクを実行している TiDB インスタンスに接続し、 `KILL TIDB ${id};`文を実行する必要があります。クライアントを使用して別の TiDB インスタンスに接続している場合、またはクライアントと TiDB クラスタの間にプロキシがある場合、 `KILL`文ではバックグラウンド`ANALYZE`タスクを終了できません。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    `ANALYZE`タスクを終了するには、 `KILL TIDB ${id};`ステートメントを実行します。ここで、 `${id}`前の手順で取得されたバックグラウンド`ANALYZE`タスクの`ID`です。

    </CustomContent>

`KILL`ステートメントの詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)参照してください。

### <code>ANALYZE</code>同時実行を制御する {#control-code-analyze-code-concurrency}

`ANALYZE`ステートメントを実行すると、システム変数を使用して同時実行性を調整し、システムへの影響を制御できます。

関連するシステム変数の関係を以下に示します。

![analyze\_concurrency](/media/analyze_concurrency.png)

上図に示すように、 `tidb_build_stats_concurrency` 、 `tidb_build_sampling_stats_concurrency` 、 `tidb_analyze_partition_concurrency`上流と下流の関係にあります。実際の合計同時実行数は`tidb_build_stats_concurrency` * ( `tidb_build_sampling_stats_concurrency` + `tidb_analyze_partition_concurrency` ) です。これらの変数を変更する際には、それぞれの値も同時に考慮する必要があります。 `tidb_analyze_partition_concurrency` 、 `tidb_build_sampling_stats_concurrency` 、 `tidb_build_stats_concurrency`の順に1つずつ調整し、システムへの影響を確認することをお勧めします。これらの3つの変数の値が大きいほど、システムへのリソースオーバーヘッドが大きくなります。

#### <code>tidb_build_stats_concurrency</code> {#code-tidb-build-stats-concurrency-code}

`ANALYZE`ステートメントを実行すると、タスクは複数の小さなタスクに分割されます。各タスクは、1つの列またはインデックスの統計情報のみを処理します。3 変数[`tidb_build_stats_concurrency`](/system-variables.md#tidb_build_stats_concurrency)使用して、同時に実行する小さなタスクの数を制御できます。デフォルト値は`2`です。v7.4.0 以前のバージョンでは、デフォルト値は`4`です。

#### <code>tidb_build_sampling_stats_concurrency</code> {#code-tidb-build-sampling-stats-concurrency-code}

通常の列を分析する場合、サンプリングタスクの同時実行を制御するために[`tidb_build_sampling_stats_concurrency`](/system-variables.md#tidb_build_sampling_stats_concurrency-new-in-v750)指定できます。デフォルト値は`2`です。

#### <code>tidb_analyze_partition_concurrency</code> {#code-tidb-analyze-partition-concurrency-code}

`ANALYZE`ステートメントを実行する際に、パーティションテーブルの統計情報の読み取りと書き込みの同時実行を制御するために[`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency)使用できます。デフォルト値は`2`です。v7.4.0 以前のバージョンでは、デフォルト値は`1`です。

#### <code>tidb_distsql_scan_concurrency</code> {#code-tidb-distsql-scan-concurrency-code}

通常の列を分析する場合、変数[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)を使って一度に読み取るリージョンの数を制御できます。デフォルト値は`15`です。値を変更するとクエリのパフォーマンスに影響することに注意してください。値は慎重に調整してください。

#### <code>tidb_index_serial_scan_concurrency</code> {#code-tidb-index-serial-scan-concurrency-code}

インデックス列を分析する際に、変数[`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)を使って一度に読み取るリージョンの数を制御できます。デフォルト値は`1`です。この値を変更するとクエリのパフォーマンスに影響することに注意してください。値は慎重に調整してください。

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [負荷統計](/sql-statements/sql-statement-load-stats.md)
-   [ドロップ統計](/sql-statements/sql-statement-drop-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報をアンロック](/sql-statements/sql-statement-unlock-stats.md)
-   [統計を表示_ロック済み](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [負荷統計](/sql-statements/sql-statement-load-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [統計情報をアンロック](/sql-statements/sql-statement-unlock-stats.md)
-   [統計を表示_ロック済み](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>
