---
title: UNPIVOT
summary: UNPIVOT 操作は、カラムを行に変換することでテーブルを回転させます。
---

# UNPIVOT

`UNPIVOT` 操作は、カラムを行に変換することでテーブルを回転させます。

これは、2 つのカラム（テーブルまたはサブクエリから）とカラムのリストを受け取り、リストで指定された各カラムに対して 1 行を生成するリレーショナル演算子です。クエリでは、テーブル名またはサブクエリの後の FROM 句で指定します。

**See also:** [PIVOT](/tidb-cloud-lake/sql/pivot.md)

## 構文 {#syntax}

```sql
SELECT ...
FROM ...
    UNPIVOT ( <value_column>
    FOR <name_column> IN ( <column_list> ) )

[ ... ]
```

以下のとおりです。

* `<value_column>`: `<column_list>` に列挙されたカラムから抽出された値を格納するカラムです。
* `<name_column>`: 値の抽出元となったカラム名を格納するカラムです。
* `<column_list>`: UNPIVOT の対象となるカラムのリストで、カンマ区切りで指定します。`AS` を使うか、文字列リテラルだけを指定して、カラム名に別名を付けることもできます。

## 例 {#examples}

各従業員について、月ごとの個別カラムを UNPIVOT して、月ごとの単一の売上値を返してみましょう。

### データの作成と挿入 {#creating-and-inserting-data}

```sql
-- Create the unpivoted_monthly_sales table
CREATE TABLE unpivoted_monthly_sales(
  empid INT,
  jan INT,
  feb INT,
  mar INT,
  apr INT
);

-- Insert sales data
INSERT INTO unpivoted_monthly_sales VALUES
  (1, 10400,  8000, 11000, 18000),
  (2, 39500, 90700, 12000,  5300);
```

### UNPIVOT の使用 {#using-unpivot}

```sql
SELECT *
FROM unpivoted_monthly_sales
    UNPIVOT (amount
    FOR month IN (jan as 'Jan', feb AS 'Feb', mar 'MARCH', apr));
```

出力:

```sql
┌──────────────────────────────────────────────────────┐
│      empid      │       month      │      amount     │
├─────────────────┼──────────────────┼─────────────────┤
│               1 │ Jan              │           10400 │
│               1 │ Feb              │            8000 │
│               1 │ MARCH            │           11000 │
│               1 │ apr              │           18000 │
│               2 │ Jan              │           39500 │
│               2 │ Feb              │           90700 │
│               2 │ MARCH            │           12000 │
│               2 │ apr              │            5300 │
└──────────────────────────────────────────────────────┘

```