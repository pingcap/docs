---
title: TiDB 2.1.8 Release Notes
---

# TiDB2.1.8リリースノート {#tidb-2-1-8-release-notes}

発売日：2019年4月12日

TiDBバージョン：2.1.8

TiDB Ansibleバージョン：2.1.8

## TiDB {#tidb}

-   NULL値のパラメーター[＃9930](https://github.com/pingcap/tidb/pull/9930)がある場合、 `GROUP_CONCAT`の関数の処理ロジックがMySQLと互換性がないという問題を修正します。
-   `Distinct`モード[＃9931](https://github.com/pingcap/tidb/pull/9931)での10進値の等価性チェックの問題を修正しました
-   `SHOW FULL COLUMNS`ステートメントの日付、日時、およびタイムスタンプタイプの照合順序互換性の問題を修正します
    -   [＃9938](https://github.com/pingcap/tidb/pull/9938)
    -   [＃10114](https://github.com/pingcap/tidb/pull/10114)
-   フィルタリング条件に相関列が含まれている場合に行数の推定が不正確になる問題を修正します[＃9937](https://github.com/pingcap/tidb/pull/9937)
-   `DATE_ADD`と`DATE_SUB`の関数間の互換性の問題を修正します
    -   [＃9963](https://github.com/pingcap/tidb/pull/9963)
    -   [＃9966](https://github.com/pingcap/tidb/pull/9966)
-   互換性を向上させるために、 `STR_TO_DATE`関数の`%H`形式をサポートします[＃9964](https://github.com/pingcap/tidb/pull/9964)
-   `GROUP_CONCAT`の関数が一意のインデックスでグループ化されている場合に結果が間違っているという問題を修正します[＃9969](https://github.com/pingcap/tidb/pull/9969)
-   オプティマイザのヒントに一致しないテーブル名が含まれている場合に警告を返します[＃9970](https://github.com/pingcap/tidb/pull/9970)
-   ログ形式を統合して、分析用ツールを使用したログの収集を容易にします統合ログ形式
-   多くのNULL値が不正確な統計推定を引き起こす問題を修正します[＃9979](https://github.com/pingcap/tidb/pull/9979)
-   TIMESTAMPタイプのデフォルト値が境界値[＃9987](https://github.com/pingcap/tidb/pull/9987)の場合にエラーが報告される問題を修正します
-   13の[＃10000](https://github.com/pingcap/tidb/pull/10000)を検証し`time_zone`
-   `2019.01.01`回のフォーマットをサポート[＃10001](https://github.com/pingcap/tidb/pull/10001)
-   場合によっては`EXPLAIN`ステートメントによって返される結果に行数の見積もりが正しく表示されない問題を修正します[＃10044](https://github.com/pingcap/tidb/pull/10044)
-   `KILL TIDB [session id]`がステートメントの実行を即座に停止できない場合があるという問題を修正します[＃9976](https://github.com/pingcap/tidb/pull/9976)
-   場合によっては、一定のフィルタリング条件の述語プッシュダウンの問題を修正します[＃10049](https://github.com/pingcap/tidb/pull/10049)
-   読み取り専用ステートメントが正しく処理されない場合があるという問題を修正します[＃10048](https://github.com/pingcap/tidb/pull/10048)

## PD {#pd}

-   `regionScatterer`が無効な[＃1482](https://github.com/pingcap/pd/pull/1482)を生成する可能性がある問題を修正し`OperatorStep`
-   ホットストアがキーの誤った統計を作成する問題を修正します[＃1487](https://github.com/pingcap/pd/pull/1487)
-   `MergeRegion`演算子[＃1495](https://github.com/pingcap/pd/pull/1495)の短すぎるタイムアウトの問題を修正します
-   TSO要求を処理するPDサーバーの経過時間メトリックを追加します[＃1502](https://github.com/pingcap/pd/pull/1502)

## TiKV {#tikv}

-   読み取りトラフィックの誤った統計の問題を修正します[＃4441](https://github.com/tikv/tikv/pull/4441)
-   リージョンが多すぎる場合のraftstoreのパフォーマンスの問題を修正します[＃4484](https://github.com/tikv/tikv/pull/4484)
-   レベル[＃4464](https://github.com/tikv/tikv/pull/4464)のSSTファイルの数が`level_zero_slowdown_writes_trigger/2`を超える場合は、ファイルを取り込めないでください。

## ツール {#tools}

-   Lightningのテーブルのインポート順序を最適化して、インポートプロセス中にクラスタで`Checksum`と`Analyze`を実行する大きなテーブルの影響を減らし、 `Checksum`と[＃156](https://github.com/pingcap/tidb-lightning/pull/156)の成功率を向上させ`Analyze` 。
-   KVエンコーダー[＃145](https://github.com/pingcap/tidb-lightning/pull/145)の追加の解析作業を回避するために、データソースファイルのコンテンツをTiDBの`types.Datum`に直接解析することにより、LightningのエンコードSQLパフォーマンスを50％向上させます。
-   PiDB Binlog Pumpに`storage.sync-log`の構成アイテムを追加して、 [＃529](https://github.com/pingcap/tidb-binlog/pull/529)でローカルストレージのディスクの非同期フラッシュをサポートします。
-   TiDBBinlogPumpとDrainer1間の通信のトラフィック圧縮をサポートし[＃530](https://github.com/pingcap/tidb-binlog/pull/530)
-   TiDB Binlog Drainerに`syncer.sql-mode`の構成アイテムを追加して、異なる`sql-mode`秒を使用したDDLクエリの解析をサポートします[＃513](https://github.com/pingcap/tidb-binlog/pull/513)
-   TiDB Binlog Drainerに`syncer.ignore-table`の構成アイテムを追加して、複製されないフィルタリングテーブルをサポートします[＃526](https://github.com/pingcap/tidb-binlog/pull/526)

## TiDB Ansible {#tidb-ansible}

-   オペレーティングシステムのバージョン制限を変更し、CentOS7.0以降およびRedHat7.0以降のみをサポートします[＃734](https://github.com/pingcap/tidb-ansible/pull/734)
-   すべてのOS3で`epollexclusive`がサポートされているかどうかをチェックする機能を追加し[＃728](https://github.com/pingcap/tidb-ansible/pull/728)
-   ローリングアップデートのバージョン制限を追加して、2.0.1以前のバージョンから2.1以前のバージョンへのアップグレードを禁止します[＃728](https://github.com/pingcap/tidb-ansible/pull/728)
