---
title: CREATE TRANSIENT TABLE
summary: Time Travel 用の履歴データを保存しないテーブルを作成します。
---

# CREATE TRANSIENT TABLE

Time Travel 用の履歴データを保存しないテーブルを作成します。

トランジェントテーブルは、データ保護やリカバリの仕組みを必要としない一時的なデータを保持するために使用されます。{{{ .lake }}} はトランジェントテーブルの履歴データを保持しないため、Time Travel 機能を使用してトランジェントテーブルの以前のバージョンをクエリできません。たとえば、SELECT 文の [AT](/tidb-cloud-lake/sql/at.md) 句はトランジェントテーブルでは機能しません。なお、トランジェントテーブルは引き続き [drop](/tidb-cloud-lake/sql/drop-table.md) および [undrop](/tidb-cloud-lake/sql/undrop-table.md) できます。

> **Note:**
>
> トランジェントテーブルに対する同時変更（書き込み操作を含む）は、データ破損を引き起こし、データが読み取れなくなる可能性があります。この不具合は現在修正中です。修正されるまでは、トランジェントテーブルに対する同時変更を避けてください。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] TRANSIENT TABLE
       [ IF NOT EXISTS ]
       [ <database_name>. ]<table_name>
       ...
```

省略された部分は [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) の構文に従います。

## 例 {#examples}

この例では、`visits` という名前のトランジェントテーブルを作成します。

```sql
CREATE TRANSIENT TABLE visits (
  visitor_id BIGINT
);
```