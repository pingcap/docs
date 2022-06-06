---
title: Partitioning
summary: Learn how to use partitioning in TiDB.
---

# パーティショニング {#partitioning}

このドキュメントでは、TiDBによるパーティショニングの実装を紹介します。

## パーティショニングタイプ {#partitioning-types}

このセクションでは、TiDBのパーティショニングのタイプを紹介します。現在、 [リストのパーティション化](#list-partitioning)は[範囲分割](#range-partitioning) 、および[COLUMNSパーティショニングを一覧表示します](#list-columns-partitioning)をサポートしてい[ハッシュ分割](#hash-partitioning) 。

範囲分割、リスト分割、およびリスト列分割は、アプリケーションでの大量の削除によって引き起こされるパフォーマンスの問題を解決し、高速ドロップ分割操作をサポートするために使用されます。ハッシュ分割は、大量の書き込みがある場合にデータを分散させるために使用されます。

### 範囲分割 {#range-partitioning}

テーブルがRangeでパーティション化されている場合、各パーティションには、パーティション化式の値が指定されたRange内にある行が含まれます。範囲は隣接している必要がありますが、重複してはなりません。 `VALUES LESS THAN`を使用して定義できます。

次のように、人事レコードを含むテーブルを作成する必要があると想定します。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
);
```

必要に応じて、さまざまな方法で範囲ごとにテーブルを分割できます。たとえば、 `store_id`列を使用してパーティション化できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN (21)
);
```

このパーティションスキームでは、 `store_id`が1から5の従業員に対応するすべての行が`p0`パーティションに格納され、 `store_id`が6から10のすべての従業員が`p1`に格納されます。範囲分割では、パーティションを最低から最高の順に並べる必要があります。

データ`(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`の行を挿入すると、その行は`p2`パーティションに分類されます。ただし、 `store_id`が20より大きいレコードを挿入すると、TiDBはこのレコードを挿入するパーティションを認識できないため、エラーが報告されます。この場合、テーブルを作成するときに`MAXVALUE`を使用できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (store_id) (
    PARTITION p0 VALUES LESS THAN (6),
    PARTITION p1 VALUES LESS THAN (11),
    PARTITION p2 VALUES LESS THAN (16),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

`MAXVALUE`は、他のすべての整数値よりも大きい整数値を表します。これで、 `store_id`が16（定義された最大値）以上のすべてのレコードが`p3`パーティションに格納されます。

`job_code`列の値である従業員のジョブコードでテーブルを分割することもできます。 2桁のジョブコードは正社員を表し、3桁のコードはオフィスおよびカスタマーサポート担当者を表し、4桁のコードは管理者を表すと想定します。次に、次のようなパーティションテーブルを作成できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT NOT NULL
)

PARTITION BY RANGE (job_code) (
    PARTITION p0 VALUES LESS THAN (100),
    PARTITION p1 VALUES LESS THAN (1000),
    PARTITION p2 VALUES LESS THAN (10000)
);
```

この例では、正社員に関連するすべての行が`p0`パーティションに格納され、すべてのオフィスおよびカスタマーサポート担当者が`p1`パーティションに格納され、すべての管理担当者が`p2`パーティションに格納されます。

テーブルを`store_id`で分割するだけでなく、テーブルを日付で分割することもできます。たとえば、従業員の離職年ごとに分割できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY RANGE ( YEAR(separated) ) (
    PARTITION p0 VALUES LESS THAN (1991),
    PARTITION p1 VALUES LESS THAN (1996),
    PARTITION p2 VALUES LESS THAN (2001),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

範囲分割では、 `timestamp`列の値に基づいて分割し、 `unix_timestamp()`関数を使用できます。次に例を示します。

{{< copyable "" >}}

```sql
CREATE TABLE quarterly_report_status (
    report_id INT NOT NULL,
    report_status VARCHAR(20) NOT NULL,
    report_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)

PARTITION BY RANGE ( UNIX_TIMESTAMP(report_updated) ) (
    PARTITION p0 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-01-01 00:00:00') ),
    PARTITION p1 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-04-01 00:00:00') ),
    PARTITION p2 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-07-01 00:00:00') ),
    PARTITION p3 VALUES LESS THAN ( UNIX_TIMESTAMP('2008-10-01 00:00:00') ),
    PARTITION p4 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-01-01 00:00:00') ),
    PARTITION p5 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-04-01 00:00:00') ),
    PARTITION p6 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-07-01 00:00:00') ),
    PARTITION p7 VALUES LESS THAN ( UNIX_TIMESTAMP('2009-10-01 00:00:00') ),
    PARTITION p8 VALUES LESS THAN ( UNIX_TIMESTAMP('2010-01-01 00:00:00') ),
    PARTITION p9 VALUES LESS THAN (MAXVALUE)
);
```

タイムスタンプ列を含む他のパーティショニング式を使用することは許可されていません。

範囲分割は、次の1つ以上の条件が満たされる場合に特に役立ちます。

-   古いデータを削除したい。前の例の`employees`テーブルを使用すると、 `ALTER TABLE employees DROP PARTITION p0;`を使用するだけで、1991年より前にこの会社を退職した従業員のすべてのレコードを削除できます。 `DELETE FROM employees WHERE YEAR(separated) <= 1990;`操作を実行するよりも高速です。
-   時刻または日付の値を含む列、または他のシリーズから生じる値を含む列を使用するとします。
-   パーティション分割に使用される列に対して頻繁にクエリを実行する必要があります。たとえば、 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;`のようなクエリを実行すると、TiDBは、他のパーティションが`WHERE`の条件に一致しないため、 `p2`のパーティションのデータのみをスキャンする必要があることをすばやく知ることができます。

### リストのパーティション化 {#list-partitioning}

> **警告：**
>
> リストの分割は実験的機能です。実稼働環境で使用することはお勧めしません。

リストパーティションテーブルを作成する前に、セッション変数`tidb_enable_list_partition`の値を`ON`に設定する必要があります。

{{< copyable "" >}}

