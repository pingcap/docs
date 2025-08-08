---
title: Temporary Tables
summary: TiDB の一時テーブル機能について学習し、一時テーブルを使用してアプリケーションの中間データを保存する方法を学習します。これにより、テーブル管理のオーバーヘッドが削減され、パフォーマンスが向上します。
---

# 一時テーブル {#temporary-tables}

TiDB v5.3.0では、一時テーブル機能が導入されました。この機能は、アプリケーションの中間結果を一時的に保存するという問題を解決し、頻繁なテーブルの作成と削除から解放します。中間計算データは一時テーブルに保存できます。中間データが不要になると、TiDBは自動的に一時テーブルをクリーンアップして再利用します。これにより、ユーザーアプリケーションの複雑化を防ぎ、テーブル管理のオーバーヘッドを削減し、パフォーマンスを向上させます。

このドキュメントでは、ユーザー シナリオと一時テーブルの種類を紹介し、一時テーブルのメモリ使用量を制限する使用例と手順を示し、他の TiDB 機能との互換性の制限について説明します。

## ユーザーシナリオ {#user-scenarios}

TiDB 一時テーブルは、次のシナリオで使用できます。

-   アプリケーションの中間一時データをキャッシュします。計算が完了すると、データは通常のテーブルにダンプされ、一時テーブルは自動的に解放されます。
-   短時間で同じデータに対して複数のDML操作を実行します。例えば、eコマースのショッピングカートアプリケーションでは、商品の追加、変更、削除、支払いの完了、ショッピングカート情報の削除などが可能です。
-   中間一時データを一括で素早くインポートし、一時データのインポートのパフォーマンスを向上させます。
-   データを一括更新します。データベース内の一時テーブルにデータを一括インポートし、データの変更が完了したらファイルにエクスポートします。

## 一時テーブルの種類 {#types-of-temporary-tables}

TiDB の一時テーブルは、ローカル一時テーブルとグローバル一時テーブルの 2 種類に分かれています。

-   ローカル一時テーブルの場合、テーブル定義とテーブル内のデータは現在のセッションでのみ参照可能です。このタイプは、セッション中の中間データを一時的に保存するのに適しています。
-   グローバル一時テーブルの場合、テーブル定義はTiDBクラスタ全体から参照可能で、テーブル内のデータは現在のトランザクションからのみ参照可能です。このタイプは、トランザクション中の中間データを一時的に保存するのに適しています。

## ローカル一時テーブル {#local-temporary-tables}

TiDBのローカル一時テーブルのセマンティクスは、MySQLの一時テーブルと一致しています。その特徴は次のとおりです。

-   ローカル一時テーブルのテーブル定義は永続的ではありません。ローカル一時テーブルは、テーブルが作成されたセッションでのみ参照可能であり、他のセッションからはアクセスできません。
-   異なるセッションで同じ名前のローカル一時テーブルを作成できます。各セッションでは、セッションで作成されたローカル一時テーブルに対してのみ読み取りと書き込みが行われます。
-   ローカル一時テーブルのデータは、セッション内のすべてのトランザクションに表示されます。
-   セッションが終了すると、セッションで作成されたローカル一時テーブルは自動的に削除されます。
-   ローカル一時テーブルは通常のテーブルと同じ名前を持つことができます。この場合、DDLおよびDMLステートメントでは、ローカル一時テーブルが削除されるまで、通常のテーブルは非表示になります。

ローカル一時テーブルを作成するには、 `CREATE TEMPORARY TABLE`文を使用します。ローカル一時テーブルを削除するには、 `DROP TABLE`文または`DROP TEMPORARY TABLE`文を使用します。

MySQL とは異なり、TiDB のローカル一時テーブルはすべて外部テーブルであり、SQL ステートメントの実行時に内部一時テーブルは自動的に作成されません。

### ローカル一時テーブルの使用例 {#usage-examples-of-local-temporary-tables}

