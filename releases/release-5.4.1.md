---
title: TiDB 5.4.1 Release Notes
---

# TiDB5.4.1リリースノート {#tidb-5-4-1-release-notes}

発売日：2022年5月13日

TiDBバージョン：5.4.1

## 互換性の変更 {#compatibility-changes}

TiDB v5.4.2では、製品設計に互換性の変更は導入されていません。ただし、このリリースのバグ修正により、互換性も変更される可能性があることに注意してください。詳細については、 [バグの修正](#bug-fixes)を参照してください。

## 改善 {#improvements}

-   TiDB

    -   `_tidb_rowid`列[＃31543](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリでのPointGetプランの使用をサポートする
    -   `Apply`演算子のログとメトリックをさらに追加して、並列[＃33887](https://github.com/pingcap/tidb/issues/33887)かどうかを示します。
    -   統計の収集に使用されるAnalyzeバージョン2の`TopN`のプルーニングロジックを改善します[＃34256](https://github.com/pingcap/tidb/issues/34256)
    -   Grafanaダッシュボードでの複数のKubernetesクラスターの表示のサポート[＃32593](https://github.com/pingcap/tidb/issues/32593)

-   TiKV

    -   Grafanaダッシュボードでの複数のKubernetesクラスターの表示のサポート[＃12104](https://github.com/tikv/tikv/issues/12104)

-   PD

    -   Grafanaダッシュボードでの複数のKubernetesクラスターの表示のサポート[＃4673](https://github.com/tikv/pd/issues/4673)

-   TiFlash

    -   Grafanaダッシュボードでの複数のKubernetesクラスターの表示のサポート[＃4129](https://github.com/pingcap/tiflash/issues/4129)

-   ツール

    -   TiCDC

        -   Grafanaダッシュボードで複数のKubernetesクラスターをサポートする[＃4665](https://github.com/pingcap/tiflow/issues/4665)
        -   Kafkaプロデューサーの構成パラメーターを公開して、 [＃4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にします。

    -   TiDBデータ移行（DM）

        -   `/tmp`ではなくDM-workerの作業ディレクトリを使用して内部ファイルを書き込み、タスクの停止後にディレクトリをクリーンアップするSyncerをサポートします[＃4107](https://github.com/pingcap/tiflow/issues/4107)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDBの`date_format`がMySQLと互換性のない方法で`'\n'`を処理する問題を修正します[＃32232](https://github.com/pingcap/tidb/issues/32232)
    -   `ENUM`列または`SET`列のエンコードが間違っているためにTiDBが間違ったデータを書き込む問題を修正します[＃32302](https://github.com/pingcap/tidb/issues/32302)
    -   マージ結合演算子が特定の場合に間違った結果を取得する問題を修正します[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[＃32089](https://github.com/pingcap/tidb/issues/32089)を返すときにTiDBが間違った結果を取得する問題を修正します
    -   TiFlashはまだ空の範囲のテーブルの読み取りをサポートしていませんが、TiFlashを使用して空の範囲のテーブルをスキャンするとTiDBが間違った結果を取得する問題を修正します[＃33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiDB [＃31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`列または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   クエリがエラーを報告したときにCTEがブロックされる可能性があるバグを修正します[＃31302](https://github.com/pingcap/tidb/issues/31302)
    -   列挙値[＃32428](https://github.com/pingcap/tidb/issues/32428)のNulleq関数の誤った範囲計算結果を修正しました
    -   ChunkRPCを使用してデータをエクスポートするときの[＃30880](https://github.com/pingcap/tidb/issues/30880)を修正[＃31981](https://github.com/pingcap/tidb/issues/31981)
    -   `tidb_restricted_read_only`が有効になっているときに`tidb_super_read_only`が自動的に有効にならないバグを修正します[＃31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を取得する問題を修正します[＃31789](https://github.com/pingcap/tidb/issues/31789)
    -   エスケープ文字[＃31589](https://github.com/pingcap/tidb/issues/31589)でデータが壊れた場合のデータのロードパニックを修正
    -   インデックスルックアップ結合[＃30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`のエラーを修正しました
    -   `left join`を使用して複数のテーブルのデータを削除した誤った結果を[＃31321](https://github.com/pingcap/tidb/issues/31321)
    -   TiDBが重複タスクをTiFlash1にディスパッチする可能性があるバグを修正し[＃32814](https://github.com/pingcap/tidb/issues/32814)
    -   [＃33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`の特権の付与が失敗する可能性がある問題を修正します。
    -   MySQLバイナリプロトコルでテーブルスキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションパニックを修正します[＃33509](https://github.com/pingcap/tidb/issues/33509)
    -   `tidb_enable_vectorized_expression`が有効になっている`compress()`の式を持つSQLステートメントの実行が失敗する問題を修正します[＃33397](https://github.com/pingcap/tidb/issues/33397)
    -   `reArrangeFallback`関数[＃30353](https://github.com/pingcap/tidb/issues/30353)による高いCPU使用率の問題を修正します
    -   新しいパーティションが追加されたときにテーブル属性がインデックスに登録されない問題と、パーティションが変更されたときにテーブル範囲情報が更新されない問題を修正します[＃33929](https://github.com/pingcap/tidb/issues/33929)
    -   初期化中のテーブルの`TopN`統計情報が正しくソートされないバグを修正します[＃34216](https://github.com/pingcap/tidb/issues/34216)
    -   識別できないテーブル属性をスキップして、 `INFORMATION_SCHEMA.ATTRIBUTES`テーブルから読み取るときに発生するエラーを修正します[＃33665](https://github.com/pingcap/tidb/issues/33665)
    -   `@@tidb_enable_parallel_apply`が設定されていても、 `order`プロパティが存在する場合に`Apply`演算子が並列化されないというバグを修正します[＃34237](https://github.com/pingcap/tidb/issues/34237)
    -   `sql_mode`が[＃34099](https://github.com/pingcap/tidb/issues/34099)に設定されている場合に`'0000-00-00 00:00:00'`が`datetime`列に挿入される可能性があるバグを修正し`NO_ZERO_DATE`
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`のテーブルが照会されたときにTiDBサーバーのメモリが不足する可能性がある問題を修正します。この問題は、Grafanaダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックしたときに発生する可能性があります
    -   `NOWAIT`ステートメントで、実行中のトランザクションがロック[＃32754](https://github.com/pingcap/tidb/issues/32754)に遭遇したときにすぐに返されないバグを修正します。
    -   `GBK`文字セットと`gbk_bin`照合順序[＃31308](https://github.com/pingcap/tidb/issues/31308)でテーブルを作成するときに失敗するバグを修正します
    -   `enable-new-charset`が`on`の場合、照合順序を使用した`GBK`文字セットテーブルの作成が「不明な文字セット」エラー[＃31297](https://github.com/pingcap/tidb/issues/31297)で失敗するバグを修正します。

-   TiKV

    -   マージされるターゲットリージョンが無効であるためにTiKVがパニックになり、ピアを予期せず破壊する問題を修正します[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージが原因でTiKVがパニックになるバグを修正します[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足（OOM）の問題を修正します[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   TiKVが[＃9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する可能性のあるパニックの問題を修正します。
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[＃12109](https://github.com/tikv/tikv/issues/12109)
    -   ターゲットピアがリージョン[＃12048](https://github.com/tikv/tikv/issues/12048)のマージ時に初期化されずに破棄されたピアに置き換えられたときに発生するTiKVパニックの問題を修正します。
    -   TiKVが2年以上実行されている場合にパニックになる可能性があるバグを修正します[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   ロックの解決ステップ[＃11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことにより、TiCDCの回復時間を短縮します。
    -   ピアステータスが`Applying`のときにスナップショットファイルを削除することによって引き起こされるパニックの問題を修正し[＃11746](https://github.com/tikv/tikv/issues/11746)
    -   ピアを破棄すると待ち時間が長くなる可能性があるという問題を修正します[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   リソースメータリング[＃12234](https://github.com/tikv/tikv/issues/12234)の無効なアサーションによって引き起こされるパニックの問題を修正します
    -   一部のコーナーケースでスコアの計算が不正確になる問題を修正します[＃12254](https://github.com/tikv/tikv/issues/12254)
    -   `resolved_ts`モジュールによって引き起こされたOOMの問題を修正し、メトリックを追加します[＃12159](https://github.com/tikv/tikv/issues/12159)
    -   ネットワークが貧弱な場合に、正常にコミットされた楽観的なトランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[＃34066](https://github.com/pingcap/tidb/issues/34066)
    -   貧弱なネットワークでレプリカ読み取りが有効になっている場合に発生するTiKVパニックの問題を修正します[＃12046](https://github.com/tikv/tikv/issues/12046)

-   PD

    -   `dr-autosync`の`Duration`のフィールドを動的に構成できない問題を修正します[＃4651](https://github.com/tikv/pd/issues/4651)
    -   大容量のストア（たとえば2T）が存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されないという問題を修正します[＃4805](https://github.com/tikv/pd/issues/4805)
    -   ラベル分布のメトリックにラベルが残っている問題を修正します[＃4825](https://github.com/tikv/pd/issues/4825)

-   TiFlash

    -   TLSが有効になっているときに発生するパニックの問題を修正します[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   遅れているリージョンピア[＃4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンマージによって引き起こされる可能性のあるメタデータの破損を修正します
    -   エラーが発生した場合に`JOIN`を含むクエリがハングする可能性がある問題を修正します[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPPタスクがスレッドを永久にリークする可能性があるバグを修正します[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   `FLOAT`から[＃3998](https://github.com/pingcap/tiflash/issues/3998)をキャストするときに発生するオーバーフローを修正し`DECIMAL`
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   ローカルトンネルが有効になっている場合、MPPクエリをキャンセルすると、タスクが永久にハングする可能性があるバグを修正します[＃4229](https://github.com/pingcap/tiflash/issues/4229)
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します[＃4098](https://github.com/pingcap/tiflash/issues/4098)
    -   `DATETIME`から[＃4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正し`DECIMAL`
    -   `Snapshot`が複数のDDL操作と同時に適用された場合のTiFlashパニックの潜在的な問題を修正します[＃4072](https://github.com/pingcap/tiflash/issues/4072)
    -   無効なストレージディレクトリ構成が予期しない動作につながるバグを修正します[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないというバグを修正します[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `INT`から`DECIMAL`をキャストするとオーバーフロー[＃3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正します
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正します
    -   日付形式が`'\n'`を無効な区切り文字[＃4036](https://github.com/pingcap/tiflash/issues/4036)として識別する問題を修正します
    -   読み取りワークロードが重い場合に列を追加した後の潜在的なクエリエラーを修正する[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   メモリ制限が有効になっているときに発生するパニックの問題を修正します[＃3902](https://github.com/pingcap/tiflash/issues/3902)
    -   [＃4778](https://github.com/pingcap/tiflash/issues/4778)の潜在的なデータ破損を修正
    -   多くの削除操作があるテーブルでクエリを実行するときに発生する可能性のあるエラーを修正する[＃4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多くの「キープアライブウォッチドッグ起動」エラーをランダムに報告するバグを修正します[＃4192](https://github.com/pingcap/tiflash/issues/4192)
    -   どの領域範囲にも一致しないデータがTiFlashノード[＃4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正します
    -   GC1の後に空のセグメントをマージできないバグを修正し[＃4511](https://github.com/pingcap/tiflash/issues/4511)

-   ツール

    -   バックアップと復元（BR）

        -   バックアップの再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正します[＃32423](https://github.com/pingcap/tidb/issues/32423)
        -   BRがRawKV1のバックアップに失敗する問題を修正し[＃32607](https://github.com/pingcap/tidb/issues/32607)
        -   インクリメンタル復元後にレコードをテーブルに挿入するときに重複する主キーを修正する[＃33596](https://github.com/pingcap/tidb/issues/33596)
        -   空のクエリ[＃33322](https://github.com/pingcap/tidb/issues/33322)を使用したDDLジョブが原因で、BRインクリメンタルリストアが誤ってエラーを返すバグを修正します。
        -   復元操作の終了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[＃31034](https://github.com/pingcap/tidb/issues/31034)
        -   復元中にリージョンに一貫性がない場合にBRが十分な回数再試行しない問題を修正します[＃33419](https://github.com/pingcap/tidb/issues/33419)
        -   小さなファイルのマージが有効になっているときにBRがときどきパニックになる可能性がある問題を修正します[＃33801](https://github.com/pingcap/tidb/issues/33801)
        -   BRまたはTiDBLightningが異常終了した後にスケジューラが再開しない問題を修正します[＃33546](https://github.com/pingcap/tidb/issues/33546)

    -   TiCDC

        -   所有者の変更によって引き起こされた誤ったメトリックを修正する[＃4774](https://github.com/pingcap/tiflow/issues/4774)
        -   `Canal-JSON`がnil3をサポートしていないために発生する可能性のあるTiCDCパニックの問題を修正し[＃4736](https://github.com/pingcap/tiflow/issues/4736)
        -   UnifiedSorter1で使用されるworkerpoolの安定性の問題を修正し[＃4447](https://github.com/pingcap/tiflow/issues/4447)
        -   シーケンスが誤って複製される場合があるバグを修正します[＃4563](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON`が35を誤って処理したときに発生する可能性がある`string`パニックの問題を修正し[＃4635](https://github.com/pingcap/tiflow/issues/4635)
        -   PDリーダーが殺されたときにTiCDCノードが異常終了するバグを修正します[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合にMySQLシンクが重複した`replace`のSQLステートメントを生成するバグを修正します[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `rename tables`によって引き起こされるDMLコンストラクトエラーを修正し[＃5059](https://github.com/pingcap/tiflow/issues/5059)
        -   所有者が変更され、新しいスケジューラが有効になっている（デフォルトでは無効になっている）場合、まれにレプリケーションがスタックする可能性がある問題を修正します[＃4963](https://github.com/pingcap/tiflow/issues/4963)
        -   新しいスケジューラが有効になっている（デフォルトでは無効になっている）ときにエラーErrProcessorDuplicateOperationsが報告される問題を修正します[＃4769](https://github.com/pingcap/tiflow/issues/4769)
        -   TLSを有効にした後、 `--pd`に設定された最初のPDが使用できない場合にTiCDCが起動しない問題を修正します[＃4777](https://github.com/pingcap/tiflow/issues/4777)
        -   テーブルがスケジュールされているときにチェックポイントメトリックが欠落する問題を修正します[＃4714](https://github.com/pingcap/tiflow/issues/4714)

    -   TiDB Lightning

        -   チェックサムエラー「GCの有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
        -   空のテーブルのチェックに失敗したときにTiDBLightningがスタックする問題を修正します[＃31797](https://github.com/pingcap/tidb/issues/31797)
        -   一部のインポートタスクにソースファイルが含まれていない場合にTiDBLightningがメタデータスキーマを削除しない可能性があるバグを修正します[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   事前チェックでローカルディスクリソースとクラスタの可用性がチェックされない問題を修正します[＃34213](https://github.com/pingcap/tidb/issues/34213)

    -   TiDBデータ移行（DM）

        -   何百もの「チェックポイントに変更がない、同期フラッシュチェックポイントをスキップする」がログに出力され、レプリケーションが非常に遅いという問題を修正します[＃4619](https://github.com/pingcap/tiflow/issues/4619)
        -   [＃4637](https://github.com/pingcap/tiflow/issues/4637)がエラーを報告するバグを修正します`Column length too big`
        -   セーフモードでの更新ステートメントの実行エラーがDMワーカーのパニックを引き起こす可能性がある問題を修正します[＃4317](https://github.com/pingcap/tiflow/issues/4317)
        -   場合によっては、ダウンストリームでフィルター処理されたDDLを手動で実行すると、タスクの再開が失敗する可能性があるという問題を修正します[＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   アップストリーム[＃5121](https://github.com/pingcap/tiflow/issues/5121)でbinlogが有効になっていない場合に、 `query-status`コマンドのデータが返されないバグを修正します。
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの最初に主キーがない場合に発生するDMワーカーのパニックの問題を修正します。
        -   GTIDを有効にした場合、またはタスクが自動的に再開された場合に、CPU使用率が増加し、大量のログが出力される可能性がある問題を修正します[＃5063](https://github.com/pingcap/tiflow/issues/5063)
