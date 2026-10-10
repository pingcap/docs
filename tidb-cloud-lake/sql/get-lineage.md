---
title: GET_LINEAGE
summary: テーブル、ビュー、stage、またはカラムの上流または下流のリネージを返します。返される各行は、リネージパス内の 1 つのソースからターゲットへの関係を表します。
---

# GET_LINEAGE

テーブル、ビュー、stage、またはカラムの上流または下流のリネージを返します。返される各行は、リネージパス内の 1 つのソースからターゲットへの関係を表します。

## 構文 {#syntax}

```sql
GET_LINEAGE(
    '<object_name>',
    '<object_domain>',
    '<direction>'
    [, <distance> ]
)
```

## 引数 {#arguments}

| 引数 | 説明 |
|----------|-------------|
| `object_name` | 開始対象のオブジェクトです。テーブルまたはビューには `[catalog.]database.object`、stage には `stage_name`、カラムには `[catalog.]database.object.column` を使用します。catalog または database を省略した名前では、現在のセッション値が使用されます。 |
| `object_domain` | オブジェクトタイプ: `TABLE`、`VIEW`、`STAGE`、または `COLUMN`。 |
| `direction` | `UPSTREAM` はソース方向へ追跡し、`DOWNSTREAM` は利用先方向へ追跡します。 |
| `distance` | 省略可能な、たどる hop 数の最大値です。`1` から `5` まで指定でき、デフォルトは `5` です。 |

引数は位置指定です。

## 出力カラム {#output-columns}

| カラム | 型 | 説明 |
|--------|------|-------|
| `source_object_catalog` | Nullable(String) | ソースオブジェクトを含む catalog。stage の場合は `NULL`。 |
| `source_object_database` | Nullable(String) | ソースオブジェクトを含む database。stage の場合は `NULL`。 |
| `source_object_name` | Nullable(String) | ソースオブジェクトの名前。 |
| `source_object_domain` | Nullable(String) | ソースオブジェクトのドメイン: `TABLE`、`VIEW`、または `STAGE`。 |
| `source_column_name` | Nullable(String) | カラムリネージにおけるソースカラム。それ以外は `NULL`。 |
| `source_status` | String | `ACTIVE`、またはソースカラムに masking policy がある場合は `MASKED`。 |
| `target_object_catalog` | Nullable(String) | ターゲットオブジェクトを含む catalog。stage の場合は `NULL`。 |
| `target_object_database` | Nullable(String) | ターゲットオブジェクトを含む database。stage の場合は `NULL`。 |
| `target_object_name` | Nullable(String) | ターゲットオブジェクトの名前。 |
| `target_object_domain` | Nullable(String) | ターゲットオブジェクトのドメイン: `TABLE`、`VIEW`、または `STAGE`。 |
| `target_column_name` | Nullable(String) | カラムリネージにおけるターゲットカラム。それ以外は `NULL`。 |
| `target_status` | String | `ACTIVE`、またはターゲットカラムに masking policy がある場合は `MASKED`。 |
| `distance` | Int32 | 要求されたオブジェクトからの hop 数です。直接の関係は距離 `1` です。 |
| `process` | Nullable(String) | 関係を作成した操作に関する JSON 形式のメタデータです。たとえば、query ID、query text、user、time、lineage kind などが含まれます。 |

## 例 {#examples}

このセクションでは、リネージを追跡するためのクエリ例を示します。

### 上流テーブルを探す {#find-upstream-tables}

このクエリは、`agg_customer_sales` に対して最大 2 hop 上流までを返します。

```sql
SELECT
    distance,
    source_object_catalog,
    source_object_database,
    source_object_name,
    source_object_domain,
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

### 下流カラムを探す {#find-downstream-columns}

このクエリは、`fact_orders.amount` がどこで使用されているかを追跡します。

```sql
SELECT
    distance,
    source_object_name,
    source_column_name,
    target_object_name,
    target_column_name
FROM GET_LINEAGE(
    'lineage_demo.fact_orders.amount',
    'COLUMN',
    'DOWNSTREAM',
    5
)
ORDER BY distance, target_object_name, target_column_name;
```

## 使用上の注意 {#usage-notes}

- オブジェクトが存在していても、記録されたリネージがない場合、この関数は行を返しません。
- 結果は、現在のロールのオブジェクト可視性に従ってフィルタリングされます。
- stage の関係はオブジェクトレベルのみです。staged file のフィールドは安定したカラムとして返されません。
- システムオブジェクトおよび `information_schema` オブジェクトは、リネージソースとして記録されません。
- 外部 catalog のオブジェクトは終端のエンドポイントとして返され、それ以上はたどられません。
- リネージが有効化される前から存在していたビューのリネージをバックフィルするには、[`REFRESH LINEAGE`](/tidb-cloud-lake/sql/refresh-lineage.md) を使用します。