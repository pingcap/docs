---
title: TiFlash Query Result Materialization
summary: Learn how to save the query results of TiFlash in a transaction.
---

# TiFlashクエリ結果の具体化 {#tiflash-query-result-materialization}

このドキュメントでは、 TiFlashクエリ結果を`INSERT INTO SELECT`トランザクションで指定した TiDB テーブルに保存する方法を紹介します。

v6.5.0 以降、TiDB は、 TiFlashクエリ結果のテーブルへの保存、つまりTiFlashクエリ結果の具体化をサポートします。 `INSERT INTO SELECT`ステートメントの実行中に、TiDB が`SELECT`サブクエリをTiFlashにプッシュダウンすると、 TiFlashクエリ結果を`INSERT INTO`句で指定された TiDB テーブルに保存できます。 v6.5.0 より前の TiDB バージョンの場合、 TiFlashクエリ結果は読み取り専用であるため、 TiFlashクエリ結果を保存する場合は、アプリケーション レベルから結果を取得し、別のトランザクションまたはプロセスに保存する必要があります。

> **注記：**
>
> デフォルト ( [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50) ) では、オプティマイザは[SQLモード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュするかどうかをインテリジェントに決定します。
>
> -   現在のセッションの[SQLモード](/sql-mode.md)厳密でない場合 (つまり、 `sql_mode`値に`STRICT_TRANS_TABLES` &#39; と`STRICT_ALL_TABLES`が含まれていない場合)、オプティマイザは、 TiFlashレプリカのコスト推定に基づいて、 `INSERT INTO SELECT`の`SELECT`サブクエリをTiFlashにプッシュするかどうかをインテリジェントに決定します。このモードでは、オプティマイザのコスト見積もりを無視してクエリをTiFlashにプッシュダウンするようにしたい場合は、 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)システム変数を`ON`に設定できます。
> -   現在のセッションの[SQLモード](/sql-mode.md)厳密である場合 (つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`または`STRICT_ALL_TABLES`含まれる)、 `INSERT INTO SELECT`の`SELECT`サブクエリをTiFlashにプッシュダウンすることはできません。

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

たとえば、次の`INSERT INTO SELECT`ステートメントを使用して、 `SELECT`句のテーブル`t1`のクエリ結果をテーブル`t2`に保存できます。

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 典型的な推奨される使用シナリオ {#typical-and-recommended-usage-scenarios}

-   効率的な BI ソリューション

    多くの BI アプリケーションでは、分析クエリ リクエストは非常に大量です。たとえば、多くのユーザーが同時にレポートにアクセスして更新する場合、BI アプリケーションは大量の同時クエリ リクエストを処理する必要があります。この状況に効果的に対処するには、 `INSERT INTO SELECT`を使用してレポートのクエリ結果を TiDB テーブルに保存します。その後、エンド ユーザーは、レポートの更新時に結果テーブルから直接データをクエリできるため、計算や分析を何度も繰り返す必要がなくなります。同様に、履歴分析結果を保存することで、長時間の履歴データ分析の計算量をさらに削減できます。たとえば、毎日の販売利益の分析に使用されるレポート`A`ある場合、 `INSERT INTO SELECT`を使用してレポート`A`の結果を結果テーブル`T`に保存できます。その後、先月の販売利益を分析するレポート`B`を生成する必要がある場合、表`T`の日次分析結果を直接使用できます。これにより、計算量が大幅に削減されるだけでなく、クエリの応答速度が向上し、システムの負荷も軽減されます。

-   TiFlashを使用してオンライン アプリケーションを提供する

    TiFlashでサポートされる同時リクエストの数は、データの量とクエリの複雑さによって異なりますが、通常は 100 QPS を超えません。 `INSERT INTO SELECT`を使用してTiFlashクエリ結果を保存し、クエリ結果テーブルを使用して高度な同時オンライン要求をサポートできます。結果テーブルのデータは、高いレベルのデータの鮮度を維持しながら、 TiFlash の同時実行制限を大幅に下回る低頻度 (たとえば、0.5 秒間隔) でバックグラウンドで更新できます。

## 実行プロセス {#execution-process}

-   `INSERT INTO SELECT`ステートメントの実行中、 TiFlash はまず`SELECT`句のクエリ結果をクラスター内の TiDBサーバーに返し、次にその結果をターゲット テーブル ( TiFlashレプリカを持つことができる) に書き込みます。
-   `INSERT INTO SELECT`ステートメントの実行により、 ACIDプロパティが保証されます。

## 制限 {#restrictions}

<CustomContent platform="tidb">

-   `INSERT INTO SELECT`ステートメントの TiDBメモリ制限は、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を使用して調整できます。 v6.5.0 以降、トランザクションメモリサイズを制御するために[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)を使用することは推奨されません。

    詳細については、 [TiDBメモリ制御](/configure-memory-usage.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `INSERT INTO SELECT`ステートメントの TiDBメモリ制限は、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を使用して調整できます。 v6.5.0 以降、トランザクションメモリサイズを制御するために[`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)を使用することは推奨されません。

    詳細については、 [TiDBメモリ制御](https://docs.pingcap.com/tidb/stable/configure-memory-usage)を参照してください。

</CustomContent>

-   TiDB には`INSERT INTO SELECT`ステートメントの同時実行性に対する厳密な制限はありませんが、次のプラクティスを考慮することをお勧めします。

    -   「書き込みトランザクション」が 1 GiB に近いなど大きい場合は、同時実行数を 10 以下に制御することをお勧めします。
    -   「書き込みトランザクション」が 100 MiB 未満など小さい場合は、同時実行数を 30 以下に制御することをお勧めします。
    -   テスト結果と特定の状況に基づいて同時実行性を決定します。

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

毎日の分析結果を保存します。

```sql
SET @@tidb_enable_tiflash_read_for_write_stmt=ON;

INSERT INTO daily_data (rec_date, customer_id, daily_fee)
SELECT DATE(ts), customer_id, sum(detail_fee) FROM detail_data WHERE DATE(ts) = CURRENT_DATE() GROUP BY DATE(ts), customer_id;
```

日次分析データに基づいて月次データを分析します。

```sql
SELECT MONTH(rec_date), customer_id, sum(daily_fee) FROM daily_data GROUP BY MONTH(rec_date), customer_id;
```

上記の例では、日次の分析結果を具体化して日次結果テーブルに保存し、それを基に月次のデータ分析を高速化し、データ分析の効率を向上させます。
