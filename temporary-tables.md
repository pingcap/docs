---
title: Temporary Tables
summary: TiDB の一時テーブル機能について学習し、一時テーブルを使用してアプリケーションの中間データを保存する方法を学習します。これにより、テーブル管理のオーバーヘッドが削減され、パフォーマンスが向上します。
---

# 一時テーブル {#temporary-tables}

一時テーブル機能は、TiDB v5.3.0 で導入されました。この機能は、アプリケーションの中間結果を一時的に保存するという問題を解決し、テーブルを頻繁に作成したり削除したりする手間を省きます。中間計算データは一時テーブルに保存できます。中間データが不要になると、TiDB は一時テーブルを自動的にクリーンアップしてリサイクルします。これにより、ユーザー アプリケーションが複雑になりすぎることがなくなり、テーブル管理のオーバーヘッドが削減され、パフォーマンスが向上します。

このドキュメントでは、ユーザー シナリオと一時テーブルの種類を紹介し、一時テーブルのメモリ使用量を制限する方法の使用例と手順を示し、他の TiDB 機能との互換性の制限について説明します。

## ユーザーシナリオ {#user-scenarios}

TiDB 一時テーブルは、次のシナリオで使用できます。

-   アプリケーションの中間一時データをキャッシュします。計算が完了すると、データは通常のテーブルにダンプされ、一時テーブルは自動的に解放されます。
-   短時間で同じデータに対して複数の DML 操作を実行します。たとえば、電子商取引のショッピング カート アプリケーションでは、製品の追加、変更、削除、支払いの完了、ショッピング カート情報の削除などを行います。
-   中間一時データを一括で素早くインポートし、一時データのインポートのパフォーマンスを向上させます。
-   データを一括更新します。データをデータベース内の一時テーブルに一括でインポートし、データの変更が完了したらデータをファイルにエクスポートします。

## 一時テーブルの種類 {#types-of-temporary-tables}

TiDB の一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの 2 種類に分かれています。

-   ローカル一時テーブルの場合、テーブル定義とテーブル内のデータは現在のセッションでのみ表示されます。このタイプは、セッションで中間データを一時的に保存するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義は TiDB クラスター全体に表示され、テーブル内のデータは現在のトランザクションにのみ表示されます。このタイプは、トランザクション内の中間データを一時的に保存するのに適しています。

## ローカル一時テーブル {#local-temporary-tables}

TiDB のローカル一時テーブルのセマンティクスは、MySQL の一時テーブルのセマンティクスと一致しています。特徴は次のとおりです。

-   ローカル一時テーブルのテーブル定義は永続的ではありません。ローカル一時テーブルは、テーブルが作成されたセッションでのみ表示され、他のセッションはテーブルにアクセスできません。
-   異なるセッションで同じ名前のローカル一時テーブルを作成できます。各セッションでは、セッションで作成されたローカル一時テーブルに対してのみ読み取りと書き込みが行われます。
-   ローカル一時テーブルのデータは、セッション内のすべてのトランザクションに表示されます。
-   セッションが終了すると、セッションで作成されたローカル一時テーブルは自動的に削除されます。
-   ローカル一時テーブルは、通常のテーブルと同じ名前を持つことができます。この場合、DDL および DML ステートメントでは、ローカル一時テーブルが削除されるまで、通常のテーブルは非表示になります。

ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLE`ステートメントを使用できます。ローカル一時テーブルを削除するには、 `DROP TABLE`または`DROP TEMPORARY TABLE`ステートメントを使用できます。

MySQL とは異なり、TiDB のローカル一時テーブルはすべて外部テーブルであり、SQL ステートメントが実行されても内部一時テーブルは自動的に作成されません。

### ローカル一時テーブルの使用例 {#usage-examples-of-local-temporary-tables}

> **注記：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)と[MySQL 一時テーブルとの互換性](#compatibility-with-mysql-temporary-tables)に注意してください。
> -   TiDB v5.3.0 より前のクラスターでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスターが TiDB v5.3.0 以降のバージョンにアップグレードされた後も通常のテーブルとして扱われます。

通常のテーブル`users`があると仮定します。

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

セッション A では、ローカル一時テーブル`users`を作成しても、通常のテーブル`users`と競合しません。セッション A がテーブル`users`にアクセスすると、ローカル一時テーブル`users`にアクセスします。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

    Query OK, 0 rows affected (0.01 sec)

`users`にデータを挿入すると、セッション A のローカル一時テーブル`users`にデータが挿入されます。

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

    Query OK, 1 row affected (0.00 sec)

```sql
SELECT * FROM users;
```

    +------+-------+------------+
    | id   | name  | city       |
    +------+-------+------------+
    | 1001 | Davis | LosAngeles |
    +------+-------+------------+
    1 row in set (0.00 sec)

セッション B では、ローカル一時テーブル`users`を作成しても、セッション A の通常のテーブル`users`またはローカル一時テーブル`users`と競合しません。セッション B がテーブル`users`にアクセスすると、セッション B のローカル一時テーブル`users`にアクセスします。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

    Query OK, 0 rows affected (0.01 sec)

`users`にデータを挿入すると、セッション B のローカル一時テーブル`users`にデータが挿入されます。

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'James', 'NewYork');
```

    Query OK, 1 row affected (0.00 sec)

