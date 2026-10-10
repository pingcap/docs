---
title: データリネージ
summary: "{{{ .lake }}} でデータリネージを有効化して探索する方法を学びます。"
---

# データリネージ

データリネージは、データがソースオブジェクトからターゲットオブジェクトへどのように移動するかを示します。これを使用すると、依存関係の把握、変更の影響評価、データパイプラインのトラブルシューティング、派生カラムのソース追跡が可能になります。

{{{ .lake }}} は、オブジェクトレベルとカラムレベルの両方の関係を記録します。

- **上流リネージ** は、オブジェクトにデータを供給するテーブル、ビュー、または stage を特定します。
- **下流リネージ** は、オブジェクトのデータを利用するオブジェクトを特定します。
- **カラムリネージ** は、ソースカラムと派生したターゲットカラムの対応関係を示します。

![{{{ .lake }}} におけるテーブルおよびカラムのリネージ](/media/tidb-cloud-lake/data-lineage.png)

## データリネージを有効化する {#enable-data-lineage}

{{{ .lake }}} は、**Lineage** タブ（**Data** > **Databases** > **databaseName** > **tableName**）をサポートする Warehouse のリネージ設定を管理します。

## リネージを生成する {#generate-lineage}

リネージを有効化すると、{{{ .lake }}} は `CREATE TABLE ... AS SELECT`、`CREATE VIEW`、`INSERT ... SELECT`、複数テーブルへの `INSERT`、`REPLACE`、`MERGE`、`COPY` などの操作によって作成された関係を自動的に記録します。ストリームは、その基盤となるテーブルに解決されます。

次の例では、2 ホップのリネージパスを作成します。

```sql
CREATE OR REPLACE DATABASE lineage_demo;

CREATE OR REPLACE TABLE lineage_demo.fact_orders (
    order_id BIGINT,
    customer_id BIGINT,
    amount DECIMAL(12, 2),
    order_time TIMESTAMP
);

CREATE OR REPLACE TABLE lineage_demo.agg_customer_sales AS
SELECT
    customer_id,
    sum(amount) AS total_amount,
    count(*) AS order_count,
    max(order_time) AS last_order_time
FROM lineage_demo.fact_orders
GROUP BY customer_id;

CREATE OR REPLACE TABLE lineage_demo.customer_segments AS
SELECT
    customer_id,
    total_amount,
    order_count,
    if(total_amount >= 1000, 'high_value', 'standard') AS segment,
    now() AS updated_at
FROM lineage_demo.agg_customer_sales;
```

## リネージを探索する {#explore-lineage}

{{{ .lake }}} で、Database Explorer からテーブルまたはビューを開き、**Lineage** タブを選択します。グラフには上流および下流のオブジェクトが表示され、カラムリネージが利用可能な場合はカラム間の接続も表示されます。

SQL でリネージを取得するには、[`GET_LINEAGE`](/tidb-cloud-lake/sql/get-lineage.md) テーブル関数を使用します。

```sql
SELECT
    distance,
    source_object_database,
    source_object_name,
    target_object_database,
    target_object_name
FROM GET_LINEAGE(
    'lineage_demo.agg_customer_sales',
    'TABLE',
    'UPSTREAM',
    2
)
ORDER BY distance;
```

カラムレベルのリネージについては、カラム名を修飾し、`COLUMN` ドメインを使用します。

```sql
SELECT
    distance,
    source_object_name,
    source_column_name,
    target_object_name,
    target_column_name
FROM GET_LINEAGE(
    'lineage_demo.customer_segments.segment',
    'COLUMN',
    'UPSTREAM',
    2
)
ORDER BY distance;
```

## 既存のビューのリネージを更新する {#refresh-lineage-for-existing-views}

リネージを有効化した後に作成されたビューは、自動的に追跡されます。すでにビューを含むデプロイでリネージを有効化した場合は、不足している関係または古くなった関係をプレビューしてから更新します。

```sql
REFRESH LINEAGE FOR ALL VIEWS DRY RUN;
REFRESH LINEAGE FOR ALL VIEWS;
```

この更新では、`default` カタログ内のすべてのビューのリネージが整合されます。変更が必要なビュー、または処理できなかったビューのみが報告され、変更不要のビューは出力されません。このコマンドにはグローバル `SUPER` 権限が必要です。出力の詳細については、[`REFRESH LINEAGE`](/tidb-cloud-lake/sql/refresh-lineage.md) を参照してください。

## 制限事項 {#limitations}

- `GET_LINEAGE` がたどれるのは最大 5 ホップです。
- システムオブジェクトおよび `information_schema` オブジェクトは、リネージのソースから除外されます。
- stage はオブジェクトレベルのリネージには含まれますが、stage 上のファイルフィールドでは安定したカラムレベルのマッピングは提供されません。
- 外部カタログのオブジェクトはエンドポイントとして表示されることがありますが、外部カタログの境界を越えてたどることはできません。
- 結果には、現在のロールから参照可能なオブジェクトのみが含まれます。