---
title: CRUD SQL in TiDB
summary: A brief introduction to TiDB's CURD SQL.
---

# TiDB の CRUD SQL {#crud-sql-in-tidb}

このドキュメントでは、TiDB の CURD SQL の使用方法を簡単に紹介します。

## 始める前に {#before-you-start}

TiDB クラスターに接続していることを確認してください。そうでない場合は、 [TiDB Cloud(Serverless Tier) で TiDBクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してServerless Tierクラスターを作成してください。

## TiDB で SQL を調べる {#explore-sql-with-tidb}

> **ノート：**
>
> このドキュメントでは、 [TiDB で SQL を調べる](/basic-sql-operations.md)参照して簡略化しています。詳細については、 [TiDB で SQL を調べる](/basic-sql-operations.md)を参照してください。

TiDB は MySQL と互換性があり、ほとんどの場合、MySQL ステートメントを直接使用できます。サポートされていない機能については、 [MySQL との互換性](/mysql-compatibility.md#unsupported-features)を参照してください。

SQL を試して、TiDB と MySQL クエリとの互換性をテストするには、 [TiDB をインストールせずに Web ブラウザーで直接実行する](https://tour.tidb.io/)ことができます。最初に TiDB クラスターをデプロイしてから、そこで SQL ステートメントを実行することもできます。

このページでは、DDL、DML、CRUD 操作などの基本的なTiDB SQLステートメントについて説明します。 TiDB ステートメントの完全なリストについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/)を参照してください。

## カテゴリー {#category}

SQL は、その関数によって次の 4 つのタイプに分けられます。

-   **DDL (データ定義言語)** : データベース、テーブル、ビュー、インデックスなどのデータベース オブジェクトを定義するために使用されます。

-   **DML (Data Manipulation Language)** : アプリケーション関連のレコードを操作するために使用されます。

-   **DQL (Data Query Language)** : 条件付きフィルタリングの後にレコードを照会するために使用されます。

-   **DCL (Data Control Language)** : アクセス権限とセキュリティ レベルを定義するために使用されます。

以下では主にDMLとDQLについて紹介します。 DDL および DCL の詳細については、 [TiDB で SQL を調べる](/basic-sql-operations.md)または[TiDB SQL構文の詳細な説明](https://pingcap.github.io/sqlgram/)を参照してください。

## データ操作言語 {#data-manipulation-language}

一般的な DML 機能は、テーブル レコードの追加、変更、および削除です。対応するコマンドは`INSERT` 、 `UPDATE` 、および`DELETE`です。

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

> **ノート：**
>
> フィルターとしての`WHERE`句のない`UPDATE`ステートメントと`DELETE`ステートメントは、テーブル全体に作用します。

## データクエリ言語 {#data-query-language}

DQL は、テーブルまたは複数のテーブルから目的のデータ行を取得するために使用されます。

テーブル内のデータを表示するには、 `SELECT`ステートメントを使用します。

```sql
SELECT * FROM person;
```

特定の列を照会するには、 `SELECT`キーワードの後に列名を追加します。

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

```sql
SELECT * FROM person WHERE id < 5;
```
