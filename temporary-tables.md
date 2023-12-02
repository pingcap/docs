---
title: Temporary Tables
summary: Learn the temporary tables feature in TiDB, and learn how to use temporary tables to store intermediate data of an application, which helps reduce table management overhead and improve performance.
---

# 一時テーブル {#temporary-tables}

一時テーブル機能は TiDB v5.3.0 で導入されました。この機能は、アプリケーションの中間結果を一時的に保存する問題を解決し、頻繁にテーブルを作成したり削除したりする必要がなくなります。中間計算データを一時テーブルに保存できます。中間データが不要になると、TiDB は一時テーブルを自動的にクリーンアップしてリサイクルします。これにより、ユーザー アプリケーションが複雑になりすぎることが回避され、テーブル管理のオーバーヘッドが軽減され、パフォーマンスが向上します。

このドキュメントでは、ユーザー シナリオと一時テーブルの種類を紹介し、使用例と一時テーブルのメモリ使用量を制限する方法について説明し、他の TiDB 機能との互換性制限について説明します。

## ユーザーシナリオ {#user-scenarios}

TiDB 一時テーブルは次のシナリオで使用できます。

-   アプリケーションの中間一時データをキャッシュします。計算が完了すると、データは通常のテーブルにダンプされ、一時テーブルは自動的に解放されます。
-   同じデータに対して短時間に複数の DML 操作を実行します。たとえば、電子商取引ショッピング カート アプリケーションでは、製品の追加、変更、削除、支払いの完了、ショッピング カート情報の削除を行います。
-   中間一時データをバッチで迅速にインポートし、一時データのインポートのパフォーマンスを向上させます。
-   データをバッチで更新します。データベース内の一時テーブルにデータをバッチでインポートし、データの変更が完了したら、データをファイルにエクスポートします。

## 一時テーブルの種類 {#types-of-temporary-tables}

TiDB の一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの 2 つのタイプに分類されます。

-   ローカル一時テーブルの場合、テーブル定義とテーブル内のデータは現在のセッションでのみ表示されます。このタイプは、セッション内の中間データを一時的に保存するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義は TiDB クラスター全体に表示され、テーブル内のデータは現在のトランザクションにのみ表示されます。トランザクション内の中間データを一時的に保存するのに適した型です。

## ローカル一時テーブル {#local-temporary-tables}

TiDB のローカル一時テーブルのセマンティクスは、MySQL 一時テーブルのセマンティクスと一致しています。特徴は次のとおりです。

