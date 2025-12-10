---
title: Partitioning
summary: TiDB でパーティショニングを使用する方法を学習します。
---

# パーティショニング {#partitioning}

このドキュメントでは、TiDB のパーティショニングの実装について説明します。

## パーティションの種類 {#partitioning-types}

このセクションでは、TiDBにおけるパーティションの種類について説明します。現在、TiDBは[範囲分割](#range-partitioning) 、 [範囲列パーティション](#range-columns-partitioning) 、 [List パーティショニング](#list-partitioning) 、 [List COLUMNS パーティショニング](#list-columns-partitioning) 、 [ハッシュパーティショニング](#hash-partitioning) 、および[キーパーティショニング](#key-partitioning)をサポートしています。

-   範囲パーティション、範囲列パーティション、List パーティショニング、およびList COLUMNS パーティショニングは、アプリケーションでの大量の削除によって発生するパフォーマンスの問題を解決するために使用され、パーティションの迅速な削除をサポートします。
-   ハッシュ・パーティショニングとキー・パーティショニングは、書き込み回数が多いシナリオでデータを分散するために使用されます。ハッシュ・パーティショニングと比較して、キー・パーティショニングは複数列のデータの分散と非整数列によるパーティショニングをサポートします。

### 範囲分割 {#range-partitioning}

テーブルが範囲でパーティション化されている場合、各パーティションには、パーティション式の値が指定された範囲内にある行が含まれます。範囲は連続している必要がありますが、重複してはなりません。範囲は`VALUES LESS THAN`で定義できます。

次のような人事記録を含むテーブルを作成する必要があるとします。

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

必要に応じて、様々な方法でテーブルを範囲でパーティション分割できます。例えば、 `store_id`列目を使ってパーティション分割できます。

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

このパーティションスキームでは、 `store_id`が 1 から 5 までの従業員に対応するすべての行が`p0`パーティションに格納され、 `store_id`が 6 から 10 までの従業員に対応するすべての行が`p1`パーティションに格納されます。範囲パーティション分割では、パーティションを最小から最大の順に並べる必要があります。

`(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`というデータ行を挿入すると、パーティション`p2`に該当します。しかし、 `store_id`が 20 より大きいレコードを挿入すると、TiDB はどのパーティションに挿入すべきかを判断できないため、エラーが報告されます。この場合、テーブル作成時に`MAXVALUE`使用できます。

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

`MAXVALUE`他のすべての整数値よりも大きい整数値を表します。つまり、 `store_id`が16（定義されている最大値）以上のすべてのレコードは、 `p3`パーティションに格納されます。

従業員の職種コード（ `job_code`列目の値）でテーブルをパーティション分割することもできます。2桁の職種コードは一般従業員、3桁のコードは事務・顧客サポート担当者、4桁のコードは管理職を表すと仮定します。こうすると、次のようなパーティションテーブルを作成できます。

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

この例では、正社員に関連するすべての行は`p0`パーティションに格納され、オフィスおよび顧客サポート担当者はすべて`p1`番目のパーティションに格納され、管理職はすべて`p2`パーティションに格納されます。

テーブルを`store_id`で分割するだけでなく、日付でパーティション分割することもできます。例えば、従業員の退職年でパーティション分割できます。

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

範囲パーティション分割では、 `timestamp`列目の値に基づいてパーティション分割し、 `unix_timestamp()`関数を使用できます。次に例を示します。

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

範囲パーティション分割は、次の条件の 1 つ以上が満たされている場合に特に役立ちます。

-   古いデータを削除したいとします。前の例のテーブル`employees`を使用すると、 `ALTER TABLE employees DROP PARTITION p0;`実行するだけで、1991年以前にこの会社を退職した従業員のすべてのレコードを削除できます。 `DELETE FROM employees WHERE YEAR(separated) <= 1990;`を実行するよりも高速です。
-   時刻または日付の値を含む列、あるいは他の系列から発生した値を含む列を使用します。
-   パーティション分割に使用する列に対して、頻繁にクエリを実行する必要があります。例えば、 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;`ようなクエリを実行する場合、TiDBは`p2`パーティションのデータのみをスキャンする必要があることをすぐに認識します。これは、他のパーティションが`WHERE`条件に一致しないためです。

### 範囲列パーティション {#range-columns-partitioning}

レンジCOLUMNSパーティショニングは、レンジパーティショニングの一種です。1つ以上の列をパーティショニングキーとして使用できます。パーティション列のデータ型は、整数、文字列（ `CHAR`または`VARCHAR` ）、 `DATE` `DATETIME`いずれかです。COLUMNS以外のパーティショニングなどの式はサポートされていません。

レンジパーティションと同様に、レンジ列パーティションでもパーティション範囲は厳密に増加する必要があります。次の例のパーティション定義はサポートされていません。

```sql
CREATE TABLE t(
    a int,
    b datetime,
    c varchar(8)
) PARTITION BY RANGE COLUMNS(`c`,`b`)
(PARTITION `p20240520A` VALUES LESS THAN ('A','2024-05-20 00:00:00'),
 PARTITION `p20240520Z` VALUES LESS THAN ('Z','2024-05-20 00:00:00'),
 PARTITION `p20240521A` VALUES LESS THAN ('A','2024-05-21 00:00:00'));
```

    Error 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

名前でパーティション分割し、古くて無効なデータを削除する場合は、次のようにテーブルを作成できます。

```sql
CREATE TABLE t (
  valid_until datetime,
  name varchar(255) CHARACTER SET ascii,
  notes text
)
PARTITION BY RANGE COLUMNS(name, valid_until)
(PARTITION `p2022-g` VALUES LESS THAN ('G','2023-01-01 00:00:00'),
 PARTITION `p2023-g` VALUES LESS THAN ('G','2024-01-01 00:00:00'),
 PARTITION `p2022-m` VALUES LESS THAN ('M','2023-01-01 00:00:00'),
 PARTITION `p2023-m` VALUES LESS THAN ('M','2024-01-01 00:00:00'),
 PARTITION `p2022-s` VALUES LESS THAN ('S','2023-01-01 00:00:00'),
 PARTITION `p2023-s` VALUES LESS THAN ('S','2024-01-01 00:00:00'))
```

上記のSQL文は、 `[ ('', ''), ('G', '2023-01-01 00:00:00') )` `[ ('S', '2023-01-01 00:00:00'), ('S', '2024-01-01 00:00:00') )`範囲でデータを年と名前でパーティション分割します。これにより`[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` `name` `[ ('M', '2023-01-01 00:00:00'), ('M', '2024-01-01 00:00:00') )` `[ ('G', '2024-01-01 00:00:00'), ('M', '2023-01-01 00:00:00') )` `[ ('M', '2024-01-01 00:00:00'), ('S', '2023-01-01 00:00:00') )` `valid_until`目の両方でパーティションプルーニングのメリットを活用しながら、無効なデータを簡単に削除できます。この例では、 `[,)`左閉じ、右開きの範囲を示しています。例えば、 `[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 、名前が`'G'` 、年に`2023-01-01 00:00:00`が含まれ、 `2023-01-01 00:00:00`より大きく`2024-01-01 00:00:00`より小さいデータの範囲を示しています。29 `(G, 2024-01-01 00:00:00)`含まれません。

### 範囲INTERVALパーティション分割 {#range-interval-partitioning}

レンジ・インターバル・パーティショニングはレンジ・パーティショニングの拡張版であり、指定した間隔のパーティションを簡単に作成できます。バージョン6.3.0以降、インターバル・パーティショニングはTiDBにシンタックスシュガーとして導入されました。

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

次のテーブルが作成されます。

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

範囲 INTERVAL パーティションは[範囲列](#range-columns-partitioning)パーティションでも機能します。

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

次のテーブルが作成されます。

    CREATE TABLE `monthly_report_status` (
      `report_id` int NOT NULL,
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

オプションパラメータ`NULL PARTITION` 、定義が`PARTITION P_NULL VALUES LESS THAN (<minimum value of the column type>)`であるパーティションを作成します。これは、パーティション式が`NULL`と評価される場合にのみ一致します。 [範囲分割によるNULLの扱い](#handling-of-null-with-range-partitioning)参照してください。これは、 `NULL`他のどの値よりも小さいとみなされることを示しています。

オプションパラメータ`MAXVALUE PARTITION` 、最後のパーティションを`PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`として作成します。

#### ALTER INTERVAL パーティションテーブル {#alter-interval-partitioned-tables}

INTERVAL パーティション化では、パーティションの追加と削除のためのより簡単な構文も追加されます。

次の文は最初のパーティションを変更します。指定された式より小さい値を持つすべてのパーティションを削除し、一致したパーティションを新しい最初のパーティションにします。NULLパーティションには影響しません。

    ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)

次の文は最後のパーティションを変更します。つまり、より広い範囲を持つパーティションを追加し、新しいデータのためのスペースを確保します。指定された式を含む、現在のINTERVALを持つ新しいパーティションが追加されます。1 `MAXVALUE PARTITION`存在する場合は、データの再編成が必要となるため、この文は機能しません。

    ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)

#### INTERVALパーティションの詳細と制限 {#interval-partitioning-details-and-limitations}

-   INTERVALパーティショニング機能は`CREATE/ALTER TABLE`構文のみを使用します。メタデータには変更がないため、新しい構文で作成または変更されたテーブルは引き続きMySQLと互換性があります。
-   MySQLの互換性を保つため、 `SHOW CREATE TABLE`の出力形式には変更はありません。
-   新しい構文`ALTER`は、INTERVALに準拠する既存のテーブルに適用されます。これらのテーブルを構文`INTERVAL`で作成する必要はありません。
-   `RANGE COLUMNS`パーティションに`INTERVAL`構文を使用する場合、パーティション キーとして指定できるのは`INTEGER` 、 `DATE` 、または`DATETIME`タイプの 1 つの列のみです。

### List パーティショニング {#list-partitioning}

List パーティショニングはレンジパーティションに似ています。レンジパーティションとは異なり、List パーティショニングでは、各パーティションのすべての行のパーティション式の値が特定の値セットに含まれます。各パーティションに定義されたこの値セットには、任意の数の値を含めることができますが、重複する値を含めることはできません。値セットを定義するには、 `PARTITION ... VALUES IN (...)`句を使用します。

人事記録テーブルを作成したいとします。テーブルは次のように作成できます。

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

次の表に示すように、4 つの地区に 20 店舗が分散しているとします。

    | Region  | Store ID Numbers     |
    | ------- | -------------------- |
    | North   | 1, 2, 3, 4, 5        |
    | East    | 6, 7, 8, 9, 10       |
    | West    | 11, 12, 13, 14, 15   |
    | Central | 16, 17, 18, 19, 20   |

同じ地域の従業員の人事データを同じパーティションに保存する場合は、 `store_id`に基づいてリストパーティションテーブルを作成できます。

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

上記のようにパーティションを作成すれば、テーブル内の特定の地域に関連するレコードを簡単に追加または削除できます。例えば、東部地域（East）のすべての店舗が別の会社に売却されたとします。この場合、 `ALTER TABLE employees TRUNCATE PARTITION pEast`実行することで、この地域の店舗従業員に関連するすべての行データを削除できます。これは、同等のステートメント`DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)`を実行するよりもはるかに効率的です。

`ALTER TABLE employees DROP PARTITION pEast`実行して関連するすべての行を削除することもできますが、このステートメントはテーブル定義から`pEast`目のパーティションも削除します。この場合、テーブルの元のパーティションスキームを復元するには、 `ALTER TABLE ... ADD PARTITION`目のステートメントを実行する必要があります。

#### デフォルトのリストパーティション {#default-list-partition}

バージョン7.3.0以降では、リストまたはリスト列パーティションテーブルにデフォルトパーティションを追加できます。デフォルトパーティションはフォールバックパーティションとして機能し、どのパーティションの値セットにも一致しない行を配置できます。

> **注記：**
>
> この機能は、MySQL構文に対するTiDBの拡張です。デフォルトパーティションを持つリストまたはリスト列パーティションテーブルの場合、テーブル内のデータはMySQLに直接複製できません。

次のリストパーティションテーブルを例に挙げます。

```sql
CREATE TABLE t (
  a INT,
  b INT
)
PARTITION BY LIST (a) (
  PARTITION p0 VALUES IN (1, 2, 3),
  PARTITION p1 VALUES IN (4, 5, 6)
);
Query OK, 0 rows affected (0.11 sec)
```

次のように、 `pDef`という名前のデフォルトのリスト パーティションをテーブルに追加できます。

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef DEFAULT);
```

または

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef VALUES IN (DEFAULT));
```

この方法では、どのパーティションの値セットにも一致しない新しく挿入された値は、自動的にデフォルトのパーティションに移動されます。

```sql
INSERT INTO t VALUES (7, 7);
Query OK, 1 row affected (0.01 sec)
```

リストまたはリスト列パーティションテーブルを作成するときに、デフォルトのパーティションを追加することもできます。例:

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
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20),
    PARTITION pDefault DEFAULT
);
```

デフォルトパーティションのないリストまたはリスト列パーティションテーブルの場合、 `INSERT`番目のステートメントを使用して挿入する値は、テーブルの`PARTITION ... VALUES IN (...)`番目の句で定義された値セットと一致する必要があります。挿入する値がどのパーティションの値セットとも一致しない場合、ステートメントは失敗し、次の例に示すようにエラーが返されます。

```sql
CREATE TABLE t (
  a INT,
  b INT
)
PARTITION BY LIST (a) (
  PARTITION p0 VALUES IN (1, 2, 3),
  PARTITION p1 VALUES IN (4, 5, 6)
);
Query OK, 0 rows affected (0.11 sec)

INSERT INTO t VALUES (7, 7);
ERROR 1525 (HY000): Table has no partition for value 7
```

上記のエラーを無視するには、 `INSERT`ステートメントにキーワード`IGNORE`を追加します。このキーワードを追加すると、 `INSERT`ステートメントはパーティション値セットに一致する行のみを挿入し、一致しない行は挿入しません。エラーは返されません。

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

List COLUMNS パーティショニングは`DATETIME`List パーティショニングのバリエーションです。複数の列をパーティションキーとして使用できます。整数データ型に加えて、文字列、 `DATE`データ型の列もパーティション列として使用できます。

次の表に示すように、次の 12 都市の店舗従業員を 4 つの地域に分割するとします。

    | Region | Cities                         |
    | :----- | ------------------------------ |
    | 1      | LosAngeles,Seattle, Houston    |
    | 2      | Chicago, Columbus, Boston      |
    | 3      | NewYork, LongIsland, Baltimore |
    | 4      | Atlanta, Raleigh, Cincinnati   |

次に示すように、 List COLUMNS パーティショニングを使用してテーブルを作成し、従業員の都市に対応するパーティション内の各行を保存できます。

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

List パーティショニングとは異なり、List COLUMNS パーティショニングでは、列の値を整数に変換するために`COLUMNS()`句の式を使用する必要はありません。

List COLUMNS パーティショニングは、次の例に示すように、 `DATE`番目と`DATETIME`番目の列を使用して実装することもできます。この例では、前の`employees_1`番目のテーブルと同じ名前と列を使用していますが、 `hired`番目の列に基づいてList COLUMNS パーティショニングを使用しています。

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

さらに、 `COLUMNS()`節に複数の列を追加することもできます。例：

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

ハッシュパーティションは、データを一定数のパーティションに均等に分散させるために使用されます。レンジパーティションでは、各パーティションの列値の範囲を指定する必要がありますが、ハッシュパーティションではパーティションの数のみを指定すれば済みます。

ハッシュパーティションテーブルを作成するには、 `CREATE TABLE`文に`PARTITION BY HASH (expr)`句を追加する必要があります。5 `expr`整数を返す式です。この列の型が整数の場合、列名を指定できます。さらに、 `PARTITIONS num`追加する必要がある場合もあります。9 `num` 、テーブルがパーティションに分割されている数を示す正の整数です。

次の操作は、 `store_id`ずつ 4 つのパーティションに分割されたハッシュパーティションテーブルを作成します。

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

`PARTITIONS num`が指定されていない場合、デフォルトのパーティション数は 1 になります。

`expr`に対して整数を返すSQL式を使用することもできます。例えば、採用年度でテーブルをパーティション分割できます。

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

最も効率的なハッシュ関数は、単一のテーブル列に対して動作し、その値が列の値に応じて一貫して増加または減少する関数です。

たとえば、 `date_col`はタイプが`DATE`ある列であり、 `TO_DAYS(date_col)`式の値は`date_col`の値によって変化します。 `YEAR(date_col)`は`TO_DAYS(date_col)`とは異なります。これは、 `date_col`のすべての可能な変更が`YEAR(date_col)`に同等の変更をもたらすとは限らないためです。

対照的に、型が`INT`である列が`int_col`あると仮定します。式`POW(5-int_col,3) + 6`について考えてみましょう。しかし、これは適切なハッシュ関数ではありません`int_col`の値が変化しても、式の結果は比例して変化しないからです。9 `int_col`値の変化は、式の結果に大きな変化をもたらす可能性があります。例えば、 `int_col` 5 から 6 に変化した場合、式の結果の変化は -1 です。しかし、 `int_col` 6 から 7 に変化した場合、結果の変化は -7 になる可能性があります。

結論として、式が`y = cx`に近い形をしているほど、ハッシュ関数としてより適しています。式が非線形であるほど、パーティション間のデータが不均一に分散する傾向があるためです。

理論上は、複数の列値を含む式に対してもプルーニングは可能ですが、どの式が適切かを判断するのは非常に困難で時間がかかります。そのため、複数の列を含むハッシュ式の使用は特に推奨されません。

`PARTITION BY HASH`使用する場合、TiDBは式の結果の絶対値に基づいて、データがどのパーティションに分類されるかを決定します。つまり、パーティション式が`expr`でパーティション数が`num`場合、 `MOD(expr, num)`によってデータが格納されるパーティションが決定されます。9 `t1`次のように定義されていると仮定します。

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

`t1`にデータ行を挿入し、 `col3`の値が &#39;2005-09-15&#39; の場合、この行はパーティション 1 に挿入されます。

    MOD(YEAR('2005-09-01'),4)
    =  MOD(2005,4)
    =  1

### キーパーティショニング {#key-partitioning}

TiDBはv7.0.0以降、キーパーティションをサポートしています。v7.0.0より前のバージョンのTiDBでは、キーパーティションテーブルを作成しようとすると、非パーティションテーブルとして作成され、警告が返されます。

キーパーティショニングとハッシュパーティショニングはどちらも、データを一定数のパーティションに均等に分散できます。ハッシュパーティショニングは指定された整数式または整数列に基づくデータ分散のみをサポートするのに対し、キーパーティショニングは列リストに基づくデータ分散をサポートし、パーティション列は整数型に限定されません。TiDBのキーパーティショニングにおけるハッシュアルゴリズムはMySQLのそれとは異なるため、テーブルデータの分散も異なります。

キーパーティションテーブルを作成するには、 `CREATE TABLE`ステートメントに`PARTITION BY KEY (columnList)`句を追加する必要があります。 `columnList`は、1つ以上の列名を含む列リストです。リスト内の各列のデータ型は、 `BLOB` 、 `JSON` 、 `GEOMETRY`を除く任意の型にすることができます（TiDBは`GEOMETRY`サポートしていないことに注意してください）。さらに、 `PARTITIONS num` （ `num`はテーブルがパーティションに分割されている数を示す正の整数）を追加したり、パーティション名の定義を追加したりする必要がある場合もあります。たとえば、 `(PARTITION p0, PARTITION p1)`を追加すると、テーブルが`p0`と`p1`という2つのパーティションに分割されます。

次の操作は、 `store_id`ずつ 4 つのパーティションに分割されたキーパーティションテーブルを作成します。

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

PARTITION BY KEY(store_id)
PARTITIONS 4;
```

`PARTITIONS num`が指定されていない場合、デフォルトのパーティション数は 1 になります。

VARCHARなどの非整数列に基づいてキーパーティションテーブルを作成することもできます。例えば、 `fname`番目の列でテーブルをパーティション分割できます。

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

PARTITION BY KEY(fname)
PARTITIONS 4;
```

複数の列に基づいてキーパーティションテーブルを作成することもできます。例えば、 `fname`と`store_id`に基づいてテーブルを4つのパーティションに分割できます。

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

PARTITION BY KEY(fname, store_id)
PARTITIONS 4;
```

MySQLと同様に、TiDBは`PARTITION BY KEY`で指定された空のパーティション列リストを持つキーパーティションテーブルの作成をサポートしています。例えば、次の文は、主キー`id`をパーティションキーとしてパーティションテーブルを作成します。

```sql
CREATE TABLE employees (
    id INT NOT NULL PRIMARY KEY,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)

PARTITION BY KEY()
PARTITIONS 4;
```

テーブルに主キーがなく、一意のキーが含まれている場合は、一意のキーがパーティション キーとして使用されます。

```sql
CREATE TABLE k1 (
    id INT NOT NULL,
    name VARCHAR(20),
    UNIQUE KEY (id)
)
PARTITION BY KEY()
PARTITIONS 2;
```

ただし、一意のキー列が`NOT NULL`として定義されていない場合、前のステートメントは失敗します。

#### TiDBが線形ハッシュパーティションを処理する方法 {#how-tidb-handles-linear-hash-partitions}

v6.4.0より前のバージョンでは、TiDBで[MySQL 線形ハッシュ](https://dev.mysql.com/doc/refman/8.0/en/partitioning-linear-hash.html)パーティションのDDL文を実行すると、TiDBは非パーティションテーブルしか作成できませんでした。この場合、TiDBでパーティションテーブルを引き続き使用したい場合は、DDL文を変更する必要があります。

バージョン6.4.0以降、TiDBはMySQL `PARTITION BY LINEAR HASH`構文の解析をサポートしていますが、その中のキーワード`LINEAR`は無視されます。MySQL線形ハッシュパーティションの既存のDDLおよびDML文がある場合は、変更せずにTiDBで実行できます。

-   MySQLの線形ハッシュパーティションの`CREATE`文に対して、TiDBは非線形ハッシュパーティションテーブルを作成します（TiDBには線形ハッシュパーティションテーブルはありません）。パーティション数が2の累乗の場合、TiDBハッシュパーティションテーブルの行はMySQLの線形ハッシュパーティションテーブルと同じように分散されます。それ以外の場合、TiDBでのこれらの行の分散はMySQLとは異なります。これは、非線形パーティションテーブルでは単純な「パーティション数を係数とする」のに対し、線形パーティションテーブルでは「次の2の累乗を係数とし、パーティション数と次の2の累乗の間の値を畳む」ためです。詳細については、 [＃38450](https://github.com/pingcap/tidb/issues/38450)参照してください。

-   MySQL リニア ハッシュ パーティションのその他のすべてのステートメントは、パーティション数が 2 の累乗でない場合、行の分散方法が異なり、 [パーティションの選択](#partition-selection) 、 `TRUNCATE PARTITION` 、 `EXCHANGE PARTITION`で異なる結果になることを除いて、TiDB でも MySQL と同じように動作します。

### TiDBがリニアキーパーティションを処理する方法 {#how-tidb-handles-linear-key-partitions}

TiDB v7.0.0以降、キーパーティショニングのためのMySQL `PARTITION BY LINEAR KEY`構文の解析がサポートされています。ただし、TiDBは`LINEAR`キーワードを無視し、代わりに非線形ハッシュアルゴリズムを使用します。

v7.0.0 より前では、キーパーティションテーブルを作成しようとすると、TiDB はそれを非パーティションテーブルとして作成し、警告を返します。

### TiDBパーティショニングがNULLを処理する方法 {#how-tidb-partitioning-handles-null}

TiDB では、パーティション式の計算結果として`NULL`使用できます。

> **注記：**
>
> `NULL`は整数ではありません。TiDB のパーティショニング実装では、 `ORDER BY`と同様に、 `NULL`他の整数値よりも小さいものとして扱われます。

#### 範囲分割によるNULLの扱い {#handling-of-null-with-range-partitioning}

範囲によってパーティション化されたテーブルに行を挿入し、パーティションを決定するために使用される列の値が`NULL`の場合、この行は最下位のパーティションに挿入されます。

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

    Query OK, 0 rows affected (0.09 sec)

```sql
select * from t1 partition(p0);
```

    +------|--------+
    | c1   | c2     |
    +------|--------+
    | NULL | mothra |
    +------|--------+
    1 row in set (0.00 sec)

```sql
select * from t1 partition(p1);
```

    Empty set (0.00 sec)

```sql
select * from t1 partition(p2);
```

    Empty set (0.00 sec)

`p0`パーティションを削除し、結果を確認します。

```sql
alter table t1 drop partition p0;
```

    Query OK, 0 rows affected (0.08 sec)

```sql
select * from t1;
```

    Empty set (0.00 sec)

#### ハッシュパーティションによるNULLの扱い {#handling-of-null-with-hash-partitioning}

ハッシュでテーブルをパーティション分割する場合、 `NULL`値を処理する方法が異なります。パーティション式の計算結果が`NULL`の場合、 `0`と見なされます。

```sql
CREATE TABLE th (
    c1 INT,
    c2 VARCHAR(20)
)

PARTITION BY HASH(c1)
PARTITIONS 2;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
INSERT INTO th VALUES (NULL, 'mothra'), (0, 'gigan');
```

    Query OK, 2 rows affected (0.04 sec)

```sql
select * from th partition (p0);
```

    +------|--------+
    | c1   | c2     |
    +------|--------+
    | NULL | mothra |
    |    0 | gigan  |
    +------|--------+
    2 rows in set (0.00 sec)

```sql
select * from th partition (p1);
```

    Empty set (0.00 sec)

挿入されたレコード`(NULL, 'mothra')` `(0, 'gigan')`と同じパーティションに分類されることがわかります。

> **注記：**
>
> TiDBのハッシュパーティションにおける`NULL`値は、 [MySQLパーティショニングにおけるNULLの扱い](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html)で説明したのと同じ方法で処理されますが、これはMySQLの実際の動作とは一致していません。言い換えれば、この場合のMySQLの実装は、ドキュメントと一致していません。
>
> この場合、TiDB の実際の動作はこのドキュメントの説明と一致します。

#### キーパーティショニングによるNULLの扱い {#handling-of-null-with-key-partitioning}

キーパーティショニングでは、 `NULL`値の扱い方はハッシュパーティショニングと同じです。パーティショニングフィールドの値が`NULL`の場合、 `0`として扱われます。

## パーティション管理 {#partition-management}

`RANGE` 、 `RANGE COLUMNS` 、 `LIST` 、および`LIST COLUMNS`にパーティション化されたテーブルの場合、次のようにパーティションを管理できます。

-   `ALTER TABLE <table name> ADD PARTITION (<partition specification>)`ステートメントを使用してパーティションを追加します。
-   `ALTER TABLE <table name> DROP PARTITION <list of partitions>`ステートメントを使用してパーティションを削除します。
-   `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>`ステートメントを使用して、指定されたパーティションからすべてのデータを削除します。3 のロジックは`TRUNCATE PARTITION` [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)似ていますが、パーティションを対象としています。
-   `ALTER TABLE <table name> REORGANIZE PARTITION <list of partitions> INTO (<new partition definitions>)`ステートメントを使用して、パーティションを結合、分割、またはその他の変更を行います。

`HASH`および`KEY`パーティション化されたテーブルの場合、次のようにパーティションを管理できます。

-   `ALTER TABLE <table name> COALESCE PARTITION <number of partitions to decrease by>`ステートメントを使用してパーティション数を減らします。この操作では、テーブル全体を新しいパーティション数にオンラインでコピーすることで、パーティションを再編成します。
-   `ALTER TABLE <table name> ADD PARTITION <number of partitions to increase by | (additional partition definitions)>`ステートメントを使用してパーティション数を増やします。この操作では、テーブル全体を新しいパーティション数にオンラインでコピーすることで、パーティションを再編成します。
-   `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>`ステートメントを使用して、指定されたパーティションからすべてのデータを削除します。3 のロジックは`TRUNCATE PARTITION` [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)似ていますが、パーティションを対象としています。

`EXCHANGE PARTITION` 、 `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2`ようなテーブルの名前を変更する場合と同様に、パーティションとパーティションテーブルを交換することによって機能します。

たとえば、 `ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table` `partitioned_table`テーブル`p1`パーティションを`non_partitioned_table`テーブルと交換します。

パーティションに交換するすべての行がパーティション定義と一致していることを確認してください。一致しない場合、ステートメントは失敗します。

TiDBには、 `EXCHANGE PARTITION`影響を与える可能性のある特定の機能がいくつかあります。テーブル構造にそのような機能が含まれている場合は、 `EXCHANGE PARTITION` [MySQLのEXCHANGE PARTITION条件](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html)を満たしていることを確認する必要があります。また、これらの特定の機能がパーティションテーブルと非パーティションテーブルの両方で同じように定義されていることを確認してください。これらの特定の機能には、以下のものが含まれます。

<CustomContent platform="tidb">

-   [SQLの配置ルール](/placement-rules-in-sql.md) : 配置ポリシーは同じです。

</CustomContent>

-   [TiFlash](/tikv-overview.md) : TiFlashレプリカの数は同じです。
-   [クラスター化インデックス](/clustered-indexes.md) : パーティション化されたテーブルとパーティション化されていないテーブルの両方が`CLUSTERED` 、または両方が`NONCLUSTERED`です。

さらに、 `EXCHANGE PARTITION`と他のコンポーネントとの互換性には制限があります。パーティションテーブルと非パーティションテーブルの両方の定義が同じである必要があります。

-   TiFlash: パーティション化されたテーブルとパーティション化されていないテーブルのTiFlashレプリカ定義が異なる場合、 `EXCHANGE PARTITION`操作は実行できません。
-   TiCDC: TiCDCは、パーティションテーブルと非パーティションテーブルの両方に主キーまたは一意キーがある場合、 `EXCHANGE PARTITION`操作を複製します。それ以外の場合、TiCDCは操作を複製しません。
-   TiDB LightningおよびBR: TiDB Lightningを使用したインポート中、またはBRを使用した復元中に`EXCHANGE PARTITION`操作を実行しません。

### 範囲、範囲列、リスト、リスト列のパーティションを管理する {#manage-range-range-columns-list-and-list-columns-partitions}

このセクションでは、次の SQL ステートメントによって作成されたパーティション テーブルを例として使用して、範囲パーティションとリスト パーティションを管理する方法を示します。

```sql
CREATE TABLE members (
    id int,
    fname varchar(255),
    lname varchar(255),
    dob date,
    data json
)
PARTITION BY RANGE (YEAR(dob)) (
 PARTITION pBefore1950 VALUES LESS THAN (1950),
 PARTITION p1950 VALUES LESS THAN (1960),
 PARTITION p1960 VALUES LESS THAN (1970),
 PARTITION p1970 VALUES LESS THAN (1980),
 PARTITION p1980 VALUES LESS THAN (1990),
 PARTITION p1990 VALUES LESS THAN (2000));

CREATE TABLE member_level (
 id int,
 level int,
 achievements json
)
PARTITION BY LIST (level) (
 PARTITION l1 VALUES IN (1),
 PARTITION l2 VALUES IN (2),
 PARTITION l3 VALUES IN (3),
 PARTITION l4 VALUES IN (4),
 PARTITION l5 VALUES IN (5));
```

#### パーティションを削除する {#drop-partitions}

```sql
ALTER TABLE members DROP PARTITION p1990;

ALTER TABLE member_level DROP PARTITION l5;
```

#### パーティションを切り捨てる {#truncate-partitions}

```sql
ALTER TABLE members TRUNCATE PARTITION p1980;

ALTER TABLE member_level TRUNCATE PARTITION l4;
```

#### パーティションを追加する {#add-partitions}

```sql
ALTER TABLE members ADD PARTITION (PARTITION `p1990to2010` VALUES LESS THAN (2010));

ALTER TABLE member_level ADD PARTITION (PARTITION l5_6 VALUES IN (5,6));
```

範囲パーティションテーブルの場合、 `ADD PARTITION`既存の最後のパーティションの後に新しいパーティションを追加します。既存のパーティションと比較して、 `VALUES LESS THAN`で定義された新しいパーティションの値は大きくなければなりません。そうでない場合、エラーが報告されます。

```sql
ALTER TABLE members ADD PARTITION (PARTITION p1990 VALUES LESS THAN (2000));
```

    ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

#### パーティションを再編成する {#reorganize-partitions}

パーティションを分割します。

```sql
ALTER TABLE members REORGANIZE PARTITION `p1990to2010` INTO
(PARTITION p1990 VALUES LESS THAN (2000),
 PARTITION p2000 VALUES LESS THAN (2010),
 PARTITION p2010 VALUES LESS THAN (2020),
 PARTITION p2020 VALUES LESS THAN (2030),
 PARTITION pMax VALUES LESS THAN (MAXVALUE));

ALTER TABLE member_level REORGANIZE PARTITION l5_6 INTO
(PARTITION l5 VALUES IN (5),
 PARTITION l6 VALUES IN (6));
```

パーティションを結合する:

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1950,p1950 INTO (PARTITION pBefore1960 VALUES LESS THAN (1960));

ALTER TABLE member_level REORGANIZE PARTITION l1,l2 INTO (PARTITION l1_2 VALUES IN (1,2));
```

パーティション スキームの定義を変更します。

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1960,p1960,p1970,p1980,p1990,p2000,p2010,p2020,pMax INTO
(PARTITION p1800 VALUES LESS THAN (1900),
 PARTITION p1900 VALUES LESS THAN (2000),
 PARTITION p2000 VALUES LESS THAN (2100));

ALTER TABLE member_level REORGANIZE PARTITION l1_2,l3,l4,l5,l6 INTO
(PARTITION lOdd VALUES IN (1,3,5),
 PARTITION lEven VALUES IN (2,4,6));
```

パーティションを再編成するときは、次の重要な点に注意する必要があります。

-   パーティションの再編成 (パーティションの結合や分割を含む) により、リストされたパーティションを新しいパーティション定義セットに変更できますが、パーティションのタイプを変更することはできません (たとえば、リスト タイプを範囲タイプに変更したり、範囲 COLUMNS タイプを範囲タイプに変更したりすることはできません)。

-   範囲パーティション テーブルの場合、テーブル内の隣接するパーティションのみを再編成できます。

    ```sql
    ALTER TABLE members REORGANIZE PARTITION p1800,p2000 INTO (PARTITION p2000 VALUES LESS THAN (2100));
    ```

        ERROR 8200 (HY000): Unsupported REORGANIZE PARTITION of RANGE; not adjacent partitions

-   レンジパーティションテーブルの場合、範囲の終了位置を変更するには、 `VALUES LESS THAN`で定義した新しい終了位置が最後のパーティションの既存の行をカバーする必要があります。そうでない場合、既存の行が収まらなくなり、エラーが報告されます。

    ```sql
    INSERT INTO members VALUES (313, "John", "Doe", "2022-11-22", NULL);
    ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2050)); -- This statement will work as expected, because 2050 covers the existing rows.
    ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2020)); -- This statement will fail with an error, because 2022 does not fit in the new range.
    ```

        ERROR 1526 (HY000): Table has no partition for value 2022

-   リストパーティションテーブルの場合、パーティションに定義された値のセットを変更するには、新しい定義がそのパーティション内の既存の値をカバーする必要があります。そうでない場合は、エラーが報告されます。

    ```sql
    INSERT INTO member_level (id, level) values (313, 6);
    ALTER TABLE member_level REORGANIZE PARTITION lEven INTO (PARTITION lEven VALUES IN (2,4));
    ```

        ERROR 1526 (HY000): Table has no partition for value 6

-   パーティションが再編成されると、対応するパーティションの統計情報が古くなるため、以下の警告が表示されます。この場合、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを使用して統計情報を更新できます。

    ```sql
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Level   | Code | Message                                                                                                                                                |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

### ハッシュとキーのパーティションを管理する {#manage-hash-and-key-partitions}

このセクションでは、以下のSQL文で作成されたパーティションテーブルを例に、ハッシュパーティションの管理方法を説明します。キーパーティションの場合も、同様の管理文を使用できます。

```sql
CREATE TABLE example (
  id INT PRIMARY KEY,
  data VARCHAR(1024)
)
PARTITION BY HASH(id)
PARTITIONS 2;
```

#### パーティションの数を増やす {#increase-the-number-of-partitions}

`example`テーブルのパーティション数を 1 つ増やします (2 から 3 へ)。

```sql
ALTER TABLE example ADD PARTITION PARTITIONS 1;
```

パーティション定義を追加することで、パーティションオプションを指定することもできます。例えば、次のステートメントを使用してパーティション数を3から5に増やし、新しく追加したパーティションの名前を`pExample4`と`pExample5`に指定できます。

```sql
ALTER TABLE example ADD PARTITION
(PARTITION pExample4 COMMENT = 'not p3, but pExample4 instead',
 PARTITION pExample5 COMMENT = 'not p4, but pExample5 instead');
```

#### パーティションの数を減らす {#decrease-the-number-of-partitions}

範囲List パーティショニングとは異なり、ハッシュパーティション分割やキーパーティション分割では`DROP PARTITION`サポートされていませんが、 `COALESCE PARTITION`を使用してパーティション数を減らしたり、 `TRUNCATE PARTITION`を使用して特定のパーティションからすべてのデータを削除したりすることができます。

`example`テーブルのパーティション数を 1 つ減らします (5 から 4 に)。

```sql
ALTER TABLE example COALESCE PARTITION 1;
```

> **注記：**
>
> ハッシュまたはキーでパーティション化されたテーブルのパーティション数を変更するプロセスでは、すべてのデータを新しいパーティション数にコピーすることでパーティションが再編成されます。そのため、ハッシュまたはキーでパーティションパーティションテーブルのパーティション数を変更すると、統計情報が古くなっているという次の警告が表示されます。この場合、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを使用して統計情報を更新できます。
>
> ```sql
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Level   | Code | Message                                                                                                                                                |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> 1 row in set (0.00 sec)
> ```

`example`テーブルが現在どのように構成されているかをよりよく理解するために、次のように`example`テーブルを再作成するために使用される SQL ステートメントを示します。

```sql
SHOW CREATE TABLE\G
```

    *************************** 1. row ***************************
           Table: example
    Create Table: CREATE TABLE `example` (
      `id` int NOT NULL,
      `data` varchar(1024) DEFAULT NULL,
      PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
    PARTITION BY HASH (`id`)
    (PARTITION `p0`,
     PARTITION `p1`,
     PARTITION `p2`,
     PARTITION `pExample4` COMMENT 'not p3, but pExample4 instead')
    1 row in set (0.01 sec)

#### パーティションを切り捨てる {#truncate-partitions}

パーティションからすべてのデータを削除します。

```sql
ALTER TABLE example TRUNCATE PARTITION p0;
```

    Query OK, 0 rows affected (0.03 sec)

### パーティションテーブルを非パーティションテーブルに変換する {#convert-a-partitioned-table-to-a-non-partitioned-table}

パーティションテーブルを非パーティションテーブルに変換するには、次のステートメントを使用します。このステートメントは、パーティションを削除し、テーブルのすべての行をコピーし、テーブルのインデックスをオンラインで再作成します。

```sql
ALTER TABLE <table_name> REMOVE PARTITIONING
```

たとえば、 `members`パーティションテーブルを非パーティションテーブルに変換するには、次のステートメントを実行します。

```sql
ALTER TABLE members REMOVE PARTITIONING
```

### 既存のテーブルをパーティション分割する {#partition-an-existing-table}

既存のパーティションテーブルをパーティション化したり、既存のパーティションテーブルのパーティション タイプを変更したりするには、次のステートメントを使用できます。このステートメントは、すべての行をコピーし、新しいパーティション定義に従ってオンラインでインデックスを再作成します。

```sql
ALTER TABLE <table_name> PARTITION BY <new partition type and definitions> [UPDATE INDEXES (<index name> {GLOBAL|LOCAL}[ , <index name> {GLOBAL|LOCAL}...])]
```

例:

既存の`members`テーブルを 10 個のパーティションを持つ HASHパーティションテーブルに変換するには、次のステートメントを実行します。

```sql
ALTER TABLE members PARTITION BY HASH(id) PARTITIONS 10;
```

既存の`member_level`テーブルを RANGEパーティションテーブルに変換するには、次のステートメントを実行します。

```sql
ALTER TABLE member_level PARTITION BY RANGE(level)
(PARTITION pLow VALUES LESS THAN (1),
 PARTITION pMid VALUES LESS THAN (3),
 PARTITION pHigh VALUES LESS THAN (7)
 PARTITION pMax VALUES LESS THAN (MAXVALUE));
```

パーティション化パーティションテーブルをパーティション化する場合、またはすでにパーティションテーブルを再パーティション化する場合は、必要に応じてインデックスを[グローバルインデックス](/global-indexes.md)またはローカル インデックスに更新できます。

```sql
CREATE TABLE t1 (
    col1 INT NOT NULL,
    col2 DATE NOT NULL,
    col3 INT NOT NULL,
    col4 INT NOT NULL,
    UNIQUE KEY uidx12(col1, col2),
    UNIQUE KEY uidx3(col3)
);

ALTER TABLE t1 PARTITION BY HASH (col1) PARTITIONS 3 UPDATE INDEXES (uidx12 LOCAL, uidx3 GLOBAL);
```

## パーティションプルーニング {#partition-pruning}

[パーティションプルーニング](/partition-pruning.md)は、一致しないパーティションをスキャンしないという非常に単純な考えに基づいた最適化です。

パーティションテーブル`t1`を作成すると仮定します。

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

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

結果がパーティション`p1`または`p2`のいずれかに該当することは明らかです。つまり、一致する行をパーティション`p1`とパーティション`p2`で検索するだけで済みます。不要なパーティションを除外することを「プルーニング」と呼びます。オプティマイザがパーティションの一部をプルーニングできれば、パーティションテーブルでのクエリ実行は、パーティションテーブルでのクエリ実行よりもはるかに高速になります。

オプティマイザーは、次の 2 つのシナリオで`WHERE`条件を通じてパーティションを整理できます。

-   パーティション列 = 定数
-   パーティション列 IN (定数1、定数2、...、定数N)

現在、パーティション プルーニングは`LIKE`条件では機能しません。

### パーティションプルーニングが効果を発揮するいくつかのケース {#some-cases-for-partition-pruning-to-take-effect}

1.  パーティション プルーニングでは、パーティションテーブル上のクエリ条件が使用されるため、プランナーの最適化ルールに従ってクエリ条件をパーティションテーブルにプッシュダウンできない場合、このクエリにはパーティション プルーニングは適用されません。

    例えば：

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    create table t2 (x int);
    ```

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x where t2.x > 5;
    ```

    このクエリでは、残された結合が内部結合に変換され、 `t1.x > 5` `t1.x = t2.x`と`t2.x > 5`から導出されるため、パーティション プルーニングに使用できるようになり、パーティション`p1`のみが残ります。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    このクエリでは、 `t2.x > 5` `t1`パーティションテーブルにプッシュダウンできないため、このクエリではパーティション プルーニングは有効になりません。

2.  パーティション プルーニングはプランの最適化フェーズで実行されるため、実行フェーズまでフィルター条件が不明な場合には適用されません。

    例えば：

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    ```

    ```sql
    explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
    ```

    このクエリは、 `t2`から行を読み取り、その結果を`t1`のサブクエリに使用します。理論的には、サブクエリ内の`t1.x > val`式によってパーティションプルーニングの効果が期待できますが、これは実行フェーズで行われるため、ここでは効果がありません。

3.  現在の実装の制限により、クエリ条件を TiKV にプッシュダウンできない場合は、パーティション プルーニングで使用できません。

    `fn(col)`式を例に挙げましょう。TiKVコプロセッサがこの`fn`機能をサポートしている場合、プラン最適化フェーズで述語プッシュダウンルールに従って`fn(col)`がリーフノード（つまりパーティションテーブル）にプッシュダウンされ、パーティションプルーニングで利用できるようになります。

    TiKVコプロセッサがこの`fn`機能をサポートしていない場合、 `fn(col)`リーフノードにプッシュダウンされず、リーフノードの`Selection`番目のノードになります。現在のパーティションプルーニング実装では、この種のプランツリーはサポートされていません。

4.  ハッシュおよびキー パーティション タイプの場合、パーティション プルーニングでサポートされるクエリは、等しい条件のみです。

5.  レンジパーティションの場合、パーティションプルーニングを有効にするには、パーティション式が`col`または`fn(col)`の形式であり、クエリ条件が`>` 、 `<` 、 `=` 、 `>=` 、 `<=`のいずれかである必要があります。パーティション式が`fn(col)`の形式である場合、 `fn`関数は単調である必要があります。

    関数`fn`が単調であれば、任意の`x`と`y`に対して、また`x > y`であれば`fn(x) > fn(y)`に対して単調です。したがって、この`fn`関数は厳密に単調であると言えます。任意の`x`と`y`に対して、また`x > y`であれば`fn(x) >= fn(y)`に対して単調です。この場合、 `fn`も「単調」と言えるでしょう。理論的には、すべての単調関数はパーティション・プルーニングによってサポートされます。

    現在、TiDB のパーティション プルーニングは、次の単調な関数のみをサポートしています。

    -   [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    -   [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)
    -   [`EXTRACT(&#x3C;time unit> FROM &#x3C;DATETIME/DATE/TIME column>)`](/functions-and-operators/date-and-time-functions.md) 。2 `DATE`および`DATETIME`列の場合、 `YEAR`および`YEAR_MONTH`時間単位は単調関数とみなされます。10 `TIME`の場合、 `HOUR` 、および`HOUR_SECOND` `HOUR_MICROSECOND`単調関数とみなされます。パーティションプルーニングでは`HOUR_MINUTE` `EXTRACT`では`WEEK`時間単位としてサポートされていないことに注意してください。

    たとえば、パーティション式は単純な列です。

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    または、パーティション式は`fn(col)` `fn`が`to_days`である形式になります。

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    例外として、パーティション式が`floor(unix_timestamp())`場合、TiDBはケースバイケースで最適化を行うため、パーティションプルーニングによってサポートされます。

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where ts > '2020-04-18 02:00:42.123';
    ```

## パーティションの選択 {#partition-selection}

`SELECT`ステートメントは、 `PARTITION`オプションを使用して実装されるパーティション選択をサポートします。

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

```sql
SELECT * FROM employees PARTITION (p1);
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

複数のパーティションの行を取得したい場合は、パーティション名をカンマで区切ったリストを使用できます。例えば、 `SELECT * FROM employees PARTITION (p1, p2)`指定すると、パーティション`p1`と`p2`のすべての行が返されます。

パーティション選択を使用する場合でも、 `WHERE`条件と`ORDER BY`や`LIMIT`などのオプションを使用できます。また、 `HAVING`や`GROUP BY`などの集計オプションも使用できます。

```sql
SELECT * FROM employees PARTITION (p0, p2)
    WHERE lname LIKE 'S%';
```

    +----|-------|-------|----------|---------------+
    | id | fname | lname | store_id | department_id |
    +----|-------|-------|----------|---------------+
    |  4 | Jim   | Smith |        2 |             4 |
    | 11 | Jill  | Stone |        1 |             4 |
    +----|-------|-------|----------|---------------+
    2 rows in set (0.00 sec)

```sql
SELECT id, CONCAT(fname, ' ', lname) AS name
    FROM employees PARTITION (p0) ORDER BY lname;
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

```sql
SELECT store_id, COUNT(department_id) AS c
    FROM employees PARTITION (p1,p2,p3)
    GROUP BY store_id HAVING c > 4;
```

    +---|----------+
    | c | store_id |
    +---|----------+
    | 5 |        2 |
    | 5 |        3 |
    +---|----------+
    2 rows in set (0.00 sec)

パーティションの選択は、レンジパーティションとハッシュパーティションを含むすべてのタイプのテーブルパーティションでサポートされています。ハッシュパーティションの場合、パーティション名が指定されていない場合は、 `p0` 、 `p1` 、 `p2` 、...、または`pN-1`自動的にパーティション名として使用されます。

`SELECT` in `INSERT ... SELECT`ではパーティション選択も使用できます。

## パーティションに関する制限と制約 {#restrictions-and-limitations-on-partitions}

このセクションでは、TiDB のパーティション テーブルに関するいくつかの制限と制約について説明します。

-   [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)ステートメントを使用してパーティション テーブルの列タイプを変更することはサポートされていません。
-   [`ALTER TABLE ... CACHE`](/cached-tables.md)ステートメントを使用してパーティション テーブルをキャッシュ テーブルに設定することはサポートされていません。
-   TiDB の[一時テーブル](/temporary-tables.md)はパーティション テーブルと互換性が**ありません**。
-   パーティションテーブルに[外部キー](/foreign-key.md)を作成することはサポートされていません。
-   パーティション テーブル上のインデックスは順番に読み取ることができないため、ヒント[`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)はパーティション テーブルとその関連インデックスでは機能しません。

### パーティションキー、主キー、一意キー {#partitioning-keys-primary-keys-and-unique-keys}

このセクションでは、パーティションキーと主キーおよび一意キーの関係について説明します。この関係を規定するルールは次のとおりです。パーティションテーブル上のすべての一意キー（主キーを含む）は、テーブルのパーティション式のすべての列を使用する必要があります。これは、主キーが定義上一意キーでもあるためです。

> **注記：**
>
> [グローバルインデックス](/global-indexes.md)使用する場合、このルールは無視できます。

たとえば、次のテーブル作成ステートメントは無効です。

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

いずれの場合も、提案されたテーブルには、パーティション式で使用されるすべての列が含まれていない一意のキーが少なくとも 1 つあります。

有効なステートメントは次のとおりです。

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

次の例ではエラーが表示されます。

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

    ERROR 8264 (HY000): Global Index is needed for index 'col1', since the unique index is not including all partitioning columns, and GLOBAL is not given as IndexOption

`CREATE TABLE`文は、提案されたパーティションキーに`col1`と`col3`両方が含まれているものの、どちらの列もテーブル上の両方の一意キーに含まれていないため失敗します。以下の変更を加えると、 `CREATE TABLE`文は有効になります。

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

次のテーブルは、両方の一意のキーに属する列をパーティション キーに含めることができないため、まったくパーティション化できません。

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

上記の例では、パーティション式で参照されているすべての列が主キーに含まれていません。主キーに不足している列を追加すると、 `CREATE TABLE`文は有効になります。

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

テーブルに一意のキーも主キーもない場合は、この制限は適用されません。

DDL文を使用してテーブルを変更する場合、ユニークインデックスを追加する際にはこの制限も考慮する必要があります。例えば、以下のようにパーティションテーブルを作成するとします。

```sql
CREATE TABLE t_no_pk (c1 INT, c2 INT)
    PARTITION BY RANGE(c1) (
        PARTITION p0 VALUES LESS THAN (10),
        PARTITION p1 VALUES LESS THAN (20),
        PARTITION p2 VALUES LESS THAN (30),
        PARTITION p3 VALUES LESS THAN (40)
    );
```

    Query OK, 0 rows affected (0.12 sec)

`ALTER TABLE`ステートメントを使用することで、一意でないインデックスを追加できます。ただし、一意のインデックスを追加する場合は、 `c1`列目が一意のインデックスに含まれている必要があります。

パーティションテーブルを使用する場合、プレフィックス インデックスを一意の属性として指定することはできません。

```sql
CREATE TABLE t (a varchar(20), b blob,
    UNIQUE INDEX (a(5)))
    PARTITION by range columns (a) (
    PARTITION p0 values less than ('aaaaa'),
    PARTITION p1 values less than ('bbbbb'),
    PARTITION p2 values less than ('ccccc'));
```

```sql
ERROR 8264 (HY000): Global Index is needed for index 'a', since the unique index is not including all partitioning columns, and GLOBAL is not given as IndexOption
```

### グローバルインデックス {#global-indexes}

グローバルインデックスの詳細については、 [グローバルインデックス](/global-indexes.md)参照してください。

### 関数に関するパーティションの制限 {#partitioning-limitations-relating-to-functions}

パーティション式では、次のリストに示す関数のみが許可されます。

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

### MySQLとの互換性 {#compatibility-with-mysql}

現在、TiDBはレンジパーティショニング、レンジ列パーティショニング、List パーティショニング、List COLUMNS パーティショニング、ハッシュパーティショニング、キーパーティショニングをサポートしています。MySQLで利用可能なその他のパーティショニングタイプは、TiDBではまだサポートされていません。

サポートされていないパーティション タイプの場合、TiDB でテーブルを作成すると、パーティション情報は無視され、警告が報告されて通常の形式でテーブルが作成されます。

`LOAD DATA`構文は現在 TiDB でのパーティション選択をサポートしていません。

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

通常の`LOAD DATA`操作がサポートされています。

```sql
load local data infile "xxx" into t ...
```

しかし、 `Load Data`パーティション選択をサポートしていません。

```sql
load local data infile "xxx" into t partition (p1)...
```

パーティションテーブルの場合、 `select * from t`によって返される結果はパーティション間で順序付けされません。これは、パーティション間では順序付けされますが、パーティション内では順序付けされない MySQL の結果とは異なります。

```sql
create table t (id int, val int) partition by range (id) (
    partition p0 values less than (3),
    partition p1 values less than (7),
    partition p2 values less than (11));
```

    Query OK, 0 rows affected (0.10 sec)

```sql
insert into t values (1, 2), (3, 4),(5, 6),(7,8),(9,10);
```

    Query OK, 5 rows affected (0.01 sec)
    Records: 5  Duplicates: 0  Warnings: 0

TiDB は毎回異なる結果を返します。たとえば、次のようになります。

```sql
select * from t;
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

MySQL で返された結果:

```sql
select * from t;
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

## 動的プルーニングモード {#dynamic-pruning-mode}

TiDBは、パーティション化されたテーブルにモード`dynamic`またはモード`static`でアクセスします。バージョン6.3.0以降、デフォルトでモード`dynamic`が使用されます。ただし、動的パーティション分割は、テーブルレベルの統計情報（グローバル統計情報）が完全に収集された後にのみ有効になります。グローバル統計情報の収集が完了する前にプルーニングモード`dynamic`を有効にすると、TiDBはグローバル統計情報が完全に収集されるまでモード`static`のままになります。グローバル統計情報の詳細については、 [動的プルーニングモードでパーティションテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

手動ANALYZEと通常のクエリでは、セッションレベル`tidb_partition_prune_mode`設定が使用されます。バックグラウンドで実行される`auto-analyze`操作では、グローバル設定の`tidb_partition_prune_mode`が使用されます。

モード`static`では、パーティションテーブルはパーティションレベルの統計を使用します。モード`dynamic`では、パーティションテーブルはテーブルレベルのグローバル統計を使用します。

モード`static`からモード`dynamic`に切り替える際は、統計情報を手動で確認・収集する必要があります。これは、モード`dynamic`への切り替え後、パーティションテーブルにはパーティションレベルの統計情報しかなく、テーブルレベルの統計情報は含まれないためです。グローバル統計情報は、次のモード`auto-analyze`操作時にのみ収集されます。

```sql
set session tidb_partition_prune_mode = 'dynamic';
show stats_meta where table_name like "t";
```

    +---------+------------+----------------+---------------------+--------------+-----------+
    | Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
    +---------+------------+----------------+---------------------+--------------+-----------+
    | test    | t          | p0             | 2022-05-27 20:23:34 |            1 |         2 |
    | test    | t          | p1             | 2022-05-27 20:23:34 |            2 |         4 |
    | test    | t          | p2             | 2022-05-27 20:23:34 |            2 |         4 |
    +---------+------------+----------------+---------------------+--------------+-----------+
    3 rows in set (0.01 sec)

グローバル`dynamic`プルーニング モードを有効にした後、SQL ステートメントで使用される統計が正しいことを確認するには、テーブルまたはテーブルのパーティションで`analyze`手動でトリガーして、グローバル統計を取得する必要があります。

```sql
analyze table t partition p1;
show stats_meta where table_name like "t";
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

`analyze`プロセス中に次の警告が表示された場合、パーティション統計に矛盾があるため、これらのパーティションまたはテーブル全体の統計を再度収集する必要があります。

    | Warning | 8244 | Build table: `t` column: `a` global-level stats failed due to missing partition-level column stats, please run analyze table to refresh columns of all partitions

スクリプトを使用して、すべてのパーティションテーブルの統計情報を更新することもできます。詳細については、 [動的プルーニングモードでパーティションテーブルの統計を更新する](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。

テーブル レベルの統計が準備できたら、すべての SQL 文と`auto-analyze`操作に有効なグローバル動的プルーニング モードを有効にできます。

```sql
set global tidb_partition_prune_mode = dynamic
```

`static`モードでは、TiDB は複数の演算子を用いて各パーティションに個別にアクセスし、その結果を`Union`を用いてマージします。次の例は、TiDB が`Union`を用いて対応する 2 つのパーティションの結果をマージする単純な読み取り操作です。

```sql
mysql> create table t1(id int, age int, key(id)) partition by range(id) (
        partition p0 values less than (100),
        partition p1 values less than (200),
        partition p2 values less than (300),
        partition p3 values less than (400));
Query OK, 0 rows affected (0.01 sec)

mysql> explain select * from t1 where id < 150;
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

`dynamic`モードでは、各演算子が複数のパーティションへの直接アクセスをサポートするため、TiDB は`Union`使用しなくなります。

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

上記のクエリ結果から、パーティション プルーニングは引き続き有効であり、実行プランの`Union`演算子は消え、実行プランは`p0`と`p1`のみにアクセスすることがわかります。

`dynamic`モードでは、実行計画がよりシンプルで明確になります。Union演算を省略することで実行効率が向上し、Union同時実行の問題を回避できます。さらに、 `dynamic`モードでは、 `static`モードでは使用できないIndexJoinを使用した実行計画も使用できます。（以下の例を参照）

**例 1** : 次の例では、IndexJoin を使用した実行プランを使用して、クエリが`static`モードで実行されます。

```sql
mysql> create table t1 (id int, age int, key(id)) partition by range(id)
    (partition p0 values less than (100),
     partition p1 values less than (200),
     partition p2 values less than (300),
     partition p3 values less than (400));
Query OK, 0 rows affected (0,08 sec)

mysql> create table t2 (id int, code int);
Query OK, 0 rows affected (0.01 sec)

mysql> set @@tidb_partition_prune_mode = 'static';
Query OK, 0 rows affected, 1 warning (0.00 sec)

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

例 1 から、ヒント`TIDB_INLJ`を使用しても、パーティションテーブルに対するクエリでは IndexJoin を使用した実行プランを選択できないことがわかります。

**例 2** : 次の例では、IndexJoin を使用した実行プランを使用して、クエリが`dynamic`モードで実行されます。

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

例 2 から、 `dynamic`モードでは、クエリを実行するときに IndexJoin を使用した実行プランが選択されることがわかります。

現在、 `static`プルーニング モードでは、準備済みステートメントと非準備済みステートメントの両方のプラン キャッシュはサポートされていません。

### 動的プルーニングモードでパーティションテーブルの統計を更新する {#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

1.  すべてのパーティション化されたテーブルを見つけます。

    ```sql
    SELECT DISTINCT CONCAT(TABLE_SCHEMA,'.', TABLE_NAME)
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA', 'mysql', 'sys', 'PERFORMANCE_SCHEMA', 'METRICS_SCHEMA');
    ```

        +-------------------------------------+
        | concat(TABLE_SCHEMA,'.',TABLE_NAME) |
        +-------------------------------------+
        | test.t                              |
        +-------------------------------------+
        1 row in set (0.02 sec)

2.  すべてのパーティション テーブルの統計を更新するためのステートメントを生成します。

    ```sql
    SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;')
        FROM information_schema.PARTITIONS
        WHERE TIDB_PARTITION_ID IS NOT NULL
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');
    ```

        +----------------------------------------------------------------------+
        | concat('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') |
        +----------------------------------------------------------------------+
        | ANALYZE TABLE test.t ALL COLUMNS;                                    |
        +----------------------------------------------------------------------+
        1 row in set (0.01 sec)

    `ALL COLUMNS`必要な列に変更できます。

3.  バッチ更新ステートメントをファイルにエクスポートします。

    ```shell
    mysql --host xxxx --port xxxx -u root -p -e "SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') \
        FROM information_schema.PARTITIONS \
        WHERE TIDB_PARTITION_ID IS NOT NULL \
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');" | tee gatherGlobalStats.sql
    ```

4.  バッチ更新を実行します。

    `source`コマンドを実行する前に SQL ステートメントを処理します。

        sed -i "" '1d' gatherGlobalStats.sql --- mac
        sed -i '1d' gatherGlobalStats.sql --- linux

    ```sql
    SET session tidb_partition_prune_mode = dynamic;
    source gatherGlobalStats.sql
    ```
