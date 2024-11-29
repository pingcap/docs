---
title: TiDB 2.1.4 Release Notes
summary: TiDB 2.1.4 および TiDB Ansible 2.1.4 は、2019 年 2 月 15 日にリリースされました。このリリースには、安定性、SQL オプティマイザー、統計、および実行エンジンの改善が含まれています。修正には、SQL オプティマイザー/エグゼキューター、サーバー、DDL、および TiKV に関する問題が含まれます。Lightning ツールの最適化には、メモリ使用量、チャンク分離の削除、I/O 同時実行の制限、バッチ データ インポートのサポート、および TiKV インポート モードでの自動圧縮が含まれます。さらに、TiKV の定期的なレベル 1 圧縮パラメーターを無効にし、インポート エンジンの数を制限するためのサポートが追加されました。Sync-diff-inspector は、TiDB 統計を使用してチャンクを分割できるようになりました。
---

# TiDB 2.1.4 リリースノート {#tidb-2-1-4-release-notes}

2019 年 2 月 15 日に、TiDB 2.1.4 がリリースされました。対応する TiDB Ansible 2.1.4 もリリースされました。TiDB 2.1.3 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `VALUES`関数が FLOAT 型を正しく処理しない問題を修正[＃9223](https://github.com/pingcap/tidb/pull/9223)
    -   一部のケースで Float を String にキャストしたときに誤った結果になる問題を修正[＃9227](https://github.com/pingcap/tidb/pull/9227)
    -   `FORMAT`関数が一部のケースで誤った結果になる問題を修正[＃9235](https://github.com/pingcap/tidb/pull/9235)
    -   場合によっては結合クエリを処理するときにpanic問題を修正[＃9264](https://github.com/pingcap/tidb/pull/9264)
    -   `VALUES`関数がENUM型を正しく処理しない問題を修正[＃9280](https://github.com/pingcap/tidb/pull/9280)
    -   一部のケースで`DATE_ADD`の間違った`DATE_SUB`の問題を修正[＃9284](https://github.com/pingcap/tidb/pull/9284)
-   サーバ
    -   「リロード権限成功」ログを最適化し、DEBUG レベル[＃9274](https://github.com/pingcap/tidb/pull/9274)に変更します。
-   DDL
    -   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`グローバル変数[＃9134](https://github.com/pingcap/tidb/pull/9134)に変更する
    -   いくつかの異常な状況で生成された列にインデックスを追加することによって発生するバグを修正[＃9289](https://github.com/pingcap/tidb/pull/9289)

## ティクヴ {#tikv}

-   TiKV [＃4146](https://github.com/tikv/tikv/pull/4146)閉じるときに重複書き込みの問題を修正
-   一部のケースでイベントリスナーの異常な結果の問題を修正[＃4132](https://github.com/tikv/tikv/pull/4132)

## ツール {#tools}

-   稲妻
    -   メモリ使用量を最適化する[＃107](https://github.com/pingcap/tidb-lightning/pull/107) , [＃108](https://github.com/pingcap/tidb-lightning/pull/108)
    -   ダンプファイルの余分な解析を避けるために、ダンプファイルのチャンク分離を削除します[＃109](https://github.com/pingcap/tidb-lightning/pull/109)
    -   ダンプファイルの読み取りのI/O同時実行を制限し、キャッシュミスが多すぎることによるパフォーマンスの低下を回避します[＃110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   インポートの安定性を向上させるために、単一のテーブルに対してデータを一括インポートする機能をサポート[＃110](https://github.com/pingcap/tidb-lightning/pull/113)
    -   TiKV [＃4199](https://github.com/tikv/tikv/pull/4199)のインポートモードで自動圧縮を有効にする
    -   TiKV クラスタバージョンが 2.1.4 以降の場合、レベル 1 圧縮はインポートモードで自動的に実行されるため、TiKV 定期的なレベル 1 圧縮パラメータを無効にすることをサポートします[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
    -   インポーターのディスク容量を過度に消費しないように、インポートエンジンの数を制限します[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
-   sync-diff-inspector [＃197](https://github.com/pingcap/tidb-tools/pull/197)の TiDB 統計を使用してチャンクを分割する機能をサポート
