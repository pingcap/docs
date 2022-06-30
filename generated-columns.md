---
title: Generated Columns
summary: Learn how to use generated columns.
---

# 生成された列 {#generated-columns}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

このドキュメントでは、生成された列の概念と使用法を紹介します。

## 基本概念 {#basic-concepts}

一般的な列とは異なり、生成された列の値は、列定義の式によって計算されます。生成された列を挿入または更新する場合、値を割り当てることはできませんが、 `DEFAULT`のみを使用してください。

生成される列には、仮想列と保存列の2種類があります。仮想的に生成された列はストレージを占有せず、読み取られるときに計算されます。保存された生成列は、書き込まれる（挿入または更新される）ときに計算され、ストレージを占有します。仮想で生成された列と比較して、保存された生成された列の読み取りパフォーマンスは向上しますが、より多くのディスク領域を占有します。

生成された列が仮想であるか保存されているかに関係なく、生成された列にインデックスを作成できます。

## 使用法 {#usage}

生成された列の主な用途の1つは、JSONデータ型からデータを抽出し、データにインデックスを付けることです。

MySQL 5.7とTiDBの両方で、JSON型の列に直接インデックスを付けることはできません。つまり、次のテーブルスキーマは**サポートされていません**。

{{< copyable "" >}}

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

JSON列にインデックスを付けるには、最初に生成された列としてJSON列を抽出する必要があります。

例として`address_info`の`city`フィールドを使用すると、仮想的に生成された列を作成し、そのインデックスを追加できます。

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

この表では、 `city`列は**仮想的に生成された列**であり、インデックスがあります。次のクエリでは、インデックスを使用して実行を高速化できます。

{{< copyable "" >}}

```sql
SELECT name, id FROM person WHERE city = 'Beijing';
```

{{< copyable "" >}}

```sql
EXPLAIN SELECT name, id FROM person WHERE city = 'Beijing';
```

```
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| id                              | estRows | task      | access object                  | operator info                                               |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
| Projection_4                    | 10.00   | root      |                                | test.person.name, test.person.id                            |
| └─IndexLookUp_10                | 10.00   | root      |                                |                                                             |
|   ├─IndexRangeScan_8(Build)     | 10.00   | cop[tikv] | table:person, index:city(city) | range:["Beijing","Beijing"], keep order:false, stats:pseudo |
|   └─TableRowIDScan_9(Probe)     | 10.00   | cop[tikv] | table:person                   | keep order:false, stats:pseudo                              |
+---------------------------------+---------+-----------+--------------------------------+-------------------------------------------------------------+
```

クエリ実行プランから、条件`city ='Beijing'`を満たす行の`HANDLE`を読み取るために`city`インデックスが使用され、次にこの`HANDLE`を使用して行のデータが読み取られることがわかります。

パス`$.city`にデータが存在しない場合、 `JSON_EXTRACT`は`NULL`を返します。 `city`が`NOT NULL`でなければならないという制約を適用する場合は、仮想生成列を次のように定義できます。

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

`INSERT`ステートメントと`UPDATE`ステートメントの両方が仮想列の定義をチェックします。検証に合格しない行はエラーを返します。

{{< copyable "" >}}

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## 生成された列のインデックス置換ルール {#generated-columns-index-replacement-rule}

クエリ内の式がインデックス付きの生成された列と同等である場合、TiDBは式を対応する生成された列に置き換え、オプティマイザーが実行プランの構築中にそのインデックスを考慮できるようにします。

たとえば、次の例では、式`a+1`の生成された列を作成し、インデックスを追加します。

```sql
create table t(a int);
desc select a+1 from t where a+1=3;
+---------------------------+----------+-----------+---------------+--------------------------------+
| id                        | estRows  | task      | access object | operator info                  |
+---------------------------+----------+-----------+---------------+--------------------------------+
| Projection_4              | 8000.00  | root      |               | plus(test.t.a, 1)->Column#3    |
| └─TableReader_7           | 8000.00  | root      |               | data:Selection_6               |
|   └─Selection_6           | 8000.00  | cop[tikv] |               | eq(plus(test.t.a, 1), 3)       |
|     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+---------------------------+----------+-----------+---------------+--------------------------------+
4 rows in set (0.00 sec)

alter table t add column b bigint as (a+1) virtual;
alter table t add index idx_b(b);
desc select a+1 from t where a+1=3;
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
> 式の型と生成された列の型が厳密に等しい場合にのみ、置換が実行されます。
>
> 上記の例では、 `a`の列型はintであり、 `a+1`の列型はbigintです。生成された列のタイプがintに設定されている場合、置換は行われません。
>
> 型変換規則については、 [式評価の型変換](/functions-and-operators/type-conversion-in-expression-evaluation.md)を参照してください。

## 制限事項 {#limitations}

JSONと生成された列の現在の制限は次のとおりです。

-   保存された生成列を`ALTER TABLE`から追加することはできません。
-   `ALTER TABLE`ステートメントを使用して、格納された生成列を通常の列に変換したり、通常の列を格納された生成列に変換したりすることはできません。
-   `ALTER TABLE`ステートメントを使用して、保存された生成列の式を変更することはできません。
-   [JSON関数](/functions-and-operators/json-functions.md)すべてがサポートされているわけではありません。
-   現在、生成された列インデックス置換ルールは、生成された列が仮想的に生成された列である場合にのみ有効です。保存された生成列では無効ですが、生成列自体を直接使用してインデックスを使用することはできます。
