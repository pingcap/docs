---
title: Vector Search Integration Overview
summary: サポートされている AI フレームワーク、埋め込みモデル、ORM ライブラリを含む、TiDB ベクトル検索統合の概要。
---

# ベクトル検索統合の概要 {#vector-search-integration-overview}

このドキュメントでは、サポートされている AI フレームワーク、埋め込みモデル、オブジェクト リレーショナル マッピング (ORM) ライブラリなど、TiDB ベクトル検索統合の概要を説明します。

<CustomContent platform="tidb">

> **警告：**
>
> ベクトル検索機能は実験的です。本番環境での使用は推奨されません。この機能は予告なく変更される可能性があります。バグを見つけた場合は、GitHub で[問題](https://github.com/pingcap/tidb/issues)を報告できます。

</CustomContent>

> **注記：**
>
> ベクトル検索機能は、TiDB セルフマネージド クラスターと[TiDB Cloudサーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)クラスターでのみ使用できます。

## AIフレームワーク {#ai-frameworks}

TiDB は以下の AI フレームワークを公式にサポートしており、これらのフレームワークに基づいて開発された AI アプリケーションを TiDB Vector Search に簡単に統合できます。

| AIフレームワーク | チュートリアル                                                               |
| --------- | --------------------------------------------------------------------- |
| ランチェイン    | [ベクトル検索をLangChainと統合する](/vector-search-integrate-with-langchain.md)   |
| ラマインデックス  | [ベクトル検索をLlamaIndexと統合する](/vector-search-integrate-with-llamaindex.md) |

さらに、TiDB は、ドキュメントのstorageや AI アプリケーション用のナレッジ グラフのstorageなど、さまざまな目的に使用できます。

## モデルとサービスの埋め込み {#embedding-models-and-services}

TiDB Vector Search は、最大 16383 次元のベクトルの保存をサポートしており、ほとんどの埋め込みモデルに対応します。

ベクトルを生成するには、自己展開されたオープンソースの埋め込みモデルを使用するか、サードパーティの埋め込みプロバイダーが提供するサードパーティの埋め込み API を使用できます。

次の表に、いくつかの主要な埋め込みサービス プロバイダーと、対応する統合チュートリアルを示します。

| 埋め込みサービスプロバイダー | チュートリアル                                                                                 |
| -------------- | --------------------------------------------------------------------------------------- |
| ジナ・アイ          | [ベクトル検索をJina AI Embeddings APIと統合する](/vector-search-integrate-with-jinaai-embedding.md) |

## オブジェクトリレーショナルマッピング（ORM）ライブラリ {#object-relational-mapping-orm-libraries}

TiDB Vector Search を ORM ライブラリと統合して、TiDB データベースと対話することができます。

次の表に、サポートされている ORM ライブラリと対応する統合チュートリアルを示します。

<table><tr><th>言語</th><th>ORM/クライアント</th><th>インストール方法</th><th>チュートリアル</th></tr><tr><td rowspan="4">パイソン</td><td>TiDB ベクター クライアント</td><td><code>pip install tidb-vector[client]</code></td><td> <a href="/tidb/v8.5/vector-search-get-started-using-python">Python を使用したベクトル検索の開始</a></td></tr><tr><td>SQLアルケミー</td><td><code>pip install tidb-vector</code></td><td> <a href="/tidb/v8.5/vector-search-integrate-with-sqlalchemy">TiDB ベクトル検索を SQLAlchemy と統合する</a></td></tr><tr><td>ピーウィー</td><td><code>pip install tidb-vector</code></td><td> <a href="/tidb/v8.5/vector-search-integrate-with-peewee">TiDB Vector Search を peewee と統合する</a></td></tr><tr><td>ジャンゴ</td><td><code>pip install django-tidb[vector]</code></td><td> <a href="/tidb/v8.5/vector-search-integrate-with-django-orm">TiDB ベクトル検索を Django に統合する</a></td></tr></table>
