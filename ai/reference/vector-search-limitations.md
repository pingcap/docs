---
title: Vector Search Limitations
summary: TiDB ベクトル検索の制限について学習します。
aliases: ['/tidb/stable/vector-search-limitations/','/tidb/dev/vector-search-limitations/','/tidbcloud/vector-search-limitations/']
---

# ベクトル検索の制限 {#vector-search-limitations}

このドキュメントでは、TiDB ベクトル検索の既知の制限について説明します。

> **注記：**
>
> -   ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。
> -   ベクトル検索機能は[TiDBセルフマネージド](/overview.md) 、 [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用可能です。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## ベクトルデータ型の制限 {#vector-data-type-limitations}

-   [ベクター](/ai/reference/vector-search-data-types.md)最大 16383 次元をサポートします。
-   ベクトル データ型では、 `NaN` 、 `Infinity` 、または`-Infinity`値を格納できません。
-   ベクトルデータ型は倍精度浮動小数点数を格納できません。ベクトル列に倍精度浮動小数点数を挿入または格納すると、TiDB はそれらを単精度浮動小数点数に変換します。
-   ベクター列は主キーとして、または主キーの一部として使用することはできません。
-   ベクター列は、一意のインデックスとして、または一意のインデックスの一部として使用することはできません。
-   ベクター列はパーティション キーとして、またはパーティション キーの一部として使用することはできません。
-   現在、TiDB はベクター列を他のデータ型 ( `JSON`や`VARCHAR`など) に変更することをサポートしていません。

## ベクトルインデックスの制限 {#vector-index-limitations}

[ベクトル検索の制限](/ai/reference/vector-search-index.md#restrictions)参照。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

ベクトル検索を使用する場合は、次の互換性の問題に注意してください。

-   TiDB Cloud の機能:

    -   [TiDB Cloudコンソールのデータ移行機能](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 、MySQL ベクトル データ型のTiDB Cloudへの移行または複製をサポートしていません。

-   TiDB セルフマネージド ツール:

    -   データのバックアップと復元には、v8.4.0 以降のバージョン[BR](/br/backup-and-restore-overview.md)を使用していることを確認してください。ベクトルデータ型のテーブルを v8.4.0 より前の TiDB クラスターに復元することはサポートされていません。
    -   [TiDB データ移行 (DM)](/dm/dm-overview.md)では、MySQL ベクトル データ型の TiDB への移行または複製はサポートされていません。
    -   [TiCDC](/ticdc/ticdc-overview.md)ベクターデータをベクターデータ型をサポートしていない下流に複製する場合、ベクターデータ型は別の型に変更されます。詳細については、 [ベクトルデータ型との互換性](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)参照してください。

## フィードバック {#feedback}

私たちはあなたのフィードバックを大切にしており、いつでもお手伝いいたします。

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)