```sql
SELECT * FROM users;
```

    +------+-------+---------+
    | id   | name  | city    |
    +------+-------+---------+
    | 1001 | James | NewYork |
    +------+-------+---------+
    1 row in set (0.00 sec)

### MySQL 一時テーブルとの互換性 {#compatibility-with-mysql-temporary-tables}

TiDB ローカル一時テーブルの次の機能と制限は、MySQL 一時テーブルと同じです。

-   ローカル一時テーブルを作成または削除すると、現在のトランザクションは自動的にコミットされません。
-   ローカル一時テーブルが配置されているスキーマを削除した後も、一時テーブルは削除されず、引き続き読み取りおよび書き込み可能です。
-   ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLES`権限が必要です。テーブルに対するその後のすべての操作には、権限は必要ありません。
-   ローカル一時テーブルは外部キーとパーティション化されたテーブルをサポートしません。
-   ローカル一時テーブルに基づくビューの作成はサポートされていません。
-   `SHOW [FULL] TABLES`ローカル一時テーブルは表示されません。

TiDB のローカル一時テーブルは、次の点で MySQL 一時テーブルと互換性がありません。

-   TiDB ローカル一時テーブルは`ALTER TABLE`サポートしていません。
-   TiDB ローカル一時テーブルは`ENGINE`テーブル オプションを無視し、常に[メモリ制限](#limit-the-memory-usage-of-temporary-tables)を使用して一時テーブル データを TiDBメモリに格納します。
-   storageエンジンとして`MEMORY`宣言されている場合、TiDB ローカル一時テーブルは`MEMORY`storageエンジンによって制限されません。
-   storageエンジンとして`INNODB`または`MYISAM`宣言されている場合、TiDB ローカル一時テーブルは InnoDB 一時テーブルに固有のシステム変数を無視します。
-   MySQL では、同じ SQL ステートメントで同じ一時テーブルを複数回参照することは許可されません。TiDB のローカル一時テーブルにはこの制限はありません。
-   MySQL の一時テーブルを表示するシステム テーブル`information_schema.INNODB_TEMP_TABLE_INFO`は、TiDB には存在しません。現在、TiDB にはローカル一時テーブルを表示するシステム テーブルがありません。
-   TiDB には内部一時テーブルがありません。内部一時テーブルの MySQL システム変数は TiDB には適用されません。

## グローバル一時テーブル {#global-temporary-tables}

グローバル一時テーブルは TiDB の拡張機能です。特徴は次のとおりです。

-   グローバル一時テーブルのテーブル定義は永続的であり、すべてのセッションで表示されます。
-   グローバル一時テーブルのデータは、現在のトランザクションでのみ表示されます。トランザクションが終了すると、データは自動的にクリアされます。
-   グローバル一時テーブルには、通常のテーブルと同じ名前を付けることはできません。

グローバル一時テーブルを作成するには、 `ON COMMIT DELETE ROWS`で終わる`CREATE GLOBAL TEMPORARY TABLE`ステートメントを使用できます。グローバル一時テーブルを削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`ステートメントを使用できます。

### グローバル一時テーブルの使用例 {#usage-examples-of-global-temporary-tables}

