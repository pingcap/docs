---
title: system.copy_history
summary: コピー履歴に関する情報を含みます。
---

# system.copy_history

コピー履歴に関する情報を含みます。

## 構文 {#syntax}

```sql
SELECT * FROM copy_history('<table_name>');
```

- `table_name`: テーブル名です。

```sql
select * from copy_history('my_table');

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                          file_name                          │ content_length │        last_modified       │       etag       │
│                            String                           │     UInt64     │     Nullable(Timestamp)    │ Nullable(String) │
├─────────────────────────────────────────────────────────────┼────────────────┼────────────────────────────┼──────────────────┤
│ data_0199db4c843a70b2b81f115f01c8de97_0000_00000000.parquet │          10531 │ 2025-10-13 02:00:49.083208 │ NULL             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

`system.copy_history` の結果は、設定 `load_file_metadata_expire_hours` の影響を受けることに注意してください。デフォルト値は 24 時間です。