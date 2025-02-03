---
title: Partitioning
summary: TiDB でパーティション分割を使用する方法を学習します。
---

# パーティショニング {#partitioning}

このドキュメントでは、TiDB のパーティショニングの実装について説明します。

## パーティションタイプ {#partitioning-types}

このセクションでは、TiDB のパーティションの種類について説明します。現在、TiDB は[範囲分割](#range-partitioning) 、 [範囲列パーティション分割](#range-columns-partitioning) 、 [List パーティショニング](#list-partitioning) 、 [List COLUMNS パーティショニング](#list-columns-partitioning) 、 [ハッシュパーティショニング](#hash-partitioning) 、および[キーの分割](#key-partitioning)をサポートしています。

-   範囲パーティション分割、範囲列パーティション分割、List パーティショニング、およびList COLUMNS パーティショニングは、アプリケーションでの大量の削除によって発生するパフォーマンスの問題を解決し、パーティションの迅速な削除をサポートするために使用されます。
-   ハッシュ パーティション分割とキー パーティション分割は、書き込み回数が多いシナリオでデータを分散するために使用されます。ハッシュ パーティション分割と比較して、キー パーティション分割は、複数の列のデータの分散と非整数列によるパーティション分割をサポートします。

### 範囲分割 {#range-partitioning}

テーブルが範囲によってパーティション化されている場合、各パーティションには、パーティション化式の値が指定された範囲内にある行が含まれます。範囲は連続している必要がありますが、重複してはなりません。これは`VALUES LESS THAN`使用して定義できます。

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

必要に応じて、さまざまな方法で範囲別にテーブルをパーティション分割できます。たとえば、 `store_id`列を使用してパーティション分割できます。

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

このパーティション スキームでは、 `store_id`が 1 から 5 までの従業員に対応するすべての行が`p0`パーティションに格納され、 `store_id`が 6 から 10 までの従業員に対応するすべての行が`p1`パーティションに格納されます。範囲パーティション分割では、パーティションを最小から最大の順に並べる必要があります。

`(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`のデータ行を挿入すると、パーティション`p2`に分類されます。ただし、 `store_id`が 20 より大きいレコードを挿入すると、TiDB はこのレコードをどのパーティションに挿入すればよいか分からないため、エラーが報告されます。この場合、テーブルを作成するときに`MAXVALUE`使用できます。

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

`MAXVALUE` 、他のすべての整数値よりも大きい整数値を表します。これで、 `store_id`が 16 (定義されている最大値) 以上であるすべてのレコードが`p3`パーティションに格納されます。

従業員のジョブ コード ( `job_code`列の値) でテーブルをパーティション化することもできます。2 桁のジョブ コードは一般従業員、3 桁のコードはオフィスおよび顧客サポート担当者、4 桁のコードは管理職を表すものとします。次のようにパーティションテーブルを作成できます。

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

この例では、正社員に関連するすべての行は`p0`パーティションに格納され、オフィスおよび顧客サポート担当者はすべて`p1`パーティションに格納され、管理職はすべて`p2`パーティションに格納されます。

テーブルを`store_id`ずつ分割するだけでなく、日付でテーブルをパーティション分割することもできます。たとえば、従業員の退職年でパーティション分割できます。

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

範囲パーティション分割では、 `timestamp`列の値に基づいてパーティション分割し、 `unix_timestamp()`関数を使用できます。次に例を示します。

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

-   古いデータを削除したいとします。前の例の`employees`テーブルを使用すると、 `ALTER TABLE employees DROP PARTITION p0;`使用するだけで、1991 年以前にこの会社を退職した従業員のすべてのレコードを削除できます。 `DELETE FROM employees WHERE YEAR(separated) <= 1990;`操作を実行するよりも高速です。
-   時刻または日付の値を含む列、または他の系列から発生した値を含む列を使用します。
-   パーティション分割に使用される列に対してクエリを頻繁に実行する必要があります。たとえば、 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;`ようなクエリを実行すると、他のパーティションは`WHERE`条件に一致しないため、 TiDB は`p2`パーティションのデータのみをスキャンする必要があることをすぐに認識できます。

### 範囲列パーティション分割 {#range-columns-partitioning}

範囲 COLUMNS パーティション分割は、範囲 パーティション分割のバリエーションです。1 つ以上の列をパーティション キーとして使用できます。パーティション列のデータ型は、整数、文字列 ( `CHAR`または`VARCHAR` )、 `DATE` 、および`DATETIME`です。非 COLUMNS パーティション分割などの式はサポートされていません。

範囲パーティション分割と同様に、範囲列パーティション分割でもパーティション範囲は厳密に増加する必要があります。次の例のパーティション定義はサポートされていません。

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

上記の SQL 文は、範囲`[ ('', ''), ('G', '2023-01-01 00:00:00') )` 、 `[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 、 `[ ('G', '2024-01-01 00:00:00'), ('M', '2023-01-01 00:00:00') )` 、 `[ ('M', '2023-01-01 00:00:00'), ('M', '2024-01-01 00:00:00') )` 、 `[ ('M', '2024-01-01 00:00:00'), ('S', '2023-01-01 00:00:00') )` 、および`[ ('S', '2023-01-01 00:00:00'), ('S', '2024-01-01 00:00:00') )`でデータを年と名前でパーティション分割します。これにより、 `name`と`valid_until`列の両方でパーティション プルーニングのメリットを享受しながら、無効なデータを簡単に削除できます。この例では、 `[,)`左閉じ、右開きの範囲を示します。たとえば、 `[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 、名前が`'G'`で、年に`2023-01-01 00:00:00`含まれ、 `2023-01-01 00:00:00`より大きく`2024-01-01 00:00:00`より小さいデータの範囲を示します。 `(G, 2024-01-01 00:00:00)`含まれません。

### 範囲INTERVALパーティション分割 {#range-interval-partitioning}

範囲 INTERVAL パーティションは範囲パーティションの拡張であり、指定した間隔のパーティションを簡単に作成できます。v6.3.0 以降、TiDB では INTERVAL パーティションが構文糖として導入されています。

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

範囲 INTERVAL パーティション分割は[範囲列](#range-columns-partitioning)パーティション分割でも機能します。

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

次のテーブルが作成されます:

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

オプションのパラメータ`NULL PARTITION`は、定義が`PARTITION P_NULL VALUES LESS THAN (<minimum value of the column type>)`のパーティションを作成します。これは、パーティション式が`NULL`に評価される場合にのみ一致します。 `NULL`他のどの値よりも小さいと見なされることを説明している[範囲分割による NULL の扱い](#handling-of-null-with-range-partitioning)を参照してください。

オプションパラメータ`MAXVALUE PARTITION`は、最後のパーティションを`PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`として作成します。

#### ALTER INTERVAL パーティションテーブル {#alter-interval-partitioned-tables}

INTERVAL パーティション化では、パーティションの追加と削除のためのより簡単な構文も追加されます。

次のステートメントは、最初のパーティションを変更します。指定された式より小さい値を持つすべてのパーティションを削除し、一致したパーティションを新しい最初のパーティションにします。NULL パーティションには影響しません。

    ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)

次のステートメントは最後のパーティションを変更します。つまり、範囲が広く、新しいデータのためのスペースがあるパーティションを追加します。指定された式までの現在の INTERVAL で新しいパーティションを追加します。1 `MAXVALUE PARTITION`存在する場合は、データの再編成が必要になるため機能しません。

    ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)

#### INTERVAL パーティションの詳細と制限 {#interval-partitioning-details-and-limitations}

-   INTERVAL パーティショニング機能には`CREATE/ALTER TABLE`構文のみが関係します。メタデータには変更がないため、新しい構文で作成または変更されたテーブルは引き続き MySQL と互換性があります。
-   MySQL との互換性を保つため、 `SHOW CREATE TABLE`の出力形式には変更はありません。
-   新しい`ALTER`構文は、INTERVAL に準拠する既存のテーブルに適用されます。これらのテーブルを`INTERVAL`構文で作成する必要はありません。
-   `RANGE COLUMNS`パーティション分割に`INTERVAL`構文を使用する場合、パーティション キーとして指定できるのは`INTEGER` 、 `DATE` 、または`DATETIME`タイプの単一の列のみです。

### List パーティショニング {#list-partitioning}

リストパーティションテーブルを作成する前に、次のシステム変数がデフォルト値の`ON`に設定されていることを確認してください。

-   [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)
-   [`tidb_enable_table_partition`](/system-variables.md#tidb_enable_table_partition)

List パーティショニングは、範囲パーティションに似ています。範囲パーティションとは異なり、List パーティショニングでは、各パーティションのすべての行のパーティション式の値が、特定の値セットに含まれます。各パーティションに定義されたこの値セットには、任意の数の値を含めることができますが、重複する値を含めることはできません。値セットを定義するには、 `PARTITION ... VALUES IN (...)`句を使用できます。

人事記録テーブルを作成するとします。テーブルは次のように作成できます。

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

上記のようにパーティションを作成した後は、テーブル内の特定の地域に関連するレコードを簡単に追加または削除できます。たとえば、東部地域 (East) のすべての店舗が別の会社に売却されたとします。次に、 `ALTER TABLE employees TRUNCATE PARTITION pEast`実行することで、この地域の店舗従業員に関連するすべての行データを削除できます。これは、同等のステートメント`DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)`よりもはるかに効率的です。

`ALTER TABLE employees DROP PARTITION pEast`実行して関連するすべての行を削除することもできますが、このステートメントはテーブル定義から`pEast`パーティションも削除します。この状況では、 `ALTER TABLE ... ADD PARTITION`ステートメントを実行して、テーブルの元のパーティション スキームを回復する必要があります。

#### デフォルトのリストパーティション {#default-list-partition}

v7.3.0 以降では、リストまたはリスト列パーティションテーブルにデフォルト パーティションを追加できます。デフォルト パーティションはフォールバック パーティションとして機能し、どのパーティションの値セットにも一致しない行を配置できます。

> **注記：**
>
> この機能は、MySQL 構文に対する TiDB 拡張です。デフォルト パーティションを持つリストまたはリスト COLUMNSパーティションテーブルの場合、テーブル内のデータを MySQL に直接複製することはできません。

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

デフォルト パーティションのないリストまたはリスト COLUMNSパーティションテーブルの場合、 `INSERT`ステートメントを使用して挿入される値は、テーブルの`PARTITION ... VALUES IN (...)`の句で定義された値セットと一致する必要があります。挿入される値がどのパーティションの値セットとも一致しない場合、ステートメントは失敗し、次の例に示すようにエラーが返されます。

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

前述のエラーを無視するには、 `INSERT`ステートメントに`IGNORE`キーワードを追加します。このキーワードを追加すると、 `INSERT`ステートメントはパーティション値セットに一致する行のみを挿入し、一致しない行は挿入せず、エラーは返されません。

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

List COLUMNS パーティショニングは、 `DATETIME`List パーティショニングのバリエーションです。複数の列をパーティション キーとして使用できます。整数データ型の他に、文字列、 `DATE`データ型の列もパーティション列として使用できます。

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

List COLUMNS パーティショニングは、次の例に示すように、 `DATE`および`DATETIME`タイプの列を使用して実装することもできます。この例では、前の`employees_1`テーブルと同じ名前と列を使用しますが、 `hired`列に基づいてList COLUMNS パーティショニングを使用します。

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

さらに、 `COLUMNS()`句に複数の列を追加することもできます。例:

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

ハッシュ パーティション分割は、データが一定数のパーティションに均等に分散されるようにするために使用されます。範囲パーティション分割を使用する場合、範囲パーティション分割を使用するときは各パーティションの列値の範囲を指定する必要がありますが、ハッシュ パーティション分割を使用する場合はパーティションの数を指定するだけで済みます。

ハッシュパーティションテーブルを作成するには、 `CREATE TABLE`ステートメントに`PARTITION BY HASH (expr)`句を追加する必要があります。 `expr`整数を返す式です。この列の型が整数の場合は、列名にすることができます。さらに、 `PARTITIONS num`追加する必要がある場合もあります。ここで、 `num`は、テーブルがいくつのパーティションに分割されているかを示す正の整数です。

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

`expr`に対して整数を返す SQL 式を使用することもできます。たとえば、雇用年ごとにテーブルをパーティション分割できます。

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

たとえば、 `date_col`タイプが`DATE`である列であり、 `TO_DAYS(date_col)`式の値は`date_col`の値によって変化します。 `YEAR(date_col)`は`TO_DAYS(date_col)`とは異なります。これは、 `date_col`のすべての可能な変更が`YEAR(date_col)`の同等の変更を生成するとは限らないためです。

対照的に、 `INT`型の`int_col`列があるとします。ここで、式`POW(5-int_col,3) + 6`について考えてみましょう。ただし、 `int_col`の値が変わっても、式の結果は比例して変化しないため、これは適切なハッシュ関数ではありません。 `int_col`の値が変わると、式の結果が大きく変わる可能性があります。たとえば、 `int_col` 5 から 6 に変わると、式の結果の変化は -1 になります。しかし、 `int_col` 6 から 7 に変わると、結果の変化は -7 になる可能性があります。

結論として、式が`y = cx`に近い形式である場合、ハッシュ関数に適しています。式が非線形であるほど、パーティション間でデータが不均一に分散される傾向があるためです。

理論上は、複数の列値を含む式に対してもプルーニングは可能ですが、どの式が適切かを判断するのは非常に難しく、時間がかかります。このため、複数の列を含むハッシュ式の使用は特に推奨されません。

`PARTITION BY HASH`使用する場合、TiDB は式の結果の係数に基づいて、データがどのパーティションに分類されるかを決定します。つまり、パーティション式が`expr`パーティション数が`num`の場合、 `MOD(expr, num)`によってデータが格納されるパーティションが決まります。 `t1`次のように定義されていると仮定します。

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

`t1`にデータ行を挿入し、 `col3`の値が「2005-09-15」の場合、この行はパーティション 1 に挿入されます。

    MOD(YEAR('2005-09-01'),4)
    =  MOD(2005,4)
    =  1

### キーの分割 {#key-partitioning}

v7.0.0 以降、TiDB はキー パーティションをサポートします。v7.0.0 より前のバージョンの TiDB では、キーパーティションテーブルを作成しようとすると、TiDB はそれを非パーティションテーブルとして作成し、警告を返します。

キー パーティショニングとハッシュ パーティショニングはどちらも、一定数のパーティションにデータを均等に分散できます。違いは、ハッシュ パーティショニングは指定された整数式または整数列に基づいてデータを分散することしかサポートしていないのに対し、キー パーティショニングは列リストに基づいてデータを分散することをサポートしており、キー パーティショニングのパーティション列は整数型に限定されていないことです。TiDB のキー パーティショニングのハッシュ アルゴリズムは MySQL のハッシュ アルゴリズムとは異なるため、テーブル データの分散も異なります。

キーパーティションテーブルを作成するには、 `CREATE TABLE`ステートメントに`PARTITION BY KEY (columnList)`句を追加する必要があります。 `columnList` 、1 つ以上の列名を含む列リストです。リスト内の各列のデータ型は、 `BLOB` 、 `JSON` 、および`GEOMETRY`除く任意の型にすることができます (TiDB は`GEOMETRY`サポートしていないことに注意してください)。さらに、 `PARTITIONS num` ( `num`はテーブルがいくつのパーティションに分割されているかを示す正の整数) を追加したり、パーティション名の定義を追加したりする必要がある場合もあります。たとえば、 `(PARTITION p0, PARTITION p1)`追加すると、テーブルが`p0`と`p1`名前の 2 つのパーティションに分割されます。

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

VARCHAR などの非整数列に基づいてキーパーティションテーブルを作成することもできます。たとえば、 `fname`列でテーブルをパーティション分割できます。

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

複数の列に基づいてキーパーティションテーブルを作成することもできます。たとえば、 `fname`と`store_id`に基づいてテーブルを 4 つのパーティションに分割できます。

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

MySQL と同様に、TiDB は`PARTITION BY KEY`で指定された空のパーティション列リストを使用してキー パーティション テーブルの作成をサポートします。たとえば、次のステートメントは、プライマリ キー`id`パーティション キーとして使用してパーティションテーブルを作成します。

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

v6.4.0 より前では、TiDB で[MySQL 線形ハッシュ](https://dev.mysql.com/doc/refman/8.0/en/partitioning-linear-hash.html)パーティションの DDL ステートメントを実行すると、TiDB はパーティション化されていないテーブルしか作成できませんでした。この場合、TiDB でパーティション化されたテーブルを引き続き使用するには、DDL ステートメントを変更する必要があります。

v6.4.0 以降、TiDB は MySQL `PARTITION BY LINEAR HASH`構文の解析をサポートしていますが、その中の`LINEAR`キーワードは無視されます。MySQL リニア ハッシュ パーティションの既存の DDL および DML ステートメントがある場合は、変更せずに TiDB で実行できます。

-   MySQL リニア ハッシュ パーティションの`CREATE`ステートメントに対して、TiDB は非線形ハッシュパーティションテーブルを作成します (TiDB にはリニア ハッシュパーティションテーブルがないことに注意してください)。パーティション数が 2 の累乗の場合、TiDB ハッシュパーティションテーブルの行は、MySQL リニア ハッシュパーティションテーブルと同じように分散されます。それ以外の場合、TiDB でのこれらの行の分散は MySQL とは異なります。これは、非線形パーティション テーブルでは単純な「パーティション数の係数」が使用されるのに対し、リニア パーティション テーブルでは「次の 2 の累乗を係数とし、パーティション数と次の 2 の累乗の間で値を折り返す」ためです。詳細については、 [＃38450](https://github.com/pingcap/tidb/issues/38450)参照してください。

-   MySQL リニア ハッシュ パーティションの他のすべてのステートメントは、パーティション数が 2 の累乗でない場合、行が異なる方法で分散され、 [パーティションの選択](#partition-selection) 、 `TRUNCATE PARTITION` 、 `EXCHANGE PARTITION`に対して異なる結果が生成されることを除いて、TiDB でも MySQL と同じように機能します。

### TiDBがリニアキーパーティションを処理する方法 {#how-tidb-handles-linear-key-partitions}

v7.0.0 以降、TiDB はキー パーティショニングの MySQL `PARTITION BY LINEAR KEY`構文の解析をサポートしています。ただし、TiDB は`LINEAR`キーワードを無視し、代わりに非線形ハッシュ アルゴリズムを使用します。

v7.0.0 より前では、キーパーティションテーブルを作成しようとすると、TiDB はそれを非パーティションテーブルとして作成し、警告を返します。

### TiDB パーティショニングが NULL を処理する方法 {#how-tidb-partitioning-handles-null}

TiDB では、パーティション式の計算結果として`NULL`使用できます。

> **注記：**
>
> `NULL`整数ではありません。TiDB のパーティショニング実装では、 `ORDER BY`と同様に、 `NULL`他の整数値よりも小さいものとして扱われます。

#### 範囲分割による NULL の扱い {#handling-of-null-with-range-partitioning}

範囲によってパーティション化されたテーブルに行を挿入し、パーティションを決定するために使用される列の値が`NULL`場合、この行は最下位のパーティションに挿入されます。

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

パーティション`p0`を削除し、結果を確認します。

```sql
alter table t1 drop partition p0;
```

    Query OK, 0 rows affected (0.08 sec)

```sql
select * from t1;
```

    Empty set (0.00 sec)

#### ハッシュパーティションによるNULLの扱い {#handling-of-null-with-hash-partitioning}

ハッシュでテーブルをパーティション分割する場合、 `NULL`値を処理する方法が異なります。パーティション式の計算結果が`NULL`場合、 `0`と見なされます。

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
> TiDB のハッシュパーティションによる`NULL`値は、 [MySQL パーティショニングが NULL を処理する方法](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html)で説明したのと同じ方法で処理されますが、これは MySQL の実際の動作と一致していません。つまり、この場合の MySQL の実装は、ドキュメントと一致していません。
>
> この場合、TiDB の実際の動作はこのドキュメントの説明と一致します。

#### キー分割によるNULLの処理 {#handling-of-null-with-key-partitioning}

キーパーティショニングの場合、 `NULL`値の扱い方はハッシュパーティショニングと同じです。パーティショニングフィールドの値が`NULL`の場合、 `0`として扱われます。

## パーティション管理 {#partition-management}

`RANGE` 、 `RANGE COLUMNS` 、 `LIST` 、および`LIST COLUMNS`にパーティション化されたテーブルの場合、次のようにパーティションを管理できます。

-   `ALTER TABLE <table name> ADD PARTITION (<partition specification>)`ステートメントを使用してパーティションを追加します。
-   `ALTER TABLE <table name> DROP PARTITION <list of partitions>`ステートメントを使用してパーティションを削除します。
-   `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>`ステートメントを使用して、指定されたパーティションからすべてのデータを削除します`TRUNCATE PARTITION`のロジックは[`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)と似ていますが、パーティション用です。
-   `ALTER TABLE <table name> REORGANIZE PARTITION <list of partitions> INTO (<new partition definitions>)`ステートメントを使用して、パーティションを結合、分割、またはその他の変更を行います。

