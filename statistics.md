---
title: Introduction to Statistics
summary: Learn how the statistics collect table-level and column-level information.
---

# 統計入門 {#introduction-to-statistics}

TiDB は統計を使用して決定します[どのインデックスを選択するか](/choose-index.md) 。

## 統計のバージョン {#versions-of-statistics}

`tidb_analyze_version`変数は、TiDB によって収集される統計を制御します。現在、統計の 2 つのバージョン、 `tidb_analyze_version = 1`と`tidb_analyze_version = 2`がサポートされています。

-   TiDB セルフホストの場合、v5.3.0 以降、この変数のデフォルト値は`1`から`2`に変更されます。
-   TiDB Cloudの場合、v6.5.0 以降、この変数のデフォルト値は`1`から`2`に変更されます。
-   クラスターが以前のバージョンからアップグレードされた場合、デフォルト値の`tidb_analyze_version`はアップグレード後も変更されません。

バージョン 1 と比較して、バージョン 2 の統計は、データ量が膨大な場合にハッシュの衝突によって引き起こされる潜在的な不正確さを回避します。また、ほとんどのシナリオで推定精度も維持されます。

これら 2 つのバージョンには、TiDB に異なる情報が含まれています。

| 情報               | バージョン1                            | バージョン2                                                        |
| ---------------- | --------------------------------- | ------------------------------------------------------------- |
| テーブル内の総行数        | √                                 | √                                                             |
| カラム数 - 最小スケッチ    | √                                 | ×                                                             |
| インデックス数 - 最小スケッチ | √                                 | ×                                                             |
| カラム上位 N          | √                                 | √ (メンテナンス方法と精度の向上)                                            |
| インデックストップN       | √ (メンテナンス精度が不十分だと精度が低下する可能性があります) | √ (メンテナンス方法と精度の向上)                                            |
| カラムヒストグラム        | √                                 | √ (ヒストグラムには上位 N 値は含まれません。)                                    |
| インデックスヒストグラム     | √                                 | √ (ヒストグラム バケットには、各バケット内の異なる値の数が記録されます。ヒストグラムには上位 N 値は含まれません。) |
| 列内の`NULL`の数      | √                                 | √                                                             |
| インデックス内の`NULL`の数 | √                                 | √                                                             |
| 列の平均長さ           | √                                 | √                                                             |
| インデックスの平均長       | √                                 | √                                                             |

`tidb_analyze_version = 2`の場合、 `ANALYZE`実行後にメモリオーバーフローが発生した場合は、バージョン 1 にフォールバックするように`tidb_analyze_version = 1`を設定し、次のいずれかの操作を実行する必要があります。

-   `ANALYZE`ステートメントを手動で実行する場合は、分析対象のすべてのテーブルを手動で分析します。

    ```sql
    SELECT DISTINCT(CONCAT('ANALYZE TABLE ', table_schema, '.', table_name, ';')) FROM information_schema.tables, mysql.stats_histograms WHERE stats_ver = 2 AND table_id = tidb_table_id;
    ```

-   自動分析が有効になっているために TiDB が`ANALYZE`ステートメントを自動的に実行する場合は、 `DROP STATS`ステートメントを生成する次のステートメントを実行します。

    ```sql
    SELECT DISTINCT(CONCAT('DROP STATS ', table_schema, '.', table_name, ';')) FROM information_schema.tables, mysql.stats_histograms WHERE stats_ver = 2 AND table_id = tidb_table_id;
    ```

-   前のステートメントの結果が長すぎてコピーして貼り付けることができない場合は、次のように結果を一時テキスト ファイルにエクスポートし、そのファイルから実行できます。

    ```sql
    SELECT DISTINCT ... INTO OUTFILE '/tmp/sql.txt';
    mysql -h ${TiDB_IP} -u user -P ${TIDB_PORT} ... < '/tmp/sql.txt'
    ```

このドキュメントでは、ヒストグラム、Count-Min Sketch、および Top-N について簡単に紹介し、統計の収集と保守について詳しく説明します。

## ヒストグラム {#histogram}

ヒストグラムは、データの分布を近似的に表現したものです。値の範囲全体を一連のバケットに分割し、バケットに含まれる値の数などの単純なデータを使用して各バケットを説明します。 TiDB では、各テーブルの特定の列に対して同じ深さのヒストグラムが作成されます。等深度ヒストグラムを使用して、間隔クエリを推定できます。

ここで「深さが等しい」とは、各バケットに入る値の数が可能な限り等しいことを意味します。たとえば、特定のセット {1.6、1.9、1.9、2.0、2.4、2.6、2.7、2.7、2.8、2.9、3.4、3.5} に対して、4 つのバケットを生成するとします。等深度ヒストグラムは次のとおりです。これには、4 つのバケット [1.6、1.9]、[2.0、2.6]、[2.7、2.8]、[2.9、3.5] が含まれています。バケットの深さは 3 です。

![Equal-depth Histogram Example](/media/statistics-1.png)

