---
title: TiFlash Query Result Materialization
summary: TiFlashのクエリ結果をトランザクションに保存する方法を学びます。
---

# TiFlashクエリ結果のマテリアライゼーション {#tiflash-query-result-materialization}

このドキュメントでは、 `INSERT INTO SELECT`トランザクションでTiFlashクエリ結果を指定された TiDB テーブルに保存する方法を紹介します。

v6.5.0 以降、TiDB はTiFlashクエリ結果をテーブルに保存すること、つまりTiFlashクエリ結果のマテリアライゼーションをサポートしています`INSERT INTO SELECT`文の実行中に、TiDB が`SELECT`サブクエリをTiFlashにプッシュダウンすると、 TiFlashクエリ結果を`INSERT INTO`句で指定された TiDB テーブルに保存できます。v6.5.0 より前のバージョンの TiDB では、 TiFlashクエリ結果は読み取り専用であるため、 TiFlashクエリ結果を保存する場合は、アプリケーション レベルから結果を取得してから、別のトランザクションまたはプロセスで保存する必要があります。

> **注記：**
>
> デフォルトでは（ [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50) ）、オプティマイザは[SQL モード](/sql-mode.md)とTiFlashレプリカのコスト見積もりに基づいて、クエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。
>
> -   現在のセッションの[SQL モード](/sql-mode.md)厳密でない場合 (つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`と`STRICT_ALL_TABLES`が含まれていない場合)、オプティマイザは、 TiFlashレプリカのコスト見積もりに基づいて、 `INSERT INTO SELECT`の`SELECT`サブクエリをTiFlashにプッシュダウンするかどうかをインテリジェントに決定します。 このモードでは、オプティマイザのコスト見積もりを無視し、クエリがTiFlashにプッシュダウンされるようにするには、 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51)システム変数を`ON`に設定できます。
> -   現在のセッションの[SQL モード](/sql-mode.md)が厳密な場合 (つまり、 `sql_mode`値に`STRICT_TRANS_TABLES`または`STRICT_ALL_TABLES`いずれかが含まれている場合)、 `INSERT INTO SELECT`の`SELECT`サブクエリをTiFlashにプッシュダウンすることはできません。

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

たとえば、次の`INSERT INTO SELECT`ステートメントを使用して、 `SELECT`番目の句のテーブル`t1`からのクエリ結果をテーブル`t2`に保存できます。

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 一般的な推奨使用シナリオ {#typical-and-recommended-usage-scenarios}

-   効率的なBIソリューション

    多くの BI アプリケーションでは、分析クエリ要求が非常に重くなります。たとえば、多くのユーザーが同時にレポートにアクセスして更新する場合、BI アプリケーションは大量の同時クエリ要求を処理する必要があります。この状況に効果的に対処するには、 `INSERT INTO SELECT`使用してレポートのクエリ結果を TiDB テーブルに保存します。次に、レポートが更新されたときにエンドユーザーは結果テーブルから直接データをクエリできるため、複数の計算と分析が繰り返されるのを回避できます。同様に、履歴分析結果を保存することで、長時間の履歴データ分析の計算量をさらに削減できます。たとえば、毎日の売上利益を分析するために使用されるレポート`A`がある場合、 `INSERT INTO SELECT`を使用してレポート`A`の結果を結果テーブル`T`に保存できます。次に、過去 1 か月の売上利益を分析するためにレポート`B`を生成する必要があるときに、テーブル`T`の毎日の分析結果を直接使用できます。この方法では、計算量が大幅に削減されるだけでなく、クエリ応答速度が向上し、システム負荷が軽減されます。

-   TiFlashによるオンライン アプリケーションの提供

    TiFlashでサポートされる同時リクエストの数は、データの量とクエリの複雑さによって異なりますが、通常は 100 QPS を超えることはありません。1 `INSERT INTO SELECT`使用してTiFlashクエリ結果を保存し、クエリ結果テーブルを使用して同時オンライン リクエストをサポートできます。結果テーブル内のデータは、 TiFlash の同時実行制限を大幅に下回る低頻度 (たとえば、0.5 秒間隔) でバックグラウンドで更新できますが、データの鮮度は高いレベルに維持されます。

## 実行プロセス {#execution-process}

-   `INSERT INTO SELECT`文の実行中、 TiFlash はまず`SELECT`句のクエリ結果をクラスター内の TiDBサーバーに返し、次にその結果をターゲット テーブルに書き込みます。ターゲット テーブルにはTiFlashレプリカを含めることができます。
-   `INSERT INTO SELECT`ステートメントの実行により、 ACIDプロパティが保証されます。

## 制限 {#restrictions}

<CustomContent platform="tidb">

-   `INSERT INTO SELECT`ステートメントの TiDBメモリ制限は、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を使用して調整できます。v6.5.0 以降では、トランザクションメモリサイズを制御するために[`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)を使用することは推奨されません。

    詳細については[TiDBメモリ制御](/configure-memory-usage.md)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   `INSERT INTO SELECT`ステートメントの TiDBメモリ制限は、システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を使用して調整できます。v6.5.0 以降では、トランザクションメモリサイズを制御するために[`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit)を使用することは推奨されません。

    詳細については[TiDBメモリ制御](https://docs.pingcap.com/tidb/stable/configure-memory-usage)参照してください。

</CustomContent>

-   TiDB では、 `INSERT INTO SELECT`ステートメントの同時実行性に厳しい制限はありませんが、次の点を考慮することをお勧めします。

    -   「書き込みトランザクション」が 1 GiB に近いなど大きい場合は、同時実行を 10 以下に制御することをお勧めします。
    -   「書き込みトランザクション」が 100 MiB 未満などのように小さい場合は、同時実行を 30 以下に制御することをお勧めします。
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
('2023-1-6 12:2:3', 'cus002', 20.86),
('2023-1-7 12:2:3', 'cus004', 120.56),
('2023-1-8 12:2:3', 'cus005', 320.16);

-- Execute the following SQL statement 13 times to insert a cumulative total of 65,536 rows into the table.
INSERT INTO detail_data SELECT * FROM detail_data;
```

毎日の分析結果を保存します:

```sql
SET @@sql_mode='NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO';

INSERT INTO daily_data (rec_date, customer_id, daily_fee)
SELECT DATE(ts), customer_id, sum(detail_fee) FROM detail_data WHERE DATE(ts) > DATE('2023-1-1 12:2:3') GROUP BY DATE(ts), customer_id;
```

日次分析データに基づいて月次データを分析します。

```sql
SELECT MONTH(rec_date), customer_id, sum(daily_fee) FROM daily_data GROUP BY MONTH(rec_date), customer_id;
```

上記の例では、日次分析結果をマテリアライズして日次結果テーブルに保存し、それに基づいて月次データ分析を高速化することで、データ分析の効率を向上させます。