```sql
set @@session.tidb_enable_list_partition = ON
```

また、デフォルト設定である`tidb_enable_table_partition`が`ON`に設定されていることを確認してください。

リストのパーティション化は、範囲のパーティション化に似ています。範囲パーティショニングとは異なり、リストパーティショニングでは、各パーティションのすべての行のパーティショニング式の値が特定の値セットに含まれます。パーティションごとに定義されたこの値セットには、任意の数の値を含めることができますが、重複する値を含めることはできません。 `PARTITION ... VALUES IN (...)`句を使用して、値セットを定義できます。

人事記録テーブルを作成するとします。次のようにテーブルを作成できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

次の表に示すように、4つの地区に20の店舗が分散しているとします。

```
| Region  | Store ID Numbers     |
| ------- | -------------------- |
| North   | 1, 2, 3, 4, 5        |
| East    | 6, 7, 8, 9, 10       |
| West    | 11, 12, 13, 14, 15   |
| Central | 16, 17, 18, 19, 20   |
```

同じ地域の従業員の人事データを同じパーティションに保存する場合は、 `store_id`に基づいてリストパーティションテーブルを作成できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
```

上記のようにパーティションを作成した後、テーブル内の特定の領域に関連するレコードを簡単に追加または削除できます。たとえば、東部地域（東部）のすべての店舗が別の会社に売却されたとします。次に、このリージョンの店舗従業員に関連するすべての行データを`ALTER TABLE employees TRUNCATE PARTITION pEast`を実行することで削除できます。これは、同等のステートメント`DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)`よりもはるかに効率的です。

`ALTER TABLE employees DROP PARTITION pEast`を実行して関連するすべての行を削除することもできますが、このステートメントはテーブル定義から`pEast`パーティションも削除します。この状況では、 `ALTER TABLE ... ADD PARTITION`ステートメントを実行して、テーブルの元のパーティションスキームを回復する必要があります。

範囲パーティショニングとは異なり、リストパーティショニングには、他のパーティションに属していないすべての値を格納するための同様の`MAXVALUE`パーティションがありません。代わりに、パーティション式のすべての期待値を`PARTITION ... VALUES IN (...)`句に含める必要があります。 `INSERT`ステートメントに挿入される値がどのパーティションの列値セットとも一致しない場合、ステートメントは実行に失敗し、エラーが報告されます。次の例を参照してください。

```sql
test> CREATE TABLE t (
    ->   a INT,
    ->   b INT
    -> )
    -> PARTITION BY LIST (a) (
    ->   PARTITION p0 VALUES IN (1, 2, 3),
    ->   PARTITION p1 VALUES IN (4, 5, 6)
    -> );
Query OK, 0 rows affected (0.11 sec)

test> INSERT INTO t VALUES (7, 7);
ERROR 1525 (HY000): Table has no partition for value 7
```

上記のエラータイプを無視するには、 `IGNORE`キーワードを使用できます。このキーワードを使用した後、どのパーティションの列値セットとも一致しない値が行に含まれている場合、この行は挿入されません。代わりに、値が一致する行が挿入され、エラーは報告されません。

```sql
test> TRUNCATE t;
Query OK, 1 row affected (0.00 sec)

test> INSERT IGNORE INTO t VALUES (1, 1), (7, 7), (8, 8), (3, 3), (5, 5);
Query OK, 3 rows affected, 2 warnings (0.01 sec)
Records: 5  Duplicates: 2  Warnings: 2

test> select * from t;
+------+------+
| a    | b    |
+------+------+
|    5 |    5 |
|    1 |    1 |
|    3 |    3 |
+------+------+
3 rows in set (0.01 sec)
```

### COLUMNSパーティショニングを一覧表示します {#list-columns-partitioning}

> **警告：**
>
> List COLUMNSパーティショニングは、実験的機能です。実稼働環境で使用することはお勧めしません。

List COLUMNSパーティショニングは、Listパーティショニングの変形です。複数の列をパーティションキーとして使用できます。整数データ型に加えて、文字列、 `DATE` 、および`DATETIME`データ型の列をパーティション列として使用することもできます。

次の表に示すように、次の12の都市の店舗の従業員を4つの地域に分割するとします。

```
| Region | Cities                         |
| :----- | ------------------------------ |
| 1      | LosAngeles,Seattle, Houston    |
| 2      | Chicago, Columbus, Boston      |
| 3      | NewYork, LongIsland, Baltimore |
| 4      | Atlanta, Raleigh, Cincinnati   |
```

以下に示すように、List COLUMNSパーティション化を使用してテーブルを作成し、従業員の都市に対応するパーティションに各行を格納できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees_1 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT,
    city VARCHAR(15)
)
PARTITION BY LIST COLUMNS(city) (
    PARTITION pRegion_1 VALUES IN('LosAngeles', 'Seattle', 'Houston'),
    PARTITION pRegion_2 VALUES IN('Chicago', 'Columbus', 'Boston'),
    PARTITION pRegion_3 VALUES IN('NewYork', 'LongIsland', 'Baltimore'),
    PARTITION pRegion_4 VALUES IN('Atlanta', 'Raleigh', 'Cincinnati')
);
```

リストのパーティション化とは異なり、リストのCOLUMNSパーティション化では、列の値を整数に変換するために`COLUMNS()`節の式を使用する必要はありません。

次の例に示すように、リストCOLUMNSパーティショニングは、 `DATE`タイプと`DATETIME`タイプの列を使用して実装することもできます。この例では、前の`employees_1`の表と同じ名前と列を使用していますが、 `hired`の列に基づいてListCOLUMNSパーティションを使用しています。

{{< copyable "" >}}

