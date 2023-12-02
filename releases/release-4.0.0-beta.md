---
title: TiDB 4.0 Beta Release Notes
---

# TiDB 4.0 ベータ版リリースノート {#tidb-4-0-beta-release-notes}

発売日：2020年1月17日

TiDB バージョン: 4.0.0 ベータ版

TiDB Ansible バージョン: 4.0.0 ベータ版

## TiDB {#tidb}

-   `INSERT` / `REPLACE` / `DELETE` / `UPDATE`の実行中に使用されたメモリが`MemQuotaQuery`設定項目で指定した制限を超えた場合、ログを出力するか、SQLの実行をキャンセルします。実際の動作は`OOMAction`構成によって異なります。 [#14179](https://github.com/pingcap/tidb/pull/14179) [#14289](https://github.com/pingcap/tidb/pull/14289) [#14299](https://github.com/pingcap/tidb/pull/14299)
-   駆動テーブルと被駆動テーブルの両方の行数を考慮することで、コスト`Index Join`の計算精度が向上します[#12085](https://github.com/pingcap/tidb/pull/12085)
-   オプティマイザーの動作を制御し、オプティマイザーをより安定させるための 15 個の SQL ヒントを追加します。
    -   [#11253](https://github.com/pingcap/tidb/pull/11253) [#11364](https://github.com/pingcap/tidb/pull/11364) [#11673](https://github.com/pingcap/tidb/pull/11673) [#11740](https://github.com/pingcap/tidb/pull/11740) [#11746](https://github.com/pingcap/tidb/pull/11746)
    -   [#11809](https://github.com/pingcap/tidb/pull/11809) [#11996](https://github.com/pingcap/tidb/pull/11996) [#12043](https://github.com/pingcap/tidb/pull/12043) [#12059](https://github.com/pingcap/tidb/pull/12059) [#12246](https://github.com/pingcap/tidb/pull/12246)
    -   [#12382](https://github.com/pingcap/tidb/pull/12382)
-   クエリに含まれる列をインデックス[#12022](https://github.com/pingcap/tidb/pull/12022)で完全にカバーできる場合、パフォーマンスが向上します。
-   インデックス マージ機能のサポートにより、テーブル クエリのパフォーマンスが向上します[#10121](https://github.com/pingcap/tidb/pull/10121) [#10512](https://github.com/pingcap/tidb/pull/10512) [#11245](https://github.com/pingcap/tidb/pull/11245) [#12225](https://github.com/pingcap/tidb/pull/12225) [#12248](https://github.com/pingcap/tidb/pull/12248) [#12305](https://github.com/pingcap/tidb/pull/12305) [#12843](https://github.com/pingcap/tidb/pull/12843)
-   インデックス結果をキャッシュし、重複した結果を排除することで、範囲計算のパフォーマンスを向上させ、CPU オーバーヘッドを削減します[#12856](https://github.com/pingcap/tidb/pull/12856)
-   低速ログのレベルを通常のログのレベルから分離します[#12359](https://github.com/pingcap/tidb/pull/12359)
-   `oom-use-tmp-storage`パラメータ (デフォルトでは`true` ) を追加して、単一の SQL ステートメントの実行によるメモリ使用量が`mem-quota-query`を超え、SQL に`Hash Join` [#11832](https://github.com/pingcap/tidb/pull/11832) [#11937](https://github.com/pingcap/tidb/pull/11937) [#12116](https://github.com/pingcap/tidb/pull/12116) [#12067](https://github.com/pingcap/tidb/pull/12067)が含まれる場合に、一時ファイルを使用して中間結果をキャッシュするかどうかを制御します。
-   `create index` / `alter table`を使用した式インデックスの作成と`drop index`を使用した式インデックス[#14117](https://github.com/pingcap/tidb/pull/14117)の削除をサポート
-   切り捨てられる SQL 出力の数を減らすには、 `query-log-max-len`パラメータのデフォルト値を`4096`に増やします。このパラメータは動的に調整できます。 [#12491](https://github.com/pingcap/tidb/pull/12491)
-   システムがランダムな整数を主キーに自動的に割り当てるかどうかを制御するために、列属性に`AutoRandom`キーワードを追加することをサポートします。これにより、 `AUTO_INCREMENT`主キーによって引き起こされるホットスポット問題が回避されます[#13127](https://github.com/pingcap/tidb/pull/13127)
-   サポートテーブルロック[#11038](https://github.com/pingcap/tidb/pull/11038)
-   条件付きフィルタリングに`ADMIN SHOW DDL JOBS`の`LIKE`または`WHERE`句を使用するサポート[#12484](https://github.com/pingcap/tidb/pull/12484)
-   `information_schema.tables`テーブルの`TIDB_ROW_ID_SHARDING_INFO`列を追加して、 `RowID`散乱情報を出力します (たとえば、テーブル`A`の`SHARD_ROW_ID_BITS`列の値は`"SHARD_BITS={bit_number}"`です) [#13418](https://github.com/pingcap/tidb/pull/13418)
-   SQL エラー メッセージのエラー コードを最適化し、 `ERROR 1105 (HY000)`コードが複数のエラー メッセージに使用される状況 ( `Unknown Error`タイプ) を回避します。
    -   [#14002](https://github.com/pingcap/tidb/pull/14002) [#13874](https://github.com/pingcap/tidb/pull/13874) [#13733](https://github.com/pingcap/tidb/pull/13733) [#13654](https://github.com/pingcap/tidb/pull/13654) [#13646](https://github.com/pingcap/tidb/pull/13646)
    -   [#13540](https://github.com/pingcap/tidb/pull/13540) [#13366](https://github.com/pingcap/tidb/pull/13366) [#13329](https://github.com/pingcap/tidb/pull/13329) [#13300](https://github.com/pingcap/tidb/pull/13300) [#13233](https://github.com/pingcap/tidb/pull/13233)
    -   [#13033](https://github.com/pingcap/tidb/pull/13033) [#12866](https://github.com/pingcap/tidb/pull/12866) [#14054](https://github.com/pingcap/tidb/pull/14054)
-   離散型の狭いデータ範囲を`point set`に変換し、行数推定時にCM-Sketchを使用して推定精度を向上させる[#11524](https://github.com/pingcap/tidb/pull/11524)
-   通常の`Analyze`について`TopN`情報を CM-Sketch から抽出し、頻繁に発生する値を別途保持する[#11409](https://github.com/pingcap/tidb/pull/11409)
-   CM-Sketchの奥行きと幅、 `TopN`情報[#11278](https://github.com/pingcap/tidb/pull/11278)の数の動的調整をサポート
-   SQL バインディングの自動キャプチャと進化をサポート[#13199](https://github.com/pingcap/tidb/pull/13199) [#12434](https://github.com/pingcap/tidb/pull/12434)
-   `Chunk`を使用してTiKVとの通信のエンコード形式を最適化し、通信パフォーマンスを向上させます[#12023](https://github.com/pingcap/tidb/pull/12023) [#12536](https://github.com/pingcap/tidb/pull/12536) [#12613](https://github.com/pingcap/tidb/pull/12613) [#12621](https://github.com/pingcap/tidb/pull/12621) [#12899](https://github.com/pingcap/tidb/pull/12899) [#13060](https://github.com/pingcap/tidb/pull/13060) [#13349](https://github.com/pingcap/tidb/pull/13349)
-   新しい行ストア形式をサポートして、ワイドテーブル[#12634](https://github.com/pingcap/tidb/pull/12634)のパフォーマンスを向上させます。
-   `Recover Binlog`インターフェイスを最適化して、クライアント[#13740](https://github.com/pingcap/tidb/pull/13740)に戻る前にすべてのトランザクションがコミットされるのを確実に待機します。
-   HTTP `info/all`インターフェイス[#13025](https://github.com/pingcap/tidb/pull/13025)を介して、クラスター内の TiDB サーバーによって有効になっているbinlogステータスのクエリをサポートします。
-   悲観的トランザクション モード[#14087](https://github.com/pingcap/tidb/pull/14087)を使用する場合、MySQL 互換の`Read Committed`トランザクション分離レベルをサポートします。
-   大規模な取引をサポートします。トランザクション サイズは、物理メモリのサイズによって制限されます。
    -   [#11999](https://github.com/pingcap/tidb/pull/11999) [#11986](https://github.com/pingcap/tidb/pull/11986) [#11974](https://github.com/pingcap/tidb/pull/11974) [#11817](https://github.com/pingcap/tidb/pull/11817) [#11807](https://github.com/pingcap/tidb/pull/11807)
    -   [#12133](https://github.com/pingcap/tidb/pull/12133) [#12223](https://github.com/pingcap/tidb/pull/12223) [#12980](https://github.com/pingcap/tidb/pull/12980) [#13123](https://github.com/pingcap/tidb/pull/13123) [#13299](https://github.com/pingcap/tidb/pull/13299)
    -   [#13432](https://github.com/pingcap/tidb/pull/13432) [#13599](https://github.com/pingcap/tidb/pull/13599)
-   `Kill` [#10841](https://github.com/pingcap/tidb/pull/10841)の安定性を向上
-   `LOAD DATA` [#11029](https://github.com/pingcap/tidb/pull/11029)の区切り文字として 16 進数および 2 進数の式をサポート
-   `IndexLookupJoin`を`IndexHashJoin`と`IndexMergeJoin`に分割することで、 `IndexLookupJoin`のパフォーマンスを向上させ、実行時のメモリ消費量を削減します[#8861](https://github.com/pingcap/tidb/pull/8861) [#12139](https://github.com/pingcap/tidb/pull/12139) [#12349](https://github.com/pingcap/tidb/pull/12349) [#13238](https://github.com/pingcap/tidb/pull/13238) [#13451](https://github.com/pingcap/tidb/pull/13451) [#13714](https://github.com/pingcap/tidb/pull/13714)
-   RBAC [#13896](https://github.com/pingcap/tidb/pull/13896) [#13820](https://github.com/pingcap/tidb/pull/13820) [#13940](https://github.com/pingcap/tidb/pull/13940) [#14090](https://github.com/pingcap/tidb/pull/14090) [#13940](https://github.com/pingcap/tidb/pull/13940) [#13014](https://github.com/pingcap/tidb/pull/13014)に関連するいくつかの問題を修正
-   `SELECT`ステートメントに`union` [#12595](https://github.com/pingcap/tidb/pull/12595)が含まれるため`VIEW`が作成できない問題を修正
-   `CAST`機能に関するいくつかの問題を修正
    -   [#12858](https://github.com/pingcap/tidb/pull/12858) [#11968](https://github.com/pingcap/tidb/pull/11968) [#11640](https://github.com/pingcap/tidb/pull/11640) [#11483](https://github.com/pingcap/tidb/pull/11483) [#11493](https://github.com/pingcap/tidb/pull/11493)
    -   [#11376](https://github.com/pingcap/tidb/pull/11376) [#11355](https://github.com/pingcap/tidb/pull/11355) [#11114](https://github.com/pingcap/tidb/pull/11114) [#14405](https://github.com/pingcap/tidb/pull/14405) [#14323](https://github.com/pingcap/tidb/pull/14323)
    -   [#13837](https://github.com/pingcap/tidb/pull/13837) [#13401](https://github.com/pingcap/tidb/pull/13401) [#13334](https://github.com/pingcap/tidb/pull/13334) [#12652](https://github.com/pingcap/tidb/pull/12652) [#12864](https://github.com/pingcap/tidb/pull/12864)
    -   [#12623](https://github.com/pingcap/tidb/pull/12623) [#11989](https://github.com/pingcap/tidb/pull/11989)
-   トラブルシューティングを容易にするために、TiKV RPC の詳細`backoff`情報をスロー ログに出力します[#13770](https://github.com/pingcap/tidb/pull/13770)
-   高価なログ[#12809](https://github.com/pingcap/tidb/pull/12809)のメモリ統計の形式を最適化し、統一します。
-   `EXPLAIN`の明示的な形式を最適化し、オペレーターによるメモリとディスクの使用状況に関する情報の出力をサポートします[#13914](https://github.com/pingcap/tidb/pull/13914) [#13692](https://github.com/pingcap/tidb/pull/13692) [#13686](https://github.com/pingcap/tidb/pull/13686) [#11415](https://github.com/pingcap/tidb/pull/11415) [#13927](https://github.com/pingcap/tidb/pull/13927) [#13764](https://github.com/pingcap/tidb/pull/13764) [#13720](https://github.com/pingcap/tidb/pull/13720)
-   トランザクション サイズに基づいて`LOAD DATA`重複値のチェックを最適化し、 `tidb_dml_batch_size`パラメータを構成することでトランザクション サイズの設定をサポートします[#11132](https://github.com/pingcap/tidb/pull/11132)
-   データ準備ルーチンとコミット ルーチンを分離し、ワークロードを異なるワーカーに割り当てることで`LOAD DATA`のパフォーマンスを最適化します[#11533](https://github.com/pingcap/tidb/pull/11533) [#11284](https://github.com/pingcap/tidb/pull/11284)

## TiKV {#tikv}

-   RocksDB バージョンを 6.4.6 にアップグレードします。
-   TiKV の起動時に 2GB の空のファイルを自動的に作成することで、ディスク容量が使い果たされると、システムが圧縮タスクを正常に実行できなくなる問題を修正します[#6321](https://github.com/tikv/tikv/pull/6321)
-   迅速なバックアップと復元をサポート
    -   [#6462](https://github.com/tikv/tikv/pull/6462) [#6395](https://github.com/tikv/tikv/pull/6395) [#6378](https://github.com/tikv/tikv/pull/6378) [#6374](https://github.com/tikv/tikv/pull/6374) [#6349](https://github.com/tikv/tikv/pull/6349)
    -   [#6339](https://github.com/tikv/tikv/pull/6339) [#6308](https://github.com/tikv/tikv/pull/6308) [#6295](https://github.com/tikv/tikv/pull/6295) [#6286](https://github.com/tikv/tikv/pull/6286) [#6283](https://github.com/tikv/tikv/pull/6283)
    -   [#6261](https://github.com/tikv/tikv/pull/6261) [#6222](https://github.com/tikv/tikv/pull/6222) [#6209](https://github.com/tikv/tikv/pull/6209) [#6204](https://github.com/tikv/tikv/pull/6204) [#6202](https://github.com/tikv/tikv/pull/6202)
    -   [#6198](https://github.com/tikv/tikv/pull/6198) [#6186](https://github.com/tikv/tikv/pull/6186) [#6177](https://github.com/tikv/tikv/pull/6177) [#6146](https://github.com/tikv/tikv/pull/6146) [#6071](https://github.com/tikv/tikv/pull/6071)
    -   [#6042](https://github.com/tikv/tikv/pull/6042) [#5877](https://github.com/tikv/tikv/pull/5877) [#5806](https://github.com/tikv/tikv/pull/5806) [#5803](https://github.com/tikv/tikv/pull/5803) [#5800](https://github.com/tikv/tikv/pull/5800)
    -   [#5781](https://github.com/tikv/tikv/pull/5781) [#5772](https://github.com/tikv/tikv/pull/5772) [#5689](https://github.com/tikv/tikv/pull/5689) [#5683](https://github.com/tikv/tikv/pull/5683)
-   Followerレプリカからのデータ読み取りのサポート
    -   [#5051](https://github.com/tikv/tikv/pull/5051) [#5118](https://github.com/tikv/tikv/pull/5118) [#5213](https://github.com/tikv/tikv/pull/5213) [#5316](https://github.com/tikv/tikv/pull/5316) [#5401](https://github.com/tikv/tikv/pull/5401)
    -   [#5919](https://github.com/tikv/tikv/pull/5919) [#5887](https://github.com/tikv/tikv/pull/5887) [#6340](https://github.com/tikv/tikv/pull/6340) [#6348](https://github.com/tikv/tikv/pull/6348) [#6396](https://github.com/tikv/tikv/pull/6396)
-   インデックス[#5682](https://github.com/tikv/tikv/pull/5682)による TiDB 読み取りデータのパフォーマンスを向上させます。
-   `CAST`関数の動作が TiKV と TiDB で一貫性がない問題を修正
    -   [#6459](https://github.com/tikv/tikv/pull/6459) [#6461](https://github.com/tikv/tikv/pull/6461) [#6458](https://github.com/tikv/tikv/pull/6458) [#6447](https://github.com/tikv/tikv/pull/6447) [#6440](https://github.com/tikv/tikv/pull/6440)
    -   [#6425](https://github.com/tikv/tikv/pull/6425) [#6424](https://github.com/tikv/tikv/pull/6424) [#6390](https://github.com/tikv/tikv/pull/6390) [#5842](https://github.com/tikv/tikv/pull/5842) [#5528](https://github.com/tikv/tikv/pull/5528)
    -   [#5334](https://github.com/tikv/tikv/pull/5334) [#5199](https://github.com/tikv/tikv/pull/5199) [#5167](https://github.com/tikv/tikv/pull/5167) [#5146](https://github.com/tikv/tikv/pull/5146) [#5141](https://github.com/tikv/tikv/pull/5141)
    -   [#4998](https://github.com/tikv/tikv/pull/4998) [#5029](https://github.com/tikv/tikv/pull/5029) [#5099](https://github.com/tikv/tikv/pull/5099) [#5006](https://github.com/tikv/tikv/pull/5006) [#5095](https://github.com/tikv/tikv/pull/5095)
    -   [#5093](https://github.com/tikv/tikv/pull/5093) [#5090](https://github.com/tikv/tikv/pull/5090) [#4987](https://github.com/tikv/tikv/pull/4987) [#5066](https://github.com/tikv/tikv/pull/5066) [#5038](https://github.com/tikv/tikv/pull/5038)
    -   [#4962](https://github.com/tikv/tikv/pull/4962) [#4890](https://github.com/tikv/tikv/pull/4890) [#4727](https://github.com/tikv/tikv/pull/4727) [#6060](https://github.com/tikv/tikv/pull/6060) [#5761](https://github.com/tikv/tikv/pull/5761)
    -   [#5793](https://github.com/tikv/tikv/pull/5793) [#5468](https://github.com/tikv/tikv/pull/5468) [#5540](https://github.com/tikv/tikv/pull/5540) [#5548](https://github.com/tikv/tikv/pull/5548) [#5455](https://github.com/tikv/tikv/pull/5455)
    -   [#5543](https://github.com/tikv/tikv/pull/5543) [#5433](https://github.com/tikv/tikv/pull/5433) [#5431](https://github.com/tikv/tikv/pull/5431) [#5423](https://github.com/tikv/tikv/pull/5423) [#5179](https://github.com/tikv/tikv/pull/5179)
    -   [#5134](https://github.com/tikv/tikv/pull/5134) [#4685](https://github.com/tikv/tikv/pull/4685) [#4650](https://github.com/tikv/tikv/pull/4650) [#6463](https://github.com/tikv/tikv/pull/6463)

## PD {#pd}

-   storageノードの負荷情報に応じたホットスポットスケジューリングの最適化をサポート
    -   [#1870](https://github.com/pingcap/pd/pull/1870) [#1982](https://github.com/pingcap/pd/pull/1982) [#1998](https://github.com/pingcap/pd/pull/1998) [#1843](https://github.com/pingcap/pd/pull/1843) [#1750](https://github.com/pingcap/pd/pull/1750)
-   さまざまなスケジュール ルールを組み合わせて、任意のデータ範囲のレプリカ数、storageの場所、storageホストの種類、役割の制御をサポートする配置ルール機能を追加します。
    -   [#2051](https://github.com/pingcap/pd/pull/2051) [#1999](https://github.com/pingcap/pd/pull/1999) [#2042](https://github.com/pingcap/pd/pull/2042) [#1917](https://github.com/pingcap/pd/pull/1917) [#1904](https://github.com/pingcap/pd/pull/1904)
    -   [#1897](https://github.com/pingcap/pd/pull/1897) [#1894](https://github.com/pingcap/pd/pull/1894) [#1865](https://github.com/pingcap/pd/pull/1865) [#1855](https://github.com/pingcap/pd/pull/1855) [#1834](https://github.com/pingcap/pd/pull/1834)
-   プラグインを使用したサポート (実験的) [#1799](https://github.com/pingcap/pd/pull/1799)
-   スケジューラーがカスタマイズされた構成とキー範囲をサポートする機能を追加 (実験的) [#1735](https://github.com/pingcap/pd/pull/1735) [#1783](https://github.com/pingcap/pd/pull/1783) [#1791](https://github.com/pingcap/pd/pull/1791)
-   クラスターの負荷情報に応じてスケジューリング速度を自動的に調整するサポート (実験的、デフォルトで無効) [#1875](https://github.com/pingcap/pd/pull/1875) [#1887](https://github.com/pingcap/pd/pull/1887) [#1902](https://github.com/pingcap/pd/pull/1902)

## ツール {#tools}

-   TiDB Lightning
    -   コマンドライン ツールにパラメータを追加して、ダウンストリーム データベース[#253](https://github.com/pingcap/tidb-lightning/pull/253)のパスワードを設定します。

## TiDB Ansible {#tidb-ansible}

-   ダウンロードしたパッケージが不完全な場合に備えて、パッケージにチェックサムチェックを追加します[#1002](https://github.com/pingcap/tidb-ansible/pull/1002)
-   systemd バージョンのチェックをサポートします`systemd-219-52`以降である必要があります[#1020](https://github.com/pingcap/tidb-ansible/pull/1020) [#1074](https://github.com/pingcap/tidb-ansible/pull/1074)
-   TiDB Lightningの起動時にログ ディレクトリが誤って作成される問題を修正[#1103](https://github.com/pingcap/tidb-ansible/pull/1103)
-   TiDB Lightningのカスタマイズポートが無効になる問題を修正[#1107](https://github.com/pingcap/tidb-ansible/pull/1107)
-   TiFlash [#1119](https://github.com/pingcap/tidb-ansible/pull/1119)の導入と保守のサポート
