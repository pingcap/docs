---
title: Partitioning
summary: Learn how to use partitioning in TiDB.
---

# パーティショニング {#partitioning}

このドキュメントでは、TiDB のパーティショニングの実装について紹介します。

## パーティショニングの種類 {#partitioning-types}

このセクションでは、TiDB のパーティショニングの種類を紹介します。現在、TiDB は[範囲分割](#range-partitioning) 、 [範囲 COLUMNS パーティショニング](#range-columns-partitioning) 、 [List パーティショニング](#list-partitioning) 、 [List COLUMNS パーティショニング](#list-columns-partitioning) 、および[ハッシュパーティショニング](#hash-partitioning)をサポートしています。

範囲パーティション化、範囲 COLUMNS パーティション化、List パーティショニング、およびList COLUMNS パーティショニングを使用して、アプリケーションでの大量の削除によって引き起こされるパフォーマンスの問題を解決し、パーティションの高速削除操作をサポートします。ハッシュ パーティショニングは、大量の書き込みがある場合にデータを分散させるために使用されます。

### 範囲分割 {#range-partitioning}

テーブルが範囲でパーティション分割されている場合、各パーティションには、パーティション式の値が特定の範囲内にある行が含まれます。範囲は連続している必要がありますが、重複してはなりません。 `VALUES LESS THAN`を使用して定義できます。

次のように、人事レコードを含むテーブルを作成する必要があるとします。

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

必要に応じて、さまざまな方法で範囲によってテーブルを分割できます。たとえば、 `store_id`列を使用して分割できます。

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

このパーティション・スキームでは、 `store_id`が 1 から 5 である従業員に対応するすべての行が`p0`パーティションに格納され、 `store_id`が 6 から 10 であるすべての従業員が`p1`に格納されます。レンジ・パーティション化では、パーティションを最低から最高の順に並べる必要があります。

データ`(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`の行を挿入すると、それは`p2`パーティションに分類されます。しかし、 `store_id`が 20 より大きいレコードを挿入すると、エラーが報告されます。これは、TiDB がこのレコードを挿入すべきパーティションを認識できないためです。この場合、テーブルを作成するときに`MAXVALUE`を使用できます。

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

`MAXVALUE`他のすべての整数値より大きい整数値を表します。これで、 `store_id`が 16 (定義された最大値) 以上のすべてのレコードが`p3`パーティションに格納されます。

従業員の職務コード ( `job_code`列の値) でテーブルを分割することもできます。 2 桁のジョブ コードは正社員、3 桁のコードはオフィスおよびカスタマー サポート担当者、4 桁のコードは管理職を表すとします。次に、次のようにパーティションテーブルを作成できます。

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

この例では、正社員に関連するすべての行が`p0`パーティションに格納され、すべてのオフィスおよび顧客サポート担当者が`p1`パーティションに格納され、すべての管理職が`p2`パーティションに格納されます。

テーブルを`store_id`で分割する以外に、テーブルを日付で分割することもできます。たとえば、従業員の離職年で分割できます。

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

タイムスタンプ列を含む他のパーティション式を使用することはできません。

レンジ パーティション分割は、次の条件の 1 つ以上が満たされている場合に特に役立ちます。

-   古いデータを削除したい。前の例で`employees`テーブルを使用すると、 `ALTER TABLE employees DROP PARTITION p0;`使用するだけで、1991 年より前にこの会社を退職した従業員のすべてのレコードを削除できます。 `DELETE FROM employees WHERE YEAR(separated) <= 1990;`操作を実行するよりも高速です。
-   時刻または日付の値を含む列、または他の系列から生じる値を含む列を使用したい。
-   パーティション分割に使用される列に対してクエリを頻繁に実行する必要があります。たとえば、 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;`のようなクエリを実行すると、TiDB は`p2`パーティションのデータのみをスキャンする必要があることをすぐに認識できます。これは、他のパーティションが`WHERE`条件に一致しないためです。

### 範囲 COLUMNS パーティショニング {#range-columns-partitioning}

レンジ COLUMNS パーティショニングは、レンジ パーティショニングの一種です。パーティション分割キーとして 1 つ以上の列を使用できます。パーティション列のデータ型は、整数、文字列 ( `CHAR`または`VARCHAR` )、 `DATE` 、および`DATETIME`です。非 COLUMNS パーティショニングなどの式はサポートされていません。

名前でパーティション化し、古い無効なデータを削除すると仮定すると、次のようにテーブルを作成できます。

```sql
CREATE TABLE t (
  valid_until datetime,
  name varchar(255) CHARACTER SET ascii,
  notes text
)
PARTITION BY RANGE COLUMNS(name,valid_until)
(PARTITION `p2022-g` VALUES LESS THAN ('G','2023-01-01 00:00:00'),
 PARTITION `p2023-g` VALUES LESS THAN ('G','2024-01-01 00:00:00'),
 PARTITION `p2024-g` VALUES LESS THAN ('G','2025-01-01 00:00:00'),
 PARTITION `p2022-m` VALUES LESS THAN ('M','2023-01-01 00:00:00'),
 PARTITION `p2023-m` VALUES LESS THAN ('M','2024-01-01 00:00:00'),
 PARTITION `p2024-m` VALUES LESS THAN ('M','2025-01-01 00:00:00'),
 PARTITION `p2022-s` VALUES LESS THAN ('S','2023-01-01 00:00:00'),
 PARTITION `p2023-s` VALUES LESS THAN ('S','2024-01-01 00:00:00'),
 PARTITION `p2024-s` VALUES LESS THAN ('S','2025-01-01 00:00:00'),
 PARTITION `p2022-` VALUES LESS THAN (0x7f,'2023-01-01 00:00:00'),
 PARTITION `p2023-` VALUES LESS THAN (0x7f,'2024-01-01 00:00:00'),
 PARTITION `p2024-` VALUES LESS THAN (0x7f,'2025-01-01 00:00:00'))
```

データは、[&#39;&#39;, &#39;G&#39;)、[&#39;G&#39;, &#39;M&#39;)、[&#39;M&#39;, &#39;S&#39;) および [&#39;S&#39;,)] の範囲の年および名前で分割されます。これにより、 `name`と`valid_until`列の両方でパーティションのプルーニングを利用しながら、無効なデータを簡単に削除できます。この例では、 `[,)`左が閉じ、右が開いている範囲を示します。たとえば、 [&#39;G&#39;, &#39;M&#39;) は、 `G`と`G`から`M`を含み、 `M`を除く範囲を示します。

### 範囲 INTERVAL パーティショニング {#range-interval-partitioning}

Range INTERVAL パーティショニングは、Range パーティショニングを拡張したもので、指定した間隔のパーティションを簡単に作成できます。 v6.3.0 から、INTERVAL パーティショニングがシンタックス シュガーとして TiDB に導入されました。

> **警告：**
>
> これは実験的機能であり、予告なしに変更または削除される可能性があります。構文と実装は、GA の前に変更される可能性があります。バグを見つけた場合は、 [TiDB リポジトリ](https://github.com/pingcap/tidb/issues)で問題を開いてください。

構文は次のとおりです。

```sql
PARTITION BY RANGE [COLUMNS] (<partitioning expression>)
INTERVAL (<interval expression>)
FIRST PARTITION LESS THAN (<expression>)
LAST PARTITION LESS THAN (<expression>)
[NULL PARTITION]
[MAXVALUE PARTITION]
```

例えば：

```sql
CREATE TABLE employees (
    id int unsigned NOT NULL,
    fname varchar(30),
    lname varchar(30),
    hired date NOT NULL DEFAULT '1970-01-01',
    separated date DEFAULT '9999-12-31',
    job_code int,
    store_id int NOT NULL
) PARTITION BY RANGE (id)
INTERVAL (100) FIRST PARTITION LESS THAN (100) LAST PARTITION LESS THAN (10000) MAXVALUE PARTITION
```

次の表が作成されます。

```sql
CREATE TABLE `employees` (
  `id` int unsigned NOT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `lname` varchar(30) DEFAULT NULL,
  `hired` date NOT NULL DEFAULT '1970-01-01',
  `separated` date DEFAULT '9999-12-31',
  `job_code` int DEFAULT NULL,
  `store_id` int NOT NULL
)
PARTITION BY RANGE (`id`)
(PARTITION `P_LT_100` VALUES LESS THAN (100),
 PARTITION `P_LT_200` VALUES LESS THAN (200),
...
 PARTITION `P_LT_9900` VALUES LESS THAN (9900),
 PARTITION `P_LT_10000` VALUES LESS THAN (10000),
 PARTITION `P_MAXVALUE` VALUES LESS THAN (MAXVALUE))
```

範囲 INTERVAL パーティショニングは、 [範囲列](#range-columns-partitioning)パーティショニングでも機能します。

例えば：

```sql
CREATE TABLE monthly_report_status (
    report_id int NOT NULL,
    report_status varchar(20) NOT NULL,
    report_date date NOT NULL
)
PARTITION BY RANGE COLUMNS (report_date)
INTERVAL (1 MONTH) FIRST PARTITION LESS THAN ('2000-01-01') LAST PARTITION LESS THAN ('2025-01-01')
```

次のテーブルを作成します。

```
CREATE TABLE `monthly_report_status` (
  `report_id` int(11) NOT NULL,
  `report_status` varchar(20) NOT NULL,
  `report_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
PARTITION BY RANGE COLUMNS(`report_date`)
(PARTITION `P_LT_2000-01-01` VALUES LESS THAN ('2000-01-01'),
 PARTITION `P_LT_2000-02-01` VALUES LESS THAN ('2000-02-01'),
...
 PARTITION `P_LT_2024-11-01` VALUES LESS THAN ('2024-11-01'),
 PARTITION `P_LT_2024-12-01` VALUES LESS THAN ('2024-12-01'),
 PARTITION `P_LT_2025-01-01` VALUES LESS THAN ('2025-01-01'))
```

オプションのパラメーター`NULL PARTITION`は、定義が`PARTITION P_NULL VALUES LESS THAN (<minimum value of the column type>)`パーティションを作成し、パーティション式が`NULL`に評価された場合にのみ一致します。 [レンジ分割でのNULLの扱い](#handling-of-null-with-range-partitioning)参照してください。これは、 `NULL`が他のどの値よりも小さいと見なされることを説明しています。

オプションのパラメーター`MAXVALUE PARTITION`は、最後のパーティションを`PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`として作成します。

#### ALTER INTERVAL 分割テーブル {#alter-interval-partitioned-tables}

INTERVAL パーティショニングは、パーティションを追加および削除するためのより単純な構文も追加します。

次のステートメントは、最初のパーティションを変更します。値が指定された式より小さいすべてのパーティションを削除し、一致したパーティションを新しい最初のパーティションにします。 NULL PARTITION には影響しません。

```
ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)
```

次のステートメントは、最後のパーティションを変更します。つまり、より高い範囲と新しいデータ用のスペースを持つパーティションをさらに追加します。指定された式までの現在の間隔で新しいパーティションを追加します。データの再編成が必要なため、 `MAXVALUE PARTITION`存在する場合は機能しません。

```
ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)
```

#### INTERVAL パーティショニングの詳細と制限 {#interval-partitioning-details-and-limitations}

-   INTERVAL パーティショニング機能には、 `CREATE/ALTER TABLE`構文のみが含まれます。メタデータに変更はないため、新しい構文で作成または変更されたテーブルは引き続き MySQL と互換性があります。
-   MySQL の互換性を維持するために、 `SHOW CREATE TABLE`の出力形式に変更はありません。
-   新しい`ALTER`構文は、INTERVAL に準拠する既存のテーブルに適用されます。これらのテーブルを`INTERVAL`構文で作成する必要はありません。
-   `RANGE COLUMNS`の場合、integer、date、および datetime 列タイプのみがサポートされます。

### List パーティショニング {#list-partitioning}

リストパーティションテーブルを作成する前に、セッション変数の値を`tidb_enable_list_partition`から`ON`に設定する必要があります。

{{< copyable "" >}}

```sql
set @@session.tidb_enable_list_partition = ON
```

また、 `tidb_enable_table_partition`がデフォルト設定の`ON`に設定されていることを確認してください。

List パーティショニングは、レンジ パーティショニングに似ています。レンジ パーティション分割とは異なり、List パーティショニングでは、各パーティション内のすべての行のパーティション式の値が特定の値セットに含まれます。各パーティションに定義されたこの値セットは、任意の数の値を持つことができますが、重複する値を持つことはできません。 `PARTITION ... VALUES IN (...)`句を使用して、値セットを定義できます。

人事記録表を作成するとします。次のようにテーブルを作成できます。

{{< copyable "" >}}

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

次の表に示すように、4 つの地区に 20 の店舗が分布しているとします。

```
| Region  | Store ID Numbers     |
| ------- | -------------------- |
| North   | 1, 2, 3, 4, 5        |
| East    | 6, 7, 8, 9, 10       |
| West    | 11, 12, 13, 14, 15   |
| Central | 16, 17, 18, 19, 20   |
```

同じ地域の従業員の人事データを同じパーティションに格納する場合は、 `store_id`に基づいてリストパーティションテーブルを作成できます。

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

上記のようにパーティションを作成した後、テーブル内の特定の地域に関連するレコードを簡単に追加または削除できます。たとえば、East リージョン (East) のすべての店舗が別の会社に売却されたとします。次に、この地域の店舗従業員に関連するすべての行データを`ALTER TABLE employees TRUNCATE PARTITION pEast`実行することで削除できます。これは、同等のステートメント`DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)`よりもはるかに効率的です。

`ALTER TABLE employees DROP PARTITION pEast`を実行して関連するすべての行を削除することもできますが、このステートメントはテーブル定義から`pEast`パーティションも削除します。この状況では、 `ALTER TABLE ... ADD PARTITION`ステートメントを実行して、テーブルの元のパーティション スキームを復元する必要があります。

レンジ パーティション分割とは異なり、List パーティショニングには、他のパーティションに属さないすべての値を格納するための同様の`MAXVALUE`のパーティションはありません。代わりに、パーティション式のすべての予期される値を`PARTITION ... VALUES IN (...)`句に含める必要があります。 `INSERT`ステートメントに挿入される値がどのパーティションの列値セットとも一致しない場合、ステートメントは実行に失敗し、エラーが報告されます。次の例を参照してください。

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

上記のエラー タイプを無視するには、 `IGNORE`キーワードを使用できます。このキーワードを使用した後、どのパーティションの列値セットとも一致しない値が行に含まれている場合、この行は挿入されません。代わりに、値が一致する行が挿入され、エラーは報告されません。

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

### List COLUMNS パーティショニング {#list-columns-partitioning}

List COLUMNS パーティショニングは、 List パーティショニングの一種です。複数の列をパーティション キーとして使用できます。整数データ型のほかに、string、 `DATE` 、および`DATETIME`データ型の列をパーティション列として使用することもできます。

次の表に示すように、次の 12 都市の従業員を 4 つの地域に分割するとします。

```
| Region | Cities                         |
| :----- | ------------------------------ |
| 1      | LosAngeles,Seattle, Houston    |
| 2      | Chicago, Columbus, Boston      |
| 3      | NewYork, LongIsland, Baltimore |
| 4      | Atlanta, Raleigh, Cincinnati   |
```

以下に示すように、List COLUMNS パーティショニングを使用してテーブルを作成し、各行を従業員の都市に対応するパーティションに格納できます。

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

List パーティショニングとは異なり、 List COLUMNS パーティショニングでは、列の値を整数に変換するために`COLUMNS()`句で式を使用する必要はありません。

List COLUMNS パーティショニングは、次の例に示すように、 `DATE`型と`DATETIME`型の列を使用して実装することもできます。この例では、前の`employees_1`テーブルと同じ名前と列を使用していますが、 `hired`列に基づいてList COLUMNS パーティショニングを使用しています。

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

### ハッシュパーティショニング {#hash-partitioning}

ハッシュ パーティショニングは、データが特定の数のパーティションに均等に分散されるようにするために使用されます。レンジ パーティショニングでは、レンジ パーティショニングを使用する場合は各パーティションの列値の範囲を指定する必要がありますが、ハッシュ パーティショニングを使用する場合はパーティションの数を指定するだけで済みます。

ハッシュによるパーティション分割では、 `PARTITION BY HASH (expr)`句を`CREATE TABLE`ステートメントに追加する必要があります。 `expr`は整数を返す式です。この列のタイプが整数の場合は、列名にすることができます。さらに、 `PARTITIONS num`追加する必要がある場合もあります。ここで`num` 、テーブルが分割されているパーティションの数を示す正の整数です。

次の操作では、 `store_id`で 4 つのパーティションに分割されたハッシュパーティションテーブルが作成されます。

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

`PARTITIONS num`が指定されていない場合、デフォルトのパーティション数は 1 です。

`expr`の整数を返す SQL 式を使用することもできます。たとえば、雇用年でテーブルを分割できます。

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

最も効率的なハッシュ関数は、単一のテーブル列で動作し、その値が列の値に応じて一貫して増加または減少するものです。

たとえば、 `date_col`は型が`DATE`列であり、 `TO_DAYS(date_col)`式の値は`date_col`の値によって異なります。 `YEAR(date_col)`は`TO_DAYS(date_col)`とは異なります。これは、 `date_col`で考えられるすべての変更が`YEAR(date_col)`で同等の変更を生成するわけではないためです。

対照的に、タイプが`INT`の`int_col`列があるとします。式`POW(5-int_col,3) + 6`について考えてみましょう。ただし、 `int_col`の値が変化しても式の結果が比例して変化しないため、これは適切なハッシュ関数ではありません。 `int_col`での値の変更は、式の結果に大きな変化をもたらす可能性があります。たとえば、 `int_col` 5 から 6 に変化すると、式の結果の変化は -1 になります。しかし、 `int_col` 6 から 7 に変わると、結果の変化は -7 になる可能性があります。

結論から言うと、式が`y = cx`に近い形であればハッシュ関数の方が適しています。式が非線形であるほど、パーティション間でデータが不均一に分散される傾向があります。

理論的には、プルーニングは複数の列値を含む式でも可能ですが、そのような式のどれが適切かを判断することは非常に難しく、時間がかかる場合があります。このため、複数の列を含むハッシュ式の使用は特にお勧めしません。

`PARTITION BY HASH`を使用すると、TiDB は、式の結果のモジュラスに基づいて、データがどのパーティションに分類されるかを決定します。つまり、分割式が`expr`で分割数が`num`の場合、データを格納する分割は`MOD(expr, num)`で決まります。 `t1`が次のように定義されているとします。

{{< copyable "" >}}

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

データ行を`t1`に挿入し、 `col3`の値が「2005-09-15」の場合、この行はパーティション 1 に挿入されます。

```
MOD(YEAR('2005-09-01'),4)
=  MOD(2005,4)
=  1
```

#### TiDB が Linear Hash パーティションを処理する方法 {#how-tidb-handles-linear-hash-partitions}

v6.4.0 より前では、TiDB で[MySQL 線形ハッシュ](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html)パーティションの DDL ステートメントを実行すると、TiDB は非パーティション テーブルしか作成できませんでした。この場合、TiDB で分割されたテーブルを引き続き使用する場合は、DDL ステートメントを変更する必要があります。

v6.4.0 以降、TiDB は MySQL `PARTITION BY LINEAR HASH`構文の解析をサポートしていますが、その中の`LINEAR`キーワードを無視します。 MySQL Linear Hash パーティションの既存の DDL および DML ステートメントがいくつかある場合は、変更せずに TiDB でそれらを実行できます。

-   MySQL 線形ハッシュ パーティションの`CREATE`ステートメントの場合、TiDB は非線形ハッシュパーティションテーブルを作成します (TiDB には線形ハッシュパーティションテーブルがないことに注意してください)。パーティションの数が 2 の累乗である場合、TiDB ハッシュパーティションテーブルの行は、MySQL リニア ハッシュパーティションテーブルの行と同じように分散されます。それ以外の場合、TiDB でのこれらの行の分散は MySQL とは異なります。これは、非線形分割テーブルが単純な「分割のモジュラス数」を使用するのに対し、線形分割テーブルは「次の 2 の累乗を法とし、分割数と次の 2 の累乗の間で値を折り畳む」ことを使用するためです。詳細については、 [#38450](https://github.com/pingcap/tidb/issues/38450)を参照してください。

-   MySQL Linear Hash パーティションの他のすべてのステートメントについては、TiDB でも MySQL と同じように機能しますが、パーティションの数が 2 の累乗でない場合は行が異なる方法で分散され、 [パーティションの選択](#partition-selection) 、 `TRUNCATE PARTITION` 3 に対して異なる結果が得られます。と`EXCHANGE PARTITION` 。

### TiDB パーティショニングが NULL を処理する方法 {#how-tidb-partitioning-handles-null}

TiDB では、分割式の計算結果として`NULL`を使用できます。

> **ノート：**
>
> `NULL`は整数ではありません。 TiDB のパーティショニングの実装では、 `ORDER BY`と同様に、 `NULL`を他の整数値より小さいものとして扱います。

#### レンジ分割でのNULLの扱い {#handling-of-null-with-range-partitioning}

範囲によってパーティション化されたテーブルに行を挿入し、パーティションを決定するために使用される列の値が`NULL`である場合、この行は最下位のパーティションに挿入されます。

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

`p0`パーティションを削除し、結果を確認します。

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

#### ハッシュ分割によるNULLの扱い {#handling-of-null-with-hash-partitioning}

テーブルを Hash で分割する場合、 `NULL`値を処理する別の方法があります。分割式の計算結果が`NULL`の場合、それは`0`と見なされます。

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

挿入されたレコード`(NULL, 'mothra')` `(0, 'gigan')`と同じパーティションに分類されることがわかります。

> **ノート：**
>
> TiDB のハッシュ パーティションによる`NULL`値は[MySQL パーティショニングが NULL を処理する方法](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html)で説明されているのと同じ方法で処理されますが、これは MySQL の実際の動作とは一致しません。つまり、この場合の MySQL の実装は、そのドキュメントと一致していません。
>
> この場合、TiDB の実際の動作は、このドキュメントの説明に沿っています。

## パーティション管理 {#partition-management}

`LIST`および`RANGE`パーティション テーブルの場合、 `ALTER TABLE <table name> ADD PARTITION (<partition specification>)`または`ALTER TABLE <table name> DROP PARTITION <list of partitions>`ステートメントを使用してパーティションを追加および削除できます。

`LIST`および`RANGE`分割テーブルの場合、 `REORGANIZE PARTITION`はまだサポートされていません。

`HASH`分割テーブルの場合、 `COALESCE PARTITION`と`ADD PARTITION`はまだサポートされていません。

`EXCHANGE PARTITION` `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2`のようにテーブルの名前を変更するのと同様に、パーティションとパーティションテーブルを交換することで機能します。

たとえば、 `ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table` `partitioned_table`テーブル`p1`パーティションを`non_partitioned_table`テーブルとスワップします。

パーティションに交換するすべての行がパーティション定義と一致していることを確認してください。そうしないと、ステートメントは失敗します。

TiDB には、影響を与える可能性のある特定の機能がいくつかあることに注意してください`EXCHANGE PARTITION` 。テーブル構造にそのような機能が含まれている場合、 `EXCHANGE PARTITION` [MySQL の EXCHANGE PARTITION 条件](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html)を満たしていることを確認する必要があります。一方、これらの特定の機能が、パーティション化されたテーブルとパーティション化されていないテーブルの両方で同じように定義されていることを確認してください。これらの特定の機能には、次のものが含まれます。

<CustomContent platform="tidb">

-   [SQL の配置規則](/placement-rules-in-sql.md) : 配置ポリシーは同じです。

</CustomContent>

-   [TiFlash](/tikv-overview.md) : TiFlashレプリカの数は同じです。
-   [クラスタ化インデックス](/clustered-indexes.md) : パーティション化されたテーブルとパーティション化されていないテーブルの両方が`CLUSTERED` 、または両方が`NONCLUSTERED`です。

さらに、 `EXCHANGE PARTITION`と他のコンポーネントとの互換性には制限があります。パーティション化されたテーブルとパーティション化されていないテーブルの両方が同じ定義を持っている必要があります。

-   TiFlash: 分割テーブルと非分割テーブルのTiFlashレプリカ定義が異なる場合、 `EXCHANGE PARTITION`操作は実行できません。
-   TiCDC: TiCDC は、パーティション化されたテーブルとパーティション化されていないテーブルの両方に主キーまたは一意のキーがある場合に、 `EXCHANGE PARTITION`操作をレプリケートします。そうしないと、TiCDC は操作を複製しません。
-   TiDB LightningおよびBR: TiDB Lightningを使用したインポート中、またはBRを使用した復元中は、 `EXCHANGE PARTITION`操作を実行しないでください。

### レンジパーティション管理 {#range-partition-management}

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

パーティションをドロップします。

{{< copyable "" >}}

```sql
ALTER TABLE members DROP PARTITION p2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

パーティションを空にします。

{{< copyable "" >}}

```sql
ALTER TABLE members TRUNCATE PARTITION p1;
```

```
Query OK, 0 rows affected (0.03 sec)
```

> **ノート：**
>
> `ALTER TABLE ... REORGANIZE PARTITION`は現在、TiDB ではサポートされていません。

パーティションを追加します。

{{< copyable "" >}}

```sql
ALTER TABLE members ADD PARTITION (PARTITION p3 VALUES LESS THAN (2010));
```

テーブルを範囲で分割する場合、 `ADD PARTITION`パーティション リストの最後にのみ追加できます。既存の Range パーティションに追加すると、エラーが報告されます。

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

レンジ パーティショニングとは異なり、ハッシュ パーティショニングでは`DROP PARTITION`はサポートされません。

現在、 `ALTER TABLE ... COALESCE PARTITION`は TiDB でもサポートされていません。現在サポートされていないパーティション管理ステートメントの場合、TiDB はエラーを返します。

{{< copyable "" >}}

```sql
alter table members optimize partition p0;
```

```sql
ERROR 8200 (HY000): Unsupported optimize partition
```

## パーティションの剪定 {#partition-pruning}

[パーティションの剪定](/partition-pruning.md)は、非常に単純なアイデアに基づく最適化です。一致しないパーティションはスキャンしません。

パーティションテーブル`t1`を作成するとします。

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

この`SELECT`ステートメントの結果を取得したい場合:

{{< copyable "" >}}

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

結果が`p1`または`p2`パーティションのいずれかに該当することは明らかです。つまり、 `p1`および`p2`で一致する行を検索するだけで済みます。不要なパーティションを除外することは、いわゆる「プルーニング」です。オプティマイザーがパーティションの一部をプルーニングできる場合、パーティションテーブルでのクエリの実行は、パーティション化されていないパーティションテーブルでのクエリの実行よりもはるかに高速になります。

オプティマイザは、次の 2 つのシナリオで`WHERE`条件を使用してパーティションをプルーニングできます。

-   partition_column = 定数
-   partition_column IN (定数 1、定数 2、...、定数 N)

現在、パーティションプルーニングは`LIKE`条件では機能しません。

### パーティションのプルーニングが有効になるケース {#some-cases-for-partition-pruning-to-take-effect}

1.  パーティションのプルーニングはパーティションテーブルのクエリ条件を使用するため、プランナーの最適化ルールに従ってクエリ条件をパーティションテーブルにプッシュ ダウンできない場合、パーティションのプルーニングはこのクエリには適用されません。

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

    このクエリでは、左アウト結合が内部結合に変換され、次に`t1.x = t2.x`と`t2.x > 5`から`t1.x > 5`が導出されるため、パーティションのプルーニングで使用でき、パーティション`p1`のみが残ります。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    このクエリでは、 `t2.x > 5` `t1`パーティションテーブルにプッシュ ダウンできないため、このクエリではパーティションのプルーニングは有効になりません。

2.  パーティションのプルーニングはプランの最適化フェーズで行われるため、実行フェーズまでフィルター条件が不明な場合には適用されません。

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

    このクエリは`t2`から行を読み取り、その結果を`t1`のサブクエリに使用します。理論的には、パーティションのプルーニングはサブクエリの`t1.x > val`式の恩恵を受ける可能性がありますが、実行フェーズで発生するため、そこでは効果がありません。

3.  現在の実装の制限により、クエリ条件を TiKV にプッシュ ダウンできない場合、パーティション プルーニングで使用できません。

    例として`fn(col)`式を取り上げます。 TiKV コプロセッサがこの`fn`関数をサポートしている場合、 `fn(col)` 、計画最適化フェーズ中に述語プッシュダウン ルールに従ってリーフ ノード (つまり、パーティションテーブル) にプッシュ ダウンされる可能性があり、パーティション プルーニングで使用できます。

    TiKV コプロセッサがこの`fn`機能をサポートしていない場合、 `fn(col)`リーフ ノードにプッシュされません。代わりに、リーフ ノードの`Selection`ノード上になります。現在のパーティション プルーニングの実装では、この種のプラン ツリーはサポートされていません。

4.  ハッシュ パーティションの場合、パーティションのプルーニングでサポートされる唯一のクエリは、等しい条件です。

5.  範囲パーティションの場合、パーティションのプルーニングを有効にするには、パーティション式が`col`または`fn(col)`の形式である必要があり、クエリ条件が`>` 、 `<` 、 `=` 、 `>=` 、および`<=`のいずれかである必要があります。パーティション式が`fn(col)`の形式の場合、 `fn`関数は単調でなければなりません。

    `fn`関数が単調な場合、任意の`x`および`y`に対して、 `x > y`の場合、 `fn(x) > fn(y)` .すると、この`fn`関数は厳密に単調であると言えます。任意の`x`および`y`場合、 `x > y`の場合は`fn(x) >= fn(y)` 。この場合、 `fn` 「単調」とも言えます。理論的には、すべての単調な関数はパーティション プルーニングによってサポートされます。

    現在、TiDB でのパーティションのプルーニングは、次のような単調な関数のみをサポートしています。

    -   [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    -   [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)

    たとえば、パーティション式は単純な列です。

    {{< copyable "" >}}

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    または、パーティション式は`fn(col)`の形式で、 `fn`は`to_days`です。

    {{< copyable "" >}}

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    例外は、パーティション式として`floor(unix_timestamp())`です。 TiDB はケースバイケースで最適化を行うため、パーティションのプルーニングによってサポートされます。

    {{< copyable "" >}}

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where ts > '2020-04-18 02:00:42.123';
    ```

## パーティションの選択 {#partition-selection}

`SELECT`ステートメントは、 `PARTITION`オプションを使用して実装されるパーティション選択をサポートします。

{{< copyable "" >}}

```sql
SET @@sql_mode = '';

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

`p1`パーティションに格納されている行を表示できます。

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

複数のパーティションの行を取得する場合は、コンマで区切られたパーティション名のリストを使用できます。たとえば、 `SELECT * FROM employees PARTITION (p1, p2)` `p1`および`p2`パーティションのすべての行を返します。

パーティション選択を使用する場合でも、 `WHERE`条件と`ORDER BY`や`LIMIT`などのオプションを使用できます。 `HAVING`や`GROUP BY`などの集計オプションの使用もサポートされています。

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

パーティションの選択は、レンジ パーティション分割やハッシュ パーティション分割など、すべてのタイプのテーブル パーティション分割でサポートされています。ハッシュ パーティションの場合、パーティション名が指定されていない場合、 `p0` 、 `p1` 、 `p2` 、...、または`pN-1`がパーティション名として自動的に使用されます。

`SELECT` in `INSERT ... SELECT`はパーティション選択も使用できます。

## パーティションに関する制限と制限 {#restrictions-and-limitations-on-partitions}

このセクションでは、TiDB のパーティション分割されたテーブルに関するいくつかの制限と制限を紹介します。

### 分割キー、主キー、一意キー {#partitioning-keys-primary-keys-and-unique-keys}

このセクションでは、分割キーと主キーおよび一意キーとの関係について説明します。この関係を管理するルールは、次のように表現できます。**テーブルのすべての一意のキーは、テーブルのパーティション式のすべての列を使用する必要があります**。これにはテーブルの主キーも含まれます。これは定義上、一意のキーであるためです。

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

いずれの場合も、提案されたテーブルには、パーティション式で使用されるすべての列を含まない一意のキーが少なくとも 1 つあります。

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

次の例では、エラーが表示されます。

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

`col1`と`col3`の両方が提案されたパーティション化キーに含まれているため、 `CREATE TABLE`ステートメントは失敗しますが、これらの列はどちらもテーブルの両方の一意のキーの一部ではありません。次の変更後、 `CREATE TABLE`ステートメントが有効になります。

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

両方の一意のキーに属する列をパーティション化キーに含める方法がないため、次のテーブルはまったくパーティション化できません。

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

すべての主キーは定義上一意のキーであるため、次の 2 つのステートメントは無効です。

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

上記の例では、パーティション式で参照されるすべての列が主キーに含まれているわけではありません。主キーに欠落している列を追加すると、 `CREATE TABLE`ステートメントが有効になります。

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

DDL ステートメントを使用してテーブルを変更する場合、一意のインデックスを追加するときに、この制限も考慮する必要があります。たとえば、次のようにパーティションテーブルを作成するとします。

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

`ALTER TABLE`ステートメントを使用して、一意でないインデックスを追加できます。ただし、一意のインデックスを追加する場合は、 `c1`列を一意のインデックスに含める必要があります。

パーティションテーブルを使用する場合、プレフィックス インデックスを一意の属性として指定することはできません。

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

### 関数に関するパーティショニングの制限事項 {#partitioning-limitations-relating-to-functions}

パーティショニング式では、次のリストに示す関数のみを使用できます。

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

### MySQL との互換性 {#compatibility-with-mysql}

現在、TiDB は、Range パーティショニング、Range COLUMNS パーティショニング、 List パーティショニング、 List COLUMNS パーティショニング、および Hash パーティショニングをサポートしています。キー パーティショニングなど、MySQL で利用可能な他のパーティショニング タイプは、TiDB ではまだサポートされていません。

パーティション管理に関しては、下部の実装でデータを移動する必要がある操作は現在サポートされていません。これには、ハッシュパーティションテーブルのパーティション数の調整、レンジパーティションテーブルの範囲の変更、パーティションのマージ、およびこれらに限定されません。パーティションを交換します。

サポートされていないパーティショニング タイプの場合、TiDB でテーブルを作成すると、パーティショニング情報は無視され、通常の形式でテーブルが作成され、警告が報告されます。

`LOAD DATA`構文は、現在 TiDB でのパーティション選択をサポートしていません。

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

パーティションテーブルの場合、 `select * from t`によって返される結果はパーティション間で順序付けされていません。これは、パーティション間では順序付けされているが、パーティション内では順序付けられていない MySQL の結果とは異なります。

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

TiDB は毎回異なる結果を返します。次に例を示します。

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

MySQL に返される結果:

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

この変数は、テーブルの作成でのみ使用されます。テーブルが作成された後、この変数の値を変更しても効果はありません。詳細については、 [システム変数](/system-variables.md#tidb_enable_list_partition-new-in-v50)を参照してください。

### 動的プルーニングモード {#dynamic-pruning-mode}

TiDB は、パーティション化されたテーブルに`dynamic`または`static`モードでアクセスします。 v6.3.0 以降、デフォルトで`dynamic`モードが使用されます。ただし、動的パーティション分割は、完全なテーブル レベルの統計 (GlobalStats) が収集された後にのみ有効になります。 GlobalStats が収集される前に、TiDB は代わりに`static`モードを使用します。 GlobalStats の詳細については、 [動的プルーニング モードで分割されたテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)を参照してください。

{{< copyable "" >}}

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

手動の ANALYZE と通常のクエリでは、セッション レベル`tidb_partition_prune_mode`の設定が使用されます。バックグラウンドでの`auto-analyze`操作は、グローバル`tidb_partition_prune_mode`設定を使用します。

`static`モードでは、パーティション テーブルはパーティション レベルの統計を使用します。 `dynamic`モードでは、分割されたテーブルはテーブル レベルの GlobalStats を使用します。

`static`モードから`dynamic`モードに切り替える場合は、手動で統計を確認して収集する必要があります。これは、 `dynamic`モードに切り替えた後、パーティション化されたテーブルにはパーティション レベルの統計のみがあり、テーブル レベルの統計がないためです。 GlobalStats は、次の`auto-analyze`操作時にのみ収集されます。

{{< copyable "" >}}

```sql
set session tidb_partition_prune_mode = 'dynamic';
show stats_meta where table_name like "t";
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
| test    | t          | p1             | 2022-05-27 20:23:34 |            2 |         4 |
| test    | t          | p2             | 2022-05-27 20:23:34 |            2 |         4 |
+---------+------------+----------------+---------------------+--------------+-----------+
3 rows in set (0.01 sec)
```

グローバル`dynamic`プルーニング モードを有効にした後、SQL ステートメントで使用される統計が正しいことを確認するには、テーブルまたはテーブルのパーティションで`analyze`手動でトリガーして、GlobalStats を取得する必要があります。

{{< copyable "" >}}

```sql
analyze table t partition p1;
show stats_meta where table_name like "t";
```

```
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          | global         | 2022-05-27 20:50:53 |            0 |         5 |
| test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
| test    | t          | p1             | 2022-05-27 20:50:52 |            0 |         2 |
| test    | t          | p2             | 2022-05-27 20:50:08 |            0 |         2 |
+---------+------------+----------------+---------------------+--------------+-----------+
4 rows in set (0.00 sec)
```

`analyze`処理中に次の警告が表示された場合は、パーティションの統計に一貫性がないため、これらのパーティションまたはテーブル全体の統計を再度収集する必要があります。

```
| Warning | 8244 | Build table: `t` column: `a` global-level stats failed due to missing partition-level column stats, please run analyze table to refresh columns of all partitions
```

スクリプトを使用して、分割されたすべてのテーブルの統計を更新することもできます。詳細については、 [動的プルーニング モードで分割されたテーブルの統計を更新する](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode)を参照してください。

テーブル レベルの統計の準備ができたら、グローバルな動的プルーニング モードを有効にできます。これは、すべての SQL ステートメントと`auto-analyze`の操作に有効です。

{{< copyable "" >}}

```sql
set global tidb_partition_prune_mode = dynamic
```

`static`モードでは、TiDB は複数の演算子を使用して各パーティションに個別にアクセスし、次に`Union`を使用して結果をマージします。次の例は、TiDB が`Union`を使用して 2 つの対応するパーティションの結果をマージする単純な読み取り操作です。

{{< copyable "" >}}

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id) (
    ->     partition p0 values less than (100),
    ->     partition p1 values less than (200),
    ->     partition p2 values less than (300),
    ->     partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
```

```
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

`dynamic`モードでは、各オペレーターが複数のパーティションへの直接アクセスをサポートするため、TiDB は`Union`使用しなくなりました。

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

上記のクエリ結果から、パーティションのプルーニングがまだ有効であり、実行プランが`p0`と`p1`にのみアクセスしている間に、実行プランの`Union`演算子が消えていることがわかります。

`dynamic`モードでは、実行計画がより単純かつ明確になります。 Union 操作を省略すると、実行効率が向上し、Union 同時実行の問題を回避できます。さらに、 `dynamic`モードでは、 `static`モードでは使用できない IndexJoin を使用した実行プランも可能です。 (以下の例を参照)

**例 1** : 次の例では、IndexJoin を使用した実行プランを使用して、クエリが`static`モードで実行されます。

{{< copyable "" >}}

```sql
mysql> create table t1 (id int, age int, key(id)) partition by range(id)
    -> (partition p0 values less than (100),
    ->  partition p1 values less than (200),
    ->  partition p2 values less than (300),
    ->  partition p3 values less than (400));
Query OK, 0 rows affected (0,08 sec)

mysql> create table t2 (id int, code int);
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

mysql> show warnings;
+---------+------+------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                            |
+---------+------+------------------------------------------------------------------------------------+
| Warning | 1815 | Optimizer Hint /*+ INL_JOIN(t1, t2) */ or /*+ TIDB_INLJ(t1, t2) */ is inapplicable |
+---------+------+------------------------------------------------------------------------------------+
1 row in set (0,00 sec)
```

例 1 から、 `TIDB_INLJ`ヒントを使用しても、パーティションテーブルに対するクエリは IndexJoin で実行プランを選択できないことがわかります。

**例 2** : 次の例では、クエリは IndexJoin を使用した実行プランを使用して`dynamic`モードで実行されます。

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
| └─IndexLookUp_10(Probe)         | 12.49    | root      | partition:all          |                                                                                                                     |
|   ├─Selection_9(Build)          | 12.49    | cop[tikv] |                        | not(isnull(test.t1.id))                                                                                             |
|   │ └─IndexRangeScan_7          | 12.50    | cop[tikv] | table:t1, index:id(id) | range: decided by [eq(test.t1.id, test.t2.id)], keep order:false, stats:pseudo                                      |
|   └─TableRowIDScan_8(Probe)     | 12.49    | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                                                      |
+---------------------------------+----------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------------+
8 rows in set (0.00 sec)
```

例 2 から、 `dynamic`モードでは、クエリを実行すると IndexJoin を使用した実行プランが選択されることがわかります。

現在、プルーニング モード`static`と`dynamic`のどちらも、準備済みステートメントのプラン キャッシュをサポートしていません。

#### 動的プルーニング モードで分割されたテーブルの統計を更新する {#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

1.  分割されたすべてのテーブルを見つけます。

    {{< copyable "" >}}

    ```sql
    SELECT DISTINCT CONCAT(TABLE_SCHEMA,'.', TABLE_NAME)
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA', 'mysql', 'sys', 'PERFORMANCE_SCHEMA', 'METRICS_SCHEMA');
    ```

    ```
    +-------------------------------------+
    | concat(TABLE_SCHEMA,'.',TABLE_NAME) |
    +-------------------------------------+
    | test.t                              |
    +-------------------------------------+
    1 row in set (0.02 sec)
    ```

2.  すべての分割テーブルの統計を更新するためのステートメントを生成します。

    {{< copyable "" >}}

    ```sql
    select distinct concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;')
        from information_schema.PARTITIONS
        where TABLE_SCHEMA not in ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');
    +----------------------------------------------------------------------+
    | concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') |
    +----------------------------------------------------------------------+
    | ANALYZE TABLE test.t ALL COLUMNS;                                    |
    +----------------------------------------------------------------------+
    1 row in set (0.01 sec)
    ```

    `ALL COLUMNS`を必要な列に変更できます。

3.  バッチ更新ステートメントをファイルにエクスポートします。

    {{< copyable "" >}}

    ```sql
    mysql --host xxxx --port xxxx -u root -p -e "select distinct concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') \
        from information_schema.PARTITIONS \
        where TABLE_SCHEMA not in ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');" | tee gatherGlobalStats.sql
    ```

4.  バッチ更新を実行します。

    `source`コマンドを実行する前に SQL ステートメントを処理します。

    ```
    sed -i "" '1d' gatherGlobalStats.sql --- mac
    sed -i '1d' gatherGlobalStats.sql --- linux
    ```

    {{< copyable "" >}}

    ```sql
    SET session tidb_partition_prune_mode = dynamic;
    source gatherGlobalStats.sql
    ```
