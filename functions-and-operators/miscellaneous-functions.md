---
title: Miscellaneous Functions
summary: TiDBの様々な関数について学びましょう。
---

# その他の機能 {#miscellaneous-functions}

TiDB は、MySQL 8.0 で利用可能な[その他の関数](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html)のほとんどをサポートしています。

## サポートされている関数 {#supported-functions}

| 名前                                    | 説明                                                                                                                                                                                                                                                                         |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ANY_VALUE()`](#any_value)           | `ONLY_FULL_GROUP_BY`値の拒否を抑制します                                                                                                                                                                                                                                             |
| [`BIN_TO_UUID()`](#bin_to_uuid)       | UUIDをバイナリ形式からテキスト形式に変換する                                                                                                                                                                                                                                                   |
| [`DEFAULT()`](#default)               | テーブル列のデフォルト値を返します                                                                                                                                                                                                                                                          |
| [`GROUPING()`](#grouping)             | `GROUP BY`操作の修飾子                                                                                                                                                                                                                                                           |
| [`INET_ATON()`](#inet_aton)           | IPアドレスの数値を返します                                                                                                                                                                                                                                                             |
| [`INET_NTOA()`](#inet_ntoa)           | 数値からIPアドレスを返します                                                                                                                                                                                                                                                            |
| [`INET6_ATON()`](#inet6_aton)         | IPv6アドレスの数値を返します                                                                                                                                                                                                                                                           |
| [`INET6_NTOA()`](#inet6_ntoa)         | 数値からIPv6アドレスを返します                                                                                                                                                                                                                                                          |
| [`IS_IPV4()`](#is_ipv4)               | 引数が IPv4 アドレスかどうか                                                                                                                                                                                                                                                          |
| [`IS_IPV4_COMPAT()`](#is_ipv4_compat) | 引数が IPv4 互換アドレスであるかどうか                                                                                                                                                                                                                                                     |
| [`IS_IPV4_MAPPED()`](#is_ipv4_mapped) | 引数が IPv4 マップド アドレスであるかどうか                                                                                                                                                                                                                                                  |
| [`IS_IPV6()`](#is_ipv6)               | 引数が IPv6 アドレスかどうか                                                                                                                                                                                                                                                          |
| [`IS_UUID()`](#is_uuid)               | 引数がUUIDかどうか                                                                                                                                                                                                                                                                |
| [`NAME_CONST()`](#name_const)         | 列名を変更するために使用できます                                                                                                                                                                                                                                                           |
| [`SLEEP()`](#sleep)                   | 指定された秒数だけスリープします。TiDB [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスの場合、 `SLEEP()`関数には制限があり、最大スリープ時間は 300 秒までしかサポートされないことに注意してください。 |
| [`UUID()`](#uuid)                     | ユニバーサル一意識別子（UUID）を返します。                                                                                                                                                                                                                                                    |
| [`UUID_TO_BIN()`](#uuid_to_bin)       | UUIDをテキスト形式からバイナリ形式に変換する                                                                                                                                                                                                                                                   |
| [`VALUES()`](#values)                 | INSERT時に使用される値を定義します                                                                                                                                                                                                                                                       |

### 任意の値() {#any-value}

`ANY_VALUE()`関数は、値のグループから任意の値を返します。通常、 `SELECT`ステートメントに集計されていない列を`GROUP BY`句とともに含める必要があるシナリオで使用されます。

```sql
CREATE TABLE fruits (id INT PRIMARY KEY, name VARCHAR(255));
Query OK, 0 rows affected (0.14 sec)

INSERT INTO fruits VALUES (1,'apple'),(2,'apple'),(3,'pear'),(4,'banana'),(5, 'pineapple');
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

SELECT id,name FROM fruits GROUP BY name;
ERROR 1055 (42000): Expression #1 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'test.fruits.id' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by

SELECT ANY_VALUE(id),GROUP_CONCAT(id),name FROM fruits GROUP BY name;
+---------------+------------------+-----------+
| ANY_VALUE(id) | GROUP_CONCAT(id) | name      |
+---------------+------------------+-----------+
|             1 | 1,2              | apple     |
|             3 | 3                | pear      |
|             4 | 4                | banana    |
|             5 | 5                | pineapple |
+---------------+------------------+-----------+
4 rows in set (0.00 sec)
```

前述の例では、 `SELECT`列が非集計列であり、 `id`句に含まれていないため、TiDB は最初の`GROUP BY`ステートメントに対してエラーを返します。この問題を解決するために、2 番目の`SELECT`クエリでは、 `ANY_VALUE()`を使用して各グループから任意の値を取得し、 `GROUP_CONCAT()`を使用して各グループ内の`id`列のすべての値を単一の文字列に連結します。この方法により、非集計列の SQL モードを変更することなく、各グループから 1 つの値とグループ内のすべての値を取得できます。

### BIN_TO_UUID() {#bin-to-uuid}

`BIN_TO_UUID()`と`UUID_TO_BIN()`は、テキスト形式の UUID とバイナリ形式の UUID を相互に変換するために使用できます。どちらの関数も 2 つの引数を受け取ります。

-   最初の引数は、変換する値を指定します。
-   2番目の引数（オプション）は、バイナリ形式におけるフィールドの順序を制御します。

```sql
SET @a := UUID();
Query OK, 0 rows affected (0.00 sec)

