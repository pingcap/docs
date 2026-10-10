---
title: SYSTEM$SET_CACHE_CAPACITY
summary: 実行時に名前付きキャッシュの容量を調整します。
---

# SYSTEM$SET_CACHE_CAPACITY

実行時に、名前付きキャッシュの最大容量を設定します。変更は即座に反映されますが、**永続化されません**。そのため、再起動後は設定ファイル内の値に戻ります。

関連情報: [system.caches](/tidb-cloud-lake/sql/system-caches.md)

## 構文 {#syntax}

```sql
CALL system$set_cache_capacity('<cache_name>', <new_capacity>)
```

| パラメータ   | 説明                                                              |
|--------------|-------------------------------------------------------------------|
| cache_name   | キャッシュ名（[system.caches](/tidb-cloud-lake/sql/system-caches.md) のキャッシュ一覧を参照） |
| new_capacity | 新しい容量の値。単位（件数またはバイト）はキャッシュの種類によって異なります。                                                                 |

## 注意事項 {#notes}

- 新しい容量が現在の値より**大きい**場合、既存のキャッシュエントリは保持されます。
- 新しい容量が**小さい**場合、LRU ポリシーに従ってエントリが削除されることがあります。
- 変更は**永続化されません**。再起動後、容量は設定ファイルの値に戻ります。
- `disk_cache_column_data` はこのコマンドでは調整できません。

## 例 {#examples}

bloom index metadata cache を 5000 エントリに設定します。

```sql
CALL system$set_cache_capacity('memory_cache_bloom_index_file_meta_data', 5000);

┌────────────────────────┬────────┐
│ node                   │ result │
├────────────────────────┼────────┤
│ Gwo2DYOLZ9zAdYbGTWY9y6 │ Ok     │
└────────────────────────┴────────┘
```

テストのために partition pruning cache を無効化します。

```sql
CALL system$set_cache_capacity('memory_cache_prune_partitions', 0);
```