---
title: TiFlash Query Result Materialization
summary: Learn how to save the query results of TiFlash in a transaction.
---

# TiFlashクエリ結果の実体化 {#tiflash-query-result-materialization}

> **警告：**
>
> これは実験的機能であり、予告なしに変更または削除される可能性があります。構文と実装は、GA の前に変更される可能性があります。問題が発生した場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

このドキュメントでは、 TiFlashクエリの結果を指定された TiDB テーブルに`INSERT INTO SELECT`のトランザクションで保存する方法を紹介します。

v6.5.0 以降、TiDB はTiFlashクエリ結果のテーブルへの保存、つまりTiFlashクエリ結果の実体化をサポートしています。 `INSERT INTO SELECT`ステートメントの実行中に、TiDB が`SELECT`サブクエリをTiFlashにプッシュ ダウンすると、 TiFlashクエリの結果を`INSERT INTO`句で指定された TiDB テーブルに保存できます。 v6.5.0 より前のバージョンの TiDB では、 TiFlashクエリの結果は読み取り専用であるため、 TiFlashクエリの結果を保存する場合は、アプリケーション レベルから取得し、別のトランザクションまたはプロセスで保存する必要があります。

> **ノート：**
>
> -   デフォルト ( [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50) ) では、TiDB オプティマイザーは、クエリ コストに基づいて、クエリを TiKV またはTiFlashにプッシュ ダウンすることをインテリジェントに選択します。クエリがTiFlashにプッシュされるようにするには、システム変数[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)を`ON`に設定します。
> -   実験的段階では、この機能はデフォルトで無効になっています。この機能を有効にするには、システム変数[`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)から`ON`を設定します。

`INSERT INTO SELECT`の構文は次のとおりです。

```sql
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...
    [ON DUPLICATE KEY UPDATE assignment_list]value:
    {expr | DEFAULT}

assignment:
    col_name = valueassignment_list:
    assignment [, assignment] ...
```

たとえば、次の`INSERT INTO SELECT`ステートメントを使用して、 `SELECT`句のテーブル`t1`からのクエリ結果をテーブル`t2`に保存できます。

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 一般的および推奨される使用シナリオ {#typical-and-recommended-usage-scenarios}

-   効率的な BI ソリューション

    多くの BI アプリケーションでは、分析クエリ要求は非常に重いものです。たとえば、多数のユーザーが同時にレポートにアクセスして更新する場合、BI アプリケーションは多数の同時クエリ要求を処理する必要があります。この状況に効果的に対処するために、 `INSERT INTO SELECT`を使用して、レポートのクエリ結果を TiDB テーブルに保存できます。その後、エンド ユーザーは、レポートが更新されたときに結果テーブルから直接データをクエリできます。これにより、計算と分析を何度も繰り返す必要がなくなります。同様に、ヒストリカル解析結果を保存することで、長時間のヒストリカルデータ解析の計算量をさらに削減できます。たとえば、毎日の販売利益を分析するために使用されるレポート`A`ある場合、 `INSERT INTO SELECT`を使用してレポート`A`の結果を結果テーブル`T`に保存できます。次に、レポート`B`を生成して過去 1 か月の売上利益を分析する必要がある場合は、表`T`の日次分析結果を直接使用できます。これにより、計算量が大幅に削減されるだけでなく、クエリの応答速度が向上し、システムの負荷が軽減されます。

-   TiFlashを使用したオンライン アプリケーションの提供

    TiFlashでサポートされる同時リクエストの数は、データの量とクエリの複雑さによって異なりますが、通常は 100 QPS を超えません。 `INSERT INTO SELECT`を使用してTiFlashクエリ結果を保存し、クエリ結果テーブルを使用して高度な同時オンライン リクエストをサポートできます。結果テーブルのデータは、バックグラウンドで低頻度 (たとえば、0.5 秒間隔) で更新できます。これは、 TiFlash の同時実行制限を十分に下回っていますが、データの鮮度を高いレベルで維持しています。

## 実行プロセス {#execution-process}

-   `INSERT INTO SELECT`ステートメントの実行中、 TiFlash は最初に`SELECT`節のクエリ結果をクラスター内の TiDBサーバーに返し、次に結果をターゲット テーブルに書き込みます。ターゲット テーブルには、 TiFlashレプリカを含めることができます。
-   `INSERT INTO SELECT`ステートメントを実行すると、 ACIDプロパティが保証されます。

## 制限 {#restrictions}

<CustomContent platform="tidb">

-   `INSERT INTO SELECT`ステートメントの TiDBメモリ制限は、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を使用して調整できます。 v6.5.0 以降では、 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)を使用してトランザクションメモリサイズを制御することはお勧めしません。

    詳細については、 [TiDBメモリ制御](/configure-memory-usage.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `INSERT INTO SELECT`ステートメントの TiDBメモリ制限は、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を使用して調整できます。 v6.5.0 以降では、 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)を使用してトランザクションメモリサイズを制御することはお勧めしません。

    詳細については、 [TiDBメモリ制御](https://docs.pingcap.com/tidb/stable/configure-memory-usage)を参照してください。

</CustomContent>

-   TiDB には`INSERT INTO SELECT`ステートメントの同時実行性に厳密な制限はありませんが、次のプラクティスを考慮することをお勧めします。

    -   「書き込みトランザクション」が 1 GiB に近いなど、大きい場合は、同時実行数を 10 以下に制御することをお勧めします。
    -   「書き込みトランザクション」が 100 MiB 未満などの小さい場合は、同時実行数を 30 以下に制御することをお勧めします。
    -   テスト結果と特定の状況に基づいて同時実行数を決定します。

## 例 {#example}

データ定義:

```sql
CREATE TABLE detail_data (
    ts DATETIME,                -- Fee generation time
    customer_id VARCHAR(20),    -- Customer ID
    detail_fee DECIMAL(20,2));  -- Amount of fee

CREATE TABLE daily_data (
    rec_date DATE,              -- Date when data is collected
    customer_id VARCHAR(20),    -- Customer ID
    daily_fee DECIMAL(20,2));   -- Amount of fee for per day

ALTER TABLE detail_data SET TIFLASH REPLICA 1;
ALTER TABLE daily_data SET TIFLASH REPLICA 1;

-- ... (detail_data table continues updating)
INSERT INTO detail_data(ts,customer_id,detail_fee) VALUES
('2023-1-1 12:2:3', 'cus001', 200.86),
('2023-1-2 12:2:3', 'cus002', 100.86),
('2023-1-3 12:2:3', 'cus002', 2200.86),
('2023-1-4 12:2:3', 'cus003', 2020.86),
('2023-1-5 12:2:3', 'cus003', 1200.86),
('2023-1-6 12:2:3', 'cus002', 20.86);
```

毎日の分析結果を保存:

```sql
SET @@tidb_enable_tiflash_read_for_write_stmt=ON;

INSERT INTO daily_data (rec_date, customer_id, daily_fee)
SELECT DATE(ts), customer_id, sum(detail_fee) FROM detail_data WHERE DATE(ts) = CURRENT_DATE() GROUP BY DATE(ts), customer_id;
```

毎日の分析データに基づいて毎月のデータを分析します。

```sql
SELECT MONTH(rec_date), customer_id, sum(daily_fee) FROM daily_data GROUP BY MONTH(rec_date), customer_id;
```

上記の例では、日次分析結果を具体化し、日次結果表に保存します。これに基づいて、月次データ分析が高速化され、データ分析効率が向上します。
