---
title: SHARD_ROW_ID_BITS
summary: Learn the SHARD_ROW_ID_BITS attribute.
---

# SHARD_ROW_ID_BITS {#shard-row-id-bits}

このドキュメントでは、暗黙の`_tidb_rowid`がシャーディングされた後にシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS`テーブル属性を紹介します。

## 概念 {#concept}

非整数の主キーがあるテーブルまたは主キーがないテーブルの場合、TiDBは暗黙の自動インクリメント行IDを使用します。 `INSERT`の操作を多数実行すると、データが1つのリージョンに書き込まれ、書き込みホットスポットが発生します。

ホットスポットの問題を軽減するために、 `SHARD_ROW_ID_BITS`を構成できます。行IDは分散しており、データは複数の異なるリージョンに書き込まれます。

-   `SHARD_ROW_ID_BITS = 4`は16個のシャードを示します
-   `SHARD_ROW_ID_BITS = 6`は64個のシャードを示します
-   `SHARD_ROW_ID_BITS = 0`はデフォルトの1シャードを示します

## 例 {#examples}

-   `CREATE TABLE` ： `CREATE TABLE t (c int) SHARD_ROW_ID_BITS = 4;`
-   `ALTER TABLE` ： `ALTER TABLE t SHARD_ROW_ID_BITS = 4;`
