---
title: TiDB 2.1.4 Release Notes
---

# TiDB2.1.4リリースノート {#tidb-2-1-4-release-notes}

2019年2月15日、TiDB2.1.4がリリースされました。対応するTiDBAnsible2.1.4もリリースされています。 TiDB 2.1.3と比較して、このリリースでは、安定性、SQLオプティマイザー、統計、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー/エグゼキューター
    -   `VALUES`関数がFLOATタイプを正しく処理しない問題を修正します[＃9223](https://github.com/pingcap/tidb/pull/9223)
    -   場合によってはFloatをStringにキャストするときの間違った結果の問題を修正します[＃9227](https://github.com/pingcap/tidb/pull/9227)
    -   場合によっては`FORMAT`関数の間違った結果の問題を修正します[＃9235](https://github.com/pingcap/tidb/pull/9235)
    -   場合によっては、結合クエリを処理するときのパニックの問題を修正します[＃9264](https://github.com/pingcap/tidb/pull/9264)
    -   `VALUES`関数がENUMタイプを正しく処理しない問題を修正します[＃9280](https://github.com/pingcap/tidb/pull/9280)
    -   場合によっては`DATE_ADD`の間違った結果の問題を修正し[＃9284](https://github.com/pingcap/tidb/pull/9284) `DATE_SUB`
-   サーバ
    -   「リロード特権の成功」ログを最適化し、DEBUGレベル[＃9274](https://github.com/pingcap/tidb/pull/9274)に変更します。
-   DDL
    -   `tidb_ddl_reorg_worker_cnt`と`tidb_ddl_reorg_batch_size`をグローバル変数[＃9134](https://github.com/pingcap/tidb/pull/9134)に変更します
    -   いくつかの異常な状態で生成された列にインデックスを追加することによって引き起こされるバグを修正します[＃9289](https://github.com/pingcap/tidb/pull/9289)

## TiKV {#tikv}

-   TiKV1を閉じるときの重複書き込みの問題を修正し[＃4146](https://github.com/tikv/tikv/pull/4146)
-   場合によっては、イベントリスナーの異常な結果の問題を修正します[＃4132](https://github.com/tikv/tikv/pull/4132)

## ツール {#tools}

-   雷
    -   メモリ使用量を[＃108](https://github.com/pingcap/tidb-lightning/pull/108)化する[＃107](https://github.com/pingcap/tidb-lightning/pull/107)
    -   ダンプファイルの余分な解析を回避するために、ダンプファイルのチャンク分離を削除します[＃109](https://github.com/pingcap/tidb-lightning/pull/109)
    -   キャッシュミスが多すぎることによるパフォーマンスの低下を回避するために、ダンプファイルの読み取りのI/O同時実行を制限します[＃110](https://github.com/pingcap/tidb-lightning/pull/110)
    -   インポートの安定性を向上させるために、単一のテーブルのデータをバッチでインポートすることをサポートします[＃110](https://github.com/pingcap/tidb-lightning/pull/113)
    -   [＃4199](https://github.com/tikv/tikv/pull/4199)のインポートモードで自動圧縮を有効にする
    -   TiKVクラスタのバージョンが2.1.4以降の場合、レベル1の圧縮はインポートモードで自動的に実行されるため、TiKVの定期的なレベル1の圧縮パラメーターの無効化をサポートします[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
    -   インポートエンジンの数を制限して、インポーターのディスク領域を過度に消費しないようにします[＃119](https://github.com/pingcap/tidb-lightning/pull/119)
-   sync-diff-inspector1で[＃197](https://github.com/pingcap/tidb-tools/pull/197)統計を使用したチャンクの分割をサポートします
