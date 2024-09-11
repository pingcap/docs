---
title: CRUD SQL in TiDB
summary: TiDB の CURD SQL の簡単な紹介。
---

# TiDB の CRUD SQL {#crud-sql-in-tidb}

このドキュメントでは、TiDB の CURD SQL の使用方法を簡単に紹介します。

## 始める前に {#before-you-start}

TiDB クラスターに接続していることを確認してください。接続していない場合は、 [TiDB Cloudサーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)を参照してTiDB Cloud Serverless クラスターを作成してください。

## TiDB で SQL を探索する {#explore-sql-with-tidb}

> **注記：**
>
> この文書では[TiDB で SQL を探索する](/basic-sql-operations.md)参照して簡略化しています。詳細については[TiDB で SQL を探索する](/basic-sql-operations.md)を参照してください。

TiDB は MySQL と互換性があり、ほとんどの場合 MySQL ステートメントを直接使用できます。サポートされていない機能については、 [MySQLとの互換性](/mysql-compatibility.md#unsupported-features)参照してください。

SQL を試して、MySQL クエリと TiDB の互換性をテストするには、 [TiDB プレイグラウンド](https://play.tidbcloud.com/?utm_source=docs&#x26;utm_medium=basic-sql-operations)試すことができます。また、最初に TiDB クラスターをデプロイし、その中で SQL ステートメントを実行することもできます。

このページでは、DDL、DML、CRUD 操作などの基本的なTiDB SQLステートメントについて説明します。TiDB ステートメントの完全なリストについては、 [TiDB SQL構文図](https://pingcap.github.io/sqlgram/)を参照してください。

## カテゴリ {#category}

SQL は関数に応じて次の 4 つのタイプに分けられます。

-   **DDL (データ定義言語)** : データベース、テーブル、ビュー、インデックスなどのデータベース オブジェクトを定義するために使用されます。

-   **DML (データ操作言語)** : アプリケーション関連のレコードを操作するために使用されます。

-   **DQL (データ クエリ言語)** : 条件付きフィルタリング後にレコードをクエリするために使用されます。

-   **DCL (データ制御言語)** : アクセス権限とセキュリティ レベルを定義するために使用されます。

以下では主にDMLとDQLについて紹介します。DDLとDCLの詳細については[TiDB で SQL を探索する](/basic-sql-operations.md)または[TiDB SQL構文の詳細な説明](https://pingcap.github.io/sqlgram/)を参照してください。

## データ操作言語 {#data-manipulation-language}

一般的な DML 機能は、テーブル レコードの追加、変更、および削除です。対応するコマンドは`INSERT` 、 `UPDATE` 、および`DELETE`です。

テーブルにデータを挿入するには、 `INSERT`ステートメントを使用します。

```sql
INSERT INTO person VALUES(1,'tom','20170912');
```

いくつかのフィールドのデータを含むレコードをテーブルに挿入するには、次`INSERT`ステートメントを使用します。

```sql
INSERT INTO person(id,name) VALUES('2','bob');
```

テーブル内のレコードの一部のフィールドを更新するには、次`UPDATE`ステートメントを使用します。

```sql
UPDATE person SET birthday='20180808' WHERE id=2;
```

テーブル内のデータを削除するには、次`DELETE`ステートメントを使用します。

```sql
DELETE FROM person WHERE id=2;
```

> **注記：**
>
> フィルターとして`WHERE`節を使用しない`UPDATE`および`DELETE`ステートメントは、テーブル全体に対して動作します。

## データクエリ言語 {#data-query-language}

DQL は、1 つまたは複数のテーブルから必要なデータ行を取得するために使用されます。

テーブル内のデータを表示するには、 `SELECT`ステートメントを使用します。

```sql
SELECT * FROM person;
```

特定の列をクエリするには、 `SELECT`キーワードの後に列名を追加します。

```sql
SELECT name FROM person;
```

結果は以下のようになります。

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

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
