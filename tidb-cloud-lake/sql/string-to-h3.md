---
title: STRING_TO_H3
summary: 将字符串表示形式转换为 H3 (uint64) 表示形式。
---

# STRING_TO_H3

将字符串表示形式转换为 [H3](https://eng.uber.com/h3/)（uint64）表示形式。

## 语法 {#syntax}

```sql
STRING_TO_H3(h3)
```

## 示例 {#examples}

```sql
SELECT STRING_TO_H3('8d11aa6a38826ff');

┌─────────────────────────────────┐
│ string_to_h3('8d11aa6a38826ff') │
├─────────────────────────────────┤
│              635318325446452991 │
└─────────────────────────────────┘
```