SELECT @a;
+--------------------------------------+
| @a                                   |
+--------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56 |
+--------------------------------------+
1 row in set (0.00 sec)

SELECT UUID_TO_BIN(@a);
+------------------------------------+
| UUID_TO_BIN(@a)                    |
+------------------------------------+
| 0x9A17B457EB6D11EEBACF5405DB7AAD56 |
+------------------------------------+
1 row in set (0.00 sec)

SELECT BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56);
+-------------------------------------------------+
| BIN_TO_UUID(0x9A17B457EB6D11EEBACF5405DB7AAD56) |
+-------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56            |
+-------------------------------------------------+
1 row in set (0.00 sec)

SELECT UUID_TO_BIN(@a, 1);
+----------------------------------------+
| UUID_TO_BIN(@a, 1)                     |
+----------------------------------------+
| 0x11EEEB6D9A17B457BACF5405DB7AAD56     |
+----------------------------------------+
1 row in set (0.00 sec)

SELECT BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1);
+----------------------------------------------------+
| BIN_TO_UUID(0x11EEEB6D9A17B457BACF5405DB7AAD56, 1) |
+----------------------------------------------------+
| 9a17b457-eb6d-11ee-bacf-5405db7aad56               |
+----------------------------------------------------+
1 row in set (0.00 sec)
```

[UUID()](#uuid)および[UUIDのベストプラクティス](/best-practices/uuid.md)も参照してください。

### デフォルト（） {#default}

`DEFAULT()`関数は、列のデフォルト値を取得するために使用されます。

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT DEFAULT 5);
Query OK, 0 rows affected (0.15 sec)

INSERT INTO t1 VALUES (1, 1);
Query OK, 1 row affected (0.01 sec)

UPDATE t1 SET c1=DEFAULT(c1)+3;
Query OK, 1 row affected (0.02 sec)
Rows matched: 1  Changed: 1  Warnings: 0

TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |    8 |
+----+------+
1 row in set (0.00 sec)
```

前述の例では、 `UPDATE`ステートメントは`c1`列の値を、列のデフォルト値 ( `5` ) に`3`を加えた値に設定し、結果として`8`という新しい値になります。

### グループ化() {#grouping}

[`GROUP BY`修飾子](/functions-and-operators/group-by-modifier.md)を参照してください。

### INET_ATON() {#inet-aton}

`INET_ATON()`関数は、ドット付き四分音符表記の IPv4 アドレスを、効率的に保存できるバイナリ バージョンに変換します。

```sql
SELECT INET_ATON('127.0.0.1');
```

    +------------------------+
    | INET_ATON('127.0.0.1') |
    +------------------------+
    |             2130706433 |
    +------------------------+
    1 row in set (0.00 sec)

### INET_NTOA() {#inet-ntoa}

`INET_NTOA()`関数は、バイナリ IPv4 アドレスをドット付き四角形表記に変換します。

```sql
SELECT INET_NTOA(2130706433);
```

    +-----------------------+
    | INET_NTOA(2130706433) |
    +-----------------------+
    | 127.0.0.1             |
    +-----------------------+
    1 row in set (0.00 sec)

### INET6_ATON() {#inet6-aton}