`HASH`パーティション テーブルと`KEY`パーティション テーブルの場合、次のようにパーティションを管理できます。

-   `ALTER TABLE <table name> COALESCE PARTITION <number of partitions to decrease by>`ステートメントを使用してパーティションの数を減らします。この操作は、テーブル全体をオンラインで新しいパーティションの数にコピーして、パーティションを再編成します。
-   `ALTER TABLE <table name> ADD PARTITION <number of partitions to increase by | (additional partition definitions)>`ステートメントを使用してパーティションの数を増やします。この操作は、テーブル全体をオンラインで新しいパーティションの数にコピーして、パーティションを再編成します。
-   `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>`ステートメントを使用して、指定されたパーティションからすべてのデータを削除します`TRUNCATE PARTITION`のロジックは[`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)と似ていますが、パーティション用です。

`EXCHANGE PARTITION` 、 `RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2`ようなテーブルの名前変更の動作と同様に、パーティションとパーティションテーブルを交換することによって動作します。

たとえば、 `ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table` `partitioned_table`テーブル`p1`パーティションを`non_partitioned_table`テーブルと交換します。

パーティションに交換するすべての行がパーティション定義と一致していることを確認してください。一致しない場合、ステートメントは失敗します。

TiDB には`EXCHANGE PARTITION`影響する可能性のある特定の機能がいくつかあることに注意してください。テーブル構造にそのような機能が含まれている場合は、 `EXCHANGE PARTITION` [MySQLのEXCHANGE PARTITION条件](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html)を満たしていることを確認する必要があります。また、これらの特定の機能がパーティション化されたテーブルとパーティション化されていないテーブルの両方で同じように定義されていることを確認してください。これらの特定の機能には次のものが含まれます。

<CustomContent platform="tidb">

-   [SQL の配置ルール](/placement-rules-in-sql.md) : 配置ポリシーは同じです。

</CustomContent>

-   [TiFlash](/tikv-overview.md) : TiFlashレプリカの数は同じです。
-   [クラスター化インデックス](/clustered-indexes.md) : パーティション化されたテーブルとパーティション化されていないテーブルの両方が`CLUSTERED`あるか、両方が`NONCLUSTERED` 。

さらに、 `EXCHANGE PARTITION`と他のコンポーネントとの互換性には制限があります。パーティション化されたテーブルとパーティション化されていないテーブルの両方の定義が同じである必要があります。

-   TiFlash: パーティション化されたテーブルとパーティション化されていないテーブルのTiFlashレプリカ定義が異なる場合、 `EXCHANGE PARTITION`操作は実行できません。
-   TiCDC: パーティション化されたテーブルとパーティション化されていないテーブルの両方に主キーまたは一意のキーがある場合、TiCDC は`EXCHANGE PARTITION`操作を複製します。それ以外の場合、TiCDC は操作を複製しません。
-   TiDB LightningおよびBR: TiDB Lightning を使用したインポート中、またはBRを使用した復元中に`EXCHANGE PARTITION`操作を実行しません。

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

範囲パーティションテーブルの場合、 `ADD PARTITION`最後の既存パーティションの後に新しいパーティションを追加します。既存のパーティションと比較して、新しいパーティションに対して`VALUES LESS THAN`で定義された値の方が大きくなければなりません。そうでない場合は、エラーが報告されます。

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

パーティションを結合:

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

-   パーティションの再編成 (パーティションの結合または分割を含む) により、リストされたパーティションを新しいパーティション定義セットに変更できますが、パーティション分割のタイプを変更することはできません (たとえば、リスト タイプを範囲タイプに変更したり、範囲列タイプを範囲タイプに変更したりすることはできません)。

-   範囲パーティション テーブルの場合、テーブル内の隣接するパーティションのみを再編成できます。

    ```sql
    ALTER TABLE members REORGANIZE PARTITION p1800,p2000 INTO (PARTITION p2000 VALUES LESS THAN (2100));
    ```

        ERROR 8200 (HY000): Unsupported REORGANIZE PARTITION of RANGE; not adjacent partitions

-   範囲パーティションテーブルの場合、範囲の終了を変更するには、 `VALUES LESS THAN`で定義した新しい終了が最後のパーティションの既存の行をカバーする必要があります。そうでない場合、既存の行が収まらなくなり、エラーが報告されます。

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

-   パーティションが再編成されると、対応するパーティションの統計が古くなるため、次の警告が表示されます。この場合、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを使用して統計を更新できます。

    ```sql
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Level   | Code | Message                                                                                                                                                |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

### ハッシュとキーのパーティションを管理する {#manage-hash-and-key-partitions}

このセクションでは、次の SQL ステートメントによって作成されたパーティションテーブルを例として使用して、ハッシュ パーティションを管理する方法を示します。キー パーティションの場合も、同じ管理ステートメントを使用できます。

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

パーティション定義を追加してパーティション オプションを指定することもできます。たとえば、次のステートメントを使用してパーティションの数を 3 から 5 に増やし、新しく追加されたパーティションの名前を`pExample4`と`pExample5`として指定できます。

```sql
ALTER TABLE example ADD PARTITION
(PARTITION pExample4 COMMENT = 'not p3, but pExample4 instead',
 PARTITION pExample5 COMMENT = 'not p4, but pExample5 instead');
```

#### パーティションの数を減らす {#decrease-the-number-of-partitions}

範囲List パーティショニングとは異なり、ハッシュパーティション分割やキーパーティション分割では`DROP PARTITION`サポートされていませんが、 `COALESCE PARTITION`使用してパーティションの数を減らしたり、 `TRUNCATE PARTITION`を使用して特定のパーティションからすべてのデータを削除したりできます。

`example`テーブルのパーティション数を 1 つ減らします (5 から 4 に)。

```sql
ALTER TABLE example COALESCE PARTITION 1;
```

> **注記：**
>
> ハッシュまたはキー パーティション テーブルのパーティション数を変更するプロセスでは、すべてのデータを新しいパーティション数にコピーしてパーティションを再編成します。そのため、ハッシュまたはキーパーティションテーブルのパーティション数を変更すると、古い統計に関する次の警告が表示されます。この場合、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを使用して統計を更新できます。
>
> ```sql
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Level   | Code | Message                                                                                                                                                |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> 1 row in set (0.00 sec)
> ```

`example`テーブルが現在どのように構成されているかをよりよく理解するために、 `example`テーブルを再作成するために使用される SQL ステートメントを次のように示します。

```sql
SHOW CREATE TABLE\G
```

    *************************** 1. row ***************************
           Table: example
    Create Table: CREATE TABLE `example` (
      `id` int(11) NOT NULL,
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

パーティションテーブルをパーティションテーブルに変換するには、次のステートメントを使用します。このステートメントは、パーティション化を削除し、テーブルのすべての行をコピーし、テーブルのインデックスをオンラインで再作成します。

```sql
ALTER TABLE <table_name> REMOVE PARTITIONING
```

たとえば、 `members`パーティションテーブルを非パーティションテーブルに変換するには、次のステートメントを実行します。

```sql
ALTER TABLE members REMOVE PARTITIONING
```

### 既存のテーブルをパーティション分割する {#partition-an-existing-table}

既存の非パーティションテーブルをパーティション化したり、既存のパーティションテーブルのパーティション タイプを変更したりするには、次のステートメントを使用します。このステートメントは、すべての行をコピーし、新しいパーティション定義に従ってインデックスをオンラインで再作成します。

```sql
ALTER TABLE <table_name> PARTITION BY <new partition type and definitions>
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

## パーティションの整理 {#partition-pruning}

[パーティションの整理](/partition-pruning.md)は、一致しないパーティションをスキャンしないという非常に単純な考えに基づいた最適化です。

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

結果が`p1`または`p2`パーティションのいずれかに該当することは明らかです。つまり、 `p1`と`p2`で一致する行を検索するだけで済みます。不要なパーティションを除外することを「プルーニング」と呼びます。オプティマイザーがパーティションの一部をプルーニングできる場合、パーティションテーブルでのクエリの実行は、パーティションテーブルでのクエリの実行よりもはるかに高速になります。

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

    このクエリでは、残された結合が内部結合に変換され、 `t1.x > 5`が`t1.x = t2.x`と`t2.x > 5`から導出されるため、パーティション プルーニングに使用でき、パーティション`p1`のみが残ります。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    このクエリでは、 `t2.x > 5` `t1`のパーティションテーブルにプッシュダウンすることはできないため、このクエリではパーティション プルーニングは有効になりません。

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

    このクエリは`t2`から行を読み取り、その結果を`t1`のサブクエリに使用します。理論的には、パーティション プルーニングはサブクエリの`t1.x > val`から恩恵を受ける可能性がありますが、実行フェーズで発生するため、ここでは効果がありません。

3.  現在の実装の制限により、クエリ条件を TiKV にプッシュダウンできない場合は、パーティション プルーニングで使用できません。

    `fn(col)`式を例に挙げます。TiKV コプロセッサがこの`fn`機能をサポートしている場合、プラン最適化フェーズ中に述語プッシュダウン ルールに従って`fn(col)`がリーフ ノード (つまり、パーティションテーブル) にプッシュダウンされ、パーティション プルーニングで使用できます。

    TiKV コプロセッサがこの`fn`機能をサポートしていない場合、 `fn(col)`リーフ ノードにプッシュダウンされません。代わりに、リーフ ノードの上の`Selection`ノードになります。現在のパーティション プルーニング実装では、この種のプラン ツリーはサポートされていません。

4.  ハッシュおよびキー パーティション タイプの場合、パーティション プルーニングでサポートされるクエリは等しい条件のみです。

5.  範囲パーティションの場合、パーティション プルーニングを有効にするには、パーティション式が`col`または`fn(col)`形式であり、クエリ条件が`>` 、 `<` 、 `=` 、 `>=` 、および`<=`のいずれかである必要があります。パーティション式が`fn(col)`の形式である場合、 `fn`関数は単調である必要があります。

    `fn`関数が単調である場合、任意の`x`および`y`に対して、 `x > y`であれば`fn(x) > fn(y)`です。この場合、この`fn`関数は厳密に単調であると言えます。任意の`x`および`y`に対して、 `x > y`であれば`fn(x) >= fn(y)`です。この場合、 `fn`も「単調」であると言えます。理論的には、すべての単調関数はパーティション プルーニングによってサポートされます。

    現在、TiDB のパーティション プルーニングでは、次の単調な関数のみがサポートされています。

    -   [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    -   [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)

    たとえば、パーティション式は単純な列です。

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    または、パーティション式は`fn(col)`の形式で、 `fn`は`to_days`なります。

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    例外は、パーティション式が`floor(unix_timestamp())`場合です。TiDB は、その場合、ケースごとに最適化を行うため、パーティション プルーニングによってサポートされます。

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

`p1`パーティションに保存されている行を表示できます。

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

複数のパーティションの行を取得する場合は、カンマで区切られたパーティション名のリストを使用できます。たとえば、 `SELECT * FROM employees PARTITION (p1, p2)`パーティション`p1`と`p2`のすべての行を返します。

パーティション選択を使用する場合でも、 `WHERE`条件と`ORDER BY`や`LIMIT`などのオプションを使用できます。 `HAVING`や`GROUP BY`などの集計オプションの使用もサポートされています。

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

パーティションの選択は、範囲パーティションやハッシュ パーティションを含むすべてのタイプのテーブル パーティションでサポートされています。ハッシュ パーティションの場合、パーティション名が指定されていない場合は、 `p0` 、 `p1` 、 `p2` 、...、または`pN-1`パーティション名として自動的に使用されます。

`SELECT` in `INSERT ... SELECT`ではパーティション選択も使用できます。

## パーティションの制限と制約 {#restrictions-and-limitations-on-partitions}

このセクションでは、TiDB のパーティション テーブルに関するいくつかの制限と制約について説明します。

-   [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)ステートメントを使用してパーティション テーブルの列タイプを変更することはサポートされていません。
-   [`ALTER TABLE ... CACHE`](/cached-tables.md)ステートメントを使用してパーティション テーブルをキャッシュ テーブルに設定することはサポートされていません。
-   TiDB の[一時テーブル](/temporary-tables.md)はパーティション テーブルと互換性**がありません**。
-   パーティションテーブルに[外部キー](/foreign-key.md)を作成することはサポートされていません。
-   パーティション テーブル上のインデックスは順番に読み取ることができないため、 [`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)ヒントはパーティション テーブルとその関連インデックスには機能しません。

### パーティションキー、主キー、一意キー {#partitioning-keys-primary-keys-and-unique-keys}

このセクションでは、パーティション キーと主キーおよび一意キーとの関係について説明します。この関係を規定するルールは、次のように表現できます。**テーブルのすべての一意キーは、テーブルのパーティション式のすべての列を使用する必要があります**。これには、テーブルの主キーも含まれます。これは、定義上、一意キーであるためです。

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

    ERROR 1491 (HY000): A PRIMARY KEY must include all columns in the table's partitioning function

`CREATE TABLE`ステートメントは、提案されたパーティション キーに`col1`と`col3`両方が含まれていますが、これらの列はどちらもテーブル上の両方の一意のキーの一部ではないため失敗します。次の変更を行うと、 `CREATE TABLE`ステートメントが有効になります。

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

次のテーブルは、両方の一意のキーに属する列をパーティション キーに含める方法がないため、まったくパーティション化できません。

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

上記の例では、プライマリ キーにパーティション式で参照されるすべての列が含まれていません。プライマリ キーに不足している列を追加すると、 `CREATE TABLE`ステートメントが有効になります。

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

テーブルに一意のキーも主キーもない場合、この制限は適用されません。

DDL ステートメントを使用してテーブルを変更する場合は、一意のインデックスを追加するときにこの制限も考慮する必要があります。たとえば、次に示すようにパーティションテーブルを作成するとします。

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

`ALTER TABLE`ステートメントを使用して、一意でないインデックスを追加できます。ただし、一意のインデックスを追加する場合は、一意のインデックスに`c1`列が含まれている必要があります。

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
ERROR 1503 (HY000): A UNIQUE INDEX must include all columns in the table's partitioning function
```

### 関数に関するパーティション分割の制限 {#partitioning-limitations-relating-to-functions}

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

現在、TiDB は、範囲パーティション、範囲列パーティション、List パーティショニング、List COLUMNS パーティショニング、ハッシュ パーティション、およびキー パーティションをサポートしています。MySQL で使用できるその他のパーティション タイプは、TiDB ではまだサポートされていません。

サポートされていないパーティション タイプの場合、TiDB でテーブルを作成すると、パーティション情報は無視され、警告が報告されて通常の形式でテーブルが作成されます。

`LOAD DATA`構文は現在 TiDB のパーティション選択をサポートしていません。

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

通常の`LOAD DATA`操作がサポートされています:

```sql
load local data infile "xxx" into t ...
```

しかし、 `Load Data`パーティション選択をサポートしていません。

```sql
load local data infile "xxx" into t partition (p1)...
```

パーティションテーブルの場合、 `select * from t`によって返される結果はパーティション間で順序付けられていません。これは、パーティション間では順序付けられているがパーティション内では順序付けられていない MySQL の結果とは異なります。

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

`tidb_enable_list_partition`環境変数は、パーティションテーブル機能を有効にするかどうかを制御します。この変数を`OFF`に設定すると、テーブルの作成時にパーティション情報は無視され、このテーブルは通常のテーブルとして作成されます。

この変数はテーブル作成時にのみ使用されます。テーブル作成後にこの変数の値を変更しても効果はありません。詳細については[システム変数](/system-variables.md#tidb_enable_list_partition-new-in-v50)参照してください。

### 動的プルーニングモード {#dynamic-pruning-mode}

TiDB は、 `dynamic`または`static`モードのいずれかでパーティション テーブルにアクセスします。v6.3.0 以降では、 `dynamic`モードがデフォルトで使用されます。ただし、動的パーティション分割は、完全なテーブル レベルの統計、つまり GlobalStats が収集された後にのみ有効になります。GlobalStats が収集される前は、TiDB は代わりに`static`モードを使用します。GlobalStats の詳細については、 [動的プルーニングモードでパーティションテーブルの統計を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

手動の ANALYZE と通常のクエリでは、セッション レベル`tidb_partition_prune_mode`設定が使用されます。バックグラウンドでの`auto-analyze`操作では、グローバル`tidb_partition_prune_mode`設定が使用されます。

`static`モードでは、パーティション テーブルはパーティション レベルの統計を使用します。3 `dynamic`では、パーティション テーブルはテーブル レベルの GlobalStats を使用します。

`static`モードから`dynamic`モードに切り替えるときは、統計を手動で確認して収集する必要があります。これは、 `dynamic`モードに切り替えた後、パーティション テーブルにはパーティション レベルの統計のみがあり、テーブル レベルの統計がないためである。GlobalStats は次の`auto-analyze`操作でのみ収集されます。

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

グローバル`dynamic`プルーニング モードを有効にした後、SQL ステートメントで使用される統計が正しいことを確認するには、テーブルまたはテーブルのパーティションで`analyze`手動でトリガーして GlobalStats を取得する必要があります。

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

スクリプトを使用して、すべてのパーティション テーブルの統計を更新することもできます。詳細については、 [動的プルーニングモードでパーティションテーブルの統計を更新する](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。

テーブル レベルの統計が準備できたら、すべての SQL ステートメントと`auto-analyze`操作に有効なグローバル動的プルーニング モードを有効にできます。

```sql
set global tidb_partition_prune_mode = dynamic
```

`static`モードでは、 TiDB は複数の演算子を使用して各パーティションに個別にアクセスし、 `Union`使用して結果をマージします。次の例は、 TiDB が`Union`を使用して 2 つの対応するパーティションの結果をマージする単純な読み取り操作です。

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

上記のクエリ結果から、パーティション プルーニングは引き続き有効であるものの、実行プラン内の`Union`演算子は消え、実行プランは`p0`と`p1`のみにアクセスすることがわかります。

`dynamic`モードでは、実行プランがよりシンプルで明確になります。Union 操作を省略すると、実行効率が向上し、Union 同時実行の問題を回避できます。さらに、 `dynamic`モードでは、 `static`モードでは使用できない IndexJoin を使用した実行プランも使用できます。(以下の例を参照)

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

#### 動的プルーニングモードでパーティションテーブルの統計を更新する {#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

1.  パーティション化されたすべてのテーブルを見つけます。

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
