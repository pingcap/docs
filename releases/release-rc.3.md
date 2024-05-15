---
title: TiDB RC3 Release Notes
summary: TiDB RC3, released on June 16, 2017, focuses on MySQL compatibility, SQL optimization, stability, and performance. Highlights include refined privilege management, accelerated DDL, optimized load balancing, and open-sourced TiDB Ansible for easy cluster management. Detailed updates for TiDB, Placement Driver (PD), and TiKV include improved SQL query optimization, complete privilege management, support for HTTP API, system variables for query concurrency control, and more efficient data balance. PD supports gRPC, disaster recovery toolkit, and hot Region scheduling. TiKV supports gRPC, SST format snapshot, memory leak detection, and improved data importing speed. Overall, the release enhances performance, stability, and management capabilities.
---

# TiDB RC3 リリースノート {#tidb-rc3-release-notes}

2017 年 6 月 16 日に、TiDB RC3 がリリースされました。このリリースは、MySQL 互換性、SQL 最適化、安定性、パフォーマンスに重点を置いています。

## ハイライト {#highlight}

-   権限管理が改良され、ユーザーは MySQL と同じ方法でデータ アクセス権限を管理できるようになりました。
-   DDL が加速されます。
-   負荷分散ポリシーとプロセスはパフォーマンスのために最適化されています。
-   TiDB Ansible はオープンソースです。TiDB-Ansible を使用すると、ワンクリックで TiDB クラスターをデプロイ、アップグレード、起動、シャットダウンできます。

## 詳細な更新 {#detailed-updates}

## ティビ {#tidb}

-   SQL クエリ オプティマイザーでは、次の機能が追加または改善されています。
    -   増分統計をサポート
    -   `Merge Sort Join`オペレーターをサポート
    -   `Index Lookup Join`オペレーターをサポート
    -   `Optimizer Hint`構文をサポートする
    -   `Scan` `Aggregation`のメモリ消費`Join`最適化する
    -   コストベースオプティマイザー（CBO）フレームワークを最適化する
    -   リファクタリング`Expression`
-   より完全な権限管理をサポート
-   DDLアクセラレーション
-   HTTP APIを使用してテーブルのデータ分布情報を取得できるようになりました
-   システム変数を使用してクエリの同時実行を制御することをサポート
-   MySQL組み込み関数を追加する
-   システム変数を使用して、大きなトランザクションを小さなトランザクションに自動的に分割してコミットすることをサポートします。

## 配置Driver（PD） {#placement-driver-pd}

-   gRPC をサポート
-   災害復旧ツールキットを提供する
-   ガベージコレクションを使用して古いデータを自動的に消去する
-   より効率的なデータバランスをサポート
-   ホットリージョンスケジューリングをサポートし、負荷分散とデータインポートの高速化を実現します。
-   パフォーマンス
    -   クライアントTSOの取得を加速
    -   リージョンハートビート処理の効率を向上
-   `pd-ctl`機能を改善する
    -   レプリカ構成を動的に更新する
    -   タイムスタンプ Oracle (TSO) を取得する
    -   IDを使用してリージョン情報を取得する

## ティクヴ {#tikv}

-   gRPC をサポート
-   クラスターの負荷分散速度を向上させるために、Sorted String Table (SST) 形式のスナップショットをサポートします。
-   ヒーププロファイルを使用してメモリリークを発見するサポート
-   ストリーミングSIMD拡張（SSE）をサポートし、CRC32計算を高速化します。
-   リーダーの転送を高速化して負荷分散を高速化
-   バッチ適用を使用してCPU使用率を削減し、書き込みパフォーマンスを向上させる
-   トランザクション書き込み速度を向上させる並列プリライトをサポート
-   コプロセッサスレッドプールのスケジュールを最適化して、ポイント取得に対する大きなクエリの影響を軽減します。
-   新しいローダーは、テーブル レベルでのデータのインポートをサポートするほか、大きなテーブルを小さな論理ブロックに分割して同時にインポートすることで、データのインポート速度を向上させます。
