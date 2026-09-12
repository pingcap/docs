---
title: DROP SEQUENCE
summary: 从 {{{ .lake }}} 中删除现有的 sequence。
---

# DROP SEQUENCE

从 {{{ .lake }}} 中删除现有的 sequence。

## 语法 {#syntax}

```sql
DROP SEQUENCE [IF EXISTS] <sequence>
```

| 参数 | 描述 |
|--------------|-----------------------------------------|
| `<sequence>` | 要删除的 sequence 的名称。 |

## 示例 {#examples}

```sql
-- Delete a sequence named staff_id_seq
DROP SEQUENCE staff_id_seq;
```