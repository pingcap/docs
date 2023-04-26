---
title: TiDB 2.1.1 Release Notes
---

# TiDB 2.1.1 リリースノート {#tidb-2-1-1-release-notes}

2018 年 12 月 12 日に、TiDB 2.1.1 がリリースされました。 TiDB 2.1.0 と比較すると、このリリースでは、安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー/エグゼキューター
    -   負の日付の丸め誤差を修正[#8574](https://github.com/pingcap/tidb/pull/8574)
    -   `uncompress`関数がデータ長をチェックしない問題を修正[#8606](https://github.com/pingcap/tidb/pull/8606)
    -   `execute`コマンドの実行後に`prepare`ステートメントのバインド引数をリセットする[#8652](https://github.com/pingcap/tidb/pull/8652)
    -   パーティションテーブルの統計情報の自動収集をサポート[#8649](https://github.com/pingcap/tidb/pull/8649)
    -   `abs`関数[#8628](https://github.com/pingcap/tidb/pull/8628)を押し下げるときに、誤って構成された整数型を修正します
    -   JSON 列[#8660](https://github.com/pingcap/tidb/pull/8660)のデータ競合を修正する
-   サーバ
    -   PD故障時にTSOを取得したトランザクションが正しくない問題を修正[#8567](https://github.com/pingcap/tidb/pull/8567)
    -   ANSI 標準に準拠していないステートメントが原因で発生したブートストラップ エラーを修正します[#8576](https://github.com/pingcap/tidb/pull/8576)
    -   トランザクションの再試行で誤ったパラメーターが使用される問題を修正します[#8638](https://github.com/pingcap/tidb/pull/8638)
-   DDL
    -   テーブルのデフォルトの文字セットと照合順序を`utf8mb4` [#8590](https://github.com/pingcap/tidb/pull/8590)に変更します
    -   `ddl_reorg_batch_size`変数を追加して、インデックス[#8614](https://github.com/pingcap/tidb/pull/8614)を追加する速度を制御します
    -   DDL の大文字と小文字を区別しない文字セットと照合順序オプションのコンテンツを作成する[#8611](https://github.com/pingcap/tidb/pull/8611)
    -   生成された列にインデックスを追加する問題を修正します[#8655](https://github.com/pingcap/tidb/pull/8655)

## PD {#pd}

-   設定ファイル[#1334](https://github.com/pingcap/pd/pull/1334)で一部の設定項目を`0`に設定できない問題を修正
-   PD [#1362](https://github.com/pingcap/pd/pull/1362)の起動時に未定義の構成を確認する
-   潜在的な遅延を最適化するために、新しく作成されたピアにリーダーを転送しないでください[#1339](https://github.com/pingcap/pd/pull/1339)
-   デッドロックが原因で`RaftCluster`が停止できない問題を修正[#1370](https://github.com/pingcap/pd/pull/1370)

## TiKV {#tikv}

-   潜在的な遅延を最適化するために、新しく作成されたピアにリーダーを転送しないでください[#3878](https://github.com/tikv/tikv/pull/3878)

## ツール {#tools}

-   雷
    -   インポートされたテーブルの`analyze`メカニズムを最適化して、インポート速度を向上させます
    -   チェックポイント情報のローカルファイルへの保存をサポート
-   TiDBBinlog
    -   主キー列のみのテーブルが pb イベントを生成できない pb ファイルの出力バグを修正
