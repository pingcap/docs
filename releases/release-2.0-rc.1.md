---
title: TiDB 2.0 RC1 Release Notes
summary: TiDB 2.0 RC1, released on March 9, 2018, brings improvements in MySQL compatibility, SQL optimization, and stability. Key updates include memory usage limitation for SQL statements, Stream Aggregate operator support, configuration file validation, and HTTP API for configuration information. TiDB also enhances MySQL syntax compatibility, optimizer, and Boolean field length. PD sees logic and performance optimizations, while TiKV fixes gRPC call and adds gRPC APIs for metrics. Additionally, TiKV checks SSD usage, optimizes read performance, and improves metrics usage.
---

# TiDB 2.0 RC1 リリースノート {#tidb-2-0-rc1-release-notes}

2018 年 3 月 9 日に、TiDB 2.0 RC1 がリリースされました。このリリースでは、MySQL 互換性、SQL 最適化、安定性が大幅に向上しています。

## ティビ {#tidb}

-   OOMのリスクを軽減するために、単一のSQL文によるメモリ使用量の制限をサポートします。
-   Stream Aggregate 演算子を TiKV にプッシュダウンするサポート
-   構成ファイルの検証をサポート
-   HTTP API 経由で TiDB 構成情報を取得する機能をサポート
-   パーサーのより多くのMySQL構文と互換性がある
-   Navicatとの互換性を向上
-   オプティマイザを改良し、複数のOR条件を持つ共通式を抽出して、より良いクエリプランを選択する
-   オプティマイザを改善し、より多くのシナリオでサブクエリを結合演算子に変換して、より優れたクエリプランを選択します。
-   バッチモードでロックを解決してガベージコレクションの速度を上げる
-   互換性を向上させるためにブールフィールドの長さを修正しました
-   インデックス追加操作を最適化し、すべての書き込みおよび読み取り操作の優先度を低くして、オンラインビジネスへの影響を軽減します。

## PD {#pd}

-   リージョンステータスを確認するために使用されるコードのロジックを最適化してパフォーマンスを向上します
-   異常時のログ情報の出力を最適化し、デバッグを容易にします。
-   TiKVノードのディスク容量が不足しているというモニター統計を修正
-   TLS が有効になっている場合のヘルス インターフェースの誤ったレポートの問題を修正しました
-   安定性を向上させるために、レプリカの同時追加が構成のしきい値を超える可能性がある問題を修正しました。

## ティクヴ {#tikv}

-   PDリーダーが切り替わってもgRPC呼び出しがキャンセルされない問題を修正
-   初期設定後に変更できない重要な設定を保護する
-   メトリクスを取得するために使用されるgRPC APIを追加する
-   クラスターを起動するときにSSDが使用されているかどうかを確認する
-   ReadPoolを使用して読み取りパフォーマンスを最適化し、 `raw get`テストでパフォーマンスを30%向上
-   指標を改善し、指標の使用を最適化する
