---
title: Vector Search Limitations
summary: TiDBベクトル検索の限界について理解しましょう。
aliases: ['/ja/tidb/stable/vector-search-limitations/','/ja/tidb/dev/vector-search-limitations/','/ja/tidbcloud/vector-search-limitations/']
---

# ベクトル検索の制限 {#vector-search-limitations}

この文書では、TiDBベクトル検索の既知の制限事項について説明します。

> **注記：**
>
> -   ベクトル検索機能はベータ版です。予告なく変更される場合があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)を報告してください。
> -   ベクトル検索機能は、 [TiDBセルフマネージド](/overview.md)[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential) 、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)で利用できます。TiDB Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBのバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## ベクトルデータ型の制限 {#vector-data-type-limitations}

-   それぞれ最大 16383 次元 [ベクター](/ai/reference/vector-search-data-types.md)サポートします。
-   ベクトルデータ型は、 `NaN` 、 `Infinity` 、または`-Infinity`の値を格納することはできません。
-   ベクトルデータ型は倍精度浮動小数点数を格納することはできません。ベクトル列に倍精度浮動小数点数を挿入または格納すると、TiDBはそれらを単精度浮動小数点数に変換します。
-   ベクトル列は、主キーとして、または主キーの一部として使用することはできません。
-   ベクトル列は、一意インデックスとして、または一意インデックスの一部として使用することはできません。
-   ベクトル列は、パーティションキーとして、またはパーティションキーの一部として使用することはできません。
-   現在、TiDB はベクトル列を他のデータ型 ( `JSON`や`VARCHAR`など) に変更することをサポートしていません。

## ベクトルインデックスの制限 {#vector-index-limitations}

[ベクトル検索制限](/ai/reference/vector-search-index.md#restrictions)参照してください。

## TiDBツールとの互換性 {#compatibility-with-tidb-tools}

ベクトル検索を使用する際は、以下の互換性の問題にご注意ください。

-   TiDB Cloudの機能：

    -   [TiDB Cloudコンソールのデータ移行機能](/tidb-cloud/migrate-from-mysql-using-data-migration.md)MySQL ベクター データ型のTiDB Cloudへの移行または複製をサポートしていません。

-   TiDBセルフマネージドツール：

    -   データのバックアップと復元には、 [BR](/br/backup-and-restore-overview.md)のバージョン8.4.0以降を使用していることを確認してください。ベクトルデータ型のテーブルをTiDBバージョン8.4.0より前のバージョンに復元することはサポートされていません。
    -   [TiDBデータ移行（DM）](/dm/dm-overview.md) MySQLベクトルデータ型をTiDBに移行または複製することをサポートしていません。
    -   [TiCDC](/ticdc/ticdc-overview.md)ベクトル データ タイプをサポートしていないダウンストリームにベクトル データをレプリケートすると、ベクトル データ タイプが別のタイプに変更されます。詳細については、 [ベクトルデータ型との互換性](/ticdc/ticdc-compatibility.md#compatibility-with-vector-data-types)を参照してください。

## フィードバック {#feedback}

お客様からのご意見を大切にし、いつでもお手伝いいたします。

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
