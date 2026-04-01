---
title: SHARD_ROW_ID_BITS
summary: SHARD_ROW_ID_BITS属性について学びましょう。
---

# SHARD_ROW_ID_BITS {#shard-row-id-bits}

このドキュメントでは、暗黙的に[`_tidb_rowid`](/tidb-rowid.md)シャーディングされた後にシャードのビット数を設定するために使用される`SHARD_ROW_ID_BITS`テーブル属性を紹介します。

## コンセプト {#concept}

クラスタ化されていないプライマリキーまたはプライマリキーのないテーブルの場合、TiDB は自動的に生成された[`_tidb_rowid`](/tidb-rowid.md)暗黙の自動インクリメント行 ID として使用します。多数の`INSERT`操作が実行されると、データは単一のリージョンに書き込まれるため、書き込みホットスポットが発生します。

ホットスポットの問題を軽減するには、 `SHARD_ROW_ID_BITS`設定できます。行 ID は分散しており、データは複数の異なるリージョンに書き込まれます。

-   `SHARD_ROW_ID_BITS = 4` 16個のシャードを示します
-   `SHARD_ROW_ID_BITS = 6` 64個のシャードを示します
-   `SHARD_ROW_ID_BITS = 0`デフォルトの1シャードを示します

`SHARD_ROW_ID_BITS = S`設定すると、 `_tidb_rowid`の構造は次のようになります。

| サインビット | 破片の断片  | 自動インクリメントビット |
| ------ | ------ | ------------ |
| 1ビット   | `S`ビット | `63-S`ビット    |

-   自動インクリメントビットの値はTiKVに格納され、順次割り当てられます。値が割り当てられるたびに、次の値は1ずつ増加します。自動インクリメントビットの値が使い果たされると（つまり、最大値に達すると）、以降の自動割り当てはエラー`Failed to read auto-increment value from storage engine`で失敗します。
-   値の範囲は`_tidb_rowid`です。最終的に生成される値の最大ビット数は、シャードビット + 自動インクリメントビットなので、最大値は`(2^63)-1`です。

> **警告：**
>
> `_tidb_rowid`は TiDB によって暗黙的に割り当てられる内部行 ID です。すべての場合においてグローバルに一意であると想定しないでください。クラスタ化インデックスを使用しないパーティション テーブルの場合、 `ALTER TABLE ... EXCHANGE PARTITION`異なるパーティションに同じ`_tidb_rowid`値を残す可能性があります。詳細については、 [`_tidb_rowid`](/tidb-rowid.md)参照してください。

> **注記：**
>
> シャードビットの選択（ `S` ）：
>
> -   `_tidb_rowid`の合計ビット数は64であるため、シャードビットの数は自動インクリメントビットの数に影響します。シャードビットの数が増えると自動インクリメントビットの数は減り、その逆もまた然りです。したがって、自動インクリメント値のランダム性と利用可能な自動インクリメント領域のバランスを取る必要があります。
> -   ベストプラクティスは、シャードビットを`log(2, x)`に設定することです。ここで、 `x`クラスタ内のTiKVノードの数です。たとえば、TiDBクラスタに16個のTiKVノードがある場合、シャードビットを`log(2, 16)` （ `4`に相当）に設定することをお勧めします。すべてのリージョンが各TiKVノードに均等にスケジュールされた後、バルク書き込みの負荷をさまざまなTiKVノードに均等に分散して、リソース利用率を最大化できます。

<CustomContent platform="tidb">

使用方法の詳細については、 [ホットスポットの問題のトラブルシューティングガイド](/troubleshoot-hot-spot-issues.md#use-shard_row_id_bits-to-process-hotspots)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

使用方法の詳細については、 [ホットスポットの問題のトラブルシューティングガイド](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#use-shard_row_id_bits-to-process-hotspots)参照してください。

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
