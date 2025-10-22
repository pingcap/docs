---
title: Improve Vector Search Performance
summary: TiDB Vector Search のパフォーマンスを向上させるためのベスト プラクティスを学びます。
---

# ベクトル検索のパフォーマンスを向上させる {#improve-vector-search-performance}

TiDB Vector Searchを使用すると、画像、ドキュメント、その他の入力に類似した結果を検索する近似近傍法（ANN）クエリを実行できます。クエリのパフォーマンスを向上させるには、以下のベストプラクティスを確認してください。

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

## ベクトル列にベクトル検索インデックスを追加する {#add-vector-search-index-for-vector-columns}

[ベクター検索インデックス](/vector-search/vector-search-index.md) 、リコール率がわずかに低下するだけのトレードオフで、ベクトル検索クエリのパフォーマンスを通常 10 倍以上大幅に向上させます。

## ベクトルインデックスが完全に構築されていることを確認する {#ensure-vector-indexes-are-fully-built}

大量のベクターデータを挿入すると、その一部がデルタレイヤーに保持され、永続化を待機している可能性があります。このようなデータのベクターインデックスは、データが永続化された後に構築されます。すべてのベクターデータがインデックス化されるまで、ベクター検索のパフォーマンスは最適ではありません。インデックス構築の進行状況を確認するには、 [インデックス構築の進行状況をビュー](/vector-search/vector-search-index.md#view-index-build-progress)参照してください。

## ベクトルの次元を減らすか埋め込みを短くする {#reduce-vector-dimensions-or-shorten-embeddings}

ベクトルの次元が大きくなるにつれて、ベクトル検索のインデックス作成とクエリの計算の複雑さが大幅に増加し、より多くの浮動小数点の比較が必要になります。

パフォーマンスを最適化するには、可能な限りベクトル次元を減らすことを検討してください。これは通常、別の埋め込みモデルへの切り替えが必要になります。モデルを切り替える際には、モデルの変更がベクトルクエリの精度に与える影響を評価する必要があります。

OpenAI `text-embedding-3-large`などの特定の埋め込みモデルは[埋め込みの短縮](https://openai.com/index/new-embedding-models-and-api-updates/)サポートしています。これは、埋め込みの概念表現特性を失うことなく、ベクトルシーケンスの末尾からいくつかの数値を削除します。このような埋め込みモデルを使用して、ベクトルの次元を削減することもできます。

## 結果からベクター列を除外する {#exclude-vector-columns-from-the-results}

ベクトル埋め込みデータは通常サイズが大きく、検索プロセスでのみ使用されます。クエリ結果からベクトル列を除外することで、TiDBサーバーとSQLクライアント間で転送されるデータ量を大幅に削減し、クエリパフォーマンスを向上させることができます。

ベクター列を除外するには、 `SELECT *`使用してすべての列を取得するのではなく、 `SELECT`句で取得する列を明示的にリストします。

## インデックスをウォームアップする {#warm-up-the-index}

一度も使用されていない、または長期間アクセスされていないインデックス（コールドアクセス）にアクセスする場合、TiDBはインデックス全体をメモリではなくクラウドstorageまたはディスクから読み込む必要があります。このプロセスには時間がかかり、多くの場合、クエリのレイテンシーが長くなります。さらに、長期間（例えば数時間）SQLクエリが実行されない場合、コンピューティングリソースが再利用されるため、以降のアクセスはコールドアクセスになります。

このようなクエリのレイテンシーを回避するには、実際のワークロードの前に、ベクトル インデックスにヒットする同様のベクトル検索クエリを実行して、インデックスをウォームアップします。
