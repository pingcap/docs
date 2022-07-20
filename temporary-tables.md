---
title: Temporary Tables
summary: Learn the temporary tables feature in TiDB, and learn how to use temporary tables to store intermediate data of an application, which helps reduce table management overhead and improve performance.
---

# 一時的なテーブル {#temporary-tables}

一時テーブル機能は、TiDBv5.3.0で導入されました。この機能は、アプリケーションの中間結果を一時的に保存する問題を解決します。これにより、テーブルを頻繁に作成および削除する必要がなくなります。中間計算データを一時テーブルに保存できます。中間データが不要になると、TiDBは一時テーブルを自動的にクリーンアップしてリサイクルします。これにより、ユーザーアプリケーションが複雑になりすぎるのを防ぎ、テーブル管理のオーバーヘッドを減らし、パフォーマンスを向上させます。

このドキュメントでは、ユーザーシナリオと一時テーブルの種類を紹介し、使用例と一時テーブルのメモリ使用量を制限する方法について説明し、他のTiDB機能との互換性の制限について説明します。

## ユーザーシナリオ {#user-scenarios}

次のシナリオでTiDB一時テーブルを使用できます。

-   アプリケーションの中間一時データをキャッシュします。計算が完了すると、データは通常のテーブルにダンプされ、一時テーブルは自動的に解放されます。
-   短時間で同じデータに対して複数のDML操作を実行します。たとえば、eコマースショッピングカートアプリケーションでは、商品の追加、変更、削除、支払いの完了、ショッピングカート情報の削除を行います。
-   中間一時データをバッチですばやくインポートして、一時データのインポートのパフォーマンスを向上させます。
-   データをバッチで更新します。データをデータベースの一時テーブルにバッチでインポートし、データの変更が完了した後、データをファイルにエクスポートします。

## 一時テーブルの種類 {#types-of-temporary-tables}

TiDBの一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの2つのタイプに分けられます。

-   ローカル一時テーブルの場合、テーブル定義とテーブル内のデータは、現在のセッションにのみ表示されます。このタイプは、セッションに中間データを一時的に保存するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義はTiDBクラスタ全体に表示され、テーブル内のデータは現在のトランザクションにのみ表示されます。このタイプは、トランザクションで中間データを一時的に保存するのに適しています。

## ローカル一時テーブル {#local-temporary-tables}

TiDBのローカル一時テーブルのセマンティクスは、MySQL一時テーブルのセマンティクスと一致しています。特徴は次のとおりです。

