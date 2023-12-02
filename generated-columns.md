---
title: Generated Columns
summary: Learn how to use generated columns.
---

# 生成された列 {#generated-columns}

このドキュメントでは、生成された列の概念と使用法を紹介します。

## 基本概念 {#basic-concepts}

一般的な列とは異なり、生成される列の値は列定義内の式によって計算されます。生成された列を挿入または更新する場合、値を割り当てることはできません。使用できるのは`DEFAULT`のみです。

生成される列には、仮想列と格納列の 2 種類があります。仮想生成列はstorageを占有せず、読み取り時に計算されます。格納された生成列は、書き込み (挿入または更新) 時に計算され、storageを占有します。仮想生成列と比較して、保存された生成列は読み取りパフォーマンスが優れていますが、より多くのディスク領域を消費します。

生成された列が仮想列であるか、格納されている列であるかに関係なく、その列にインデックスを作成できます。

## 使用法 {#usage}

生成された列の主な用途の 1 つは、JSON データ型からデータを抽出し、データにインデックスを付けることです。

MySQL 5.7と TiDB の両方で、JSON 型の列に直接インデックスを付けることはできません。つまり、次のテーブル スキーマは**サポートされていません**。

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

JSON 列にインデックスを付けるには、まず生成された列として抽出する必要があります。

例として`address_info`の`city`フィールドを使用すると、仮想生成列を作成し、その列にインデックスを追加できます。

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

このテーブルの`city`列は**仮想生成列**であり、インデックスがあります。次のクエリでは、インデックスを使用して実行を高速化できます。

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

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

クエリ実行プランから、条件`city ='Beijing'`を満たす行の`HANDLE`読み取るために`city`インデックスが使用され、その後、この`HANDLE`を使用して行のデータが読み取られることがわかります。

パス`$.city`にデータが存在しない場合、 `JSON_EXTRACT` `NULL`を返します。 `city`が`NOT NULL`でなければならないという制約を強制する場合は、次のように仮想生成列を定義できます。

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

`INSERT`と`UPDATE`ステートメントは両方とも仮想列定義をチェックします。検証に合格しない行はエラーを返します。

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## 生成された列のインデックス置換ルール {#generated-columns-index-replacement-rule}

クエリ内の式がインデックス付きの生成列と厳密に同等である場合、TiDB はその式を対応する生成列に置き換えます。これにより、オプティマイザーは実行プランの構築中にそのインデックスを考慮できるようになります。

次の例では、式`a+1`に対して生成された列を作成し、インデックスを追加します。 `a`の列の型は int で、 `a+1`の列の型は bigint です。生成された列の型が int に設定されている場合、置換は行われません。型変換規則については、 [式評価の型変換](/functions-and-operators/type-conversion-in-expression-evaluation.md)を参照してください。

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

> **注記：**
>
> 置換される式と生成される列が両方とも文字列型であるが長さが異なる場合でも、システム変数[`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)から`ON`を設定することで式を置換できます。このシステム変数を構成するときは、生成された列によって計算された値が生成された列の定義を厳密に満たしていることを確認してください。そうしないと、長さの違いによりデータが切り捨てられ、不正確な結果が生じる可能性があります。 GitHub の問題[#35490](https://github.com/pingcap/tidb/issues/35490#issuecomment-1211658886)を参照してください。

## 制限事項 {#limitations}

JSON と生成された列の現在の制限は次のとおりです。

-   `ALTER TABLE`を介して格納された生成列を追加することはできません。
-   `ALTER TABLE`ステートメントを使用して格納された生成列を通常の列に変換したり、通常の列を格納された生成列に変換したりすることはできません。
-   `ALTER TABLE`ステートメントを使用して、保存された生成列の式を変更することはできません。
-   すべての[JSON関数](/functions-and-operators/json-functions.md)サポートされているわけではありません。
-   現在、生成列インデックス置換ルールは、生成列が仮想生成列である場合にのみ有効です。格納された生成列では無効ですが、生成列自体を直接使用することでインデックスを引き続き使用できます。
