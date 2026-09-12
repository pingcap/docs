---
title: DESC SEQUENCE
summary: 描述序列的属性。
---

# DESC SEQUENCE

描述序列的属性。

## 语法 {#syntax}

```sql
DESC SEQUENCE <sequence_name>
```

| 参数 | 描述 |
|----------------|-----------------------------------------------------------------------------------------------------------------------------|
| sequence_name  | 要描述的序列名称。该命令会显示该序列的所有属性，包括起始值、间隔、当前值、创建时间戳、最后修改时间戳以及注释。 |

## 示例 {#examples}

```sql
-- Create a sequence
CREATE SEQUENCE seq;

-- Use the sequence in an INSERT statement
CREATE TABLE tmp(a int, b uint64, c int);
INSERT INTO tmp select 10,nextval(seq),20 from numbers(3);

-- Describe the sequence
DESC SEQUENCE seq;

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│  name  │  start │ interval │ current │         created_on         │         updated_on         │      comment     │
├────────┼────────┼──────────┼─────────┼────────────────────────────┼────────────────────────────┼──────────────────┤
│ seq    │      1 │        1 │       4 │ 2025-05-20 02:48:49.749338 │ 2025-05-20 02:49:14.302917 │ NULL             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```