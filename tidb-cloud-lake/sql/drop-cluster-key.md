---
title: DROP CLUSTER KEY
summary: テーブルのクラスターキーを削除します。
---

# DROP CLUSTER KEY

テーブルのクラスターキーを削除します。

関連情報: [ALTER CLUSTER KEY](/tidb-cloud-lake/sql/alter-cluster-key.md)

## 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <name> DROP CLUSTER KEY
```

## 例 {#examples}

このコマンドは、テーブル *test* のクラスターキーを削除します。

```sql
ALTER TABLE test DROP CLUSTER KEY
```