---
title: LEFT
summary: 返回字符串 `str` 最左侧的 `len` 个字符；如果任一参数为 NULL，则返回 NULL。如果 `len` 大于 `str` 的长度，则返回整个 `str`。
---

# LEFT

返回字符串 `str` 最左侧的 `len` 个字符；如果任一参数为 NULL，则返回 NULL。如果 `len` 大于 `str` 的长度，则返回整个 `str`。

## 语法 {#syntax}

```sql
LEFT(<str>, <len>);
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|----------------------------------------------------------|
| `<str>`   | 要从中提取字符的主字符串 |
| `<len>`   | 字符数量 |

## 返回类型 {#return-type}

`VARCHAR`

## 示例 {#examples}

```sql
SELECT LEFT('foobarbar', 5), LEFT('foobarbar', 10);

┌──────────────────────────────────────────────┐
│ left('foobarbar', 5) │ left('foobarbar', 10) │
├──────────────────────┼───────────────────────┤
│ fooba                │ foobarbar             │
└──────────────────────────────────────────────┘
```