-   ローカル一時テーブルのテーブル定義は永続的ではありません。ローカル一時テーブルは、テーブルが作成されたセッションにのみ表示され、他のセッションはテーブルにアクセスできません。
-   異なるセッションに同じ名前のローカル一時テーブルを作成できます。各セッションは、セッション内で作成されたローカル一時テーブルに対して読み取り専用と書き込み専用を行います。
-   ローカル一時テーブルのデータは、セッション内のすべてのトランザクションに表示されます。
-   セッションが終了すると、セッションで作成されたローカル一時テーブルは自動的に削除されます。
-   ローカル一時テーブルには、通常のテーブルと同じ名前を付けることができます。この場合、DDL および DML ステートメントでは、ローカル一時テーブルが削除されるまで、通常のテーブルは非表示になります。

ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLE`ステートメントを使用できます。ローカル一時テーブルを削除するには、 `DROP TABLE`または`DROP TEMPORARY TABLE`ステートメントを使用できます。

MySQL とは異なり、TiDB のローカル一時テーブルはすべて外部テーブルであり、SQL ステートメントの実行時に内部一時テーブルが自動的に作成されることはありません。

### ローカル一時テーブルの使用例 {#usage-examples-of-local-temporary-tables}

> **注記：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性制限](#compatibility-restrictions-with-other-tidb-features)と[MySQL 一時テーブルとの互換性](#compatibility-with-mysql-temporary-tables)に注意してください。
> -   TiDB v5.3.0 より前のクラスター上にローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスターが TiDB v5.3.0 以降のバージョンにアップグレードされた後は通常のテーブルとして扱われます。

通常のテーブル`users`があると仮定します。

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

セッション A では、ローカル一時テーブル`users`の作成は通常のテーブル`users`と競合しません。セッション A がテーブル`users`にアクセスすると、ローカル一時テーブル`users`にアクセスします。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

    Query OK, 0 rows affected (0.01 sec)

`users`にデータを挿入すると、データはセッション A のローカル一時テーブル`users`に挿入されます。

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

セッション B では、ローカル一時テーブル`users`を作成しても、セッション A の通常のテーブル`users`やローカル一時テーブル`users`と競合しません。セッション B がテーブル`users`にアクセスする場合、セッション B のローカル一時テーブル`users`にアクセスします。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

    Query OK, 0 rows affected (0.01 sec)

`users`にデータを挿入すると、データはセッション B のローカル一時テーブル`users`に挿入されます。

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

TiDB ローカル一時テーブルの次の機能と制限は、MySQL 一時テーブルの機能と制限と同じです。

-   ローカル一時テーブルを作成または削除する場合、現在のトランザクションは自動的にコミットされません。
-   ローカル一時テーブルが配置されているスキーマを削除した後、一時テーブルは削除されず、引き続き読み取りおよび書き込み可能です。
-   ローカル一時テーブルを作成するには`CREATE TEMPORARY TABLES`権限が必要です。テーブルに対する後続のすべての操作には権限は必要ありません。
-   ローカル一時テーブルは、外部キーとパーティション テーブルをサポートしません。
-   ローカル一時テーブルに基づくビューの作成はサポートされていません。
-   `SHOW [FULL] TABLES`はローカル一時テーブルを表示しません。

TiDB のローカル一時テーブルは、次の点で MySQL 一時テーブルと互換性がありません。

-   TiDB ローカル一時テーブルは`ALTER TABLE`をサポートしません。
-   TiDB ローカル一時テーブルは`ENGINE`テーブル オプションを無視し、常に一時テーブル データを TiDBメモリに[メモリ制限](#limit-the-memory-usage-of-temporary-tables)で保存します。
-   storageエンジンとして`MEMORY`が宣言されている場合、TiDB ローカル一時テーブルは`MEMORY`storageエンジンによって制限されません。
-   `INNODB`または`MYISAM`がstorageエンジンとして宣言されている場合、TiDB ローカル一時テーブルは InnoDB 一時テーブルに固有のシステム変数を無視します。
-   MySQL では、同じ SQL ステートメント内で同じ一時テーブルを複数回参照することは許可されません。 TiDB ローカル一時テーブルにはこの制限はありません。
-   MySQL の一時テーブルを示すシステム テーブル`information_schema.INNODB_TEMP_TABLE_INFO`は TiDB には存在しません。現在、TiDB にはローカル一時テーブルを表示するシステム テーブルがありません。
-   TiDB には内部一時テーブルがありません。内部一時テーブルの MySQL システム変数は TiDB に対しては有効ではありません。

## グローバル一時テーブル {#global-temporary-tables}

グローバル一時テーブルは TiDB の拡張機能です。特徴は次のとおりです。

-   グローバル一時テーブルのテーブル定義は永続的であり、すべてのセッションから参照できます。
-   グローバル一時テーブルのデータは、現在のトランザクションでのみ表示されます。トランザクションが終了すると、データは自動的に消去されます。
-   グローバル一時テーブルに通常のテーブルと同じ名前を付けることはできません。

グローバル一時テーブルを作成するには、 `ON COMMIT DELETE ROWS`で終わる`CREATE GLOBAL TEMPORARY TABLE`ステートメントを使用できます。グローバル一時テーブルを削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`ステートメントを使用できます。

### グローバル一時テーブルの使用例 {#usage-examples-of-global-temporary-tables}

