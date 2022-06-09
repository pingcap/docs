---
title: TiDB 4.0 RC.2 Release Notes
---

# TiDB4.0RC.2リリースノート {#tidb-4-0-rc-2-release-notes}

発売日：2020年5月15日

TiDBバージョン：4.0.0-rc.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDB Binlogが有効になっている場合、単一トランザクションのサイズ制限（100 MB）を削除します。現在、トランザクションのサイズ制限は10GBです。ただし、TiDB Binlogが有効で、ダウンストリームがKafkaの場合は、Kafka3の1GBのメッセージサイズ制限に従って`txn-total-size-limit`パラメーターを構成し[＃16941](https://github.com/pingcap/tidb/pull/16941) 。
    -   `CLUSTER_LOG`テーブル[＃17003](https://github.com/pingcap/tidb/pull/17003)のクエリ時に時間範囲が指定されていない場合は、動作をデフォルトの時間範囲のクエリからエラーの返送と指定された時間範囲の要求に変更します。
    -   `CREATE TABLE`ステートメントを使用してパーティションテーブルを作成するときにサポートされていない`sub-partition`または`linear hash`オプションが指定されている場合、オプションが無視されたパーティションテーブルではなく、通常のテーブルが作成されます[＃17197](https://github.com/pingcap/tidb/pull/17197)

-   TiKV

    -   暗号化関連の構成をセキュリティ関連の構成に移動し[＃7810](https://github.com/tikv/tikv/pull/7810) 。つまり、TiKV構成ファイルの`[encryption]`を35に変更し`[security.encryption]` 。

-   ツール

    -   TiDB Lightning

        -   互換性を向上させるために、データをインポートするときにデフォルトのSQLモードを`ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER`に変更します[＃316](https://github.com/pingcap/tidb-lightning/pull/316)
        -   tidb-backendモードでPDまたはTiKVポートへのアクセスを禁止する[＃312](https://github.com/pingcap/tidb-lightning/pull/312)
        -   デフォルトでログ情報をtmpファイルに出力し、TiDBLightningの起動時にtmpファイルのパスを出力します[＃313](https://github.com/pingcap/tidb-lightning/pull/313)

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `WHERE`句に同等の条件が1つしかない場合に、間違ったパーティションが選択される問題を修正します[＃17054](https://github.com/pingcap/tidb/pull/17054)
    -   `WHERE`句に文字列列[＃16660](https://github.com/pingcap/tidb/pull/16660)のみが含まれている場合に、誤ったインデックス範囲を作成することによって引き起こされる誤った結果の問題を修正します。
    -   `DELETE`の操作の後にトランザクションで`PointGet`のクエリを実行するときに発生するパニックの問題を修正します[＃16991](https://github.com/pingcap/tidb/pull/16991)
    -   エラーが発生したときにGCワーカーがデッドロックに遭遇する可能性がある問題を修正します[＃16915](https://github.com/pingcap/tidb/pull/16915)
    -   TiKVの応答が遅いがダウンしていない場合は、不要なRegionMissの再試行を避けてください[＃16956](https://github.com/pingcap/tidb/pull/16956)
    -   MySQLプロトコルのハンドシェイクフェーズでクライアントのログレベルを`DEBUG`に変更して、ログ出力[＃16881](https://github.com/pingcap/tidb/pull/16881)に干渉する問題を解決します。
    -   `TRUNCATE`の操作の後にテーブルで定義された`PRE_SPLIT_REGIONS`の情報に従ってリージョンが事前に分割されないという問題を修正します[＃16776](https://github.com/pingcap/tidb/pull/16776)
    -   2フェーズコミットの第2フェーズでTiKVが使用できない場合に、再試行によって発生するゴルーチンの急上昇の問題を修正します[＃16876](https://github.com/pingcap/tidb/pull/16876)
    -   一部の式をプッシュダウンできない場合のステートメント実行のパニック問題を修正[＃16869](https://github.com/pingcap/tidb/pull/16869)
    -   パーティションテーブル[＃17124](https://github.com/pingcap/tidb/pull/17124)でのIndexMerge操作の誤った実行結果を修正します
    -   メモリトラッカー[＃17234](https://github.com/pingcap/tidb/pull/17234)のミューテックス競合によって引き起こされる`wide_table`のパフォーマンス低下を修正しました

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、アップグレード後にシステムが正常に起動できない問題を修正します

## 新機能 {#new-features}

-   TiDB

    -   データをバックアップおよび復元するための`BACKUP`および`RESTORE`コマンドのサポートを追加します[＃16960](https://github.com/pingcap/tidb/pull/16960)
    -   コミットする前に単一のリージョンのデータボリュームを事前にチェックし、データボリュームがしきい値を超えたときにリージョンを事前に分割することをサポートします[＃16959](https://github.com/pingcap/tidb/pull/16959)
    -   最後に実行されたステートメントがプランキャッシュにヒットするかどうかを示すために、スコープが`Session`の新しい`LAST_PLAN_FROM_CACHE`変数を追加します[＃16830](https://github.com/pingcap/tidb/pull/16830)
    -   `Cop_time`の情報を低速ログに記録し、 `SLOW_LOG`の表を[＃16904](https://github.com/pingcap/tidb/pull/16904)に記録することをサポートします。
    -   GoRuntime1のメモリステータスを監視するメトリックをGrafanaに追加し[＃16928](https://github.com/pingcap/tidb/pull/16928)
    -   一般ログ[＃16946](https://github.com/pingcap/tidb/pull/16946)での`forUpdateTS`および`Read Consistency`の分離レベル情報の出力をサポートします
    -   TiKVリージョン[＃16925](https://github.com/pingcap/tidb/pull/16925)でロックを解決する重複リクエストの折りたたみをサポート
    -   `SET CONFIG`ステートメントを使用してPD/TiKVノードの構成を変更することをサポート[＃16853](https://github.com/pingcap/tidb/pull/16853)
    -   `CREATE TABLE`ステートメント[＃16813](https://github.com/pingcap/tidb/pull/16813)で`auto_random`オプションをサポートする
    -   DistSQLリクエストにTaskIDを割り当てて、TiKVがリクエストをより適切にスケジュールおよび処理できるようにします[＃17155](https://github.com/pingcap/tidb/pull/17155)
    -   MySQLクライアントにログインした後のTiDBサーバーのバージョン情報の表示をサポート[＃17187](https://github.com/pingcap/tidb/pull/17187)
    -   `GROUP_CONCAT`関数[＃16990](https://github.com/pingcap/tidb/pull/16990)の`ORDER BY`節をサポートします。
    -   ステートメントがプランキャッシュ[＃17121](https://github.com/pingcap/tidb/pull/17121)にヒットするかどうかを示すために、スローログに`Plan_from_cache`の情報を表示することをサポートします。
    -   TiDBダッシュボードがTiFlashマルチディスク展開の容量情報を表示できる機能を追加します
    -   ダッシュボードのSQLステートメントを使用してTiFlashログをクエリする機能を追加します

-   TiKV

    -   tikv-ctlの暗号化デバッグをサポートし、暗号化ストレージが有効になっているときにtikv-ctlを使用してクラスタを操作および管理できるようにします[＃7698](https://github.com/tikv/tikv/pull/7698)
    -   スナップショット[＃7712](https://github.com/tikv/tikv/pull/7712)でロック列ファミリーの暗号化をサポートする
    -   GrafanaダッシュボードのRaftstoreレイテンシーサマリーのヒートマップを使用して、ジッターの問題をより適切に診断します[＃7717](https://github.com/tikv/tikv/pull/7717)
    -   gRPCメッセージのサイズの上限設定のサポート[＃7824](https://github.com/tikv/tikv/pull/7824)
    -   Grafanaダッシュボードに暗号化関連の監視メトリックを追加します[＃7827](https://github.com/tikv/tikv/pull/7827)
    -   アプリケーション層プロトコルネゴシエーション（ALPN） [＃7825](https://github.com/tikv/tikv/pull/7825)をサポートする
    -   タイタン[＃7818](https://github.com/tikv/tikv/pull/7818)に関する統計を追加する
    -   同じトランザクション内の別のタスクによってタスクの優先度が低下することを回避するために、統合読み取りプール内のIDとしてクライアントによって提供されたタスクIDの使用をサポートします[＃7814](https://github.com/tikv/tikv/pull/7814)
    -   `batch insert`リクエストのパフォーマンスを向上させる[＃7718](https://github.com/tikv/tikv/pull/7718)

-   PD

    -   ノードをオフラインにするときにピアを削除する速度制限を排除する[＃2372](https://github.com/pingcap/pd/pull/2372)

-   TiFlash

    -   Grafanaの**読み取りインデックス**のカウントグラフの名前を<strong>Ops</strong>に変更します
    -   システム負荷が低いときにファイル記述子を開くためにデータを最適化して、システムリソースの消費を削減します
    -   容量関連の構成パラメーターを追加して、データストレージ容量を制限します

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctlに`fetch-mode`つのサブコマンドを追加して、TiKVクラスタモード[＃287](https://github.com/pingcap/tidb-lightning/pull/287)を出力します。

    -   TiCDC

        -   `cdc cli` （changefeed） [＃546](https://github.com/pingcap/tiflow/pull/546)を使用してレプリケーションタスクの管理をサポートする

    -   バックアップと復元（BR）

        -   バックアップ中のGC時間の自動調整をサポート[＃257](https://github.com/pingcap/br/pull/257)
        -   データを復元するときにPDパラメータを調整して、復元を高速化します[＃198](https://github.com/pingcap/br/pull/198)

## バグの修正 {#bug-fixes}

-   TiDB

    -   複数の演算子で式の実行にベクトル化を使用するかどうかを決定するロジックを改善する[＃16383](https://github.com/pingcap/tidb/pull/16383)
    -   `IndexMerge`ヒントがデータベース名を正しくチェックできない問題を修正します[＃16932](https://github.com/pingcap/tidb/pull/16932)
    -   シーケンスオブジェクトの切り捨てを禁止する[＃17037](https://github.com/pingcap/tidb/pull/17037)
    -   `INSERT` `DELETE`がシーケンスオブジェクト`ANALYZE`で[＃16957](https://github.com/pingcap/tidb/pull/16957)できる問題を修正し`UPDATE`
    -   ブートストラップフェーズの内部SQLステートメントがステートメントの概要テーブル[＃17062](https://github.com/pingcap/tidb/pull/17062)で内部クエリとして正しくマークされない問題を修正します。
    -   TiFlashではサポートされているがTiKVではサポートされていないフィルター条件が`IndexLookupJoin`オペレーター[＃17036](https://github.com/pingcap/tidb/pull/17036)にプッシュダウンされたときに発生するエラーを修正します。
    -   照合順序を有効にした後に発生する可能性がある`LIKE`式の同時実行の問題を修正します[＃16997](https://github.com/pingcap/tidb/pull/16997)
    -   照合順序を有効にした後、 `LIKE`関数が`Range`クエリインデックスを正しく構築できない問題を修正します[＃16783](https://github.com/pingcap/tidb/pull/16783)
    -   `Plan Cache`ステートメントがトリガーされた後に`@@LAST_PLAN_FROM_CACHE`を実行すると、間違った値が返される問題を修正します[＃16831](https://github.com/pingcap/tidb/pull/16831)
    -   `IndexMerge` [＃16947](https://github.com/pingcap/tidb/pull/16947)の候補パスを計算するときに、インデックスの`TableFilter`が失われる問題を修正します。
    -   `MergeJoin`ヒントを使用し、 `TableDual`演算子が存在する場合、物理クエリプランを生成できない問題を修正します[＃17016](https://github.com/pingcap/tidb/pull/17016)
    -   ステートメントの要約表[＃17018](https://github.com/pingcap/tidb/pull/17018)の`Stmt_Type`列の値の誤った大文字化を修正します。
    -   異なるユーザーが同じ[＃16996](https://github.com/pingcap/tidb/pull/16996)を使用するとサービスを開始できないため、 `Permission Denied`エラーが報告される問題を修正し`tmp-storage-path` 。
    -   結果タイプが[＃16995](https://github.com/pingcap/tidb/pull/16995)などの複数の入力列によって決定される式に対して、 `NotNullFlag`の結果タイプが誤って設定される問題を修正し`CASE WHEN` 。
    -   ダーティストアが存在する場合、緑色のGCが未解決のロックを残す可能性がある問題を修正します[＃16949](https://github.com/pingcap/tidb/pull/16949)
    -   複数の異なるロックを持つ単一のキーに遭遇したときに、緑色のGCが未解決のロックを残す可能性がある問題を修正します[＃16948](https://github.com/pingcap/tidb/pull/16948)
    -   サブクエリが親クエリ列[＃16952](https://github.com/pingcap/tidb/pull/16952)を参照するため、 `INSERT VALUE`ステートメントに間違った値を挿入する問題を修正します。
    -   `Float`の値[＃16666](https://github.com/pingcap/tidb/pull/16666)で`AND`演算子を使用した場合の誤った結果の問題を修正します
    -   高価なログ[＃16907](https://github.com/pingcap/tidb/pull/16907)の`WAIT_TIME`フィールドの間違った情報を修正します
    -   悲観的トランザクションモード[＃16897](https://github.com/pingcap/tidb/pull/16897)では、 `SELECT FOR UPDATE`のステートメントを低速ログに記録できない問題を修正します。
    -   `Enum`または`Set`タイプ[＃16892](https://github.com/pingcap/tidb/pull/16892)の列で`SELECT DISTINCT`を実行したときに発生する誤った結果を修正します
    -   `SHOW CREATE  TABLE`ステートメント[＃16864](https://github.com/pingcap/tidb/pull/16864)の`auto_random_base`の表示エラーを修正します。
    -   `WHERE`節[＃16559](https://github.com/pingcap/tidb/pull/16559)の誤った値`string_value`を修正します
    -   `GROUP BY`ウィンドウ関数のエラーメッセージがMySQL3のエラーメッセージと矛盾する問題を修正し[＃16165](https://github.com/pingcap/tidb/pull/16165)
    -   データベース名に大文字の[＃17167](https://github.com/pingcap/tidb/pull/17167)が含まれている場合に`FLASH TABLE`ステートメントが実行されない問題を修正します
    -   Projectionexecutorの不正確なメモリトレースを修正します[＃17118](https://github.com/pingcap/tidb/pull/17118)
    -   異なるタイムゾーンでの`SLOW_QUERY`のテーブルの誤った時間フィルタリングの問題を修正します[＃17164](https://github.com/pingcap/tidb/pull/17164)
    -   仮想生成された列[＃17126](https://github.com/pingcap/tidb/pull/17126)で`IndexMerge`が使用されたときに発生するパニックの問題を修正します
    -   `INSTR`および`LOCATE`関数の大文字化の問題を修正します[＃17068](https://github.com/pingcap/tidb/pull/17068)
    -   `tidb_allow_batch_cop`の構成を有効にした後に`tikv server timeout`のエラーが頻繁に報告される問題を修正します[＃17161](https://github.com/pingcap/tidb/pull/17161)
    -   Floatタイプで`XOR`の操作を実行した結果が、 [＃16978](https://github.com/pingcap/tidb/pull/16978)の結果と矛盾する問題を修正します。
    -   サポートされていない`ALTER TABLE REORGANIZE PARTITION`ステートメントが実行されたときにエラーが報告されない問題を修正します[＃17178](https://github.com/pingcap/tidb/pull/17178)
    -   `EXPLAIN FORMAT="dot"  FOR CONNECTION ID`がサポートされていないプランに遭遇したときにエラーが報告される問題を修正します[＃17160](https://github.com/pingcap/tidb/pull/17160)
    -   ステートメント要約表[＃17086](https://github.com/pingcap/tidb/pull/17086)の`EXEC_COUNT`列にあるプリペアドステートメントのレコードの問題を修正します。
    -   ステートメントサマリーシステム変数[＃17129](https://github.com/pingcap/tidb/pull/17129)を設定するときに値が検証されない問題を修正します
    -   プランキャッシュが有効になっているときにオーバーフロー値を使用して`UNSIGNED BIGINT`主キーをクエリすると、エラーが報告される問題を修正します[＃17120](https://github.com/pingcap/tidb/pull/17120)
    -   **GrafanaTiDBサマリー**ダッシュボードのマシンインスタンスとリクエストタイプによる誤ったQPS表示を修正します[＃17105](https://github.com/pingcap/tidb/pull/17105)

-   TiKV

    -   復元後に多くの空のリージョンが生成される問題を修正します[＃7632](https://github.com/tikv/tikv/pull/7632)
    -   順不同の読み取りインデックス応答を受信したときのRaftstoreのパニック問題を修正します[＃7370](https://github.com/tikv/tikv/pull/7370)
    -   統合スレッドプールが有効になっている場合に、無効なストレージまたはコプロセッサーの読み取りプール構成が拒否されない可能性がある問題を修正します[＃7513](https://github.com/tikv/tikv/pull/7513)
    -   TiKVサーバーがシャットダウンされたときの`join`操作のパニック問題を修正します[＃7713](https://github.com/tikv/tikv/pull/7713)
    -   診断API1を介してTiKV低速ログを検索すると結果が返されない問題を修正し[＃7776](https://github.com/tikv/tikv/pull/7776)
    -   TiKVノードが長時間実行されているときに顕著なメモリの断片化が生成される問題を修正します[＃7556](https://github.com/tikv/tikv/pull/7556)
    -   無効な日付が保存されている場合にSQLステートメントが実行されない問題を修正します[＃7268](https://github.com/tikv/tikv/pull/7268)
    -   GCS1からバックアップデータを復元できない問題を修正し[＃7739](https://github.com/tikv/tikv/pull/7739)
    -   保管時の暗号化中にKMSキーIDが検証されない問題を修正します[＃7719](https://github.com/tikv/tikv/pull/7719)
    -   異なるアーキテクチャのコンパイラでのコプロセッサの根本的な正確性の問題を修正し[＃7730](https://github.com/tikv/tikv/pull/7730) [＃7714](https://github.com/tikv/tikv/pull/7714)
    -   暗号化が有効になっている場合の`snapshot ingestion`のエラーを修正します[＃7815](https://github.com/tikv/tikv/pull/7815)
    -   構成ファイルを書き換えるときの`Invalid cross-device link`のエラーを修正します[＃7817](https://github.com/tikv/tikv/pull/7817)
    -   構成ファイルを空のファイルに書き込むときの誤ったtoml形式の問題を修正します[＃7817](https://github.com/tikv/tikv/pull/7817)
    -   Raftstoreで破棄されたピアが引き続きリクエストを処理できる問題を修正します[＃7836](https://github.com/tikv/tikv/pull/7836)

-   PD

    -   pd-ctl5で`region key`コマンドを使用したときに発生する`404`の問題を修正し[＃2399](https://github.com/pingcap/pd/pull/2399) 。
    -   TSOとID割り当てのモニターメトリックがGrafanaダッシュボードから欠落している問題を修正します[＃2405](https://github.com/pingcap/pd/pull/2405)
    -   pd-recoverがDockerイメージに含まれていない問題を修正します[＃2406](https://github.com/pingcap/pd/pull/2406)
    -   データディレクトリのパスを絶対パスに解析して、TiDBダッシュボードがPD情報を正しく表示しない可能性がある問題を修正します[＃2420](https://github.com/pingcap/pd/pull/2420)
    -   pd- [＃2416](https://github.com/pingcap/pd/pull/2416)で`scheduler config shuffle-region-scheduler`コマンドを使用するとデフォルトの出力がないという問題を修正します。

-   TiFlash

    -   一部のシナリオで、使用済み容量の誤った情報が報告されるという問題を修正します

-   ツール

    -   TiDB Binlog

        -   ダウンストリームがKafka3の場合、 `mediumint`タイプのデータが処理されない問題を修正し[＃962](https://github.com/pingcap/tidb-binlog/pull/962)
        -   DDLのデータベース名がキーワード[＃961](https://github.com/pingcap/tidb-binlog/pull/961)の場合、reparoがDDLステートメントの解析に失敗する問題を修正します。

    -   TiCDC

        -   `TZ`の環境変数が設定されていないときに間違ったタイムゾーンを使用する問題を修正します[＃512](https://github.com/pingcap/tiflow/pull/512)

        -   一部のエラーが正しく処理されないために、サーバーの終了時に所有者がリソースをクリーンアップしない問題を修正します[＃528](https://github.com/pingcap/tiflow/pull/528)

        -   TiKV1に再接続するときにTiCDCがスタックする可能性がある問題を修正し[＃531](https://github.com/pingcap/tiflow/pull/531)

        -   テーブルスキーマ[＃534](https://github.com/pingcap/tiflow/pull/534)を初期化するときにメモリ使用量を最適化する

        -   `watch`モードを使用してレプリケーションステータスの変更を監視し、準リアルタイム更新を実行してレプリケーションの遅延を減らします[＃481](https://github.com/pingcap/tiflow/pull/481)

    <!---->

    -   バックアップと復元（BR）

        -   BRが`auto_random`属性[＃241](https://github.com/pingcap/br/issues/241)のテーブルを復元した後、データを挿入すると`duplicate entry`エラーがトリガーされる可能性がある問題を修正します。