```sql
CREATE TABLE employees_2 (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT,
    city VARCHAR(15)
)
PARTITION BY LIST COLUMNS(hired) (
    PARTITION pWeek_1 VALUES IN('2020-02-01', '2020-02-02', '2020-02-03',
        '2020-02-04', '2020-02-05', '2020-02-06', '2020-02-07'),
    PARTITION pWeek_2 VALUES IN('2020-02-08', '2020-02-09', '2020-02-10',
        '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14'),
    PARTITION pWeek_3 VALUES IN('2020-02-15', '2020-02-16', '2020-02-17',
        '2020-02-18', '2020-02-19', '2020-02-20', '2020-02-21'),
    PARTITION pWeek_4 VALUES IN('2020-02-22', '2020-02-23', '2020-02-24',
        '2020-02-25', '2020-02-26', '2020-02-27', '2020-02-28')
);
```

さらに、 `COLUMNS()`句に複数の列を追加することもできます。例えば：

{{< copyable "" >}}

```sql
CREATE TABLE t (
    id int,
    name varchar(10)
)
PARTITION BY LIST COLUMNS(id,name) (
     partition p0 values IN ((1,'a'),(2,'b')),
     partition p1 values IN ((3,'c'),(4,'d')),
     partition p3 values IN ((5,'e'),(null,null))
);
```

### ハッシュ分割 {#hash-partitioning}

ハッシュパーティショニングは、データが特定の数のパーティションに均等に分散されるようにするために使用されます。範囲パーティショニングでは、範囲パーティショニングを使用する場合は各パーティションの列値の範囲を指定する必要がありますが、ハッシュパーティショニングを使用する場合はパーティションの数を指定するだけで済みます。

ハッシュによるパーティショニングでは、 `CREATE TABLE`ステートメントに`PARTITION BY HASH (expr)`句を追加する必要があります。 `expr`は整数を返す式です。この列のタイプが整数の場合は、列名にすることができます。さらに、 `PARTITIONS num`を追加する必要がある場合もあります。ここで、 `num`は、テーブルが分割されるパーティションの数を示す正の整数です。

次の操作により、ハッシュパーティションテーブルが作成されます。このテーブルは、 `store_id`で4つのパーティションに分割されます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH(store_id)
PARTITIONS 4;
```

`PARTITIONS num`が指定されていない場合、デフォルトのパーティション数は1です。

`expr`の整数を返すSQL式を使用することもできます。たとえば、雇用年ごとにテーブルを分割できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY HASH( YEAR(hired) )
PARTITIONS 4;
```

最も効率的なハッシュ関数は、単一のテーブル列を操作する関数であり、その値は列の値に応じて増減します。

たとえば、 `date_col`はタイプが`DATE`の列であり、 `TO_DAYS(date_col)`式の値は`date_col`の値によって変化します。 `YEAR(date_col)`は`TO_DAYS(date_col)`とは異なります。これは、 `date_col`で可能なすべての変更が、 `YEAR(date_col)`で同等の変更を生成するわけではないためです。

対照的に、タイプが`INT`の`int_col`列があると仮定します。次に、式`POW(5-int_col,3) + 6`について考えます。ただし、 `int_col`の値が変化しても、式の結果は比例して変化しないため、これは適切なハッシュ関数ではありません。 `int_col`の値を変更すると、式の結果が大幅に変更される可能性があります。たとえば、 `int_col`が5から6に変わると、式の結果の変化は-1になります。ただし、 `int_col`が6から7に変更されると、結果の変更は-7になる可能性があります。

結論として、式の形式が`y = cx`に近い場合は、ハッシュ関数である方が適しています。式が非線形であるほど、パーティション間でデータが不均一に分散する傾向があります。

理論的には、複数の列値を含む式に対してプルーニングも可能ですが、そのような式のどれが適切であるかを判断することは非常に困難で時間がかかる可能性があります。このため、複数の列を含むハッシュ式の使用は特にお勧めしません。

`PARTITION BY HASH`を使用する場合、TiDBは、式の結果のモジュラスに基づいて、データがどのパーティションに分類されるかを決定します。つまり、パーティショニング式が`expr`で、パーティション数が`num`の場合、 `MOD(expr, num)`がデータを格納するパーティションを決定します。 `t1`が次のように定義されていると仮定します。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

データの行を`t1`に挿入し、 `col3`の値が「2005-09-15」の場合、この行はパーティション1に挿入されます。

```
MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)
=  1
```

### TiDBパーティショニングがNULLを処理する方法 {#how-tidb-partitioning-handles-null}

TiDBでは、パーティショニング式の計算結果として`NULL`を使用できます。

> **ノート：**
>
> `NULL`は整数ではありません。 TiDBのパーティショニング実装は、 `ORDER BY`と同様に、 `NULL`を他の整数値よりも小さいものとして扱います。

#### 範囲分割によるNULLの処理 {#handling-of-null-with-range-partitioning}

Rangeでパーティション化されたテーブルに行を挿入し、パーティションの決定に使用される列の値が`NULL`の場合、この行は最下位のパーティションに挿入されます。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY RANGE(c1) (
    PARTITION p0 VALUES LESS THAN (0),
    PARTITION p1 VALUES LESS THAN (10),
    PARTITION p2 VALUES LESS THAN MAXVALUE
);
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "" >}}

```sql
select * from t1 partition(p0);
```

```
+------|--------+
| c1   | c2     |
+------|--------+
| NULL | mothra |
+------|--------+
1 row in set (0.00 sec)
```

{{< copyable "" >}}

```sql
select * from t1 partition(p1);
```

```
Empty set (0.00 sec)
```

{{< copyable "" >}}

```sql
select * from t1 partition(p2);
```

```
Empty set (0.00 sec)
```

`p0`つのパーティションを削除し、結果を確認します。

{{< copyable "" >}}

```sql
alter table t1 drop partition p0;
```

```
Query OK, 0 rows affected (0.08 sec)
```

{{< copyable "" >}}

```sql
select * from t1;
```

```
Empty set (0.00 sec)
```

#### ハッシュ分割によるNULLの処理 {#handling-of-null-with-hash-partitioning}

ハッシュでテーブルを分割する場合、 `NULL`の値を処理する別の方法があります。分割式の計算結果が`NULL`の場合、 `0`と見なされます。

{{< copyable "" >}}

```sql
CREATE TABLE th (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY HASH(c1)
PARTITIONS 2;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
```

