---
title: DROP TAG
summary: 删除一个标签。如果某个对象仍在引用该标签，则无法删除。
---

# DROP TAG

删除一个标签。如果某个对象仍在引用该标签，则无法删除——你必须先从所有对象中取消设置该标签，或删除这些对象。

另请参阅：[CREATE TAG](/tidb-cloud-lake/sql/create-tag.md)、[SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

## 语法 {#syntax}

```sql
DROP TAG [ IF EXISTS ] <tag_name>
```

## 示例 {#examples}

```sql
-- Fails if the tag is still in use
DROP TAG env;
-- Error: Tag 'env' still has references

-- Remove the tag reference first
ALTER TABLE my_table UNSET TAG env;

-- Now it succeeds
DROP TAG env;
```

仅当标签存在时才删除该标签：

```sql
DROP TAG IF EXISTS env;
```