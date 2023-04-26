---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 リリースノート {#tidb-5-0-3-release-notes}

発売日：2021年7月2日

TiDB バージョン: 5.0.3

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   v4.0 クラスターが v5.0 以降のバージョン (dev または v5.1) にアップグレードされると、 `tidb_multi_statement_mode`変数のデフォルト値が`WARN`から`OFF`に変更されます。
    -   TiDB は現在、 MySQL 5.7の noop 変数`innodb_default_row_format`と互換性があります。この変数を設定しても効果はありません。 [#23541](https://github.com/pingcap/tidb/issues/23541)

## 機能強化 {#feature-enhancements}

-   ツール

    -   TiCDC

        -   ノード[#1955](https://github.com/pingcap/tiflow/pull/1955)の変更フィード情報とヘルス情報を取得するための HTTP API を追加します。
        -   kafka シンク[#1942](https://github.com/pingcap/tiflow/pull/1942)の SASL/SCRAM サポートを追加します。
        -   サーバーレベル[#2070](https://github.com/pingcap/tiflow/pull/2070)でTiCDC対応`--data-dir`にする

## 改良点 {#improvements}

-   TiDB

    -   `TopN`オペレーターをTiFlash [#25162](https://github.com/pingcap/tidb/pull/25162)にプッシュダウンするサポート
    -   組み込み関数`json_unquote()`を TiKV [#24415](https://github.com/pingcap/tidb/issues/24415)にプッシュ ダウンするサポート
    -   デュアル テーブル[#25614](https://github.com/pingcap/tidb/pull/25614)からのユニオン ブランチの削除のサポート
    -   ビルトイン機能`replace()`のTiFlash [#25565](https://github.com/pingcap/tidb/pull/25565)へのプッシュダウンに対応
    -   組み込み関数`unix_timestamp()` 、 `concat()` 、 `year()` 、 `day()` 、 `datediff()` 、 `datesub()` 、および`concat_ws()`をTiFlash [#25564](https://github.com/pingcap/tidb/pull/25564)にプッシュダウンするサポート
    -   集計演算子のコスト ファクター[#25241](https://github.com/pingcap/tidb/pull/25241)を最適化する
    -   `Limit`オペレーターをTiFlash [#25159](https://github.com/pingcap/tidb/pull/25159)にプッシュダウンするサポート
    -   ビルトイン機能`str_to_date`のTiFlash [#25148](https://github.com/pingcap/tidb/pull/25148)へのプッシュダウンに対応
    -   MPP 外部結合が、テーブルの行数[#25142](https://github.com/pingcap/tidb/pull/25142)に基づいて構築テーブルを選択できるようにします。
    -   組み込み関数`left()` 、 `right()` 、および`abs()`のTiFlash [#25133](https://github.com/pingcap/tidb/pull/25133)へのプッシュダウンをサポート
    -   ブロードキャスト デカルト結合をTiFlash [#25106](https://github.com/pingcap/tidb/pull/25106)にプッシュ ダウンするサポート
    -   `Union All`オペレーターをTiFlash [#25051](https://github.com/pingcap/tidb/pull/25051)にプッシュダウンするサポート
    -   リージョン[#24724](https://github.com/pingcap/tidb/pull/24724)に基づく異なるTiFlashノード間での MPP クエリ ワークロードのバランス調整をサポート
    -   MPP クエリ実行後のキャッシュ内の古いリージョンの無効化をサポート[#24432](https://github.com/pingcap/tidb/pull/24432)
    -   フォーマット指定子の組み込み関数`str_to_date`の MySQL 互換性を向上させる`%b/%M/%r/%T` [#25767](https://github.com/pingcap/tidb/pull/25767)

-   TiKV

    -   TiCDC シンクのメモリ消費を制限する[#10305](https://github.com/tikv/tikv/pull/10305)
    -   TiCDC 古い値キャッシュ[#10313](https://github.com/tikv/tikv/pull/10313)のメモリ制限付き上限を追加します。

-   PD

    -   TiDB ダッシュボードを v2021.06.15.1 に更新する[#3798](https://github.com/pingcap/pd/pull/3798)

-   TiFlash

    -   `STRING`型から`DOUBLE`型へのキャスト対応
    -   `STR_TO_DATE()`機能をサポート
    -   複数のスレッドを使用して、右外部結合で結合されていないデータを最適化する
    -   デカルト結合をサポート
    -   `LEFT()`と`RIGHT()`関数をサポート
    -   MPP クエリで古いリージョンを自動的に無効にするサポート
    -   `ABS()`機能をサポート

-   ツール

    -   TiCDC

        -   gRPC の再接続ロジックを改良し、KV クライアントのスループットを向上させる[#1586](https://github.com/pingcap/tiflow/issues/1586) [#1501](https://github.com/pingcap/tiflow/issues/1501#issuecomment-820027078) [#1682](https://github.com/pingcap/tiflow/pull/1682) [#1393](https://github.com/pingcap/tiflow/issues/1393) [#1847](https://github.com/pingcap/tiflow/pull/1847) [#1905](https://github.com/pingcap/tiflow/issues/1905) [#1904](https://github.com/pingcap/tiflow/issues/1904)
        -   ソーターの I/O エラーをより使いやすくする

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SET`型の列[#25669](https://github.com/pingcap/tidb/issues/25669)でマージ結合を使用すると、誤った結果が返される問題を修正します。
    -   `IN`式の引数[#25591](https://github.com/pingcap/tidb/issues/25591)のデータ破損の問題を修正します
    -   GC のセッションがグローバル変数の影響を受けないようにする[#24976](https://github.com/pingcap/tidb/issues/24976)
    -   ウィンドウ関数クエリで`limit`を使用すると発生するpanicの問題を修正します[#25344](https://github.com/pingcap/tidb/issues/25344)
    -   `Limit` [#24636](https://github.com/pingcap/tidb/issues/24636)を使用してパーティションテーブルをクエリするときに返される間違った値を修正します
    -   `ENUM`または`SET`タイプの列[#24944](https://github.com/pingcap/tidb/issues/24944)で`IFNULL`が正しく反映されない問題を修正
    -   結合サブクエリの`count` `first_row` [#24865](https://github.com/pingcap/tidb/issues/24865)に変更することによって引き起こされる誤った結果を修正します。
    -   `TopN`演算子[#24930](https://github.com/pingcap/tidb/issues/24930)の下で`ParallelApply`使用すると発生するクエリ ハングの問題を修正します。
    -   複数列のプレフィックス インデックス[#24356](https://github.com/pingcap/tidb/issues/24356)を使用して SQL ステートメントを実行すると、予想よりも多くの結果が返される問題を修正します。
    -   `<=>`オペレーターが正しく発効できない問題を修正[#24477](https://github.com/pingcap/tidb/issues/24477)
    -   並列`Apply`演算子[#23280](https://github.com/pingcap/tidb/issues/23280)のデータ競合の問題を修正します。
    -   PartitionUnion 演算子[#23919](https://github.com/pingcap/tidb/issues/23919)の IndexMerge の結果を並べ替えると、 `index out of range`のエラーが報告される問題を修正します。
    -   `tidb_snapshot`変数を予想外に大きな値に設定すると、トランザクションの分離が損なわれる可能性がある問題を修正します[#25680](https://github.com/pingcap/tidb/issues/25680)
    -   ODBC スタイルの定数 (たとえば、 `{d '2020-01-01'}` ) を式[#25531](https://github.com/pingcap/tidb/issues/25531)として使用できないという問題を修正します。
    -   `SELECT DISTINCT`を`Batch Get`に変換すると誤った結果が生じる問題を修正[#25320](https://github.com/pingcap/tidb/issues/25320)
    -   TiFlashから TiKV へのバックオフ クエリがトリガーされない問題を修正します。 [#23665](https://github.com/pingcap/tidb/issues/23665) [#24421](https://github.com/pingcap/tidb/issues/24421)
    -   `only_full_group_by` [#23839](https://github.com/pingcap/tidb/issues/23839)のチェック時に発生する`index-out-of-range`エラーを修正します。
    -   相関サブクエリのインデックス結合の結果が間違っている問題を修正[#25799](https://github.com/pingcap/tidb/issues/25799)

-   TiKV

    -   間違った`tikv_raftstore_hibernated_peer_state`メトリクスを修正する[#10330](https://github.com/tikv/tikv/issues/10330)
    -   コプロセッサ[#10176](https://github.com/tikv/tikv/issues/10176)の`json_unquote()`関数の間違った引数タイプを修正します。
    -   グレースフル シャットダウン中にコールバックのクリアをスキップして、場合によってはACIDの中断を回避します[#10353](https://github.com/tikv/tikv/issues/10353) [#10307](https://github.com/tikv/tikv/issues/10307)
    -   Leader[#10347](https://github.com/tikv/tikv/issues/10347)のレプリカ読み取りで読み取りインデックスが共有されるバグを修正します。
    -   `DOUBLE`を`DOUBLE` [#25200](https://github.com/pingcap/tidb/issues/25200)にキャストする間違った関数を修正

-   PD

    -   スケジューラーの開始後に TTL 構成をロードするときに発生するデータ競合の問題を修正します[#3771](https://github.com/tikv/pd/issues/3771)
    -   TiDB の`TIKV_REGION_PEERS`テーブルの`is_learner`フィールドが間違っているバグを修正[#3372](https://github.com/tikv/pd/issues/3372) [#24293](https://github.com/pingcap/tidb/issues/24293)
    -   ゾーン内のすべての TiKV ノードがオフラインまたはダウンしている場合、PD がレプリカを他のゾーンにスケジュールしないという問題を修正します[#3705](https://github.com/tikv/pd/issues/3705)
    -   スキャッタリージョンスケジューラが追加された後、PD がpanicになることがある問題を修正します[#3762](https://github.com/tikv/pd/pull/3762)

-   TiFlash

    -   分割失敗によりTiFlash が再起動し続ける問題を修正
    -   TiFlash が差分データを削除できない潜在的な問題を修正
    -   TiFlashが`CAST`関数で非バイナリ文字に誤ったパディングを追加するバグを修正
    -   複雑な`GROUP BY`列の集計クエリを処理するときに誤った結果が生じる問題を修正
    -   書き込み圧力が高い場合に発生するTiFlashpanicの問題を修正します。
    -   右側の jon キーが nullalbe ではなく、左側の join キーが nullable の場合に発生するpanicを修正します。
    -   `read-index`リクエストに時間がかかる潜在的な問題を修正
    -   読み取り負荷が高い場合に発生するpanicの問題を修正
    -   `Date_Format`関数が`STRING`の型引数と`NULL`値で呼び出されたときに発生する可能性があるpanicの問題を修正します。

-   ツール

    -   TiCDC

        -   チェックポイント[#1902](https://github.com/pingcap/tiflow/issues/1902)の更新時に TiCDC 所有者が終了する問題を修正
        -   MySQL シンクがエラーに遭遇して一時停止した後、一部の MySQL 接続がリークする可能性があるというバグを修正します[#1946](https://github.com/pingcap/tiflow/pull/1946)
        -   TiCDC が`/proc/meminfo` [#2024](https://github.com/pingcap/tiflow/pull/2024)の読み取りに失敗したときに発生するpanicの問題を修正します。
        -   TiCDC の実行時のメモリ消費を削減する[#2012](https://github.com/pingcap/tiflow/pull/2012) [#1958](https://github.com/pingcap/tiflow/pull/1958)
        -   解決された ts [#1576](https://github.com/pingcap/tiflow/issues/1576)の計算が遅れるため、TiCDCサーバーを引き起こす可能性があるバグを修正します。
        -   プロセッサ[#2142](https://github.com/pingcap/tiflow/pull/2142)の潜在的なデッドロックの問題を修正します。

    -   バックアップと復元 (BR)

        -   復元中にすべてのシステム テーブルがフィルター処理されるというバグを修正します[#1197](https://github.com/pingcap/br/issues/1197) [#1201](https://github.com/pingcap/br/issues/1201)
        -   復元中に TDE が有効になっていると、バックアップと復元で「ファイルが既に存在します」というエラーが報告される問題を修正します[#1179](https://github.com/pingcap/br/issues/1179)

    -   TiDB Lightning

        -   一部の特殊なデータに対するTiDB Lightningpanicの問題を修正します[#1213](https://github.com/pingcap/br/issues/1213)
        -   TiDB Lightning がインポートされた大きな CSV ファイルを分割するときに報告される EOF エラーを修正します[#1133](https://github.com/pingcap/br/issues/1133)
        -   TiDB Lightning が`FLOAT`または`DOUBLE`タイプ[#1186](https://github.com/pingcap/br/pull/1186)の`auto_increment`列を持つテーブルをインポートすると、非常に大きなベース値が生成されるバグを修正します
        -   TiDB が Parquet ファイルの`DECIMAL`型データの解析に失敗する問題を修正[#1277](https://github.com/pingcap/br/pull/1277)
