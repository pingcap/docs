---
title: Partitioning
summary: TiDBにおけるパーティショニングの使い方を学びましょう。
---

# パーティショニング {#partitioning}

このドキュメントでは、TiDBにおけるパーティショニングの実装について説明します。

## パーティショニングの種類 {#partitioning-types}

このセクションでは、TiDB のパーティショニングの種類を紹介します。現在、TiDB は[範囲分割](#range-partitioning)、[範囲列パーティショニング](#range-columns-partitioning)ショニング、 [List パーティショニング](#list-partitioning)、 [List COLUMNS パーティショニング](#list-columns-partitioning)、[ハッシュパーティショニング](#hash-partitioning)、および[キーパーティショニング](#key-partitioning)をサポートしています。

-   範囲パーティショニング、範囲列パーティショニング、List パーティショニング、およびList COLUMNS パーティショニングは、アプリケーション内での大量の削除によって引き起こされるパフォーマンスの問題を解決し、パーティションを迅速に削除するために使用されます。
-   ハッシュパーティショニングとキーパーティショニングは、書き込み回数が多いシナリオでデータを分散するために使用されます。ハッシュパーティショニングと比較して、キーパーティショニングは複数の列のデータ分散と、非整数列によるパーティショニングをサポートします。

### 範囲分割 {#range-partitioning}

テーブルが範囲によってパーティション分割されている場合、各パーティションには、パーティション式値が指定された範囲内にある行が含まれます。範囲は連続している必要がありますが、重複してはなりません。これは`VALUES LESS THAN`を使用して定義できます。

次のような人事記録を含むテーブルを作成する必要があると仮定します。

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

必要に応じて、さまざまな方法で範囲に基づいてテーブルをパーティション分割できます。たとえば、 `store_id`列を使用してパーティション分割できます。

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

このパーティション方式では、 `store_id`が 1 ～ 5 である従業員に対応するすべての行が`p0`パーティションに格納され、 `store_id`が 6 ～ 10 である従業員はすべて`p1`パーティションに格納されます。範囲パーティショニングでは、パーティションを最小値から最大値の順に並べる必要があります。

`(72, 'Tom', 'John', '2015-06-25', NULL, NULL, 15)`のデータ行を挿入すると、 `p2`パーティションに配置されます。しかし、 `store_id`が 20 より大きいレコードを挿入すると、TiDB はこのレコードをどのパーティションに挿入すべきかを判断できないため、エラーが報告されます。この場合、テーブルを作成する際に`MAXVALUE`を使用できます。

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

`MAXVALUE`他のすべての整数値よりも大きい整数値を表します。したがって、 `store_id`が 16 (定義されている最大値) 以上であるすべてのレコードは`p3`パーティションに格納されます。

従業員の職種コード`job_code`列の値）に基づいてテーブルをパーティション分割することもできます。2桁の職種コードは一般従業員、3桁のコードは事務および顧客サポート担当者、4桁のコードは管理職を表すと仮定します。すると、次のようなパーティションテーブルを作成できます。

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

この例では、一般従業員に関するすべての行は`p0`パーティションに、すべての事務および顧客サポート担当者は`p1`パーティションに、すべての管理職は`p2`パーティションに格納されます。

`store_id`でテーブルを分割する以外にも、日付でテーブルを分割することができます。たとえば、従業員の退職年で分割できます。

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

範囲パーティショニングでは、 `timestamp`列の値に基づいてパーティショニングを行い、 `unix_timestamp()`関数を使用できます。例：

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

範囲分割は、以下の条件の1つ以上が満たされる場合に特に有効です。

-   古いデータを削除したい場合、前の例の`employees` `ALTER TABLE employees DROP PARTITION p0;` `DELETE FROM employees WHERE YEAR(separated) <= 1990;`操作を実行するよりも高速です。
-   時刻や日付の値を含む列、または他の系列から得られた値を含む列を使用したい場合。
-   パーティショニングに使用される列に対して、頻繁にクエリを実行する必要があります。たとえば、 `EXPLAIN SELECT COUNT(*) FROM employees WHERE separated BETWEEN '2000-01-01' AND '2000-12-31' GROUP BY store_id;`のようなクエリを実行すると、他のパーティション`p2`の条件に一致しないため、 `WHERE`パーティション内のデータのみをスキャンする必要があることを TiDB は迅速に認識できます。

### 範囲列パーティショニング {#range-columns-partitioning}

範囲列パーティショニングは、範囲パーティショニングのバリアントです。1 つ以上の列をパーティショニング キーとして使用できます。パーティション列のデータ型は、整数、文字列 ( `CHAR`または`VARCHAR` )、 `DATE` 、および`DATETIME` 。列を使用しないパーティショニングなどの式はサポートされていません。

範囲パーティショニングと同様に、範囲列パーティショニングでも、パーティション範囲は厳密に増加している必要があります。次の例のパーティション定義はサポートされていません。

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

名前でパーティション分割し、古いデータや無効なデータを削除したい場合は、次のようにテーブルを作成できます。

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

上記の SQL ステートメントは`[ ('', ''), ('G', '2023-01-01 00:00:00') )` 、 `[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 、 `[ ('G', '2024-01-01 00:00:00'), ('M', '2023-01-01 00:00:00') )` 、 `[ ('M', '2023-01-01 00:00:00'), ('M', '2024-01-01 00:00:00') )` 、および`[ ('M', '2024-01-01 00:00:00'), ('S', '2023-01-01 00:00:00') )`範囲内で、年と名前でデータをパーティション分割します。これにより`[ ('S', '2023-01-01 00:00:00'), ('S', '2024-01-01 00:00:00') )`と`name` `valid_until`の両方でパーティション剪定のメリットを享受しながら、無効なデータを簡単に削除できます。この例では、 `[,)`左が閉じられ、右が開いている範囲を示しています。例えば、 `[ ('G', '2023-01-01 00:00:00'), ('G', '2024-01-01 00:00:00') )` 、名前が`'G'`であるデータの範囲を示します。このデータの範囲には`2023-01-01 00:00:00`が含まれ、 `2023-01-01 00:00:00`より大きく、 `2024-01-01 00:00:00`より小さい値です。 `(G, 2024-01-01 00:00:00)`は含まれません。

### 範囲 INTERVAL 分割 {#range-interval-partitioning}

範囲パーティショニング（INTERVALパーティショニング）は、範囲パーティショニングの拡張機能であり、指定した間隔のパーティションを簡単に作成できます。バージョン6.3.0以降、TIDBでは構文糖衣としてINTERVALパーティショニングが導入されています。

構文は以下のとおりです。

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

以下の表が作成されます。

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

範囲間隔パーティショニングは[範囲列](#range-columns-partitioning)パーティショニングでも機能します。

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

これは以下のテーブルを作成します。

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

オプションのパラメータ`NULL PARTITION` 、 `PARTITION P_NULL VALUES LESS THAN (<minimum value of the column type>)`として定義されたパーティションを作成します。パーティション式が`NULL`と評価される場合にのみ一致します。 `NULL`他の値より小さいとみなされることを説明する [範囲分割によるNULL値の処理](#handling-of-null-with-range-partitioning)参照してください。

オプションパラメータ`MAXVALUE PARTITION`最後のパーティションを`PARTITION P_MAXVALUE VALUES LESS THAN (MAXVALUE)`として作成します。

#### ALTER INTERVAL パーティションテーブル {#alter-interval-partitioned-tables}

INTERVALパーティショニングでは、パーティションの追加と削除のための構文もよりシンプルになります。

次のステートメントは、最初のパーティションを変更します。指定された式よりも小さい値を持つすべてのパーティションを削除し、一致したパーティションを新しい最初のパーティションにします。NULL パーティションには影響しません。

    ALTER TABLE table_name FIRST PARTITION LESS THAN (<expression>)

次のステートメントは最後のパーティションを変更します。つまり、より高い範囲と新しいデータのための余裕を持つパーティションを追加します。現在の INTERVAL から指定された式までの新しいパーティションが追加されます。 `MAXVALUE PARTITION`存在する場合は、データの再編成が必要となるため、このステートメントは機能しません。

    ALTER TABLE table_name LAST PARTITION LESS THAN (<expression>)

#### INTERVALパーティショニングの詳細と制限事項 {#interval-partitioning-details-and-limitations}

-   INTERVALパーティショニング機能は、 `CREATE/ALTER TABLE`構文のみを使用します。メタデータに変更はないため、新しい構文で作成または変更されたテーブルは引き続きMySQLと互換性があります。
-   MySQLとの互換性を維持するため、 `SHOW CREATE TABLE`の出力形式に変更はありません。
-   新しい`ALTER`構文は、INTERVAL に準拠する既存のテーブルに適用されます。これらのテーブルを`INTERVAL`構文で作成する必要はありません。
-   `INTERVAL`パーティショニングに`RANGE COLUMNS`構文を使用する場合、パーティショニングキーとして指定できる列は`INTEGER` 、 `DATE` 、または`DATETIME`型の単一の列のみです。

### List パーティショニング {#list-partitioning}

List パーティショニングは、範囲パーティショニングと似ています。範囲パーティショニングとは異なり、List パーティショニングでは、各パーティション内のすべての行のパーティショニング式の値は、指定された値セットに含まれます。各パーティションに定義されるこの値セットには、任意の数の値を含めることができますが、重複する値を含めることはできません。値セットを定義するには、 `PARTITION ... VALUES IN (...)`句を使用できます。

人事記録テーブルを作成したいとします。テーブルは次のように作成できます。

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
);
```

下の表に示すように、4つの地区に20の店舗が分布していると仮定します。

    | Region  | Store ID Numbers     |
    | ------- | -------------------- |
    | North   | 1, 2, 3, 4, 5        |
    | East    | 6, 7, 8, 9, 10       |
    | West    | 11, 12, 13, 14, 15   |
    | Central | 16, 17, 18, 19, 20   |

同じ地域の従業員の人事データを同じパーティションに保存したい場合は、 `store_id`に基づいてリストパーティションテーブルを作成できます。

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

上記のようにパーティションを作成した後、テーブル内の特定の地域に関連するレコードを簡単に追加または削除できます。たとえば、東地域（East）のすべての店舗が別の会社に売却されたとします。この場合`ALTER TABLE employees TRUNCATE PARTITION pEast` `DELETE FROM employees WHERE store_id IN (6, 7, 8, 9, 10)`よりもはるかに効率的です。

`ALTER TABLE employees DROP PARTITION pEast`を実行して関連するすべての行を削除することもできますが、このステートメントはテーブル定義から`pEast`パーティションも削除します。この場合、 `ALTER TABLE ... ADD PARTITION`ステートメントを実行して、テーブルの元のパーティショニングスキームを復元する必要があります。

#### デフォルトリストパーティション {#default-list-partition}

バージョン7.3.0以降では、リストまたはリスト列でパーティションテーブルにデフォルトパーティションを追加できます。デフォルトパーティションはフォールバックパーティションとして機能し、どのパーティションの値セットにも一致しない行を配置できます。

> **Note:**
>
> この機能は、MySQL構文に対するTiDBの拡張機能です。デフォルトのパーティションを持つListまたはList COLUMNSパーティションテーブルの場合、テーブル内のデータをMySQLに直接レプリケートすることはできません。

次のリストパーティションテーブルを例として考えてみましょう。

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

テーブルに`pDef`という名前のデフォルトリストパーティションを追加するには、次のようにします。

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef DEFAULT);
```

または

```sql
ALTER TABLE t ADD PARTITION (PARTITION pDef VALUES IN (DEFAULT));
```

このようにすることで、どのパーティションの値セットにも一致しない新規挿入値は、自動的にデフォルトパーティションに格納される。

```sql
INSERT INTO t VALUES (7, 7);
Query OK, 1 row affected (0.01 sec)
```

リストまたはリスト列パーティションテーブルを作成する際に、デフォルトのパーティションを追加することもできます。例：

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

デフォルトパーティションのないリストまたはリスト COLUMNSパーティションテーブルの場合、 `INSERT`ステートメントを使用して挿入する値は、テーブルの`PARTITION ... VALUES IN (...)`句で定義されている値セットと一致する必要があります。挿入する値がどのパーティションの値セットとも一致しない場合、ステートメントは失敗し、次の例に示すようにエラーが返されます。

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

上記のエラーを無視するには、 `IGNORE`ステートメントに`INSERT` } キーワードを追加します。このキーワードを追加すると、 `INSERT`ステートメントはパーティション値セットに一致する行のみを挿入し、一致しない行は挿入せず、エラーも返しません。

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

List COLUMNS パーティショニングは、List パーティショニングの一種です。複数の列をパーティションキーとして使用できます。整数データ型の他に、文字列、 `DATE` 、および`DATETIME`データ型の列もパーティション列として使用できます。

次の表に示すように、以下の12都市の店舗従業員を4つの地域に分けたいとします。

    | Region | Cities                         |
    | :----- | ------------------------------ |
    | 1      | LosAngeles,Seattle, Houston    |
    | 2      | Chicago, Columbus, Boston      |
    | 3      | NewYork, LongIsland, Baltimore |
    | 4      | Atlanta, Raleigh, Cincinnati   |

以下に示すように、List COLUMNS パーティショニングを使用してテーブルを作成し、各行を従業員の都市に対応するパーティションに格納することができます。

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

List COLUMNS パーティショニングは、次の例に示すように、 `DATE`型と`DATETIME`型の列を使用して実装することもできます。この例では、前の`employees_1`テーブルと同じ名前と列を使用していますが、 `hired`列に基づくList COLUMNS パーティショニングを使用しています。

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

さらに、 `COLUMNS()`句に複数の列を追加することもできます。例：

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

ハッシュパーティショニングは、データが一定数のパーティションに均等に分散されるようにするために使用されます。範囲パーティショニングを使用する場合は、各パーティションの列値の範囲を指定する必要がありますが、ハッシュパーティショニングを使用する場合は、パーティションの数を指定するだけで済みます。

ハッシュパーティションテーブルを作成するには、 `PARTITION BY HASH (expr)`ステートメントに`CREATE TABLE` } 句を追加する必要があります。 `expr`は整数を返す式です。この列の型が整数型の場合は、列名にすることができます。さらに、 `PARTITIONS num`を追加する必要がある場合もあります。ここで、 `num`は、テーブルが分割されるパーティションの数を示す正の整数です。

以下の操作は、 `store_id`によって 4 つのパーティションに分割されたハッシュパーティションテーブルを作成します。

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

`expr`に対して整数を返す SQL 式を使用することもできます。たとえば、入社年でテーブルをパーティション分割できます。

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

最も効率的なハッシュ関数は、単一のテーブル列に対して作用し、その値が列の値に応じて一貫して増減するものです。

例えば、 `date_col`は型が`DATE`の列であり、 `TO_DAYS(date_col)`式の値は`date_col`の値によって変化します。 `YEAR(date_col)`は`TO_DAYS(date_col)`とは異なります。なぜなら、 `date_col`のすべての変更が`YEAR(date_col)`で同等の変更を引き起こすわけではないからです。

対照的に、型が`int_col`である`INT`列があると仮定します。ここで、式`POW(5-int_col,3) + 6`について考えてみましょう。これは良いハッシュ関数ではありません。なぜなら、 `int_col`の値が変化しても、式の結果は比例して変化しないからです。 `int_col`の値の変化によって、式の結果が大きく変化する可能性があります。たとえば、 `int_col` 5 から 6 に変化すると、式の結果の変化は -1 になります。しかし、 `int_col` 6 から 7 に変化すると、結果の変化は -7 になる可能性があります。

結論として、式が`y = cx`に近い形式である場合、ハッシュ関数としてより適しています。なぜなら、式の非線形性が高いほど、パーティション間でデータが不均一に分散される傾向があるからです。

理論的には、複数の列値を含む式に対しても枝刈りは可能ですが、どの式が適切かを判断するのは非常に困難で時間もかかります。そのため、複数の列を含むハッシュ式の使用は特に推奨されません。

`PARTITION BY HASH`を使用する場合、TiDB は式の計算結果の剰余に基づいて、データがどのパーティションに格納されるべきかを決定します。つまり、パーティショニング式が`expr`で、パーティション数が`num`の場合、 `MOD(expr, num)`によってデータが格納されるパーティションが決定されます。 `t1`が次のように定義されていると仮定します。

```sql
CREATE TABLE t1 (col1 INT, col2 CHAR(5), col3 DATE)
    PARTITION BY HASH( YEAR(col3) )
    PARTITIONS 4;
