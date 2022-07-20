---
title: Introduction to Statistics
summary: Learn how the statistics collect table-level and column-level information.
---

# 統計入門 {#introduction-to-statistics}

TiDBは統計を使用して[どのインデックスを選択するか](/choose-index.md)を決定します。 `tidb_analyze_version`変数は、TiDBによって収集される統計を制御します。現在、 `tidb_analyze_version = 1`と`tidb_analyze_version = 2`の2つのバージョンの統計がサポートされています。 v5.1.0より前のバージョンでは、この変数のデフォルト値は`1`です。 v5.3.0以降のバージョンでは、この変数のデフォルト値は`2`であり、これは実験的機能として機能します。クラスタがv5.3.0より前のバージョンからv5.3.0以降にアップグレードされた場合、デフォルト値の`tidb_analyze_version`は変更されません。

> **ノート：**
>
> `tidb_analyze_version = 2`の場合、 `ANALYZE`の実行後にメモリオーバーフローが発生した場合は、 `tidb_analyze_version = 1`を設定し、次のいずれかの操作を行う必要があります。
>
> -   `ANALYZE`ステートメントを手動で実行する場合は、分析するすべてのテーブルを手動で分析します。
>
>     {{< copyable "" >}}
>
>     ```sql
>     select distinct(concat('ANALYZE ',table_schema, '.', table_name,';')) from information_schema.tables, mysql.stats_histograms where stats_ver = 2 and table_id = tidb_table_id ;
>     ```
>
> -   自動分析が有効になっているためにTiDBが`ANALYZE`ステートメントを自動的に実行する場合は、次のステートメントを実行して`DROP STATS`ステートメントを生成します。
>
>     {{< copyable "" >}}
>
>     ```sql
>     select distinct(concat('DROP STATS ',table_schema, '.', table_name,';')) from information_schema.tables, mysql.stats_histograms where stats_ver = 2 and table_id = tidb_table_id ;
>     ```

これらの2つのバージョンには、TiDBに異なる情報が含まれています。

| 情報                | バージョン1                            | バージョン2                                                |
| ----------------- | --------------------------------- | ----------------------------------------------------- |
| テーブルの行の総数         | √                                 | √                                                     |
| カラム数-最小スケッチ       | √                                 | ××                                                    |
| インデックスカウント-最小スケッチ | √                                 | ××                                                    |
| カラムTop-N          | √                                 | √（メンテナンス方法と精度が向上）                                     |
| インデックストップ-N       | √（メンテナンス精度が不十分な場合、不正確になる可能性があります） | √（メンテナンス方法と精度が向上）                                     |
| カラムヒストグラム         | √                                 | √（ヒストグラムにはTop-N値は含まれていません。）                           |
| インデックスヒストグラム      | √                                 | √（ヒストグラムバケットは各バケットの異なる値の数を記録し、ヒストグラムにはTop-N値は含まれません。） |
| 列の`NULL`の数        | √                                 | √                                                     |
| インデックス内の`NULL`の数  | √                                 | √                                                     |
| 列の平均の長さ           | √                                 | √                                                     |
| インデックスの平均の長さ      | √                                 | √                                                     |

バージョン1と比較して、バージョン2の統計は、データ量が膨大な場合にハッシュの衝突によって引き起こされる潜在的な不正確さを回避します。また、ほとんどのシナリオで推定精度を維持します。

このドキュメントでは、ヒストグラム、Count-Min Sketch、およびTop-Nを簡単に紹介し、統計の収集と保守について詳しく説明します。

## ヒストグラム {#histogram}

ヒストグラムは、データの分布のおおよその表現です。値の全範囲を一連のバケットに分割し、単純なデータを使用して、バケットに含まれる値の数など、各バケットを記述します。 TiDBでは、各テーブルの特定の列に対して同じ深さのヒストグラムが作成されます。等深ヒストグラムを使用して、間隔クエリを推定できます。

ここで「等しい深さ」とは、各バケットに分類される値の数が可能な限り等しいことを意味します。たとえば、特定のセット{1.6、1.9、1.9、2.0、2.4、2.6、2.7、2.7、2.8、2.9、3.4、3.5}に対して、4つのバケットを生成するとします。等深ヒストグラムは次のとおりです。 4つのバケット[1.6、1.9]、[2.0、2.6]、[2.7、2.8]、[2.9、3.5]が含まれています。バケットの深さは3です。

![Equal-depth Histogram Example](/media/statistics-1.png)

