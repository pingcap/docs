---
title: Temporary Tables
summary: Learn the temporary tables feature in TiDB, and learn how to use temporary tables to store intermediate data of an application, which helps reduce table management overhead and improve performance.
---

# 一時テーブル {#temporary-tables}

一時テーブル機能は、TiDB v5.3.0 で導入されました。この機能により、アプリケーションの中間結果を一時的に保管するという問題が解決され、頻繁にテーブルを作成および削除する必要がなくなります。中間計算データを一時テーブルに格納できます。中間データが不要になると、TiDB は一時テーブルを自動的にクリーンアップしてリサイクルします。これにより、ユーザー アプリケーションが複雑になりすぎず、テーブル管理のオーバーヘッドが削減され、パフォーマンスが向上します。

このドキュメントでは、ユーザー シナリオと一時テーブルの種類を紹介し、使用例と一時テーブルのメモリ使用量を制限する方法について説明し、他の TiDB 機能との互換性の制限について説明します。

## ユーザー シナリオ {#user-scenarios}

次のシナリオでは、TiDB 一時テーブルを使用できます。

-   アプリケーションの中間一時データをキャッシュします。計算が完了すると、データは通常のテーブルにダンプされ、一時テーブルは自動的に解放されます。
-   短期間に同じデータに対して複数の DML 操作を実行します。たとえば、e コマースのショッピング カート アプリケーションでは、商品の追加、変更、削除、支払いの完了、ショッピング カート情報の削除を行います。
-   中間一時データをバッチですばやくインポートして、一時データのインポートのパフォーマンスを向上させます。
-   バッチでデータを更新します。データベースの一時テーブルにデータを一括でインポートし、データの変更が完了したら、データをファイルにエクスポートします。

## 一時テーブルの種類 {#types-of-temporary-tables}

TiDB の一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの 2 種類に分けられます。

-   ローカル一時テーブルの場合、テーブルの定義とテーブル内のデータは、現在のセッションにのみ表示されます。このタイプは、セッション内の中間データを一時的に格納するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義は TiDB クラスター全体に表示され、テーブル内のデータは現在のトランザクションにのみ表示されます。このタイプは、トランザクションの中間データを一時的に格納するのに適しています。

## ローカル一時テーブル {#local-temporary-tables}

TiDB のローカル一時テーブルのセマンティクスは、MySQL 一時テーブルのセマンティクスと一致しています。特徴は次のとおりです。

-   ローカル一時テーブルのテーブル定義は永続的ではありません。ローカル一時テーブルは、テーブルが作成されたセッションにのみ表示され、他のセッションはテーブルにアクセスできません。
-   異なるセッションで同じ名前のローカル一時テーブルを作成できます。各セッションは、セッションで作成されたローカル一時テーブルに対してのみ読み取りと書き込みのみを行います。
-   ローカル一時テーブルのデータは、セッション内のすべてのトランザクションに表示されます。
-   セッションが終了すると、セッションで作成されたローカル一時テーブルは自動的に削除されます。
-   ローカル一時テーブルには、通常のテーブルと同じ名前を付けることができます。この場合、DDL および DML ステートメントでは、ローカル一時テーブルが削除されるまで、通常のテーブルは非表示になります。

ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLE`ステートメントを使用できます。ローカル一時テーブルを削除するには、 `DROP TABLE`または`DROP TEMPORARY TABLE`ステートメントを使用できます。

MySQL とは異なり、TiDB のローカル一時テーブルはすべて外部テーブルであり、SQL ステートメントの実行時に内部一時テーブルが自動的に作成されることはありません。

### ローカル一時テーブルの使用例 {#usage-examples-of-local-temporary-tables}

> **ノート：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)と[MySQL 一時テーブルとの互換性](#compatibility-with-mysql-temporary-tables)に注意してください。
> -   TiDB v5.3.0 より前のクラスターでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスターが TiDB v5.3.0 以降のバージョンにアップグレードされた後は通常のテーブルとして扱われます。

通常のテーブル`users`があるとします。

{{< copyable "" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

セッション A では、ローカル一時表の作成`users`通常の表と競合しません`users` 。セッション A が`users`テーブルにアクセスすると、ローカル一時テーブル`users`にアクセスします。

{{< copyable "" >}}

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

`users`にデータを挿入すると、データはセッション A のローカル一時テーブル`users`に挿入されます。

{{< copyable "" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

セッション B では、ローカル一時テーブル`users`の作成は、セッション A の通常テーブル`users`またはローカル一時テーブル`users`と競合しません。セッション B が`users`テーブルにアクセスすると、セッション B のローカル一時テーブル`users`にアクセスします。

{{< copyable "" >}}

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

`users`にデータを挿入すると、データはセッション B のローカル一時テーブル`users`に挿入されます。

{{< copyable "" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'James', 'NewYork');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+---------+
| id   | name  | city    |
+------+-------+---------+
| 1001 | James | NewYork |
+------+-------+---------+
1 row in set (0.00 sec)
```