> **注記：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性制限](#compatibility-restrictions-with-other-tidb-features)点に注意してください。
> -   v5.3.0 以降の TiDB クラスター上にグローバル一時テーブルを作成した場合、クラスターが v5.3.0 より前のバージョンにダウングレードされると、これらのテーブルは通常のテーブルとして処理されます。この場合、データエラーが発生します。

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

`users`に書き込まれたデータは、現在のトランザクションから参照できます。

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

トランザクションが終了すると、データは自動的に消去されます。

```sql
COMMIT;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SELECT * FROM users;
```

    Empty set (0.00 sec)

セッション A で`users`が作成されると、セッション B もテーブル`users`の読み取りと書き込みを行うことができます。

```sql
SELECT * FROM users;
```

    Empty set (0.00 sec)

> **注記：**
>
> トランザクションが自動的にコミットされる場合、SQL ステートメントの実行後、挿入されたデータは自動的にクリアされ、後続の SQL 実行では使用できなくなります。したがって、グローバル一時テーブルの読み取りおよび書き込みには、非自動コミット トランザクションを使用する必要があります。

## 一時テーブルのメモリ使用量を制限する {#limit-the-memory-usage-of-temporary-tables}

テーブルを定義するときにどのstorageエンジンが`ENGINE`として宣言されていても、ローカル一時テーブルとグローバル一時テーブルのデータは TiDB インスタンスのメモリにのみ保存されます。このデータは永続化されません。

メモリのオーバーフローを避けるために、 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)システム変数を使用して各一時テーブルのサイズを制限できます。一時テーブルが`tidb_tmp_table_max_size`しきい値を超えると、TiDB はエラーを報告します。デフォルト値の`tidb_tmp_table_max_size`は`64MB`です。

たとえば、一時テーブルの最大サイズを`256MB`に設定します。

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 他の TiDB 機能との互換性制限 {#compatibility-restrictions-with-other-tidb-features}

TiDB のローカル一時テーブルおよびグローバル一時テーブルは、次の TiDB 機能と互換性**がありません**。

-   `AUTO_RANDOM`列
-   `SHARD_ROW_ID_BITS`および`PRE_SPLIT_REGIONS`テーブル オプション
-   パーティション化されたテーブル
-   `SPLIT REGION`件のステートメント
-   `ADMIN CHECK TABLE`および`ADMIN CHECKSUM TABLE`ステートメント
-   `FLASHBACK TABLE`および`RECOVER TABLE`ステートメント
-   一時テーブルに基づいて`CREATE TABLE LIKE`ステートメントを実行する
-   ステイル読み取り
-   外部キー
-   SQLバインディング
-   TiFlashレプリカ
-   一時テーブルでのビューの作成
-   配置ルール
-   一時テーブルを含む実行プランは`prepare plan cache`によってキャッシュされません。

TiDB のローカル一時テーブルは次の機能をサポートしてい**ません**。

-   `tidb_snapshot`システム変数を使用して履歴データを読み取ります。

## TiDB 移行ツールのサポート {#tidb-migration-tool-support}

ローカル一時テーブルは現在のセッションでのみ表示されるため、TiDB 移行ツールによってエクスポート、バックアップ、複製されません。

グローバル一時テーブルは、テーブル定義がグローバルに表示されるため、TiDB 移行ツールによってエクスポート、バックアップ、複製されます。テーブル上のデータはエクスポートされないことに注意してください。

> **注記：**
>
> -   TiCDC を使用して一時テーブルをレプリケートするには、TiCDC v5.3.0 以降が必要です。それ以外の場合、下流表の表定義が間違っています。
> -   BRを使用して一時テーブルをバックアップするには、 BR v5.3.0 以降が必要です。そうしないと、バックアップされた一時テーブルのテーブル定義が間違っています。
> -   エクスポートするクラスター、データ復元後のクラスター、およびレプリケーションのダウンストリーム クラスターは、グローバル一時テーブルをサポートする必要があります。それ以外の場合は、エラーが報告されます。

## こちらも参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [次のようなテーブルを作成します](/sql-statements/sql-statement-create-table-like.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