ヒストグラムバケット数の上限を決定するパラメータの詳細については、 [手動コレクション](#manual-collection)を参照してください。バケットの数が多いほど、ヒストグラムの精度が高くなります。ただし、精度が高くなると、メモリリソースの使用量が犠牲になります。この数値は、実際のシナリオに応じて適切に調整できます。

## カウント-最小スケッチ {#count-min-sketch}

Count-MinSketchはハッシュ構造です。等価クエリに`a = 1`つまたは`IN`のクエリ（たとえば、 `a in (1, 2, 3)` ）が含まれている場合、TiDBはこのデータ構造を使用して推定します。

Count-Min Sketchはハッシュ構造であるため、ハッシュの衝突が発生する可能性があります。 `EXPLAIN`ステートメントでは、同等のクエリの推定値が実際の値から大きく外れている場合、大きい値と小さい値が一緒にハッシュされていると見なすことができます。この場合、ハッシュの衝突を回避するために次のいずれかの方法をとることができます。

-   `WITH NUM TOPN`パラメーターを変更します。 TiDBは、高周波（top x）データを個別に保存し、他のデータはCount-MinSketchに保存します。したがって、大きい値と小さい値が一緒にハッシュされるのを防ぐために、 `WITH NUM TOPN`の値を増やすことができます。 TiDBでは、デフォルト値は20です。最大値は1024です。このパラメーターの詳細については、 [フルコレクション](#full-collection)を参照してください。
-   2つのパラメータ`WITH NUM CMSKETCH DEPTH`と`WITH NUM CMSKETCH WIDTH`を変更します。どちらもハッシュバケットの数と衝突確率に影響します。実際のシナリオに従って2つのパラメーターの値を適切に増やして、ハッシュの衝突の可能性を減らすことができますが、統計のメモリ使用量が高くなります。 TiDBでは、デフォルト値の`WITH NUM CMSKETCH DEPTH`は5で、デフォルト値の`WITH NUM CMSKETCH WIDTH`は2048です。2つのパラメーターの詳細については、 [フルコレクション](#full-collection)を参照してください。

## トップN値 {#top-n-values}

Top-N値は、列またはインデックスで上位N個のオカレンスを持つ値です。 TiDBは、Top-N値の値と発生を記録します。

## 統計を収集する {#collect-statistics}

### 手動収集 {#manual-collection}

`ANALYZE`ステートメントを実行して、統計を収集できます。

> **ノート：**
>
> TiDBの実行時間`ANALYZE TABLE`は、MySQLまたはInnoDBの実行時間よりも長くなります。 InnoDBでは、少数のページのみがサンプリングされますが、TiDBでは、包括的な統計セットが完全に再構築されます。 MySQL用に作成されたスクリプトは、 `ANALYZE TABLE`が短期間の操作であると素朴に予想する場合があります。
>
> より迅速な分析のために、 `tidb_enable_fast_analyze`から`1`に設定して、クイック分析機能を有効にすることができます。このパラメーターのデフォルト値は`0`です。
>
> クイック分析を有効にすると、TiDBは約10,000行のデータをランダムにサンプリングして統計を作成します。したがって、不均一なデータ分布や比較的少量のデータの場合、統計情報の精度は比較的低くなります。間違ったインデックスを選択するなど、実行計画が不十分になる可能性があります。通常の`ANALYZE`ステートメントの実行時間が許容できる場合は、クイック分析機能を無効にすることをお勧めします。
>
> `tidb_enable_fast_analyze`は実験的機能であり、現在`tidb_analyze_version=2`の統計情報と**正確には一致していません**。したがって、 `tidb_enable_fast_analyze`が有効になっている場合は、 `tidb_analyze_version`から`1`の値を設定する必要があります。

#### フルコレクション {#full-collection}

次の構文を使用して、完全な収集を実行できます。

-   `TableNameList`のすべてのテーブルの統計を収集するには：

    {{< copyable "" >}}

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `WITH NUM BUCKETS`は、生成されたヒストグラムのバケットの最大数を指定します。

-   `WITH NUM TOPN`は、生成される`TOPN`秒の最大数を指定します。

-   `WITH NUM CMSKETCH DEPTH`は、CMスケッチの深さを指定します。

-   `WITH NUM CMSKETCH WIDTH`は、CMスケッチの幅を指定します。

-   `WITH NUM SAMPLES`はサンプル数を指定します。

-   `WITH FLOAT_NUM SAMPLERATE`はサンプリングレートを指定します。

`WITH NUM SAMPLES`と`WITH FLOAT_NUM SAMPLERATE`は、サンプルを収集する2つの異なるアルゴリズムに対応します。

-   `WITH NUM SAMPLES`は、サンプリングセットのサイズを指定します。これは、TiDBのリザーバーサンプリング方法で実装されます。テーブルが大きい場合、この方法を使用して統計を収集することはお勧めしません。リザーバーサンプリングの中間結果セットには冗長な結果が含まれているため、メモリなどのリソースに追加の圧力がかかります。
-   `WITH FLOAT_NUM SAMPLERATE`は、v5.3.0で導入されたサンプリング方法です。値の範囲が`(0, 1]`の場合、このパラメーターはサンプリングレートを指定します。これは、TiDBのベルヌーイサンプリングの方法で実装されます。これは、より大きなテーブルのサンプリングに適しており、収集効率とリソース使用量のパフォーマンスが向上します。

v5.3.0より前では、TiDBはリザーバーサンプリング方式を使用して統計を収集していました。 v5.3.0以降、TiDBバージョン2統計は、デフォルトでベルヌーイサンプリング法を使用して統計を収集します。貯留層サンプリング法を再利用するには、 `WITH NUM SAMPLES`ステートメントを使用できます。

> **ノート：**
>
> 現在のサンプリングレートは、適応アルゴリズムに基づいて計算されます。 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)を使用してテーブルの行数を確認できる場合、この行数を使用して、100,000行に対応するサンプリングレートを計算できます。この数値がわからない場合は、 [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)表の`TABLE_KEYS`列を別の参照として使用して、サンプリングレートを計算できます。
>
> 通常、 `STATS_META`は`TABLE_KEYS`よりも信頼できます。ただし、 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)などの方法でデータをインポートすると、 `STATS_META`の結果は`0`になります。この状況を処理するために、 `STATS_META`の結果が`TABLE_KEYS`の結果よりもはるかに小さい場合に、 `TABLE_KEYS`を使用してサンプリングレートを計算できます。

##### 一部の列の統計を収集する {#collect-statistics-on-some-columns}

ほとんどの場合、SQLステートメントを実行するとき、オプティマイザーは一部の列（ `WHERE` 、および`JOIN` `GROUP BY`の列など）の統計のみを使用し`ORDER BY` 。これらの列は`PREDICATE COLUMNS`と呼ばれます。

テーブルに多くの列がある場合、すべての列の統計を収集すると、大きなオーバーヘッドが発生する可能性があります。オーバーヘッドを削減するために、オプティマイザーが使用する特定の列または`PREDICATE COLUMNS`つのみの統計を収集できます。

> **ノート：**
>
> 一部の列の統計の収集は、 `tidb_analyze_version = 2`にのみ適用されます。

-   特定の列の統計を収集するには、次の構文を使用します。

    {{< copyable "" >}}

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    構文では、 `ColumnNameList`はターゲット列の名前リストを指定します。複数の列を指定する必要がある場合は、コンマ`,`を使用して列名を区切ります。たとえば、 `ANALYZE table t columns a, b` 。この構文は、特定のテーブルの特定の列の統計を収集するだけでなく、インデックス付きの列とそのテーブルのすべてのインデックスの統計を同時に収集します。

    > **ノート：**
    >
    > 上記の構文は完全なコレクションです。たとえば、この構文を使用して列`a`と`b`の統計を収集した後、列`c`の統計も収集する場合は、 `ANALYZE TABLE t COLUMNS c`を使用して追加の列`c`を指定するだけでなく、 `ANALYZE table t columns a, b, c`を使用して3つの列すべてを指定する必要があります。

-   `PREDICATE COLUMNS`の統計を収集するには、次のようにします。

    > **警告：**
    >
    > 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。実稼働環境で使用することはお勧めしません。

    1.  [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定して、TiDBが`PREDICATE COLUMNS`を収集できるようにします。

        設定後、TiDBは100* [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`の情報を`mysql.column_stats_usage`のシステムテーブルに書き込みます。

    2.  ビジネスのクエリパターンが比較的安定したら、次の構文を使用して`PREDICATE COLUMNS`の統計を収集します。

        {{< copyable "" >}}

        ```sql
        ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
        ```

        この構文は、特定のテーブルの`PREDICATE COLUMNS`に関する統計を収集するだけでなく、インデックス付きの列とそのテーブル内のすべてのインデックスの統計を同時に収集します。

        > **ノート：**
        >
        > -   `mysql.column_stats_usage`のシステムテーブルにそのテーブルの`PREDICATE COLUMNS`のレコードが含まれていない場合、前述の構文は、そのテーブルのすべての列とすべてのインデックスの統計を収集します。
        > -   この構文を使用して統計を収集した後、新しいタイプのSQLクエリを実行すると、オプティマイザーはこの時点で一時的に古い列または疑似列の統計を使用する場合があり、TiDBは次回から使用された列の統計を収集します。

-   すべての列とインデックスの統計を収集するには、次の構文を使用します。

    {{< copyable "" >}}

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

`ANALYZE`ステートメント（ `COLUMNS ColumnNameList` 、および`PREDICATE COLUMNS`を含む）の列構成を永続化する場合は、 `tidb_persist_analyze_options`システム変数の値を`ALL COLUMNS`に設定して、 `ON`機能を使用可能に[ANALYZE構成の永続性](#persist-analyze-configurations)ます。 ANALYZE構成永続化機能を有効にした後：

-   TiDBが統計を自動的に収集する場合、または列構成を指定せずに`ANALYZE`ステートメントを実行して統計を手動で収集する場合、TiDBは統計収集に以前に永続化された構成を引き続き使用します。
-   列構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDBは、最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続構成を上書きします。

統計が収集された`PREDICATE COLUMNS`列と列を見つけるには、次の構文を使用します。

{{< copyable "" >}}

```sql
SHOW COLUMN_STATS_USAGE [ShowLikeOrWhere];
```

`SHOW COLUMN_STATS_USAGE`ステートメントは、次の6列を返します。

| カラム名               | 説明                    |
| ------------------ | --------------------- |
| `Db_name`          | データベース名               |
| `Table_name`       | テーブル名                 |
| `Partition_name`   | パーティション名              |
| `Column_name`      | 列名                    |
| `Last_used_at`     | クエリ最適化で列統計が最後に使用されたとき |
| `Last_analyzed_at` | カラム統計が最後に収集されたとき      |

次の例では、 `ANALYZE TABLE t PREDICATE COLUMNS;`を実行した後、 `d`は列`b` 、および`c`の統計を収集します。ここで、列`d`は`b`で、列`PREDICATE COLUMN`および`c`はインデックス列です。

{{< copyable "" >}}

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
SHOW COLUMN_STATS_USAGE WHERE db_name = 'test' AND table_name = 't' AND last_used_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at |
+---------+------------+----------------+-------------+---------------------+------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | NULL             |
+---------+------------+----------------+-------------+---------------------+------------------+
1 row in set (0.00 sec)

ANALYZE TABLE t PREDICATE COLUMNS;
Query OK, 0 rows affected, 1 warning (0.03 sec)

-- Specify `last_analyzed_at IS NOT NULL` to show the columns for which statistics have been collected.
SHOW COLUMN_STATS_USAGE WHERE db_name = 'test' AND table_name = 't' AND last_analyzed_at IS NOT NULL;
+---------+------------+----------------+-------------+---------------------+---------------------+
| Db_name | Table_name | Partition_name | Column_name | Last_used_at        | Last_analyzed_at    |
+---------+------------+----------------+-------------+---------------------+---------------------+
| test    | t          |                | b           | 2022-01-05 17:21:33 | 2022-01-05 17:23:06 |
| test    | t          |                | c           | NULL                | 2022-01-05 17:23:06 |
| test    | t          |                | d           | NULL                | 2022-01-05 17:23:06 |
+---------+------------+----------------+-------------+---------------------+---------------------+
3 rows in set (0.00 sec)
```

##### インデックスに関する統計を収集する {#collect-statistics-on-indexes}

`TableName`の`IndexNameList`のすべてのインデックスの統計を収集するには、次の構文を使用します。

{{< copyable "" >}}

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

`IndexNameList`が空の場合、この構文は`TableName`のすべてのインデックスの統計を収集します。

> **ノート：**
>
> 収集の前後の統計情報に一貫性を持たせるために、 `tidb_analyze_version`が`2`の場合、この構文は、インデックスだけでなく、テーブル全体（すべての列とインデックスを含む）の統計を収集します。

##### パーティションに関する統計を収集する {#collect-statistics-on-partitions}

-   `TableName`の`PartitionNameList`のすべてのパーティションの統計を収集するには、次の構文を使用します。

    {{< copyable "" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `TableName`の`PartitionNameList`のすべてのパーティションのインデックス統計を収集するには、次の構文を使用します。

    {{< copyable "" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   テーブル内の一部のパーティションのうち[一部の列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)だけが必要な場合は、次の構文を使用します。

    > **警告：**
    >
    > 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。実稼働環境で使用することはお勧めしません。

    {{< copyable "" >}}

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

##### 動的プルーニングモードでパーティションテーブルの統計を収集する {#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

[動的剪定モード](/partitioned-table.md#dynamic-pruning-mode)でパーティションテーブルにアクセスする場合、TiDBはGlobalStatsと呼ばれるテーブルレベルの統計を収集します。現在、GlobalStatsはすべてのパーティションの統計から集計されています。動的プルーニング・モードでは、パーティション化された表の統計更新により、GlobalStatsが更新される可能性があります。

> **ノート：**
>
> -   GlobalStatsの更新がトリガーされたとき：
>
>     -   一部のパーティションに統計がない場合（分析されたことがない新しいパーティションなど）、GlobalStatsの生成が中断され、パーティションで使用可能な統計がないことを示す警告メッセージが表示されます。
>     -   一部の列の統計が特定のパーティションに存在しない場合（これらのパーティションで分析するために異なる列が指定されている場合）、これらの列の統計が集約されるとGlobalStatsの生成が中断され、一部の列の統計が特定に存在しないことを示す警告メッセージが表示されますパーティション。
> -   動的プルーニングモードでは、パーティションとテーブルの分析構成は同じである必要があります。したがって、 `ANALYZE TABLE TableName PARTITION PartitionNameList`ステートメントの後に`COLUMNS`構成を指定するか、 `WITH`の後に`OPTIONS`構成を指定すると、TiDBはそれらを無視し、警告を返します。

#### インクリメンタルコレクション {#incremental-collection}

完全収集後の分析速度を向上させるために、増分収集を使用して、時間列などの単調に減少しない列に新しく追加されたセクションを分析できます。

> **ノート：**
>
> -   現在、インクリメンタルコレクションはインデックス用にのみ提供されています。
> -   インクリメンタルコレクションを使用する場合は、テーブルに`INSERT`の操作のみが存在し、インデックス列に新しく挿入された値が単調に減少しないことを確認する必要があります。そうしないと、統計情報が不正確になり、TiDBオプティマイザが適切な実行プランを選択するのに影響を与える可能性があります。

次の構文を使用して、増分収集を実行できます。

-   `TableName`分の`IndexNameLists`すべてのインデックス列の統計を段階的に収集するには：

    {{< copyable "" >}}

    ```sql
    ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `TableName`分の`PartitionNameLists`すべてのパーティションのインデックス列の統計を段階的に収集するには：

    {{< copyable "" >}}

    ```sql
    ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

### 自動更新 {#automatic-update}

`INSERT` 、または`DELETE`ステートメントの場合、 `UPDATE`は行数と更新された行を自動的に更新します。 TiDBはこの情報を定期的に保持し、更新サイクルは20* `stats-lease`です。デフォルト値の`stats-lease`は`3s`です。値を`0`に指定すると、自動的に更新されません。

統計の自動更新に関連する3つのシステム変数は次のとおりです。

| システム変数                         | デフォルト値        | 説明                     |
| ------------------------------ | ------------- | ---------------------- |
| `tidb_auto_analyze_ratio`      | 0.5           | 自動更新のしきい値              |
| `tidb_auto_analyze_start_time` | `00:00 +0000` | TiDBが自動更新を実行できる1日の開始時刻 |
| `tidb_auto_analyze_end_time`   | `23:59 +0000` | TiDBが自動更新を実行できる1日の終了時刻 |

テーブル内の`tbl`の行の総数に対する変更された行の数の比率が`tidb_auto_analyze_ratio`より大きく、現在の時刻が`tidb_auto_analyze_start_time`の場合、 `tidb_auto_analyze_end_time`はバックグラウンドで`ANALYZE TABLE tbl`ステートメントを実行して、この統計を自動的に更新します。テーブル。

> **ノート：**
>
> 現在、自動更新では、マニュアル`ANALYZE`で入力された構成項目は記録されません。したがって、 `WITH`構文を使用して`ANALYZE`の収集動作を制御する場合は、統計を収集するためにスケジュールされたタスクを手動で設定する必要があります。

TiDB v5.0より前では、クエリを実行すると、TiDBは`feedback-probability`でフィードバックを収集し、フィードバックに基づいてヒストグラムとカウント最小スケッチを更新します。 **v5.0以降、この機能はデフォルトで無効になっているため、この機能を有効にすることはお勧めしません。**

TiDB v6.0以降、TiDBは`KILL`ステートメントを使用してバックグラウンドで実行されている`ANALYZE`タスクを終了することをサポートしています。バックグラウンドで実行されている`ANALYZE`のタスクが多くのリソースを消費し、アプリケーションに影響を与えることがわかった場合は、次の手順を実行して`ANALYZE`のタスクを終了できます。

1.  次のSQLステートメントを実行します。

    {{< copyable "" >}}

    ```sql
    SHOW ANALYZE STATUS
    ```

    結果の`instance`列と`process_id`列を確認することで、TiDBインスタンスアドレスとバックグラウンド`ANALYZE`タスクのタスク`ID`を取得できます。

2.  バックグラウンドで実行されている`ANALYZE`のタスクを終了します。

    -   [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が`true` （デフォルトでは`true` ）の場合、 `KILL TIDB ${id};`ステートメントを直接実行できます。ここで、 `${id}`は、前のステップで取得したバックグラウンド`ANALYZE`タスクの`ID`です。
    -   `enable-global-kill`が`false`の場合、クライアントを使用して、バックエンド`ANALYZE`タスクを実行しているTiDBインスタンスに接続してから、 `KILL TIDB ${id};`ステートメントを実行する必要があります。クライアントを使用して別のTiDBインスタンスに接続する場合、またはクライアントとTiDBクラスタの間にプロキシがある場合、 `KILL`ステートメントはバックグラウンド`ANALYZE`タスクを終了できません。

`KILL`ステートメントの詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

### <code>ANALYZE</code>並行性を制御する {#control-code-analyze-code-concurrency}

`ANALYZE`ステートメントを実行する場合、次のパラメーターを使用して並行性を調整し、システムへの影響を制御できます。

#### <code>tidb_build_stats_concurrency</code> {#code-tidb-build-stats-concurrency-code}

現在、 `ANALYZE`ステートメントを実行すると、タスクは複数の小さなタスクに分割されます。各タスクは、1つの列またはインデックスでのみ機能します。 `tidb_build_stats_concurrency`パラメーターを使用して、同時タスクの数を制御できます。デフォルト値は`4`です。

#### <code>tidb_distsql_scan_concurrency</code> {#code-tidb-distsql-scan-concurrency-code}

通常の列を分析する場合、 `tidb_distsql_scan_concurrency`パラメーターを使用して、一度に読み取るリージョンの数を制御できます。デフォルト値は`15`です。

#### <code>tidb_index_serial_scan_concurrency</code> {#code-tidb-index-serial-scan-concurrency-code}

インデックス列を分析する場合、 `tidb_index_serial_scan_concurrency`パラメーターを使用して、一度に読み取るリージョンの数を制御できます。デフォルト値は`1`です。

### ANALYZE構成を永続化する {#persist-analyze-configurations}

v5.4.0以降、TiDBはいくつかの`ANALYZE`構成の永続化をサポートしています。この機能を使用すると、既存の構成を将来の統計収集に簡単に再利用できます。

永続性をサポートする`ANALYZE`の構成は次のとおりです。

| 構成            | 対応するANALYZE構文                                                                                                  |
| ------------- | -------------------------------------------------------------------------------------------------------------- |
| ヒストグラムバケットの数  | NUM個のバケット付き                                                                                                    |
| トップNの数        | NUMTOPN付き                                                                                                      |
| サンプル数         | NUMサンプル付き                                                                                                      |
| サンプリングレート     | FLOATNUMSAMPLERATEを使用                                                                                          |
| `ANALYZE`列タイプ | AnalyzeColumnOption :: =（&#39;ALL COLUMNS&#39; |&#39;PREDICATE COLUMNS&#39; |&#39;COLUMNS&#39; ColumnNameList） |
| `ANALYZE`列    | ColumnNameList :: =識別子（&#39;、&#39;識別子）*                                                                        |

#### ANALYZE構成の永続性を有効にする {#enable-analyze-configuration-persistence}

`ANALYZE`構成永続化機能は、デフォルトで有効になっています（システム変数`tidb_analyze_version`は`2`で、 `tidb_persist_analyze_options`はデフォルトで`ON`です）。この機能を使用して、ステートメントを手動で実行するときに、 `ANALYZE`ステートメントで指定された永続性構成を記録できます。記録されると、次にTiDBが統計を自動的に更新するか、これらの構成を指定せずに手動で統計を収集すると、TiDBは記録された構成に従って統計を収集します。

永続性構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDBは、最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続性構成を上書きします。

#### ANALYZE構成の永続性を無効にする {#disable-analyze-configuration-persistence}

`ANALYZE`構成の永続化機能を無効にするには、 `tidb_persist_analyze_options`システム変数を`OFF`に設定します。 `ANALYZE`構成の永続化機能は`tidb_analyze_version = 1`には適用できないため、 `tidb_analyze_version = 1`を設定すると機能を無効にすることもできます。

`ANALYZE`構成永続化機能を無効にした後、TiDBは永続化された構成レコードをクリアしません。したがって、この機能を再度有効にすると、TiDBは、以前に記録された永続的な構成を使用して統計を収集し続けます。

> **ノート：**
>
> `ANALYZE`構成の永続性機能を再度有効にしたときに、以前に記録された永続性構成が最新のデータに適用できなくなった場合は、 `ANALYZE`ステートメントを手動で実行し、新しい永続性構成を指定する必要があります。

### 統計を収集するためのメモリ割り当て {#the-memory-quota-for-collecting-statistics}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

TiDB v6.1.0以降、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)を使用して、TiDBで統計を収集するためのメモリクォータを制御できます。

`tidb_mem_quota_analyze`の適切な値を設定するには、クラスタのデータサイズを考慮してください。デフォルトのサンプリングレートを使用する場合、主な考慮事項は、列の数、列の値のサイズ、およびTiDBのメモリ構成です。最大値と最小値を構成するときは、次の提案を考慮してください。

> **ノート：**
>
> 以下の提案は参照用です。実際のシナリオに基づいて値を構成する必要があります。

-   最小値：TiDBが最も多くの列を持つテーブルから統計を収集する場合、最大メモリ使用量よりも大きくする必要があります。おおよそのリファレンス：TiDBがデフォルト構成を使用して20列のテーブルから統計を収集する場合、最大メモリ使用量は約800MiBです。 TiDBがデフォルト構成を使用して160列のテーブルから統計を収集する場合、最大メモリ使用量は約5GiBです。
-   最大値：TiDBが統計を収集していない場合は、使用可能なメモリよりも小さくする必要があります。

### <code>ANALYZE</code>状態をビュー {#view-code-analyze-code-state}

`ANALYZE`ステートメントを実行する場合、次のSQLステートメントを使用して`ANALYZE`の現在の状態を表示できます。

{{< copyable "" >}}

```sql
SHOW ANALYZE STATUS [ShowLikeOrWhere]
```

このステートメントは、 `ANALYZE`の状態を返します。 `ShowLikeOrWhere`を使用して、必要な情報をフィルタリングできます。

現在、 `SHOW ANALYZE STATUS`ステートメントは次の11列を返します。

| カラム名           | 説明                                                                                                |
| :------------- | :------------------------------------------------------------------------------------------------ |
| table_schema   | データベース名                                                                                           |
| table_name     | テーブル名                                                                                             |
| partition_name | パーティション名                                                                                          |
| job_info       | タスク情報。インデックスを分析する場合、この情報にはインデックス名が含まれます。 `tidb_analyze_version =2`の場合、この情報にはサンプルレートなどの構成項目が含まれます。 |
| 処理された行         | 分析された行の数                                                                                          |
| 始まる時間          | タスクが開始する時刻                                                                                        |
| 州              | `pending` 、 `finished` `running`を含むタスクの`failed`                                                   |
| fail_reason    | タスクが失敗する理由。実行が成功した場合、値は`NULL`です。                                                                  |
| 実例             | タスクを実行するTiDBインスタンス                                                                                |
| process_id     | タスクを実行するプロセスID                                                                                    |

TiDB v6.1.0以降、 `SHOW ANALYZE STATUS`ステートメントはクラスターレベルのタスクの表示をサポートします。 TiDBを再起動した後でも、このステートメントを使用して、再起動前のタスクレコードを表示できます。 TiDB v6.1.0より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンスレベルのタスクのみを表示でき、タスクレコードはTiDBの再起動後にクリアされます。

`SHOW ANALYZE STATUS`は、最新のタスクレコードのみを示します。 TiDB v6.1.0以降、システムテーブル`mysql.analyze_jobs`から過去7日間の履歴タスクを表示できます。

[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)が設定され、TiDBバックグラウンドで実行されている自動`ANALYZE`タスクがこのしきい値よりも多くのメモリを使用する場合、タスクは再試行されます。 `SHOW ANALYZE STATUS`ステートメントの出力で、失敗したタスクと再試行されたタスクを確認できます。

[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)が0より大きく、TiDBバックグラウンドで実行されている自動`ANALYZE`タスクにこのしきい値よりも長い時間がかかる場合、タスクは終了します。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

## 統計をビューする {#view-statistics}

次のステートメントを使用して、統計ステータスを表示できます。

### テーブルのメタデータ {#metadata-of-tables}

`SHOW STATS_META`ステートメントを使用して、行の総数と更新された行の数を表示できます。

{{< copyable "" >}}

```sql
SHOW STATS_META [ShowLikeOrWhere];
```

`ShowLikeOrWhereOpt`の構文は次のとおりです。

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

現在、 `SHOW STATS_META`ステートメントは次の6列を返します。

| カラム名             | 説明       |
| :--------------- | :------- |
| `db_name`        | データベース名  |
| `table_name`     | テーブル名    |
| `partition_name` | パーティション名 |
| `update_time`    | 更新の時間    |
| `modify_count`   | 変更された行の数 |
| `row_count`      | 行の総数     |

> **ノート：**
>
> TiDBがDMLステートメントに従って行の総数と変更された行の数を自動的に更新すると、 `update_time`も更新されます。したがって、 `update_time`は、 `ANALYZE`ステートメントが最後に実行された時刻を必ずしも示しているわけではありません。

### テーブルのヘルス状態 {#health-state-of-tables}

`SHOW STATS_HEALTHY`ステートメントを使用して、テーブルの正常性状態を確認し、統計の精度を大まかに見積もることができます。 `modify_count` &gt; = `row_count`の場合、ヘルス状態は0です。 `modify_count` &lt; `row_count`の場合、ヘルス状態は（ `modify_count` / `row_count` ）*100です。

構文は次のとおりです。

{{< copyable "" >}}

```sql
SHOW STATS_HEALTHY [ShowLikeOrWhere];
```

`SHOW STATS_HEALTHY`の概要は次のとおりです。

![ShowStatsHealthy](/media/sqlgram/ShowStatsHealthy.png)

現在、 `SHOW STATS_HEALTHY`ステートメントは次の4列を返します。

| カラム名             | 説明         |
| :--------------- | :--------- |
| `db_name`        | データベース名    |
| `table_name`     | テーブル名      |
| `partition_name` | パーティション名   |
| `healthy`        | テーブルのヘルス状態 |

### 列のメタデータ {#metadata-of-columns}

`SHOW STATS_HISTOGRAMS`ステートメントを使用して、すべての列のさまざまな値の数と`NULL`の数を表示できます。

構文は次のとおりです。

{{< copyable "" >}}

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere]
```

このステートメントは、すべての列の異なる値の数と`NULL`の数を返します。 `ShowLikeOrWhere`を使用して、必要な情報をフィルタリングできます。

現在、 `SHOW STATS_HISTOGRAMS`ステートメントは次の10列を返します。

| カラム名             | 説明                                                   |
| :--------------- | :--------------------------------------------------- |
| `db_name`        | データベース名                                              |
| `table_name`     | テーブル名                                                |
| `partition_name` | パーティション名                                             |
| `column_name`    | 列名（ `is_index`が`0`の場合）またはインデックス名（ `is_index`が`1`の場合） |
| `is_index`       | インデックス列かどうか                                          |
| `update_time`    | 更新の時間                                                |
| `distinct_count` | 異なる値の数                                               |
| `null_count`     | `NULL`の数                                             |
| `avg_col_size`   | 列の平均の長さ                                              |
| 相関               | 列のピアソン相関係数と、2つの列間の関連度を示す整数主キー                        |

### ヒストグラムのバケット {#buckets-of-histogram}

`SHOW STATS_BUCKETS`ステートメントを使用して、ヒストグラムの各バケットを表示できます。

構文は次のとおりです。

{{< copyable "" >}}

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere]
```

回路図は以下の通りです：

![SHOW STATS\_BUCKETS](/media/sqlgram/SHOW_STATS_BUCKETS.png)

このステートメントは、すべてのバケットに関する情報を返します。 `ShowLikeOrWhere`を使用して、必要な情報をフィルタリングできます。

現在、 `SHOW STATS_BUCKETS`ステートメントは次の11列を返します。

| カラム名             | 説明                                                                         |
| :--------------- | :------------------------------------------------------------------------- |
| `db_name`        | データベース名                                                                    |
| `table_name`     | テーブル名                                                                      |
| `partition_name` | パーティション名                                                                   |
| `column_name`    | 列名（ `is_index`が`0`の場合）またはインデックス名（ `is_index`が`1`の場合）                       |
| `is_index`       | インデックス列かどうか                                                                |
| `bucket_id`      | バケットのID                                                                    |
| `count`          | バケットと前のバケットに該当するすべての値の数                                                    |
| `repeats`        | 最大値の発生数                                                                    |
| `lower_bound`    | 最小値                                                                        |
| `upper_bound`    | 最大値                                                                        |
| `ndv`            | バケット内の異なる値の数。 `tidb_analyze_version` = `1`の場合、 `ndv`は常に`0`であり、実際の意味はありません。 |

### トップN情報 {#top-n-information}

`SHOW STATS_TOPN`ステートメントを使用して、TiDBによって現在収集されているTop-N情報を表示できます。

構文は次のとおりです。

{{< copyable "" >}}

```sql
SHOW STATS_TOPN [ShowLikeOrWhere];
```

現在、 `SHOW STATS_TOPN`ステートメントは次の7列を返します。

| カラム名             | 説明                                                   |
| ---------------- | ---------------------------------------------------- |
| `db_name`        | データベース名                                              |
| `table_name`     | テーブル名                                                |
| `partition_name` | パーティション名                                             |
| `column_name`    | 列名（ `is_index`が`0`の場合）またはインデックス名（ `is_index`が`1`の場合） |
| `is_index`       | インデックス列かどうか                                          |
| `value`          | この列の値                                                |
| `count`          | 値が表示される回数                                            |

## 統計を削除する {#delete-statistics}

`DROP STATS`ステートメントを実行して、統計を削除できます。

{{< copyable "" >}}

```sql
DROP STATS TableName
```

上記のステートメントは、 `TableName`のすべての統計を削除します。パーティションテーブルが指定されている場合、このステートメントは、このテーブル内のすべてのパーティションの統計と、動的プルーニングモードで生成されたGlobalStatsを削除します。

{{< copyable "" >}}

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

この前述のステートメントは、 `PartitionNameList`の指定されたパーティションの統計のみを削除します。

{{< copyable "" >}}

```sql
DROP STATS TableName GLOBAL;
```

上記のステートメントは、指定されたテーブルの動的プルーニングモードで生成されたGlobalStatsのみを削除します。

## 負荷統計 {#load-statistics}

デフォルトでは、列統計のサイズに応じて、TiDBは次のように統計を異なる方法でロードします。

-   小さなスペース（count、distinctCount、nullCountなど）を消費する統計の場合、列データが更新されている限り、TiDBは対応する統計をメモリに自動的にロードしてSQL最適化段階で使用します。
-   大きなスペースを消費する統計（ヒストグラム、TopN、Count-Min Sketchなど）の場合、SQL実行のパフォーマンスを確保するために、TiDBはオンデマンドで統計を非同期にロードします。例としてヒストグラムを取り上げます。 TiDBは、オプティマイザがその列のヒストグラム統計を使用する場合にのみ、列のヒストグラム統計をメモリにロードします。オンデマンドの非同期統計のロードはSQL実行のパフォーマンスに影響を与えませんが、SQL最適化の統計が不完全になる可能性があります。

v5.4.0以降、TiDBは同期ロード統計機能を導入しています。この機能により、SQLステートメントの実行時にTiDBが大規模な統計（ヒストグラム、TopN、Count-Min Sketch統計など）をメモリに同期的にロードできるようになり、SQL最適化の統計の完全性が向上します。

> **警告：**
>
> 現在、統計を同期的にロードすることは実験的機能です。実稼働環境で使用することはお勧めしません。

統計の同期ロード機能はデフォルトで無効になっています。この機能を有効にするには、 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)システム変数の値を、SQL最適化が完全な列統計を同期的にロードするために最大で待機できるタイムアウト（ミリ秒単位）に設定します。この変数のデフォルト値は`0`で、機能が無効になっていることを示します。

同期ロード統計機能を有効にした後、次のように機能をさらに構成できます。

-   SQL最適化の待機時間がタイムアウトに達したときのTiDBの動作を制御するには、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更します。この変数のデフォルト値は`OFF`で、タイムアウト後にSQLの実行が失敗することを示します。この変数を`ON`に設定すると、タイムアウト後、SQL最適化プロセスはどの列にもヒストグラム、TopN、またはCMSketch統計を使用しませんが、疑似統計の使用に戻ります。
-   同期ロード統計機能が同時に処理できる列の最大数を指定するには、TiDB構成ファイルの[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)オプションの値を変更します。デフォルト値は`5`です。
-   同期ロード統計機能がキャッシュできる列要求の最大数を指定するには、TiDB構成ファイルの[`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)オプションの値を変更します。デフォルト値は`1000`です。

## 統計のインポートとエクスポート {#import-and-export-statistics}

### 統計のエクスポート {#export-statistics}

統計をエクスポートするためのインターフェースは次のとおりです。

-   `${db_name}`データベースの`${table_name}`テーブルのJSON形式の統計を取得するには：

    {{< copyable "" >}}

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}
    ```

    例えば：

    {{< copyable "" >}}

    ```
    curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json
    ```

-   特定の時間に`${db_name}`データベースの`${table_name}`テーブルのJSON形式の統計を取得するには：

    {{< copyable "" >}}

    ```
    http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}
    ```

### 統計のインポート {#import-statistics}

> **ノート：**
>
> MySQLクライアントを起動するときは、 `--local-infile=1`オプションを使用します。

通常、インポートされた統計は、エクスポートインターフェイスを使用して取得されたJSONファイルを参照します。

構文：

{{< copyable "" >}}

```
LOAD STATS 'file_name'
```

`file_name`は、インポートする統計のファイル名です。

## も参照してください {#see-also}

-   [統計のロード](/sql-statements/sql-statement-load-stats.md)
-   [ドロップ統計](/sql-statements/sql-statement-drop-stats.md)
