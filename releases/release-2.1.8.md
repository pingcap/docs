---
title: TiDB 2.1.8 Release Notes
summary: TiDB 2.1.8は2019年4月12日にリリースされました。TiDB、PD、TiKV、ツール、TiDB Ansibleの様々なバグ修正と改善が含まれています。主な修正としては、MySQLとの互換性の問題、統計情報の不正確な推定、パフォーマンスの向上などが挙げられます。また、このリリースでは、TiDB Binlog PumpとDrainerの新しい設定項目と機能が追加されました。さらに、TiDB Ansibleにはオペレーティングシステムのバージョン制限とローリングアップデートが導入されました。
---

# TiDB 2.1.8 リリースノート {#tidb-2-1-8-release-notes}

発売日：2019年4月12日

TiDB バージョン: 2.1.8

TiDB Ansible バージョン: 2.1.8

## TiDB {#tidb}

-   NULL値のパラメータがある場合、 `GROUP_CONCAT`関数の処理ロジックがMySQLと互換性がない問題を修正しました[＃9930](https://github.com/pingcap/tidb/pull/9930)
-   `Distinct`モードの小数値の等価性チェックの問題を修正 [＃9931](https://github.com/pingcap/tidb/pull/9931)
-   `SHOW FULL COLUMNS`文の日付、日付時刻、およびタイムスタンプ型の照合順序順序の互換性の問題を修正しました。
    -   [＃9938](https://github.com/pingcap/tidb/pull/9938)
    -   [＃10114](https://github.com/pingcap/tidb/pull/10114)
-   フィルタリング条件に相関列が含まれている場合に行数の推定が不正確になる問題を修正[＃9937](https://github.com/pingcap/tidb/pull/9937)
-   `DATE_ADD`と`DATE_SUB`関数間の互換性の問題を修正
    -   [＃9963](https://github.com/pingcap/tidb/pull/9963)
    -   [＃9966](https://github.com/pingcap/tidb/pull/9966)
-   互換性を向上させるために、 `STR_TO_DATE`機能の`%H`フォーマットをサポートする[＃9964](https://github.com/pingcap/tidb/pull/9964)
-   `GROUP_CONCAT`関数が一意インデックスでグループ化されたときに結果が間違っている問題を修正しました [＃9969](https://github.com/pingcap/tidb/pull/9969)
-   オプティマイザヒントに一致しないテーブル名が含まれている場合に警告を返す[＃9970](https://github.com/pingcap/tidb/pull/9970)
-   ログ形式を統一し、分析ツールを使用してログを収集しやすくする統合ログ形式
-   NULL値が多すぎると統計推定が不正確になる問題を修正[＃9979](https://github.com/pingcap/tidb/pull/9979)
-   TIMESTAMP型のデフォルト値が境界値場合にエラーが報告される問題を修正 [＃9987](https://github.com/pingcap/tidb/pull/9987)
-   `time_zone` の値を検証する [＃10000](https://github.com/pingcap/tidb/pull/10000)
-   `2019.01.01`回限りのフォーマットサポート [＃10001](https://github.com/pingcap/tidb/pull/10001)
-   `EXPLAIN`文によって返される結果で行数の推定値が正しく表示されない場合がある問題を修正[＃10044](https://github.com/pingcap/tidb/pull/10044)
-   `KILL TIDB [session id]`場合によっては文の実行を即座に停止できない問題を修正[＃9976](https://github.com/pingcap/tidb/pull/9976)
-   いくつかのケースにおける定数フィルタリング条件の述語プッシュダウンの問題を修正[＃10049](https://github.com/pingcap/tidb/pull/10049)
-   読み取り専用ステートメントが一部のケースで正しく処理されない問題を修正[＃10048](https://github.com/pingcap/tidb/pull/10048)

## PD {#pd}

-   `regionScatterer`無効な`OperatorStep` を生成する可能性がある問題を修正 [＃1482](https://github.com/pingcap/pd/pull/1482)
-   ホットストアがキーの統計情報を正しく生成しない問題を修正 [＃1487](https://github.com/pingcap/pd/pull/1487)
-   `MergeRegion`オペレータの短すぎるタイムアウト問題を修正 [＃1495](https://github.com/pingcap/pd/pull/1495)
-   TSOリクエストを処理するPDサーバーの経過時間メトリックを追加する[＃1502](https://github.com/pingcap/pd/pull/1502)

## TiKV {#tikv}

-   読み取りトラフィックの統計が間違っている問題を修正[＃4441](https://github.com/tikv/tikv/pull/4441)
-   リージョンが多すぎる場合の raftstore のパフォーマンス問題を修正[＃4484](https://github.com/tikv/tikv/pull/4484)
-   レベル0のSSTファイルの数が`level_zero_slowdown_writes_trigger/2` を超える場合はファイルをインジェストしない [＃4464](https://github.com/tikv/tikv/pull/4464)

## ツール {#tools}

-   Lightning のテーブルインポートの順序を最適化して、インポートプロセス中にクラスター上で`Checksum`と`Analyze`実行する大きなテーブルの影響を軽減し、 `Checksum`と`Analyze`の成功率を向上させます[＃156](https://github.com/pingcap/tidb-lightning/pull/156)
-   KVエンコーダの追加解析作業を回避するために、データソースファイルの内容をTiDBの`types.Datum`に直接解析することで、LightningのエンコードSQLパフォーマンスを50％向上しました。 [＃145](https://github.com/pingcap/tidb-lightning/pull/145)
-   TiDB Binlog Pumpに`storage.sync-log`構成項目を追加して、 Pump でローカルストレージのディスクを非同期にフラッシュすることをサポートします。 [＃529](https://github.com/pingcap/tidb-binlog/pull/529)
-   TiDB Binlog PumpとDrainer 間の通信のトラフィック圧縮をサポート [＃530](https://github.com/pingcap/tidb-binlog/pull/530)
-   TiDB Binlog Drainerに`syncer.sql-mode`構成項目を追加して、異なる`sql-mode` sを使用してDDLクエリを解析できるようにします[＃513](https://github.com/pingcap/tidb-binlog/pull/513)
-   TiDB Binlog Drainerに`syncer.ignore-table`構成項目を追加して、複製しないテーブルのフィルタリングをサポートします[＃526](https://github.com/pingcap/tidb-binlog/pull/526)

## TiDB Ansible {#tidb-ansible}

-   オペレーティングシステムのバージョン制限を変更し、CentOS 7.0以降とRed Hat 7.0以降のみをサポートします[＃734](https://github.com/pingcap/tidb-ansible/pull/734)
-   `epollexclusive`すべてのOS でサポートされているかどうかを確認する機能を追加 [＃728](https://github.com/pingcap/tidb-ansible/pull/728)
-   ローリングアップデートのバージョン制限を追加して、2.0.1 以前のバージョンから 2.1 以降のバージョンへのアップグレードを禁止します[＃728](https://github.com/pingcap/tidb-ansible/pull/728)
