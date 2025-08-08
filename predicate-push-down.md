---
title: Predicates Push Down
summary: TiDB のロジック最適化ルールの 1 つである述語プッシュ ダウン (PPD) を導入します。
---

# Predicate Push Down（PPD） {#predicates-push-down-ppd}

このドキュメントでは、TiDBのロジック最適化ルールの一つである述語プッシュダウン（PPD）について紹介します。このドキュメントは、述語プッシュダウンを理解し、適用可能なシナリオと適用不可能なシナリオを把握することを目的としています。

PPD は、選択演算子をデータ ソースに可能な限り近づけて、データのフィルタリングをできるだけ早く完了します。これにより、データ転送や計算のコストが大幅に削減されます。

## 例 {#examples}

以下のケースでは、PPD の最適化について説明します。ケース 1、2、3 は PPD が適用可能なシナリオであり、ケース 4、5、6 は PPD が適用できないシナリオです。

### ケース1: 述語をstorageレイヤーにプッシュする {#case-1-push-predicates-to-storage-layer}

```sql
create table t(id int primary key, a int);
explain select * from t where a < 1;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 3323.33  | root      |               | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

このクエリでは、述語`a < 1` TiKVレイヤーにプッシュダウンしてデータをフィルター処理すると、ネットワーク転送のオーバーヘッドを削減できます。

### ケース2: 述語をstorageレイヤーにプッシュする {#case-2-push-predicates-to-storage-layer}

```sql
create table t(id int primary key, a int not null);
explain select * from t where a < substring('123', 1, 1);
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 3323.33  | root      |               | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
```

このクエリはケース1のクエリと同じ実行プランを持ちます。これは、述語`a < substring('123', 1, 1)`の`substring`の入力パラメータが定数であるため、事前に計算できるためです。その後、述語は同等の述語`a < 1`に簡略化されます。その後、TiDBは`a < 1` TiKVにプッシュダウンできます。

### ケース3: 述語を結合演算子の下にプッシュする {#case-3-push-predicates-below-join-operator}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t join s on t.a = s.a where t.a < 1;
+------------------------------+----------+-----------+---------------+--------------------------------------------+
| id                           | estRows  | task      | access object | operator info                              |
+------------------------------+----------+-----------+---------------+--------------------------------------------+
| HashJoin_8                   | 4154.17  | root      |               | inner join, equal:[eq(test.t.a, test.s.a)] |
| ├─TableReader_15(Build)      | 3323.33  | root      |               | data:Selection_14                          |
| │ └─Selection_14             | 3323.33  | cop[tikv] |               | lt(test.s.a, 1)                            |
| │   └─TableFullScan_13       | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo             |
| └─TableReader_12(Probe)      | 3323.33  | root      |               | data:Selection_11                          |
|   └─Selection_11             | 3323.33  | cop[tikv] |               | lt(test.t.a, 1)                            |
|     └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo             |
+------------------------------+----------+-----------+---------------+--------------------------------------------+
7 rows in set (0.00 sec)
```

このクエリでは、述語`t.a < 1`結合の下にプッシュして事前にフィルタリングすることで、結合の計算オーバーヘッドを削減できます。

さらに、このSQL文では内部結合が実行され、条件`ON`は`t.a = s.a`です。述語`s.a <1` `t.a < 1`から導出され、結合演算子の下のテーブル`s`にプッシュダウンされます。テーブル`s`フィルタリングすることで、結合の計算オーバーヘッドをさらに削減できます。

### ケース4:storage層でサポートされていない述語はプッシュダウンできない {#case-4-predicates-that-are-not-supported-by-storage-layers-cannot-be-pushed-down}

```sql
create table t(id int primary key, a varchar(10) not null);
desc select * from t where truncate(a, " ") = '1';
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
| id                      | estRows  | task      | access object | operator info                                     |
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
| Selection_5             | 8000.00  | root      |               | eq(truncate(cast(test.t.a, double BINARY), 0), 1) |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6                              |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                    |
+-------------------------+----------+-----------+---------------+---------------------------------------------------+
```

このクエリには述語`truncate(a, " ") = '1'`があります。

`explain`結果から、述語が計算のために TiKV にプッシュダウンされていないことがわかります。これは、TiKV コプロセッサが組み込み関数`truncate`サポートしていないためです。

### ケース5: 外部結合の内部テーブルの述語はプッシュダウンできない {#case-5-predicates-of-inner-tables-on-the-outer-join-can-t-be-pushed-down}

```sql
create table t(id int primary key, a int not null);
create table s(id int primary key, a int not null);
explain select * from t left join s on t.a = s.a where s.a is null;
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
| id                            | estRows  | task      | access object | operator info                                   |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
| Selection_7                   | 10000.00 | root      |               | isnull(test.s.a)                                |
| └─HashJoin_8                  | 12500.00 | root      |               | left outer join, equal:[eq(test.t.a, test.s.a)] |
|   ├─TableReader_13(Build)     | 10000.00 | root      |               | data:TableFullScan_12                           |
|   │ └─TableFullScan_12        | 10000.00 | cop[tikv] | table:s       | keep order:false, stats:pseudo                  |
|   └─TableReader_11(Probe)     | 10000.00 | root      |               | data:TableFullScan_10                           |
|     └─TableFullScan_10        | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo                  |
+-------------------------------+----------+-----------+---------------+-------------------------------------------------+
6 rows in set (0.00 sec)
```

このクエリでは、内部テーブル`s`に述語`s.a is null`あります。

`explain`結果から、述語が結合演算子の下にプッシュされていないことがわかります。これは、外部結合によって`on`番目の条件が満たされない場合に内部テーブルに`NULL`値が代入され、述語`s.a is null`結合後の結果をフィルタリングするために使用されているためです。述語7が結合演算子の下の内部テーブルにプッシュダウンされると、実行プランは元のプランと同等ではなくなります。

### ケース6: ユーザー変数を含む述語はプッシュダウンできない {#case-6-the-predicates-which-contain-user-variables-cannot-be-pushed-down}

```sql
create table t(id int primary key, a char);
set @a = 1;
explain select * from t where a < @a;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| Selection_5             | 8000.00  | root      |               | lt(test.t.a, getvar("a"))      |
| └─TableReader_7         | 10000.00 | root      |               | data:TableFullScan_6           |
|   └─TableFullScan_6     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

このクエリでは、テーブル`t`に述語`a < @a`あります。述語の`@a`ユーザー変数です。

`explain`結果からわかるように、述語はケース 2 とは異なり、ケース`a < 1`に簡略化されて TiKV にプッシュダウンされます。これは、ユーザー変数`@a`の値が計算中に変化する可能性があり、TiKV がその変化を認識しないためです。そのため、TiDB は`@a` `1`に置き換えず、TiKV にプッシュダウンしません。

理解を助ける例は次のとおりです。

```sql
create table t(id int primary key, a int);
insert into t values(1, 1), (2,2);
set @a = 1;
select id, a, @a:=@a+1 from t where a = @a;
+----+------+----------+
| id | a    | @a:=@a+1 |
+----+------+----------+
|  1 |    1 | 2        |
|  2 |    2 | 3        |
+----+------+----------+
2 rows in set (0.00 sec)
```

このクエリからわかるように、 `@a`の値はクエリの実行中に変化します。そのため、 `a = @a` `a = 1`に置き換えてTiKVにプッシュダウンしても、同等の実行プランにはなりません。
