---
title: TiDB 2.1.14 Release Notes
---

# TiDB 2.1.14 リリースノート {#tidb-2-1-14-release-notes}

リリース日: 2019 年 7 月 4 日

TiDB バージョン: 2.1.14

TiDB アンシブル バージョン: 2.1.14

## TiDB {#tidb}

-   場合によっては列のプルーニングによって引き起こされる誤ったクエリ結果を修正します[#11019](https://github.com/pingcap/tidb/pull/11019)
-   `show processlist` [#11000](https://github.com/pingcap/tidb/pull/11000)の`db`と`info`列に誤って表示された情報を修正します。
-   `MAX_EXECUTION_TIME`が SQL ヒントやグローバル変数として機能しない場合がある問題を修正[#10999](https://github.com/pingcap/tidb/pull/10999)
-   負荷に基づいて自動インクリメント ID によって割り当てられたインクリメンタル ギャップを自動的に調整するサポート[#10997](https://github.com/pingcap/tidb/pull/10997)
-   クエリ終了時に`Distsql` `MemTracker`のメモリ情報が正しく消去されない問題を修正[#10971](https://github.com/pingcap/tidb/pull/10971)
-   `information_schema.processlist`テーブルに`MEM`列を追加して、クエリのメモリ使用量を記述します[#10896](https://github.com/pingcap/tidb/pull/10896)
-   `max_execution_time`グローバル システム変数を追加して、クエリの最大実行時間を制御します[#10940](https://github.com/pingcap/tidb/pull/10940)
-   サポートされていない集計関数の使用によるpanicを修正します[#10911](https://github.com/pingcap/tidb/pull/10911)
-   `load data`ステートメントが失敗したときの最後のトランザクションの自動ロールバック機能を追加します[#10862](https://github.com/pingcap/tidb/pull/10862)
-   `OOMAction`構成項目が`Cancel` [#11016](https://github.com/pingcap/tidb/pull/11016)に設定されている場合、TiDB が間違った結果を返すことがある問題を修正します。
-   TiDBpanicの問題[#11039](https://github.com/pingcap/tidb/pull/11039)を回避するために`TRACE`ステートメントを無効にします。
-   特定の関数をプッシュダウンすることを動的に有効/無効にする`mysql.expr_pushdown_blacklist`システム テーブルをコプロセッサー[#10998](https://github.com/pingcap/tidb/pull/10998)に追加します。
-   `ONLY_FULL_GROUP_BY`モード[#10994](https://github.com/pingcap/tidb/pull/10994)で`ANY_VALUE`機能が動作しない問題を修正
-   文字列型[#11043](https://github.com/pingcap/tidb/pull/11043)のユーザー変数を評価するときに、ディープ コピーを実行しないことによって引き起こされる誤った評価を修正します。

## TiKV {#tikv}

-   Raftstoreメッセージの処理時に空のコールバックの処理を最適化して、不要なメッセージの送信を回避する[#4682](https://github.com/tikv/tikv/pull/4682)

## PD {#pd}

-   無効な設定項目の読み取り時のログ出力レベルを`Error`から`Warning`に調整します[#1577](https://github.com/pingcap/pd/pull/1577)

## ツール {#tools}

TiDBBinlog

-   Reparo
    -   `safe-mode`構成アイテムを追加し、このアイテムが有効になった後に重複データのインポートをサポートします[#662](https://github.com/pingcap/tidb-binlog/pull/662)
-   Pump
    -   `stop-write-at-available-space`構成項目を追加して、使用可能なbinlogスペースを制限します[#659](https://github.com/pingcap/tidb-binlog/pull/659)
    -   LevelDB の L0 ファイル数が 0 [#648](https://github.com/pingcap/tidb-binlog/pull/648)の場合に Garbage Collector が動作しないことがある問題を修正
    -   スペースの解放を高速化するために、ログ ファイルを削除するアルゴリズムを最適化します[#648](https://github.com/pingcap/tidb-binlog/pull/648)
-   Drainer
    -   ダウンストリーム[#655](https://github.com/pingcap/tidb-binlog/pull/655)の`BIT`列を更新できない問題を修正

## TiDB アンシブル {#tidb-ansible}

-   `ansible`コマンドとその`jmespath`および`jinja2`依存パッケージの事前チェック機能を追加します[#807](https://github.com/pingcap/tidb-ansible/pull/807)
-   Pumpに`stop-write-at-available-space`パラメーター (デフォルトでは 10 GiB) を追加し、使用可能なディスク容量がパラメーター値[#807](https://github.com/pingcap/tidb-ansible/pull/807)よりも少ない場合は、 Pumpでbinlogファイルの書き込みを停止します。