### MySQL 一時テーブルとの互換性 {#compatibility-with-mysql-temporary-tables}

TiDB ローカル一時テーブルの次の機能と制限は、MySQL 一時テーブルと同じです。

-   ローカル一時テーブルを作成または削除すると、現在のトランザクションは自動的にコミットされません。
-   ローカル一時テーブルが配置されているスキーマを削除した後、一時テーブルは削除されず、引き続き読み取りと書き込みが可能です。
-   ローカル一時テーブルを作成するには`CREATE TEMPORARY TABLES`権限が必要です。テーブルに対する後続のすべての操作には、権限は必要ありません。
-   ローカル一時テーブルは、外部キーとパーティション テーブルをサポートしていません。
-   ローカル一時テーブルに基づくビューの作成はサポートされていません。
-   `SHOW [FULL] TABLES`は、ローカル一時テーブルを表示しません。

TiDB のローカル一時テーブルは、次の点で MySQL 一時テーブルと互換性がありません。

-   TiDB ローカル一時テーブルは`ALTER TABLE`をサポートしていません。
-   TiDB ローカル一時テーブルは`ENGINE`テーブル オプションを無視し、常に一時テーブル データを TiDBメモリに[メモリ制限](#limit-the-memory-usage-of-temporary-tables)で格納します。
-   `MEMORY`がstorageエンジンとして宣言されている場合、TiDB ローカル一時テーブルは`MEMORY`storageエンジンによって制限されません。
-   `INNODB`または`MYISAM`がstorageエンジンとして宣言されている場合、TiDB ローカル一時テーブルは InnoDB 一時テーブルに固有のシステム変数を無視します。
-   MySQL では、同じ SQL ステートメントで同じ一時テーブルを複数回参照することは許可されていません。 TiDB ローカル一時テーブルには、この制限はありません。
-   MySQL の一時テーブルを示すシステム テーブル`information_schema.INNODB_TEMP_TABLE_INFO`は、TiDB には存在しません。現在、TiDB には、ローカルの一時テーブルを表示するシステム テーブルがありません。
-   TiDB には内部一時テーブルがありません。内部一時テーブルの MySQL システム変数は、TiDB では有効になりません。

## グローバル一時テーブル {#global-temporary-tables}

グローバル一時テーブルは TiDB の拡張です。特徴は次のとおりです。

-   グローバル一時テーブルのテーブル定義は永続的で、すべてのセッションに表示されます。
-   グローバル一時テーブルのデータは、現在のトランザクションでのみ表示されます。取引が終了すると、データは自動的に消去されます。
-   グローバル一時テーブルは、通常のテーブルと同じ名前を持つことはできません。

グローバル一時テーブルを作成するには、 `ON COMMIT DELETE ROWS`で終わる`CREATE GLOBAL TEMPORARY TABLE`ステートメントを使用できます。グローバル一時テーブルを削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`ステートメントを使用できます。

### グローバル一時テーブルの使用例 {#usage-examples-of-global-temporary-tables}

> **ノート：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)に注意してください。
> -   v5.3.0以降のTiDBクラスターにグローバル一時テーブルを作成した場合、クラスターをv5.3.0より前のバージョンにダウングレードすると、これらのテーブルは通常のテーブルとして扱われます。この場合、データエラーが発生します。

セッション A にグローバル一時テーブル`users`を作成します。

{{< copyable "" >}}

```sql
CREATE GLOBAL TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

```
Query OK, 0 rows affected (0.01 sec)
```

`users`に書き込まれたデータは、現在のトランザクションに表示されます。

{{< copyable "" >}}

```sql
BEGIN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

トランザクションが終了すると、データは自動的に消去されます。

{{< copyable "" >}}

```sql
COMMIT;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

セッション A で`users`が作成された後、セッション B も`users`テーブルの読み取りと書き込みを行うことができます。

{{< copyable "" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

> **ノート：**
>
> トランザクションが自動的にコミットされる場合、SQL ステートメントの実行後、挿入されたデータは自動的にクリアされ、後続の SQL 実行では使用できなくなります。したがって、非自動コミット トランザクションを使用して、グローバル一時テーブルの読み取りと書き込みを行う必要があります。

## 一時テーブルのメモリ使用量を制限する {#limit-the-memory-usage-of-temporary-tables}

テーブルを定義するときにどのstorageエンジンが`ENGINE`として宣言されても、ローカル一時テーブルとグローバル一時テーブルのデータは TiDB インスタンスのメモリにのみ格納されます。このデータは保持されません。

メモリオーバーフローを回避するために、 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)システム変数を使用して各一時テーブルのサイズを制限できます。一時テーブルが`tidb_tmp_table_max_size`しきい値を超えると、TiDB はエラーを報告します。デフォルト値の`tidb_tmp_table_max_size`は`64MB`です。

たとえば、一時テーブルの最大サイズを`256MB`に設定します。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 他の TiDB 機能との互換性の制限 {#compatibility-restrictions-with-other-tidb-features}

TiDB のローカル一時テーブルとグローバル一時テーブルは、次の TiDB 機能と互換性**がありません**。

-   `AUTO_RANDOM`列
-   `SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`テーブル オプション
-   分割されたテーブル
-   `SPLIT REGION`ステートメント
-   `ADMIN CHECK TABLE`および`ADMIN CHECKSUM TABLE`ステートメント
-   `FLASHBACK TABLE`および`RECOVER TABLE`ステートメント
-   一時テーブルに基づいて`CREATE TABLE LIKE`ステートメントを実行する
-   ステイル読み取り
-   外部キー
-   SQL バインディング
-   TiFlashレプリカ
-   一時テーブルでのビューの作成
-   配置ルール
-   一時テーブルを含む実行プランは`prepare plan cache`によってキャッシュされません。

TiDB のローカル一時テーブルは、次の機能をサポートしてい**ません**。

-   `tidb_snapshot`システム変数を使用した履歴データの読み取り。

## TiDB 移行ツールのサポート {#tidb-migration-tool-support}

ローカルの一時テーブルは、TiDB 移行ツールによってエクスポート、バックアップ、または複製されません。これは、これらのテーブルが現在のセッションにのみ表示されるためです。

テーブル定義はグローバルに表示されるため、グローバル一時テーブルは TiDB 移行ツールによってエクスポート、バックアップ、および複製されます。テーブルのデータはエクスポートされないことに注意してください。

> **ノート：**
>
> -   TiCDC を使用して一時テーブルを複製するには、TiCDC v5.3.0 以降が必要です。そうでない場合は、下流のテーブルのテーブル定義が間違っています。
> -   BRを使用して一時テーブルをバックアップするには、 BR v5.3.0 以降が必要です。それ以外の場合は、バッキングされた一時テーブルのテーブル定義が間違っています。
> -   エクスポートするクラスター、データ復元後のクラスター、およびレプリケーションのダウンストリーム クラスターは、グローバル一時テーブルをサポートする必要があります。それ以外の場合、エラーが報告されます。

## こちらもご覧ください {#see-also}

-   [テーブルを作成](/sql-statements/sql-statement-create-table.md)
-   [次のようなテーブルを作成](/sql-statements/sql-statement-create-table-like.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
