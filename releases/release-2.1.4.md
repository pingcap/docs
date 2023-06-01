---
title: TiDB 2.1.4 Release Notes
---

# TiDB 2.1.4 リリースノート {#tidb-2-1-4-release-notes}

2019 年 2 月 15 日に、TiDB 2.1.4 がリリースされました。対応する TiDB Ansible 2.1.4 もリリースされています。 TiDB 2.1.3 と比較して、このリリースでは安定性、SQL オプティマイザー、統計、実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   `VALUES`関数が FLOAT 型を正しく処理しない問題を修正[<a href="https://github.com/pingcap/tidb/pull/9223">#9223</a>](https://github.com/pingcap/tidb/pull/9223)
    -   場合によっては Float を String にキャストするときに間違った結果が発生する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/9227">#9227</a>](https://github.com/pingcap/tidb/pull/9227)
    -   場合によっては`FORMAT`関数の結果が間違っていた問題を修正[<a href="https://github.com/pingcap/tidb/pull/9235">#9235</a>](https://github.com/pingcap/tidb/pull/9235)
    -   場合によっては結合クエリを処理する際のpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/9264">#9264</a>](https://github.com/pingcap/tidb/pull/9264)
    -   `VALUES`関数が ENUM 型を正しく処理しない問題を修正[<a href="https://github.com/pingcap/tidb/pull/9280">#9280</a>](https://github.com/pingcap/tidb/pull/9280)
    -   場合によっては`DATE_ADD` / `DATE_SUB`という間違った結果が発生する問題を修正[<a href="https://github.com/pingcap/tidb/pull/9284">#9284</a>](https://github.com/pingcap/tidb/pull/9284)
-   サーバ
    -   「リロード権限成功」ログを最適化し、DEBUG レベル[<a href="https://github.com/pingcap/tidb/pull/9274">#9274</a>](https://github.com/pingcap/tidb/pull/9274)に変更します。
-   DDL
    -   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`をグローバル変数[<a href="https://github.com/pingcap/tidb/pull/9134">#9134</a>](https://github.com/pingcap/tidb/pull/9134)に変更します。
    -   一部の異常な状況で生成されたカラムにインデックスを追加することによって引き起こされるバグを修正[<a href="https://github.com/pingcap/tidb/pull/9289">#9289</a>](https://github.com/pingcap/tidb/pull/9289)

## TiKV {#tikv}

-   TiKV [<a href="https://github.com/tikv/tikv/pull/4146">#4146</a>](https://github.com/tikv/tikv/pull/4146)を閉じるときの重複書き込みの問題を修正
-   場合によってはイベントリスナーの結果が異常になる問題を修正[<a href="https://github.com/tikv/tikv/pull/4132">#4132</a>](https://github.com/tikv/tikv/pull/4132)

## ツール {#tools}

-   雷
    -   メモリ使用量を最適化する[<a href="https://github.com/pingcap/tidb-lightning/pull/107">#107</a>](https://github.com/pingcap/tidb-lightning/pull/107) 、 [<a href="https://github.com/pingcap/tidb-lightning/pull/108">#108</a>](https://github.com/pingcap/tidb-lightning/pull/108)
    -   ダンプ ファイルの余分な解析を避けるために、ダンプ ファイルのチャンク分離を削除します[<a href="https://github.com/pingcap/tidb-lightning/pull/109">#109</a>](https://github.com/pingcap/tidb-lightning/pull/109)
    -   ダンプ ファイルの読み取りの同時 I/O を制限して、キャッシュ ミスが多すぎることによるパフォーマンスの低下を回避します[<a href="https://github.com/pingcap/tidb-lightning/pull/110">#110</a>](https://github.com/pingcap/tidb-lightning/pull/110)
    -   単一テーブルのデータのバッチインポートをサポートし、インポートの安定性を向上[<a href="https://github.com/pingcap/tidb-lightning/pull/113">#110</a>](https://github.com/pingcap/tidb-lightning/pull/113)
    -   TiKV [<a href="https://github.com/tikv/tikv/pull/4199">#4199</a>](https://github.com/tikv/tikv/pull/4199)のインポート モードで自動圧縮を有効にする
    -   TiKV クラスターのバージョンが 2.1.4 以降の場合、レベル 1 圧縮はインポート モードで自動的に実行されるため、TiKV の定期的なレベル 1 圧縮パラメーターの無効化をサポートします[<a href="https://github.com/pingcap/tidb-lightning/pull/119">#119</a>](https://github.com/pingcap/tidb-lightning/pull/119)
    -   インポーターのディスク容量を過剰に消費しないように、インポート エンジンの数を制限します[<a href="https://github.com/pingcap/tidb-lightning/pull/119">#119</a>](https://github.com/pingcap/tidb-lightning/pull/119)
-   sync-diff-inspector [<a href="https://github.com/pingcap/tidb-tools/pull/197">#197</a>](https://github.com/pingcap/tidb-tools/pull/197)で TiDB 統計を使用したチャンクの分割をサポートします。
