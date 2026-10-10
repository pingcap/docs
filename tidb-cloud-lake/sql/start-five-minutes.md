---
title: TO_START_OF_FIVE_MINUTES
summary: 時刻を含む日付（timestamp/datetime）を 5 分間隔の開始時刻に切り捨てます。## Syntax.
---

# TO_START_OF_FIVE_MINUTES

時刻を含む日付（timestamp/datetime）を 5 分間隔の開始時刻に切り捨てます。

## Syntax {#syntax}

```sql
TO_START_OF_FIVE_MINUTES(<expr>)
```

## Arguments {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<expr>`  | timestamp   |

## Return Type {#return-type}

`TIMESTAMP`。日付を `YYYY-MM-DD hh:mm:ss.ffffff` 形式で返します。

## Examples {#examples}

```sql
SELECT
  to_start_of_five_minutes('2023-11-12 09:38:18.165575')

┌────────────────────────────────────────────────────────┐
│ to_start_of_five_minutes('2023-11-12 09:38:18.165575') │
├────────────────────────────────────────────────────────┤
│ 2023-11-12 09:35:00                                    │
└────────────────────────────────────────────────────────┘
```