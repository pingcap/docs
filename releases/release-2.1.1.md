---
title: TiDB 2.1.1 Release Notes
summary: TiDB 2.1.1は2018年12月12日にリリースされ、安定性、SQLオプティマイザー、統計情報、実行エンジンが改善されました。修正には、負の日付の丸め誤差、解凍関数のデータ長チェック、トランザクションの再試行が含まれます。テーブルのデフォルトの文字セットと照合順序はutf8mb4に変更されました。PDとTiKVにも様々な修正と最適化が施されました。Lightningツールは分析メカニズムを最適化し、チェックポイント情報をローカルに保存するサポートを追加しました。TiDB Binlog、主キー列のみを持つテーブルのpbファイル出力のバグが修正されました。
---

# TiDB 2.1.1 リリースノート {#tidb-2-1-1-release-notes}

2018年12月12日にTiDB 2.1.1がリリースされました。TiDB 2.1.0と比較して、このリリースでは安定性、SQLオプティマイザー、統計情報、実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   負の日付[＃8574](https://github.com/pingcap/tidb/pull/8574)の丸め誤差を修正
    -   `uncompress`関数がデータ長[＃8606](https://github.com/pingcap/tidb/pull/8606)チェックしない問題を修正
    -   `execute`コマンドが実行された後に`prepare`のバインド引数をリセットする[＃8652](https://github.com/pingcap/tidb/pull/8652)
    -   パーティションテーブル[＃8649](https://github.com/pingcap/tidb/pull/8649)の統計情報の自動収集をサポート
    -   `abs`関数[＃8628](https://github.com/pingcap/tidb/pull/8628)を押し下げるときに誤って構成された整数型を修正します
    -   JSON列[＃8660](https://github.com/pingcap/tidb/pull/8660)のデータ競合を修正
-   サーバ
    -   PDが故障したときにTSOで取得したトランザクションが正しくない問題を修正[＃8567](https://github.com/pingcap/tidb/pull/8567)
    -   ANSI標準[＃8576](https://github.com/pingcap/tidb/pull/8576)に準拠していないステートメントによって発生するブートストラップエラーを修正
    -   トランザクションの再試行で誤ったパラメータが使用される問題を修正[＃8638](https://github.com/pingcap/tidb/pull/8638)
-   DDL
    -   テーブルのデフォルトの文字セットと照合順序を`utf8mb4` [＃8590](https://github.com/pingcap/tidb/pull/8590)に変更します
    -   インデックス[＃8614](https://github.com/pingcap/tidb/pull/8614)を追加する速度を制御するために`ddl_reorg_batch_size`変数を追加します
    -   DDLの文字セットと照合順序オプションの内容を大文字と小文字を区別しないようにする[＃8611](https://github.com/pingcap/tidb/pull/8611)
    -   生成された列[＃8655](https://github.com/pingcap/tidb/pull/8655)インデックス追加に関する問題を修正

## PD {#pd}

-   構成ファイル[＃1334](https://github.com/pingcap/pd/pull/1334)で一部の構成項目を`0`に設定できない問題を修正
-   PD [＃1362](https://github.com/pingcap/pd/pull/1362)起動するときに未定義の構成を確認します
-   遅延を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃1339](https://github.com/pingcap/pd/pull/1339)
-   デッド`RaftCluster` [＃1370](https://github.com/pingcap/pd/pull/1370)により停止できない問題を修正

## TiKV {#tikv}

-   遅延を最適化するために、リーダーを新しく作成されたピアに転送しないでください[＃3878](https://github.com/tikv/tikv/pull/3878)

## ツール {#tools}

-   稲妻
    -   インポートされたテーブルの`analyze`メカニズムを最適化してインポート速度を向上させます
    -   チェックポイント情報をローカルファイルに保存する機能をサポート
-   TiDBBinlog
    -   主キー列のみを持つテーブルがpbイベントを生成できないpbファイル出力のバグを修正しました
