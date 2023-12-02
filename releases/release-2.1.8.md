---
title: TiDB 2.1.8 Release Notes
---

# TiDB 2.1.8 リリースノート {#tidb-2-1-8-release-notes}

発売日：2019年4月12日

TiDB バージョン: 2.1.8

TiDB Ansible バージョン: 2.1.8

## TiDB {#tidb}

-   NULL値パラメータ[#9930](https://github.com/pingcap/tidb/pull/9930)がある場合、 `GROUP_CONCAT`関数の処理ロジックがMySQLと互換性がない問題を修正
-   `Distinct`モード[#9931](https://github.com/pingcap/tidb/pull/9931)における 10 進数値の等価性チェックの問題を修正しました。
-   `SHOW FULL COLUMNS`ステートメントの日付、日時、およびタイムスタンプ タイプの照合順序順序の互換性の問題を修正します。
    -   [#9938](https://github.com/pingcap/tidb/pull/9938)
    -   [#10114](https://github.com/pingcap/tidb/pull/10114)
-   フィルタ条件に相関列[#9937](https://github.com/pingcap/tidb/pull/9937)が含まれる場合、行数の推定が不正確になる問題を修正
-   `DATE_ADD`と`DATE_SUB`関数間の互換性の問題を修正
    -   [#9963](https://github.com/pingcap/tidb/pull/9963)
    -   [#9966](https://github.com/pingcap/tidb/pull/9966)
-   互換性を向上させるために`STR_TO_DATE`機能の`%H`フォーマットをサポート[#9964](https://github.com/pingcap/tidb/pull/9964)
-   `GROUP_CONCAT`関数を一意のインデックスでグループ化すると結果が不正になる問題を修正[#9969](https://github.com/pingcap/tidb/pull/9969)
-   オプティマイザー ヒントに一致しないテーブル名が含まれている場合に警告を返します[#9970](https://github.com/pingcap/tidb/pull/9970)
-   ログフォーマットを統一し、分析ツールによるログ収集を容易にする 統一ログフォーマット
-   NULL 値が多いと統計推定が不正確になる問題を修正[#9979](https://github.com/pingcap/tidb/pull/9979)
-   TIMESTAMP型のデフォルト値が境界値[#9987](https://github.com/pingcap/tidb/pull/9987)の場合にエラーが報告される問題を修正
-   `time_zone` [＃10000](https://github.com/pingcap/tidb/pull/10000)の値を検証します
-   `2019.01.01`回フォーマット[#10001](https://github.com/pingcap/tidb/pull/10001)をサポート
-   場合によっては、 `EXPLAIN`によって返される結果に行数の推定が正しく表示されない問題を修正します[#10044](https://github.com/pingcap/tidb/pull/10044)
-   `KILL TIDB [session id]`ステートメントの実行を即座に停止できない場合がある問題を修正[#9976](https://github.com/pingcap/tidb/pull/9976)
-   場合によっては定数フィルタリング条件の述語プッシュダウンの問題を修正します[#10049](https://github.com/pingcap/tidb/pull/10049)
-   場合によっては読み取り専用ステートメントが正しく処理されない問題を修正します[#10048](https://github.com/pingcap/tidb/pull/10048)

## PD {#pd}

-   `regionScatterer`が無効な`OperatorStep` [#1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正
-   ホット ストアがキーの不正な統計を作成する問題を修正します[#1487](https://github.com/pingcap/pd/pull/1487)
-   `MergeRegion`オペレーター[#1495](https://github.com/pingcap/pd/pull/1495)の短すぎるタイムアウト問題を修正
-   TSO リクエストを処理する PDサーバーの経過時間メトリクスを追加[#1502](https://github.com/pingcap/pd/pull/1502)

## TiKV {#tikv}

-   読み取りトラフィックの統計が間違っている問題を修正[#4441](https://github.com/tikv/tikv/pull/4441)
-   存在するリージョンが多すぎる場合の raftstore のパフォーマンスの問題を修正[#4484](https://github.com/tikv/tikv/pull/4484)
-   レベル 0 SST ファイルの数が`level_zero_slowdown_writes_trigger/2` [#4464](https://github.com/tikv/tikv/pull/4464)を超える場合はファイルを取り込まない

## ツール {#tools}

-   Lightning のテーブルのインポート順序を最適化して、インポート プロセス中にクラスタ上で`Checksum`と`Analyze`を実行する大きなテーブルの影響を軽減し、 `Checksum`と`Analyze`の成功率を向上させます[#156](https://github.com/pingcap/tidb-lightning/pull/156)
-   KV エンコーダ[#145](https://github.com/pingcap/tidb-lightning/pull/145)追加の解析作業を回避するために、データ ソース ファイルのコンテンツを TiDB の`types.Datum`に直接解析することで、Lightning のエンコード SQL パフォーマンスが 50% 向上しました。
-   TiDB Binlog Pumpに`storage.sync-log`構成項目を追加して、 Pump [#529](https://github.com/pingcap/tidb-binlog/pull/529)でのローカルstorageのディスクの非同期フラッシュをサポートします。
-   TiDB Binlog PumpとDrainer [#530](https://github.com/pingcap/tidb-binlog/pull/530)間の通信のトラフィック圧縮をサポート
-   TiDB Binlog Drainerに`syncer.sql-mode`構成項目を追加して、DDL クエリの解析に異なる`sql-mode`の使用をサポートします[#513](https://github.com/pingcap/tidb-binlog/pull/513)
-   複製されないテーブルのフィルタリングをサポートするために、TiDB Binlog Drainerに`syncer.ignore-table`構成項目を追加します[#526](https://github.com/pingcap/tidb-binlog/pull/526)

## TiDB Ansible {#tidb-ansible}

-   オペレーティング システムのバージョン制限を変更し、CentOS 7.0 以降および Red Hat 7.0 以降のみをサポートするようにします[#734](https://github.com/pingcap/tidb-ansible/pull/734)
-   `epollexclusive`が各OSでサポートされているかを確認する機能を追加[#728](https://github.com/pingcap/tidb-ansible/pull/728)
-   ローリング アップデートのバージョン制限を追加して、2.0.1 以前のバージョンから 2.1 以降のバージョンへのアップグレードを禁止します[#728](https://github.com/pingcap/tidb-ansible/pull/728)
