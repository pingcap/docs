---
title: TiDB 2.1.1 Release Notes
---

# TiDB 2.1.1 リリースノート {#tidb-2-1-1-release-notes}

2018 年 12 月 12 日に、TiDB 2.1.1 がリリースされました。 TiDB 2.1.0 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   負の日付の丸め誤差を修正[<a href="https://github.com/pingcap/tidb/pull/8574">#8574</a>](https://github.com/pingcap/tidb/pull/8574)
    -   `uncompress`関数がデータ長をチェックしない問題を修正[<a href="https://github.com/pingcap/tidb/pull/8606">#8606</a>](https://github.com/pingcap/tidb/pull/8606)
    -   `execute`コマンドの実行後に`prepare`ステートメントのバインド引数をリセットします[<a href="https://github.com/pingcap/tidb/pull/8652">#8652</a>](https://github.com/pingcap/tidb/pull/8652)
    -   パーティションテーブルの統計情報の自動収集をサポート[<a href="https://github.com/pingcap/tidb/pull/8649">#8649</a>](https://github.com/pingcap/tidb/pull/8649)
    -   `abs`関数[<a href="https://github.com/pingcap/tidb/pull/8628">#8628</a>](https://github.com/pingcap/tidb/pull/8628)を押したときに誤って設定された整数型を修正しました。
    -   JSON列[<a href="https://github.com/pingcap/tidb/pull/8660">#8660</a>](https://github.com/pingcap/tidb/pull/8660)のデータ競合を修正する
-   サーバ
    -   PDがダウンした場合にTSOを取得したトランザクションが正しくない問題を修正[<a href="https://github.com/pingcap/tidb/pull/8567">#8567</a>](https://github.com/pingcap/tidb/pull/8567)
    -   ANSI 標準に準拠していないステートメントによって引き起こされるブートストラップの失敗を修正[<a href="https://github.com/pingcap/tidb/pull/8576">#8576</a>](https://github.com/pingcap/tidb/pull/8576)
    -   トランザクションの再試行で不正なパラメータが使用される問題を修正[<a href="https://github.com/pingcap/tidb/pull/8638">#8638</a>](https://github.com/pingcap/tidb/pull/8638)
-   DDL
    -   デフォルトの文字セットとテーブルの照合順序を`utf8mb4` [<a href="https://github.com/pingcap/tidb/pull/8590">#8590</a>](https://github.com/pingcap/tidb/pull/8590)に変更します。
    -   `ddl_reorg_batch_size`変数を追加してインデックス[<a href="https://github.com/pingcap/tidb/pull/8614">#8614</a>](https://github.com/pingcap/tidb/pull/8614)の追加速度を制御します
    -   文字セットと照合順序オプションの内容を DDL で大文字と小文字を区別しないようにします[<a href="https://github.com/pingcap/tidb/pull/8611">#8611</a>](https://github.com/pingcap/tidb/pull/8611)
    -   生成された列のインデックス追加の問題を修正[<a href="https://github.com/pingcap/tidb/pull/8655">#8655</a>](https://github.com/pingcap/tidb/pull/8655)

## PD {#pd}

-   設定ファイル[<a href="https://github.com/pingcap/pd/pull/1334">#1334</a>](https://github.com/pingcap/pd/pull/1334)の一部の設定項目が`0`に設定できない問題を修正
-   PD [<a href="https://github.com/pingcap/pd/pull/1362">#1362</a>](https://github.com/pingcap/pd/pull/1362)起動時に未定義の構成を確認する
-   起こり得る遅延を最適化するために、リーダーを新しく作成されたピアに転送しないようにします[<a href="https://github.com/pingcap/pd/pull/1339">#1339</a>](https://github.com/pingcap/pd/pull/1339)
-   `RaftCluster`がデッドロックにより停止できない問題を修正[<a href="https://github.com/pingcap/pd/pull/1370">#1370</a>](https://github.com/pingcap/pd/pull/1370)

## TiKV {#tikv}

-   起こり得る遅延を最適化するために、リーダーを新しく作成されたピアに転送しないようにします[<a href="https://github.com/tikv/tikv/pull/3878">#3878</a>](https://github.com/tikv/tikv/pull/3878)

## ツール {#tools}

-   雷
    -   インポートされたテーブルの`analyze`メカニズムを最適化してインポート速度を向上させます
    -   チェックポイント情報のローカル ファイルへの保存をサポート
-   TiDBBinlog
    -   主キーカラムのみを持つテーブルではpbイベントが発生できないというpbファイルの出力バグを修正
