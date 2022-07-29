---
title: CRUD SQL in TiDB
summary: A brief introduction to TiDB's CURD SQL.
---

# TiDBのCRUDSQL {#crud-sql-in-tidb}

このドキュメントでは、TiDBのCURDSQLの使用方法を簡単に紹介します。

## 始める前に {#before-you-start}

TiDBクラスタに接続していることを確認してください。そうでない場合は、 [TiDB CloudでTiDBクラスターを構築する（DevTier）](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster)を参照して無料のクラスタを作成します。

## TiDBでSQLを探索する {#explore-sql-with-tidb}

> **ノート：**
>
> このドキュメントでは、 [TiDBでSQLを探索する](/basic-sql-operations.md)を参照して簡略化しています。詳細については、 [TiDBでSQLを探索する](/basic-sql-operations.md)を参照してください。

TiDBはMySQLと互換性があり、ほとんどの場合、MySQLステートメントを直接使用できます。サポートされていない機能については、 [MySQLとの互換性](/mysql-compatibility.md#unsupported-features)を参照してください。

SQLを試し、MySQLクエリとのTiDBの互換性をテストするには、次のことができます[TiDBをインストールせずにWebブラウザで直接実行する](https://tour.tidb.io/) 。最初にTiDBクラスタをデプロイしてから、その中でSQLステートメントを実行することもできます。

このページでは、DDL、DML、CRUD操作などの基本的なTiDB SQLステートメントについて説明します。 TiDBステートメントの完全なリストについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/)を参照してください。

## カテゴリー {#category}

SQLは、その関数に応じて次の4つのタイプに分類されます。

-   **DDL（データ定義言語）** ：データベース、テーブル、ビュー、インデックスなどのデータベースオブジェクトを定義するために使用されます。

-   **DML（データ操作言語）** ：アプリケーション関連のレコードを操作するために使用されます。

-   **DQL（データクエリ言語）** ：条件付きフィルタリング後にレコードをクエリするために使用されます。

-   **DCL（データ制御言語）** ：アクセス特権とセキュリティレベルを定義するために使用されます。

以下は主にDMLとDQLを紹介します。 DDLとDCLの詳細については、 [TiDBでSQLを探索する](/basic-sql-operations.md)または[TiDB SQL構文の詳細な説明](https://pingcap.github.io/sqlgram/)を参照してください。

## データ操作言語 {#data-manipulation-language}

一般的なDML機能は、テーブルレコードの追加、変更、および削除です。対応するコマンドは、 `INSERT` 、および`UPDATE` `DELETE` 。

テーブルにデータを挿入するには、次の`INSERT`のステートメントを使用します。

{{< copyable "" >}}

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

一部のフィールドのデータを含むレコードをテーブルに挿入するには、 `INSERT`ステートメントを使用します。

{{< copyable "" >}}

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、 `UPDATE`ステートメントを使用します。

{{< copyable "" >}}

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、次の`DELETE`のステートメントを使用します。

{{< copyable "" >}}

```sql
DELETE FROM person WHERE id=2;
```

> **ノート：**
>
> フィルタとして`WHERE`句を含まない`UPDATE`および`DELETE`ステートメントは、テーブル全体で機能します。

## データクエリ言語 {#data-query-language}

DQLは、1つまたは複数のテーブルから目的のデータ行を取得するために使用されます。

テーブル内のデータを表示するには、次の`SELECT`のステートメントを使用します。

{{< copyable "" >}}

```sql
SELECT * FROM person;
```

特定の列を照会するには、 `SELECT`キーワードの後に列名を追加します。

{{< copyable "" >}}

```sql
SELECT name FROM person;
```

結果は次のとおりです。

```
+------+
| name |
+------+
| tom  |
+------+
1 rows in set (0.00 sec)
```

`WHERE`句を使用して、条件に一致するすべてのレコードをフィルタリングし、結果を返します。

{{< copyable "" >}}

```sql
SELECT * FROM person WHERE id < 5;
```
