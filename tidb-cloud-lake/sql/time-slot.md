---
title: TIME_SLOT
summary: 時刻を30分単位に丸めます。## Syntax。
---

# TIME_SLOT

時刻を30分単位に丸めます。

## Syntax {#syntax}

```sql
time_slot(<expr>)
```

## Arguments {#arguments}

| 引数 | 説明 |
| ----------- | ----------- |
| `<expr>`    | timestamp   |

## Return Type {#return-type}

`TIMESTAMP`。`YYYY-MM-DD hh:mm:ss.ffffff` 形式で返します。

## Examples {#examples}

```sql
SELECT
  time_slot('2023-11-12 09:38:18.165575');

┌─────────────────────────────────────────┐
│ time_slot('2023-11-12 09:38:18.165575') │
├─────────────────────────────────────────┤
│ 2023-11-12 09:30:00                     │
└─────────────────────────────────────────┘
```