---
title: Vector Search Limitations
summary: TiDB ベクトル検索の制限について学習します。
---

# ベクトル検索の制限 {#vector-search-limitations}

このドキュメントでは、TiDB Vector Search の既知の制限について説明します。

> **注記**
>
> TiDB Vector Search は、TiDB Self-Managed (TiDB &gt;= v8.4) および[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)でのみ使用できます。 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)では使用できません。

## ベクトルデータ型の制限 {#vector-data-type-limitations}

-   [ベクター](/tidb-cloud/vector-search-data-types.md)最大 16383 次元をサポートします。
-   ベクトル データ型では、 `NaN` 、 `Infinity` 、または`-Infinity`値を格納できません。
-   ベクトル データ型では倍精度浮動小数点数を格納できません。ベクトル列に倍精度浮動小数点数を挿入または格納すると、TiDB はそれを単精度浮動小数点数に変換します。
-   ベクトル列は、主キー、一意のインデックス、またはパーティション キーでは使用できません。ベクトル検索のパフォーマンスを高速化するには、 [ベクター検索インデックス](/tidb-cloud/vector-search-index.md)使用します。
-   テーブルには複数のベクトル列を含めることができます。ただし、 [テーブル内の列の総数の制限](/tidb-limitations.md#limitations-on-a-single-table)あります。
-   現在、TiDB はベクトル インデックスを持つベクトル列の削除をサポートしていません。このような列を削除するには、まずベクトル インデックスを削除し、次にベクトル列を削除します。
-   現在、TiDB はベクター列を`JSON`や`VARCHAR`などの他のデータ型に変更することをサポートしていません。

## ベクトルインデックスの制限 {#vector-index-limitations}

-   ベクトル インデックスはベクトル検索に使用されます。範囲クエリや等価クエリなどの他のクエリを高速化することはできません。したがって、ベクトル以外の列や複数のベクトル列にベクトル インデックスを作成することはできません。
-   テーブルには複数のベクトル インデックスを設定できます。ただし、 [テーブル内のインデックスの総数の制限](/tidb-limitations.md#limitations-on-a-single-table)しかありません。
-   同じ列に複数のベクトル インデックスを作成できるのは、異なる距離関数を使用する場合のみです。
-   現在、ベクトル インデックスの距離関数としてサポートされているのは`VEC_COSINE_DISTANCE()`と`VEC_L2_DISTANCE()`のみです。
-   現在、TiDB はベクトル インデックスを持つベクトル列の削除をサポートしていません。このような列を削除するには、まずベクトル インデックスを削除し、次にベクトル列を削除します。
-   現在、TiDB はベクトル インデックスを[見えない](/sql-statements/sql-statement-alter-index.md)に設定することをサポートしていません。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

-   TiDB Cloudコンソールのデータ移行機能では、MySQL 9.0 ベクトル データ型のTiDB Cloudへの移行または複製はサポートされていません。

## フィードバック {#feedback}

私たちはあなたのフィードバックを大切にしており、いつでもお手伝いいたします。

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルにアクセス](https://tidb.support.pingcap.com/)
