---
title: TiDB 2.1.1 Release Notes
summary: TiDB 2.1.1 は、安定性、SQL オプティマイザー、統計情報、実行エンジンの改善を伴い、2018 年 12 月 12 日にリリースされました。修正には、負の日付の丸め誤差、圧縮解除関数のデータ長チェック、トランザクションの再試行が含まれます。テーブルのデフォルトの文字セットと照合順序は、utf8mb4 に変更されました。PD と TiKV にもさまざまな修正と最適化が加えられました。Lightning ツールは分析メカニズムを最適化し、チェックポイント情報をローカルに保存するためのサポートを追加しました。TiDB Binlog は、主キー列のみを持つテーブルの pb ファイルの出力バグを修正しました。
---

# TiDB 2.1.1 リリースノート {#tidb-2-1-1-release-notes}

2018 年 12 月 12 日に、TiDB 2.1.1 がリリースされました。TiDB 2.1.0 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## ティビ {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   負の日付[＃8574](https://github.com/pingcap/tidb/pull/8574)の丸め誤差を修正
    -   `uncompress`関数がデータ長[＃8606](https://github.com/pingcap/tidb/pull/8606)をチェックしない問題を修正
    -   `execute`コマンドが実行された後に`prepare`ステートメントのバインド引数をリセットします[＃8652](https://github.com/pingcap/tidb/pull/8652)
    -   パーティションテーブル[＃8649](https://github.com/pingcap/tidb/pull/8649)の統計情報の自動収集をサポート
    -   `abs`関数[＃8628](https://github.com/pingcap/tidb/pull/8628)をプッシュダウンするときに誤って設定された整数型を修正
    -   JSON列[＃8660](https://github.com/pingcap/tidb/pull/8660)のデータ競合を修正
-   サーバ
    -   PDが故障したときにTSOで取得したトランザクションが正しくない問題を修正[＃8567](https://github.com/pingcap/tidb/pull/8567)
    -   ANSI標準[＃8576](https://github.com/pingcap/tidb/pull/8576)に準拠していないステートメントによって発生するブートストラップエラーを修正
    -   トランザクション再試行で誤ったパラメータが使用される問題を修正[＃8638](https://github.com/pingcap/tidb/pull/8638)
-   DDL
    -   テーブルのデフォルトの文字セットと照合順序を`utf8mb4` [＃8590](https://github.com/pingcap/tidb/pull/8590)に変更します
    -   インデックス[＃8614](https://github.com/pingcap/tidb/pull/8614)を追加する速度を制御するために`ddl_reorg_batch_size`変数を追加します
    -   DDLの文字セットと照合順序オプションの内容を大文字と小文字を区別しないようにする[＃8611](https://github.com/pingcap/tidb/pull/8611)
    -   生成された列[＃8655](https://github.com/pingcap/tidb/pull/8655)インデックス追加に関する問題を修正

## PD {#pd}

-   設定ファイル[＃1334](https://github.com/pingcap/pd/pull/1334)で一部の設定項目を`0`に設定できない問題を修正
-   PD [＃1362](https://github.com/pingcap/pd/pull/1362)を起動するときに未定義の構成を確認します
-   遅延を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃1339](https://github.com/pingcap/pd/pull/1339)
-   デッドロック[＃1370](https://github.com/pingcap/pd/pull/1370)により停止でき`RaftCluster`問題を修正

## ティクヴ {#tikv}

-   遅延を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃3878](https://github.com/tikv/tikv/pull/3878)

## ツール {#tools}

-   稲妻
    -   インポートされたテーブルの`analyze`メカニズムを最適化してインポート速度を向上します
    -   チェックポイント情報をローカルファイルに保存する機能をサポート
-   TiDBBinlog
    -   主キー列のみを持つテーブルがpbイベントを生成できないpbファイル出力のバグを修正しました
