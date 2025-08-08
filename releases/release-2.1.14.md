---
title: TiDB 2.1.14 Release Notes
summary: TiDB 2.1.14は2019年7月4日にリリースされました。クエリ結果の誤りの修正、新しいシステム変数の追加、メモリ使用量の最適化、TiDB BinlogおよびTiDB Ansibleの新しい設定項目の追加など、様々なバグ修正と改善が含まれています。さらに、TiKVとPDの最適化も行われています。
---

# TiDB 2.1.14 リリースノート {#tidb-2-1-14-release-notes}

発売日：2019年7月4日

TiDB バージョン: 2.1.14

TiDB Ansible バージョン: 2.1.14

## TiDB {#tidb}

-   一部のケースで列プルーニングによって発生する誤ったクエリ結果を修正[＃11019](https://github.com/pingcap/tidb/pull/11019)
-   `show processlist` [＃11000](https://github.com/pingcap/tidb/pull/11000)の`db`列目と`info`列目に誤って表示された情報を修正
-   `MAX_EXECUTION_TIME` SQLヒントとグローバル変数が場合によっては機能しない問題を修正[＃10999](https://github.com/pingcap/tidb/pull/10999)
-   負荷[＃10997](https://github.com/pingcap/tidb/pull/10997)に基づいて自動増分IDによって割り当てられた増分ギャップを自動的に調整する機能をサポート
-   クエリ終了時にメモリ情報`Distsql` `MemTracker`正しく消去されない問題を修正[＃10971](https://github.com/pingcap/tidb/pull/10971)
-   クエリ[＃10896](https://github.com/pingcap/tidb/pull/10896)のメモリ使用量を説明するために、 `information_schema.processlist`表に`MEM`列を追加します。
-   クエリの最大実行時間を制御するグローバルシステム変数を`max_execution_time`追加する[＃10940](https://github.com/pingcap/tidb/pull/10940)
-   サポートされていない集計関数の使用によって発生するpanicを修正[＃10911](https://github.com/pingcap/tidb/pull/10911)
-   `load data`文が失敗した場合、最後のトランザクションに自動ロールバック機能を追加します[＃10862](https://github.com/pingcap/tidb/pull/10862)
-   `OOMAction`構成項目が`Cancel` [＃11016](https://github.com/pingcap/tidb/pull/11016)に設定されている場合に TiDB が誤った結果を返す場合がある問題を修正しました。
-   TiDBpanic問題[＃11039](https://github.com/pingcap/tidb/pull/11039)回避するために`TRACE`文を無効にする
-   特定の関数をコプロセッサー[＃10998](https://github.com/pingcap/tidb/pull/10998)にプッシュダウンすることを動的に有効/無効にする`mysql.expr_pushdown_blacklist`システム テーブルを追加します。
-   `ANY_VALUE`機能が`ONLY_FULL_GROUP_BY`モード[＃10994](https://github.com/pingcap/tidb/pull/10994)で動作しない問題を修正
-   文字列型[＃11043](https://github.com/pingcap/tidb/pull/11043)のユーザー変数を評価する際にディープコピーを行わないことで発生する誤った評価を修正しました。

## TiKV {#tikv}

-   Raftstoreメッセージを処理するときに空のコールバックの処理を最適化して、不要なメッセージ[＃4682](https://github.com/tikv/tikv/pull/4682)送信を回避します。

## PD {#pd}

-   無効な構成項目[＃1577](https://github.com/pingcap/pd/pull/1577)読み取るときにログ出力レベルを`Error`から`Warning`に調整します

## ツール {#tools}

TiDBBinlog

-   Reparo
    -   `safe-mode`構成項目を追加し、この項目を有効にした後に重複したデータのインポートをサポートします[＃662](https://github.com/pingcap/tidb-binlog/pull/662)
-   Pump
    -   利用可能なbinlogスペースを制限するための`stop-write-at-available-space`設定項目を追加します[＃659](https://github.com/pingcap/tidb-binlog/pull/659)
    -   LevelDB L0ファイルの数が[＃648](https://github.com/pingcap/tidb-binlog/pull/648)の場合にガベージコレクターが動作しないことがある問題を修正しました。
    -   ログファイルを削除するアルゴリズムを最適化して、スペースの解放を高速化します[＃648](https://github.com/pingcap/tidb-binlog/pull/648)
-   Drainer
    -   下流[＃655](https://github.com/pingcap/tidb-binlog/pull/655)の`BIT`列の更新の失敗を修正

## TiDB アンシブル {#tidb-ansible}

-   `ansible`コマンドとその`jmespath`および`jinja2`依存パッケージ[＃807](https://github.com/pingcap/tidb-ansible/pull/807)事前チェック機能を追加します。
-   Pumpに`stop-write-at-available-space`パラメータ（デフォルトでは 10 GiB）を追加し、使用可能なディスク容量がパラメータ値[＃807](https://github.com/pingcap/tidb-ansible/pull/807)より小さい場合にPumpでのbinlogファイルの書き込みを停止します。