```
Query OK, 2 rows affected (0.04 sec)
```

{{< copyable "" >}}

```sql
select * from th partition (p0);
```

```
+------|--------+
| c1   | c2     |
+------|--------+
| NULL | mothra |
|    0 | gigan  |
+------|--------+
2 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
select * from th partition (p1);
```

```
Empty set (0.00 sec)
```

挿入されたレコード`(NULL, 'mothra')`が`(0, 'gigan')`と同じパーティションに分類されることがわかります。

> **注：** TiDBのハッシュパーティションによる`NULL`の値は、 [MySQLパーティショニングがNULLを処理する方法](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html)で説明したのと同じ方法で処理されますが、MySQLの実際の動作とは一致しません。言い換えると、この場合のMySQLの実装は、そのドキュメントと一致していません。
>
> この場合、TiDBの実際の動作は、このドキュメントの説明と一致しています。

## パーティション管理 {#partition-management}

`LIST`および`RANGE`パーティションテーブルの場合、 `ALTER TABLE <table name> ADD PARTITION (<partition specification>)`または`ALTER TABLE <table name> DROP PARTITION <list of partitions>`ステートメントを使用してパーティションを追加および削除できます。

`LIST`および`RANGE`パーティションテーブルの場合、 `REORGANIZE PARTITION`はまだサポートされていません。

`HASH`つのパーティションテーブルの場合、 `COALESCE PARTITION`と`ADD PARTITION`はまだサポートされていません。

`EXCHANGE PARTITION`は、パーティションと非パーティションテーブルを交換することで機能します。これは、 `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2`のようにテーブルの名前を変更する場合と同様です。

たとえば、 `ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table`は`p1`パーティションの`non_partitioned_table`テーブルを`partitioned_table`テーブルと交換します。

パーティションに交換するすべての行がパーティション定義と一致することを確認してください。そうしないと、これらの行が見つからず、予期しない問題が発生します。

> **警告：**
>
> `EXCHANGE PARTITION`は実験的機能です。実稼働環境での使用はお勧めしません。これを有効にするには、 `tidb_enable_exchange_partition`システム変数を`ON`に設定します。

### 範囲パーティション管理 {#range-partition-management}

パーティションテーブルを作成します。

{{< copyable "" >}}

```sql
CREATE TABLE members (
    id INT,
    fname VARCHAR(25),
    lname VARCHAR(25),
    dob DATE
)

PARTITION BY RANGE( YEAR(dob) ) (
    PARTITION p0 VALUES LESS THAN (1980),
    PARTITION p1 VALUES LESS THAN (1990),
    PARTITION p2 VALUES LESS THAN (2000)
);
```

パーティションを削除します。

{{< copyable "" >}}

```sql
ALTER TABLE members DROP PARTITION p2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

パーティションを空にします：

{{< copyable "" >}}

```sql
ALTER TABLE members TRUNCATE PARTITION p1;
```

```
Query OK, 0 rows affected (0.03 sec)
```

> **ノート：**
>
> `ALTER TABLE ... REORGANIZE PARTITION`は現在TiDBではサポートされていません。

パーティションを追加します。

{{< copyable "" >}}

```sql
ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));
```

テーブルを範囲でパーティション化する場合、 `ADD PARTITION`はパーティションリストの最後にのみ追加できます。既存の範囲パーティションに追加されている場合、エラーが報告されます。

{{< copyable "" >}}

```sql
ALTER TABLE members
    ADD PARTITION (
    PARTITION n VALUES LESS THAN (1970));
```

```
ERROR 1463 (HY000): VALUES LESS THAN value must be strictly »
   increasing for each partition
```

### ハッシュパーティション管理 {#hash-partition-management}

範囲分割とは異なり、 `DROP PARTITION`はハッシュ分割ではサポートされていません。

現在、 `ALTER TABLE ... COALESCE PARTITION`はTiDBでもサポートされていません。現在サポートされていないパーティション管理ステートメントの場合、TiDBはエラーを返します。

{{< copyable "" >}}

```sql
alter table members optimize partition p0;
```

```sql
ERROR 8200 (HY000): Unsupported optimize partition
```

## パーティションの剪定 {#partition-pruning}

[パーティションの剪定](/partition-pruning.md)は、非常に単純なアイデアに基づく最適化です。一致しないパーティションをスキャンしないでください。

パーティションテーブルを作成するとします`t1` ：

{{< copyable "" >}}

```sql
CREATE TABLE t1 (
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    region_code TINYINT UNSIGNED NOT NULL,
    dob DATE NOT NULL
)