```

`t1`にデータ行を挿入し、 `col3`の値が「2005-09-15」である場合、この行はパーティション1に挿入されます。

    MOD(YEAR('2005-09-01'),4)
    =  MOD(2005,4)
    =  1

### キーパーティショニング {#key-partitioning}

TiDBはバージョン7.0.0以降、キーパーティショニングをサポートしています。バージョン7.0.0より前のTiDBでは、キーパーティションテーブルを作成しようとすると、TiDBはそれをパーティションテーブルとして作成し、警告を返します。

キーパーティショニングとハッシュパーティショニングはどちらも、データを一定数のパーティションに均等に分散できます。違いは、ハッシュパーティショニングは指定された整数式または整数列に基づいてのみデータを分散できるのに対し、キーパーティショニングは列リストに基づいてデータを分散できる点です。また、キーパーティショニングのパーティション列は整数型に限定されません。TiDBのキーパーティショニングにおけるハッシュアルゴリズムはMySQLとは異なるため、テーブルデータの分散方法も異なります。

キーパーティションテーブルを作成するには、 `PARTITION BY KEY (columnList)`ステートメントに`CREATE TABLE` } 句を追加する必要があります。 `columnList`は、1 つ以上の列名を含む列リストです。リスト内の各列のデータ型は`BLOB` 、 `JSON` 、および`GEOMETRY`除く任意の型にすることができます (TiDB は`GEOMETRY` } をサポートしていないことに注意してください)。さらに、 `PARTITIONS num` (ここで`num`テーブルが分割されるパーティションの数を示す正の整数) を追加したり、パーティション名の定義を追加したりする必要がある場合もあります。たとえば、 `(PARTITION p0, PARTITION p1)`を追加すると、テーブルが`p0`と`p1`という名前の 2 つのパーティションに分割されます。

以下の操作では、 `store_id`によって 4 つのパーティションに分割されたキーパーティションテーブルを作成します。

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

`PARTITIONS num`が指定されていない場合、デフォルトのパーティション数は 1 です。

VARCHARなどの非整数型の列に基づいてキーパーティションテーブルを作成することもできます。たとえば、 `fname`列でテーブルをパーティション化できます。

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

MySQLと同様に、TiDBは`PARTITION BY KEY`で指定された空のパーティション列リストを使用して、キーパーティションテーブルを作成することをサポートしています。たとえば、次のステートメントは、主キー`id`パーティションキーとして使用してパーティションテーブルを作成します。

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

テーブルに主キーがなく、一意キーが存在する場合、その一意キーがパーティショニングキーとして使用されます。

```sql
CREATE TABLE k1 (
    id INT NOT NULL,
    name VARCHAR(20),
    UNIQUE KEY (id)
)
PARTITION BY KEY()
PARTITIONS 2;
```

ただし、一意キー列が`NOT NULL`として定義されていない場合、上記のステートメントは失敗します。

#### TiDBが線形ハッシュパーティションを処理する方法 {#how-tidb-handles-linear-hash-partitions}

バージョン6.4.0より前では、 [MySQL 線形ハッシュ](https://dev.mysql.com/doc/refman/8.0/en/partitioning-linear-hash.html)のDDLステートメントを実行すると TiDBでパーティション分割されたテーブルを作成すると、TiDBはパーティション分割されていないテーブルしか作成できません。この場合、TiDBでパーティション分割されたテーブルを使用したい場合は、DDLステートメントを変更する必要があります。

バージョン6.4.0以降、TiDBはMySQLの`PARTITION BY LINEAR HASH`構文の解析をサポートしていますが、その中の`LINEAR`キーワードは無視します。MySQLリニアハッシュパーティションの既存のDDLおよびDMLステートメントがある場合は、TiDBで変更せずに実行できます。

-   MySQL の線形ハッシュパーティションの`CREATE`ステートメントの場合、TiDB は非線形ハッシュパーティションテーブルを作成します (TiDB には線形ハッシュパーティションテーブルはありません)。パーティション数が 2 のべき乗の場合、TiDB ハッシュパーティションテーブルの行は MySQL の線形ハッシュパーティションテーブルと同じように分散されます。それ以外の場合、TiDB でのこれらの行の分散は MySQL とは異なります。これは、非線形パーティションテーブルは単純な「パーティション数の剰余」を使用するのに対し、線形パーティションテーブルは「次の 2 のべき乗の剰余」を使用し、パーティション数と次の 2 のべき乗の間の値を折り返す」ためです。詳細については、 [#38450](https://github.com/pingcap/tidb/issues/38450)を参照してください。

-   MySQL の線形ハッシュパーティションのその他のすべてのステートメントについては、パーティション数が 2 のべき乗でない場合、行の分散方法が異なることを除いて、TiDB では MySQL と同じように動作します。この違いにより、 [パーティション選択](#partition-selection)、 `TRUNCATE PARTITION` 、および`EXCHANGE PARTITION`の結果は MySQL とは異なります。

### TiDBが線形キーパーティションを処理する方法 {#how-tidb-handles-linear-key-partitions}

バージョン7.0.0以降、TiDBはキーパーティショニングのためのMySQLの`PARTITION BY LINEAR KEY`構文の解析をサポートしています。ただし、TiDBは`LINEAR`キーワードを無視し、代わりに非線形ハッシュアルゴリズムを使用します。

バージョン7.0.0より前のバージョンでは、キーパーティションテーブルを作成しようとすると、TiDBはそれを非パーティションテーブルとして作成し、警告を返します。

### TiDBのパーティショニングがNULLをどのように処理するか {#how-tidb-partitioning-handles-null}

TiDBでは`NULL`パーティショニング式の計算結果として使用することが許可されています。

> **Note:**
>
> `NULL`整数ではありません。TiDB のパーティショニング実装では`NULL`は、 `ORDER BY`と同様に、他のどの整数値よりも小さい値として扱われます。

#### 範囲分割によるNULL値の処理 {#handling-of-null-with-range-partitioning}

範囲でパーティション分けされたテーブルに行を挿入し、パーティションを決定するために使用される列の値が`NULL`の場合、この行は最も低いパーティションに挿入されます。

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

`p0`パーティションを削除して、結果を確認してください。

```sql
alter table t1 drop partition p0;
```

    Query OK, 0 rows affected (0.08 sec)

```sql
select * from t1;
```

    Empty set (0.00 sec)

#### ハッシュパーティショニングによるNULLの処理 {#handling-of-null-with-hash-partitioning}

テーブルをハッシュで分割する場合、 `NULL`の値の処理方法が異なります。分割式の計算結果が`NULL`の場合、 `0`とみなされます。

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

挿入されたレコード`(NULL, 'mothra')`は`(0, 'gigan')`と同じパーティションに属していることがわかります。

> **Note:**
>
> TiDB のハッシュ パーティションによる`NULL`値は[MySQLパーティショニングがNULLをどのように処理するか](https://dev.mysql.com/doc/refman/8.0/en/partitioning-handling-nulls.html)で説明されているのと同じ方法で処理されますが、これは MySQL の実際の動作と一致しません。言い換えれば、この場合の MySQL の実装はそのドキュメントと一致していません。
>
> この場合、TiDBの実際の動作はこの文書の説明と一致しています。

#### キー分割によるNULLの処理 {#handling-of-null-with-key-partitioning}

キーパーティショニングの場合、 `NULL`値の処理方法はハッシュパーティショニングと同様です。パーティショニングフィールドの値が`NULL`の場合、 `0`として扱われます。

## パーティション管理 {#partition-management}

`RANGE` 、 `RANGE COLUMNS` 、 `LIST` 、および`LIST COLUMNS`パーティションテーブルの場合、パーティションは次のように管理できます。

-   `ALTER TABLE <table name> ADD PARTITION (<partition specification>)`ステートメントを使用してパーティションを追加します。
-   `ALTER TABLE <table name> DROP PARTITION <list of partitions>`ステートメントを使用してパーティションを削除します。
-   `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>`ステートメントを使用して、指定されたパーティションからすべてのデータを削除します。 `TRUNCATE PARTITION`のロジックは[`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)と似ていますが、パーティションを対象としています。
-   `ALTER TABLE <table name> REORGANIZE PARTITION <list of partitions> INTO (<new partition definitions>)`ステートメントを使用して、パーティションをマージ、分割、またはその他の変更します。

