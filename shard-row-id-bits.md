---
title: SHARD_ROW_ID_BITS
summary: Learn the SHARD_ROW_ID_BITS attribute.
---

# SHARD_ROW_ID_BITS {#shard-row-id-bits}

このドキュメントでは、暗黙的な`_tidb_rowid`がシャードされた後にシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS` table 属性を紹介します。

## コンセプト {#concept}

非クラスター化主キーを持つテーブル、または主キーがないテーブルの場合、TiDB は暗黙的な自動インクリメント行 ID を使用します。多数の`INSERT`操作が実行されると、データが 1 つのリージョンに書き込まれ、書き込みホット スポットが発生します。

ホット スポットの問題を軽減するには、 `SHARD_ROW_ID_BITS`を構成します。行 ID は分散されており、データは複数の異なるリージョンに書き込まれます。

-   `SHARD_ROW_ID_BITS = 4` 16 個のシャードを示します
-   `SHARD_ROW_ID_BITS = 6` 64 個のシャードを示します
-   `SHARD_ROW_ID_BITS = 0`デフォルトの 1 シャードを示します

<CustomContent platform="tidb">

使用方法の詳細については、 [ホットスポットの問題のトラブルシューティング ガイド](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

使用方法の詳細については、 [ホットスポットの問題のトラブルシューティング ガイド](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)を参照してください。

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
