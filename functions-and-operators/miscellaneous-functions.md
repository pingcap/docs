---
title: Miscellaneous Functions
summary: TiDB のさまざまな関数について学習します。
---

# その他の機能 {#miscellaneous-functions}

TiDB は、MySQL 8.0 で利用可能な[その他の関数](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html)のほとんどをサポートしています。

## サポートされている関数 {#supported-functions}

| 名前                                    | 説明                                                                                                                                                                               |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`ANY_VALUE()`](#any_value)           | `ONLY_FULL_GROUP_BY`値を拒否しない                                                                                                                                                      |
| [`BIN_TO_UUID()`](#bin_to_uuid)       | UUIDをバイナリ形式からテキスト形式に変換する                                                                                                                                                         |
| [`DEFAULT()`](#default)               | テーブル列のデフォルト値を返します                                                                                                                                                                |
| [`GROUPING()`](#grouping)             | `GROUP BY`操作の修飾子                                                                                                                                                                 |
| [`INET_ATON()`](#inet_aton)           | IPアドレスの数値を返す                                                                                                                                                                     |
| [`INET_NTOA()`](#inet_ntoa)           | 数値からIPアドレスを返す                                                                                                                                                                    |
| [`INET6_ATON()`](#inet6_aton)         | IPv6アドレスの数値を返す                                                                                                                                                                   |
| [`INET6_NTOA()`](#inet6_ntoa)         | 数値から IPv6 アドレスを返します                                                                                                                                                              |
| [`IS_IPV4()`](#is_ipv4)               | 引数がIPv4アドレスかどうか                                                                                                                                                                  |
| [`IS_IPV4_COMPAT()`](#is_ipv4_compat) | 引数がIPv4互換アドレスであるかどうか                                                                                                                                                             |
| [`IS_IPV4_MAPPED()`](#is_ipv4_mapped) | 引数がIPv4マップアドレスであるかどうか                                                                                                                                                            |
| [`IS_IPV6()`](#is_ipv6)               | 引数がIPv6アドレスかどうか                                                                                                                                                                  |
| [`IS_UUID()`](#is_uuid)               | 引数がUUIDかどうか                                                                                                                                                                      |
| [`NAME_CONST()`](#name_const)         | 列名を変更するために使用できます                                                                                                                                                                 |
| [`SLEEP()`](#sleep)                   | 指定した秒数スリープします。1 クラスターの場合、 `SLEEP()`関数には最大 300 秒のスリープ時間しか[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)できないという制限があることに注意してください。 |
| [`UUID()`](#uuid)                     | ユニバーサルユニーク識別子 (UUID) を返す                                                                                                                                                         |
| [`UUID_TO_BIN()`](#uuid_to_bin)       | UUIDをテキスト形式からバイナリ形式に変換する                                                                                                                                                         |
| [`VALUES()`](#values)                 | INSERT中に使用される値を定義します                                                                                                                                                             |

### 任意の値() {#any-value}

`ANY_VALUE()`関数は、値のグループから任意の値を返します。通常、この関数は、 `GROUP BY`句とともに`SELECT`ステートメントに非集計列を含める必要があるシナリオで使用されます。

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

前の例では、列`id`が非集計であり、句`GROUP BY`に含まれていないため、TiDB は最初の`SELECT`ステートメントに対してエラーを返します。この問題に対処するために、2 番目の`SELECT`クエリは`ANY_VALUE()`使用して各グループから任意の値を取得し、 `GROUP_CONCAT()`使用して各グループ内の列`id`のすべての値を 1 つの文字列に連結します。このアプローチにより、非集計列の SQL モードを変更せずに、各グループから 1 つの値とグループのすべての値を取得できます。

### BIN_TO_UUID() {#bin-to-uuid}

`BIN_TO_UUID()`と`UUID_TO_BIN()`テキスト形式の UUID とバイナリ形式間の変換に使用できます。どちらの関数2 つの引数を受け入れます。

-   最初の引数は変換する値を指定します。
-   2 番目の引数 (オプション) は、バイナリ形式でのフィールドの順序を制御します。

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

[UUID()](#uuid)と[UUIDのベストプラクティス](/best-practices/uuid.md)も参照してください。

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

前の例では、 `UPDATE`ステートメントは`c1`列の値を列のデフォルト値 ( `5` ) に`3`を加えた値に設定し、新しい値は`8`になります。

### グループ化() {#grouping}

[`GROUP BY`修飾子](/functions-and-operators/group-by-modifier.md)参照。

### INET_ATON() {#inet-aton}

`INET_ATON()`関数は、ドット区切りの 4 進表記の IPv4 アドレスを、効率的に保存できるバイナリ バージョンに変換します。

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

`INET_NTOA()`関数は、バイナリ IPv4 アドレスをドット区切りの 4 つの表記に変換します。

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

`INET6_ATON()`機能は[`INET_ATON()`](#inet_aton)と似ていますが、 `INET6_ATON()` IPv6 アドレスも処理できます。

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

`INET6_NTOA()`機能は[`INET_NTOA()`](#inet_ntoa)と似ていますが、 `INET6_NTOA()` IPv6 アドレスも処理できます。

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

### IS_IPV4_MAPPED() {#is-ipv4-mapped}

`IS_IPV4_MAPPED()`関数は、指定された引数が IPv4 マップ アドレスであるかどうかをテストします。

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

`IS_UUID()`関数は、指定された引数が[言語](/best-practices/uuid.md)であるかどうかをテストします。

```sql
SELECT IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56');
```

    +-------------------------------------------------+
    | IS_UUID('eb48c08c-eb71-11ee-bacf-5405db7aad56') |
    +-------------------------------------------------+
    |                                               1 |
    +-------------------------------------------------+
    1 row in set (0.00 sec)

### 名前_CONST() {#name-const}

`NAME_CONST()`関数は列に名前を付けるために使用されます。代わりに列の別名を使用することをお勧めします。

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

前のステートメントでは`NAME_CONST()`使用され、次のステートメントでは列のエイリアスに推奨される方法が使用されます。

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

`SLEEP()`関数は、指定された秒数の間クエリの実行を一時停止するために使用されます。

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

### UUID_TO_BIN {#uuid-to-bin}

[BIN_TO_UUID()](#bin_to_uuid)参照。

### 値() {#values}

`VALUES(col_name)`関数は、 [`INSERT`](/sql-statements/sql-statement-insert.md)ステートメントの`ON DUPLICATE KEY UPDATE`句内の特定の列の値を参照するために使用されます。

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
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short) | TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620)には存在しない特定の仮定に基づいて一意のUUIDを提供します。 |
