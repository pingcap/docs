---
title: 字符串
summary: 基本的字符串数据类型。
---

# 字符串

## 字符串数据类型 {#string-data-types}

在 {{{ .lake }}} 中，字符串可以存储在 `VARCHAR` 字段中，其存储大小是可变的。

| 名称    | 别名 | 存储大小 |
|---------|---------|--------------|
| VARCHAR | STRING  | variable     |

## 函数 {#functions}

参见 [字符串函数](/tidb-cloud-lake/sql/string-functions-overview.md)。

## 示例 {#example}

```sql
CREATE TABLE string_table(text VARCHAR);
```

```
DESC string_table;
```

结果：

```
┌──────────────────────────────────────────────┐
│  Field │   Type  │  Null  │ Default │  Extra │
├────────┼─────────┼────────┼─────────┼────────┤
│ text   │ VARCHAR │ YES    │ NULL    │        │
└──────────────────────────────────────────────┘
```

```sql
INSERT INTO string_table VALUES('tidbcloudlake');
```

```
SELECT * FROM string_table;
```

结果：

```
┌──────────────────┐
│       text       │
├──────────────────┤
│ tidbcloudlake    │
└──────────────────┘
```