> **注記：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)に注意してください。
> -   v5.3.0 以降の TiDB クラスターでグローバル一時テーブルを作成した場合、クラスターを v5.3.0 より前のバージョンにダウングレードすると、これらのテーブルは通常のテーブルとして扱われます。この場合、データ エラーが発生します。

セッション A にグローバル一時テーブル`users`を作成します。

```sql
CREATE GLOBAL TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

    Query OK, 0 rows affected (0.01 sec)

`users`に書き込まれたデータは現在のトランザクションに表示されます。

```sql
BEGIN;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

    Query OK, 1 row affected (0.00 sec)

```sql
SELECT * FROM users;
```

    +------+-------+------------+
    | id   | name  | city       |
    +------+-------+------------+
    | 1001 | Davis | LosAngeles |
    +------+-------+------------+
    1 row in set (0.00 sec)

トランザクションが終了すると、データは自動的にクリアされます。

```sql
COMMIT;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SELECT * FROM users;
```

    Empty set (0.00 sec)

セッション A で`users`が作成されると、セッション B は`users`テーブルを読み書きすることもできます。

```sql
SELECT * FROM users;
```

    Empty set (0.00 sec)

> **注記：**
>
> トランザクションが自動的にコミットされる場合、SQL ステートメントの実行後、挿入されたデータは自動的にクリアされ、後続の SQL 実行では使用できなくなります。したがって、グローバル一時テーブルからの読み取りと書き込みには、非自動コミット トランザクションを使用する必要があります。

## 一時テーブルのメモリ使用量を制限する {#limit-the-memory-usage-of-temporary-tables}

テーブルを定義するときにどのstorageエンジンを`ENGINE`として宣言したとしても、ローカル一時テーブルとグローバル一時テーブルのデータは TiDB インスタンスのメモリにのみ保存されます。このデータは永続化されません。

メモリオーバーフローを回避するには、 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)システム変数を使用して各一時テーブルのサイズを制限できます。一時テーブルが`tidb_tmp_table_max_size`しきい値を超えると、TiDB はエラーを報告します。デフォルト値は`tidb_tmp_table_max_size`で、 `64MB`です。

たとえば、一時テーブルの最大サイズを`256MB`に設定します。

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 他の TiDB 機能との互換性の制限 {#compatibility-restrictions-with-other-tidb-features}

TiDB のローカル一時テーブルとグローバル一時テーブルは、次の TiDB 機能と互換性が**ありません**。

-   `AUTO_RANDOM`列
-   `SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`テーブル オプション
-   パーティションテーブル
-   `SPLIT REGION`発言
-   `ADMIN CHECK TABLE`と`ADMIN CHECKSUM TABLE`ステートメント
-   `FLASHBACK TABLE`と`RECOVER TABLE`ステートメント
-   一時テーブルに基づいて`CREATE TABLE LIKE`ステートメントを実行しています
-   ステイル読み取り
-   外部キー
-   SQL バインディング
-   TiFlashレプリカ
-   一時テーブルにビューを作成する
-   配置ルール
-   一時テーブルを含む実行プランは`prepare plan cache`によってキャッシュされません。

TiDB のローカル一時テーブルは次の機能をサポートしていませ**ん**。

-   `tidb_snapshot`システム変数を使用して履歴データを読み取ります。

## TiDB移行ツールのサポート {#tidb-migration-tool-support}

ローカル一時テーブルは現在のセッションでのみ表示されるため、TiDB 移行ツールによってエクスポート、バックアップ、または複製されることはありません。

テーブル定義はグローバルに表示されるため、グローバル一時テーブルは TiDB 移行ツールによってエクスポート、バックアップ、および複製されます。テーブル上のデータはエクスポートされないことに注意してください。

> **注記：**
>
> -   TiCDC を使用して一時テーブルを複製するには、TiCDC v5.3.0 以降が必要です。そうでない場合、ダウンストリーム テーブルのテーブル定義が間違っています。
> -   BR を使用して一時テーブルをバックアップするには、 BR v5.3.0 以降が必要です。そうでない場合、バックアップされた一時テーブルのテーブル定義が間違っています。
> -   エクスポートするクラスター、データ復元後のクラスター、およびレプリケーションのダウンストリーム クラスターは、グローバル一時テーブルをサポートする必要があります。そうでない場合は、エラーが報告されます。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [次のようなテーブルを作成する](/sql-statements/sql-statement-create-table-like.md)
-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
