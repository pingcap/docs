---
title: TiDB 5.4.1 Release Notes
---

# TiDB 5.4.1 リリースノート {#tidb-5-4-1-release-notes}

リリース日：2022年5月13日

TiDB バージョン: 5.4.1

## 互換性の変更 {#compatibility-changes}

TiDB v5.4.1 では、製品設計に互換性の変更は導入されていません。ただし、このリリースでのバグ修正により、互換性も変更される可能性があることに注意してください。詳細については、 [バグの修正](#bug-fixes)を参照してください。

## 改良点 {#improvements}

-   TiDB

    -   `_tidb_rowid`列[#31543](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリの PointGet プランを使用したサポート
    -   `Apply`オペレーターのログとメトリクスを追加して、並列かどうかを示します[#33887](https://github.com/pingcap/tidb/issues/33887)
    -   `TopN`統計の収集に使用される Analyze バージョン 2 のプルーニング ロジックを改善する[#34256](https://github.com/pingcap/tidb/issues/34256)
    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#32593](https://github.com/pingcap/tidb/issues/32593)

-   TiKV

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#12104](https://github.com/tikv/tikv/issues/12104)

-   PD

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#4673](https://github.com/tikv/pd/issues/4673)

-   TiFlash

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[#4129](https://github.com/pingcap/tiflash/issues/4129)

-   ツール

    -   TiCDC

        -   Grafana ダッシュボードで複数の Kubernetes クラスターをサポートする[#4665](https://github.com/pingcap/tiflow/issues/4665)
        -   Kafka プロデューサーの構成パラメーターを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にする

    -   TiDB データ移行 (DM)

        -   内部ファイルの書き込みに`/tmp`ではなく DM-worker の作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングする Syncer をサポートします[#4107](https://github.com/pingcap/tiflow/issues/4107)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[#32232](https://github.com/pingcap/tidb/issues/32232)
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[#32302](https://github.com/pingcap/tidb/issues/32302)
    -   Merge Join 演算子が特定のケースで間違った結果を取得する問題を修正します[#33042](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[#32089](https://github.com/pingcap/tidb/issues/32089)を返すと、TiDB が間違った結果を取得する問題を修正します。
    -   TiFlashを使用して空の範囲を持つテーブルをスキャンすると、TiDB が間違った結果を取得する問題を修正しますが、 TiFlash はまだ空の範囲を持つテーブルの読み取りをサポートしていません[#33083](https://github.com/pingcap/tidb/issues/33083)
    -   TiDB [#31638](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   クエリがエラーを報告したときに CTE がブロックされる可能性があるバグを修正します[#31302](https://github.com/pingcap/tidb/issues/31302)
    -   Enum 値[#32428](https://github.com/pingcap/tidb/issues/32428)の Nulleq 関数の誤った範囲計算結果を修正
    -   ChunkRPC を使用してデータをエクスポートするときの TiDB OOM を修正[#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    -   `tidb_restricted_read_only`を有効にすると`tidb_super_read_only`が自動的に有効にならない不具合を修正[#31745](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を取得する問題を修正します[#31789](https://github.com/pingcap/tidb/issues/31789)
    -   データがエスケープ文字[#31589](https://github.com/pingcap/tidb/issues/31589)で壊れた場合のロード データpanicを修正
    -   インデックス ルックアップ ジョイン[#30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正します。
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除したときの誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   [#33588](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`特権の付与が失敗する可能性がある問題を修正します。
    -   MySQL バイナリ プロトコル[#33509](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマ変更後にプリペアドステートメントを実行するとセッション パニックが発生するpanicを修正
    -   `tidb_enable_vectorized_expression`が有効な`compress()`式を持つ SQL ステートメントの実行が失敗する問題を修正します[#33397](https://github.com/pingcap/tidb/issues/33397)
    -   `reArrangeFallback`機能でCPU使用率が高くなる問題を修正[#30353](https://github.com/pingcap/tidb/issues/30353)
    -   新しいパーティションが追加されたときにテーブルの属性がインデックス化されない問題と、パーティションが変更されたときにテーブルの範囲情報が更新されない問題を修正します[#33929](https://github.com/pingcap/tidb/issues/33929)
    -   `TopN`初期化中のテーブルの統計情報が正しくソートされないバグを修正[#34216](https://github.com/pingcap/tidb/issues/34216)
    -   識別できないテーブル属性をスキップして`INFORMATION_SCHEMA.ATTRIBUTES`テーブルから読み取るときに発生するエラーを修正します[#33665](https://github.com/pingcap/tidb/issues/33665)
    -   `@@tidb_enable_parallel_apply`が設定されていても、 `order`プロパティが存在する場合に`Apply`演算子が並列化されないバグを修正[#34237](https://github.com/pingcap/tidb/issues/34237)
    -   `sql_mode`を`NO_ZERO_DATE` [#34099](https://github.com/pingcap/tidb/issues/34099)に設定すると`datetime`列に`'0000-00-00 00:00:00'`を挿入できるバグを修正
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると、TiDBサーバーがメモリ不足になることがある問題を修正します。この問題は、Grafana ダッシュボードでスロー クエリを確認すると発生する可能性があります[#33893](https://github.com/pingcap/tidb/issues/33893)
    -   `NOWAIT`ステートメントで、実行中のトランザクションがロックに遭遇したときにすぐに戻らないというバグを修正します[#32754](https://github.com/pingcap/tidb/issues/32754)
    -   `GBK`文字セットで`gbk_bin`照合順序[#31308](https://github.com/pingcap/tidb/issues/31308)テーブルを作成すると失敗するバグを修正
    -   `enable-new-charset`が`on`の場合、照合順序`GBK`文字セットのテーブルを作成すると、「不明な文字セット」エラー[#31297](https://github.com/pingcap/tidb/issues/31297)で失敗するバグを修正します

-   TiKV

    -   マージする対象のリージョンが無効であるため、TiKV が予期せずパニックになり、ピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージが原因で TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリック[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローが原因で発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu [#9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します。
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[#12109](https://github.com/tikv/tikv/issues/12109)
    -   リージョン[#12048](https://github.com/tikv/tikv/issues/12048)のマージ時にターゲット ピアが初期化されずに破棄されたピアに置き換えられると発生する TiKVpanicの問題を修正します。
    -   TiKVが2年以上稼働しているとpanicになることがあるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   ピア ステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除すると発生するpanicの問題を修正します。
    -   ピアを破棄すると高レイテンシーが発生する可能性がある問題を修正します[#10210](https://github.com/tikv/tikv/issues/10210)
    -   リソース メータリング[#12234](https://github.com/tikv/tikv/issues/12234)で無効なアサーションが原因で発生するpanicの問題を修正します。
    -   一部のまれなケースでスロースコア計算が不正確になる問題を修正します[#12254](https://github.com/tikv/tikv/issues/12254)
    -   `resolved_ts`モジュールが原因で発生した OOM の問題を修正し、メトリックを追加します[#12159](https://github.com/tikv/tikv/issues/12159)
    -   ネットワークが貧弱な場合、楽観的トランザクションを正常にコミットしても`Write Conflict`エラーが報告される可能性がある問題を修正します[#34066](https://github.com/pingcap/tidb/issues/34066)
    -   貧弱なネットワークでレプリカ読み取りが有効になっている場合に発生する TiKVpanicの問題を修正します[#12046](https://github.com/tikv/tikv/issues/12046)

-   PD

    -   `dr-autosync`のフィールドのうち`Duration`フィールドを動的に構成できないという問題を修正します[#4651](https://github.com/tikv/pd/issues/4651)
    -   大容量(例えば2T)のストアが存在する場合、満杯に割り当てられた小さなストアが検出されず、バランス演算子が生成されない問題を修正します[#4805](https://github.com/tikv/pd/issues/4805)
    -   ラベル分布がメトリクス[#4825](https://github.com/tikv/pd/issues/4825)に残留ラベルを持つ問題を修正します。

-   TiFlash

    -   TLS が有効になっているときに発生するpanicの問題を修正します[#4196](https://github.com/pingcap/tiflash/issues/4196)
    -   遅れているリージョンピア[#4437](https://github.com/pingcap/tiflash/issues/4437)でのリージョンマージによって発生する可能性のあるメタデータの破損を修正します。
    -   エラーが発生した場合に`JOIN`含むクエリがハングする可能性がある問題を修正します[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正します[#4238](https://github.com/pingcap/tiflash/issues/4238)
    -   `FLOAT`から`DECIMAL` [#3998](https://github.com/pingcap/tiflash/issues/3998)へのキャスト時に発生するオーバーフローを修正
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルすると、タスクが[#4229](https://github.com/pingcap/tiflash/issues/4229)にハングする可能性があるというバグを修正します。
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します。 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストしたときに発生する誤った結果を修正します
    -   `Snapshot`が複数の DDL 操作と同時に適用された場合のTiFlashpanicの潜在的な問題を修正します[#4072](https://github.com/pingcap/tiflash/issues/4072)
    -   無効なstorageディレクトリ構成が予期しない動作を引き起こすバグを修正します[#4093](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が適切に処理されないバグを修正[#4101](https://github.com/pingcap/tiflash/issues/4101)
    -   `INT`から`DECIMAL`をキャストするとオーバーフロー[#3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正
    -   多値式で`IN`の結果が正しくない問題を修正[#4016](https://github.com/pingcap/tiflash/issues/4016)
    -   日付形式が`'\n'`を無効な区切り文字として識別する問題を修正します[#4036](https://github.com/pingcap/tiflash/issues/4036)
    -   重い読み取りワークロードの下で列を追加した後の潜在的なクエリ エラーを修正します[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   メモリ制限が有効になっているときに発生するpanicの問題を修正します[#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   DTFiles [#4778](https://github.com/pingcap/tiflash/issues/4778)の潜在的なデータ破損を修正
    -   削除操作が多いテーブルに対してクエリを実行するときに発生する可能性のあるエラーを修正します[#4747](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多数の &quot;Keepalive watchdog の起動&quot; エラーをランダムに報告するバグを修正[#4192](https://github.com/pingcap/tiflash/issues/4192)
    -   どのリージョン範囲とも一致しないデータがTiFlashノード[#4414](https://github.com/pingcap/tiflash/issues/4414)に残るバグを修正
    -   GC [#4511](https://github.com/pingcap/tiflash/issues/4511)の後で空のセグメントをマージできないバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップの再試行中に暗号化情報が失われると、復元操作が失敗する原因となるバグを修正します[#32423](https://github.com/pingcap/tidb/issues/32423)
        -   BR がRawKV [#32607](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正
        -   増分復元後にテーブルにレコードを挿入するときに重複する主キーを修正する[#33596](https://github.com/pingcap/tidb/issues/33596)
        -   空のクエリを持つ DDL ジョブが原因で、 BR増分復元が誤ってエラーを返すバグを修正します[#33322](https://github.com/pingcap/tidb/issues/33322)
        -   復元操作の完了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[#31034](https://github.com/pingcap/tidb/issues/31034)
        -   復元中にリージョンが一致しない場合、 BR が十分な回数再試行しないという問題を修正します[#33419](https://github.com/pingcap/tidb/issues/33419)
        -   小さなファイルのマージが有効になっていると、 BR が時々panicになることがある問題を修正します[#33801](https://github.com/pingcap/tidb/issues/33801)
        -   BRまたはTiDB Lightning が異常終了した後、スケジューラが再開されない問題を修正します[#33546](https://github.com/pingcap/tidb/issues/33546)

    -   TiCDC

        -   所有者の変更による不正確な指標の修正[#4774](https://github.com/pingcap/tiflow/issues/4774)
        -   `Canal-JSON`が nil [#4736](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性のある TiCDCpanicの問題を修正します。
        -   Unified Sorter [#4447](https://github.com/pingcap/tiflow/issues/4447)が使用するワーカープールの安定性の問題を修正
        -   場合によってはシーケンスが正しく複製されないというバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON` `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)を正しく処理しない場合に発生する可能性のある TiCDCpanicの問題を修正します。
        -   PD リーダーが強制終了されたときに TiCDC ノードが異常終了するバグを修正します[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正します[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   `rename tables` DDL [#5059](https://github.com/pingcap/tiflow/issues/5059)によって引き起こされた DML 構成エラーを修正します。
        -   所有者が変更され、新しいスケジューラが有効になっている場合 (デフォルトでは無効)、 [#4963](https://github.com/pingcap/tiflow/issues/4963)にレプリケーションが停止する問題を修正します。
        -   新しいスケジューラが有効になっている場合 (デフォルトでは無効)、エラー ErrProcessorDuplicateOperations が報告される問題を修正します[#4769](https://github.com/pingcap/tiflow/issues/4769)
        -   TLS が有効になった後、 `--pd`で設定された最初の PD が使用できない場合、TiCDC が開始に失敗する問題を修正します[#4777](https://github.com/pingcap/tiflow/issues/4777)
        -   テーブルがスケジュールされているときにチェックポイント メトリックが欠落している問題を修正します[#4714](https://github.com/pingcap/tiflow/issues/4714)

    -   TiDB Lightning

        -   チェックサム エラー「GC ライフ タイムがトランザクション期間よりも短い」を修正します[#32733](https://github.com/pingcap/tidb/issues/32733)
        -   空のテーブルのチェックに失敗するとTiDB Lightningがスタックする問題を修正[#31797](https://github.com/pingcap/tidb/issues/31797)
        -   一部のインポート タスクにソース ファイルが含まれていない場合、 TiDB Lightning がメタデータ スキーマを削除しないことがあるというバグを修正します[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   事前チェックでローカル ディスク リソースとクラスタの可用性がチェックされない問題を修正します[#34213](https://github.com/pingcap/tidb/issues/34213)

    -   TiDB データ移行 (DM)

        -   何百もの &quot;checkpoint has no change, skip sync flush checkpoint&quot; がログに出力され、レプリケーションが非常に遅いという問題を修正します[#4619](https://github.com/pingcap/tiflow/issues/4619)
        -   長い varchar がエラーを報告するバグを修正`Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        -   セーフモードで update ステートメントの実行エラーが発生すると、DM-workerpanic[#4317](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開に失敗する場合があるという問題を修正します[#5272](https://github.com/pingcap/tiflow/issues/5272)
        -   アップストリームでbinlog が有効になっていない場合に`query-status`コマンドに対してデータが返されないバグを修正[#5121](https://github.com/pingcap/tiflow/issues/5121)
        -   主キーが`SHOW CREATE TABLE`ステートメントによって返されるインデックスの先頭にない場合に発生する DM ワーカーpanicの問題を修正します[#5159](https://github.com/pingcap/tiflow/issues/5159)
        -   GTID有効時やタスク自動再開時にCPU使用率が上昇し、大量のログが出力されることがある問題を修正[#5063](https://github.com/pingcap/tiflow/issues/5063)
