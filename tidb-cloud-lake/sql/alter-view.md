---
title: ALTER VIEW
summary: 使用另一个 QUERY 修改现有视图。
---

# ALTER VIEW

为现有视图设置或移除标签。标签必须先通过 [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) 创建。完整说明请参见 [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

> **Note:**
>
> 不支持 `ALTER VIEW ... AS ...`。如需更改视图的查询或输出列，请改用 [CREATE OR REPLACE VIEW](/tidb-cloud-lake/sql/create-view.md)。

## 语法 {#syntax}

```sql
ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

## 示例 {#examples}

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
ALTER VIEW default.active_users UNSET TAG env, owner;
```