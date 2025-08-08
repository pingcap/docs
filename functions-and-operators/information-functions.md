---
title: Information Functions
summary: 情報関数について学習します。
---

# 情報機能 {#information-functions}

TiDB は、MySQL 8.0 で利用可能な[情報関数](https://dev.mysql.com/doc/refman/8.0/en/information-functions.html)ほとんどをサポートしています。

## TiDB がサポートする MySQL関数 {#tidb-supported-mysql-functions}

| 名前                                                 | 説明                                            |
| :------------------------------------------------- | :-------------------------------------------- |
| [`BENCHMARK()`](#benchmark)                        | ループ内で式を実行する                                   |
| [`CONNECTION_ID()`](#connection_id)                | 接続の接続ID（スレッドID）を返します                          |
| [`CURRENT_ROLE()`](#current_role)                  | 接続で使用されているロールを返します                            |
| [`CURRENT_USER()` 、 `CURRENT_USER`](#current_user) | 認証されたユーザー名とホスト名を返す                            |
| [`DATABASE()`](#database)                          | デフォルト（現在の）データベース名を返す                          |
| [`FOUND_ROWS()`](#found_rows)                      | `LIMIT`節を持つ`SELECT`の場合、 `LIMIT`節がない場合に返される行の数 |
| [`LAST_INSERT_ID()`](#last_insert_id)              | 最後の`INSERT`列の`AUTOINCREMENT`番目の値を返す           |
| [`ROW_COUNT()`](#row_count)                        | 影響を受ける行数                                      |
| [`SCHEMA()`](#schema)                              | `DATABASE()`の同義語                              |
| [`SESSION_USER()`](#session_user)                  | `USER()`の同義語                                  |
| [`SYSTEM_USER()`](#system_user)                    | `USER()`の同義語                                  |
| [`USER()`](#user)                                  | クライアントから提供されたユーザー名とホスト名を返します                  |
| [`VERSION()`](#version)                            | MySQLサーバーのバージョンを示す文字列を返します                    |

### ベンチマーク（） {#benchmark}

`BENCHMARK()`関数は、指定された回数、指定された式を実行します。

構文：

```sql
BENCHMARK(count, expression)
```

-   `count` : 式を実行する回数。
-   `expression` : 繰り返し実行される式。

例：

```sql
SELECT BENCHMARK(5, SLEEP(2));
```

    +------------------------+
    | BENCHMARK(5, SLEEP(2)) |
    +------------------------+
    |                      0 |
    +------------------------+
    1 row in set (10.00 sec)

### 接続ID() {#connection-id}

<CustomContent platform="tidb">

`CONNECTION_ID()`関数は接続IDを返します。TiDBの[`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730)設定項目の値に基づいて、この関数は32ビットまたは64ビットの接続IDを返します。

[`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)が有効になっている場合、接続 ID を使用して、同じクラスターの複数の TiDB インスタンス間でクエリを強制終了できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

`CONNECTION_ID()`関数は接続IDを返します。TiDBの[`enable-32bits-connection-id`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-32bits-connection-id-new-in-v730)設定項目の値に基づいて、この関数は32ビットまたは64ビットの接続IDを返します。

[`enable-global-kill`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#enable-global-kill-new-in-v610)が有効になっている場合、接続 ID を使用して、同じクラスターの複数の TiDB インスタンス間でクエリを強制終了できます。

</CustomContent>

```sql
SELECT CONNECTION_ID();
```

    +-----------------+
    | CONNECTION_ID() |
    +-----------------+
    |       322961414 |
    +-----------------+
    1 row in set (0.00 sec)

### 現在のロール() {#current-role}

<CustomContent platform="tidb">

`CURRENT_ROLE()`関数は、現在のセッションの現在の[役割](/role-based-access-control.md)返します。

</CustomContent>

<CustomContent platform="tidb-cloud">

`CURRENT_ROLE()`関数は、現在のセッションの現在の[役割](https://docs.pingcap.com/tidb/stable/role-based-access-control)返します。

</CustomContent>

```sql
SELECT CURRENT_ROLE();
```

    +----------------+
    | CURRENT_ROLE() |
    +----------------+
    | NONE           |
    +----------------+
    1 row in set (0.00 sec)

### 現在のユーザー() {#current-user}

`CURRENT_USER()`関数は、現在のセッションで使用されているアカウントを返します。

```sql
SELECT CURRENT_USER();
```

    +----------------+
    | CURRENT_USER() |
    +----------------+
    | root@%         |
    +----------------+
    1 row in set (0.00 sec)

### データベース() {#database}

`DATABASE()`関数は、現在のセッションで使用されているデータベース スキーマを返します。

```sql
SELECT DATABASE();
```

    +------------+
    | DATABASE() |
    +------------+
    | test       |
    +------------+
    1 row in set (0.00 sec)

### 見つかった行() {#found-rows}

`FOUND_ROWS()`関数は、最後に実行された`SELECT`ステートメントの結果セット内の行数を返します。

```sql
SELECT 1 UNION ALL SELECT 2;
```

    +------+
    | 1    |
    +------+
    |    2 |
    |    1 |
    +------+
    2 rows in set (0.01 sec)

```sql
SELECT FOUND_ROWS();
```

    +--------------+
    | FOUND_ROWS() |
    +--------------+
    |            2 |
    +--------------+
    1 row in set (0.00 sec)

> **注記：**
>
> クエリ修飾子`SQL_CALC_FOUND_ROWS` 、クエリ修飾子`LIMIT`を考慮せずに結果セットの合計行数を計算しますが、クエリ修飾子[`tidb_enable_noop_functions`](/system-variables.md#tidb_enable_noop_functions-new-in-v40)有効な場合にのみ使用できます。このクエリ修飾子は、MySQL 8.0.17 以降では非推奨です。代わりにクエリ修飾子`COUNT(*)`使用することをお勧めします。

### 最終挿入ID() {#last-insert-id}

`LAST_INSERT_ID()`関数は、 [`AUTO_INCREMENT`](/auto-increment.md)または[`AUTO_RANDOM`](/auto-random.md)列を含むテーブルに最後に挿入された行の ID を返します。

```sql
CREATE TABLE t1(id SERIAL);
Query OK, 0 rows affected (0.17 sec)

INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.03 sec)

INSERT INTO t1() VALUES();
Query OK, 1 row affected (0.00 sec)

SELECT LAST_INSERT_ID();
+------------------+
| LAST_INSERT_ID() |
+------------------+
|                3 |
+------------------+
1 row in set (0.00 sec)

TABLE t1;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

> **注記**
>
> -   TiDBでは、 [`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache)指定するとMySQLが返す結果と異なる結果になる可能性があります。この不一致は、TiDBが各ノードにIDをキャッシュするため、IDの順序が乱れたり、IDに空白が生じたりする可能性があるためです。アプリケーションで厳密なID順序の維持が不可欠な場合は、 [MySQL互換モード](/auto-increment.md#mysql-compatibility-mode)有効にすることができます。
>
> -   上の例ではIDが2ずつ増加しますが、MySQLでは同じシナリオでIDが1ずつ増加します。互換性に関する詳細は[自動増分ID](/mysql-compatibility.md#auto-increment-id)参照してください。

`LAST_INSERT_ID(expr)`関数は式を引数として受け取り、その値を`LAST_INSERT_ID()`次回呼び出し時に保存します。MySQL互換のシーケンス生成メソッドとして使用できます。TiDBは[シーケンス関数](/functions-and-operators/sequence-functions.md)もサポートしています。

### ROW_COUNT() {#row-count}

`ROW_COUNT()`関数は影響を受ける行の数を返します。

```sql
CREATE TABLE t1(id BIGINT UNSIGNED PRIMARY KEY AUTO_RANDOM);
Query OK, 0 rows affected, 1 warning (0.16 sec)

INSERT INTO t1() VALUES (),(),();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

SELECT ROW_COUNT();
+-------------+
| ROW_COUNT() |
+-------------+
|           3 |
+-------------+
1 row in set (0.00 sec)
```

### スキーマ() {#schema}

`SCHEMA()`関数は[`DATABASE()`](#database)の同義語です。

### セッションユーザー() {#session-user}

`SESSION_USER()`関数は[`USER()`](#user)の同義語です。

### SYSTEM_USER() {#system-user}

`SYSTEM_USER()`関数は[`USER()`](#user)の同義語です。

### ユーザー（） {#user}

`USER()`関数は現在の接続のユーザーを返します。5 `USER()`ワイルドカードではなく実際のIPアドレスを表示するため、 `CURRENT_USER()`の出力とは若干異なる場合があります。

```sql
SELECT USER(), CURRENT_USER();
```

    +----------------+----------------+
    | USER()         | CURRENT_USER() |
    +----------------+----------------+
    | root@127.0.0.1 | root@%         |
    +----------------+----------------+
    1 row in set (0.00 sec)

### バージョン() {#version}

`VERSION()`関数は、MySQLと互換性のある形式でTiDBのバージョンを返します。より詳細な結果を取得するには、 [`TIDB_VERSION()`](/functions-and-operators/tidb-functions.md#tidb_version)関数を使用します。

```sql
SELECT VERSION();
+--------------------+
| VERSION()          |
+--------------------+
| 8.0.11-TiDB-v7.5.1 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_VERSION()\G
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v7.5.1
Edition: Community
Git Commit Hash: 7d16cc79e81bbf573124df3fd9351c26963f3e70
Git Branch: heads/refs/tags/v7.5.1
UTC Build Time: 2024-02-27 14:28:32
GoVersion: go1.21.6
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

上記の例は、MySQL 8.0.11 として識別される TiDB v7.5.1 からのものです。

<CustomContent platform="tidb">

返されるバージョンを変更する場合は、 [`server-version`](/tidb-configuration-file.md#server-version)構成項目を変更できます。

</CustomContent>

## TiDB固有の関数 {#tidb-specific-functions}

次の関数は TiDB でのみサポートされており、MySQL には同等の関数はありません。

| 名前                                                                                              | 説明                                  |
| :---------------------------------------------------------------------------------------------- | :---------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](/functions-and-operators/tidb-functions.md#current_resource_group) | 現在のセッションがバインドされているリソース グループの名前を返します |

## サポートされていない関数 {#unsupported-functions}

-   `CHARSET()`
-   `COERCIBILITY()`
-   `COLLATION()`
-   `ICU_VERSION()`
-   `ROLES_GRAPHML()`
