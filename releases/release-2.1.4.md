---
title: TiDB 2.1.4 Release Notes
summary: TiDB 2.1.4およびTiDB Ansible 2.1.4は、2019年2月15日にリリースされました。このリリースでは、安定性、SQLオプティマイザ、統計、実行エンジンが改善されています。SQLオプティマイザ/エグゼキュータ、サーバー、DDL、TiKVに関する問題が修正されています。Lightningツールの最適化には、メモリ使用量、チャンク分割の削除、I/O同時実行制限、バッチデータインポートのサポート、TiKVインポートモードでの自動圧縮が含まれます。さらに、TiKVの定期的なレベル1圧縮パラメータの無効化とインポートエンジン数の制限もサポートされました。Sync-diff-inspectorは、TiDB統計を使用したチャンク分割をサポートするようになりました。
---

# TiDB 2.1.4 リリースノート {#tidb-2-1-4-release-notes}

2019年2月15日にTiDB 2.1.4がリリースされました。対応するTiDB Ansible 2.1.4もリリースされました。このリリースでは、TiDB 2.1.3と比較して、安定性、SQLオプティマイザー、統計、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `VALUES`関数が FLOAT 型を正しく処理しない問題を修正[＃9223](https://github.com/pingcap/tidb/pull/9223)
    -   一部のケースで Float を String にキャストすると結果が間違ってしまう問題を修正[＃9227](https://github.com/pingcap/tidb/pull/9227)
    -   `FORMAT`関数が一部のケースで誤った結果を出す問題を修正[＃9235](https://github.com/pingcap/tidb/pull/9235)
    -   Joinクエリの処理時に発生するpanic問題を修正[＃9264](https://github.com/pingcap/tidb/pull/9264)
    -   `VALUES`関数がENUM型を正しく処理しない問題を修正[＃9280](https://github.com/pingcap/tidb/pull/9280)
    -   一部のケースで`DATE_ADD` `DATE_SUB`間違った結果の問題を修正[＃9284](https://github.com/pingcap/tidb/pull/9284)
-   サーバ
    -   「権限の再読み込み成功」ログを最適化し、DEBUGレベル[＃9274](https://github.com/pingcap/tidb/pull/9274)に変更します。
-   DDL
    -   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`グローバル変数[＃9134](https://github.com/pingcap/tidb/pull/9134)に変更する
    -   いくつかの異常な状況で生成された列にインデックスを追加することによって発生するバグを修正しました[＃9289](https://github.com/pingcap/tidb/pull/9289)

## TiKV {#tikv}

-   TiKV [＃4146](https://github.com/tikv/tikv/pull/4146)を閉じるときに重複書き込みの問題を修正
-   一部のケースでイベントリスナーの異常な結果の問題を修正[＃4132](https://github.com/tikv/tikv/pull/4132)

## ツール {#tools}

-   稲妻
    -   メモリ使用量を最適化する[＃107](https://github.com/pingcap/tidb-lightning/pull/107) , [＃108](https://github.com/pingcap/tidb-lightning/pull/108)
    -   ダンプファイルのチャンク分離を削除して、ダンプファイルの余分な解析を回避します[＃109](https://github.com/pingcap/tidb-lightning/pull/109)
    -   ダンプファイルの読み取りI/O同時実行を制限し、キャッシュミスが多すぎることによるパフォーマンスの低下を回避します[＃110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   インポートの安定性を向上させるために、単一のテーブルへのデータのバッチインポートをサポートします[＃110](https://github.com/pingcap/tidb-lightning/pull/113)
    -   TiKV [＃4199](https://github.com/tikv/tikv/pull/4199)のインポートモードで自動圧縮を有効にする
    -   TiKV クラスタバージョンが 2.1.4 以降の場合、インポートモードでレベル 1 圧縮が自動的に実行されるため、TiKV 定期的なレベル 1 圧縮パラメータを無効にすることをサポートします[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
    -   インポーターのディスク容量を過度に消費しないようにインポートエンジンの数を制限する[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
-   sync-diff-inspector [＃197](https://github.com/pingcap/tidb-tools/pull/197)の TiDB 統計を使用したチャンクの分割をサポート
