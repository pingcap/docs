---
title: Predicates Push Down
summary: Introduce one of the TiDB's logic optimization rules—Predicate Push Down (PPD).
---

# Predicate Push Down(PPD) {#predicates-push-down-ppd}

このドキュメントでは、TiDB のロジック最適化ルールの 1 つである Predicate Push Down (PPD) を紹介します。述語のプッシュダウンを理解し、その適用可能なシナリオと適用できないシナリオを知るのに役立つことを目的としています。

PPD は、データ フィルタリングをできるだけ早く完了するために、選択演算子をできる限りデータ ソースに近づけることで、データ送信または計算のコストを大幅に削減します。

## 例 {#examples}

次のケースでは、PPD の最適化について説明します。 Case 1、2、および 3 は PPD が適用されるシナリオであり、Case 4、5、および 6 は PPD が適用されないシナリオです。

### ケース 1: 述語をstorageレイヤーにプッシュする {#case-1-push-predicates-to-storage-layer}

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

このクエリでは、述語`a < 1` TiKVレイヤーにプッシュダウンしてデータをフィルタリングすることで、ネットワーク送信のオーバーヘッドを削減できます。

### ケース 2: 述語をstorageレイヤーにプッシュする {#case-2-push-predicates-to-storage-layer}

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

このクエリは、ケース 1 のクエリと同じ実行プランを持ちます。述語`a < substring('123', 1, 1)`の`substring`の入力パラメータは定数なので、事前に計算できます。次に、述語は同等の述語に簡略化されます`a < 1` 。その後、TiDB は`a < 1`を TiKV にプッシュダウンできます。

### ケース 3: 述語を結合演算子の下にプッシュする {#case-3-push-predicates-below-join-operator}

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

このクエリでは、述語`t.a < 1`が結合の下にプッシュされて事前にフィルタリングされており、結合の計算オーバーヘッドを削減できます。

また、この SQL ステートメントでは内部結合が実行されており、 `ON`条件は`t.a = s.a`です。述語`s.a <1` `t.a < 1`から派生し、結合演算子の下の`s`テーブルにプッシュダウンできます。 `s`テーブルをフィルタリングすると、結合の計算オーバーヘッドをさらに削減できます。

### ケース 4:storage層でサポートされていない述語はプッシュダウンできません {#case-4-predicates-that-are-not-supported-by-storage-layers-cannot-be-pushed-down}

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

このクエリには述語`truncate(a, " ") = '1'`あります。

`explain`結果から、述語が計算のために TiKV にプッシュダウンされていないことがわかります。これは、TiKV コプロセッサが組み込み関数`truncate`をサポートしていないためです。

### ケース 5: 外部結合上の内部テーブルの述語をプッシュダウンできない {#case-5-predicates-of-inner-tables-on-the-outer-join-can-t-be-pushed-down}

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

このクエリでは、内部テーブル`s`に述語`s.a is null`があります。

`explain`の結果から、述語が結合演算子の下にプッシュされていないことがわかります。これは、条件`on`が満たされない場合、外部結合によって内部テーブルに`NULL`値が入力され、結合後の結果のフィルター処理に述語`s.a is null`が使用されるためです。結合の下の内部テーブルにプッシュダウンされた場合、実行計画は元の実行計画と等価ではなくなります。

### ケース 6: ユーザー変数を含む述語をプッシュダウンできない {#case-6-the-predicates-which-contain-user-variables-cannot-be-pushed-down}

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

このクエリでは、テーブル`t`に述語`a < @a`があります。述語の`@a`はユーザー変数です。

`explain`の結果からわかるように、述語はケース 2 とは異なり、ケース 2 は`a < 1`に単純化され、TiKV にプッシュされます。これは、ユーザー変数`@a`の値が計算中に変更される可能性があり、TiKV はその変更を認識しないためです。したがって、TiDB は`@a` `1`に置き換えず、それを TiKV にプッシュダウンしません。

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

このクエリからわかるように、 `@a`の値はクエリ中に変化します。したがって、 `a = @a` `a = 1`に置き換えて TiKV にプッシュダウンした場合、それは同等の実行プランではありません。