PARTITION BY RANGE( region_code ) (
    PARTITION p0 VALUES LESS THAN (64),
    PARTITION p1 VALUES LESS THAN (128),
    PARTITION p2 VALUES LESS THAN (192),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

この`SELECT`のステートメントの結果を取得する場合：

{{< copyable "" >}}

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

結果が`p1`または`p2`パーティションに分類されることは明らかです。つまり、 `p1`と`p2`で一致する行を検索するだけで済みます。不要なパーティションを除外することは、いわゆる「プルーニング」です。オプティマイザがパーティションの一部をプルーニングできる場合、パーティション化されたテーブルでのクエリの実行は、パーティション化されていないテーブルでのクエリの実行よりもはるかに高速になります。

オプティマイザは、次の2つのシナリオで、 `WHERE`つの条件でパーティションを整理できます。

-   partition_column=定数
-   partition_column IN（constant1、constant2、...、constantN）

### パーティションプルーニングが有効になる場合 {#some-cases-for-partition-pruning-to-take-effect}

1.  パーティションプルーニングはパーティションテーブルのクエリ条件を使用するため、プランナーの最適化ルールに従ってクエリ条件をパーティションテーブルにプッシュダウンできない場合、パーティションプルーニングはこのクエリには適用されません。

    例えば：

    {{< copyable "" >}}

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    create table t2 (x int);
    ```

    {{< copyable "" >}}

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x where t2.x > 5;
    ```

    このクエリでは、除外された結合が内部結合に変換され、次に`t1.x > 5`が`t1.x = t2.x`と`t2.x > 5`から派生するため、パーティションのプルーニングに使用でき、パーティション`p1`のみが残ります。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    このクエリでは、 `t2.x > 5`を`t1`パーティションテーブルにプッシュダウンできないため、このクエリではパーティションプルーニングは有効になりません。

2.  パーティションのプルーニングはプランの最適化フェーズで実行されるため、実行フェーズまでフィルター条件が不明な場合には適用されません。

    例えば：

    {{< copyable "" >}}

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    ```

    {{< copyable "" >}}

    ```sql
    explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
    ```

    このクエリは`t2`から行を読み取り、その結果を`t1`のサブクエリに使用します。理論的には、パーティションのプルーニングはサブクエリの`t1.x > val`式の恩恵を受ける可能性がありますが、実行フェーズで発生するため、そこでは有効になりません。

3.  現在の実装からの制限の結果として、クエリ条件をTiKVにプッシュダウンできない場合、パーティションプルーニングで使用することはできません。

    例として`fn(col)`式を取り上げます。 TiKVコプロセッサーがこの`fn`の機能をサポートしている場合、プランの最適化フェーズ中に述語プッシュダウン・ルールに従って`fn(col)`がリーフ・ノード（つまり、パーティション化されたテーブル）にプッシュダウンされ、パーティションのプルーニングでそれを使用できます。

    TiKVコプロセッサーがこの`fn`の機能をサポートしていない場合、 `fn(col)`はリーフノードにプッシュダウンされません。代わりに、リーフノードの上の`Selection`ノードになります。現在のパーティションプルーニングの実装は、この種のプランツリーをサポートしていません。

4.  ハッシュパーティションの場合、パーティションプルーニングでサポートされるクエリはequal条件のみです。

5.  範囲パーティションの場合、パーティションプルーニングを有効にするには、パーティション式が`col`または`fn(col)`の形式である必要があり、クエリ条件は`>` 、および`<`の`>=`かである必要が`<=` `=` 。パーティション式が`fn(col)`の形式である場合、 `fn`関数は単調である必要があります。

    `fn`関数が単調である場合、任意の`x`と`y`について、 `x > y`の場合、 `fn(x) > fn(y)` 。そうすれば、この`fn`の関数は厳密に単調と呼ぶことができます。 `x`と`y`の場合、 `x > y`の場合、 `fn(x) >= fn(y)` 。この場合、 `fn`は「単調」とも呼ばれます。理論的には、すべての単調な関数はパーティションプルーニングによってサポートされます。

    現在、TiDBのパーティションプルーニングは、これらの単調な機能のみをサポートしています。

    ```
    unix_timestamp
    to_days
    ```

    たとえば、パーティション式は単純な列です。

    {{< copyable "" >}}

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where t > 6;
    ```

    または、パーティション式は`fn(col)`の形式で、 `fn`は`to_days`です。

    {{< copyable "" >}}

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where t > '2020-04-18';
    ```

    例外は、パーティション式としての`floor(unix_timestamp())`です。 TiDBはそのケースバイケースでいくつかの最適化を行うため、パーティションプルーニングによってサポートされます。

    {{< copyable "" >}}

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where t > '2020-04-18 02:00:42.123';
    ```

## パーティションの選択 {#partition-selection}

`SELECT`ステートメントは、 `PARTITION`オプションを使用して実装されるパーティション選択をサポートします。

{{< copyable "" >}}

```sql
CREATE TABLE employees  (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(25) NOT NULL,
    lname VARCHAR(25) NOT NULL,
    store_id INT NOT NULL,
    department_id INT NOT NULL
)

PARTITION BY RANGE(id)  (
    PARTITION p0 VALUES LESS THAN (5),
    PARTITION p1 VALUES LESS THAN (10),
    PARTITION p2 VALUES LESS THAN (15),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);

INSERT INTO employees VALUES
    ('', 'Bob', 'Taylor', 3, 2), ('', 'Frank', 'Williams', 1, 2),
    ('', 'Ellen', 'Johnson', 3, 4), ('', 'Jim', 'Smith', 2, 4),
    ('', 'Mary', 'Jones', 1, 1), ('', 'Linda', 'Black', 2, 3),
    ('', 'Ed', 'Jones', 2, 1), ('', 'June', 'Wilson', 3, 1),
    ('', 'Andy', 'Smith', 1, 3), ('', 'Lou', 'Waters', 2, 4),
    ('', 'Jill', 'Stone', 1, 4), ('', 'Roger', 'White', 3, 2),
    ('', 'Howard', 'Andrews', 1, 2), ('', 'Fred', 'Goldberg', 3, 3),
    ('', 'Barbara', 'Brown', 2, 3), ('', 'Alice', 'Rogers', 2, 2),
    ('', 'Mark', 'Morgan', 3, 3), ('', 'Karen', 'Cole', 3, 2);
```

`p1`つのパーティションに格納されている行を表示できます。

{{< copyable "" >}}

```sql
SELECT * FROM employees PARTITION (p1);
```

```
+----|-------|--------|----------|---------------+
| id | fname | lname  | store_id | department_id |
+----|-------|--------|----------|---------------+
|  5 | Mary  | Jones  |        1 |             1 |
|  6 | Linda | Black  |        2 |             3 |
|  7 | Ed    | Jones  |        2 |             1 |
|  8 | June  | Wilson |        3 |             1 |
|  9 | Andy  | Smith  |        1 |             3 |
+----|-------|--------|----------|---------------+
5 rows in set (0.00 sec)
```

複数のパーティションの行を取得する場合は、コンマで区切られたパーティション名のリストを使用できます。たとえば、 `SELECT * FROM employees PARTITION (p1, p2)`は`p1`パーティションと`p2`パーティションのすべての行を返します。

パーティション選択を使用する場合でも、 `WHERE`の条件と`ORDER BY`や`LIMIT`などのオプションを使用できます。 `HAVING`や`GROUP BY`などの集計オプションの使用もサポートされています。

{{< copyable "" >}}

```sql
SELECT * FROM employees PARTITION (p0, p2)
    WHERE lname LIKE 'S%';
```

```
+----|-------|-------|----------|---------------+
| id | fname | lname | store_id | department_id |
+----|-------|-------|----------|---------------+
|  4 | Jim   | Smith |        2 |             4 |
| 11 | Jill  | Stone |        1 |             4 |
+----|-------|-------|----------|---------------+
2 rows in set (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT id, CONCAT(fname, ' ', lname) AS name
    FROM employees PARTITION (p0) ORDER BY lname;
```

```
+----|----------------+
| id | name           |
+----|----------------+
|  3 | Ellen Johnson  |
|  4 | Jim Smith      |
|  1 | Bob Taylor     |
|  2 | Frank Williams |
+----|----------------+
4 rows in set (0.06 sec)
```

{{< copyable "" >}}

```sql
SELECT store_id, COUNT(department_id) AS c
    FROM employees PARTITION (p1,p2,p3)
    GROUP BY store_id HAVING c > 4;
```

```
+---|----------+
| c | store_id |
+---|----------+
| 5 |        2 |
| 5 |        3 |
+---|----------+
2 rows in set (0.00 sec)
```

パーティションの選択は、範囲パーティショニングやハッシュパーティショニングを含むすべてのタイプのテーブルパーティショニングでサポートされています。ハッシュパーティションの場合、パーティション名が指定されて`p2`ない場合、パーティション`p1`として`p0` 、...、または`pN-1`が自動的に使用されます。

`SELECT`でも`INSERT ... SELECT`選択を使用できます。

## パーティションの制限と制限 {#restrictions-and-limitations-on-partitions}

このセクションでは、TiDBのパーティションテーブルに関するいくつかの制限と制限を紹介します。

### パーティションキー、主キー、および一意キー {#partitioning-keys-primary-keys-and-unique-keys}

このセクションでは、パーティション化キーと主キーおよび一意キーとの関係について説明します。この関係を管理するルールは、次のように表すことができます。**テーブルのすべての一意キーは、テーブルのパーティション化式のすべての列を使用する必要があります**。定義上、一意のキーであるため、これにはテーブルの主キーも含まれます。

たとえば、次のテーブル作成ステートメントは無効です。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1),
    UNIQUE KEY (col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

いずれの場合も、提案されたテーブルには、パーティショニング式で使用されるすべての列を含まない一意のキーが少なくとも1つあります。

有効なステートメントは次のとおりです。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t2 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

次の例はエラーを表示します。

{{< copyable "" >}}

```sql
CREATE TABLE t3 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2),
    UNIQUE KEY (col3)
)

PARTITION BY HASH(col1 + col3)
PARTITIONS 4;
```

```
ERROR 1491 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function
```

提案されたパーティショニングキーに`col1`と`col3`の両方が含まれているため、 `CREATE TABLE`ステートメントは失敗しますが、これらの列はどちらもテーブル上の両方の一意のキーの一部ではありません。次の変更を行うと、 `CREATE TABLE`ステートメントが有効になります。

{{< copyable "" >}}

```sql
CREATE TABLE t3 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col2, col3),
    UNIQUE KEY (col1, col3)
)
PARTITION BY HASH(col1 + col3)
    PARTITIONS 4;
```

次のテーブルは、パーティション化キーに両方の一意のキーに属する列を含める方法がないため、パーティション化できません。

{{< copyable "" >}}

```sql
CREATE TABLE t4 (
    col1 INT NOT NULL,
    col2 INT NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY (col1, col3),
    UNIQUE KEY (col2, col4)
);
```

すべての主キーは定義上一意のキーであるため、次の2つのステートメントは無効です。

{{< copyable "" >}}

```sql
CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2)
)

PARTITION BY HASH(col3)
PARTITIONS 4;

CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col3),
    UNIQUE KEY(col2)
)

PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

上記の例では、主キーにパーティショニング式で参照されているすべての列が含まれているわけではありません。主キーに欠落している列を追加すると、 `CREATE TABLE`ステートメントが有効になります。

{{< copyable "" >}}

```sql
CREATE TABLE t5 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col3)
)
PARTITION BY HASH(col3)
PARTITIONS 4;
CREATE TABLE t6 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    PRIMARY KEY(col1, col2, col3),
    UNIQUE KEY(col2)
)
PARTITION BY HASH( YEAR(col2) )
PARTITIONS 4;
```

テーブルに一意キーも主キーもない場合、この制限は適用されません。

DDLステートメントを使用してテーブルを変更する場合、一意のインデックスを追加するときにこの制限も考慮する必要があります。たとえば、次のようにパーティションテーブルを作成する場合：

{{< copyable "" >}}

```sql
CREATE TABLE t_no_pk (c1 INT, c2 INT)
    PARTITION BY RANGE(c1) (
        PARTITION p0 VALUES LESS THAN (10),
        PARTITION p1 VALUES LESS THAN (20),
        PARTITION p2 VALUES LESS THAN (30),
        PARTITION p3 VALUES LESS THAN (40)
    );
