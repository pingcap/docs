---
title: Generated Columns
summary: 生成された列の使用方法を学習します。
---

# 生成された列 {#generated-columns}

このドキュメントでは、生成された列の概念と使用法について説明します。

## 基本概念 {#basic-concepts}

一般的な列とは異なり、生成された列の値は列定義内の式によって計算されます。生成された列を挿入または更新する場合、値を割り当てることはできず、 `DEFAULT`のみを使用できます。

生成列には、仮想生成列と保存列の 2 種類があります。仮想生成列はstorageを占有せず、読み取られるときに計算されます。保存列は、書き込まれる (挿入または更新される) ときに計算され、storageを占有します。仮想生成列と比較すると、保存列は読み取りパフォーマンスが優れていますが、より多くのディスク領域を占有します。

生成された列が仮想列であるか保存列であるかに関係なく、生成された列にインデックスを作成できます。

## 使用法 {#usage}

生成された列の主な用途の 1 つは、JSON データ型からデータを抽出し、そのデータにインデックスを付けることです。

MySQL 8.0 と TiDB の両方で、JSON 型の列を直接インデックスすることはできません。つまり、次のテーブル スキーマは**サポートされていません**。

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

JSON 列にインデックスを付けるには、まず生成された列として抽出する必要があります。

`address_info`の`city`フィールドを例にすると、仮想生成列を作成し、それにインデックスを追加できます。

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

このテーブルでは、 `city`列目は**仮想生成列**であり、インデックスがあります。次のクエリでは、インデックスを使用して実行を高速化できます。

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

クエリ実行プランからは、条件`city ='Beijing'`を満たす行の`HANDLE`読み取るために`city`インデックスが使用され、次にこの`HANDLE`を使用して行のデータを読み取ることがわかります。

パス`$.city`にデータが存在しない場合、 `JSON_EXTRACT`は`NULL`を返します。 `city`が`NOT NULL`でなければならないという制約を適用する場合は、次のように仮想生成列を定義できます。

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

`INSERT`と`UPDATE`ステートメントは両方とも仮想列の定義をチェックします。検証に合格しない行はエラーを返します。

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## 生成された列のインデックス置換ルール {#generated-columns-index-replacement-rule}

クエリ内の式がインデックス付きの生成列と厳密に同等である場合、TiDB は式を対応する生成列に置き換え、オプティマイザーが実行プランの構築時にそのインデックスを考慮できるようにします。

次の例では、式`a+1`に対して生成された列を作成し、インデックスを追加します。列`a`の型は int で、列`a+1`の型は bigint です。生成された列の型が int に設定されている場合、置換は行われません。型変換ルールについては、 [式評価の型変換](/functions-and-operators/type-conversion-in-expression-evaluation.md)を参照してください。

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
> 置換する式と生成された列の両方が文字列型で長さが異なる場合でも、システム変数[`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)を`ON`に設定することで式を置換できます。このシステム変数を構成するときは、生成された列によって計算された値が、生成された列の定義を厳密に満たしていることを確認してください。そうでない場合、長さの違いによりデータが切り捨てられ、結果が不正確になる可能性があります。GitHub の問題[＃35490](https://github.com/pingcap/tidb/issues/35490#issuecomment-1211658886)を参照してください。

## 制限事項 {#limitations}

JSON と生成された列の現在の制限は次のとおりです。

-   保存された生成列を`ALTER TABLE`経由で追加することはできません。
-   `ALTER TABLE`ステートメントを使用して、保存された生成列を通常の列に変換したり、通常の列を保存された生成列に変換したりすることはできません。
-   `ALTER TABLE`ステートメントを通じて、保存された生成列の式を変更することはできません。
-   [JSON関数](/functions-and-operators/json-functions.md)すべてがサポートされているわけではありません。
-   現在、生成列インデックスの置換ルールは、生成列が仮想生成列である場合にのみ有効です。保存された生成列では有効ではありませんが、生成列自体を直接使用することでインデックスを使用することができます。
