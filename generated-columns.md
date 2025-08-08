---
title: Generated Columns
summary: 生成された列の使用方法を学習します。
---

# 生成された列 {#generated-columns}

このドキュメントでは、生成された列の概念と使用法について説明します。

## 基本概念 {#basic-concepts}

一般的な列とは異なり、生成列の値は列定義内の式によって計算されます。生成列を挿入または更新する際には、値を割り当てることはできず、 `DEFAULT`のみを使用できます。

生成列には、仮想生成列と保存列の2種類があります。仮想生成列はstorageを占有せず、読み取り時に計算されます。保存列は書き込み（挿入または更新）時に計算され、storageを占有します。仮想生成列と比較すると、保存列は読み取りパフォーマンスに優れていますが、より多くのディスク容量を消費します。

生成された列が仮想列であるか保存列であるかに関係なく、生成された列にインデックスを作成できます。

## 使用法 {#usage}

生成された列の主な用途の 1 つは、JSON データ型からデータを抽出し、そのデータにインデックスを付けることです。

MySQL 8.0とTiDBの両方において、JSON型の列を直接インデックスすることはできません。つまり、以下のテーブルスキーマは**サポートされていません**。

```sql
CREATE TABLE person (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address_info JSON,
    KEY (address_info)
);
```

JSON 列にインデックスを付けるには、まず生成された列として抽出する必要があります。

`address_info`の`city`フィールドを例にすると、仮想生成列を作成し、そのインデックスを追加できます。

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

このテーブルでは、 `city`番目の列は**仮想生成列**であり、インデックスが設定されています。次のクエリでは、このインデックスを使用することで実行速度を向上させることができます。

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

クエリ実行プランからは、条件`city ='Beijing'`満たす行の`HANDLE`読み込むために`city`インデックスが使用され、次にこの`HANDLE`使用して行のデータを読み込んでいることがわかります。

パス`$.city`にデータが存在しない場合、 `JSON_EXTRACT` `NULL`返します。 `city`必ず`NOT NULL`になるという制約を適用したい場合は、次のように仮想生成列を定義します。

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

`INSERT`と`UPDATE`ステートメントはどちらも仮想列の定義をチェックします。検証に合格しない行はエラーを返します。

```sql
mysql> INSERT INTO person (name, address_info) VALUES ('Morgan', JSON_OBJECT('Country', 'Canada'));
ERROR 1048 (23000): Column 'city' cannot be null
```

## 生成列インデックスの置換ルール {#generated-columns-index-replacement-rule}

クエリ内の式がインデックス付きの生成列と厳密に同等である場合、TiDB は式を対応する生成列に置き換え、実行プランの構築時にオプティマイザーがそのインデックスを考慮できるようにします。

次の例では、式`a+1`に対して生成列を作成し、インデックスを追加します。列`a`の型はint、列`a+1`の型はbigintです。生成列の型がintに設定されている場合、置換は行われません。型変換ルールについては、 [式評価の型変換](/functions-and-operators/type-conversion-in-expression-evaluation.md)参照してください。

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
> 置換対象の式と生成列の両方が文字列型で長さが異なる場合でも、システム変数[`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)を`ON`に設定することで式を置換できます。このシステム変数を設定する際は、生成列によって計算される値が生成列の定義を厳密に満たしていることを確認してください。そうでない場合、長さの違いによりデータが切り捨てられ、誤った結果になる可能性があります。GitHub の問題[＃35490](https://github.com/pingcap/tidb/issues/35490#issuecomment-1211658886)参照してください。

## 制限事項 {#limitations}

JSON と生成された列の現在の制限は次のとおりです。

-   保存された生成列を`ALTER TABLE`経由で追加することはできません。
-   `ALTER TABLE`文を使用して、保存された生成列を通常の列に変換したり、通常の列を保存された生成列に変換したりすることはできません。
-   保存された生成列の式を`ALTER TABLE`ステートメントを通じて変更することはできません。
-   [JSON関数](/functions-and-operators/json-functions.md)すべてがサポートされているわけではありません。
-   [`NULLIF()`関数](/functions-and-operators/control-flow-functions.md#nullif)サポートされていません。代わりに[`CASE`関数](/functions-and-operators/control-flow-functions.md#case)使用してください。
-   現在、生成列インデックスの置換ルールは、生成列が仮想生成列である場合にのみ有効です。保存された生成列には適用されませんが、生成列自体を直接使用することでインデックスを使用することは可能です。
-   次の関数と式は生成された列の定義では許可されておらず、使用すると TiDB によってエラーが返されます。

    -   `RAND` 、 `UUID` 、 `CURRENT_TIMESTAMP`などの非決定論的な関数と式。
    -   `CONNECTION_ID`や`CURRENT_USER`など、セッション固有またはグローバル状態に依存する関数。
    -   `GET_LOCK` 、 `RELEASE_LOCK` 、 `SLEEP`など、システム状態に影響を与えたり、システムとの対話を実行したりする関数。
