---
title: DROP TAG
summary: タグを削除します。タグがいずれかのオブジェクトからまだ参照されている場合、そのタグは削除できません。
---

# DROP TAG

タグを削除します。タグがいずれかのオブジェクトからまだ参照されている場合、そのタグは削除できません。先にすべてのオブジェクトからそのタグを解除するか、それらのオブジェクトを削除する必要があります。

関連情報: [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md)、[SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

## 構文 {#syntax}

```sql
DROP TAG [ IF EXISTS ] <tag_name>
```

## 例 {#examples}

```sql
-- Fails if the tag is still in use
DROP TAG env;
-- Error: Tag 'env' still has references

-- Remove the tag reference first
ALTER TABLE my_table UNSET TAG env;

-- Now it succeeds
DROP TAG env;
```

タグが存在する場合にのみ削除します。

```sql
DROP TAG IF EXISTS env;
```