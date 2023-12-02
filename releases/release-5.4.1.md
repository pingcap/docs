---
title: TiDB 5.4.1 Release Notes
---

# TiDB 5.4.1 リリースノート {#tidb-5-4-1-release-notes}

リリース日：2022年5月13日

TiDB バージョン: 5.4.1

## 互換性の変更 {#compatibility-changes}

TiDB v5.4.1 では、製品設計に互換性の変更は導入されていません。ただし、このリリースのバグ修正により、互換性も変更される可能性があることに注意してください。詳細については、 [バグの修正](#bug-fixes)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   `_tidb_rowid`列[#31543](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリに対する PointGet プランの使用のサポート
    -   `Apply`オペレーターのログとメトリックを追加して、並列[#33887](https://github.com/pingcap/tidb/issues/33887)かどうかを示します。
    -   統計の収集に使用される Analyze バージョン 2 の`TopN`プルーニング ロジックを改善[#34256](https://github.com/pingcap/tidb/issues/34256)
    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#32593](https://github.com/pingcap/tidb/issues/32593)

-   TiKV

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#12104](https://github.com/tikv/tikv/issues/12104)

-   PD

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#4673](https://github.com/tikv/pd/issues/4673)

-   TiFlash

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#4129](https://github.com/pingcap/tiflash/issues/4129)

-   ツール

    -   TiCDC

        -   Grafana ダッシュボードで複数の Kubernetes クラスターをサポート[#4665](https://github.com/pingcap/tiflow/issues/4665)
        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。

    -   TiDB データ移行 (DM)

        -   Syncer は内部ファイルの書き込みに`/tmp`ではなく DM ワーカーの作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングすることをサポートします[#4107](https://github.com/pingcap/tiflow/issues/4107)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[#32232](https://github.com/pingcap/tidb/issues/32232)
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[#32302](https://github.com/pingcap/tidb/issues/32302)
    -   特定の場合に Merge Join 演算子が間違った結果を取得する問題を修正します[#33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[#32089](https://github.com/pingcap/tidb/issues/32089)を返すと TiDB が間違った結果を取得する問題を修正
    -   TiFlash は空の範囲を持つテーブルの読み取りをサポートしていませんが、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、 TiFlashが間違った結果を取得する問題を修正します[#33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiDB [#31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   クエリがエラーを報告すると CTE がブロックされる可能性があるバグを修正[#31302](https://github.com/pingcap/tidb/issues/31302)
    -   Enum 値[#32428](https://github.com/pingcap/tidb/issues/32428)に対する Nulleq 関数の間違った範囲計算結果を修正しました。
    -   ChunkRPC を使用してデータをエクスポートするときの TiDB OOM を修正[#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    -   `tidb_restricted_read_only`を有効にすると`tidb_super_read_only`が自動的に有効にならないバグを修正[#31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序のある`greatest`または`least`関数が間違った結果を取得する問題を修正[#31789](https://github.com/pingcap/tidb/issues/31789)
    -   エスケープ文字[#31589](https://github.com/pingcap/tidb/issues/31589)でデータが壊れた場合のロード データpanicを修正
    -   インデックス検索結合[#30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正しました。
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   v4.0 [#33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`権限の付与が失敗する場合がある問題を修正
    -   MySQL バイナリ プロトコル[#33509](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正しました。
    -   `compress()`式と`tidb_enable_vectorized_expression`を有効にした SQL ステートメントの実行が失敗する問題を修正します[#33397](https://github.com/pingcap/tidb/issues/33397)
    -   `reArrangeFallback`機能[#30353](https://github.com/pingcap/tidb/issues/30353)による CPU 使用率が高くなる問題を修正
    -   新しいパーティションの追加時にテーブル属性のインデックスが作成されない問題と、パーティションの変更時にテーブル範囲情報が更新されない問題を修正します[#33929](https://github.com/pingcap/tidb/issues/33929)
    -   `TopN`初期化時のテーブルの統計情報が正しくソートされないバグを修正[#34216](https://github.com/pingcap/tidb/issues/34216)
    -   識別できないテーブル属性[#33665](https://github.com/pingcap/tidb/issues/33665)をスキップして、 `INFORMATION_SCHEMA.ATTRIBUTES`テーブルから読み取るときに発生するエラーを修正しました。
    -   `order`プロパティが存在する場合、 `@@tidb_enable_parallel_apply`設定しても`Apply`演算子が並列化されないバグを修正[#34237](https://github.com/pingcap/tidb/issues/34237)
    -   `sql_mode`を`NO_ZERO_DATE` [#34099](https://github.com/pingcap/tidb/issues/34099)に設定した場合、 `datetime`列に`'0000-00-00 00:00:00'`挿入できるバグを修正
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[#33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックすると発生する可能性があります。
    -   `NOWAIT`ステートメントで、ロック[#32754](https://github.com/pingcap/tidb/issues/32754)が発生したときに実行中のトランザクションがすぐに返されないバグを修正しました。
    -   `GBK`文字セットと`gbk_bin`照合順序[#31308](https://github.com/pingcap/tidb/issues/31308)を使用してテーブルを作成するときに失敗するバグを修正しました。
    -   `enable-new-charset`が`on`の場合、照合順序`GBK`文字セットのテーブルを作成すると、「不明な文字セット」エラー[#31297](https://github.com/pingcap/tidb/issues/31297)が発生して失敗するバグを修正しました。

-   TiKV

    -   マージ対象のターゲットリージョンが無効であるため、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージによって TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリクス[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[#9765](https://github.com/tikv/tikv/issues/9765)
    -   レプリカの読み取りが線形化可能性[#12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   ピアのステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[#10210](https://github.com/tikv/tikv/issues/10210)
    -   リソース メータリング[#12234](https://github.com/tikv/tikv/issues/12234)の無効なアサーションによって引き起こされるpanicの問題を修正
    -   一部の特殊なケースで遅いスコア計算が不正確になる問題を修正[#12254](https://github.com/tikv/tikv/issues/12254)
    -   `resolved_ts`モジュールによって引き起こされる OOM 問題を修正し、さらにメトリクスを追加します[#12159](https://github.com/tikv/tikv/issues/12159)
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[#34066](https://github.com/pingcap/tidb/issues/34066)
    -   貧弱なネットワークでレプリカ読み取りが有効になっている場合に発生する TiKVpanicの問題を修正します[#12046](https://github.com/tikv/tikv/issues/12046)

-   PD

    -   `dr-autosync`の`Duration`フィールドを動的に設定できない問題を修正[#4651](https://github.com/tikv/pd/issues/4651)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアを検出できず、バランス演算子が生成されない問題を修正します[#4805](https://github.com/tikv/pd/issues/4805)
    -   ラベル分布のメトリクスに残留ラベルがある問題を修正します[#4825](https://github.com/tikv/pd/issues/4825)

-   TiFlash

    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   遅れているリージョンピア[#4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンのマージによって発生する可能性のあるメタデータの破損を修正します。
    -   `JOIN`を含むクエリでエラーが発生した場合にハングする可能性がある問題を修正[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   `FLOAT` ～ `DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   期限切れデータのリサイクルが遅い問題を修正[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルするとタスクが永久にハングする可能性があるバグを修正します[#4229](https://github.com/pingcap/tiflash/issues/4229)
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します[#4098](https://github.com/pingcap/tiflash/issues/4098)
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   `Snapshot`が複数の DDL 操作と同時に適用される場合のTiFlashpanicの潜在的な問題を修正します[#4072](https://github.com/pingcap/tiflash/issues/4072)
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `INT`から`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正[#3920](https://github.com/pingcap/tiflash/issues/3920)
    -   複数値式[#4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式で`'\n'`無効な区切り文字[#4036](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   メモリ制限が有効になっているときに発生するpanicの問題を修正します[#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   DTFiles [#4778](https://github.com/pingcap/tiflash/issues/4778)の潜在的なデータ破損を修正
    -   多くの削除操作を含むテーブルに対してクエリを実行する際の潜在的なエラーを修正します[#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多数の「Keepalive watchdog fired」エラーをランダムに報告するバグを修正[#4192](https://github.com/pingcap/tiflash/issues/4192)
    -   TiFlashノード[#4414](https://github.com/pingcap/tiflash/issues/4414)にどのリージョン範囲にも一致しないデータが残るバグを修正
    -   GC [#4511](https://github.com/pingcap/tiflash/issues/4511)以降に空のセグメントをマージできないバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップの再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正しました[#32423](https://github.com/pingcap/tidb/issues/32423)
        -   BR がRawKV [#32607](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正
        -   増分復元[#33596](https://github.com/pingcap/tidb/issues/33596)後にテーブルにレコードを挿入するときの重複した主キーを修正します。
        -   空のクエリ[#33322](https://github.com/pingcap/tidb/issues/33322)を含む DDL ジョブによりBR増分リストアが誤ってエラーを返すバグを修正
        -   復元操作の完了後にリージョンが不均等に分散される可能性がある潜在的な問題を修正します[#31034](https://github.com/pingcap/tidb/issues/31034)
        -   復元中にリージョンに一貫性がない場合、 BR が十分な回数再試行しない問題を修正[#33419](https://github.com/pingcap/tidb/issues/33419)
        -   小さなファイルのマージが有効になっているときにBR が時折panicする問題を修正します[#33801](https://github.com/pingcap/tidb/issues/33801)
        -   BRまたはTiDB Lightningが異常終了した後にスケジューラが再開しない問題を修正[#33546](https://github.com/pingcap/tidb/issues/33546)

    -   TiCDC

        -   所有者の変更によって引き起こされた誤ったメトリクスを修正する[#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   `Canal-JSON`が nil [#4736](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性がある TiCDCpanic問題を修正
        -   Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)によって使用されるワーカープールの安定性の問題を修正しました。
        -   場合によってはシーケンスが不正に複製されるバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON` `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)を誤って処理した場合に発生する可能性がある TiCDCpanicの問題を修正
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `rename tables` DDL [#5059](https://github.com/pingcap/tiflow/issues/5059)によって引き起こされる DML 構築エラーを修正
        -   所有者が変更され、新しいスケジューラーが有効になっている場合 (デフォルトでは無効になっている)、 [#4963](https://github.com/pingcap/tiflow/issues/4963)にレプリケーションが停止する可能性がある問題を修正します。
        -   新しいスケジューラーが有効になっている場合 (デフォルトでは無効になっています)、エラー ErrProcessorDuplicateOperations が報告される問題を修正します[#4769](https://github.com/pingcap/tiflow/issues/4769)
        -   TLS を有効にした後、 `--pd`で設定した最初の PD が利用できない場合に TiCDC の起動に失敗する問題を修正[#4777](https://github.com/pingcap/tiflow/issues/4777)
        -   テーブルがスケジュールされているときにチェックポイント メトリックが欠落する問題を修正します[#4714](https://github.com/pingcap/tiflow/issues/4714)

    -   TiDB Lightning

        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」 [#32733](https://github.com/pingcap/tidb/issues/32733)を修正
        -   TiDB Lightning が空のテーブルのチェックに失敗するとスタックする問題を修正[#31797](https://github.com/pingcap/tidb/issues/31797)
        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   事前チェックでローカル ディスク リソースとクラスターの可用性がチェックされない問題を修正します[#34213](https://github.com/pingcap/tidb/issues/34213)

    -   TiDB データ移行 (DM)

        -   ログに何百もの「チェックポイントに変更はありません。同期フラッシュ チェックポイントをスキップします」と出力され、レプリケーションが非常に遅くなる問題を修正します[#4619](https://github.com/pingcap/tiflow/issues/4619)
        -   long varchar がエラーを報告するバグを修正`Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        -   セーフモードでの更新ステートメントの実行エラーにより DM ワーカーpanic[#4317](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   場合によっては、フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開が失敗する可能性がある問題を修正します[#5272](https://github.com/pingcap/tiflow/issues/5272)
        -   アップストリーム[#5121](https://github.com/pingcap/tiflow/issues/5121)でbinlogが有効になっていない場合、 `query-status`コマンドに対してデータが返されないバグを修正
        -   `SHOW CREATE TABLE`ステートメント[#5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーのpanic問題を修正します。
        -   GTID が有効になっている場合、またはタスクが自動的に再開された場合に、CPU 使用率が増加し、大量のログが出力される場合がある問題を修正します[#5063](https://github.com/pingcap/tiflow/issues/5063)