-   ローカル一時テーブルのテーブル定義は永続的ではありません。ローカル一時テーブルは、テーブルが作成されたセッションにのみ表示され、他のセッションはテーブルにアクセスできません。
-   異なるセッションで同じ名前のローカル一時テーブルを作成できます。各セッションは、セッションで作成されたローカル一時テーブルからの読み取りと書き込みのみを行います。
-   ローカル一時テーブルのデータは、セッション内のすべてのトランザクションに表示されます。
-   セッションが終了すると、セッションで作成されたローカル一時テーブルは自動的に削除されます。
-   ローカル一時テーブルは、通常のテーブルと同じ名前にすることができます。この場合、DDLおよびDMLステートメントでは、ローカル一時テーブルが削除されるまで、通常のテーブルは非表示になります。

ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLE`ステートメントを使用できます。ローカル一時テーブルを削除するには、 `DROP TABLE`または`DROP TEMPORARY TABLE`ステートメントを使用できます。

MySQLとは異なり、TiDBのローカル一時テーブルはすべて外部テーブルであり、SQLステートメントの実行時に内部一時テーブルが自動的に作成されることはありません。

### ローカル一時テーブルの使用例 {#usage-examples-of-local-temporary-tables}

> **ノート：**
>
> -   TiDBで一時テーブルを使用する前に、 [他のTiDB機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)と[MySQL一時テーブルとの互換性](#compatibility-with-mysql-temporary-tables)に注意してください。
> -   TiDB v5.3.0より前のクラスタでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスタがTiDBv5.3.0以降のバージョンにアップグレードされた後は通常のテーブルとして扱われます。

通常のテーブルがあると仮定します`users` ：

{{< copyable "" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

セッションAでは、ローカル一時テーブル`users`の作成は、通常のテーブル`users`と競合しません。セッションAが`users`テーブルにアクセスすると、ローカル一時テーブル`users`にアクセスします。

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

`users`にデータを挿入すると、セッションAのローカル一時テーブル`users`にデータが挿入されます。

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

セッションBでは、ローカル一時テーブル`users`を作成しても、セッションAの通常のテーブル`users`またはローカル一時テーブル`users`と競合しません。セッションBが`users`テーブルにアクセスすると、セッションBのローカル一時テーブル`users`にアクセスします。

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

`users`にデータを挿入すると、セッションBのローカル一時テーブル`users`にデータが挿入されます。

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

### MySQL一時テーブルとの互換性 {#compatibility-with-mysql-temporary-tables}

TiDBローカル一時テーブルの次の機能と制限は、MySQL一時テーブルと同じです。

-   ローカル一時テーブルを作成または削除しても、現在のトランザクションは自動的にコミットされません。
-   ローカル一時テーブルが配置されているスキーマを削除した後、一時テーブルは削除されず、読み取りと書き込みが可能です。
-   ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLES`の権限が必要です。テーブルに対する後続のすべての操作には、許可は必要ありません。
-   ローカル一時テーブルは、外部キーとパーティションテーブルをサポートしていません。
-   ローカル一時テーブルに基づくビューの作成はサポートされていません。
-   `SHOW [FULL] TABLES`はローカル一時テーブルを表示しません。

TiDBのローカル一時テーブルは、次の点でMySQL一時テーブルと互換性がありません。

