---
title: Vector Search Limitations
summary: TiDB ベクトル検索の制限について学習します。
---

# ベクトル検索の制限 {#vector-search-limitations}

このドキュメントでは、TiDB ベクトル検索の既知の制限について説明します。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB セルフマネージド クラスターと[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでのみ使用できます。

## ベクトルデータ型の制限 {#vector-data-type-limitations}

-   [ベクター](/vector-search-data-types.md)最大 16383 次元をサポートします。
-   ベクトル データ型では、 `NaN` 、 `Infinity` 、または`-Infinity`値を格納できません。
-   ベクトル データ型では倍精度浮動小数点数を格納できません。ベクトル列に倍精度浮動小数点数を挿入または格納すると、TiDB はそれを単精度浮動小数点数に変換します。
-   ベクトル列は主キーとして、または主キーの一部として使用することはできません。
-   ベクター列は、一意のインデックスとして、または一意のインデックスの一部として使用することはできません。
-   ベクター列はパーティション キーとして、またはパーティション キーの一部として使用することはできません。
-   現在、TiDB はベクター列を他のデータ型 ( `JSON`や`VARCHAR`など) に変更することをサポートしていません。

## ベクトルインデックスの制限 {#vector-index-limitations}

[ベクトル検索の制限](/vector-search-index.md#restrictions)参照。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

<CustomContent platform="tidb">

-   データのバックアップと復元には、 BRの v8.4.0 以降のバージョンを使用していることを確認してください。ベクター データ型のテーブルを v8.4.0 より前の TiDB クラスターに復元することはサポートされていません。
-   TiDB データ移行 (DM) は、MySQL 9.0 ベクトル データ型の TiDB への移行または複製をサポートしていません。
-   TiCDC は、ベクター データ型をサポートしていないダウンストリームにベクター データを複製する場合、ベクター データ型を別の型に変更します。詳細については、 [ベクトルデータ型との互換性](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)参照してください。

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
-   [サポートポータルにアクセス](https://tidb.support.pingcap.com/)

</CustomContent>
