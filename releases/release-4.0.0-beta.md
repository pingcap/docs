---
title: TiDB 4.0 Beta Release Notes
---

# TiDB 4.0 ベータ版リリースノート {#tidb-4-0-beta-release-notes}

発売日：2020年1月17日

TiDB バージョン: 4.0.0 ベータ版

TiDB Ansible バージョン: 4.0.0 ベータ版

## TiDB {#tidb}

-   `INSERT` / `REPLACE` / `DELETE` / `UPDATE`の実行中に使用されたメモリが`MemQuotaQuery`設定項目で指定した制限を超えた場合、ログを出力するか、SQLの実行をキャンセルします。実際の動作は`OOMAction`構成によって異なります。 [#14299](https://github.com/pingcap/tidb/pull/14299)
-   駆動テーブルと被駆動テーブルの両方の行数を考慮することで、コスト`Index Join`の計算精度が向上します[#12085](https://github.com/pingcap/tidb/pull/12085)
-   オプティマイザーの動作を制御し、オプティマイザーをより安定させるための 15 個の SQL ヒントを追加します。
    -   [#11746](https://github.com/pingcap/tidb/pull/11746)
    -   [#12246](https://github.com/pingcap/tidb/pull/12246)
    -   [#12382](https://github.com/pingcap/tidb/pull/12382)
-   クエリに含まれる列をインデックス[#12022](https://github.com/pingcap/tidb/pull/12022)で完全にカバーできる場合、パフォーマンスが向上します。
-   インデックス マージ機能のサポートにより、テーブル クエリのパフォーマンスが向上します[#12843](https://github.com/pingcap/tidb/pull/12843)
-   インデックス結果をキャッシュし、重複した結果を排除することで、範囲計算のパフォーマンスを向上させ、CPU オーバーヘッドを削減します[#12856](https://github.com/pingcap/tidb/pull/12856)
-   低速ログのレベルを通常のログのレベルから分離します[#12359](https://github.com/pingcap/tidb/pull/12359)
-   `oom-use-tmp-storage`パラメータ (デフォルトでは`true` ) を追加して、単一の SQL ステートメントの実行でのメモリ使用量が`mem-quota-query`を超え、SQL に`Hash Join` [#12067](https://github.com/pingcap/tidb/pull/12067)が含まれる場合に、一時ファイルを使用して中間結果をキャッシュするかどうかを制御します。
-   `create index` / `alter table`を使用した式インデックスの作成と`drop index`を使用した式インデックス[#14117](https://github.com/pingcap/tidb/pull/14117)の削除をサポート
-   切り捨てられる SQL 出力の数を減らすには、 `query-log-max-len`パラメータのデフォルト値を`4096`に増やします。このパラメータは動的に調整できます。 [#12491](https://github.com/pingcap/tidb/pull/12491)
-   システムがランダムな整数を主キーに自動的に割り当てるかどうかを制御するために、列属性に`AutoRandom`キーワードを追加することをサポートします。これにより、 `AUTO_INCREMENT`主キーによって引き起こされるホットスポット問題が回避されます[#13127](https://github.com/pingcap/tidb/pull/13127)
-   サポートテーブルロック[#11038](https://github.com/pingcap/tidb/pull/11038)
-   条件付きフィルタリングに`ADMIN SHOW DDL JOBS`の`LIKE`または`WHERE`句を使用するサポート[#12484](https://github.com/pingcap/tidb/pull/12484)
-   `information_schema.tables`テーブルの`TIDB_ROW_ID_SHARDING_INFO`列を追加して、 `RowID`散乱情報を出力します (たとえば、テーブル`A`の`SHARD_ROW_ID_BITS`列の値は`"SHARD_BITS={bit_number}"`です) [#13418](https://github.com/pingcap/tidb/pull/13418)
-   SQL エラー メッセージのエラー コードを最適化し、 `ERROR 1105 (HY000)`コードが複数のエラー メッセージに使用される状況 ( `Unknown Error`タイプ) を回避します。
    -   [#13646](https://github.com/pingcap/tidb/pull/13646)
    -   [#13233](https://github.com/pingcap/tidb/pull/13233)
    -   [#14054](https://github.com/pingcap/tidb/pull/14054)
-   離散型の狭いデータ範囲を`point set`に変換し、行数推定時にCM-Sketchを使用して推定精度を向上させる[#11524](https://github.com/pingcap/tidb/pull/11524)
-   通常の`Analyze`について`TopN`情報を CM-Sketch から抽出し、頻繁に発生する値を別途保持する[#11409](https://github.com/pingcap/tidb/pull/11409)
-   CM-Sketchの奥行きと幅、 `TopN`情報[#11278](https://github.com/pingcap/tidb/pull/11278)の数の動的調整をサポート
-   SQL バインディングの自動キャプチャと進化をサポート[#12434](https://github.com/pingcap/tidb/pull/12434)
-   `Chunk`を使用してTiKVとの通信のエンコード形式を最適化し、通信パフォーマンスを向上させます[#13349](https://github.com/pingcap/tidb/pull/13349)
-   新しい行ストア形式をサポートして、ワイドテーブル[#12634](https://github.com/pingcap/tidb/pull/12634)のパフォーマンスを向上させます。
-   `Recover Binlog`インターフェイスを最適化して、クライアント[#13740](https://github.com/pingcap/tidb/pull/13740)に戻る前にすべてのトランザクションがコミットされるのを確実に待機します。
-   HTTP `info/all`インターフェイス[#13025](https://github.com/pingcap/tidb/pull/13025)を介して、クラスター内の TiDB サーバーによって有効になっているbinlogステータスのクエリをサポートします。
-   悲観的トランザクション モード[#14087](https://github.com/pingcap/tidb/pull/14087)を使用する場合、MySQL 互換の`Read Committed`トランザクション分離レベルをサポートします。
-   大規模な取引をサポートします。トランザクション サイズは、物理メモリのサイズによって制限されます。
    -   [#11807](https://github.com/pingcap/tidb/pull/11807)
    -   [#13299](https://github.com/pingcap/tidb/pull/13299)
    -   [#13599](https://github.com/pingcap/tidb/pull/13599)
-   `Kill` [#10841](https://github.com/pingcap/tidb/pull/10841)の安定性を向上
-   `LOAD DATA` [#11029](https://github.com/pingcap/tidb/pull/11029)の区切り文字として 16 進数および 2 進数の式をサポート
-   `IndexLookupJoin`を`IndexHashJoin`と`IndexMergeJoin`に分割することで、 `IndexLookupJoin`のパフォーマンスを向上させ、実行時のメモリ消費量を削減します[#13714](https://github.com/pingcap/tidb/pull/13714)
-   RBAC [#13014](https://github.com/pingcap/tidb/pull/13014)に関連するいくつかの問題を修正
-   `SELECT`ステートメントに`union` [#12595](https://github.com/pingcap/tidb/pull/12595)が含まれるため`VIEW`が作成できない問題を修正
-   `CAST`機能に関するいくつかの問題を修正
    -   [#11493](https://github.com/pingcap/tidb/pull/11493)
    -   [#14323](https://github.com/pingcap/tidb/pull/14323)
    -   [#12864](https://github.com/pingcap/tidb/pull/12864)
    -   [#11989](https://github.com/pingcap/tidb/pull/11989)
-   トラブルシューティングを容易にするために、TiKV RPC の詳細`backoff`情報をスロー ログに出力します[#13770](https://github.com/pingcap/tidb/pull/13770)
-   高価なログ[#12809](https://github.com/pingcap/tidb/pull/12809)のメモリ統計の形式を最適化し、統一します。
-   `EXPLAIN`の明示的な形式を最適化し、オペレーターによるメモリとディスクの使用状況に関する情報の出力をサポートします[#13720](https://github.com/pingcap/tidb/pull/13720)
-   トランザクション サイズに基づいて`LOAD DATA`重複値のチェックを最適化し、 `tidb_dml_batch_size`パラメータを構成することでトランザクション サイズの設定をサポートします[#11132](https://github.com/pingcap/tidb/pull/11132)
-   データ準備ルーチンとコミット ルーチンを分離し、ワークロードを異なるワーカーに割り当てることで`LOAD DATA`のパフォーマンスを最適化します[#11284](https://github.com/pingcap/tidb/pull/11284)

## TiKV {#tikv}

-   RocksDB バージョンを 6.4.6 にアップグレードします。
-   TiKV の起動時に 2GB の空のファイルを自動的に作成することで、ディスク容量が使い果たされると、システムが圧縮タスクを正常に実行できなくなる問題を修正します[#6321](https://github.com/tikv/tikv/pull/6321)
-   迅速なバックアップと復元をサポート
    -   [#6349](https://github.com/tikv/tikv/pull/6349)
    -   [#6283](https://github.com/tikv/tikv/pull/6283)
    -   [#6202](https://github.com/tikv/tikv/pull/6202)
    -   [#6071](https://github.com/tikv/tikv/pull/6071)
    -   [#5800](https://github.com/tikv/tikv/pull/5800)
    -   [#5683](https://github.com/tikv/tikv/pull/5683)
-   Followerレプリカからのデータ読み取りのサポート
    -   [#5401](https://github.com/tikv/tikv/pull/5401)
    -   [#6396](https://github.com/tikv/tikv/pull/6396)
-   インデックス[#5682](https://github.com/tikv/tikv/pull/5682)による TiDB 読み取りデータのパフォーマンスを向上させます。
-   `CAST`関数の動作が TiKV と TiDB で一貫性がない問題を修正
    -   [#6440](https://github.com/tikv/tikv/pull/6440)
    -   [#5528](https://github.com/tikv/tikv/pull/5528)
    -   [#5141](https://github.com/tikv/tikv/pull/5141)
    -   [#5095](https://github.com/tikv/tikv/pull/5095)
    -   [#5038](https://github.com/tikv/tikv/pull/5038)
    -   [#5761](https://github.com/tikv/tikv/pull/5761)
    -   [#5455](https://github.com/tikv/tikv/pull/5455)
    -   [#5179](https://github.com/tikv/tikv/pull/5179)
    -   [#6463](https://github.com/tikv/tikv/pull/6463)

## PD {#pd}

-   storageノードの負荷情報に応じたホットスポットスケジューリングの最適化をサポート
    -   [#1750](https://github.com/pingcap/pd/pull/1750)
-   さまざまなスケジュール ルールを組み合わせて、任意のデータ範囲のレプリカ数、storageの場所、storageホストの種類、役割の制御をサポートする配置ルール機能を追加します。
    -   [#1904](https://github.com/pingcap/pd/pull/1904)
    -   [#1834](https://github.com/pingcap/pd/pull/1834)
-   プラグインを使用したサポート (実験的) [#1799](https://github.com/pingcap/pd/pull/1799)
-   スケジューラーがカスタマイズされた構成とキー範囲をサポートする機能を追加 (実験的) [#1791](https://github.com/pingcap/pd/pull/1791)
-   クラスターの負荷情報に応じてスケジューリング速度を自動的に調整するサポート (実験的、デフォルトで無効) [#1902](https://github.com/pingcap/pd/pull/1902)

## ツール {#tools}

-   TiDB Lightning
    -   コマンドライン ツールにパラメータを追加して、ダウンストリーム データベース[#253](https://github.com/pingcap/tidb-lightning/pull/253)のパスワードを設定します。

## TiDB Ansible {#tidb-ansible}

-   ダウンロードしたパッケージが不完全な場合に備えて、パッケージにチェックサムチェックを追加します[#1002](https://github.com/pingcap/tidb-ansible/pull/1002)
-   systemd バージョンのチェックをサポートします`systemd-219-52`以降である必要があります[#1074](https://github.com/pingcap/tidb-ansible/pull/1074)
-   TiDB Lightningの起動時にログ ディレクトリが誤って作成される問題を修正[#1103](https://github.com/pingcap/tidb-ansible/pull/1103)
-   TiDB Lightningのカスタマイズポートが無効になる問題を修正[#1107](https://github.com/pingcap/tidb-ansible/pull/1107)
-   TiFlash [#1119](https://github.com/pingcap/tidb-ansible/pull/1119)の導入と保守のサポート
