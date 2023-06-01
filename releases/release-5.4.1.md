---
title: TiDB 5.4.1 Release Notes
---

# TiDB 5.4.1 リリースノート {#tidb-5-4-1-release-notes}

リリース日：2022年5月13日

TiDB バージョン: 5.4.1

## 互換性の変更 {#compatibility-changes}

TiDB v5.4.1 では、製品設計に互換性の変更は導入されていません。ただし、このリリースのバグ修正により、互換性も変更される可能性があることに注意してください。詳細については、 [<a href="#bug-fixes">バグの修正</a>](#bug-fixes)を参照してください。

## 改善点 {#improvements}

-   TiDB

    -   `_tidb_rowid`列[<a href="https://github.com/pingcap/tidb/issues/31543">#31543</a>](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリに対する PointGet プランの使用のサポート
    -   `Apply`オペレーターのログとメトリックを追加して、並列[<a href="https://github.com/pingcap/tidb/issues/33887">#33887</a>](https://github.com/pingcap/tidb/issues/33887)かどうかを示します。
    -   統計の収集に使用される Analyze バージョン 2 の`TopN`プルーニング ロジックを改善[<a href="https://github.com/pingcap/tidb/issues/34256">#34256</a>](https://github.com/pingcap/tidb/issues/34256)
    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[<a href="https://github.com/pingcap/tidb/issues/32593">#32593</a>](https://github.com/pingcap/tidb/issues/32593)

-   TiKV

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[<a href="https://github.com/tikv/tikv/issues/12104">#12104</a>](https://github.com/tikv/tikv/issues/12104)

-   PD

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[<a href="https://github.com/tikv/pd/issues/4673">#4673</a>](https://github.com/tikv/pd/issues/4673)

-   TiFlash

    -   Grafana ダッシュボードでの複数の Kubernetes クラスターの表示のサポート[<a href="https://github.com/pingcap/tiflash/issues/4129">#4129</a>](https://github.com/pingcap/tiflash/issues/4129)

-   ツール

    -   TiCDC

        -   Grafana ダッシュボードで複数の Kubernetes クラスターをサポート[<a href="https://github.com/pingcap/tiflow/issues/4665">#4665</a>](https://github.com/pingcap/tiflow/issues/4665)
        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [<a href="https://github.com/pingcap/tiflow/issues/4385">#4385</a>](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。

    -   TiDB データ移行 (DM)

        -   Syncer は内部ファイルの書き込みに`/tmp`ではなく DM ワーカーの作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングすることをサポートします[<a href="https://github.com/pingcap/tiflow/issues/4107">#4107</a>](https://github.com/pingcap/tiflow/issues/4107)

## バグの修正 {#bug-fixes}

-   TiDB

    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32232">#32232</a>](https://github.com/pingcap/tidb/issues/32232)
    -   `ENUM`列または`SET`列のエンコーディングが間違っているため、TiDB が間違ったデータを書き込む問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32302">#32302</a>](https://github.com/pingcap/tidb/issues/32302)
    -   特定の場合に Merge Join 演算子が間違った結果を取得する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33042">#33042</a>](https://github.com/pingcap/tidb/issues/33042)
    -   相関サブクエリが定数[<a href="https://github.com/pingcap/tidb/issues/32089">#32089</a>](https://github.com/pingcap/tidb/issues/32089)を返すと TiDB が間違った結果を取得する問題を修正
    -   TiFlash は空の範囲を持つテーブルの読み取りをまだサポートしていませんが、 TiFlashを使用して空の範囲を持つテーブルをスキャンすると、 TiFlashが間違った結果を取得する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33083">#33083</a>](https://github.com/pingcap/tidb/issues/33083)
    -   TiDB [<a href="https://github.com/pingcap/tidb/issues/31638">#31638</a>](https://github.com/pingcap/tidb/issues/31638)で新しい照合順序が有効になっている場合、 `ENUM`または`SET`列の`MAX`または`MIN`関数が間違った結果を返す問題を修正します。
    -   クエリがエラーを報告すると CTE がブロックされる可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/31302">#31302</a>](https://github.com/pingcap/tidb/issues/31302)
    -   Enum 値[<a href="https://github.com/pingcap/tidb/issues/32428">#32428</a>](https://github.com/pingcap/tidb/issues/32428)に対する Nulleq 関数の間違った範囲計算結果を修正しました。
    -   ChunkRPC を使用してデータをエクスポートするときの TiDB OOM を修正[<a href="https://github.com/pingcap/tidb/issues/31981">#31981</a>](https://github.com/pingcap/tidb/issues/31981) [<a href="https://github.com/pingcap/tidb/issues/30880">#30880</a>](https://github.com/pingcap/tidb/issues/30880)
    -   `tidb_restricted_read_only`を有効にすると`tidb_super_read_only`が自動的に有効にならないバグを修正[<a href="https://github.com/pingcap/tidb/issues/31745">#31745</a>](https://github.com/pingcap/tidb/issues/31745)
    -   照合順序のある`greatest`または`least`関数が間違った結果を取得する問題を修正[<a href="https://github.com/pingcap/tidb/issues/31789">#31789</a>](https://github.com/pingcap/tidb/issues/31789)
    -   エスケープ文字[<a href="https://github.com/pingcap/tidb/issues/31589">#31589</a>](https://github.com/pingcap/tidb/issues/31589)でデータが壊れた場合のロード データpanicを修正
    -   インデックス検索結合[<a href="https://github.com/pingcap/tidb/issues/30468">#30468</a>](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正しました。
    -   `left join` [<a href="https://github.com/pingcap/tidb/issues/31321">#31321</a>](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [<a href="https://github.com/pingcap/tidb/issues/32814">#32814</a>](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   v4.0 [<a href="https://github.com/pingcap/tidb/issues/33588">#33588</a>](https://github.com/pingcap/tidb/issues/33588)からアップグレードされたクラスターで`all`権限の付与が失敗する場合がある問題を修正
    -   MySQL バイナリ プロトコル[<a href="https://github.com/pingcap/tidb/issues/33509">#33509</a>](https://github.com/pingcap/tidb/issues/33509)でテーブル スキーマを変更した後にプリペアドステートメントを実行するときに発生するセッションpanicを修正しました。
    -   `compress()`式と`tidb_enable_vectorized_expression`を有効にした SQL ステートメントの実行が失敗する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33397">#33397</a>](https://github.com/pingcap/tidb/issues/33397)
    -   `reArrangeFallback`機能[<a href="https://github.com/pingcap/tidb/issues/30353">#30353</a>](https://github.com/pingcap/tidb/issues/30353)による CPU 使用率が高くなる問題を修正
    -   新しいパーティションの追加時にテーブル属性のインデックスが作成されない問題と、パーティションの変更時にテーブル範囲情報が更新されない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33929">#33929</a>](https://github.com/pingcap/tidb/issues/33929)
    -   `TopN`初期化時のテーブルの統計情報が正しくソートされないバグを修正[<a href="https://github.com/pingcap/tidb/issues/34216">#34216</a>](https://github.com/pingcap/tidb/issues/34216)
    -   識別できないテーブル属性[<a href="https://github.com/pingcap/tidb/issues/33665">#33665</a>](https://github.com/pingcap/tidb/issues/33665)をスキップして、 `INFORMATION_SCHEMA.ATTRIBUTES`テーブルから読み取るときに発生するエラーを修正しました。
    -   `order`プロパティが存在する場合、 `@@tidb_enable_parallel_apply`設定しても`Apply`演算子が並列化されないバグを修正[<a href="https://github.com/pingcap/tidb/issues/34237">#34237</a>](https://github.com/pingcap/tidb/issues/34237)
    -   `sql_mode`を`NO_ZERO_DATE` [<a href="https://github.com/pingcap/tidb/issues/34099">#34099</a>](https://github.com/pingcap/tidb/issues/34099)に設定した場合、 `datetime`列に`'0000-00-00 00:00:00'`挿入できるバグを修正
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[<a href="https://github.com/pingcap/tidb/issues/33893">#33893</a>](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックすると発生する可能性があります。
    -   `NOWAIT`ステートメントで、ロック[<a href="https://github.com/pingcap/tidb/issues/32754">#32754</a>](https://github.com/pingcap/tidb/issues/32754)が発生したときに実行中のトランザクションがすぐに返されないバグを修正しました。
    -   `GBK`文字セットと`gbk_bin`照合順序[<a href="https://github.com/pingcap/tidb/issues/31308">#31308</a>](https://github.com/pingcap/tidb/issues/31308)を使用してテーブルを作成するときに失敗するバグを修正しました。
    -   `enable-new-charset`が`on`の場合、照合順序`GBK`文字セットのテーブルを作成すると、「不明な文字セット」エラー[<a href="https://github.com/pingcap/tidb/issues/31297">#31297</a>](https://github.com/pingcap/tidb/issues/31297)が発生して失敗するバグを修正しました。

-   TiKV

    -   マージ対象のターゲットリージョンが無効であるため、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[<a href="https://github.com/tikv/tikv/issues/12232">#12232</a>](https://github.com/tikv/tikv/issues/12232)
    -   古いメッセージによって TiKV がpanicになるバグを修正[<a href="https://github.com/tikv/tikv/issues/12023">#12023</a>](https://github.com/tikv/tikv/issues/12023)
    -   メモリメトリクス[<a href="https://github.com/tikv/tikv/issues/12160">#12160</a>](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/9765">#9765</a>](https://github.com/tikv/tikv/issues/9765)
    -   レプリカの読み取りが線形化可能性[<a href="https://github.com/tikv/tikv/issues/12109">#12109</a>](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   リージョン[<a href="https://github.com/tikv/tikv/issues/12048">#12048</a>](https://github.com/tikv/tikv/issues/12048)をマージするときに、ターゲット ピアが初期化されずに破棄されたピアに置き換えられるときに発生する TiKVpanicの問題を修正します。
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/11940">#11940</a>](https://github.com/tikv/tikv/issues/11940)
    -   ロックの解決ステップ[<a href="https://github.com/tikv/tikv/issues/11993">#11993</a>](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   ピアのステータスが`Applying` [<a href="https://github.com/tikv/tikv/issues/11746">#11746</a>](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/10210">#10210</a>](https://github.com/tikv/tikv/issues/10210)
    -   リソース メータリング[<a href="https://github.com/tikv/tikv/issues/12234">#12234</a>](https://github.com/tikv/tikv/issues/12234)の無効なアサーションによって引き起こされるpanicの問題を修正
    -   一部の特殊なケースで遅いスコア計算が不正確になる問題を修正[<a href="https://github.com/tikv/tikv/issues/12254">#12254</a>](https://github.com/tikv/tikv/issues/12254)
    -   `resolved_ts`モジュールによって引き起こされる OOM 問題を修正し、さらにメトリクスを追加します[<a href="https://github.com/tikv/tikv/issues/12159">#12159</a>](https://github.com/tikv/tikv/issues/12159)
    -   ネットワークが貧弱な場合、正常にコミットされた楽観的トランザクションが`Write Conflict`エラーを報告する可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34066">#34066</a>](https://github.com/pingcap/tidb/issues/34066)
    -   貧弱なネットワークでレプリカ読み取りが有効になっている場合に発生する TiKVpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/12046">#12046</a>](https://github.com/tikv/tikv/issues/12046)

-   PD

    -   `dr-autosync`の`Duration`フィールドを動的に設定できない問題を修正[<a href="https://github.com/tikv/pd/issues/4651">#4651</a>](https://github.com/tikv/pd/issues/4651)
    -   大容量のストア（たとえば 2T）が存在する場合、完全に割り当てられた小さなストアが検出できず、バランス演算子が生成されない問題を修正します[<a href="https://github.com/tikv/pd/issues/4805">#4805</a>](https://github.com/tikv/pd/issues/4805)
    -   ラベル分布のメトリクスに残留ラベルがある問題を修正します[<a href="https://github.com/tikv/pd/issues/4825">#4825</a>](https://github.com/tikv/pd/issues/4825)

-   TiFlash

    -   TLS が有効になっているときに発生するpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4196">#4196</a>](https://github.com/pingcap/tiflash/issues/4196)
    -   遅れているリージョンピア[<a href="https://github.com/pingcap/tiflash/issues/4437">#4437</a>](https://github.com/pingcap/tiflash/issues/4437)でのリージョンのマージによって発生する可能性のあるメタデータの破損を修正します。
    -   `JOIN`を含むクエリでエラーが発生した場合にハングする可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4195">#4195</a>](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4238">#4238</a>](https://github.com/pingcap/tiflash/issues/4238)
    -   `FLOAT` ～ `DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/3998">#3998</a>](https://github.com/pingcap/tiflash/issues/3998)キャスト時に発生するオーバーフローを修正
    -   期限切れデータのリサイクルが遅い問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4146">#4146</a>](https://github.com/pingcap/tiflash/issues/4146)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルするとタスクが永久にハングする可能性があるバグを修正します[<a href="https://github.com/pingcap/tiflash/issues/4229">#4229</a>](https://github.com/pingcap/tiflash/issues/4229)
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4098">#4098</a>](https://github.com/pingcap/tiflash/issues/4098)
    -   `DATETIME`から`DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/4151">#4151</a>](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   `Snapshot`が複数の DDL 操作と同時に適用される場合のTiFlashpanicの潜在的な問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4072">#4072</a>](https://github.com/pingcap/tiflash/issues/4072)
    -   無効なstorageディレクトリ構成が予期せぬ動作を引き起こすバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4093">#4093</a>](https://github.com/pingcap/tiflash/issues/4093)
    -   一部の例外が正しく処理されないバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4101">#4101</a>](https://github.com/pingcap/tiflash/issues/4101)
    -   `INT`から`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3920">#3920</a>](https://github.com/pingcap/tiflash/issues/3920)
    -   複数値式[<a href="https://github.com/pingcap/tiflash/issues/4016">#4016</a>](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式で`'\n'`無効な区切り文字[<a href="https://github.com/pingcap/tiflash/issues/4036">#4036</a>](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[<a href="https://github.com/pingcap/tiflash/issues/3967">#3967</a>](https://github.com/pingcap/tiflash/issues/3967)
    -   メモリ制限が有効になっているときに発生するpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/3902">#3902</a>](https://github.com/pingcap/tiflash/issues/3902)
    -   DTFiles [<a href="https://github.com/pingcap/tiflash/issues/4778">#4778</a>](https://github.com/pingcap/tiflash/issues/4778)の潜在的なデータ破損を修正
    -   多くの削除操作を含むテーブルに対してクエリを実行する際の潜在的なエラーを修正します[<a href="https://github.com/pingcap/tiflash/issues/4747">#4747</a>](https://github.com/pingcap/tiflash/issues/4747)
    -   TiFlashが多数の「Keepalive watchdog fired」エラーをランダムに報告するバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4192">#4192</a>](https://github.com/pingcap/tiflash/issues/4192)
    -   TiFlashノード[<a href="https://github.com/pingcap/tiflash/issues/4414">#4414</a>](https://github.com/pingcap/tiflash/issues/4414)にどのリージョン範囲にも一致しないデータが残るバグを修正
    -   GC [<a href="https://github.com/pingcap/tiflash/issues/4511">#4511</a>](https://github.com/pingcap/tiflash/issues/4511)以降に空のセグメントをマージできないバグを修正

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップの再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正しました[<a href="https://github.com/pingcap/tidb/issues/32423">#32423</a>](https://github.com/pingcap/tidb/issues/32423)
        -   BR がRawKV [<a href="https://github.com/pingcap/tidb/issues/32607">#32607</a>](https://github.com/pingcap/tidb/issues/32607)のバックアップに失敗する問題を修正
        -   増分復元[<a href="https://github.com/pingcap/tidb/issues/33596">#33596</a>](https://github.com/pingcap/tidb/issues/33596)後にテーブルにレコードを挿入するときの重複した主キーを修正します。
        -   空のクエリ[<a href="https://github.com/pingcap/tidb/issues/33322">#33322</a>](https://github.com/pingcap/tidb/issues/33322)を含む DDL ジョブによりBR増分リストアが誤ってエラーを返すバグを修正
        -   復元操作の完了後にリージョンが不均等に分散される可能性がある潜在的な問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31034">#31034</a>](https://github.com/pingcap/tidb/issues/31034)
        -   復元中にリージョンに一貫性がない場合、 BR が十分な回数再試行しない問題を修正[<a href="https://github.com/pingcap/tidb/issues/33419">#33419</a>](https://github.com/pingcap/tidb/issues/33419)
        -   小さなファイルのマージが有効になっているときにBR が時折panicする問題を修正します[<a href="https://github.com/pingcap/tidb/issues/33801">#33801</a>](https://github.com/pingcap/tidb/issues/33801)
        -   BRまたはTiDB Lightningが異常終了した後にスケジューラが再開しない問題を修正[<a href="https://github.com/pingcap/tidb/issues/33546">#33546</a>](https://github.com/pingcap/tidb/issues/33546)

    -   TiCDC

        -   所有者の変更によって引き起こされた誤ったメトリクスを修正する[<a href="https://github.com/pingcap/tiflow/issues/4774">#4774</a>](https://github.com/pingcap/tiflow/issues/4774)
        -   `Canal-JSON`が nil [<a href="https://github.com/pingcap/tiflow/issues/4736">#4736</a>](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性がある TiCDCpanic問題を修正
        -   Unified Sorter [<a href="https://github.com/pingcap/tiflow/issues/4447">#4447</a>](https://github.com/pingcap/tiflow/issues/4447)によって使用されるワーカープールの安定性の問題を修正しました。
        -   場合によってはシーケンスが不正に複製されるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4552">#4563</a>](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON` `string` [<a href="https://github.com/pingcap/tiflow/issues/4635">#4635</a>](https://github.com/pingcap/tiflow/issues/4635)を誤って処理した場合に発生する可能性がある TiCDCpanicの問題を修正
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4248">#4248</a>](https://github.com/pingcap/tiflow/issues/4248)
        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4501">#4501</a>](https://github.com/pingcap/tiflow/issues/4501)
        -   `rename tables` DDL [<a href="https://github.com/pingcap/tiflow/issues/5059">#5059</a>](https://github.com/pingcap/tiflow/issues/5059)によって引き起こされる DML 構築エラーを修正
        -   所有者が変更され、新しいスケジューラーが有効になっている場合 (デフォルトでは無効になっている)、 [<a href="https://github.com/pingcap/tiflow/issues/4963">#4963</a>](https://github.com/pingcap/tiflow/issues/4963)にレプリケーションが停止する可能性がある問題を修正します。
        -   新しいスケジューラーが有効になっている場合 (デフォルトでは無効になっています)、エラー ErrProcessorDuplicateOperations が報告される問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4769">#4769</a>](https://github.com/pingcap/tiflow/issues/4769)
        -   TLS を有効にした後、 `--pd`で設定した最初の PD が利用できない場合に TiCDC の起動に失敗する問題を修正[<a href="https://github.com/pingcap/tiflow/issues/4777">#4777</a>](https://github.com/pingcap/tiflow/issues/4777)
        -   テーブルがスケジュールされているときにチェックポイント メトリックが欠落する問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4714">#4714</a>](https://github.com/pingcap/tiflow/issues/4714)

    -   TiDB Lightning

        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」 [<a href="https://github.com/pingcap/tidb/issues/32733">#32733</a>](https://github.com/pingcap/tidb/issues/32733)を修正
        -   TiDB Lightning が空のテーブルのチェックに失敗するとスタックする問題を修正[<a href="https://github.com/pingcap/tidb/issues/31797">#31797</a>](https://github.com/pingcap/tidb/issues/31797)
        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[<a href="https://github.com/pingcap/tidb/issues/28144">#28144</a>](https://github.com/pingcap/tidb/issues/28144)
        -   事前チェックでローカル ディスク リソースとクラスターの可用性がチェックされない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/34213">#34213</a>](https://github.com/pingcap/tidb/issues/34213)

    -   TiDB データ移行 (DM)

        -   ログに何百もの「チェックポイントに変更はありません。同期フラッシュ チェックポイントをスキップします」と出力され、レプリケーションが非常に遅くなる問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4619">#4619</a>](https://github.com/pingcap/tiflow/issues/4619)
        -   long varchar がエラーを報告するバグを修正`Column length too big` [<a href="https://github.com/pingcap/tiflow/issues/4637">#4637</a>](https://github.com/pingcap/tiflow/issues/4637)
        -   セーフモードでの更新ステートメントの実行エラーにより DM ワーカーpanic[<a href="https://github.com/pingcap/tiflow/issues/4317">#4317</a>](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   場合によっては、フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開が失敗する可能性がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5272">#5272</a>](https://github.com/pingcap/tiflow/issues/5272)
        -   アップストリーム[<a href="https://github.com/pingcap/tiflow/issues/5121">#5121</a>](https://github.com/pingcap/tiflow/issues/5121)でbinlogが有効になっていない場合、 `query-status`コマンドに対してデータが返されないバグを修正
        -   `SHOW CREATE TABLE`ステートメント[<a href="https://github.com/pingcap/tiflow/issues/5159">#5159</a>](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーのpanic問題を修正します。
        -   GTID が有効になっている場合、またはタスクが自動的に再開された場合に、CPU 使用率が増加し、大量のログが出力される場合がある問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/5063">#5063</a>](https://github.com/pingcap/tiflow/issues/5063)
