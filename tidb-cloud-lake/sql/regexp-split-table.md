---
title: REGEXP_SPLIT_TO_TABLE
summary: 使用正则表达式模式切分字符串，并将每个片段作为表返回。
---

# REGEXP_SPLIT_TO_TABLE

使用正则表达式模式切分字符串，并将每个片段作为表返回。

## 语法 {#syntax}

```sql
REGEXP_SPLIT_TO_TABLE(string, pattern [, flags text])
```

| 参数         | 描述                                                           |
|--------------|----------------------------------------------------------------|
| `string`     | 要切分的输入字符串（VARCHAR 类型）                             |
| `pattern`    | 用于切分的正则表达式模式（VARCHAR 类型）                       |
| `flags text` | 用于修改正则表达式行为的标记字符串。                           |

**支持的 `flags` 参数：**

通过组合以下字符，提供灵活的正则表达式配置选项，以控制匹配行为：

* `i`（不区分大小写）：模式匹配时忽略大小写。
* `c`（大小写敏感）：模式匹配区分大小写（默认行为）。
* `n` 或 `m`（多行）：启用多行模式。在此模式下，`^` 和 `$` 分别匹配字符串的开头和结尾，也匹配每一行的开头和结尾；点号 `.` 不匹配换行符。
* `s`（单行）：启用单行模式（也称为 dot-matches-newline）。在此模式下，点号 `.` 可以匹配任意字符，包括换行符。
* `x`（忽略空白）：忽略模式中的空白字符（提高模式可读性）。
* `q`（字面量）：将 `pattern` 视为字面量字符串，而不是正则表达式。

## 示例 {#examples}

### 基本行生成 {#basic-row-generation}

```sql
SELECT REGEXP_SPLIT_TO_TABLE('one,two,three', ',');
┌─────────┐
│ one     │
│ two     │
│ three   │
└─────────┘
```

### 日志解析 {#log-parsing}

```sql
SELECT REGEXP_SPLIT_TO_TABLE('ERR:404:File Not Found', ':');
┌──────────────────┐
│ ERR              │
│ 404              │
│ File Not Found   │
└──────────────────┘
```

### 使用 flag text {#with-flag-text}

```sql
SELECT regexp_split_to_table('One_Two_Three', '[_-]', 'i')

╭────────╮
│ One    │
│ Two    │
│ Three  │
╰────────╯

```

### 嵌套用法 {#nested-usage}

```sql
WITH data AS (
  SELECT 'id=123,name=John' AS kv_pairs
)
SELECT
  REGEXP_SPLIT_TO_TABLE(kv_pairs, ',') AS pair
FROM data;
┌──────────────┐
│ id=123       │
│ name=John    │
└──────────────┘
```

## 另请参阅 {#see-also}

- [SPLIT](/tidb-cloud-lake/sql/split.md)：用于简单字符串切分
- [REGEXP_SPLIT_TO_ARRAY](/tidb-cloud-lake/sql/regexp-split-array.md)：将字符串切分为数组