`INET6_ATON()`関数は[`INET_ATON()`](#inet_aton)と似ていますが、 `INET6_ATON()` IPv6 アドレスも処理できます。

```sql
SELECT INET6_ATON('::1');
```

    +--------------------------------------+
    | INET6_ATON('::1')                    |
    +--------------------------------------+
    | 0x00000000000000000000000000000001   |
    +--------------------------------------+
    1 row in set (0.00 sec)

### INET6_NTOA() {#inet6-ntoa}

`INET6_NTOA()`関数は[`INET_NTOA()`](#inet_ntoa)と似ていますが、 `INET6_NTOA()` IPv6 アドレスも処理できます。

```sql
SELECT INET6_NTOA(0x00000000000000000000000000000001);
```

    +------------------------------------------------+
    | INET6_NTOA(0x00000000000000000000000000000001) |
    +------------------------------------------------+
    | ::1                                            |
    +------------------------------------------------+
    1 row in set (0.00 sec)

### IS_IPV4() {#is-ipv4}

`IS_IPV4()`関数は、指定された引数が IPv4 アドレスであるかどうかをテストします。

```sql
SELECT IS_IPV4('127.0.0.1');
```

    +----------------------+
    | IS_IPV4('127.0.0.1') |
    +----------------------+
    |                    1 |
    +----------------------+
    1 row in set (0.00 sec)

```sql
SELECT IS_IPV4('300.0.0.1');
```

    +----------------------+
    | IS_IPV4('300.0.0.1') |
    +----------------------+
    |                    0 |
    +----------------------+
    1 row in set (0.00 sec)

### IS_IPV4_COMPAT() {#is-ipv4-compat}

`IS_IPV4_COMPAT()`関数は、指定された引数が IPv4 互換アドレスであるかどうかをテストします。

```sql
SELECT IS_IPV4_COMPAT(INET6_ATON('::127.0.0.1'));
```

    +-------------------------------------------+
    | IS_IPV4_COMPAT(INET6_ATON('::127.0.0.1')) |
    +-------------------------------------------+
    |                                         1 |
    +-------------------------------------------+
    1 row in set (0.00 sec)

### IS_IPV4_MAPPE() {#is-ipv4-mapped}

`IS_IPV4_MAPPED()`関数は、指定された引数が IPv4 マップド アドレスであるかどうかをテストします。

```sql
SELECT IS_IPV4_MAPPED(INET6_ATON('::ffff:127.0.0.1'));
```

    +------------------------------------------------+
    | IS_IPV4_MAPPED(INET6_ATON('::ffff:127.0.0.1')) |
    +------------------------------------------------+
    |                                              1 |
    +------------------------------------------------+
    1 row in set (0.00 sec)

### IS_IPV6() {#is-ipv6}

`IS_IPV6()`関数は、指定された引数が IPv6 アドレスであるかどうかをテストします。

```sql
SELECT IS_IPV6('::1');
```

    +----------------+
    | IS_IPV6('::1') |
    +----------------+
    |              1 |
    +----------------+
    1 row in set (0.00 sec)

### IS_UUID() {#is-uuid}

`IS_UUID()`関数は、指定された引数が[UUID](/best-practices/uuid.md)であるかどうかをテストします。

```sql
SELECT IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56');
```

    +-------------------------------------------------+
    | IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56') |
    +-------------------------------------------------+
    |                                               1 |
    +-------------------------------------------------+
    1 row in set (0.00 sec)

### NAME_CONST() {#name-const}

`NAME_CONST()`関数は列に名前を付けるために使用されます。代わりに列エイリアスを使用することをお勧めします。

```sql
SELECT NAME_CONST('column name', 'value') UNION ALL SELECT 'another value';
```

    +---------------+
    | column name   |
    +---------------+
    | another value |
    | value         |
    +---------------+
    2 rows in set (0.00 sec)

前述のステートメントでは`NAME_CONST()`を使用していますが、次のステートメントでは列のエイリアス付けに推奨される方法を使用しています。

```sql
SELECT 'value' AS 'column name' UNION ALL SELECT 'another value';
```

    +---------------+
    | column name   |
    +---------------+
    | value         |
    | another value |
    +---------------+
    2 rows in set (0.00 sec)

### 寝る（） {#sleep}

`SLEEP()`関数は、クエリの実行を指定された秒数だけ一時停止するために使用されます。

```sql
SELECT SLEEP(1.5);
```

    +------------+
    | SLEEP(1.5) |
    +------------+
    |          0 |
    +------------+
    1 row in set (1.50 sec)

### UUID() {#uuid}

`UUID()`関数は、 [RFC 4122](https://datatracker.ietf.org/doc/html/rfc4122)で定義されているユニバーサル一意識別子 (UUID) バージョン 1 を返します。

```sql
SELECT UUID();
```

    +--------------------------------------+
    | UUID()                               |
    +--------------------------------------+
    | cb4d5ae6-eb6b-11ee-bacf-5405db7aad56 |
    +--------------------------------------+
    1 row in set (0.00 sec)

[UUIDのベストプラクティス](/best-practices/uuid.md)も参照してください。

### UUIDからビンへ {#uuid-to-bin}

[BIN_TO_UUID()](#bin_to_uuid)を参照してください。

### 値() {#values}

`VALUES(col_name)`関数は、 [`INSERT`](/sql-statements/sql-statement-insert.md)ステートメントの`ON DUPLICATE KEY UPDATE`句で特定の列の値を参照するために使用されます。

```sql
CREATE TABLE t1 (id INT PRIMARY KEY, c1 INT);
Query OK, 0 rows affected (0.17 sec)

INSERT INTO t1 VALUES (1,51),(2,52),(3,53),(4,54),(5,55);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

INSERT INTO t1 VALUES(2,22),(4,44) ON DUPLICATE KEY UPDATE c1=VALUES(id)+100;
Query OK, 4 rows affected (0.01 sec)
Records: 2  Duplicates: 2  Warnings: 0

TABLE t1;
+----+------+
| id | c1   |
+----+------+
|  1 |   51 |
|  2 |  102 |
|  3 |   53 |
|  4 |  104 |
|  5 |   55 |
+----+------+
5 rows in set (0.00 sec)
```

## サポートされていない関数 {#unsupported-functions}

| 名前                                                                                                         | 説明                                                                                            |
| :--------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) | TiDBには存在しない特定の前提条件に基づいて一意のUUIDを提供します[TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |
