---
title: Vector Search Limitations
summary: TiDB ベクトル検索の制限について学習します。
---

# ベクトル検索の制限 {#vector-search-limitations}

このドキュメントでは、TiDB Vector Search の既知の制限について説明します。

> **注記**
>
> TiDB Vector Search は[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでのみ使用できます。TiDB TiDB Cloud Dedicated では使用できません。

## ベクトルデータ型の制限 {#vector-data-type-limitations}

-   [ベクター](/tidb-cloud/vector-search-data-types.md)最大 16383 次元をサポートします。
-   ベクトル データ型では、 `NaN` 、 `Infinity` 、または`-Infinity`値を格納できません。
-   ベクトル データ型では倍精度浮動小数点数を格納できません。ベクトル列に倍精度浮動小数点数を挿入または格納すると、TiDB はそれを単精度浮動小数点数に変換します。
-   ベクトル列は主キーとして、または主キーの一部として使用することはできません。
-   ベクター列は、一意のインデックスとして、または一意のインデックスの一部として使用することはできません。
-   ベクター列はパーティション キーとして、またはパーティション キーの一部として使用することはできません。
-   現在、TiDB はベクター列を他のデータ型 ( `JSON`や`VARCHAR`など) に変更することをサポートしていません。

## ベクトルインデックスの制限 {#vector-index-limitations}

[ベクトル検索の制限](/tidb-cloud/vector-search-index.md#restrictions)参照。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

-   TiDB Cloudコンソールのデータ移行機能では、MySQL 9.0 ベクトル データ型のTiDB Cloudへの移行または複製はサポートされていません。

## フィードバック {#feedback}

私たちはあなたのフィードバックを大切にしており、いつでもお手伝いいたします。

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルにアクセス](https://tidb.support.pingcap.com/)
