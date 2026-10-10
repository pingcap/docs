---
title: system.caches
summary: {{{ .lake }}} で管理されるさまざまなキャッシュの概要。
---

# system.caches

使用状況およびヒット率の統計を含む、{{{ .lake }}} で管理される各種キャッシュの概要です。

## カラム {#columns}

| カラム    | 説明                                                              |
|-----------|--------------------------------------------------------------------------|
| node      | ノード名                                                            |
| name      | キャッシュ名（`system$set_cache_capacity` の最初のパラメーターと同じ）  |
| num_items | キャッシュされたエントリー数                                                 |
| size      | キャッシュされたエントリーのサイズ（`unit` に応じて件数またはバイト数）              |
| capacity  | 最大容量（`unit` に応じて件数またはバイト数）                    |
| unit      | `size` と `capacity` の単位: `count` または `bytes`                       |
| access    | キャッシュアクセスの総数                                           |
| hit       | キャッシュヒット数                                                     |
| miss      | キャッシュミス数                                                   |

## キャッシュ一覧 {#cache-list}

| キャッシュ名                                    | キャッシュされるオブジェクト                                      | 単位    | 備考   |
|----------------------------------------------|----------------------------------------------------|-------|-------|
| memory_cache_table_snapshot                  | テーブルスナップショット                                     | count | デフォルトで有効。通常はデフォルト容量で十分です |
| memory_cache_table_statistics                | テーブル統計情報                                   | count | |
| memory_cache_compact_segment_info            | 圧縮テーブルセグメントのメタデータ                  | bytes | |
| memory_cache_segment_statistics              | セグメントレベルの統計情報                           | bytes | |
| memory_cache_column_oriented_segment_info    | カラム指向セグメントのメタデータ                   | bytes | |
| disk_cache_column_data                       | ディスク上のカラムデータキャッシュ                          | bytes | `system$set_cache_capacity` では調整できません |
| memory_cache_bloom_index_filter              | ブルームフィルターデータ                                  | bytes | ブロックごと・カラムごとに 1 エントリーです。メモリ使用量は小さめです。ポイントルックアップのワークロードではヒット率を監視してください。 |
| memory_cache_bloom_index_file_meta_data      | ブルームフィルターのメタデータ                              | count | 各テーブルは、そのテーブルが持つブロック数と同数までエントリーをキャッシュできます。メモリ使用量は小さめです。ポイントルックアップのワークロードではヒット率を監視してください。 |
| memory_cache_inverted_index_file_meta_data   | 転置インデックスのメタデータ                            | count | |
| memory_cache_inverted_index_file             | 転置インデックスデータ                                | bytes | |
| memory_cache_vector_index_file_meta_data     | ベクトルインデックスのメタデータ                              | count | |
| memory_cache_vector_index_file               | ベクトルインデックスデータ                                  | bytes | |
| memory_cache_spatial_index_file_meta_data    | 空間インデックスのメタデータ                             | count | |
| memory_cache_spatial_index_file              | 空間インデックスデータ                                 | bytes | |
| memory_cache_virtual_column_file_meta_data   | 仮想カラムファイルのメタデータ                       | count | |
| memory_cache_prune_partitions                | パーティションプルーニングキャッシュ                            | count | デフォルトで有効です。決定的クエリのプルーニング結果をキャッシュします。プルーニングのテストでバイパスするには、容量を 0 に設定してください。 |
| memory_cache_parquet_meta_data               | Parquet ファイルのメタデータ                              | count | Hive テーブルやその他のソースで使用されます |
| memory_cache_iceberg_table                   | Iceberg テーブルのメタデータ                             | count | |

## 例 {#example}

```sql
SELECT * FROM system.caches;
```

すべてのキャッシュの使用率とヒット率を確認します。

```sql
SELECT
    node,
    name,
    capacity,
    if(unit = 'count', (num_items + 1) / (capacity + 1),
       unit = 'bytes', (size + 1) / (capacity + 1), -1) AS utilization,
    if(access = 0, 0, hit / access)  AS hit_rate,
    if(access = 0, 0, miss / access) AS miss_rate,
    num_items,
    size,
    unit,
    access,
    hit,
    miss
FROM system.caches;
```