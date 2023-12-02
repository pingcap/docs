---
title: TiDB 2.1.1 Release Notes
---

# TiDB 2.1.1 リリースノート {#tidb-2-1-1-release-notes}

2018 年 12 月 12 日に、TiDB 2.1.1 がリリースされました。 TiDB 2.1.0 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   負の日付の丸め誤差を修正[#8574](https://github.com/pingcap/tidb/pull/8574)
    -   `uncompress`関数がデータ長をチェックしない問題を修正[#8606](https://github.com/pingcap/tidb/pull/8606)
    -   `execute`コマンドの実行後に`prepare`ステートメントのバインド引数をリセットします[#8652](https://github.com/pingcap/tidb/pull/8652)
    -   パーティションテーブルの統計情報の自動収集をサポート[#8649](https://github.com/pingcap/tidb/pull/8649)
    -   `abs`関数[#8628](https://github.com/pingcap/tidb/pull/8628)を押したときに誤って設定された整数型を修正しました。
    -   JSON列[#8660](https://github.com/pingcap/tidb/pull/8660)のデータ競合を修正する
-   サーバ
    -   PDがダウンした場合にTSOを取得したトランザクションが正しくない問題を修正[#8567](https://github.com/pingcap/tidb/pull/8567)
    -   ANSI 標準に準拠していないステートメントによって引き起こされるブートストラップの失敗を修正[#8576](https://github.com/pingcap/tidb/pull/8576)
    -   トランザクションの再試行で不正なパラメータが使用される問題を修正[#8638](https://github.com/pingcap/tidb/pull/8638)
-   DDL
    -   デフォルトの文字セットとテーブルの照合順序を`utf8mb4` [#8590](https://github.com/pingcap/tidb/pull/8590)に変更します。
    -   `ddl_reorg_batch_size`変数を追加してインデックス[#8614](https://github.com/pingcap/tidb/pull/8614)の追加速度を制御します
    -   文字セットと照合順序オプションの内容を DDL で大文字と小文字を区別しないようにします[#8611](https://github.com/pingcap/tidb/pull/8611)
    -   生成された列のインデックス追加の問題を修正[#8655](https://github.com/pingcap/tidb/pull/8655)

## PD {#pd}

-   設定ファイル[#1334](https://github.com/pingcap/pd/pull/1334)の一部の設定項目が`0`に設定できない問題を修正
-   PD [#1362](https://github.com/pingcap/pd/pull/1362)起動時に未定義の構成を確認する
-   起こり得る遅延を最適化するために、リーダーを新しく作成されたピアに転送しないようにします[#1339](https://github.com/pingcap/pd/pull/1339)
-   `RaftCluster`がデッドロックにより停止できない問題を修正[#1370](https://github.com/pingcap/pd/pull/1370)

## TiKV {#tikv}

-   起こり得る遅延を最適化するために、リーダーを新しく作成されたピアに転送しないようにします[#3878](https://github.com/tikv/tikv/pull/3878)

## ツール {#tools}

-   稲妻
    -   インポートされたテーブルの`analyze`メカニズムを最適化してインポート速度を向上させます
    -   チェックポイント情報のローカル ファイルへの保存をサポート
-   TiDBBinlog
    -   主キーカラムのみを持つテーブルではpbイベントが発生できないというpbファイルの出力バグを修正
