---
title: TiDB 4.0 RC.2 Release Notes
---

# TiDB 4.0 RC.2 リリースノート {#tidb-4-0-rc-2-release-notes}

発売日：2020年5月15日

TiDB バージョン: 4.0.0-rc.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDB Binlogが有効な場合、単一トランザクション (100 MB) のサイズ制限を削除します。現在、トランザクションのサイズ制限は 10 GB です。ただし、TiDB Binlogが有効でダウンストリームが Kafka の場合、Kafka [#16941](https://github.com/pingcap/tidb/pull/16941)の 1 GB のメッセージ サイズ制限に従って`txn-total-size-limit`パラメータを構成します。
    -   `CLUSTER_LOG`テーブルのクエリ時に時間範囲が指定されていない場合、デフォルトの時間範囲のクエリからエラーを返し、指定された時間範囲を要求するように動作を変更します[#17003](https://github.com/pingcap/tidb/pull/17003)
    -   `CREATE TABLE`ステートメントを使用してパーティションテーブルを作成するときに、サポートされていない`sub-partition`または`linear hash`オプションを指定すると、オプションが無視されたパーティションテーブルではなく、通常のテーブルが作成されます[#17197](https://github.com/pingcap/tidb/pull/17197)

-   TiKV

    -   暗号化関連の構成をセキュリティ関連の構成に移動します。つまり、TiKV 構成ファイルの`[encryption]`を`[security.encryption]` [#7810](https://github.com/tikv/tikv/pull/7810)に変更します。

-   ツール

    -   TiDB Lightning

        -   データのインポート時にデフォルトの SQL モードを`ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER`に変更して、互換性を向上させます[#316](https://github.com/pingcap/tidb-lightning/pull/316)
        -   tidb-backend モード[#312](https://github.com/pingcap/tidb-lightning/pull/312)での PD または TiKV ポートへのアクセスを許可しない
        -   ログ情報をデフォルトで tmp ファイルに出力し、 TiDB Lightningの起動時に tmp ファイルのパスを出力します[#313](https://github.com/pingcap/tidb-lightning/pull/313)

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `WHERE`節に同等の条件が 1 つしかない場合に間違ったパーティションが選択される問題を修正します[#17054](https://github.com/pingcap/tidb/pull/17054)
    -   `WHERE`句に文字列列[#16660](https://github.com/pingcap/tidb/pull/16660)のみが含まれている場合に、誤ったインデックス範囲を構築することによって引き起こされる誤った結果の問題を修正します。
    -   `DELETE`操作[#16991](https://github.com/pingcap/tidb/pull/16991)後のトランザクションで`PointGet`クエリを実行すると発生するpanicの問題を修正します。
    -   エラーが発生したときに GC ワーカーでデッドロックが発生する可能性がある問題を修正します[#16915](https://github.com/pingcap/tidb/pull/16915)
    -   TiKV 応答が遅いがダウンしていない場合、不要な RegionMiss リトライを回避する[#16956](https://github.com/pingcap/tidb/pull/16956)
    -   ログ出力に干渉する問題を解決するために、MySQL プロトコルのハンドシェイク フェーズでクライアントのログ レベルを`DEBUG`に変更します[#16881](https://github.com/pingcap/tidb/pull/16881)
    -   `TRUNCATE`操作後、テーブルで定義された`PRE_SPLIT_REGIONS`情報に従ってリージョンが事前に分割されない問題を修正します[#16776](https://github.com/pingcap/tidb/pull/16776)
    -   2 フェーズ コミット[#16876](https://github.com/pingcap/tidb/pull/16876)の第 2 フェーズで TiKV が使用できない場合、リトライによってゴルーチンが急増する問題を修正します。
    -   一部の式をプッシュダウンできない場合のステートメント実行のpanic問題を修正します[#16869](https://github.com/pingcap/tidb/pull/16869)
    -   パーティションテーブルでの IndexMerge 操作の誤った実行結果を修正します[#17124](https://github.com/pingcap/tidb/pull/17124)
    -   メモリ トラッカー[#17234](https://github.com/pingcap/tidb/pull/17234)のミューテックス競合によって引き起こされる`wide_table`のパフォーマンス低下を修正します。

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれていると、アップグレード後にシステムが正常に起動できない問題を修正

## 新機能 {#new-features}

-   TiDB

    -   データをバックアップおよび復元するための`BACKUP`および`RESTORE`コマンドのサポートを追加します[#16960](https://github.com/pingcap/tidb/pull/16960)
    -   コミット前に 1 つのリージョン内のデータ ボリュームの事前チェックをサポートし、データ ボリュームがしきい値[#16959](https://github.com/pingcap/tidb/pull/16959)を超えた場合にリージョンを事前に分割します
    -   `Session`スコープを持つ新しい`LAST_PLAN_FROM_CACHE`変数を追加して、最後に実行されたステートメントがプラン キャッシュ[#16830](https://github.com/pingcap/tidb/pull/16830)にヒットするかどうかを示します
    -   スローログと`SLOW_LOG`テーブル[#16904](https://github.com/pingcap/tidb/pull/16904)に`Cop_time`情報の記録をサポート
    -   Go ランタイム[#16928](https://github.com/pingcap/tidb/pull/16928)のメモリステータスを監視するメトリックを Grafana に追加します。
    -   一般ログ[#16946](https://github.com/pingcap/tidb/pull/16946)での分離レベル`forUpdateTS`および`Read Consistency`情報の出力をサポート
    -   TiKVリージョン[#16925](https://github.com/pingcap/tidb/pull/16925)でのロック解決の重複リクエストの折りたたみをサポート
    -   PD/TiKV ノードの構成を変更する`SET CONFIG`ステートメントを使用したサポート[#16853](https://github.com/pingcap/tidb/pull/16853)
    -   `CREATE TABLE`ステートメント[#16813](https://github.com/pingcap/tidb/pull/16813)の`auto_random`オプションをサポートする
    -   DistSQL リクエストに TaskID を割り当てて、TiKV がリクエストをより適切にスケジュールおよび処理できるようにします[#17155](https://github.com/pingcap/tidb/pull/17155)
    -   MySQL クライアントへのログイン後の TiDBサーバーのバージョン情報の表示をサポート[#17187](https://github.com/pingcap/tidb/pull/17187)
    -   `GROUP_CONCAT`機能[#16990](https://github.com/pingcap/tidb/pull/16990)で`ORDER BY`節をサポート
    -   ステートメントがプラン キャッシュにヒットするかどうかを示すために、スロー ログに`Plan_from_cache`情報を表示するサポート[#17121](https://github.com/pingcap/tidb/pull/17121)
    -   TiDBダッシュボードにTiFlashマルチディスク展開の容量情報を表示できる機能を追加
    -   ダッシュボードで SQL ステートメントを使用してTiFlashログを照会する機能を追加します

-   TiKV

    -   tikv-ctl の暗号化デバッグをサポートし、暗号化storageが有効な場合にクラスターの操作と管理に tikv-ctl を使用できるようにします[#7698](https://github.com/tikv/tikv/pull/7698)
    -   スナップショットでのロックカラムファミリーの暗号化のサポート[#7712](https://github.com/tikv/tikv/pull/7712)
    -   Grafana ダッシュボードのヒートマップを使用してRaftstoreレイテンシーの概要を表示し、ジッターの問題をより適切に診断します[#7717](https://github.com/tikv/tikv/pull/7717)
    -   gRPC メッセージ[#7824](https://github.com/tikv/tikv/pull/7824)のサイズの上限設定をサポート
    -   Grafana ダッシュボードに暗号化関連の監視メトリクスを追加します[#7827](https://github.com/tikv/tikv/pull/7827)
    -   アプリケーション層プロトコル ネゴシエーション (ALPN) [#7825](https://github.com/tikv/tikv/pull/7825)をサポート
    -   タイタン[#7818](https://github.com/tikv/tikv/pull/7818)に関する統計をさらに追加する
    -   クライアントから提供されたタスク ID を統合読み取りプールの識別子として使用して、タスクの優先度が同じトランザクション内の別のタスクによって下げられるのを回避するためのサポート[#7814](https://github.com/tikv/tikv/pull/7814)
    -   `batch insert`要求[#7718](https://github.com/tikv/tikv/pull/7718)のパフォーマンスを改善する

-   PD

    -   ノードをオフラインにする際のピア削除の速度制限をなくす[#2372](https://github.com/pingcap/pd/pull/2372)

-   TiFlash

    -   Grafana の**Read Index**の Count グラフの名前を<strong>Ops</strong>に変更します
    -   システム負荷が低いときにファイル記述子を開くためのデータを最適化して、システム リソースの消費を削減します。
    -   容量関連の構成パラメータを追加して、データstorage容量を制限します

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctl に`fetch-mode`サブコマンドを追加して、TiKV クラスター モード[#287](https://github.com/pingcap/tidb-lightning/pull/287)を出力します。

    -   TiCDC

        -   `cdc cli` (changefeed) [#546](https://github.com/pingcap/tiflow/pull/546)を使用したレプリケーション タスクの管理のサポート

    -   バックアップと復元 (BR)

        -   バックアップ中の GC 時間の自動調整をサポート[#257](https://github.com/pingcap/br/pull/257)
        -   データを復元するときに PD パラメータを調整して復元を高速化する[#198](https://github.com/pingcap/br/pull/198)

## バグの修正 {#bug-fixes}

-   TiDB

    -   複数の演算子での式の実行にベクトル化を使用するかどうかを決定するロジックを改善します[#16383](https://github.com/pingcap/tidb/pull/16383)
    -   `IndexMerge`ヒントがデータベース名を正しくチェックできない問題を修正[#16932](https://github.com/pingcap/tidb/pull/16932)
    -   シーケンス オブジェクト[#17037](https://github.com/pingcap/tidb/pull/17037)の切り詰めを禁止する
    -   シーケンス オブジェクト[#16957](https://github.com/pingcap/tidb/pull/16957)で`INSERT` / `UPDATE` / `ANALYZE` / `DELETE`ステートメントを実行できる問題を修正します。
    -   ブートストラップ フェーズの内部 SQL ステートメントがステートメント サマリー テーブルで内部クエリとして正しくマークされない問題を修正します[#17062](https://github.com/pingcap/tidb/pull/17062)
    -   TiFlashではサポートされているが TiKV ではサポートされていないフィルター条件が`IndexLookupJoin`オペレーター[#17036](https://github.com/pingcap/tidb/pull/17036)にプッシュされると発生するエラーを修正します。
    -   照合順序が有効になった後に発生する可能性がある`LIKE`式の同時実行の問題を修正します[#16997](https://github.com/pingcap/tidb/pull/16997)
    -   照合順序が有効になった後、 `LIKE`関数が`Range`クエリ インデックスを正しく構築できないという問題を修正します[#16783](https://github.com/pingcap/tidb/pull/16783)
    -   `Plan Cache`ステートメントがトリガーされた後に`@@LAST_PLAN_FROM_CACHE`を実行すると、間違った値が返される問題を修正します[#16831](https://github.com/pingcap/tidb/pull/16831)
    -   `IndexMerge` [#16947](https://github.com/pingcap/tidb/pull/16947)の候補パスを計算するときに、インデックスの`TableFilter`欠落する問題を修正します
    -   `MergeJoin`ヒントを使用し、 `TableDual`演算子が存在する場合、物理クエリ プランを生成できない問題を修正します[#17016](https://github.com/pingcap/tidb/pull/17016)
    -   明細書の概要表の`Stmt_Type`列の値の間違った大文字化を修正します[#17018](https://github.com/pingcap/tidb/pull/17018)
    -   異なるユーザーが同じ`tmp-storage-path` [#16996](https://github.com/pingcap/tidb/pull/16996)を使用するとサービスを開始できず、 `Permission Denied`エラーが報告される問題を修正
    -   `CASE WHEN` [#16995](https://github.com/pingcap/tidb/pull/16995)などの複数の入力列によって結果の型が決定される式に対して、 `NotNullFlag`結果の型が正しく設定されない問題を修正します。
    -   ダーティ ストアが存在する場合、緑色の GC が未解決のロックを残す可能性がある問題を修正します[#16949](https://github.com/pingcap/tidb/pull/16949)
    -   複数の異なるロックを持つ 1 つのキーに遭遇したときに、緑色の GC が未解決のロックを残す可能性があるという問題を修正します[#16948](https://github.com/pingcap/tidb/pull/16948)
    -   サブクエリが親クエリ列を参照するため、 `INSERT VALUE`ステートメントに間違った値を挿入する問題を修正します[#16952](https://github.com/pingcap/tidb/pull/16952)
    -   `Float`値[#16666](https://github.com/pingcap/tidb/pull/16666)で`AND`演算子を使用すると、誤った結果が得られる問題を修正
    -   高価なログ[#16907](https://github.com/pingcap/tidb/pull/16907)の`WAIT_TIME`フィールドの誤った情報を修正します。
    -   悲観的トランザクション モード[#16897](https://github.com/pingcap/tidb/pull/16897)でスロー ログに`SELECT FOR UPDATE`ステートメントが記録されない問題を修正
    -   `Enum`または`Set`タイプ[#16892](https://github.com/pingcap/tidb/pull/16892)の列で`SELECT DISTINCT`実行したときに発生する誤った結果を修正します。
    -   `SHOW CREATE TABLE`ステートメント[#16864](https://github.com/pingcap/tidb/pull/16864)の`auto_random_base`の表示エラーを修正
    -   `WHERE`節[#16559](https://github.com/pingcap/tidb/pull/16559)の誤った値`string_value`修正します。
    -   `GROUP BY`ウィンドウ関数のエラー メッセージが MySQL [#16165](https://github.com/pingcap/tidb/pull/16165)のエラー メッセージと一致しない問題を修正
    -   データベース名に大文字の[#17167](https://github.com/pingcap/tidb/pull/17167)が含まれている場合、 `FLASH TABLE`ステートメントの実行に失敗する問題を修正します。
    -   Projection executor [#17118](https://github.com/pingcap/tidb/pull/17118)の不正確なメモリトレースを修正します。
    -   異なるタイム ゾーンでの`SLOW_QUERY`テーブルの不適切な時間フィルタリングの問題を修正します[#17164](https://github.com/pingcap/tidb/pull/17164)
    -   仮想生成列[#17126](https://github.com/pingcap/tidb/pull/17126)で`IndexMerge`を使用すると発生するpanicの問題を修正します。
    -   `INSTR`および`LOCATE`関数の大文字化の問題を修正[#17068](https://github.com/pingcap/tidb/pull/17068)
    -   `tidb_allow_batch_cop`構成を有効にした後、 `tikv server timeout`エラーが頻繁に報告される問題を修正[#17161](https://github.com/pingcap/tidb/pull/17161)
    -   Float 型で`XOR`の操作を実行した結果が MySQL 8.0 の結果と一致しない問題を修正[#16978](https://github.com/pingcap/tidb/pull/16978)
    -   サポートされていない`ALTER TABLE REORGANIZE PARTITION`ステートメントを実行したときにエラーが報告されない問題を修正します[#17178](https://github.com/pingcap/tidb/pull/17178)
    -   `EXPLAIN FORMAT="dot"  FOR CONNECTION ID`サポートされていないプランに遭遇したときにエラーが報告される問題を修正します[#17160](https://github.com/pingcap/tidb/pull/17160)
    -   明細書の要約表の`EXEC_COUNT`列にあるプリペアドステートメントのレコードの問題を修正します[#17086](https://github.com/pingcap/tidb/pull/17086)
    -   Statement Summary システム変数[#17129](https://github.com/pingcap/tidb/pull/17129)を設定すると、値が検証されない問題を修正します。
    -   プラン キャッシュが有効な場合にオーバーフロー値を使用して`UNSIGNED BIGINT`主キーをクエリすると、エラーが報告される問題を修正します[#17120](https://github.com/pingcap/tidb/pull/17120)
    -   Grafana **TiDB サマリー**ダッシュボードのマシン インスタンスとリクエスト タイプによる誤った QPS 表示を修正します[#17105](https://github.com/pingcap/tidb/pull/17105)

-   TiKV

    -   復元後に空のリージョンが多数生成される問題を修正[#7632](https://github.com/tikv/tikv/pull/7632)
    -   順不同の読み取りインデックス応答を受信したときのRaftstoreのpanic問題を修正します[#7370](https://github.com/tikv/tikv/pull/7370)
    -   統合スレッド プールが有効になっている場合に、無効なstorageまたはコプロセッサの読み取りプール構成が拒否されない可能性がある問題を修正します[#7513](https://github.com/tikv/tikv/pull/7513)
    -   `join` TiKVサーバーがシャットダウンされたときの操作のpanicの問題を修正します[#7713](https://github.com/tikv/tikv/pull/7713)
    -   診断 API [#7776](https://github.com/tikv/tikv/pull/7776)を介して TiKV スロー ログを検索すると、結果が返されない問題を修正します。
    -   TiKV ノードを長時間実行すると、顕著なメモリの断片化が発生する問題を修正します[#7556](https://github.com/tikv/tikv/pull/7556)
    -   無効な日付が格納されている場合に SQL ステートメントの実行に失敗する問題を修正します[#7268](https://github.com/tikv/tikv/pull/7268)
    -   GCS [#7739](https://github.com/tikv/tikv/pull/7739)からバックアップ データを復元できない問題を修正
    -   保管時の暗号化中に KMS キー ID が検証されない問題を修正します[#7719](https://github.com/tikv/tikv/pull/7719)
    -   異なるアーキテクチャのコンパイラーにおけるコプロセッサーの根本的な正確性の問題を修正します[#7714](https://github.com/tikv/tikv/pull/7714) [#7730](https://github.com/tikv/tikv/pull/7730)
    -   暗号化が有効な場合の`snapshot ingestion`エラーを修正[#7815](https://github.com/tikv/tikv/pull/7815)
    -   `Invalid cross-device link`設定ファイル書き換え時のエラーを修正[#7817](https://github.com/tikv/tikv/pull/7817)
    -   構成ファイルを空のファイルに書き込むときの間違った toml 形式の問題を修正します[#7817](https://github.com/tikv/tikv/pull/7817)
    -   Raftstoreで破棄されたピアが引き続きリクエストを処理できる問題を修正します[#7836](https://github.com/tikv/tikv/pull/7836)

-   PD

    -   pd-ctl [#2399](https://github.com/pingcap/pd/pull/2399)で`region key`コマンドを使用するときに発生する`404`問題を修正します。
    -   TSO および ID 割り当てのモニター メトリックが Grafana ダッシュボードから欠落している問題を修正します[#2405](https://github.com/pingcap/pd/pull/2405)
    -   pd-recover が Docker イメージに含まれていない問題を修正します[#2406](https://github.com/pingcap/pd/pull/2406)
    -   データ ディレクトリのパスを絶対パスに解析して、TiDB ダッシュボードが PD 情報を正しく表示しない可能性がある問題を修正します[#2420](https://github.com/pingcap/pd/pull/2420)
    -   pd-ctl [#2416](https://github.com/pingcap/pd/pull/2416)で`scheduler config shuffle-region-scheduler`コマンドを使用するとデフォルト出力がない問題を修正

-   TiFlash

    -   一部のシナリオで使用済み容量の間違った情報が報告される問題を修正

-   ツール

    -   TiDBBinlog

        -   ダウンストリームが Kafka [#962](https://github.com/pingcap/tidb-binlog/pull/962)の場合、 `mediumint`型のデータが処理されない問題を修正
        -   DDL のデータベース名がキーワード[#961](https://github.com/pingcap/tidb-binlog/pull/961)の場合、reparo が DDL ステートメントの解析に失敗する問題を修正します。

    -   TiCDC

        -   `TZ`環境変数が設定されていない場合に間違ったタイム ゾーンを使用する問題を修正します[#512](https://github.com/pingcap/tiflow/pull/512)

        -   一部のエラーが正しく処理されないため、サーバーの終了時に所有者がリソースをクリーンアップしないという問題を修正します[#528](https://github.com/pingcap/tiflow/pull/528)

        -   TiKV [#531](https://github.com/pingcap/tiflow/pull/531)に再接続すると TiCDC がスタックする問題を修正

        -   テーブル スキーマを初期化するときのメモリ使用量を最適化します[#534](https://github.com/pingcap/tiflow/pull/534)

        -   `watch`モードを使用してレプリケーション ステータスの変化を監視し、準リアルタイムの更新を実行してレプリケーションの遅延を減らします[#481](https://github.com/pingcap/tiflow/pull/481)

    <!---->

    -   バックアップと復元 (BR)

        -   BR が`auto_random`属性[#241](https://github.com/pingcap/br/issues/241)を持つテーブルを復元した後、データを挿入すると`duplicate entry`エラーがトリガーされる可能性がある問題を修正します。