```

```
Query OK, 0 rows affected (0.12 sec)
```

`ALTER TABLE`のステートメントを使用して、一意でないインデックスを追加できます。ただし、一意のインデックスを追加する場合は、 `c1`列を一意のインデックスに含める必要があります。

パーティションテーブルを使用する場合、プレフィックスインデックスを一意の属性として指定することはできません。

{{< copyable "" >}}

```sql
CREATE TABLE t (a varchar(20), b blob,
    UNIQUE INDEX (a(5)))
    PARTITION by range columns (a) (
    PARTITION p0 values less than ('aaaaa'),
    PARTITION p1 values less than ('bbbbb'),
    PARTITION p2 values less than ('ccccc'));
```

```sql
ERROR 1503 (HY000): A UNIQUE INDEX must include all columns in the table's partitioning function
```

### 関数に関連するパーティション分割の制限 {#partitioning-limitations-relating-to-functions}

次のリストに示されている関数のみが、式のパーティション化で許可されます。

```
ABS()
CEILING()
DATEDIFF()
DAY()
DAYOFMONTH()
DAYOFWEEK()
DAYOFYEAR()
EXTRACT() (see EXTRACT() function with WEEK specifier)
FLOOR()
HOUR()
MICROSECOND()
MINUTE()
MOD()
MONTH()
QUARTER()
SECOND()
TIME_TO_SEC()
TO_DAYS()
TO_SECONDS()
UNIX_TIMESTAMP() (with TIMESTAMP columns)
WEEKDAY()
YEAR()
YEARWEEK()
```

### MySQLとの互換性 {#compatibility-with-mysql}

現在、TiDBは、範囲パーティショニング、リストパーティショニング、リストCOLUMNSパーティショニング、およびハッシュパーティショニングをサポートしています。キーパーティショニングなど、MySQLで使用可能な他のパーティショニングタイプは、TiDBではまだサポートされていません。

`RANGE COLUMNS`でパーティション化されたテーブルの場合、現在TiDBは単一のパーティション化列の使用のみをサポートしています。

パーティション管理に関しては、現在、下部の実装でデータを移動する必要がある操作はサポートされていません。これには、ハッシュパーティションテーブルのパーティション数の調整、範囲パーティションテーブルの範囲の変更、パーティションのマージ、パーティションを交換します。

サポートされていないパーティショニングタイプの場合、TiDBでテーブルを作成すると、パーティショニング情報は無視され、テーブルは通常の形式で作成され、警告が報告されます。

`LOAD DATA`構文は、現在TiDBでのパーティション選択をサポートしていません。

{{< copyable "" >}}

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

通常の`LOAD DATA`操作がサポートされています。

{{< copyable "" >}}

```sql
load local data infile "xxx" into t ...
```

ただし、 `Load Data`はパーティションの選択をサポートしていません。

{{< copyable "" >}}

```sql
load local data infile "xxx" into t partition (p1)...
```

パーティションテーブルの場合、 `select * from t`によって返される結果は、パーティション間で順序付けられていません。これは、パーティション間で順序付けられているが、パーティション内では順序付けされていないMySQLの結果とは異なります。

{{< copyable "" >}}

```sql
create table t (id int, val int) partition by range (id) (
    partition p0 values less than (3),
    partition p1 values less than (7),
    partition p2 values less than (11));
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "" >}}

