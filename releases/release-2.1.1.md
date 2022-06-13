---
title: TiDB 2.1.1 Release Notes
---

# TiDB2.1.1リリースノート {#tidb-2-1-1-release-notes}

2018年12月12日、TiDB2.1.1がリリースされました。このリリースでは、TiDB 2.1.0と比較して、安定性、SQLオプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー/エグゼキューター
    -   負の日付の丸め誤差を修正[＃8574](https://github.com/pingcap/tidb/pull/8574)
    -   `uncompress`関数がデータ長[＃8606](https://github.com/pingcap/tidb/pull/8606)をチェックしない問題を修正します
    -   `execute`コマンドの実行後に`prepare`ステートメントのバインド引数をリセットします[＃8652](https://github.com/pingcap/tidb/pull/8652)
    -   パーティションテーブルの統計情報の自動収集をサポート[＃8649](https://github.com/pingcap/tidb/pull/8649)
    -   `abs`関数[＃8628](https://github.com/pingcap/tidb/pull/8628)をプッシュダウンするときに誤って構成された整数型を修正します
    -   JSON列[＃8660](https://github.com/pingcap/tidb/pull/8660)のデータ競合を修正します
-   サーバ
    -   PDが故障したときにTSOを取得したトランザクションが正しくない問題を修正します[＃8567](https://github.com/pingcap/tidb/pull/8567)
    -   ANSI規格に準拠していないステートメントによって引き起こされたブートストラップの失敗を修正します[＃8576](https://github.com/pingcap/tidb/pull/8576)
    -   トランザクションの再試行で誤ったパラメーターが使用される問題を修正します[＃8638](https://github.com/pingcap/tidb/pull/8638)
-   DDL
    -   デフォルトの文字セットとテーブルの照合順序を[＃8590](https://github.com/pingcap/tidb/pull/8590)に変更し`utf8mb4`
    -   `ddl_reorg_batch_size`変数を追加して、インデックスの追加速度を制御します[＃8614](https://github.com/pingcap/tidb/pull/8614)
    -   文字セットと照合順序オプションのコンテンツをDDLで大文字と小文字を区別しないようにする[＃8611](https://github.com/pingcap/tidb/pull/8611)
    -   生成された列のインデックスを追加する問題を修正します[＃8655](https://github.com/pingcap/tidb/pull/8655)

## PD {#pd}

-   構成ファイル[＃1334](https://github.com/pingcap/pd/pull/1334)で一部の構成項目を`0`に設定できない問題を修正します。
-   [＃1362](https://github.com/pingcap/pd/pull/1362)を開始するときに未定義の構成を確認してください
-   遅延の可能性を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃1339](https://github.com/pingcap/pd/pull/1339)
-   デッドロック[＃1370](https://github.com/pingcap/pd/pull/1370)が原因で`RaftCluster`が停止できない問題を修正します

## TiKV {#tikv}

-   遅延の可能性を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃3878](https://github.com/tikv/tikv/pull/3878)

## ツール {#tools}

-   雷
    -   インポートされたテーブルの`analyze`メカニズムを最適化して、インポート速度を上げます
    -   チェックポイント情報のローカルファイルへの保存をサポート
-   TiDB Binlog
    -   主キー列のみを持つテーブルがpbイベントを生成できないというpbファイルの出力バグを修正します
