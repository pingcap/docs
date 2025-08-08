---
title: Vector Search Limitations
summary: TiDB ベクトル検索の制限について学習します。
---

# ベクトル検索の制限 {#vector-search-limitations}

このドキュメントでは、TiDB ベクトル検索の既知の制限について説明します。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを見つけた場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB Self-Managed、 [TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) [TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## ベクトルデータ型の制限 {#vector-data-type-limitations}

-   [ベクター](/vector-search/vector-search-data-types.md)最大 16383 次元をサポートします。
-   ベクトル データ型では、 `NaN` 、 `Infinity` 、または`-Infinity`値を格納できません。
-   ベクトルデータ型は倍精度浮動小数点数を格納できません。ベクトル列に倍精度浮動小数点数を挿入または格納すると、TiDB はそれを単精度浮動小数点数に変換します。
-   ベクター列は主キーとして、または主キーの一部として使用することはできません。
-   ベクター列は、一意のインデックスとして、または一意のインデックスの一部として使用することはできません。
-   ベクター列はパーティション キーとして、またはパーティション キーの一部として使用することはできません。
-   現在、TiDB はベクター列を他のデータ型 ( `JSON`や`VARCHAR`など) に変更することをサポートしていません。

## ベクトルインデックスの制限 {#vector-index-limitations}

[ベクトル検索の制限](/vector-search/vector-search-index.md#restrictions)参照。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

<CustomContent platform="tidb">

-   データのバックアップとリストアには、 BRの v8.4.0 以降を使用してください。ベクトルデータ型のテーブルを v8.4.0 より前の TiDB クラスターにリストアすることはサポートされていません。
-   TiDB データ移行 (DM) は、MySQL 9.0 ベクトル データ型の TiDB への移行または複製をサポートしていません。
-   TiCDCは、ベクターデータ型をサポートしていない下流にベクターデータを複製する場合、ベクターデータ型を別の型に変更します。詳細については、 [ベクトルデータ型との互換性](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

-   TiDB Cloudコンソールのデータ移行機能では、MySQL 9.0 ベクトル データ型のTiDB Cloudへの移行または複製はサポートされていません。

</CustomContent>

## フィードバック {#feedback}

私たちはあなたのフィードバックを大切にしており、いつでもお手伝いいたします。

<CustomContent platform="tidb">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルをご覧ください](https://tidb.support.pingcap.com/)

</CustomContent>
