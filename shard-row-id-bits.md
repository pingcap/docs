---
title: SHARD_ROW_ID_BITS
summary: SHARD_ROW_ID_BITS 属性について学習します。
---

# シャード行IDビット {#shard-row-id-bits}

このドキュメントでは、暗黙の`_tidb_rowid`がシャードされた後のシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS`テーブル属性について説明します。

## コンセプト {#concept}

クラスター化されていない主キーを持つテーブル、または主キーのないテーブルの場合、TiDB は暗黙的な自動増分行 ID を使用します。 `INSERT`操作が大量に実行されると、データは単一のリージョンに書き込まれ、書き込みホットスポットが発生します。

ホットスポットの問題を軽減するには、 `SHARD_ROW_ID_BITS`設定します。行 ID が分散され、データが複数の異なるリージョンに書き込まれます。

-   `SHARD_ROW_ID_BITS = 4` 16個の破片を示す
-   `SHARD_ROW_ID_BITS = 6` 64個の破片を示す
-   `SHARD_ROW_ID_BITS = 0`デフォルトの1シャードを示します

<CustomContent platform="tidb">

使用方法の詳細については[ホットスポットの問題のトラブルシューティングガイド](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

使用方法の詳細については[ホットスポットの問題のトラブルシューティングガイド](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)を参照してください。

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