```sql
insert into t values (1, 2), (3, 4),(5, 6),(7,8),(9,10);
```

```
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

TiDBは、毎回異なる結果を返します。次に例を示します。

{{< copyable "" >}}

```sql
select * from t;
```

```
+------|------+
| id   | val  |
+------|------+
|    7 |    8 |
|    9 |   10 |
|    1 |    2 |
|    3 |    4 |
|    5 |    6 |
+------|------+
5 rows in set (0.00 sec)
```

MySQLで返される結果：

{{< copyable "" >}}

```sql
select * from t;
```

```
+------|------+
| id   | val  |
+------|------+
|    1 |    2 |
|    3 |    4 |
|    5 |    6 |
|    7 |    8 |
|    9 |   10 |
+------|------+
5 rows in set (0.00 sec)
```

`tidb_enable_list_partition`環境変数は、パーティションテーブル機能を有効にするかどうかを制御します。この変数が`OFF`に設定されている場合、テーブルの作成時にパーティション情報は無視され、このテーブルは通常のテーブルとして作成されます。

この変数は、テーブルの作成でのみ使用されます。テーブルの作成後、この変数値を変更しても効果はありません。詳細については、 [システム変数](/system-variables.md#tidb_enable_list_partition-new-in-v50)を参照してください。

### 動的剪定モード {#dynamic-pruning-mode}

> **警告：**
>
> これはまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。

TiDBは、 `dynamic`モードと`static`モードの2つのモードのいずれかでパーティションテーブルにアクセスします。現在、デフォルトで`static`モードが使用されています。 `dynamic`モードを有効にする場合は、 `tidb_partition_prune_mode`変数を手動で`dynamic`に設定する必要があります。

{{< copyable "" >}}

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

`static`モードでは、TiDBは複数の演算子を使用して各パーティションに個別にアクセスし、 `Union`を使用して結果をマージします。次の例は、TiDBが`Union`を使用して2つの対応するパーティションの結果をマージする単純な読み取り操作です。

{{< copyable "" >}}

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id) (
    ->     partition p0 values less than (100),
    ->     partition p1 values less than (200),
    ->     partition p2 values less than (300),
    ->     partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
+------------------------------+----------+-----------+------------------------+--------------------------------+
| id                           | estRows  | task      | access object          | operator info                  |
+------------------------------+----------+-----------+------------------------+--------------------------------+
| PartitionUnion_9             | 6646.67  | root      |                        |                                |
| ├─TableReader_12             | 3323.33  | root      |                        | data:Selection_11              |
| │ └─Selection_11             | 3323.33  | cop[tikv] |                        | lt(test.t1.id, 150)            |
| │   └─TableFullScan_10       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo |
| └─TableReader_18             | 3323.33  | root      |                        | data:Selection_17              |
|   └─Selection_17             | 3323.33  | cop[tikv] |                        | lt(test.t1.id, 150)            |
|     └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo |
+------------------------------+----------+-----------+------------------------+--------------------------------+
7 rows in set (0.00 sec)
```

`dynamic`モードでは、各オペレーターが複数のパーティションへの直接アクセスをサポートするため、TiDBは`Union`を使用しなくなります。

{{< copyable "" >}}

```sql
mysql> set @@session.tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select * from t1 where id < 150;
+-------------------------+----------+-----------+-----------------+--------------------------------+
| id                      | estRows  | task      | access object   | operator info                  |
+-------------------------+----------+-----------+-----------------+--------------------------------+
| TableReader_7           | 3323.33  | root      | partition:p0,p1 | data:Selection_6               |
| └─Selection_6           | 3323.33  | cop[tikv] |                 | lt(test.t1.id, 150)            |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1        | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+-----------------+--------------------------------+
3 rows in set (0.00 sec)
```

