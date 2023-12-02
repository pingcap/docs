---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 リリースノート {#tidb-5-0-3-release-notes}

発売日：2021年7月2日

TiDB バージョン: 5.0.3

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0 クラスターが v5.0 以降のバージョン (dev または v5.1) にアップグレードされると、変数`tidb_multi_statement_mode`のデフォルト値が`WARN`から`OFF`に変更されます。
    -   TiDB は、 MySQL 5.7の noop 変数`innodb_default_row_format`と互換性を持つようになりました。この変数を設定しても効果はありません。 [#23541](https://github.com/pingcap/tidb/issues/23541)

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   HTTP API を追加して、ノード[#1955](https://github.com/pingcap/tiflow/pull/1955)の変更フィード情報と正常性情報を取得します。
        -   Kafka シンク[#1942](https://github.com/pingcap/tiflow/pull/1942)に SASL/SCRAM サポートを追加します。
        -   サーバーレベル[#2070](https://github.com/pingcap/tiflow/pull/2070)で TiCDC サポート`--data-dir`を作成する

## 改善点 {#improvements}

-   TiDB

    -   `TopN`オペレーターのTiFlash [#25162](https://github.com/pingcap/tidb/pull/25162)へのプッシュダウンをサポート
    -   組み込み関数`json_unquote()`の TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)へのプッシュダウンをサポート
    -   デュアルテーブル[#25614](https://github.com/pingcap/tidb/pull/25614)からの共用体ブランチの削除をサポート
    -   組み込み関数`replace()`からTiFlash [#25565](https://github.com/pingcap/tidb/pull/25565)へのプッシュダウンをサポート
    -   組み込み関数`unix_timestamp()` 、 `concat()` 、 `year()` 、 `day()` 、 `datediff()` 、 `datesub()` 、 `concat_ws()`のTiFlash [#25564](https://github.com/pingcap/tidb/pull/25564)へのプッシュダウンをサポート
    -   集約オペレーターのコスト係数[#25241](https://github.com/pingcap/tidb/pull/25241)を最適化する
    -   `Limit`オペレーターのTiFlash [#25159](https://github.com/pingcap/tidb/pull/25159)へのプッシュダウンをサポート
    -   組み込み関数`str_to_date`からTiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)へのプッシュダウンをサポート
    -   MPP 外部結合がテーブル行数[#25142](https://github.com/pingcap/tidb/pull/25142)に基づいて構築テーブルを選択できるようにします。
    -   組み込み関数`left()` 、 `right()` 、および`abs()`のTiFlash [#25133](https://github.com/pingcap/tidb/pull/25133)へのプッシュダウンをサポート
    -   TiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)へのブロードキャスト デカルト結合のプッシュダウンをサポート
    -   `Union All`オペレーターのTiFlash [#25051](https://github.com/pingcap/tidb/pull/25051)へのプッシュダウンをサポート
    -   リージョン[#24724](https://github.com/pingcap/tidb/pull/24724)に基づいて、さまざまなTiFlashノード間の MPP クエリ ワークロードのバランスをサポートします。
    -   MPP クエリの実行後のキャッシュ内の古いリージョンの無効化をサポート[#24432](https://github.com/pingcap/tidb/pull/24432)
    -   書式指定子`%b/%M/%r/%T` [#25767](https://github.com/pingcap/tidb/pull/25767)の組み込み関数`str_to_date`の MySQL 互換性を向上します。

-   TiKV

    -   TiCDC シンクのメモリ消費を制限する[#10305](https://github.com/tikv/tikv/pull/10305)
    -   TiCDC 古い値キャッシュ[#10313](https://github.com/tikv/tikv/pull/10313)にメモリ制限の上限を追加します。

-   PD

    -   TiDB ダッシュボードを v2021.06.15.1 に更新します[#3798](https://github.com/pingcap/pd/pull/3798)

-   TiFlash

    -   `STRING`型から`DOUBLE`型へのキャストをサポート
    -   `STR_TO_DATE()`機能をサポート
    -   複数のスレッドを使用して右外部結合の非結合データを最適化する
    -   デカルト結合をサポートする
    -   `LEFT()`と`RIGHT()`関数をサポート
    -   MPP クエリでの古いリージョンの自動無効化のサポート
    -   `ABS()`機能をサポート

-   ツール

    -   TiCDC

        -   gRPC の再接続ロジックを改良し、KV クライアントのスループットを向上させる[#1586](https://github.com/pingcap/tiflow/issues/1586) [#1501](https://github.com/pingcap/tiflow/issues/1501#issuecomment-820027078) [#1682](https://github.com/pingcap/tiflow/pull/1682) [#1393](https://github.com/pingcap/tiflow/issues/1393) [#1847](https://github.com/pingcap/tiflow/pull/1847) [#1905](https://github.com/pingcap/tiflow/issues/1905) [#1904](https://github.com/pingcap/tiflow/issues/1904)
        -   ソーターの I/O エラーをより使いやすくする

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SET`型列[#25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると不正な結果が返される問題を修正
    -   `IN`式の引数[#25591](https://github.com/pingcap/tidb/issues/25591)のデータ破損の問題を修正します。
    -   GC のセッションがグローバル変数の影響を受けることを回避します[#24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリ[#25344](https://github.com/pingcap/tidb/issues/25344)で`limit`使用したときに発生するpanicの問題を修正します。
    -   `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリしたときに返される間違った値を修正しました。
    -   `ENUM`または`SET`タイプの列[#24944](https://github.com/pingcap/tidb/issues/24944)に`IFNULL`が正しく反映されない問題を修正
    -   結合サブクエリの`count` `first_row` [#24865](https://github.com/pingcap/tidb/issues/24865)に変更することによって引き起こされる間違った結果を修正しました。
    -   `ParallelApply`が`TopN`演算子[#24930](https://github.com/pingcap/tidb/issues/24930)の下で使用されるときに発生するクエリハングの問題を修正します。
    -   複数列の接頭辞インデックスを使用して SQL ステートメントを実行すると、予想より多くの結果が返される問題を修正します[#24356](https://github.com/pingcap/tidb/issues/24356)
    -   `<=>`演算子が正しく有効にならない問題を修正[#24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`オペレーター[#23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合問題を修正
    -   PartitionUnion 演算子[#23919](https://github.com/pingcap/tidb/issues/23919)の IndexMerge 結果を並べ替えるときに`index out of range`エラーが報告される問題を修正します。
    -   `tidb_snapshot`変数を予想外に大きな値に設定すると、トランザクション分離[#25680](https://github.com/pingcap/tidb/issues/25680)損なわれる可能性がある問題を修正します。
    -   ODBC スタイルの定数 (たとえば、 `{d '2020-01-01'}` ) を式[#25531](https://github.com/pingcap/tidb/issues/25531)として使用できない問題を修正します。
    -   `SELECT DISTINCT`を`Batch Get`に変換すると誤った結果が生じる問題を修正[#25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashから TiKV へのバックオフ クエリをトリガーできない問題を修正[#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` [#23839](https://github.com/pingcap/tidb/issues/23839) )のチェック時に発生する`index-out-of-range`エラーを修正
    -   相関サブクエリのインデクス結合結果が正しくない問題を修正[#25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`メトリック[#10330](https://github.com/tikv/tikv/issues/10330)を修正します
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数の型を修正しました。
    -   場合によってはACIDの破損を避けるため、正常なシャットダウン中にコールバックのクリアをスキップします[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader[#10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正
    -   `DOUBLE`を`DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)にキャストする間違った関数を修正

-   PD

    -   スケジューラーの起動後に TTL 構成をロードするときに発生するデータ競合の問題を修正します[#3771](https://github.com/tikv/pd/issues/3771)
    -   TiDBの`TIKV_REGION_PEERS`テーブルの`is_learner`フィールドが間違っているバグを修正[#3372](https://github.com/tikv/pd/issues/3372) [#24293](https://github.com/pingcap/tidb/issues/24293)
    -   ゾーン内のすべての TiKV ノードがオフラインまたはダウンしている場合、PD が他のゾーンにレプリカをスケジュールしない問題を修正します[#3705](https://github.com/tikv/pd/issues/3705)
    -   スキャターリージョンスケジューラの追加後に PD がpanicになる可能性がある問題を修正[#3762](https://github.com/tikv/pd/pull/3762)

-   TiFlash

    -   スプリット障害によりTiFlashが再起動し続ける問題を修正
    -   TiFlash がデルタ データを削除できないという潜在的な問題を修正
    -   TiFlashが`CAST`関数で非バイナリ文字に間違ったパディングを追加するバグを修正
    -   複雑な`GROUP BY`列を含む集計クエリを処理するときに誤った結果が表示される問題を修正
    -   書き込み圧力が高い場合に発生するTiFlashpanicの問題を修正
    -   右の結合キーが nullalbe ではなく、左の結合キーが null 可能である場合に発生するpanicを修正しました。
    -   `read-index`リクエストに時間がかかるという潜在的な問題を修正
    -   読み取り負荷が高いときに発生するpanicの問題を修正
    -   `Date_Format`関数が`STRING`型の引数と`NULL`値で呼び出されたときに発生する可能性があるpanicの問題を修正しました。

-   ツール

    -   TiCDC

        -   チェックポイント[#1902](https://github.com/pingcap/tiflow/issues/1902)を更新するときに TiCDC 所有者が終了する問題を修正
        -   MySQL シンクがエラーに遭遇して一時停止した後、一部の MySQL 接続がリークする可能性があるバグを修正します[#1946](https://github.com/pingcap/tiflow/pull/1946)
        -   TiCDC が`/proc/meminfo` [#2024](https://github.com/pingcap/tiflow/pull/2024)の読み取りに失敗したときに発生するpanicの問題を修正
        -   TiCDC のランタイムメモリ消費量を削減[#2012](https://github.com/pingcap/tiflow/pull/2012) [#1958](https://github.com/pingcap/tiflow/pull/1958)
        -   解決された ts [#1576](https://github.com/pingcap/tiflow/issues/1576)の計算が遅いために TiCDCサーバーのpanicを引き起こす可能性があるバグを修正しました。
        -   プロセッサ[#2142](https://github.com/pingcap/tiflow/pull/2142)の潜在的なデッドロックの問題を修正します。

    -   バックアップと復元 (BR)

        -   復元中にすべてのシステム テーブルがフィルタリングされるバグを修正[#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        -   復元中に TDE が有効になっている場合、バックアップと復元で「ファイルはすでに存在します」というエラーが報告される問題を修正します[#1179](https://github.com/pingcap/br/issues/1179)

    -   TiDB Lightning

        -   一部の特殊なデータに対するTiDB Lightningpanic問題を修正[#1213](https://github.com/pingcap/br/issues/1213)
        -   TiDB Lightning がインポートされた大きな CSV ファイルを分割するときに報告される EOF エラーを修正しました[#1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightning が`FLOAT`または`DOUBLE`型[#1186](https://github.com/pingcap/br/pull/1186)の`auto_increment`カラムを持つテーブルをインポートすると、過度に大きなベース値が生成されるバグを修正
        -   TiDB が Parquet ファイル[#1277](https://github.com/pingcap/br/pull/1277)の`DECIMAL`タイプのデータの解析に失敗する問題を修正します。
