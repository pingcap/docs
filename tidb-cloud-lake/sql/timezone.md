---
title: TIMEZONE
summary: 現在の接続のタイムゾーンを返します。
---

# TIMEZONE

現在の接続のタイムゾーンを返します。

{{{ .lake }}} はデフォルトのタイムゾーンとして UTC（協定世界時）を使用しており、タイムゾーンを現在の地理的位置に変更できます。`timezone` 設定に指定できる値については、<https://docs.rs/chrono-tz/latest/chrono_tz/enum.Tz.html> を参照してください。詳細は以下の例を参照してください。

## 構文 {#syntax}

```
SELECT TIMEZONE();
```

## 例 {#examples}

```sql
-- Return the current timezone
SELECT TIMEZONE();

┌────────────┐
│ timezone() │
├────────────┤
│ UTC        │
└────────────┘

-- Set the timezone to China Standard Time
SET timezone='Asia/Shanghai';

SELECT TIMEZONE();

┌───────────────┐
│   timezone()  │
├───────────────┤
│ Asia/Shanghai │
└───────────────┘
```