ヒストグラムバケット数の上限を決定するパラメータの詳細については、 [マニュアルの収集](#manual-collection)を参照してください。バケットの数が多いほど、ヒストグラムの精度は高くなります。ただし、精度を高めるとメモリリソースの使用量が犠牲になります。実際のシナリオに応じて、この数値を適切に調整できます。

## カウントミニスケッチ {#count-min-sketch}

Count-Min Sketch はハッシュ構造です。等価性クエリに`a = 1`または`IN`クエリ (たとえば、 `a in (1, 2, 3)` ) が含まれる場合、TiDB は推定にこのデータ構造を使用します。

Count-Min Sketch はハッシュ構造であるため、ハッシュの衝突が発生する可能性があります。 `EXPLAIN`のステートメントで、同等のクエリの推定値が実際の値から大きく乖離している場合、大きい値と小さい値が一緒にハッシュ化されていると考えることができます。この場合、次のいずれかの方法でハッシュの衝突を回避できます。

-   `WITH NUM TOPN`パラメータを変更します。 TiDB は、高頻度 (上位 x) データを個別に保存し、他のデータは Count-Min Sketch に保存されます。したがって、より大きな値とより小さな値が一緒にハッシュされるのを防ぐために、 `WITH NUM TOPN`の値を増やすことができます。 TiDB では、デフォルト値は 20 です。最大値は 1024 です。このパラメータの詳細については、 [フルコレクション](#full-collection)を参照してください。
-   2 つのパラメータ`WITH NUM CMSKETCH DEPTH`と`WITH NUM CMSKETCH WIDTH`を変更します。どちらもハッシュ バケットの数と衝突確率に影響します。実際のシナリオに応じて 2 つのパラメーターの値を適切に増やしてハッシュ衝突の可能性を減らすことができますが、その代わりに統計のメモリ使用量が増加します。 TiDB では、デフォルト値`WITH NUM CMSKETCH DEPTH`は 5、デフォルト値`WITH NUM CMSKETCH WIDTH`は 2048 です。2 つのパラメータの詳細については、 [フルコレクション](#full-collection)を参照してください。

## 上位 N の値 {#top-n-values}

上位 N 値は、列またはインデックス内で上位 N 個が出現する値です。 TiDB は、値と上位 N 値の出現を記録します。

## 統計の収集 {#collect-statistics}

### 手動収集 {#manual-collection}

`ANALYZE`ステートメントを実行して統計を収集できます。

> **注記：**
>
> TiDB の`ANALYZE TABLE`の実行時間は、MySQL や InnoDB よりも長くなります。 InnoDB では、少数のページのみがサンプリングされますが、TiDB では、包括的な統計セットが完全に再構築されます。 MySQL 用に作成されたスクリプトは、単純に`ANALYZE TABLE`短期間の操作であると予想する可能性があります。
>
> 分析を迅速に行うには、 `tidb_enable_fast_analyze` ～ `1`を設定してクイック分析機能を有効にします。このパラメータのデフォルト値は`0`です。
>
> クイック分析を有効にすると、TiDB は約 10,000 行のデータをランダムにサンプリングして統計を作成します。したがって、データの分布が不均一であったり、データ量が比較的少ない場合には、統計情報の精度は比較的低くなります。間違ったインデックスを選択するなど、実行計画が不適切になる可能性があります。通常の`ANALYZE`ステートメントの実行時間が許容できる場合は、クイック分析機能を無効にすることをお勧めします。
>
> `tidb_enable_fast_analyze`は実験的機能であり、現時点では`tidb_analyze_version=2`の統計情報と**正確には一致しません**。したがって、 `tidb_enable_fast_analyze`が有効な場合は、 `tidb_analyze_version`から`1`の値を設定する必要があります。

#### フルコレクション {#full-collection}

次の構文を使用して完全な収集を実行できます。

-   `TableNameList`のすべてのテーブルの統計を収集するには:

    ```sql
    ANALYZE TABLE TableNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `WITH NUM BUCKETS`生成されるヒストグラム内のバケットの最大数を指定します。

-   `WITH NUM TOPN`生成される`TOPN`の最大数を指定します。

-   `WITH NUM CMSKETCH DEPTH` CM スケッチの深さを指定します。

-   `WITH NUM CMSKETCH WIDTH` CM スケッチの幅を指定します。

-   `WITH NUM SAMPLES`サンプル数を指定します。

-   `WITH FLOAT_NUM SAMPLERATE`サンプリングレートを指定します。

`WITH NUM SAMPLES`と`WITH FLOAT_NUM SAMPLERATE`サンプルを収集する 2 つの異なるアルゴリズムに対応します。

-   `WITH NUM SAMPLES` 、TiDB の貯留層サンプリング方法で実装されるサンプリング セットのサイズを指定します。テーブルが大きい場合、この方法を使用して統計を収集することはお勧めできません。貯留層サンプリングの中間結果セットには冗長な結果が含まれるため、メモリなどのリソースにさらなる負荷がかかります。
-   `WITH FLOAT_NUM SAMPLERATE` 、v5.3.0 で導入されたサンプリング方法です。値範囲`(0, 1]`では、このパラメータはサンプリング レートを指定します。これは、TiDB のベルヌーイ サンプリングの方法で実装されており、大規模なテーブルのサンプリングに適しており、収集効率とリソース使用率が向上します。

v5.3.0 より前では、TiDB はリザーバー サンプリング方式を使用して統計を収集します。 v5.3.0 以降、TiDB バージョン 2 統計では、デフォルトでベルヌーイ サンプリング法を使用して統計が収集されます。貯留層サンプリング方法を再利用するには、 `WITH NUM SAMPLES`ステートメントを使用します。

現在のサンプリング レートは、適応アルゴリズムに基づいて計算されます。 [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md)を使用してテーブル内の行数を確認できる場合、この行数を使用して 100,000 行に対応するサンプリング レートを計算できます。この数値を確認できない場合は、 [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)表の`TABLE_KEYS`列を別の参照として使用して、サンプリング レートを計算できます。

<CustomContent platform="tidb">

> **注記：**
>
> 通常、 `STATS_META`は`TABLE_KEYS`よりも信頼性が高くなります。ただし、 [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)のような方法でデータをインポートした後、 `STATS_META`の結果は`0`になります。この状況に対処するには、 `STATS_META`の結果が`TABLE_KEYS`の結果よりはるかに小さい場合に、 `TABLE_KEYS`使用してサンプリング レートを計算します。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 通常、 `STATS_META`は`TABLE_KEYS`よりも信頼性が高くなります。ただし、 TiDB Cloudコンソールを介してデータをインポートした後 ( [サンプルデータのインポート](/tidb-cloud/import-sample-data.md)参照)、 `STATS_META`の結果は`0`になります。この状況に対処するには、 `STATS_META`の結果が`TABLE_KEYS`の結果よりはるかに小さい場合に、 `TABLE_KEYS`使用してサンプリング レートを計算します。

</CustomContent>

##### いくつかの列の統計を収集する {#collect-statistics-on-some-columns}

ほとんどの場合、SQL ステートメントを実行するとき、オプティマイザーは一部の列 ( `WHERE` 、 `JOIN` 、 `ORDER BY` 、および`GROUP BY`ステートメントの列など) の統計のみを使用します。これらの列は`PREDICATE COLUMNS`と呼ばれます。

テーブルに多くの列がある場合、すべての列の統計を収集すると、大きなオーバーヘッドが発生する可能性があります。オーバーヘッドを軽減するために、オプティマイザで使用する特定の列または`PREDICATE COLUMNS`列のみの統計を収集できます。

> **注記：**
>
> 一部の列に関する統計の収集は`tidb_analyze_version = 2`にのみ適用されます。

-   特定の列の統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName COLUMNS ColumnNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

    構文では、 `ColumnNameList`ターゲット列の名前リストを指定します。複数の列を指定する必要がある場合は、カンマ`,`を使用して列名を区切ります。たとえば、 `ANALYZE table t columns a, b` 。この構文は、特定のテーブル内の特定の列に関する統計を収集するだけでなく、インデックス付きの列とそのテーブル内のすべてのインデックスに関する統計も同時に収集します。

    > **注記：**
    >
    > 上記の構文は完全なコレクションです。たとえば、この構文を使用して列`a`と列`b`の統計を収集した後、列`c`の統計も収集する場合は、 `ANALYZE TABLE t COLUMNS c`を使用して追加の列`c`のみを指定するのではなく、 `ANALYZE table t columns a, b, c`を使用して 3 つの列すべてを指定する必要があります。

-   `PREDICATE COLUMNS`に関する統計を収集するには、次の手順を実行します。

    > **警告：**
    >
    > 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。本番環境で使用することはお勧めできません。

    1.  TiDB が`PREDICATE COLUMNS`を収集できるようにするには、 [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v540)システム変数の値を`ON`に設定します。

        <CustomContent platform="tidb">

        設定後、TiDB は 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)ごとに`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システムテーブルに書き込みます。

        </CustomContent>

        <CustomContent platform="tidb-cloud">

        設定後、TiDB は`PREDICATE COLUMNS`情報を`mysql.column_stats_usage`システムテーブルに 300 秒ごとに書き込みます。

        </CustomContent>

    2.  ビジネスのクエリ パターンが比較的安定したら、次の構文を使用して`PREDICATE COLUMNS`に関する統計を収集します。

        ```sql
        ANALYZE TABLE TableName PREDICATE COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
        ```

        この構文は、特定のテーブルの`PREDICATE COLUMNS`に関する統計を収集するだけでなく、インデックス付きの列とそのテーブル内のすべてのインデックスの統計も同時に収集します。

        > **注記：**
        >
        > -   `mysql.column_stats_usage`システム テーブルにそのテーブルの`PREDICATE COLUMNS`が含まれていない場合、上記の構文はそのテーブル内のすべての列とすべてのインデックスに関する統計を収集します。
        > -   この構文を使用して統計を収集した後、新しいタイプの SQL クエリを実行すると、オプティマイザーは今回は古い列または疑似列の統計を一時的に使用し、TiDB は次回から使用された列の統計を収集することがあります。

-   すべての列とインデックスの統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName ALL COLUMNS [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

`ANALYZE`ステートメントの列構成 ( `COLUMNS ColumnNameList` 、 `PREDICATE COLUMNS` 、および`ALL COLUMNS`を含む) を保持したい場合は、 `tidb_persist_analyze_options`システム変数の値を`ON`に設定して[構成の永続性を分析する](#persist-analyze-configurations)機能を有効にします。 ANALYZE 構成永続化機能を有効にした後、次の手順を実行します。

-   TiDB が統計を自動的に収集する場合、または列構成を指定せずに`ANALYZE`ステートメントを実行して統計を手動で収集する場合、TiDB は統計収集のために以前に永続化された構成を引き続き使用します。
-   列構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDB は、最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続的な構成を上書きします。

統計が収集された`PREDICATE COLUMNS`および列を見つけるには、次の構文を使用します。

```sql
SHOW COLUMN_STATS_USAGE [ShowLikeOrWhere];
```

`SHOW COLUMN_STATS_USAGE`ステートメントは次の 6 つの列を返します。

| カラム名               | 説明                     |
| ------------------ | ---------------------- |
| `Db_name`          | データベース名                |
| `Table_name`       | テーブル名                  |
| `Partition_name`   | パーティション名               |
| `Column_name`      | 列名                     |
| `Last_used_at`     | クエリの最適化で列統計が最後に使用された時刻 |
| `Last_analyzed_at` | 列統計が最後に収集された時刻         |

次の例では、 `ANALYZE TABLE t PREDICATE COLUMNS;`実行後、TiDB は列`b` 、 `c` 、および`d`の統計を収集します。ここで、列`b`は`PREDICATE COLUMN`で、列`c`と`d`はインデックス列です。

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

`IndexNameList` in `TableName`のすべてのインデックスの統計を収集するには、次の構文を使用します。

```sql
ANALYZE TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
```

`IndexNameList`が空の場合、この構文は`TableName`のすべてのインデックスの統計を収集します。

> **注記：**
>
> 収集前後の統計情報の一貫性を確保するために、 `tidb_analyze_version`が`2`の場合、この構文はインデックスのみではなくテーブル全体 (すべての列とインデックスを含む) の統計を収集します。

##### パーティションに関する統計を収集する {#collect-statistics-on-partitions}

-   `PartitionNameList` in `TableName`のすべてのパーティションの統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   `PartitionNameList` in `TableName`のすべてのパーティションのインデックス統計を収集するには、次の構文を使用します。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   テーブル内の一部のパーティションのうち[いくつかの列の統計を収集する](/statistics.md#collect-statistics-on-some-columns)だけが必要な場合は、次の構文を使用します。

    > **警告：**
    >
    > 現在、 `PREDICATE COLUMNS`に関する統計の収集は実験的機能です。本番環境で使用することはお勧めできません。

    ```sql
    ANALYZE TABLE TableName PARTITION PartitionNameList [COLUMNS ColumnNameList|PREDICATE COLUMNS|ALL COLUMNS] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

##### 動的プルーニング モードでパーティション テーブルの統計を収集する {#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode)でパーティション化されたテーブルにアクセスすると、TiDB は GlobalStats と呼ばれるテーブル レベルの統計を収集します。現在、GlobalStats はすべてのパーティションの統計から集計されています。動的プルーニング モードでは、パーティションテーブルの統計の更新により、GlobalStats の更新がトリガーされる可能性があります。

> **注記：**
>
> -   GlobalStats 更新がトリガーされると、次のようになります。
>
>     -   一部のパーティションに統計がない場合 (未分析の新しいパーティションなど)、GlobalStats の生成は中断され、パーティションで利用可能な統計がないことを示す警告メッセージが表示されます。
>     -   一部の列の統計が特定のパーティションに存在しない場合 (これらのパーティションでの分析に別の列が指定されている)、これらの列の統計が集計されるときに GlobalStats の生成が中断され、特定のパーティションに一部の列の統計が存在しないことを示す警告メッセージが表示されます。パーティション。
> -   動的プルーニング モードでは、パーティションとテーブルの分析構成が同じである必要があります。したがって、 `ANALYZE TABLE TableName PARTITION PartitionNameList`ステートメントの後に`COLUMNS`構成を指定するか、 `WITH`後に`OPTIONS`構成を指定すると、TiDB はそれらを無視して警告を返します。

#### 増分コレクション {#incremental-collection}

完全収集後の分析速度を向上させるために、増分収集を使用して、時間列などの単調非減少列に新しく追加されたセクションを分析できます。

> **注記：**
>
> -   現在、増分コレクションはインデックスに対してのみ提供されています。
> -   増分コレクションを使用する場合は、テーブルに操作が`INSERT`だけ存在すること、およびインデックス列に新しく挿入された値が単調非減少であることを確認する必要があります。そうしないと、統計情報が不正確になる可能性があり、TiDB オプティマイザーによる適切な実行プランの選択に影響します。

次の構文を使用して増分収集を実行できます。

-   all `IndexNameLists` in `TableName`のインデックス列の統計を増分収集するには、次のようにします。

    ```sql
    ANALYZE INCREMENTAL TABLE TableName INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

-   all `PartitionNameLists` in `TableName`のパーティションのインデックス列に関する統計を増分収集するには、次のようにします。

    ```sql
    ANALYZE INCREMENTAL TABLE TableName PARTITION PartitionNameList INDEX [IndexNameList] [WITH NUM BUCKETS|TOPN|CMSKETCH DEPTH|CMSKETCH WIDTH]|[WITH NUM SAMPLES|WITH FLOATNUM SAMPLERATE];
    ```

### 自動更新 {#automatic-update}

<CustomContent platform="tidb">

`INSERT` 、 `DELETE` 、または`UPDATE`ステートメントの場合、TiDB は行数と変更された行数を自動的に更新します。 TiDB はこの情報を定期的に保持し、更新サイクルは 20 * [`stats-lease`](/tidb-configuration-file.md#stats-lease)です。デフォルト値`stats-lease`は`3s`です。値を`0`に指定すると、TiDB は統計の自動更新を停止します。

</CustomContent>

<CustomContent platform="tidb-cloud">

`INSERT` 、 `DELETE` 、または`UPDATE`ステートメントの場合、TiDB は行数と変更された行数を自動的に更新します。 TiDB はこの情報を定期的に保持し、更新サイクルは 20 * `stats-lease`です。デフォルト値`stats-lease`は`3s`です。

</CustomContent>

### 関連するシステム変数 {#relevant-system-variables}

統計の自動更新に関連する 3 つのシステム変数は次のとおりです。

| システム変数                                                                                                              | デフォルト値        | 説明                                                                          |
| ------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------------------- |
| [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio)                                           | 0.5           | 自動更新の閾値                                                                     |
| [`tidb_auto_analyze_start_time`](/system-variables.md#tidb_auto_analyze_start_time)                                 | `00:00 +0000` | TiDBが自動アップデートできる1日の開始時刻                                                     |
| [`tidb_auto_analyze_end_time`](/system-variables.md#tidb_auto_analyze_end_time)                                     | `23:59 +0000` | TiDB が自動更新できる 1 日の終了時刻                                                      |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640) | `1`           | パーティションテーブルを分析するとき (つまり、パーティションテーブルの統計を自動的に更新するとき)、TiDB が自動的に分析するパーティションの数。 |

テーブル内の`tbl`の合計行数に対する変更された行数の比率が`tidb_auto_analyze_ratio`より大きく、現在時刻が`tidb_auto_analyze_start_time`から`tidb_auto_analyze_end_time`の間の場合、TiDB はバックグラウンドで`ANALYZE TABLE tbl`ステートメントを実行して、このステートメントに関する統計を自動的に更新します。テーブル。

小さなテーブル上の少量のデータを変更すると自動更新が頻繁にトリガーされる状況を避けるため、テーブルの行数が 1000 未満の場合、そのようなデータ変更は TiDB での自動更新をトリガーしません。 `SHOW STATS_META`ステートメントを使用すると、テーブル内の行数を表示できます。

> **注記：**
>
> 現在、自動更新では手動`ANALYZE`で入力した設定項目は記録されません。したがって、 `WITH`構文を使用して`ANALYZE`の収集動作を制御する場合は、統計を収集するためにスケジュールされたタスクを手動で設定する必要があります。

#### 自動アップデートを無効にする {#disable-automatic-update}

統計の自動更新が過剰なリソースを消費し、オンライン アプリケーションの操作に影響を与える場合は、 [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)システム変数を使用して無効にすることができます。

#### バックグラウンドの<code>ANALYZE</code>タスクを終了する {#terminate-background-code-analyze-code-tasks}

TiDB v6.0 以降、TiDB は、 `KILL`ステートメントを使用してバックグラウンドで実行されている`ANALYZE`タスクを終了することをサポートしています。バックグラウンドで実行されている`ANALYZE`タスクが大量のリソースを消費し、アプリケーションに影響を与えていることが判明した場合は、次の手順を実行して`ANALYZE`タスクを終了できます。

1.  次の SQL ステートメントを実行します。

    ```sql
    SHOW ANALYZE STATUS
    ```

    結果の`instance`列目と`process_id`列目を確認すると、TiDBインスタンスのアドレスとバックグラウンド`ANALYZE`タスクのタスク`ID`取得できます。

2.  バックグラウンドで実行されている`ANALYZE`タスクを終了します。

    <CustomContent platform="tidb">

    -   [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が`true` (デフォルトでは`true` ) の場合、 `KILL TIDB ${id};`ステートメントを直接実行できます。9 は、前のステップ`ID`取得したバックグラウンド`ANALYZE`タスクの`${id}`です。
    -   `enable-global-kill`が`false`の場合、クライアントを使用してバックエンド`ANALYZE`タスクを実行している TiDB インスタンスに接続し、その後`KILL TIDB ${id};`ステートメントを実行する必要があります。クライアントを使用して別の TiDB インスタンスに接続する場合、またはクライアントと TiDB クラスターの間にプロキシがある場合、 `KILL`ステートメントはバックグラウンド`ANALYZE`タスクを終了できません。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    `ANALYZE`タスクを終了するには、 `KILL TIDB ${id};`ステートメントを実行します`${id}`は、前のステップで取得したバックグラウンド`ANALYZE`タスクの`ID`です。

    </CustomContent>

`KILL`ステートメントの詳細については、 [`KILL`](/sql-statements/sql-statement-kill.md)を参照してください。

### <code>ANALYZE</code>同時実行性の制御 {#control-code-analyze-code-concurrency}

`ANALYZE`ステートメントを実行するとき、次のパラメーターを使用して同時実行性を調整し、システムへの影響を制御できます。

#### <code>tidb_build_stats_concurrency</code> {#code-tidb-build-stats-concurrency-code}

現在、 `ANALYZE`ステートメントを実行すると、タスクは複数の小さなタスクに分割されます。各タスクは 1 つの列またはインデックスに対してのみ機能します。 `tidb_build_stats_concurrency`パラメータを使用して、同時タスクの数を制御できます。デフォルト値は`4`です。

#### <code>tidb_distsql_scan_concurrency</code> {#code-tidb-distsql-scan-concurrency-code}

通常の列を分析する場合、 `tidb_distsql_scan_concurrency`パラメーターを使用して、一度に読み取られるリージョンの数を制御できます。デフォルト値は`15`です。

#### <code>tidb_index_serial_scan_concurrency</code> {#code-tidb-index-serial-scan-concurrency-code}

インデックス列を分析する場合、 `tidb_index_serial_scan_concurrency`パラメーターを使用して、一度に読み取られるリージョンの数を制御できます。デフォルト値は`1`です。

### ANALYZE 構成を保持する {#persist-analyze-configurations}

v5.4.0 以降、TiDB は一部の`ANALYZE`構成の永続化をサポートします。この機能を使用すると、既存の構成を将来の統計収集に簡単に再利用できます。

永続性をサポートする構成は次の`ANALYZE`です。

| 構成              | 対応するANALYZE構文                                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------ |
| ヒストグラムバケットの数    | バケット数あり                                                                                                            |
| トップNの数          | ナンバートップン付き                                                                                                         |
| サンプル数           | サンプル数あり                                                                                                            |
| サンプリングレート       | Floatnum サンプルを使用                                                                                                   |
| `ANALYZE`カラムタイプ | AnalyzeColumnOption ::= ( &#39;ALL COLUMNS&#39; | &#39;PREDICATE COLUMNS&#39; | &#39;COLUMNS&#39; ColumnNameList ) |
| `ANALYZE`列目     | ColumnNameList ::= 識別子 ( &#39;,&#39; 識別子 )*                                                                        |

#### ANALYZE 構成の永続性を有効にする {#enable-analyze-configuration-persistence}

<CustomContent platform="tidb">

`ANALYZE`構成永続機能はデフォルトで有効`ON`なっています (デフォルトでは、システム変数`tidb_analyze_version`は`2`は`tidb_persist_analyze_options`です)。

</CustomContent>

<CustomContent platform="tidb-cloud">

`ANALYZE`構成永続化機能はデフォルトでは無効になっています。この機能を有効にするには、システム変数`tidb_persist_analyze_options`が`ON`であることを確認し、システム変数`tidb_analyze_version`を`2`に設定します。

</CustomContent>

この機能を使用すると、ステートメントを手動で実行するときに`ANALYZE`ステートメントで指定された永続性構成を記録できます。一度記録されると、次回 TiDB が自動的に統計を更新するか、これらの構成を指定せずに統計を手動で収集するときに、TiDB は記録された構成に従って統計を収集します。

永続構成を指定して`ANALYZE`ステートメントを手動で複数回実行すると、TiDB は、最新の`ANALYZE`ステートメントで指定された新しい構成を使用して、以前に記録された永続構成を上書きします。

#### ANALYZE 構成の永続性を無効にする {#disable-analyze-configuration-persistence}

`ANALYZE`構成永続化機能を無効にするには、 `tidb_persist_analyze_options`システム変数を`OFF`に設定します。 `ANALYZE`構成永続機能は`tidb_analyze_version = 1`には適用できないため、設定`tidb_analyze_version = 1`によってこの機能を無効にすることもできます。

`ANALYZE`構成永続化機能を無効にしても、TiDB は永続化された構成レコードをクリアしません。したがって、この機能を再度有効にすると、TiDB は以前に記録された永続構成を使用して統計を収集し続けます。

> **注記：**
>
> `ANALYZE`構成永続化機能を再度有効にするときに、以前に記録された永続化構成が最新のデータに適用できなくなった場合は、 `ANALYZE`ステートメントを手動で実行して、新しい永続化構成を指定する必要があります。

### 統計を収集するためのメモリ割り当て {#the-memory-quota-for-collecting-statistics}

> **警告：**
>
> 現在、 `ANALYZE`メモリクォータは実験的機能であり、本番環境ではメモリ統計が不正確になる可能性があります。

TiDB v6.1.0 以降、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)を使用して、TiDB で統計を収集するためのメモリクォータを制御できます。

適切な値`tidb_mem_quota_analyze`設定するには、クラスターのデータ サイズを考慮してください。デフォルトのサンプリング レートを使用する場合、主に考慮すべき点は、列の数、列値のサイズ、TiDB のメモリ構成です。最大値と最小値を構成するときは、次の提案を考慮してください。

> **注記：**
>
> 以下の提案は参考用です。実際のシナリオに基づいて値を構成する必要があります。

-   最小値: TiDB が最も多くの列を含むテーブルから統計を収集する場合の最大メモリ使用量より大きくなければなりません。おおよその参考値: TiDB がデフォルト構成を使用して 20 列のテーブルから統計を収集する場合、最大メモリ使用量は約 800 MiB です。 TiDB がデフォルト構成を使用して 160 列のテーブルから統計を収集する場合、最大メモリ使用量は約 5 GiB です。
-   最大値: TiDB が統計を収集していない場合は、使用可能なメモリよりも小さい値にする必要があります。

### <code>ANALYZE</code>状態のビュー {#view-code-analyze-code-state}

`ANALYZE`ステートメントを実行すると、次の SQL ステートメントを使用して`ANALYZE`の現在の状態を表示できます。

```sql
SHOW ANALYZE STATUS [ShowLikeOrWhere]
```

このステートメントは`ANALYZE`の状態を返します。 `ShowLikeOrWhere`使用して、必要な情報をフィルタリングできます。

現在、 `SHOW ANALYZE STATUS`ステートメントは次の 11 列を返します。

| カラム名     | 説明                                                                                                  |
| :------- | :-------------------------------------------------------------------------------------------------- |
| テーブルスキーマ | データベース名                                                                                             |
| テーブル名    | テーブル名                                                                                               |
| パーティション名 | パーティション名                                                                                            |
| ジョブ情報    | タスク情報。インデックスが分析される場合、この情報にはインデックス名が含まれます。 `tidb_analyze_version =2`の場合、この情報にはサンプル レートなどの設定項目が含まれます。 |
| 処理済み行数   | 分析された行数                                                                                             |
| 始まる時間    | タスクの開始時刻                                                                                            |
| 州        | タスクの状態 ( `pending` 、 `running` 、 `finished` 、および`failed`を含む)                                        |
| 失敗の理由    | タスクが失敗した理由。実行が成功した場合、値は`NULL`になります。                                                                 |
| 実例       | タスクを実行する TiDB インスタンス                                                                                |
| プロセスID   | タスクを実行するプロセスID                                                                                      |

TiDB v6.1.0 以降、 `SHOW ANALYZE STATUS`ステートメントはクラスターレベルのタスクの表示をサポートします。 TiDB の再起動後でも、このステートメントを使用して再起動前のタスク レコードを表示できます。 TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンス レベルのタスクのみを表示でき、TiDB の再起動後にタスク レコードはクリアされます。

`SHOW ANALYZE STATUS`最新のタスク レコードのみを表示します。 TiDB v6.1.0 以降、システム テーブル`mysql.analyze_jobs`を通じて過去 7 日間の履歴タスクを表示できるようになりました。

[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)が設定され、TiDB バックグラウンドで実行されている自動`ANALYZE`タスクがこのしきい値を超えるメモリを使用すると、タスクは再試行されます。 `SHOW ANALYZE STATUS`ステートメントの出力で、失敗したタスクと再試行されたタスクを確認できます。

[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)が 0 より大きく、TiDB バックグラウンドで実行されている自動`ANALYZE`タスクにこのしきい値よりも時間がかかる場合、タスクは終了します。

```sql
mysql> SHOW ANALYZE STATUS [ShowLikeOrWhere];
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| Table_schema | Table_name | Partition_name | Job_info                                                                                  | Processed_rows | Start_time          | End_time            | State    | Fail_reason                                                                   |
+--------------+------------+----------------+-------------------------------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------------------------------------------------------------------------|
| test         | sbtest1    |                | retry auto analyze table all columns with 100 topn, 0.055 samplerate                      |        2000000 | 2022-05-07 16:41:09 | 2022-05-07 16:41:20 | finished | NULL                                                                          |
| test         | sbtest1    |                | auto analyze table all columns with 100 topn, 0.5 samplerate                              |              0 | 2022-05-07 16:40:50 | 2022-05-07 16:41:09 | failed   | analyze panic due to memory quota exceeds, please try with smaller samplerate |
```

## 統計のビュー {#view-statistics}

次のステートメントを使用して統計ステータスを表示できます。

### テーブルのメタデータ {#metadata-of-tables}

`SHOW STATS_META`ステートメントを使用すると、行の合計数と更新された行の数を表示できます。

```sql
SHOW STATS_META [ShowLikeOrWhere];
```

`ShowLikeOrWhereOpt`の構文は次のとおりです。

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

現在、 `SHOW STATS_META`ステートメントは次の 6 つの列を返します。

| カラム名             | 説明        |
| :--------------- | :-------- |
| `db_name`        | データベース名   |
| `table_name`     | テーブル名     |
| `partition_name` | パーティション名  |
| `update_time`    | アップデートの時間 |
| `modify_count`   | 変更された行の数  |
| `row_count`      | 総行数       |

> **注記：**
>
> TiDB が DML ステートメントに従って総行数と変更行数を自動的に更新する場合、 `update_time`も更新されます。したがって、 `update_time`必ずしも`ANALYZE`ステートメントが最後に実行された時刻を示すわけではありません。

### テーブルのヘルス状態 {#health-state-of-tables}

`SHOW STATS_HEALTHY`ステートメントを使用すると、テーブルの健全性状態をチェックし、統計の精度を大まかに見積もることができます。 `modify_count` &gt;= `row_count`の場合、ヘルス状態は 0 です。 `modify_count` &lt; `row_count`の場合、健康状態は (1 - `modify_count` / `row_count` ) * 100 になります。

構文は次のとおりです。

```sql
SHOW STATS_HEALTHY [ShowLikeOrWhere];
```

`SHOW STATS_HEALTHY`のあらすじは以下の通りです。

![ShowStatsHealthy](/media/sqlgram/ShowStatsHealthy.png)

現在、 `SHOW STATS_HEALTHY`ステートメントは次の 4 つの列を返します。

| カラム名             | 説明         |
| :--------------- | :--------- |
| `db_name`        | データベース名    |
| `table_name`     | テーブル名      |
| `partition_name` | パーティション名   |
| `healthy`        | テーブルの健全性状態 |

### 列のメタデータ {#metadata-of-columns}

`SHOW STATS_HISTOGRAMS`ステートメントを使用すると、すべての列のさまざまな値の数と`NULL`の数を表示できます。

構文は次のとおりです。

```sql
SHOW STATS_HISTOGRAMS [ShowLikeOrWhere]
```

このステートメントは、すべての列の異なる値の数と`NULL`の数を返します。 `ShowLikeOrWhere`使用して、必要な情報をフィルタリングできます。

現在、 `SHOW STATS_HISTOGRAMS`ステートメントは次の 10 列を返します。

| カラム名             | 説明                                                        |
| :--------------- | :-------------------------------------------------------- |
| `db_name`        | データベース名                                                   |
| `table_name`     | テーブル名                                                     |
| `partition_name` | パーティション名                                                  |
| `column_name`    | カラム名 ( `is_index`が`0`の場合) またはインデックス名 ( `is_index`が`1`の場合) |
| `is_index`       | インデックス列かどうか                                               |
| `update_time`    | アップデートの時間                                                 |
| `distinct_count` | 異なる値の数                                                    |
| `null_count`     | `NULL`という数字                                               |
| `avg_col_size`   | 列の平均長さ                                                    |
| 相関               | 列のピアソン相関係数と整数の主キー。2 つの列間の関連度を示します。                        |

### ヒストグラムのバケット {#buckets-of-histogram}

`SHOW STATS_BUCKETS`ステートメントを使用して、ヒストグラムの各バケットを表示できます。

構文は次のとおりです。

```sql
SHOW STATS_BUCKETS [ShowLikeOrWhere]
```

回路図は以下の通りです：

![SHOW STATS\_BUCKETS](/media/sqlgram/SHOW_STATS_BUCKETS.png)

このステートメントは、すべてのバケットに関する情報を返します。 `ShowLikeOrWhere`使用して必要な情報をフィルタリングできます。

現在、 `SHOW STATS_BUCKETS`ステートメントは次の 11 列を返します。

| カラム名             | 説明                                                                               |
| :--------------- | :------------------------------------------------------------------------------- |
| `db_name`        | データベース名                                                                          |
| `table_name`     | テーブル名                                                                            |
| `partition_name` | パーティション名                                                                         |
| `column_name`    | カラム名 ( `is_index`が`0`の場合) またはインデックス名 ( `is_index`が`1`の場合)                        |
| `is_index`       | インデックス列かどうか                                                                      |
| `bucket_id`      | バケットのID                                                                          |
| `count`          | バケットと前のバケットに該当するすべての値の数                                                          |
| `repeats`        | 最大値の出現数                                                                          |
| `lower_bound`    | 最小値                                                                              |
| `upper_bound`    | 最大値                                                                              |
| `ndv`            | バケット内の異なる値の数。 `tidb_analyze_version` = `1`の場合、 `ndv`常に`0`になりますが、これには実際の意味はありません。 |

### トップN情報 {#top-n-information}

`SHOW STATS_TOPN`ステートメントを使用すると、TiDB によって現在収集されている上位 N 情報を表示できます。

構文は次のとおりです。

```sql
SHOW STATS_TOPN [ShowLikeOrWhere];
```

現在、 `SHOW STATS_TOPN`ステートメントは次の 7 つの列を返します。

| カラム名             | 説明                                                        |
| ---------------- | --------------------------------------------------------- |
| `db_name`        | データベース名                                                   |
| `table_name`     | テーブル名                                                     |
| `partition_name` | パーティション名                                                  |
| `column_name`    | カラム名 ( `is_index`が`0`の場合) またはインデックス名 ( `is_index`が`1`の場合) |
| `is_index`       | インデックス列かどうか                                               |
| `value`          | この列の値                                                     |
| `count`          | 値が何回出現するか                                                 |

## 統計の削除 {#delete-statistics}

`DROP STATS`ステートメントを実行して統計を削除できます。

```sql
DROP STATS TableName
```

前述のステートメントは、 `TableName`のすべての統計を削除します。パーティションテーブルが指定されている場合、このステートメントは、このテーブル内のすべてのパーティションの統計と、動的プルーニング モードで生成された GlobalStats を削除します。

```sql
DROP STATS TableName PARTITION PartitionNameList;
```

この前述のステートメントは、 `PartitionNameList`で指定されたパーティションの統計のみを削除します。

```sql
DROP STATS TableName GLOBAL;
```

前述のステートメントは、指定されたテーブルの動的プルーニング モードで生成された GlobalStats のみを削除します。

## 負荷統計 {#load-statistics}

> **注記：**
>
> 統計のロードは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

デフォルトでは、列統計のサイズに応じて、TiDB は次のように異なる方法で統計をロードします。

-   少量のメモリを消費する統計 (count、distinctCount、nullCount など) の場合、列データが更新されている限り、TiDB は対応する統計を SQL 最適化ステージで使用するために自動的にメモリにロードします。
-   大量のメモリを消費する統計 (ヒストグラム、TopN、Count-Min Sketch など) の場合、SQL 実行のパフォーマンスを確保するために、TiDB はオンデマンドで統計を非同期にロードします。ヒストグラムを例に挙げます。 TiDB は、オプティマイザがその列のヒストグラム統計を使用する場合にのみ、列のヒストグラム統計をメモリにロードします。オンデマンドの非同期統計ロードは SQL 実行のパフォーマンスには影響しませんが、SQL 最適化のための不完全な統計を提供する可能性があります。

v5.4.0 以降、TiDB には統計の同期ロード機能が導入されました。この機能により、SQL ステートメントの実行時に TiDB が大きなサイズの統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期してロードできるようになり、SQL 最適化のための統計の完全性が向上します。

この機能を有効にするには、 [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)システム変数の値を、SQL 最適化が完全な列統計を同期的にロードするまで待機できるタイムアウト (ミリ秒単位) に設定します。この変数のデフォルト値は`100`で、この機能が有効であることを示します。

<CustomContent platform="tidb">

統計の同期読み込み機能を有効にした後、次のように機能をさらに構成できます。

-   SQL 最適化の待機時間がタイムアウトに達したときの TiDB の動作を制御するには、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更します。この変数のデフォルト値は`ON` 、タイムアウト後、SQL 最適化プロセスがどの列にもヒストグラム、TopN、または CMSketch 統計を使用しないことを示します。この変数が`OFF`に設定されている場合、タイムアウト後に SQL の実行は失敗します。
-   統計の同期ロード機能が同時に処理できる列の最大数を指定するには、TiDB 構成ファイルの[`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540)オプションの値を変更します。デフォルト値は`5`です。
-   同期ロード統計機能がキャッシュできる列リクエストの最大数を指定するには、TiDB 構成ファイルの[`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)オプションの値を変更します。デフォルト値は`1000`です。

TiDB の起動中、初期統計が完全にロードされる前に実行される SQL ステートメントには最適ではない実行プランが含まれる可能性があり、そのためパフォーマンスの問題が発生します。このような問題を回避するために、TiDB v7.1.0 では構成パラメーター[`force-init-stats`](/tidb-configuration-file.md#force-init-stats-new-in-v710)が導入されています。このオプションを使用すると、起動時に統計の初期化が完了した後にのみ TiDB がサービスを提供するかどうかを制御できます。このパラメータはデフォルトでは無効になっています。

> **警告：**
>
> 軽量統計の初期化は実験的機能です。本番環境で使用することはお勧めできません。この機能は予告なく変更または削除される場合があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

v7.1.0 以降、TiDB では軽量統計初期化のために[`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710)が導入されています。

-   `lite-init-stats`の値が`true`の場合、統計の初期化では、インデックスまたは列のヒストグラム、TopN、または Count-Min スケッチがメモリにロードされません。
-   `lite-init-stats`の値が`false`の場合、統計の初期化では、インデックスと主キーのヒストグラム、TopN、および Count-Min スケッチがメモリにロードされますが、非主キー列のヒストグラム、TopN、または Count-Min スケッチはメモリにロードされません。オプティマイザーが特定のインデックスまたは列のヒストグラム、TopN、および Count-Min スケッチを必要とする場合、必要な統計が同期または非同期でメモリにロードされます。

デフォルト値の`lite-init-stats` `false`で、これは軽量統計の初期化を無効にすることを意味します。 `lite-init-stats`から`true`設定すると、不必要な統計のロードが回避されるため、統計の初期化が高速化され、TiDBメモリの使用量が削減されます。

</CustomContent>

<CustomContent platform="tidb-cloud">

統計の同期ロード機能を有効にすると、 [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)システム変数の値を変更することで、SQL 最適化の待機時間がタイムアウトに達したときの TiDB の動作を制御できます。この変数のデフォルト値は`ON` 、タイムアウト後、SQL 最適化プロセスがどの列にもヒストグラム、TopN、または CMSketch 統計を使用しないことを示します。この変数が`OFF`に設定されている場合、タイムアウト後に SQL の実行は失敗します。

</CustomContent>

## 統計のインポートとエクスポート {#import-and-export-statistics}

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このセクションはTiDB Cloudには適用されません。

</CustomContent>

### 統計のエクスポート {#export-statistics}

統計をエクスポートするインターフェイスは次のとおりです。

-   `${db_name}`データベースの`${table_name}`テーブルの JSON 形式の統計を取得するには、次の手順を実行します。

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}

    例えば：

        curl -s http://127.0.0.1:10080/stats/dump/test/t1 -o /tmp/t1.json

-   特定の時点での`${db_name}`データベース内の`${table_name}`テーブルの JSON 形式の統計を取得するには、次の手順を実行します。

        http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}/${yyyyMMddHHmmss}

### 統計のインポート {#import-statistics}

> **注記：**
>
> MySQL クライアントを起動するときは、 `--local-infile=1`オプションを使用します。

通常、インポートされた統計は、エクスポート インターフェイスを使用して取得された JSON ファイルを参照します。

構文：

    LOAD STATS 'file_name'

`file_name`は、インポートする統計のファイル名です。

## ロック統計 {#lock-statistics}

> **警告：**
>
> 統計のロックは、現在のバージョンの実験的機能です。本番環境での使用はお勧めしません。

v6.5.0 以降、TiDB はロック統計をサポートしています。テーブルの統計がロックされると、テーブルの統計を変更できなくなり、そのテーブルに対して`ANALYZE`ステートメントを実行できなくなります。例えば：

table `t`を作成し、そこにデータを挿入します。テーブル`t`の統計がロックされていない場合、 `ANALYZE`ステートメントは正常に実行できます。

```sql
mysql> create table t(a int, b int);
Query OK, 0 rows affected (0.03 sec)

mysql> insert into t values (1,2), (3,4), (5,6), (7,8);
Query OK, 4 rows affected (0.00 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> analyze table t;
Query OK, 0 rows affected, 1 warning (0.02 sec)

mysql> show warnings;
+-------+------+-----------------------------------------------------------------+
| Level | Code | Message                                                         |
+-------+------+-----------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t |
+-------+------+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

テーブル`t`の統計をロックし、 `ANALYZE`を実行します。 `SHOW STATS_LOCKED`の出力から、テーブル`t`の統計がロックされていることがわかります。警告メッセージは、 `ANALYZE`ステートメントがテーブル`t`をスキップしたことを示しています。

```sql
mysql> lock stats t;
Query OK, 0 rows affected (0.00 sec)

mysql> show stats_locked;
+---------+------------+----------------+--------+
| Db_name | Table_name | Partition_name | Status |
+---------+------------+----------------+--------+
| test    | t          |                | locked |
+---------+------------+----------------+--------+
1 row in set (0.01 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 2 warnings (0.00 sec)

mysql> show warnings;
+---------+------+-----------------------------------------------------------------+
| Level   | Code | Message                                                         |
+---------+------+-----------------------------------------------------------------+
| Note    | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t |
| Warning | 1105 | skip analyze locked table: t                                    |
+---------+------+-----------------------------------------------------------------+
2 rows in set (0.00 sec)
```

テーブル`t`と`ANALYZE`の統計のロックを解除すると、再度正常に実行できるようになります。

```sql
mysql> unlock stats t;
Query OK, 0 rows affected (0.01 sec)

mysql> analyze table t;
Query OK, 0 rows affected, 1 warning (0.03 sec)

mysql> show warnings;
+-------+------+-----------------------------------------------------------------+
| Level | Code | Message                                                         |
+-------+------+-----------------------------------------------------------------+
| Note  | 1105 | Analyze use auto adjusted sample rate 1.000000 for table test.t |
+-------+------+-----------------------------------------------------------------+
1 row in set (0.00 sec)
```

## こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   [負荷統計](/sql-statements/sql-statement-load-stats.md)
-   [統計を削除](/sql-statements/sql-statement-drop-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [ステータスのロックを解除する](/sql-statements/sql-statement-unlock-stats.md)
-   [STATS_LOCKEDを表示](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [負荷統計](/sql-statements/sql-statement-load-stats.md)
-   [ロック統計](/sql-statements/sql-statement-lock-stats.md)
-   [ステータスのロックを解除する](/sql-statements/sql-statement-unlock-stats.md)
-   [STATS_LOCKEDを表示](/sql-statements/sql-statement-show-stats-locked.md)

</CustomContent>
