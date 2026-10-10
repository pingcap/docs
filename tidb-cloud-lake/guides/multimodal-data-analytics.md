---
title: マルチモーダルデータ分析
summary: CityDrive Intelligence は、すべての走行を動画として記録します。バックグラウンド処理ツールは動画ストリームをキーフレーム画像に分割し、各画像から豊富なマルチモーダル情報を抽出して `video_id` ごとに保存します。これらのシグナルには、リレーショナルメタデータ、JSON マニフェスト、行動タグ、ベクトル埋め込み、GPS トレースが含まれます。
---

# マルチモーダルデータ分析

CityDrive Intelligence は、すべての走行を動画として記録します。バックグラウンド処理ツールは動画ストリームをキーフレーム画像に分割し、各画像から豊富なマルチモーダル情報を抽出して `video_id` ごとに保存します。これらのシグナルには、リレーショナルメタデータ、JSON マニフェスト、行動タグ、ベクトル埋め込み、GPS トレースが含まれます。

このガイドセットでは、{{{ .lake }}} がそれらすべてのワークロードを 1 つの Warehouse に集約する方法を紹介します。コピー用ジョブも、追加の検索クラスターも不要です。

| ガイド | 内容 |
|-------|----------------|
| [SQL Analytics](/tidb-cloud-lake/guides/sql-analytics.md) | ベーステーブル、フィルター、テーブル結合、ウィンドウ、集約インデックス |
| [JSON & Search](/tidb-cloud-lake/guides/json-search.md) | `frame_metadata_catalog` をロード (load) し、Elasticsearch `QUERY()` を実行して、bitmap タグを関連付ける |
| [ベクトル検索](/tidb-cloud-lake/guides/vector-search-guide.md) | 埋め込みを永続化し、コサイン検索を実行して、リスクメトリクスを結合する |
| [Geo Analytics](/tidb-cloud-lake/guides/geo-analytics.md) | `GEOMETRY`、距離/ポリゴンフィルター、信号機との結合を使用する |
| [Lakehouse ETL](/tidb-cloud-lake/guides/lakehouse-etl.md) | 一度 stage し、共有テーブルに `COPY INTO` して、streams/tasks を追加する |

これらを順にたどることで、同じ識別子が従来の SQL からテキスト検索、ベクトル、地理空間、ETL へとどのように流れていくかを確認できます。すべては単一の CityDrive シナリオに基づいています。