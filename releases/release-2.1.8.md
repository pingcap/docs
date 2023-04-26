---
title: TiDB 2.1.8 Release Notes
---

# TiDB 2.1.8 リリースノート {#tidb-2-1-8-release-notes}

発売日：2019年4月12日

TiDB バージョン: 2.1.8

TiDB アンシブル バージョン: 2.1.8

## TiDB {#tidb}

-   NULL 値のパラメータがある場合、 `GROUP_CONCAT`関数の処理ロジックが MySQL と互換性がない問題を修正[#9930](https://github.com/pingcap/tidb/pull/9930)
-   `Distinct`モード[#9931](https://github.com/pingcap/tidb/pull/9931)での 10 進数値の等値チェックの問題を修正
-   `SHOW FULL COLUMNS`ステートメントの日付、日時、およびタイムスタンプ タイプの照合順序互換性の問題を修正します。
    -   [#9938](https://github.com/pingcap/tidb/pull/9938)
    -   [#10114](https://github.com/pingcap/tidb/pull/10114)
-   フィルタリング条件に相関列が含まれている場合、行数の推定が不正確になる問題を修正します[#9937](https://github.com/pingcap/tidb/pull/9937)
-   `DATE_ADD`と`DATE_SUB`関数間の互換性の問題を修正します。
    -   [#9963](https://github.com/pingcap/tidb/pull/9963)
    -   [#9966](https://github.com/pingcap/tidb/pull/9966)
-   互換性を向上させるために`STR_TO_DATE`機能の`%H`形式をサポートします[#9964](https://github.com/pingcap/tidb/pull/9964)
-   `GROUP_CONCAT`関数が一意のインデックス[#9969](https://github.com/pingcap/tidb/pull/9969)でグループ化すると、結果が正しくない問題を修正します。
-   Optimizer Hints に一致しないテーブル名が含まれている場合に警告を返す[#9970](https://github.com/pingcap/tidb/pull/9970)
-   ログ形式を統一し、分析ツールによるログ収集を容易にする 統合ログ形式
-   多くの NULL 値が不正確な統計推定を引き起こす問題を修正します[#9979](https://github.com/pingcap/tidb/pull/9979)
-   TIMESTAMP 型のデフォルト値が境界値[#9987](https://github.com/pingcap/tidb/pull/9987)の場合にエラーが報告される問題を修正
-   `time_zone` [＃10000](https://github.com/pingcap/tidb/pull/10000)の値を検証する
-   `2019.01.01`時間フォーマット[#10001](https://github.com/pingcap/tidb/pull/10001)をサポート
-   `EXPLAIN`ステートメントが返す結果で、行数の見積もりが正しく表示されない場合がある問題を修正します[#10044](https://github.com/pingcap/tidb/pull/10044)
-   場合によってはステートメントの実行を`KILL TIDB [session id]`に停止できない問題を修正します[#9976](https://github.com/pingcap/tidb/pull/9976)
-   場合によっては一定のフィルタリング条件の述語プッシュダウンの問題を修正します[#10049](https://github.com/pingcap/tidb/pull/10049)
-   場合によっては読み取り専用ステートメントが正しく処理されない問題を修正します[#10048](https://github.com/pingcap/tidb/pull/10048)

## PD {#pd}

-   `regionScatterer`が無効な`OperatorStep` [#1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正
-   ホット ストアでキーの統計が正しくない問題を修正します[#1487](https://github.com/pingcap/pd/pull/1487)
-   `MergeRegion`オペレーター[#1495](https://github.com/pingcap/pd/pull/1495)のタイムアウトが短すぎる問題を修正
-   TSO 要求を処理する PDサーバーの経過時間メトリックを追加します[#1502](https://github.com/pingcap/pd/pull/1502)

## TiKV {#tikv}

-   読み取りトラフィックの誤った統計の問題を修正します[#4441](https://github.com/tikv/tikv/pull/4441)
-   リージョンが多すぎる場合の raftstore のパフォーマンスの問題を修正します[#4484](https://github.com/tikv/tikv/pull/4484)
-   レベル 0 の SST ファイルの数が`level_zero_slowdown_writes_trigger/2`を超える場合、ファイルを取り込まない[#4464](https://github.com/tikv/tikv/pull/4464)

## ツール {#tools}

-   Lightning 用にテーブルをインポートする順序を最適化して、インポート プロセス中にクラスターで`Checksum`と`Analyze`を実行する大きなテーブルの影響を減らし、 `Checksum`と`Analyze`の成功率を向上させます[#156](https://github.com/pingcap/tidb-lightning/pull/156)
-   KV エンコーダーの追加の解析作業を回避するために、データ ソース ファイルのコンテンツを TiDB の`types.Datum`に直接解析することにより、Lightning のエンコーディング SQL パフォーマンスを 50% 向上させます[#145](https://github.com/pingcap/tidb-lightning/pull/145)
-   TiDB Binlog Pumpに`storage.sync-log`構成項目を追加して、 Pump [#529](https://github.com/pingcap/tidb-binlog/pull/529)で非同期にローカルstorageのディスクをフラッシュすることをサポートします。
-   TiDB Binlog PumpとDrainer [#530](https://github.com/pingcap/tidb-binlog/pull/530)間の通信のトラフィック圧縮をサポート
-   TiDB Binlog Drainerに`syncer.sql-mode`構成項目を追加して、異なる`sql-mode`を使用して DDL クエリを解析することをサポートします[#513](https://github.com/pingcap/tidb-binlog/pull/513)
-   レプリケートされないテーブルのフィルタリングをサポートするために、TiDB Binlog Drainerに`syncer.ignore-table`構成項目を追加します[#526](https://github.com/pingcap/tidb-binlog/pull/526)

## TiDB アンシブル {#tidb-ansible}

-   オペレーティング システムのバージョン制限を変更し、CentOS 7.0 以降および Red Hat 7.0 以降のみをサポートします[#734](https://github.com/pingcap/tidb-ansible/pull/734)
-   `epollexclusive`がすべての OS でサポートされているかどうかをチェックする機能を追加します[#728](https://github.com/pingcap/tidb-ansible/pull/728)
-   ローリング アップデートのバージョン制限を追加して、2.0.1 以前のバージョンから 2.1 以降のバージョンへのアップグレードを禁止します[#728](https://github.com/pingcap/tidb-ansible/pull/728)
