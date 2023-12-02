---
title: TiDB 4.0 RC.2 Release Notes
---

# TiDB 4.0 RC.2 リリース ノート {#tidb-4-0-rc-2-release-notes}

発売日：2020年5月15日

TiDB バージョン: 4.0.0-rc.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDB Binlogが有効な場合、単一トランザクションのサイズ制限 (100 MB) を削除します。現在、トランザクションのサイズ制限は 10 GB です。ただし、TiDB Binlogが有効で、ダウンストリームが Kafka である場合は、Kafka [#16941](https://github.com/pingcap/tidb/pull/16941)の 1 GB のメッセージ サイズ制限に従って`txn-total-size-limit`パラメーターを構成します。
    -   デフォルトの時間範囲のクエリから、テーブル`CLUSTER_LOG`のクエリ時に時間範囲が指定されていない場合にエラーを返し、指定された時間範囲を要求するように動作を変更します[#17003](https://github.com/pingcap/tidb/pull/17003)
    -   `CREATE TABLE`ステートメントを使用してパーティションテーブルを作成するときに、サポートされていない`sub-partition`または`linear hash`オプションが指定された場合、オプションが無視されたパーティションテーブルではなく、通常のテーブルが作成されます。 [#17197](https://github.com/pingcap/tidb/pull/17197)

-   TiKV

    -   暗号化関連の構成をセキュリティ関連の構成に移動します。つまり、TiKV 構成ファイルの`[encryption]`を`[security.encryption]` [#7810](https://github.com/tikv/tikv/pull/7810)に変更します。

-   ツール

    -   TiDB Lightning

        -   互換性を向上させるために、データをインポートするときにデフォルトの SQL モードを`ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER`に変更します[#316](https://github.com/pingcap/tidb-lightning/pull/316)
        -   tidb-backend モード[#312](https://github.com/pingcap/tidb-lightning/pull/312)での PD または TiKV ポートへのアクセスを禁止します。
        -   デフォルトでログ情報を tmp ファイルに出力し、 TiDB Lightning の起動時に tmp ファイルのパスを出力します[#313](https://github.com/pingcap/tidb-lightning/pull/313)

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `WHERE`句に同等の条件が 1 つしかない場合、間違ったパーティションが選択される問題を修正[#17054](https://github.com/pingcap/tidb/pull/17054)
    -   `WHERE`句に文字列列[#16660](https://github.com/pingcap/tidb/pull/16660)のみが含まれている場合に、誤ったインデックス範囲を構築することによって引き起こされる誤った結果の問題を修正します。
    -   `DELETE`操作[#16991](https://github.com/pingcap/tidb/pull/16991)の後のトランザクションで`PointGet`クエリを実行するときに発生するpanicの問題を修正します。
    -   エラー発生時に GC ワーカーがデッドロックに遭遇する可能性がある問題を修正[#16915](https://github.com/pingcap/tidb/pull/16915)
    -   TiKV 応答が遅いがダウンしていない場合は、不必要な RegionMiss の再試行を回避します[#16956](https://github.com/pingcap/tidb/pull/16956)
    -   ログ出力を妨げる問題を解決するには、MySQL プロトコルのハンドシェイク フェーズでクライアントのログ レベルを`DEBUG`に変更します[#16881](https://github.com/pingcap/tidb/pull/16881)
    -   `TRUNCATE`操作後のテーブルで定義された`PRE_SPLIT_REGIONS`情報に従ってリージョンが事前分割されない問題を修正[#16776](https://github.com/pingcap/tidb/pull/16776)
    -   2 フェーズ コミット[#16876](https://github.com/pingcap/tidb/pull/16876)の第 2 フェーズ中に TiKV が利用できない場合の再試行によって引き起こされるゴルーチンの高騰の問題を修正
    -   一部の式をプッシュダウンできない場合のステートメント実行のpanicの問題を修正します[#16869](https://github.com/pingcap/tidb/pull/16869)
    -   パーティションテーブル[#17124](https://github.com/pingcap/tidb/pull/17124)に対する IndexMerge 操作の間違った実行結果を修正しました。
    -   Memory Tracker [#17234](https://github.com/pingcap/tidb/pull/17234)のミューテックス競合によって引き起こされるパフォーマンス低下`wide_table`を修正しました。

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、アップグレード後にシステムが正常に起動できない問題を修正

## 新機能 {#new-features}

-   TiDB

    -   データをバックアップおよび復元するための`BACKUP`および`RESTORE`コマンドのサポートを追加[#16960](https://github.com/pingcap/tidb/pull/16960)
    -   コミット前の単一リージョン内のデータ量の事前チェックと、データ量がしきい値[#16959](https://github.com/pingcap/tidb/pull/16959)を超えた場合のリージョンの事前分割をサポートします。
    -   最後に実行されたステートメントがプラン キャッシュ[#16830](https://github.com/pingcap/tidb/pull/16830)にヒットしたかどうかを示すために、スコープ`Session`持つ新しい`LAST_PLAN_FROM_CACHE`変数を追加します。
    -   スローログでの`Cop_time`情報と`SLOW_LOG`テーブルの記録をサポート[#16904](https://github.com/pingcap/tidb/pull/16904)
    -   Go ランタイム[#16928](https://github.com/pingcap/tidb/pull/16928)のメモリ状態を監視するメトリクスを Grafana に追加します。
    -   一般ログ[#16946](https://github.com/pingcap/tidb/pull/16946)での`forUpdateTS`および`Read Consistency`分離レベル情報の出力のサポート
    -   TiKVリージョン[#16925](https://github.com/pingcap/tidb/pull/16925)でのロック解決の重複リクエストの折りたたみをサポート
    -   `SET CONFIG`ステートメントを使用した PD/TiKV ノードの構成変更のサポート[#16853](https://github.com/pingcap/tidb/pull/16853)
    -   `CREATE TABLE`ステートメントの`auto_random`オプションをサポートします[#16813](https://github.com/pingcap/tidb/pull/16813)
    -   TiKV がリクエストをより適切にスケジュールおよび処理できるように、DistSQL リクエストに TaskID を割り当てます[#17155](https://github.com/pingcap/tidb/pull/17155)
    -   MySQL クライアントへのログイン後の TiDBサーバーのバージョン情報の表示をサポート[#17187](https://github.com/pingcap/tidb/pull/17187)
    -   `GROUP_CONCAT`機能[#16990](https://github.com/pingcap/tidb/pull/16990)の`ORDER BY`句をサポートします。
    -   ステートメントがプラン キャッシュ[#17121](https://github.com/pingcap/tidb/pull/17121)にヒットしたかどうかを示す、スロー ログ内の`Plan_from_cache`情報の表示をサポートします。
    -   TiDB ダッシュボードにTiFlashマルチディスク展開の容量情報を表示できる機能を追加
    -   ダッシュボードに SQL ステートメントを使用してTiFlashログをクエリする機能を追加

-   TiKV

    -   tikv-ctl の暗号化デバッグをサポートし、暗号化storageが有効な場合に tikv-ctl を使用してクラスターを操作および管理できるようにします[#7698](https://github.com/tikv/tikv/pull/7698)
    -   スナップショット[#7712](https://github.com/tikv/tikv/pull/7712)でのロックカラムファミリーの暗号化のサポート
    -   Grafana ダッシュボードのヒートマップを使用してRaftstoreレイテンシーの概要を確認し、ジッターの問題をより適切に診断します[#7717](https://github.com/tikv/tikv/pull/7717)
    -   gRPC メッセージのサイズの上限設定のサポート[#7824](https://github.com/tikv/tikv/pull/7824)
    -   Grafana ダッシュボードに暗号化関連の監視メトリクスを追加する[#7827](https://github.com/tikv/tikv/pull/7827)
    -   アプリケーション層プロトコル ネゴシエーション (ALPN) [#7825](https://github.com/tikv/tikv/pull/7825)のサポート
    -   Titan [#7818](https://github.com/tikv/tikv/pull/7818)に関する統計をさらに追加します
    -   タスクの優先度が同じトランザクション内の別のタスクによって低下することを避けるために、クライアントによって提供されたタスク ID を統合読み取りプール内の識別子として使用するサポート[#7814](https://github.com/tikv/tikv/pull/7814)
    -   `batch insert`リクエスト[#7718](https://github.com/tikv/tikv/pull/7718)のパフォーマンスを向上させる

-   PD

    -   ノードをオフラインにするときのピア削除の速度制限を排除します[#2372](https://github.com/pingcap/pd/pull/2372)

-   TiFlash

    -   Grafana の**Read Index**の Count グラフの名前を**Ops**に変更します。
    -   システム負荷が低いときにファイル記述子を開くためのデータを最適化し、システム リソースの消費を削減します。
    -   データstorage容量を制限するには、容量関連の構成パラメータを追加します。

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctl に`fetch-mode`サブコマンドを追加して、TiKV クラスター モード[#287](https://github.com/pingcap/tidb-lightning/pull/287)を出力します。

    -   TiCDC

        -   `cdc cli` (変更フィード) [#546](https://github.com/pingcap/tiflow/pull/546)を使用したレプリケーション タスクの管理のサポート

    -   バックアップと復元 (BR)

        -   バックアップ中の GC 時間の自動調整をサポート[#257](https://github.com/pingcap/br/pull/257)
        -   データを復元するときに PD パラメータを調整して復元を高速化します[#198](https://github.com/pingcap/br/pull/198)

## バグの修正 {#bug-fixes}

-   TiDB

    -   複数の演算子での式の実行にベクトル化を使用するかどうかを決定するロジックを改善します[#16383](https://github.com/pingcap/tidb/pull/16383)
    -   `IndexMerge`ヒントでデータベース名が正しくチェックできない問題を修正[#16932](https://github.com/pingcap/tidb/pull/16932)
    -   シーケンス オブジェクトの切り捨てを禁止します[#17037](https://github.com/pingcap/tidb/pull/17037)
    -   `INSERT` / `UPDATE` / `ANALYZE` / `DELETE`ステートメントがシーケンス オブジェクトに対して実行できる問題を修正[#16957](https://github.com/pingcap/tidb/pull/16957)
    -   ブートストラップ フェーズの内部 SQL ステートメントが、ステートメント サマリー テーブル[#17062](https://github.com/pingcap/tidb/pull/17062)で内部クエリとして正しくマークされない問題を修正します。
    -   TiFlashではサポートされているが TiKV ではサポートされていないフィルター条件が`IndexLookupJoin`演算子[#17036](https://github.com/pingcap/tidb/pull/17036)にプッシュダウンされた場合に発生するエラーを修正しました。
    -   照合順序が有効になった後に発生する可能性がある`LIKE`式の同時実行性の問題を修正します[#16997](https://github.com/pingcap/tidb/pull/16997)
    -   照合順序が有効になった後、 `LIKE`関数が`Range`インデックスを正しく構築できない問題を修正します[#16783](https://github.com/pingcap/tidb/pull/16783)
    -   `Plan Cache`ステートメントがトリガーされた後に`@@LAST_PLAN_FROM_CACHE`を実行すると、間違った値が返される問題を修正[#16831](https://github.com/pingcap/tidb/pull/16831)
    -   `IndexMerge` [#16947](https://github.com/pingcap/tidb/pull/16947)の候補パスを計算するときにインデックスの`TableFilter`欠落する問題を修正
    -   `MergeJoin`ヒントを使用し、 `TableDual`演算子が存在する場合、物理クエリ プランが生成できない問題を修正します[#17016](https://github.com/pingcap/tidb/pull/17016)
    -   ステートメントの概要表[#17018](https://github.com/pingcap/tidb/pull/17018)の`Stmt_Type`列の値の大文字と小文字の違いを修正します。
    -   異なるユーザーが同じ`tmp-storage-path` [#16996](https://github.com/pingcap/tidb/pull/16996)を使用するとサービスを開始できないため、 `Permission Denied`エラーが報告される問題を修正
    -   結果の型が複数の入力列によって決定される式 ( `CASE WHEN` [#16995](https://github.com/pingcap/tidb/pull/16995)など) に対して`NotNullFlag`結果の型が誤って設定される問題を修正します。
    -   ダーティ ストアが存在する場合、緑色の GC が未解決のロックを残す可能性がある問題を修正します[#16949](https://github.com/pingcap/tidb/pull/16949)
    -   単一のキーに複数の異なるロックが設定されている場合に、緑色の GC が未解決のロックを残す可能性がある問題を修正します[#16948](https://github.com/pingcap/tidb/pull/16948)
    -   サブクエリが親クエリ列[#16952](https://github.com/pingcap/tidb/pull/16952)を参照しているため、 `INSERT VALUE`ステートメントに間違った値が挿入される問題を修正します。
    -   `Float`値[#16666](https://github.com/pingcap/tidb/pull/16666)に対して`AND`演算子を使用すると、誤った結果が表示される問題を修正します。
    -   高価なログ[#16907](https://github.com/pingcap/tidb/pull/16907)の`WAIT_TIME`フィールドの誤った情報を修正
    -   悲観的トランザクションモード[#16897](https://github.com/pingcap/tidb/pull/16897)のスローログに`SELECT FOR UPDATE`ステートメントが記録できない問題を修正
    -   `Enum`または`Set`タイプ[#16892](https://github.com/pingcap/tidb/pull/16892)の列に対して`SELECT DISTINCT`実行したときに発生する間違った結果を修正しました。
    -   `SHOW CREATE TABLE`ステートメント[#16864](https://github.com/pingcap/tidb/pull/16864)の`auto_random_base`の表示エラーを修正
    -   `WHERE`節[#16559](https://github.com/pingcap/tidb/pull/16559)の誤った値`string_value`を修正します。
    -   `GROUP BY` window関数のエラーメッセージがMySQL [#16165](https://github.com/pingcap/tidb/pull/16165)のエラーメッセージと一致しない問題を修正
    -   データベース名に大文字の[#17167](https://github.com/pingcap/tidb/pull/17167)が含まれる場合、 `FLASH TABLE`ステートメントの実行が失敗する問題を修正します。
    -   Projection Executor [#17118](https://github.com/pingcap/tidb/pull/17118)の不正確なメモリトレースを修正しました。
    -   異なるタイムゾーンでの`SLOW_QUERY`テーブルの誤った時間フィルタリングの問題を修正します[#17164](https://github.com/pingcap/tidb/pull/17164)
    -   仮想生成列[#17126](https://github.com/pingcap/tidb/pull/17126)で`IndexMerge`使用したときに発生するpanicの問題を修正
    -   `INSTR`および`LOCATE`関数の大文字化の問題を修正します[#17068](https://github.com/pingcap/tidb/pull/17068)
    -   `tidb_allow_batch_cop`構成を有効にした後、 `tikv server timeout`エラーが頻繁に報告される問題を修正[#17161](https://github.com/pingcap/tidb/pull/17161)
    -   Float 型に対して`XOR`の操作を実行した結果が MySQL 8.0 の結果と一致しない問題を修正[#16978](https://github.com/pingcap/tidb/pull/16978)
    -   サポートされていない`ALTER TABLE REORGANIZE PARTITION`ステートメントが実行されたときにエラーが報告されない問題を修正します[#17178](https://github.com/pingcap/tidb/pull/17178)
    -   `EXPLAIN FORMAT="dot"  FOR CONNECTION ID`サポートされていないプランに遭遇した場合にエラーが報告される問題を修正[#17160](https://github.com/pingcap/tidb/pull/17160)
    -   ステートメント概要テーブル[#17086](https://github.com/pingcap/tidb/pull/17086)の`EXEC_COUNT`列のプリペアドステートメントのレコードの問題を修正します。
    -   Statement Summary システム変数[#17129](https://github.com/pingcap/tidb/pull/17129)を設定するときに値が検証されない問題を修正します。
    -   プラン キャッシュが有効になっている場合に、オーバーフロー値を使用して主キー`UNSIGNED BIGINT`をクエリすると、エラーが報告される問題を修正します[#17120](https://github.com/pingcap/tidb/pull/17120)
    -   Grafana **TiDB Summary**ダッシュボード[#17105](https://github.com/pingcap/tidb/pull/17105)上のマシン インスタンスおよびリクエスト タイプによる誤った QPS 表示を修正しました。

-   TiKV

    -   復元[#7632](https://github.com/tikv/tikv/pull/7632)後に空きリージョンが多数生成される問題を修正
    -   順不同の読み取りインデックス応答を受信したときのRaftstoreのpanic問題を修正[#7370](https://github.com/tikv/tikv/pull/7370)
    -   統合スレッド プールが有効になっている場合、無効なstorageまたはコプロセッサ読み取りプール構成が拒否されないことがある問題を修正します[#7513](https://github.com/tikv/tikv/pull/7513)
    -   TiKVサーバーがシャットダウンされているときの`join`操作のpanicの問題を修正します[#7713](https://github.com/tikv/tikv/pull/7713)
    -   診断 API [#7776](https://github.com/tikv/tikv/pull/7776)経由で TiKV 低速ログを検索すると結果が返されない問題を修正
    -   TiKV ノードを長時間実行すると顕著なメモリの断片化が発生する問題を修正[#7556](https://github.com/tikv/tikv/pull/7556)
    -   無効な日付が格納されている場合に SQL ステートメントの実行が失敗する問題を修正します[#7268](https://github.com/tikv/tikv/pull/7268)
    -   [#7739](https://github.com/tikv/tikv/pull/7739)からバックアップデータを復元できない問題を修正
    -   保存時の暗号化中に KMS キー ID が検証されない問題を修正[#7719](https://github.com/tikv/tikv/pull/7719)
    -   異なるアーキテクチャのコンパイラーにおけるコプロセッサーの根本的な正確性の問題を修正します[#7714](https://github.com/tikv/tikv/pull/7714) [#7730](https://github.com/tikv/tikv/pull/7730)
    -   暗号化が有効な場合の`snapshot ingestion`エラーを修正します[#7815](https://github.com/tikv/tikv/pull/7815)
    -   `Invalid cross-device link`設定ファイル書き換え時のエラーを修正[#7817](https://github.com/tikv/tikv/pull/7817)
    -   設定ファイルを空のファイルに書き込むときに間違った toml 形式が発生する問題を修正します[#7817](https://github.com/tikv/tikv/pull/7817)
    -   Raftstoreの破壊されたピアが引き続きリクエストを処理できる問題を修正します[#7836](https://github.com/tikv/tikv/pull/7836)

-   PD

    -   pd-ctl [#2399](https://github.com/pingcap/pd/pull/2399)の`region key`コマンド使用時に発生する`404`問題を修正
    -   TSO および ID 割り当ての監視メトリクスが Grafana ダッシュボードに表示されない問題を修正します[#2405](https://github.com/pingcap/pd/pull/2405)
    -   pd-recover が Docker イメージに含まれていない問題を修正[#2406](https://github.com/pingcap/pd/pull/2406)
    -   データ ディレクトリのパスを絶対パスに解析して、TiDB ダッシュボードに PD 情報が正しく表示されない可能性がある問題を修正します[#2420](https://github.com/pingcap/pd/pull/2420)
    -   pd-ctl [#2416](https://github.com/pingcap/pd/pull/2416)の`scheduler config shuffle-region-scheduler`コマンド使用時にデフォルト出力がない問題を修正

-   TiFlash

    -   一部のシナリオで誤った使用容量情報が報告される問題を修正

-   ツール

    -   TiDBBinlog

        -   ダウンストリームがKafka [#962](https://github.com/pingcap/tidb-binlog/pull/962)の場合、タイプ`mediumint`のデータが処理されない問題を修正
        -   DDL 内のデータベース名がキーワード[#961](https://github.com/pingcap/tidb-binlog/pull/961)である場合、reparo が DDL ステートメントの解析に失敗する問題を修正します。

    -   TiCDC

        -   `TZ`環境変数が設定されていない場合に間違ったタイムゾーンが使用される問題を修正します[#512](https://github.com/pingcap/tiflow/pull/512)

        -   一部のエラーが正しく処理されないため、サーバーの終了時に所有者がリソースをクリーンアップしない問題を修正します[#528](https://github.com/pingcap/tiflow/pull/528)

        -   TiKV [#531](https://github.com/pingcap/tiflow/pull/531)に再接続するときに TiCDC が停止する可能性がある問題を修正

        -   テーブルスキーマ[#534](https://github.com/pingcap/tiflow/pull/534)の初期化時のメモリ使用量を最適化します。

        -   `watch`モードを使用してレプリケーション ステータスの変化を監視し、準リアルタイム更新を実行してレプリケーションの遅延を削減します[#481](https://github.com/pingcap/tiflow/pull/481)

    <!---->

    -   バックアップと復元 (BR)

        -   BR が`auto_random`属性[#241](https://github.com/pingcap/br/issues/241)を持つテーブルを復元した後、データを挿入すると`duplicate entry`エラーがトリガーされる可能性がある問題を修正します。