上記のクエリ結果から、パーティションプルーニングが引き続き有効であり、実行プランが`p0`と`p1`にのみアクセスしている間に、実行プランの`Union`演算子が消えていることがわかります。

`dynamic`モードでは、実行計画がより単純で明確になります。ユニオン操作を省略すると、実行効率が向上し、ユニオン同時実行の問題を回避できます。さらに、 `dynamic`モードでは、 `static`モードでは解決できない2つの問題も解決されます。

-   プランキャッシュは使用できません。 （例1および2を参照）
-   IndexJoinを使用した実行プランは使用できません。 （例3および4を参照）

**例1** ：次の例では、構成ファイルでプランキャッシュ機能が有効になっており、同じクエリが`static`モードで2回実行されます。

{{< copyable "" >}}

```sql
mysql> set @a=150;
Query OK, 0 rows affected (0.00 sec)

mysql> set @@tidb_partition_prune_mode = 'static';
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t1 where id < ?';
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

-- In static mode, when the same query is executed twice, the cache cannot be hit at the second time.
mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      0 |
+------------------------+
1 row in set (0.00 sec)
```

`last_plan_from_cache`変数は、最後のクエリがプランキャッシュにヒットしたかどうかを示すことができます。例1から、 `static`モードでは、パーティション化されたテーブルで同じクエリが複数回実行されても、プランキャッシュがヒットしないことがわかります。

**例2** ：次の例では、例1と同じ操作が`dynamic`モードで実行されます。

{{< copyable "" >}}

```sql
mysql> set @@tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t1 where id < ?';
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

mysql> execute stmt using @a;
Empty set (0.00 sec)

-- In dynamic mode, the cache can be hit at the second time.
mysql> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

例2から、 `dynamic`モードで、パーティション化されたテーブルをクエリするとプランキャッシュにヒットすることがわかります。

**例3** ：次の例では、IndexJoinを使用して実行プランを使用して`static`モードでクエリを実行します。

{{< copyable "" >}}

```sql
mysql> create table t2(id int, code int);
Query OK, 0 rows affected (0.01 sec)

mysql> set @@tidb_partition_prune_mode = 'static';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select /*+ TIDB_INLJ(t1, t2) */ t1.* from t1, t2 where t2.code = 0 and t2.id = t1.id;
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
| id                             | estRows  | task      | access object          | operator info                                  |
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
| HashJoin_13                    | 12.49    | root      |                        | inner join, equal:[eq(test.t1.id, test.t2.id)] |
| ├─TableReader_42(Build)        | 9.99     | root      |                        | data:Selection_41                              |
| │ └─Selection_41               | 9.99     | cop[tikv] |                        | eq(test.t2.code, 0), not(isnull(test.t2.id))   |
| │   └─TableFullScan_40         | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                 |
| └─PartitionUnion_15(Probe)     | 39960.00 | root      |                        |                                                |
|   ├─TableReader_18             | 9990.00  | root      |                        | data:Selection_17                              |
|   │ └─Selection_17             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_16       | 10000.00 | cop[tikv] | table:t1, partition:p0 | keep order:false, stats:pseudo                 |
|   ├─TableReader_24             | 9990.00  | root      |                        | data:Selection_23                              |
|   │ └─Selection_23             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_22       | 10000.00 | cop[tikv] | table:t1, partition:p1 | keep order:false, stats:pseudo                 |
|   ├─TableReader_30             | 9990.00  | root      |                        | data:Selection_29                              |
|   │ └─Selection_29             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|   │   └─TableFullScan_28       | 10000.00 | cop[tikv] | table:t1, partition:p2 | keep order:false, stats:pseudo                 |
|   └─TableReader_36             | 9990.00  | root      |                        | data:Selection_35                              |
|     └─Selection_35             | 9990.00  | cop[tikv] |                        | not(isnull(test.t1.id))                        |
|       └─TableFullScan_34       | 10000.00 | cop[tikv] | table:t1, partition:p3 | keep order:false, stats:pseudo                 |
+--------------------------------+----------+-----------+------------------------+------------------------------------------------+
17 rows in set, 1 warning (0.00 sec)
```

例3から、 `TIDB_INLJ`のヒントが使用されている場合でも、パーティションテーブルのクエリでIndexJoinを使用して実行プランを選択できないことがわかります。

**例4** ：次の例では、クエリはIndexJoinで実行プランを使用して`dynamic`モードで実行されます。

{{< copyable "" >}}

```sql
mysql> set @@tidb_partition_prune_mode = 'dynamic';
Query OK, 0 rows affected (0.00 sec)

mysql> explain select /*+ TIDB_INLJ(t1, t2) */ t1.* from t1, t2 where t2.code = 0 and t2.id = t1.id;
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
| id                              | estRows  | task      | access object          | operator info                                                                                                       |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
| IndexJoin_11                    | 12.49    | root      |                        | inner join, inner:IndexLookUp_10, outer key:test.t2.id, inner key:test.t1.id, equal cond:eq(test.t2.id, test.t1.id) |
| ├─TableReader_16(Build)         | 9.99     | root      |                        | data:Selection_15                                                                                                   |
| │ └─Selection_15                | 9.99     | cop[tikv] |                        | eq(test.t2.code, 0), not(isnull(test.t2.id))                                                                        |
| │   └─TableFullScan_14          | 10000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                                                      |
| └─IndexLookUp_10(Probe)         | 1.25     | root      | partition:all          |                                                                                                                     |
|   ├─Selection_9(Build)          | 1.25     | cop[tikv] |                        | not(isnull(test.t1.id))                                                                                             |
|   │ └─IndexRangeScan_7          | 1.25     | cop[tikv] | table:t1, index:id(id) | range: decided by [eq(test.t1.id, test.t2.id)], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_8(Probe)     | 1.25     | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                                                      |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

例4から、 `dynamic`モードでは、クエリの実行時にIndexJoinを使用した実行プランが選択されていることがわかります。
