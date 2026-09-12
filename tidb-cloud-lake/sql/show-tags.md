---
title: SHOW TAGS
summary: 列出当前租户中的标签定义。
---

# SHOW TAGS

列出当前租户中的标签定义。你也可以通过 `system.tags` 表查询标签定义。

另请参阅：[CREATE TAG](/tidb-cloud-lake/sql/create-tag.md)、[DROP TAG](/tidb-cloud-lake/sql/drop-tag.md)。

## 语法 {#syntax}

```sql
SHOW TAGS [ LIKE '<pattern>' | WHERE <expr> ] [ LIMIT <n> ]
```

## 输出列 {#output-columns}

| 列 | 描述 |
|------------------|------------------------------------------------------|
| `name`           | 标签名称                                             |
| `allowed_values` | 允许的值列表；如果允许任意值，则为 NULL |
| `comment`        | 标签描述                                      |
| `created_on`     | 创建时间戳                                   |

## 示例 {#examples}

显示所有标签：

```sql
SHOW TAGS;
```

按名称模式筛选标签：

```sql
SHOW TAGS LIKE 'env%';
```

使用 WHERE 条件筛选：

```sql
SHOW TAGS WHERE comment IS NOT NULL;
```

限制结果数量：

```sql
SHOW TAGS LIMIT 5;
```

使用系统表的等价查询：

```sql
SELECT * FROM system.tags;
```