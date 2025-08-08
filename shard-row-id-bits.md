---
title: SHARD_ROW_ID_BITS
summary: SHARD_ROW_ID_BITS 属性について学習します。
---

# SHARD_ROW_ID_BITS {#shard-row-id-bits}

このドキュメントでは、暗黙の`_tidb_rowid`シャードされた後のシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS`テーブル属性を紹介します。

## コンセプト {#concept}

非クラスター化主キーを持つテーブル、または主キーを持たないテーブルの場合、TiDBは暗黙的な自動インクリメント行IDを使用します。大量の`INSERT`操作が実行されると、データは単一のリージョンに書き込まれ、書き込みホットスポットが発生します。

To mitigate the hot spot issue, you can configure `SHARD_ROW_ID_BITS`. The row IDs are scattered and the data are written into multiple different Regions.

-   `SHARD_ROW_ID_BITS = 4` 16個の破片を示す
-   `SHARD_ROW_ID_BITS = 6` indicates 64 shards
-   `SHARD_ROW_ID_BITS = 0`デフォルトの1シャードを示します

<CustomContent platform="tidb">

使用方法の詳細については[ホットスポットの問題のトラブルシューティングガイド](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

使用方法の詳細については[ホットスポットの問題のトラブルシューティングガイド](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)参照してください。

</CustomContent>

## 例 {#examples}

```sql
CREATE TABLE t (
    id INT PRIMARY KEY NONCLUSTERED
) SHARD_ROW_ID_BITS = 4;
```

```sql
ALTER TABLE t SHARD_ROW_ID_BITS = 4;
```
