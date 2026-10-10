---
title: DROP AGGREGATING INDEX
summary: 既存の集約インデックスを削除します。集約インデックスを削除しても、関連するストレージブロックは削除されないことに注意してください。ブロックも削除するには、VACUUM TABLE コマンドを使用します。集約インデックス機能を無効にするには、enable_aggregating_index_scan を 0 に設定します。
---

# DROP AGGREGATING INDEX

既存の集約インデックスを削除します。集約インデックスを削除しても、関連するストレージブロックは削除されないことに注意してください。ブロックも削除するには、[VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md) コマンドを使用します。集約インデックス機能を無効にするには、`enable_aggregating_index_scan` を 0 に設定します。

## 構文 {#syntax}

```sql
DROP AGGREGATING INDEX <index_name>
```

## 例 {#examples}

この例では、*my_agg_index* という名前の集約インデックスを削除します。

```sql
DROP AGGREGATING INDEX my_agg_index;
```