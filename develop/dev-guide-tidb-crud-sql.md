---
title: CRUD SQL in TiDB
summary: TiDBのCRUD SQLに関する簡単な紹介。
aliases: ['/ja/tidb/stable/dev-guide-tidb-crud-sql/','/ja/tidb/dev/dev-guide-tidb-crud-sql/','/ja/tidbcloud/dev-guide-tidb-crud-sql/']
---

# TiDBにおけるCRUD SQL {#crud-sql-in-tidb}

このドキュメントでは、TiDBのCRUD SQLの使用方法について簡単に説明します。

## 始める前に {#before-you-start}

TiDB に接続していることを確認してください。そうでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-starter-instance)、最初に接続します。

## TiDBでSQLを探求しよう {#explore-sql-with-tidb}

> **注記：**
>
> このドキュメントは[TiDBでSQLを探求しよう](/basic-sql-operations.md)を参照し、簡略化しています。詳細については、 [TiDBでSQLを探求しよう](/basic-sql-operations.md)参照してください。

TiDB は MySQL と互換性があり、ほとんどの場合、MySQL ステートメントを直接使用できます。サポートされていない機能については、 [MySQLとの互換性](/mysql-compatibility.md#unsupported-features)を参照してください。

SQL を試して、MySQL クエリと TiDB の互換性をテストするには、 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=basic-sql-operations)試すことができます。最初に[TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-starter-instance)、その中で SQL ステートメントを実行することもできます。

このページでは、DDL、DML、CRUD 操作などの基本的なTiDB SQLステートメントについて説明します。 TiDB ステートメントの完全なリストについては、 [SQLステートメントの概要](/sql-statements/sql-statement-overview.md)参照してください。

## カテゴリ {#category}

SQLは、その関数に応じて以下の4種類に分類されます。

-   **DDL（データ定義言語）** ：データベース、テーブル、ビュー、インデックスなどのデータベースオブジェクトを定義するために使用されます。

-   **DML（データ操作言語）** ：アプリケーション関連のレコードを操作するために使用されます。

-   **DQL（データクエリ言語）** ：条件付きフィルタリング後にレコードをクエリするために使用されます。

-   **DCL（データ制御言語）** ：アクセス権限とセキュリティレベルを定義するために使用されます。

以下では主にDMLとDQLについて紹介します。 DDL と DCL の詳細については、 [TiDBでSQLを探求しよう](/basic-sql-operations.md)または[SQLステートメントの概要](/sql-statements/sql-statement-overview.md)参照してください。

## データ操作言語 {#data-manipulation-language}

一般的な DML 機能には、テーブル レコードの追加、変更、削除があります。対応するコマンドは`INSERT` 、 `UPDATE` 、 `DELETE` 。

テーブルにデータを挿入するには、 `INSERT`ステートメントを使用します。

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

いくつかのフィールドのデータを含むレコードをテーブルに挿入するには、 `INSERT`ステートメントを使用します。

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、 `UPDATE`ステートメントを使用します。

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、 `DELETE`ステートメントを使用します。

```sql
DELETE FROM person WHERE id=2;
```

> **注記：**
>
> `UPDATE`および`DELETE`ステートメントは、フィルターとして`WHERE`句を指定しない場合、テーブル全体に対して動作します。

## データクエリ言語 {#data-query-language}

DQLは、テーブルまたは複数のテーブルから目的のデータ行を取得するために使用されます。

データを表形式で表示するには、 `SELECT`ステートメントを使用します。

```sql
SELECT * FROM person;
```

特定の列をクエリするには、 `SELECT`キーワードの後に​​列名を追加します。

```sql
SELECT name FROM person;
```

結果は以下のとおりです。

    +------+
    | name |
    +------+
    | tom  |
    +------+
    1 rows in set (0.00 sec)

`WHERE`句を使用して、条件に一致するすべてのレコードをフィルタリングし、結果を返します。

```sql
SELECT * FROM person WHERE id < 5;
```

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