`HASH`および`KEY`パーティションテーブルの場合、パーティションは次のように管理できます。

-   `ALTER TABLE <table name> COALESCE PARTITION <number of partitions to decrease by>`ステートメントを使用してパーティション数を減らします。この操作では、テーブル全体を新しいパーティション数にオンラインでコピーすることにより、パーティションが再編成されます。
-   `ALTER TABLE <table name> ADD PARTITION <number of partitions to increase by | (additional partition definitions)>`ステートメントを使用してパーティション数を増やします。この操作では、テーブル全体を新しいパーティション数にオンラインでコピーすることにより、パーティションが再編成されます。
-   `ALTER TABLE <table name> TRUNCATE PARTITION <list of partitions>`ステートメントを使用して、指定されたパーティションからすべてのデータを削除します。 `TRUNCATE PARTITION`のロジックは[`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)と似ていますが、パーティションを対象としています。

`EXCHANGE PARTITION`は`RENAME TABLE t1 TO t1_tmp, t2 TO t1, t1_tmp TO t2`のようなテーブルの名前を変更するのと同様に、パーティションと非パーティションテーブルを交換することで機能します。

例えば、 `ALTER TABLE partitioned_table EXCHANGE PARTITION p1 WITH TABLE non_partitioned_table`は、 `partitioned_table`テーブルの`p1`パーティションを`non_partitioned_table`テーブルと交換します。

パーティションに交換するすべての行がパーティション定義と一致していることを確認してください。一致していない場合、ステートメントは失敗します。

TiDBには`EXCHANGE PARTITION`に影響を与える可能性のある特定の機能がいくつかあります。テーブル構造にそのような機能が含まれている場合、 `EXCHANGE PARTITION` [MySQLのEXCHANGEパーティション条件](https://dev.mysql.com/doc/refman/8.0/en/partitioning-management-exchange.html)を満たしていることを確認する必要があります。また、これらの特定の機能がパーティション化されたテーブルとパーティション化されていないテーブルの両方で同じように定義されていることを確認してください。これらの特定の機能には、次のものが含まれます。

<CustomContent platform="tidb">

-   [SQLにおける配置ルール](/placement-rules-in-sql.md): 配置ポリシーは同じです。

</CustomContent>

-   [TiFlash](/tikv-overview.md) ： TiFlashレプリカの数は同数です。
-   [クラスター化インデックス](/clustered-indexes.md): パーティション化テーブルと非パーティション化テーブルは両方とも`CLUSTERED` 、または両方とも`NONCLUSTERED`です。

さらに、 `EXCHANGE PARTITION`と他のコンポーネントとの互換性には制限があります。パーティション化されたテーブルとパーティション化されていないテーブルは、同じ定義を持つ必要があります。

-   TiFlash: パーティション化されたテーブルとパーティション化されていないテーブルのTiFlashレプリカ定義が異なる場合、 `EXCHANGE PARTITION`操作は実行できません。
-   TiCDC: TiCDC は、パーティション化されたテーブルとパーティション化されていないテーブルの両方に主キーまたは一意キーが存在する場合に`EXCHANGE PARTITION`操作を複製します。それ以外の場合は、TiCDC は操作を複製しません。
-   TiDB LightningおよびBR: TiDB Lightningを使用したインポート時、またはBRを使用したリストア時に`EXCHANGE PARTITION`操作を実行しないでください。

### 範囲、範囲列、リスト、およびリスト列パーティションの管理 {#manage-range-range-columns-list-and-list-columns-partitions}

このセクションでは、以下の SQL ステートメントによって作成されたパーティション テーブルを例として、範囲パーティションとリスト パーティションの管理方法を示します。

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

#### パーティションを切り詰める {#truncate-partitions}

```sql
ALTER TABLE members TRUNCATE PARTITION p1980;

ALTER TABLE member_level TRUNCATE PARTITION l4;
```

#### パーティションを追加する {#add-partitions}

```sql
ALTER TABLE members ADD PARTITION (PARTITION `p1990to2010` VALUES LESS THAN (2010));

ALTER TABLE member_level ADD PARTITION (PARTITION l5_6 VALUES IN (5,6));
```

範囲パーティションテーブルの場合、 `ADD PARTITION`既存の最後のパーティションの後に新しいパーティションを追加します。既存のパーティションと比較して、新しいパーティションに対して`VALUES LESS THAN`で定義された値は、より大きくなければなりません。そうでない場合は、エラーが報告されます。

```sql
ALTER TABLE members ADD PARTITION (PARTITION p1990 VALUES LESS THAN (2000));
```

    ERROR 1493 (HY000): VALUES LESS THAN value must be strictly increasing for each partition

#### パーティションを再編成する {#reorganize-partitions}

パーティションを分割する：

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

パーティションをマージする:

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1950,p1950 INTO (PARTITION pBefore1960 VALUES LESS THAN (1960));

ALTER TABLE member_level REORGANIZE PARTITION l1,l2 INTO (PARTITION l1_2 VALUES IN (1,2));
```

パーティショニングスキームの定義を変更します。

```sql
ALTER TABLE members REORGANIZE PARTITION pBefore1960,p1960,p1970,p1980,p1990,p2000,p2010,p2020,pMax INTO
(PARTITION p1800 VALUES LESS THAN (1900),
 PARTITION p1900 VALUES LESS THAN (2000),
 PARTITION p2000 VALUES LESS THAN (2100));

ALTER TABLE member_level REORGANIZE PARTITION l1_2,l3,l4,l5,l6 INTO
(PARTITION lOdd VALUES IN (1,3,5),
 PARTITION lEven VALUES IN (2,4,6));
```

パーティションを再編成する際には、以下の重要な点に注意してください。

-   パーティションの再編成（パーティションのマージや分割を含む）を行うと、一覧表示されているパーティションが新しいパーティション定義のセットに変わりますが、パーティショニングの種類（たとえば、リスト型を範囲型に変更したり、範囲列型を範囲型に変更したり）は変更できません。

-   範囲パーティションテーブルの場合、その中の隣接するパーティションのみを再編成できます。

    ```sql
    ALTER TABLE members REORGANIZE PARTITION p1800,p2000 INTO (PARTITION p2000 VALUES LESS THAN (2100));
    ```

        ERROR 8200 (HY000): Unsupported REORGANIZE PARTITION of RANGE; not adjacent partitions

-   範囲パーティションテーブルの場合、範囲の末尾を変更するには、 `VALUES LESS THAN`で定義された新しい末尾が、最後のパーティション内の既存の行をすべてカバーしている必要があります。そうでない場合、既存の行が範囲に収まらなくなり、エラーが報告されます。

    ```sql
    INSERT INTO members VALUES (313, "John", "Doe", "2022-11-22", NULL);
    ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2050)); -- This statement will work as expected, because 2050 covers the existing rows.
    ALTER TABLE members REORGANIZE PARTITION p2000 INTO (PARTITION p2000 VALUES LESS THAN (2020)); -- This statement will fail with an error, because 2022 does not fit in the new range.
    ```

        ERROR 1526 (HY000): Table has no partition for value 2022

-   リストパーティションテーブルの場合、パーティションに定義された値のセットを変更するには、新しい定義がそのパーティション内の既存の値を網羅している必要があります。そうでない場合は、エラーが報告されます。

    ```sql
    INSERT INTO member_level (id, level) values (313, 6);
    ALTER TABLE member_level REORGANIZE PARTITION lEven INTO (PARTITION lEven VALUES IN (2,4));
    ```

        ERROR 1526 (HY000): Table has no partition for value 6

-   パーティションの再編成後、対応するパーティションの統計情報は古くなっているため、次の警告が表示されます。この場合、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを使用して統計情報を更新できます。

    ```sql
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Level   | Code | Message                                                                                                                                                |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
    +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

### ハッシュとキーのパーティションを管理する {#manage-hash-and-key-partitions}

このセクションでは、次の SQL ステートメントで作成されたパーティションテーブルを例として、ハッシュ パーティションの管理方法を示します。キー パーティションについても、同じ管理ステートメントを使用できます。

```sql
CREATE TABLE example (
  id INT PRIMARY KEY,
  data VARCHAR(1024)
)
PARTITION BY HASH(id)
PARTITIONS 2;
```

#### パーティション数を増やす {#increase-the-number-of-partitions}

`example`テーブルのパーティション数を 1 増やします (2 から 3 へ)。

```sql
ALTER TABLE example ADD PARTITION PARTITIONS 1;
```

パーティション定義を追加することで、パーティションオプションを指定することもできます。たとえば、次のステートメントを使用して、パーティション数を 3 から 5 に増やし、新しく追加したパーティションの名前を`pExample4`および`pExample5`として指定できます。

```sql
ALTER TABLE example ADD PARTITION
(PARTITION pExample4 COMMENT = 'not p3, but pExample4 instead',
 PARTITION pExample5 COMMENT = 'not p4, but pExample5 instead');
```

#### パーティション数を減らす {#decrease-the-number-of-partitions}

範囲パーティショニングやList パーティショニングとは異なり、 `DROP PARTITION`はハッシュパーティショニングやキーパーティショニングではサポートされていませんが、 `COALESCE PARTITION`を使用してパーティション数を減らしたり、 `TRUNCATE PARTITION`を使用して特定のパーティションからすべてのデータを削除したりすることは可能です。

`example`テーブルのパーティション数を 1 減らします (5 から 4 へ)。

```sql
ALTER TABLE example COALESCE PARTITION 1;
```

> **Note:**
>
> ハッシュまたはキーでパーティション分割されたテーブルのパーティション数を変更すると、すべてのデータが新しいパーティション数にコピーされてパーティションが再編成されます。そのため、ハッシュまたはキーでパーティションテーブルのパーティション数を変更した後、統計情報が古いという警告が表示されます。この場合、 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ステートメントを使用して統計情報を更新できます。
>
> ```sql
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Level   | Code | Message                                                                                                                                                |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Warning | 1105 | The statistics of related partitions will be outdated after reorganizing partitions. Please use 'ANALYZE TABLE' statement if you want to update it now |
> +---------+------+--------------------------------------------------------------------------------------------------------------------------------------------------------+
> 1 row in set (0.00 sec)
> ```

`example`テーブルの構成をよりよく理解するために、 `example`テーブルを再作成するために使用される SQL ステートメントを次のように表示できます。

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

#### パーティションを切り詰める {#truncate-partitions}

パーティションからすべてのデータを削除する：

```sql
ALTER TABLE example TRUNCATE PARTITION p0;
```

    Query OK, 0 rows affected (0.03 sec)

### パーティションテーブルをパーティションテーブルに変換する {#convert-a-partitioned-table-to-a-non-partitioned-table}

パーティションテーブルをパーティションテーブルに変換するには、次のステートメントを使用できます。このステートメントは、パーティション化を削除し、テーブルのすべての行をコピーし、テーブルのインデックスをオンラインで再作成します。

```sql
ALTER TABLE <table_name> REMOVE PARTITIONING
```

例えば、 `members`パーティションテーブルを非パーティションテーブルに変換するには、次のステートメントを実行します。

```sql
ALTER TABLE members REMOVE PARTITIONING
```

### 既存のテーブルをパーティション分割する {#partition-an-existing-table}

既存の非パーティションテーブルをパーティション化したり、既存のパーティションテーブルのパーティションタイプを変更したりするには、次のステートメントを使用できます。このステートメントは、すべての行をコピーし、新しいパーティション定義に従ってインデックスをオンラインで再作成します。

```sql
ALTER TABLE <table_name> PARTITION BY <new partition type and definitions> [UPDATE INDEXES (<index name> {GLOBAL|LOCAL}[ , <index name> {GLOBAL|LOCAL}...])]
```

例：

既存の`members`テーブルを 10 個のパーティションを持つハッシュパーティションテーブルに変換するには、次のステートメントを実行します。

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

パーティション化パーティションテーブルをパーティション化する場合、またはすでにパーティションテーブルを再パーティション化する場合、必要に応じてインデックスを[グローバルインデックス](/global-indexes.md)インデックスまたはローカル インデックスに更新できます。

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

## パーティション剪定 {#partition-pruning}

[パーティション剪定](/partition-pruning.md)、一致しないパーティションをスキャンしないという非常に単純なアイデアに基づいた最適化です。

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

`SELECT`ステートメントの結果を取得したい場合は、次の手順に従ってください。

```sql
SELECT fname, lname, region_code, dob
    FROM t1
    WHERE region_code > 125 AND region_code < 130;
```

結果は`p1`または`p2`パーティションのいずれかに該当することは明らかです。つまり、 `p1`と`p2`で一致する行を検索するだけで済みます。不要なパーティションを除外することを「プルーニング」と呼びます。オプティマイザがパーティションの一部をプルーニングできる場合、パーティションテーブルでのクエリの実行は、パーティションテーブルでの実行よりもはるかに高速になります。

オプティマイザは、次の 2 つのシナリオにおいて`WHERE`条件に基づいてパーティションを剪定することができます。

-   パーティション列 = 定数
-   partition_column IN (constant1, constant2, ..., constantN)

現在、パーティションプルーニングは`LIKE`条件では機能しません。

### パーティション剪定が有効なケース {#some-cases-for-partition-pruning-to-take-effect}

1.  パーティションプルーニングは、パーティションテーブル上のクエリ条件を使用するため、プランナーの最適化ルールに従ってクエリ条件をパーティションテーブルにプッシュダウンできない場合、このクエリにはパーティションプルーニングは適用されません。

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

    このクエリでは、除外結合が内部結合に変換され、 `t1.x > 5`と`t1.x = t2.x`から`t2.x > 5`が導出されるため、パーティションプルーニングに使用でき、パーティション`p1`のみが残ります。

    ```sql
    explain select * from t1 left join t2 on t1.x = t2.x and t2.x > 5;
    ```

    このクエリでは、 `t2.x > 5` `t1`パーティションテーブルにプッシュダウンできないため、このクエリに対してパーティション プルーニングは適用されません。

2.  パーティションプルーニングはプラン最適化フェーズで行われるため、フィルタ条件が実行フェーズまで不明な場合には適用されません。

    例えば：

    ```sql
    create table t1 (x int) partition by range (x) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    ```

    ```sql
    explain select * from t2 where x < (select * from t1 where t2.x < t1.x and t2.x < 2);
    ```

    このクエリは`t2`から行を読み取り、その結果を`t1`のサブクエリに使用します。理論的には、サブクエリ内の`t1.x > val`式によってパーティションプルーニングのメリットが得られる可能性がありますが、実行フェーズで発生するため、ここでは効果がありません。

3.  現在の実装上の制限により、クエリ条件をTiKVにプッシュダウンできない場合、パーティションプルーニングで使用できません。

    `fn(col)`式を例にとってみましょう。TiKV コプロセッサがこの`fn`関数をサポートしている場合、計画最適化フェーズ中に述語プッシュダウンルールに従って`fn(col)`リーフノード (つまり、パーティションテーブル) にプッシュダウンされ、パーティション剪定に使用できます。

    TiKVコプロセッサがこの`fn`関数をサポートしていない場合、 `fn(col)`はリーフノードにプッシュダウンされません。代わりに、リーフノードの上位にある`Selection`ノードになります。現在のパーティション剪定の実装では、このようなプランツリーはサポートされていません。

4.  ハッシュおよびキーのパーティションタイプの場合、パーティションプルーニングでサポートされるクエリは、等しい条件のみです。

5.  範囲パーティションの場合、パーティション剪定を有効にするには、パーティション式が`col`または`fn(col)`の形式である必要があり、クエリ条件は`>` 、 `<` 、 `=` 、 `>=` } 、および`<=`のいずれかである必要があります。パーティション式が`fn(col)`の形式の場合、 `fn`関数は単調である必要があります。

    `fn`関数が単調である場合、任意の`x`および`y`に対して、 `x > y`ならば`fn(x) > fn(y)`となります。この`fn`関数は厳密に単調であると言えます。任意の`x`および`y`に対して、 `x > y`ならば`fn(x) >= fn(y)`となります。この場合、 `fn`は「単調」とも呼ばれます。理論的には、すべての単調関数はパーティション剪定によってサポートされます。

    現在、TiDBのパーティションプルーニングは、以下の単調関数のみをサポートしています。

    -   [`UNIX_TIMESTAMP()`](/functions-and-operators/date-and-time-functions.md)
    -   [`TO_DAYS()`](/functions-and-operators/date-and-time-functions.md)
    -   [`EXTRACT(&#x3C;time unit> FROM &#x3C;DATETIME/DATE/TIME column>)`](/functions-and-operators/date-and-time-functions.md) 。 `DATE`列と`DATETIME`列の場合、 `YEAR`と`YEAR_MONTH`時間単位は単調関数とみなされます。 `TIME`列の場合、 `HOUR` 、 `HOUR_MINUTE` 、 `HOUR_SECOND`および`HOUR_MICROSECOND`は単調関数とみなされます。 `WEEK`は、 `EXTRACT`におけるパーティション剪定の時間単位としてサポートされていないことに注意してください。

    例えば、パーティション式は単純な列です。

    ```sql
    create table t (id int) partition by range (id) (
            partition p0 values less than (5),
            partition p1 values less than (10));
    select * from t where id > 6;
    ```

    または、分割式は`fn(col)`の形式で`fn`は`to_days`です。

    ```sql
    create table t (dt datetime) partition by range (to_days(id)) (
            partition p0 values less than (to_days('2020-04-01')),
            partition p1 values less than (to_days('2020-05-01')));
    select * from t where dt > '2020-04-18';
    ```

    例外として、パーティション式として`floor(unix_timestamp())`が挙げられます。TiDB はケースバイケースで最適化を行うため、パーティションプルーニングでサポートされます。

    ```sql
    create table t (ts timestamp(3) not null default current_timestamp(3))
    partition by range (floor(unix_timestamp(ts))) (
            partition p0 values less than (unix_timestamp('2020-04-01 00:00:00')),
            partition p1 values less than (unix_timestamp('2020-05-01 00:00:00')));
    select * from t where ts > '2020-04-18 02:00:42.123';
    ```

## パーティション選択 {#partition-selection}

`SELECT`ステートメントは、 `PARTITION`オプションを使用することで実装されるパーティション選択をサポートします。

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

複数のパーティションの行を取得する場合は、カンマで区切られたパーティション名のリストを使用できます。たとえば、 `SELECT * FROM employees PARTITION (p1, p2)`は`p1`と`p2`のパーティション内のすべての行を返します。

パーティション選択を使用する場合でも、 `WHERE`条件や、 `ORDER BY`や`LIMIT`などのオプションを使用できます。また、 `HAVING`や`GROUP BY`などの集約オプションもサポートされています。

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

パーティション選択は、範囲パーティショニングやハッシュパーティショニングを含む、すべてのタイプのテーブルパーティショニングでサポートされています。ハッシュパーティションの場合、パーティション名が指定されていないときは、 `p0` 、 `p1` 、 `p2` 、...、または`pN-1`がパーティション名として自動的に使用されます。

`SELECT`内の`INSERT ... SELECT`もパーティション選択を使用できます。

## パーティションに関する制限事項 {#restrictions-and-limitations-on-partitions}

このセクションでは、TiDBにおけるパーティションテーブルに関するいくつかの制限事項と制約事項について説明します。

-   [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)ステートメントを使用してパーティション テーブルの列の型を変更することはサポートされていません。
-   [`ALTER TABLE ... CACHE`](/cached-tables.md)ステートメントを使用してパーティションテーブルをキャッシュテーブルに設定することはサポートされていません。
-   TiDB の[一時テーブル](/temporary-tables.md)パーティション化されたテーブルと互換性**がありません**。
-   パーティションテーブルでの[外部キー](/foreign-key.md)の作成はサポートされていません。
-   [`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`](/optimizer-hints.md#order_indext1_name-idx1_name--idx2_name-)ヒントは、パーティション化されたテーブルとその関連インデックスには機能しません。パーティション化されたテーブルのインデックスは順番に読み取ることができないためです。

### パーティショニングキー、主キー、一意キー {#partitioning-keys-primary-keys-and-unique-keys}

このセクションでは、パーティショニングキーと主キーおよび一意キーの関係について説明します。この関係を規定するルールは次のとおりです。主キーは定義上一意キーでもあるため、主キーを含むパーティションテーブル上のすべての一意キーは、テーブルのパーティショニング式内のすべての列を使用する必要があります。

> **Note:**
>
> [グローバルインデックス](/global-indexes.md)を使用する場合、このルールは無視できます。

例えば、以下のテーブル作成ステートメントは無効です。

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

いずれの場合も、提案されたテーブルには、パーティショニング式で使用されているすべての列を含まない一意のキーが少なくとも1つ存在します。

有効な記述は以下のとおりです。

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

`CREATE TABLE`ステートメントは、 `col1`と`col3`の両方が提案されたパーティショニングキーに含まれているにもかかわらず、これらの列のどちらもテーブル上の一意キーに含まれていないため、失敗します。以下の変更を加えると、 `CREATE TABLE`ステートメントが有効になります。

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

以下の表は、パーティションキーに両方の固有キーに属する列を含める方法がないため、パーティション分割を一切行うことができません。

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

主キーは定義上一意のキーであるため、次の2つの記述は無効です。

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

上記の例では、主キーにパーティショニング式で参照されているすべての列が含まれていません。主キーに不足している列を追加すると、 `CREATE TABLE`ステートメントが有効になります。

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

テーブルに一意キーも主キーも存在しない場合、この制限は適用されません。

DDL ステートメントを使用してテーブルを変更する場合、一意インデックスを追加する際にもこの制約を考慮する必要があります。たとえば、以下に示すようにパーティションテーブルを作成する場合です。

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

`ALTER TABLE`ステートメントを使用すると、一意でないインデックスを追加できます。ただし、一意インデックスを追加する場合は、 `c1`列を一意インデックスに含める必要があります。

パーティションテーブルを使用する場合、プレフィックスインデックスを一意属性として指定することはできません。

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

グローバル インデックスの詳細については、[グローバルインデックス](/global-indexes.md)を参照してください。

### 関数に関連する分割制限 {#partitioning-limitations-relating-to-functions}

分割式で使用できる関数は、以下のリストに示されているもののみです。

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

現在、TiDBは範囲パーティショニング、範囲列パーティショニング、List パーティショニング、List COLUMNS パーティショニング、ハッシュパーティショニング、およびキーパーティショニングをサポートしています。MySQLで利用可能なその他のパーティショニングタイプは、TiDBではまだサポートされていません。

サポートされていないパーティショニングタイプの場合、TiDBでテーブルを作成する際にパーティショニング情報は無視され、警告が報告された上で通常の形式でテーブルが作成されます。

現在、TiDB では`LOAD DATA`構文はパーティション選択をサポートしていません。

```sql
create table t (id int, val int) partition by hash(id) partitions 4;
```

通常の`LOAD DATA`操作がサポートされています。

```sql
load local data infile "xxx" into t ...
```

しかし、 `Load Data`はパーティション選択をサポートしていません。

```sql
load local data infile "xxx" into t partition (p1)...
```

パーティションテーブルの場合、 `select * from t`によって返される結果は、パーティション間では順序付けされていません。これは、パーティション間では順序付けされているものの、パーティション内では順序付けされていない MySQL の結果とは異なります。

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

TiDBは毎回異なる結果を返します。例えば、次のようになります。

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

MySQLで返された結果：

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

TiDB は、 `dynamic`または`static`モードでパーティションテーブルにアクセスします。 v6.3.0 以降、 `dynamic`モードがデフォルトで使用されます。ただし、動的パーティショニングは、完全なテーブルレベルの統計、つまりグローバル統計が収集された後にのみ有効になります。グローバル統計の収集が完了する前に`dynamic`プルーニング モードを有効にすると、TiDB はグローバル統計が完全に収集されるまで`static`モードのままになります。グローバル統計の詳細については、 [動的プルーニングモードでパーティションテーブルの統計情報を収集する](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。

```sql
set @@session.tidb_partition_prune_mode = 'dynamic'
```

手動の ANALYZE および通常のクエリでは、セッション レベルの`tidb_partition_prune_mode`設定が使用されます。バックグラウンドでの`auto-analyze`操作では、グローバルな`tidb_partition_prune_mode`設定が使用されます。

`static`モードでは、パーティション テーブルはパーティション レベルの統計情報を使用します。 `dynamic`モードでは、パーティション テーブルはテーブル レベルのグローバル統計情報を使用します。

`static`モードから`dynamic`モードに切り替える際は、統計情報を手動で確認して収集する必要があります。これは、 `dynamic`モードに切り替えた後、パーティション化されたテーブルにはパーティションレベルの統計情報のみが存在し、テーブルレベルの統計情報は存在しないためです。グローバル統計情報は、次の`auto-analyze`操作時にのみ収集されます。

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

グローバルな`dynamic`プルーニングモードを有効にした後、SQLステートメントで使用される統計情報が正しいことを確認するには、テーブルまたはテーブルのパーティションで`analyze`手動でトリガーして、グローバル統計情報を取得する必要があります。

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

`analyze`処理中に次の警告が表示された場合、パーティション統計に矛盾があるため、これらのパーティションまたはテーブル全体の統計を再度収集する必要があります。

    | Warning | 8244 | Build table: `t` column: `a` global-level stats failed due to missing partition-level column stats, please run analyze table to refresh columns of all partitions

スクリプトを使用して、すべてのパーティション化されたテーブルの統計を更新することもできます。詳細については、 [動的プルーニングモードでパーティションテーブルの統計情報を更新する](#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode)参照してください。

テーブルレベルの統計情報が準備できたら、グローバルな動的プルーニング モードを有効にできます。これは、すべての SQL ステートメントと`auto-analyze`操作に有効です。

```sql
set global tidb_partition_prune_mode = dynamic
```

`static`モードでは、TiDB は複数の演算子を使用して各パーティションに個別にアクセスし、 `Union`を使用して結果をマージします。次の例は、TiDB が`Union`を使用して対応する 2 つのパーティションの結果をマージする単純な読み取り操作です。

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

`dynamic`モードでは、各オペレーターが複数のパーティションへの直接アクセスをサポートしているため、TiDB は`Union`を使用しなくなりました。

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

上記のクエリ結果から、パーティションプルーニングがまだ有効であるにもかかわらず、実行プラン内の`Union`オペレーターが消え、実行プランは`p0`と`p1`のみにアクセスすることがわかります。

`dynamic`モードでは、実行プランがよりシンプルかつ明確になります。Union 演算を省略することで、実行効率が向上し、Union の同時実行の問題を回避できます。さらに、 `dynamic`モードでは`static`モードでは使用できない IndexJoin を使用した実行プランも可能です。（以下の例を参照）

**例 1** : 次の例では、IndexJoin を使用した実行プランを使用して`static`モードでクエリが実行されます。

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

例1からわかるように、 `TIDB_INLJ`ヒントを使用しても、パーティションテーブルに対するクエリはIndexJoinを使用した実行プランを選択できません。

**例 2** : 次の例では、IndexJoin を使用した実行プランを使用して`dynamic`モードでクエリが実行されます。

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

例2から、 `dynamic`モードでは、クエリを実行するとIndexJoinを使用した実行プランが選択されることがわかります。

現在、 `static`プルーニング モードは、プリペアドステートメントと非プリペアドステートメントの両方のプラン キャッシュをサポートしていません。

### 動的プルーニングモードでパーティションテーブルの統計情報を更新する {#update-statistics-of-partitioned-tables-in-dynamic-pruning-mode}

1.  パーティション化されたテーブルをすべて特定します。

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

2.  すべてのパーティションテーブルの統計情報を更新するためのステートメントを生成します。

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

    `ALL COLUMNS`を必要な列に変更できます。

3.  バッチ更新ステートメントをファイルにエクスポートします。

    ```shell
    mysql --host xxxx --port xxxx -u root -p -e "SELECT DISTINCT CONCAT('ANALYZE TABLE ',TABLE_SCHEMA,'.',TABLE_NAME,' ALL COLUMNS;') \
        FROM information_schema.PARTITIONS \
        WHERE TIDB_PARTITION_ID IS NOT NULL \
        AND TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA','mysql','sys','PERFORMANCE_SCHEMA','METRICS_SCHEMA');" | tee gatherGlobalStats.sql
    ```

4.  バッチ更新を実行する：

    `source`コマンドを実行する前に、SQL ステートメントを処理してください。

        sed -i "" '1d' gatherGlobalStats.sql --- mac
        sed -i '1d' gatherGlobalStats.sql --- linux

    ```sql
    SET session tidb_partition_prune_mode = dynamic;
    source gatherGlobalStats.sql
    ```

## 関連リソース {#related-resources}

<RelatedResources>
  <ResourceCard title="TiDB SQL Tuning Lab 2: Partitioned Tables" type="lab" link="https://labs.tidb.io/labs/dba_307_lab_ff1" imgSrc="https://lab-static.pingcap.com/quick-demo/307-02.png" duration="90 mins" />
</RelatedResources>
