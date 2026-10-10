---
title: DROP SNAPSHOT TAG
summary: FUSE テーブルから名前付きスナップショットタグを削除します。これにより、他のタグや保持ポリシーで保護されていない場合、参照されていたスナップショットはガベージコレクションの対象になります。
---

# DROP SNAPSHOT TAG

FUSE テーブルから名前付きスナップショットタグを削除します。削除されると、他のタグや保持ポリシーで保護されていない場合、参照されていたスナップショットはガベージコレクションの対象になります。

> **Note:**
>
> - これは**実験的**機能です。使用する前に、まず `SET enable_experimental_table_ref = 1;` を有効にしてください。
> - FUSE エンジンのテーブルでのみサポートされます。

## 構文 {#syntax}

```sql
ALTER TABLE [<database_name>.]<table_name> DROP TAG <tag_name>
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| tag_name  | 削除するスナップショットタグの名前です。タグが存在しない場合はエラーが返されます。 |

## 例 {#examples}

```sql
SET enable_experimental_table_ref = 1;

CREATE TABLE t1(a INT, b STRING);
INSERT INTO t1 VALUES (1, 'a'), (2, 'b');

-- Create and then drop a tag
ALTER TABLE t1 CREATE TAG v1_0;
ALTER TABLE t1 DROP TAG v1_0;

-- Querying a dropped tag returns an error
SELECT * FROM t1 AT (TAG => v1_0);
-- Error: tag 'v1_0' not found
```