-   TiDBローカル一時テーブルは`ALTER TABLE`をサポートしていません。
-   TiDBローカル一時テーブルは`ENGINE`テーブルオプションを無視し、一時テーブルデータを常に[メモリ制限](#limit-the-memory-usage-of-temporary-tables)でTiDBメモリに保存します。
-   ストレージエンジンとして`MEMORY`が宣言されている場合、TiDBローカル一時テーブルは`MEMORY`ストレージエンジンによって制限されません。
-   `INNODB`または`MYISAM`がストレージエンジンとして宣言されている場合、TiDBローカル一時テーブルはInnoDB一時テーブルに固有のシステム変数を無視します。
-   MySQLは、同じSQLステートメントで同じ一時テーブルを複数回参照することを許可していません。 TiDBローカル一時テーブルにはこの制限はありません。
-   MySQLの一時テーブルを示すシステムテーブル`information_schema.INNODB_TEMP_TABLE_INFO`はTiDBに存在しません。現在、TiDBにはローカル一時テーブルを表示するシステムテーブルがありません。
-   TiDBには内部一時テーブルがありません。内部一時テーブルのMySQLシステム変数は、TiDBでは有効になりません。

## グローバル一時テーブル {#global-temporary-tables}

グローバル一時テーブルはTiDBの拡張です。特徴は次のとおりです。

-   グローバル一時テーブルのテーブル定義は永続的であり、すべてのセッションに表示されます。
-   グローバル一時テーブルのデータは、現在のトランザクションでのみ表示されます。トランザクションが終了すると、データは自動的にクリアされます。
-   グローバル一時テーブルに通常のテーブルと同じ名前を付けることはできません。

グローバル一時テーブルを作成するには、 `ON COMMIT DELETE ROWS`で終わる`CREATE GLOBAL TEMPORARY TABLE`ステートメントを使用できます。グローバル一時テーブルを削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`ステートメントを使用できます。

### グローバル一時テーブルの使用例 {#usage-examples-of-global-temporary-tables}

> **ノート：**
>
> -   TiDBで一時テーブルを使用する前に、 [他のTiDB機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)に注意してください。
> -   v5.3.0以降のTiDBクラスタでグローバル一時テーブルを作成した場合、クラスタがv5.3.0より前のバージョンにダウングレードされると、これらのテーブルは通常のテーブルとして処理されます。この場合、データエラーが発生します。

セッションAでグローバル一時テーブル`users`を作成します。

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

トランザクションが終了すると、データは自動的にクリアされます。

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

セッションAで`users`が作成された後、セッションBは3テーブルからの読み取りと`users`テーブルへの書き込みもできます。

{{< copyable "" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

> **ノート：**
>
> トランザクションが自動的にコミットされる場合、SQLステートメントが実行された後、挿入されたデータは自動的にクリアされ、後続のSQL実行で使用できなくなります。したがって、自動コミット以外のトランザクションを使用して、グローバル一時テーブルの読み取りと書き込みを行う必要があります。

## 一時テーブルのメモリ使用量を制限する {#limit-the-memory-usage-of-temporary-tables}

テーブルを定義するときにどのストレージエンジンが`ENGINE`として宣言されていても、ローカル一時テーブルとグローバル一時テーブルのデータはTiDBインスタンスのメモリにのみ保存されます。このデータは永続化されません。

メモリオーバーフローを回避するために、 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)のシステム変数を使用して各一時テーブルのサイズを制限できます。一時テーブルが`tidb_tmp_table_max_size`しきい値より大きくなると、TiDBはエラーを報告します。デフォルト値の`tidb_tmp_table_max_size`は`64MB`です。

たとえば、一時テーブルの最大サイズを`256MB`に設定します。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 他のTiDB機能との互換性の制限 {#compatibility-restrictions-with-other-tidb-features}

TiDBのローカル一時テーブルとグローバル一時テーブルは、次のTiDB機能と互換性があり**ません**。

-   `AUTO_RANDOM`列
-   `SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`テーブルオプション
-   パーティションテーブル
-   `SPLIT REGION`ステートメント
-   `ADMIN CHECK TABLE`および`ADMIN CHECKSUM TABLE`ステートメント
-   `FLASHBACK TABLE`および`RECOVER TABLE`ステートメント
-   一時テーブルに基づいて`CREATE TABLE LIKE`のステートメントを実行する
-   古い読み取り
-   外部キー
-   SQLバインディング
-   TiFlashレプリカ
-   一時テーブルにビューを作成する
-   配置ルール
-   一時テーブルを含む実行プランは`prepare plan cache`によってキャッシュされません。

TiDBのローカル一時テーブルは、次の機能をサポートしてい**ません**。

-   `tidb_snapshot`のシステム変数を使用して履歴データを読み取ります。

## TiDB移行ツールのサポート {#tidb-migration-tool-support}

ローカル一時テーブルは、現在のセッションでのみ表示されるため、TiDB移行ツールによってエクスポート、バックアップ、または複製されません。

テーブル定義はグローバルに表示されるため、グローバル一時テーブルはTiDB移行ツールによってエクスポート、バックアップ、および複製されます。テーブルのデータはエクスポートされないことに注意してください。

> **ノート：**
>
> -   TiCDCを使用して一時テーブルを複製するには、TiCDCv5.3.0以降が必要です。そうでない場合、ダウンストリームテーブルのテーブル定義が間違っています。
> -   BRを使用して一時テーブルをバックアップするには、BRv5.3.0以降が必要です。そうしないと、バックアップされた一時テーブルのテーブル定義が間違っています。
> -   エクスポートするクラスタ、データ復元後のクラスタ、およびレプリケーションのダウンストリームクラスタは、グローバル一時テーブルをサポートする必要があります。それ以外の場合は、エラーが報告されます。

## も参照してください {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルのようなものを作成](/sql-statements/sql-statement-create-table-like.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