> **注記：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)と[MySQLの一時テーブルとの互換性](#compatibility-with-mysql-temporary-tables)に注意してください。
> -   TiDB v5.3.0 より前のバージョンのクラスターでローカル一時テーブルを作成した場合、これらのテーブルは実際には通常のテーブルであり、クラスターが TiDB v5.3.0 以降のバージョンにアップグレードされた後は、通常のテーブルとして扱われます。

通常のテーブル`users`があると仮定します。

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

セッションAでは、ローカル一時テーブル`users`を作成しても、通常のテーブル`users`と競合しません。セッションAがテーブル`users`アクセスすると、ローカル一時テーブル`users`アクセスします。

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

セッション B でローカル一時テーブル`users`を作成しても、セッション A の通常のテーブル`users`またはローカル一時テーブル`users`と競合しません。セッション B がテーブル`users`アクセスすると、セッション B のローカル一時テーブル`users`にアクセスします。

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

    Query OK, 0 rows affected (0.01 sec)

`users`にデータを挿入すると、セッション B のローカル一時テーブル`users`にもデータが挿入されます。

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
-   ローカル一時テーブルの作成には権限`CREATE TEMPORARY TABLES`必要です。それ以降のテーブルに対する操作には権限は必要ありません。
-   ローカル一時テーブルは外部キーとパーティション化されたテーブルをサポートしません。
-   ローカル一時テーブルに基づくビューの作成はサポートされていません。
-   `SHOW [FULL] TABLES`場合、ローカル一時テーブルは表示されません。

TiDB のローカル一時テーブルは、次の点で MySQL の一時テーブルと互換性がありません。

-   TiDB ローカル一時テーブルは`ALTER TABLE`サポートしていません。
-   TiDB ローカル一時テーブルは`ENGINE`テーブル オプションを無視し、常に[メモリ制限](#limit-the-memory-usage-of-temporary-tables)を使用して一時テーブル データを TiDBメモリに格納します。
-   storageエンジンとして`MEMORY`宣言されている場合、TiDB ローカル一時テーブルは`MEMORY`storageエンジンによって制限されません。
-   storageエンジンとして`INNODB`または`MYISAM`宣言されている場合、TiDB ローカル一時テーブルは InnoDB 一時テーブルに固有のシステム変数を無視します。
-   MySQLでは、同じSQL文内で同じ一時テーブルを複数回参照することはできません。TiDBのローカル一時テーブルにはこの制限はありません。
-   MySQLの一時テーブルを表示するシステムテーブル`information_schema.INNODB_TEMP_TABLE_INFO`は、TiDBには存在しません。現在、TiDBにはローカル一時テーブルを表示するシステムテーブルはありません。
-   TiDBには内部一時テーブルがありません。内部一時テーブル用のMySQLシステム変数はTiDBには適用されません。

## グローバル一時テーブル {#global-temporary-tables}

グローバル一時テーブルはTiDBの拡張機能です。その特徴は次のとおりです。

-   グローバル一時テーブルのテーブル定義は永続的であり、すべてのセッションで表示されます。
-   グローバル一時テーブルのデータは、現在のトランザクション内でのみ参照可能です。トランザクションが終了すると、データは自動的にクリアされます。
-   グローバル一時テーブルは、通常のテーブルと同じ名前を持つことはできません。

グローバル一時テーブルを作成するには、 `ON COMMIT DELETE ROWS`で終わる`CREATE GLOBAL TEMPORARY TABLE`文を使用できます。グローバル一時テーブルを削除するには、 `DROP TABLE`または`DROP GLOBAL TEMPORARY TABLE`文を使用できます。

### グローバル一時テーブルの使用例 {#usage-examples-of-global-temporary-tables}

> **注記：**
>
> -   TiDB で一時テーブルを使用する前に、 [他の TiDB 機能との互換性の制限](#compatibility-restrictions-with-other-tidb-features)に注意してください。
> -   TiDB クラスタ v5.3.0 以降でグローバル一時テーブルを作成した場合、クラスタを v5.3.0 より前のバージョンにダウングレードすると、これらのテーブルは通常のテーブルとして扱われ、データエラーが発生します。

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

セッション A で`users`作成されると、セッション B は`users`テーブルに対して読み取りと書き込みも実行できるようになります。

```sql
SELECT * FROM users;
```

    Empty set (0.00 sec)

> **注記：**
>
> トランザクションが自動的にコミットされた場合、SQL文の実行後、挿入されたデータは自動的にクリアされ、後続のSQL実行では使用できなくなります。したがって、グローバル一時テーブルへの読み書きには、非自動コミットトランザクションを使用する必要があります。

## 一時テーブルのメモリ使用量を制限する {#limit-the-memory-usage-of-temporary-tables}

テーブル定義時にどのstorageエンジンを`ENGINE`として宣言したとしても、ローカル一時テーブルとグローバル一時テーブルのデータはTiDBインスタンスのメモリ内にのみ保存されます。これらのデータは永続化されません。

メモリオーバーフローを回避するために、システム変数[`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530)使用して各一時テーブルのサイズを制限できます。一時テーブルのサイズがしきい値`tidb_tmp_table_max_size`を超えると、TiDB はエラーを報告します。デフォルト値は`tidb_tmp_table_max_size`ですが、現在は`64MB`です。

たとえば、一時テーブルの最大サイズを`256MB`に設定します。

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 他の TiDB 機能との互換性の制限 {#compatibility-restrictions-with-other-tidb-features}

TiDB のローカル一時テーブルとグローバル一時テーブルは、次の TiDB 機能と互換性が**ありません**。

-   `AUTO_RANDOM`列
-   `SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`テーブルオプション
-   パーティションテーブル
-   `SPLIT REGION`ステートメント
-   `ADMIN CHECK TABLE`と`ADMIN CHECKSUM TABLE`文
-   `FLASHBACK TABLE`と`RECOVER TABLE`文
-   一時テーブルに基づいて`CREATE TABLE LIKE`ステートメントを実行しています
-   ステイル読み取り
-   外部キー
-   SQLバインディング
-   TiFlashレプリカ
-   一時テーブルにビューを作成する
-   配置ルール
-   一時テーブルを含む実行プランは`prepare plan cache`によってキャッシュされません。

TiDB のローカル一時テーブルは次の機能をサポートしてい**ません**。

-   `tidb_snapshot`システム変数を使用して履歴データを読み取ります。

## TiDB移行ツールのサポート {#tidb-migration-tool-support}

ローカル一時テーブルは現在のセッションでのみ表示されるため、TiDB 移行ツールによってエクスポート、バックアップ、または複製されることはありません。

グローバル一時テーブルは、テーブル定義がグローバルに参照可能であるため、TiDB移行ツールによってエクスポート、バックアップ、およびレプリケーションされます。ただし、テーブル上のデータはエクスポートされないことに注意してください。

> **注記：**
>
> -   TiCDCを使用して一時テーブルをレプリケーションするには、TiCDC v5.3.0以降が必要です。そうでない場合、ダウンストリームテーブルのテーブル定義が間違っています。
> -   BRを使用して一時テーブルをバックアップするには、 BR v5.3.0 以降が必要です。そうでない場合、バックアップされた一時テーブルのテーブル定義が間違っています。
> -   エクスポートするクラスター、データ復元後のクラスター、およびレプリケーションの下流クラスターは、グローバル一時テーブルをサポートしている必要があります。サポートされていない場合は、エラーが報告されます。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [次のようなテーブルを作成する](/sql-statements/sql-statement-create-table-like.md)
-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
