---
title: TiDB 2.1.14 Release Notes
---

# TiDB 2.1.14 リリースノート {#tidb-2-1-14-release-notes}

発売日：2019年7月4日

TiDB バージョン: 2.1.14

TiDB Ansible バージョン: 2.1.14

## TiDB {#tidb}

-   場合によっては列のプルーニングによって引き起こされる間違ったクエリ結果を修正[<a href="https://github.com/pingcap/tidb/pull/11019">#11019</a>](https://github.com/pingcap/tidb/pull/11019)
-   `show processlist` [<a href="https://github.com/pingcap/tidb/pull/11000">#11000</a>](https://github.com/pingcap/tidb/pull/11000)の`db`と`info`列目の情報が誤って表示されていたのを修正
-   SQLヒントおよびグローバル変数としての`MAX_EXECUTION_TIME`が機能しない場合がある問題を修正[<a href="https://github.com/pingcap/tidb/pull/10999">#10999</a>](https://github.com/pingcap/tidb/pull/10999)
-   負荷に基づいて自動インクリメント ID によって割り当てられた増分ギャップを自動的に調整するサポート[<a href="https://github.com/pingcap/tidb/pull/10997">#10997</a>](https://github.com/pingcap/tidb/pull/10997)
-   `MemTracker` `Distsql`メモリ情報が正しく消去されない問題を修正[<a href="https://github.com/pingcap/tidb/pull/10971">#10971</a>](https://github.com/pingcap/tidb/pull/10971)
-   クエリのメモリ使用量を説明するために、テーブル`information_schema.processlist`に`MEM`列を追加します[<a href="https://github.com/pingcap/tidb/pull/10896">#10896</a>](https://github.com/pingcap/tidb/pull/10896)
-   `max_execution_time`グローバル システム変数を追加して、クエリの最大実行時間を制御します[<a href="https://github.com/pingcap/tidb/pull/10940">#10940</a>](https://github.com/pingcap/tidb/pull/10940)
-   サポートされていない集計関数の使用によって引き起こされるpanicを修正します[<a href="https://github.com/pingcap/tidb/pull/10911">#10911</a>](https://github.com/pingcap/tidb/pull/10911)
-   `load data`ステートメントが失敗した場合の最後のトランザクションの自動ロールバック機能を追加します[<a href="https://github.com/pingcap/tidb/pull/10862">#10862</a>](https://github.com/pingcap/tidb/pull/10862)
-   `OOMAction`設定項目が`Cancel` [<a href="https://github.com/pingcap/tidb/pull/11016">#11016</a>](https://github.com/pingcap/tidb/pull/11016)に設定されている場合、TiDB が誤った結果を返す場合がある問題を修正
-   TiDBpanicの問題[<a href="https://github.com/pingcap/tidb/pull/11039">#11039</a>](https://github.com/pingcap/tidb/pull/11039)を回避するには、 `TRACE`ステートメントを無効にします。
-   特定の関数のプッシュダウンを動的に有効/無効にする`mysql.expr_pushdown_blacklist`システム テーブルをコプロセッサー[<a href="https://github.com/pingcap/tidb/pull/10998">#10998</a>](https://github.com/pingcap/tidb/pull/10998)に追加します。
-   `ONLY_FULL_GROUP_BY`モード[<a href="https://github.com/pingcap/tidb/pull/10994">#10994</a>](https://github.com/pingcap/tidb/pull/10994)で`ANY_VALUE`機能が動作しない問題を修正
-   文字列タイプ[<a href="https://github.com/pingcap/tidb/pull/11043">#11043</a>](https://github.com/pingcap/tidb/pull/11043)のユーザー変数を評価するときにディープ コピーを実行しないことによって引き起こされる誤った評価を修正しました。

## TiKV {#tikv}

-   Raftstoreメッセージの処理時に空のコールバックの処理を最適化し、不要なメッセージの送信を回避します[<a href="https://github.com/tikv/tikv/pull/4682">#4682</a>](https://github.com/tikv/tikv/pull/4682)

## PD {#pd}

-   無効な設定項目を読み込んだ場合のログ出力レベルを`Error` ～ `Warning`に調整します[<a href="https://github.com/pingcap/pd/pull/1577">#1577</a>](https://github.com/pingcap/pd/pull/1577)

## ツール {#tools}

TiDBBinlog

-   Reparo
    -   `safe-mode`構成項目を追加し、この項目を有効にした後の重複データのインポートをサポートします[<a href="https://github.com/pingcap/tidb-binlog/pull/662">#662</a>](https://github.com/pingcap/tidb-binlog/pull/662)
-   Pump
    -   `stop-write-at-available-space`構成項目を追加して、使用可能なbinlogスペースを制限します[<a href="https://github.com/pingcap/tidb-binlog/pull/659">#659</a>](https://github.com/pingcap/tidb-binlog/pull/659)
    -   LevelDB L0ファイル数が[<a href="https://github.com/pingcap/tidb-binlog/pull/648">#648</a>](https://github.com/pingcap/tidb-binlog/pull/648)の場合にガベージコレクタが動作しないことがある問題を修正
    -   ログファイルの削除アルゴリズムを最適化し、スペースの解放を高速化します[<a href="https://github.com/pingcap/tidb-binlog/pull/648">#648</a>](https://github.com/pingcap/tidb-binlog/pull/648)
-   Drainer
    -   ダウンストリーム[<a href="https://github.com/pingcap/tidb-binlog/pull/655">#655</a>](https://github.com/pingcap/tidb-binlog/pull/655)の`BIT`列の更新に失敗する問題を修正

## TiDB Ansible {#tidb-ansible}

-   `ansible`コマンドとその`jmespath`および`jinja2`依存関係パッケージの事前チェック機能を追加します[<a href="https://github.com/pingcap/tidb-ansible/pull/807">#807</a>](https://github.com/pingcap/tidb-ansible/pull/807)
-   Pumpに`stop-write-at-available-space`パラメータ (デフォルトでは 10 GiB) を追加し、利用可能なディスク容量がパラメータ値[<a href="https://github.com/pingcap/tidb-ansible/pull/807">#807</a>](https://github.com/pingcap/tidb-ansible/pull/807)未満の場合は、 Pumpへのbinlogファイルの書き込みを停止します。
