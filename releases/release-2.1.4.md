---
title: TiDB 2.1.4 Release Notes
---

# TiDB 2.1.4 リリースノート {#tidb-2-1-4-release-notes}

2019 年 2 月 15 日に、TiDB 2.1.4 がリリースされました。対応する TiDB Ansible 2.1.4 もリリースされています。 TiDB 2.1.3 と比較して、このリリースでは、安定性、SQL オプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `VALUES`関数が FLOAT 型を正しく処理しない問題を修正[#9223](https://github.com/pingcap/tidb/pull/9223)
    -   場合によっては Float を String にキャストするときの間違った結果の問題を修正します[#9227](https://github.com/pingcap/tidb/pull/9227)
    -   場合によっては`FORMAT`関数の間違った結果の問題を修正します[#9235](https://github.com/pingcap/tidb/pull/9235)
    -   場合によっては、結合クエリを処理する際のpanicの問題を修正します[#9264](https://github.com/pingcap/tidb/pull/9264)
    -   `VALUES`関数が ENUM 型を正しく処理しない問題を修正[#9280](https://github.com/pingcap/tidb/pull/9280)
    -   場合によっては`DATE_ADD` / `DATE_SUB`の間違った結果の問題を修正[#9284](https://github.com/pingcap/tidb/pull/9284)
-   サーバ
    -   「リロード権限成功」ログを最適化し、DEBUGレベル[#9274](https://github.com/pingcap/tidb/pull/9274)に変更
-   DDL
    -   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`をグローバル変数[#9134](https://github.com/pingcap/tidb/pull/9134)に変更します。
    -   いくつかの異常な状態で生成された列にインデックスを追加することによって引き起こされるバグを修正します[#9289](https://github.com/pingcap/tidb/pull/9289)

## TiKV {#tikv}

-   TiKV [#4146](https://github.com/tikv/tikv/pull/4146)を閉じる際の重複書き込みの問題を修正
-   場合によってはイベントリスナーの結果が異常になる問題を修正[#4132](https://github.com/tikv/tikv/pull/4132)

## ツール {#tools}

-   雷
    -   メモリ使用量を最適化する[#107](https://github.com/pingcap/tidb-lightning/pull/107) , [#108](https://github.com/pingcap/tidb-lightning/pull/108)
    -   ダンプ ファイルの余分な解析を避けるために、ダンプ ファイルのチャンク分離を削除します[#109](https://github.com/pingcap/tidb-lightning/pull/109)
    -   キャッシュ ミスが多すぎることによるパフォーマンスの低下を避けるために、ダンプ ファイルの読み取りの I/O 同時実行数を制限します[#110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   インポートの安定性を向上させるために、単一のテーブルのバッチでのデータのインポートをサポートします[#110](https://github.com/pingcap/tidb-lightning/pull/113)
    -   TiKV [#4199](https://github.com/tikv/tikv/pull/4199)のインポート モードで自動圧縮を有効にする
    -   TiKV クラスターのバージョンが[#119](https://github.com/pingcap/tidb-lightning/pull/119)以降の場合、レベル 1 圧縮はインポート モードで自動的に実行されるため、TiKV の定期的なレベル 1 圧縮パラメーターの無効化をサポートします。
    -   インポート エンジンの数を制限して、インポーターのディスク容量を消費しすぎないようにする[#119](https://github.com/pingcap/tidb-lightning/pull/119)
-   sync-diff-inspector [#197](https://github.com/pingcap/tidb-tools/pull/197)で TiDB 統計を使用したチャンクの分割をサポート
