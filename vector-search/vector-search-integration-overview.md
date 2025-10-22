---
title: Vector Search Integration Overview
summary: サポートされている AI フレームワーク、埋め込みモデル、ORM ライブラリなど、TiDB ベクトル検索統合の概要。
---

# ベクター検索統合の概要 {#vector-search-integration-overview}

このドキュメントでは、サポートされている AI フレームワーク、埋め込みモデル、オブジェクト リレーショナル マッピング (ORM) ライブラリなど、TiDB ベクトル検索統合の概要について説明します。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> ベクター検索機能はベータ版です。予告なく変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告を行ってください。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB Self-Managed、 [TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) [TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)利用できます[TiDB Cloud専用](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) Self-ManagedおよびTiDB Cloud Dedicatedの場合、TiDBバージョンはv8.4.0以降である必要があります（v8.5.0以降を推奨）。

## AIフレームワーク {#ai-frameworks}

TiDB は以下の AI フレームワークを公式にサポートしており、これらのフレームワークに基づいて開発された AI アプリケーションを TiDB Vector Search に簡単に統合できます。

| AIフレームワーク | チュートリアル                                                                             |
| --------- | ----------------------------------------------------------------------------------- |
| ランチェイン    | [LangChainとベクトル検索を統合する](/vector-search/vector-search-integrate-with-langchain.md)   |
| ラマインデックス  | [LlamaIndexとベクター検索を統合する](/vector-search/vector-search-integrate-with-llamaindex.md) |

さらに、TiDB は、ドキュメントのstorageや AI アプリケーション用のナレッジ グラフのstorageなど、さまざまな用途に使用できます。

## モデルとサービスの埋め込み {#embedding-models-and-services}

TiDB Vector Search は、最大 16383 次元のベクトルの保存をサポートしており、ほとんどの埋め込みモデルに対応します。

ベクトルを生成するには、自己展開されたオープンソースの埋め込みモデルを使用するか、サードパーティの埋め込みプロバイダーが提供するサードパーティの埋め込み API を使用できます。

次の表に、いくつかの主要な埋め込みサービス プロバイダーと、対応する統合チュートリアルを示します。

| 埋め込みサービスプロバイダー | チュートリアル                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------- |
| ジナ・アイ          | [Jina AI Embeddings APIとベクター検索を統合する](/vector-search/vector-search-integrate-with-jinaai-embedding.md) |

## オブジェクトリレーショナルマッピング（ORM）ライブラリ {#object-relational-mapping-orm-libraries}

TiDB Vector Search を ORM ライブラリと統合して、TiDB データベースと対話することができます。

次の表に、サポートされている ORM ライブラリと対応する統合チュートリアルを示します。

<table><tr><th>言語</th><th>ORM/クライアント</th><th>インストール方法</th><th>チュートリアル</th></tr><tr><td rowspan="4">パイソン</td><td>TiDB ベクタークライアント</td><td><code>pip install tidb-vector[client]</code></td><td> <a href="/tidb/v8.5/vector-search-get-started-using-python">Pythonを使ったベクトル検索を始めよう</a></td></tr><tr><td>SQLアルケミー</td><td><code>pip install tidb-vector</code></td><td> <a href="/tidb/v8.5/vector-search-integrate-with-sqlalchemy">TiDBベクトル検索をSQLAlchemyと統合する</a></td></tr><tr><td>ピーウィー</td><td><code>pip install tidb-vector</code></td><td> <a href="/tidb/v8.5/vector-search-integrate-with-peewee">TiDBベクトル検索をpeeweeと統合する</a></td></tr><tr><td>ジャンゴ</td><td><code>pip install django-tidb[vector]</code></td><td> <a href="/tidb/v8.5/vector-search-integrate-with-django-orm">TiDBベクトル検索をDjangoに統合する</a></td></tr></table>
