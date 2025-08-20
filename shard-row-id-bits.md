---
title: SHARD_ROW_ID_BITS
summary: SHARD_ROW_ID_BITS 属性について学習します。
---

# シャード行IDビット {#shard-row-id-bits}

このドキュメントでは、暗黙の`_tidb_rowid`シャードされた後のシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS`テーブル属性を紹介します。

## コンセプト {#concept}

非クラスター化主キーを持つテーブル、または主キーを持たないテーブルの場合、TiDBは暗黙的な自動インクリメント行IDを使用します。大量の`INSERT`操作が実行されると、データは単一のリージョンに書き込まれ、書き込みホットスポットが発生します。

ホットスポットの問題を軽減するには、 `SHARD_ROW_ID_BITS`設定します。行 ID が分散され、データが複数の異なるリージョンに書き込まれます。

-   `SHARD_ROW_ID_BITS = 4` 16個の破片を示す
-   `SHARD_ROW_ID_BITS = 6` 64個のシャードを示す
-   `SHARD_ROW_ID_BITS = 0`デフォルトの1シャードを示します

`SHARD_ROW_ID_BITS = S`設定すると、 `_tidb_rowid`の構造は次のようになります。

| 符号ビット | 破片の断片  | 自動インクリメントビット |
| ----- | ------ | ------------ |
| 1ビット  | `S`ビット | `63-S`ビット    |

-   自動インクリメントビットの値はTiKVに格納され、順次割り当てられます。値が割り当てられるたびに、次の値が1ずつ増加します。自動インクリメントビットは、列の値が`_tidb_rowid`場合、グローバルに一意であることを保証します。自動インクリメントビットの値が使い果たされると（つまり、最大値に達すると）、後続の自動割り当てはエラー`Failed to read auto-increment value from storage engine`で失敗します。
-   値の範囲は`_tidb_rowid` : 最終的に生成される値の最大ビット数 = シャード ビット + 自動インクリメント ビットなので、最大値は`(2^63)-1`です。

> **注記：**
>
> シャードビットの選択（ `S` ）：
>
> -   `_tidb_rowid`の合計ビット数は 64 であるため、シャードビット数は自動インクリメントビット数に影響します。シャードビット数が増加すると、自動インクリメントビット数は減少し、逆もまた同様です。したがって、自動インクリメント値のランダム性と利用可能な自動インクリメント領域のバランスをとる必要があります。
> -   ベストプラクティスは、シャードビットを`log(2, x)`に設定することです。ここで、 `x`クラスター内の TiKV ノードの数です。例えば、TiDB クラスターに TiKV ノードが 16 個ある場合、シャードビットを`log(2, 16)` （つまり`4`に設定することをお勧めします。すべてのリージョンが各 TiKV ノードに均等にスケジュールされると、一括書き込みの負荷を異なる TiKV ノードに均等に分散し、リソース使用率を最大化できます。

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
