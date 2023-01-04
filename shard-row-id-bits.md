---
title: SHARD_ROW_ID_BITS
summary: Learn the SHARD_ROW_ID_BITS attribute.
---

# SHARD_ROW_ID_BITS {#shard-row-id-bits}

このドキュメントでは、暗黙の`_tidb_rowid`がシャードされた後にシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS`テーブル属性を紹介します。

## 概念 {#concept}

整数でない主キーまたは主キーがないテーブルの場合、TiDB は暗黙的な自動インクリメント行 ID を使用します。多数の`INSERT`操作が実行されると、データは単一のリージョンに書き込まれ、書き込みホット スポットが発生します。

ホット スポットの問題を軽減するために、 `SHARD_ROW_ID_BITS`を構成できます。行 ID は分散しており、データは複数の異なるリージョンに書き込まれます。

-   `SHARD_ROW_ID_BITS = 4`は 16 個のシャードを示します
-   `SHARD_ROW_ID_BITS = 6`は 64 個のシャードを示します
-   `SHARD_ROW_ID_BITS = 0`はデフォルトの 1 シャードを示します

## 例 {#examples}

-   `CREATE TABLE` : `CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;`
-   `ALTER TABLE` : `ALTER TABLE t SHARD_ROW_ID_BITS = 4;`
