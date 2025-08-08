---
title: TiDB 5.4.1 Release Notes
summary: TiDB 5.4.1 リリースノート: このリリースには、TiDB、TiKV、PD、 TiFlash、およびさまざまなツールの互換性の変更、改善、バグ修正が含まれています。改善点には、PointGet プランの使用のサポート、ログとメトリックの追加、Grafana ダッシュボードでの複数の Kubernetes クラスターの表示が含まれます。バグ修正では、date_format の不適切な処理、データの書き込みエラー、クエリ結果の誤り、さまざまなパニックやエラーなどの問題に対処しています。TiKV、PD、 TiFlash、およびツールの修正も含まれています。
---

# TiDB 5.4.1 リリースノート {#tidb-5-4-1-release-notes}

リリース日：2022年5月13日

TiDB バージョン: 5.4.1

## 互換性の変更 {#compatibility-changes}

TiDB v5.4.1では、製品設計上の互換性に関する変更は行われていません。ただし、このリリースでのバグ修正により、互換性に関する変更も発生する可能性がありますのでご注意ください。詳細については、 [バグ修正](#bug-fixes)ご覧ください。

## 改善点 {#improvements}

-   TiDB

    -   `_tidb_rowid`列[＃31543](https://github.com/pingcap/tidb/issues/31543)列を読み取るクエリにPointGetプランの使用をサポート
    -   `Apply`オペレータのログとメトリクスを追加して、並列[＃33887](https://github.com/pingcap/tidb/issues/33887)であるかどうかを確認します。
    -   統計情報[＃34256](https://github.com/pingcap/tidb/issues/34256)を収集するために使用される分析バージョン 2 の`TopN`プルーニング ロジックを改善します。
    -   Grafanaダッシュボード[＃32593](https://github.com/pingcap/tidb/issues/32593)で複数のKubernetesクラスターの表示をサポート

-   TiKV

    -   Grafanaダッシュボード[＃12104](https://github.com/tikv/tikv/issues/12104)で複数のKubernetesクラスターの表示をサポート

-   PD

    -   Grafanaダッシュボード[＃4673](https://github.com/tikv/pd/issues/4673)で複数のKubernetesクラスターの表示をサポート

-   TiFlash

    -   Grafanaダッシュボード[＃4129](https://github.com/pingcap/tiflash/issues/4129)で複数のKubernetesクラスターの表示をサポート

-   ツール

    -   TiCDC

        -   Grafanaダッシュボードで複数のKubernetesクラスターをサポート[＃4665](https://github.com/pingcap/tiflow/issues/4665)
        -   Kafka プロデューサーの設定パラメータを公開して、TiCDC [＃4385](https://github.com/pingcap/tiflow/issues/4385)で設定できるようにします。

    -   TiDB データ移行 (DM)

        -   `/tmp`ではなく DM ワーカーの作業ディレクトリを使用して内部ファイルを書き込み、タスクが停止した後にディレクトリを消去する Syncer のサポート[＃4107](https://github.com/pingcap/tiflow/issues/4107)

## バグ修正 {#bug-fixes}

-   TiDB

    -   TiDBの`date_format`が`'\n'` MySQLと互換性のない方法で処理する問題を修正[＃32232](https://github.com/pingcap/tidb/issues/32232)
    -   `ENUM` [＃32302](https://github.com/pingcap/tidb/issues/32302)または`SET`列目のエンコードが間違っているためにTiDBが間違ったデータを書き込む問題を修正しました。
    -   特定のケースで Merge Join 演算子が間違った結果を返す問題を修正[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[＃32089](https://github.com/pingcap/tidb/issues/32089)返すときにTiDBが間違った結果を取得する問題を修正しました
    -   TiFlash が空の範囲を持つテーブルの読み取りをまだサポートしていないにもかかわらず、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると TiDB が間違った結果を取得する問題を修正しました[＃33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiDB [＃31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっているときに、 `ENUM`または`SET`列目の`MAX`または`MIN`関数が間違った結果を返す問題を修正しました。
    -   クエリがエラーを報告したときに CTE がブロックされる可能性があるバグを修正[＃31302](https://github.com/pingcap/tidb/issues/31302)
    -   列挙値[＃32428](https://github.com/pingcap/tidb/issues/32428)の Nulleq 関数の誤った範囲計算結果を修正しました
    -   ChunkRPC [＃31981](https://github.com/pingcap/tidb/issues/31981) [＃30880](https://github.com/pingcap/tidb/issues/30880)を使用してデータをエクスポートする際の TiDB OOM を修正
    -   `tidb_restricted_read_only`有効になっているときに`tidb_super_read_only`自動的に有効にならないバグを修正[＃31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序`greatest`または`least`関数が間違った結果を返す問題を修正しました[＃31789](https://github.com/pingcap/tidb/issues/31789)
    -   データがエスケープ文字[＃31589](https://github.com/pingcap/tidb/issues/31589)で壊れている場合のロードデータpanicを修正
    -   インデックスルックアップ結合[＃30468](https://github.com/pingcap/tidb/issues/30468)使用してクエリを実行するときに発生する`invalid transaction`エラーを修正します
    -   `left join` [＃31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDBが重複したタスクをTiFlash [＃32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正しました
    -   v4.0 [＃33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`権限の付与が失敗する可能性がある問題を修正しました
    -   MySQLバイナリプロトコル[＃33509](https://github.com/pingcap/tidb/issues/33509)でテーブルスキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正しました
    -   `tidb_enable_vectorized_expression`有効になっている`compress()`式を持つ SQL 文を実行すると失敗する問題を修正しました[＃33397](https://github.com/pingcap/tidb/issues/33397)
    -   `reArrangeFallback`機能[＃30353](https://github.com/pingcap/tidb/issues/30353)によるCPU使用率の高騰の問題を修正
    -   新しいパーティションが追加されたときにテーブル属性がインデックスされない問題と、パーティションが変更されたときにテーブル範囲情報が更新されない問題を修正しました[＃33929](https://github.com/pingcap/tidb/issues/33929)
    -   初期化中のテーブルの`TopN`情報が正しくソートされないバグを修正しました[＃34216](https://github.com/pingcap/tidb/issues/34216)
    -   識別できないテーブル属性[＃33665](https://github.com/pingcap/tidb/issues/33665)をスキップして、テーブル`INFORMATION_SCHEMA.ATTRIBUTES`からの読み取り時に発生するエラーを修正します
    -   `@@tidb_enable_parallel_apply`が設定されていても、 `order`プロパティが存在する場合に`Apply`演算子が並列化されないバグを修正[＃34237](https://github.com/pingcap/tidb/issues/34237)
    -   `sql_mode` `NO_ZERO_DATE` [＃34099](https://github.com/pingcap/tidb/issues/34099)に設定すると`datetime`列に`'0000-00-00 00:00:00'`が挿入されるバグを修正しました
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルへのクエリ実行時に TiDBサーバーのメモリが発生する問題を修正しました。この問題は、Grafana ダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)でスロークエリをチェックすると発生する可能性があります。
    -   `NOWAIT`文で実行中のトランザクションがロック[＃32754](https://github.com/pingcap/tidb/issues/32754)に遭遇してもすぐには戻らないバグを修正
    -   `GBK`文字セットと`gbk_bin`照合順序[＃31308](https://github.com/pingcap/tidb/issues/31308)でテーブルを作成するときに失敗するバグを修正しました
    -   `enable-new-charset`が`on`の場合、照合順序付きの`GBK`文字セットテーブルの作成が「不明な文字セット」エラーで失敗するバグを修正しました[＃31297](https://github.com/pingcap/tidb/issues/31297)

-   TiKV

    -   マージ対象のリージョンが無効であるため、TiKV がパニックを起こしてピアを予期せず破棄する問題を修正[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージによって TiKV がpanicを起こすバグを修正[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリックのオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足（OOM）の問題を修正しました[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   Ubuntu 18.04 [＃9765](https://github.com/tikv/tikv/issues/9765)でTiKVがプロファイリングを実行するときに発生する可能性のあるpanic問題を修正しました
    -   レプリカ読み取りが線形化可能性[＃12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正しました
    -   リージョン[＃12048](https://github.com/tikv/tikv/issues/12048)をマージする際に、ターゲットピアが初期化されずに破棄されたピアに置き換えられたときに発生するTiKVpanic問題を修正しました。
    -   TiKV が 2 年以上実行されている場合にpanic可能性があるバグを修正[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   解決ロックのステップ[＃11993](https://github.com/tikv/tikv/issues/11993)必要とする領域の数を減らすことで、TiCDC の回復時間を短縮します。
    -   ピアステータスが`Applying` [＃11746](https://github.com/tikv/tikv/issues/11746)ときにスナップショットファイルを削除すると発生するpanic問題を修正しました
    -   ピアを破棄するとレイテンシーが大きくなる可能性がある問題を修正[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   リソースメータリング[＃12234](https://github.com/tikv/tikv/issues/12234)無効なアサーションによって発生するpanic問題を修正
    -   一部のコーナーケースで遅いスコア計算が不正確になる問題を修正[＃12254](https://github.com/tikv/tikv/issues/12254)
    -   `resolved_ts`モジュールによって引き起こされたOOM問題を修正し、さらにメトリック[＃12159](https://github.com/tikv/tikv/issues/12159)を追加します
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正しました[＃34066](https://github.com/pingcap/tidb/issues/34066)
    -   低品質のネットワークでレプリカ読み取りが有効になっている場合に発生する TiKVpanic問題を修正[＃12046](https://github.com/tikv/tikv/issues/12046)

-   PD

    -   `dr-autosync`の`Duration`フィールドが動的に構成できない問題を修正[＃4651](https://github.com/tikv/pd/issues/4651)
    -   大容量（例えば2T）のストアが存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されない問題を修正しました[＃4805](https://github.com/tikv/pd/issues/4805)
    -   ラベル分布にメトリクス[＃4825](https://github.com/tikv/pd/issues/4825)の残余ラベルがある問題を修正

-   TiFlash

    -   TLS が有効になっているときに発生するpanic問題を修正[＃4196](https://github.com/pingcap/tiflash/issues/4196)
    -   遅延リージョンピア[＃4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンマージによって発生する可能性のあるメタデータ破損を修正しました
    -   エラーが発生した場合に`JOIN`を含むクエリがハングする可能性がある問題を修正しました[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[＃4238](https://github.com/pingcap/tiflash/issues/4238)
    -   `FLOAT`を`DECIMAL` [＃3998](https://github.com/pingcap/tiflash/issues/3998)にキャストするときに発生するオーバーフローを修正
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   ローカルトンネルが有効な場合、キャンセルされた MPP クエリによってタスクが永久にハングする可能性があるバグを修正しました[＃4229](https://github.com/pingcap/tiflash/issues/4229)
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正しました[＃4098](https://github.com/pingcap/tiflash/issues/4098)
    -   `DATETIME`を`DECIMAL` [＃4151](https://github.com/pingcap/tiflash/issues/4151)にキャストするときに発生する誤った結果を修正
    -   `Snapshot`複数の DDL 操作[＃4072](https://github.com/pingcap/tiflash/issues/4072)と同時に適用された場合にTiFlashpanicが発生する可能性がある問題を修正しました
    -   無効なstorageディレクトリ設定が予期しない動作を引き起こすバグを修正[＃4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないバグを修正[＃4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `INT`を`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正しました[＃3920](https://github.com/pingcap/tiflash/issues/3920)
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式が`'\n'`無効な区切り文字として認識する問題を修正[＃4036](https://github.com/pingcap/tiflash/issues/4036)
    -   読み取り負荷が高い状態で列を追加した後に発生する可能性のあるクエリエラーを修正[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   メモリ制限が有効になっているときに発生するpanic問題を修正[＃3902](https://github.com/pingcap/tiflash/issues/3902)
    -   DTFiles [＃4778](https://github.com/pingcap/tiflash/issues/4778)の潜在的なデータ破損を修正
    -   削除操作を多数含むテーブルをクエリするときに発生する可能性のあるエラーを修正[＃4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが「Keepalive watchdog fired」エラーをランダムに多数報告するバグを修正[＃4192](https://github.com/pingcap/tiflash/issues/4192)
    -   どの領域範囲にも一致しないデータがTiFlashノード[＃4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正しました
    -   GC [＃4511](https://github.com/pingcap/tiflash/issues/4511)以降に空のセグメントを結合できないバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正[＃32423](https://github.com/pingcap/tidb/issues/32423)
        -   BRがRawKV [＃32607](https://github.com/pingcap/tidb/issues/32607)バックアップに失敗する問題を修正
        -   増分復元後にテーブルにレコードを挿入するときに重複する主キーを修正する[＃33596](https://github.com/pingcap/tidb/issues/33596)
        -   BR増分リストアが空のクエリ[＃33322](https://github.com/pingcap/tidb/issues/33322)を含むDDLジョブにより誤ってエラーを返すバグを修正しました
        -   復元操作が完了した後にリージョンが不均等に分散される可能性がある問題を修正しました[＃31034](https://github.com/pingcap/tidb/issues/31034)
        -   復元中にリージョンが一致していない場合にBRが十分な回数再試行しない問題を修正[＃33419](https://github.com/pingcap/tidb/issues/33419)
        -   小さなファイルのマージが有効になっているときにBRが時々panic可能性がある問題を修正[＃33801](https://github.com/pingcap/tidb/issues/33801)
        -   BRまたはTiDB Lightningが異常終了した後にスケジューラが再開しない問題を修正[＃33546](https://github.com/pingcap/tidb/issues/33546)

    -   TiCDC

        -   所有者の変更によって生じた誤ったメトリクスを修正[＃4774](https://github.com/pingcap/tiflow/issues/4774)
        -   `Canal-JSON` nil [＃4736](https://github.com/pingcap/tiflow/issues/4736)サポートしていないために発生する可能性がある TiCDCpanic問題を修正しました
        -   Unified Sorter [＃4447](https://github.com/pingcap/tiflow/issues/4447)で使用されるワーカープールの安定性の問題を修正しました
        -   一部のケースでシーケンスが誤って複製されるバグを修正[＃4552](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON` `string` [＃4635](https://github.com/pingcap/tiflow/issues/4635)を誤って処理した場合に発生する可能性のある TiCDCpanic問題を修正しました
        -   PDリーダーが強制終了した際にTiCDCノードが異常終了するバグを修正[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   MySQLシンクが`batch-replace-enable`無効になっているときに重複した`replace` SQL文を生成するバグを修正[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `rename tables` DDL [＃5059](https://github.com/pingcap/tiflow/issues/5059)によって発生した DML 構造エラーを修正
        -   所有者が変更され、新しいスケジューラが有効になっている場合（デフォルトでは無効）に、まれにレプリケーションが停止する可能性がある問題を修正しました[＃4963](https://github.com/pingcap/tiflow/issues/4963)
        -   新しいスケジューラが有効になっているときにエラー ErrProcessorDuplicateOperations が報告される問題を修正しました (デフォルトでは無効) [＃4769](https://github.com/pingcap/tiflow/issues/4769)
        -   TLS が有効になった後、 `--pd`で設定された最初の PD が利用できない場合に TiCDC が起動に失敗する問題を修正[＃4777](https://github.com/pingcap/tiflow/issues/4777)
        -   テーブルがスケジュールされているときにチェックポイントメトリックが欠落する問題を修正しました[＃4714](https://github.com/pingcap/tiflow/issues/4714)

    -   TiDB Lightning

        -   チェックサムエラー「GCの有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
        -   空のテーブル[＃31797](https://github.com/pingcap/tidb/issues/31797)チェックに失敗した場合、 TiDB Lightning が停止する問題を修正しました。
        -   一部のインポートタスクにソースファイルが含まれていない場合にTiDB Lightningがメタデータスキーマを削除しない可能性があるバグを修正しました[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   事前チェックでローカルディスクリソースとクラスターの可用性がチェックされない問題を修正[＃34213](https://github.com/pingcap/tidb/issues/34213)

    -   TiDB データ移行 (DM)

        -   ログに「チェックポイントに変更はありません。同期フラッシュチェックポイントをスキップしてください」というメッセージが数百件出力され、レプリケーションが非常に遅くなる問題を修正しました[＃4619](https://github.com/pingcap/tiflow/issues/4619)
        -   長いvarcharsがエラーを報告するバグを修正`Column length too big` [＃4637](https://github.com/pingcap/tiflow/issues/4637)
        -   セーフモードでの更新ステートメントの実行エラーにより、DMワーカーがpanicになる可能性がある問題を修正しました[＃4317](https://github.com/pingcap/tiflow/issues/4317)
        -   下流でフィルタリングされたDDLを手動で実行すると、タスク再開が失敗する場合がある問題を修正しました[＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   アップストリーム[＃5121](https://github.com/pingcap/tiflow/issues/5121)でbinlogが有効になっていない場合に`query-status`コマンドでデータが返されないバグを修正
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーpanicの問題を修正しました。
        -   GTID が有効になっているときやタスクが自動的に再開されたときに CPU 使用率が上昇し、大量のログが出力される問題を修正しました[＃5063](https://github.com/pingcap/tiflow/issues/5063)
