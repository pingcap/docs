---
title: Generated Columns
summary: Learn how to use generated columns.
---

# 生成された列 {#generated-columns}

> **警告：**
>
> これはまだ実験的機能です。本番環境で使用することは**お**勧めしません。

このドキュメントでは、生成された列の概念と使用法を紹介します。

## 基本概念 {#basic-concepts}

一般的な列とは異なり、生成された列の値は、列定義の式によって計算されます。生成された列を挿入または更新する場合、値を割り当てることはできず、 `DEFAULT`のみを使用してください。

生成される列には、仮想列と格納列の 2 種類があります。仮想生成列はstorageを占有せず、読み取り時に計算されます。格納された生成列は、書き込み時 (挿入または更新時) に計算され、 storageを占有します。仮想生成列と比較して、格納された生成列は読み取りパフォーマンスが優れていますが、より多くのディスク領域を占有します。

仮想列か格納列かに関係なく、生成された列に索引を作成できます。

## 使用法 {#usage}

生成された列の主な用途の 1 つは、JSON データ型からデータを抽出し、データのインデックスを作成することです。

MySQL 5.7と TiDB の両方で、JSON 型の列に直接インデックスを作成することはできません。つまり、次のテーブル スキーマは**サポートされていません**。

{{< copyable "" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

JSON 列にインデックスを付けるには、最初にそれを生成された列として抽出する必要があります。

例として`address_info`の`city`フィールドを使用すると、仮想生成列を作成し、それにインデックスを追加できます。

{{< copyable "" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))), -- virtual generated column
    -- city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) VIRTUAL, -- virtual generated column
    -- city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) STORED, -- stored generated column
    KEY (city)
);
```

このテーブルでは、 `city`列は**仮想生成列**であり、インデックスがあります。次のクエリでは、インデックスを使用して実行を高速化できます。

{{< copyable "" >}}

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

{{< copyable "" >}}

```sql
EXPLAIN SELECT name, id FROM person WHERE city = 'Beijing';
```

```sql
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| id                              | estRows | task      | access object                  | operator info                                               |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| Projection_4                    | 10.00   | root      |                                | test.person.name, test.person.id                            |
| └─IndexLookUp_10                | 10.00   | root      |                                |                                                             |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:person, index:city(city) | range:["Beijing","Beijing"], keep order:false, stats:pseudo |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:person                   | keep order:false, stats:pseudo                              |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
```

クエリ実行プランから、 `city`インデックスを使用して条件`city ='Beijing'`を満たす行の`HANDLE`を読み取り、次にこの`HANDLE`を使用して行のデータを読み取ることがわかります。

パス`$.city`にデータが存在しない場合、 `JSON_EXTRACT` `NULL`を返します。 `city` `NOT NULL`でなければならないという制約を適用する場合は、仮想生成列を次のように定義できます。

{{< copyable "" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    city VARCHAR(64) AS (JSON_UNQUOTE(JSON_EXTRACT(address_info, '$.city'))) NOT NULL,
    KEY (city)
);
```

## 生成された列の検証 {#validation-of-generated-columns}

`INSERT`と`UPDATE`ステートメントの両方で、仮想列の定義がチェックされます。検証に合格しない行はエラーを返します。

{{< copyable "" >}}

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## 生成された列のインデックス置換規則 {#generated-columns-index-replacement-rule}

クエリ内の式がインデックス付きの生成された列と厳密に同等である場合、TiDB は式を対応する生成された列に置き換えます。これにより、オプティマイザは実行計画の構築中にそのインデックスを考慮に入れることができます。

次の例では、式`a+1`の生成列を作成し、インデックスを追加します。 `a`の列の型は int で、 `a+1`の列の型は bigint です。生成された列の型が int に設定されている場合、置換は行われません。型変換規則については、 [式評価の型変換](/functions-and-operators/type-conversion-in-expression-evaluation.md)を参照してください。

```sql
create table t(a int);
desc select a+1 from t where a+1=3;
```

```sql
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Projection_4              | 8000.00  | root      |               | plus(test.t.a, 1)->Column#3    |
| └─TableReader_7           | 8000.00  | root      |               | data:Selection_6               |
|   └─Selection_6           | 8000.00  | cop[tikv] |               | eq(plus(test.t.a, 1), 3)       |
|     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)
```

```sql
alter table t add column b bigint as (a+1) virtual;
alter table t add index idx_b(b);
desc select a+1 from t where a+1=3;
```

```sql
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
| id                     | estRows | task      | access object           | operator info                               |
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                         | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t, index:idx_b(b) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+-------------------------+---------------------------------------------+
2 rows in set (0.01 sec)
```

> **ノート：**
>
> 置換する式と生成される列が両方とも文字列型で長さが異なる場合でも、システム変数[`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)を`ON`に設定することで式を置換できます。このシステム変数を構成するときは、生成された列によって計算された値が、生成された列の定義を厳密に満たしていることを確認してください。そうしないと、長さの違いによってデータが切り捨てられ、誤った結果になる可能性があります。 GitHub の問題[#35490](https://github.com/pingcap/tidb/issues/35490#issuecomment-1211658886)を参照してください。

## 制限事項 {#limitations}

JSON および生成された列の現在の制限は次のとおりです。

-   保存された生成列を`ALTER TABLE`から追加することはできません。
-   `ALTER TABLE`ステートメントを使用して格納された生成列を通常の列に変換することも、通常の列を格納された生成列に変換することもできません。
-   `ALTER TABLE`ステートメントを使用して、格納された生成列の式を変更することはできません。
-   [JSON関数](/functions-and-operators/json-functions.md)すべてがサポートされているわけではありません。
-   現在、生成列インデックス置換ルールは、生成列が仮想生成列の場合にのみ有効です。格納された生成列では無効ですが、生成列自体を直接使用してインデックスを使用することはできます。
