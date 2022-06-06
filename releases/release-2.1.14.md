---
title: TiDB 2.1.14 Release Notes
---

# TiDB2.1.14リリースノート {#tidb-2-1-14-release-notes}

発売日：2019年7月4日

TiDBバージョン：2.1.14

TiDB Ansibleバージョン：2.1.14

## TiDB {#tidb}

-   場合によっては列のプルーニングによって引き起こされる誤ったクエリ結果を修正します[＃11019](https://github.com/pingcap/tidb/pull/11019)
-   [＃11000](https://github.com/pingcap/tidb/pull/11000)の`db`列と`info`列に誤って表示された情報を修正し`show processlist`
-   SQLヒントおよびグローバル変数としての`MAX_EXECUTION_TIME`が機能しない場合があるという問題を修正します[＃10999](https://github.com/pingcap/tidb/pull/10999)
-   サポートは、負荷[＃10997](https://github.com/pingcap/tidb/pull/10997)に基づいて自動増分IDによって割り当てられた増分ギャップを自動的に調整します
-   クエリが終了したときに`MemTracker`の`Distsql`メモリ情報が正しくクリーンアップされない問題を修正します[＃10971](https://github.com/pingcap/tidb/pull/10971)
-   `information_schema.processlist`テーブルに`MEM`列を追加して、クエリのメモリ使用量を説明します[＃10896](https://github.com/pingcap/tidb/pull/10896)
-   `max_execution_time`のグローバルシステム変数を追加して、クエリの最大実行時間を制御します[＃10940](https://github.com/pingcap/tidb/pull/10940)
-   サポートされていない集計関数の使用によって引き起こされるパニックを修正する[＃10911](https://github.com/pingcap/tidb/pull/10911)
-   `load data`のステートメントが失敗した場合の最後のトランザクションの自動ロールバック機能を追加します[＃10862](https://github.com/pingcap/tidb/pull/10862)
-   `OOMAction`構成項目が35に設定されている場合、 `Cancel`が誤った結果を返すことがある問題を修正し[＃11016](https://github.com/pingcap/tidb/pull/11016) 。
-   TiDBパニックの問題を回避するために`TRACE`のステートメントを無効にします[＃11039](https://github.com/pingcap/tidb/pull/11039)
-   コプロセッサー[＃10998](https://github.com/pingcap/tidb/pull/10998)への特定の機能のプッシュダウンを動的に有効/無効にする`mysql.expr_pushdown_blacklist`のシステム表を追加します。
-   `ANY_VALUE`機能が`ONLY_FULL_GROUP_BY`モードで機能しない問題を修正します[＃10994](https://github.com/pingcap/tidb/pull/10994)
-   文字列タイプ[＃11043](https://github.com/pingcap/tidb/pull/11043)のユーザー変数を評価するときにディープコピーを実行しないことによって引き起こされる誤った評価を修正します

## TiKV {#tikv}

-   Raftstoreメッセージを処理するときに空のコールバックの処理を最適化して、不要なメッセージの送信を回避します[＃4682](https://github.com/tikv/tikv/pull/4682)

## PD {#pd}

-   無効な構成項目[＃1577](https://github.com/pingcap/pd/pull/1577)を読み取る場合は、ログ出力レベルを`Error`から`Warning`に調整してください。

## ツール {#tools}

TiDB Binlog

-   レパロ
    -   `safe-mode`の構成アイテムを追加し、このアイテムを有効にした後の重複データのインポートをサポートします[＃662](https://github.com/pingcap/tidb-binlog/pull/662)
-   ポンプ
    -   `stop-write-at-available-space`の構成アイテムを追加して、使用可能なbinlogスペースを制限します[＃659](https://github.com/pingcap/tidb-binlog/pull/659)
    -   LevelDBL0ファイルの数が[＃648](https://github.com/pingcap/tidb-binlog/pull/648)のときにガベージコレクターが機能しないことがある問題を修正します
    -   ログファイルを削除するアルゴリズムを最適化して、スペースの解放を高速化します[＃648](https://github.com/pingcap/tidb-binlog/pull/648)
-   ドレイナー
    -   ダウンストリーム[＃655](https://github.com/pingcap/tidb-binlog/pull/655)の`BIT`列を更新できない問題を修正します

## TiDB Ansible {#tidb-ansible}

-   `ansible`コマンドとその`jmespath`および`jinja2`依存関係パッケージの事前チェック機能を追加します[＃807](https://github.com/pingcap/tidb-ansible/pull/807)
-   Pumpに`stop-write-at-available-space`パラメーター（デフォルトでは10 GiB）を追加し、使用可能なディスク容量がパラメーター値[＃807](https://github.com/pingcap/tidb-ansible/pull/807)未満になったら、Pumpでのbinlogファイルの書き込みを停止します。
