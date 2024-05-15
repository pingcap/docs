---
title: Pre-GA release notes
summary: TiDB Pre-GA release on August 30, 2017, focuses on MySQL compatibility, SQL optimization, stability, and performance. TiDB introduces SQL query optimizer enhancements, MySQL compatibility, JSON type support, and memory consumption reduction. Placement Driver (PD) now supports manual leader change, while TiKV uses dedicated Rocksdb for Raft log storage and improves performance. TiDB Connector for Spark Beta Release implements predicates pushdown, aggregation pushdown, and range pruning, capable of running TPC+H queries.
---

# プレGAリリースノート {#pre-ga-release-notes}

2017 年 8 月 30 日に、TiDB Pre-GA がリリースされました。このリリースは、MySQL の互換性、SQL の最適化、安定性、パフォーマンスに重点を置いています。

## ティビ {#tidb}

-   SQL クエリ オプティマイザー:
    -   コストモデルを調整する
    -   インデックススキャンを使用して、両側に異なる型を持つ`compare`式を持つ`where`句を処理します。
    -   貪欲アルゴリズムに基づく結合したテーブルの再配置付けをサポート
-   MySQLとの互換性を高めるために多くの機能強化が導入されました
-   サポート`Natural Join`
-   JSONフィールドのクエリ、更新、インデックスを含むJSONタイプ（Experimental）をサポートします。
-   無駄なデータを削除して、エグゼキュータのメモリ消費量を削減します。
-   SQL ステートメントの優先順位の設定をサポートし、クエリの種類に応じて一部のステートメントの優先順位を自動的に設定します。
-   式のリファクタリングが完了し、速度が約30%向上しました

## 配置Driver（PD） {#placement-driver-pd}

-   PDクラスタのリーダーを手動で変更する機能をサポート

## ティクヴ {#tikv}

-   専用のRocksdbインスタンスを使用してRaftログを保存する
-   レプリカの削除を高速化するには`DeleteRange`使用します
-   コプロセッサーはより多くのプッシュダウン演算子をサポートするようになりました
-   パフォーマンスと安定性を向上

## Spark 用 TiDB コネクタ ベータ版リリース {#tidb-connector-for-spark-beta-release}

-   述語プッシュダウンを実装する
-   集約プッシュダウンを実装する
-   範囲プルーニングを実装する
-   ビューのサポートを必要とする 1 つのクエリを除き、TPC+H のフルセットを実行可能
