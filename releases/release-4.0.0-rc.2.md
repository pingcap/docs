---
title: TiDB 4.0 RC.2 Release Notes
summary: TiDB 4.0 RC.2は2020年5月15日にリリースされました。このリリースには、TiDB、TiKV、PD、 TiFlash、およびさまざまなツールの互換性の変更、重要なバグ修正、新機能、バグ修正が含まれています。注目すべき変更点としては、TiDB Binlogが有効になっている場合の単一トランザクションのサイズ制限の削除、BACKUPおよびRESTOREコマンドのサポート、Grafanaダッシュボードへの暗号化関連の監視メトリックの追加などがあります。さらに、パーティションの選択ミス、インデックス範囲の構築ミス、パフォーマンスの低下などの問題に対する多数のバグ修正も行われています。このリリースでは、CREATE TABLEステートメントでのauto_randomオプションのサポートや、cdc cliを使用したレプリケーションタスクの管理機能などの新機能も導入されています。
---

# TiDB 4.0 RC.2 リリースノート {#tidb-4-0-rc-2-release-notes}

発売日：2020年5月15日

TiDB バージョン: 4.0.0-rc.2

## 互換性の変更 {#compatibility-changes}

-   TiDB

    -   TiDB Binlogが有効な場合、単一トランザクションのサイズ制限（100 MB）が削除されました。現在、トランザクションのサイズ制限は 10 GB です。ただし、TiDB Binlogが有効で、ダウンストリームが Kafka の場合は、Kafka のメッセージサイズ制限である 1 GB に合わせて`txn-total-size-limit`パラメータを設定してください。 [＃16941](https://github.com/pingcap/tidb/pull/16941)
    -   `CLUSTER_LOG`テーブル照会するときに時間範囲が指定されていない場合は、デフォルトの時間範囲を照会するのではなく、エラーを返して指定された時間範囲を要求するように動作を変更します。 [＃17003](https://github.com/pingcap/tidb/pull/17003)
    -   `CREATE TABLE`ステートメントを使用してパーティションテーブルを作成するときに、サポートされていない`sub-partition`または`linear hash`オプションが指定された場合、オプションが無視されたパーティションテーブルではなく、通常のテーブルが作成されます[＃17197](https://github.com/pingcap/tidb/pull/17197)

-   TiKV

    -   暗号化関連の設定をセキュリティ関連の設定に移動します。つまり、TiKV設定ファイルの`[encryption]` `[security.encryption]` に変更します。 [＃7810](https://github.com/tikv/tikv/pull/7810)

-   ツール

    -   TiDB Lightning

        -   互換性を向上させるために、データをインポートするときにデフォルトのSQLモードを`ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER`に変更します[＃316](https://github.com/pingcap/tidb-lightning/pull/316)
        -   tidb-backend モードで PD または TiKV ポートへのアクセスを禁止する [＃312](https://github.com/pingcap/tidb-lightning/pull/312)
        -   ログ情報をデフォルトでtmpファイルに出力し、 TiDB Lightningの起動時にtmpファイルのパスを出力します[＃313](https://github.com/pingcap/tidb-lightning/pull/313)

## 重要なバグ修正 {#important-bug-fixes}

-   TiDB

    -   `WHERE`句に同等の条件が 1 つしかない場合に間違ったパーティションが選択される問題を修正[＃17054](https://github.com/pingcap/tidb/pull/17054)
    -   `WHERE`句に文字列列のみが含まれている場合に誤ったインデックス範囲を構築することで誤った結果が発生する問題を修正しました。 [＃16660](https://github.com/pingcap/tidb/pull/16660)
    -   `DELETE`操作後にトランザクション内の`PointGet`クエリを実行するときに発生するpanic問題を修正しました [＃16991](https://github.com/pingcap/tidb/pull/16991)
    -   エラーが発生したときにGCワーカーがデッドロックに遭遇する可能性がある問題を修正しました[＃16915](https://github.com/pingcap/tidb/pull/16915)
    -   TiKVの応答が遅いがダウンしていない場合に不要なRegionMissの再試行を回避する[＃16956](https://github.com/pingcap/tidb/pull/16956)
    -   MySQLプロトコルのハンドシェイクフェーズでクライアントのログレベルを`DEBUG`に変更して、ログ出力を妨げる問題を解決します。 [＃16881](https://github.com/pingcap/tidb/pull/16881)
    -   `TRUNCATE`操作後に、テーブルで定義された`PRE_SPLIT_REGIONS`情報に従ってリージョンが事前に分割されない問題を修正しました。 [＃16776](https://github.com/pingcap/tidb/pull/16776)
    -   2 フェーズコミットの 2 番目のフェーズで TiKV が利用できない場合に再試行によって発生するゴルーチンの急上昇の問題を修正しました[＃16876](https://github.com/pingcap/tidb/pull/16876)
    -   一部の式をプッシュダウンできない場合のステートメント実行のpanic問題を修正[＃16869](https://github.com/pingcap/tidb/pull/16869)
    -   パーティションテーブルでのIndexMerge操作の誤った実行結果を修正 [＃17124](https://github.com/pingcap/tidb/pull/17124)
    -   メモリトラッカーのミューテックスの競合によって引き起こされる`wide_table`のパフォーマンス低下を修正しました [＃17234](https://github.com/pingcap/tidb/pull/17234)

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、アップグレード後にシステムが正常に起動できない問題を修正しました。

## 新機能 {#new-features}

-   TiDB

    -   データのバックアップと復元のためのコマンド`BACKUP`と`RESTORE`サポートを追加[＃16960](https://github.com/pingcap/tidb/pull/16960)
    -   コミット前に単一リージョン内のデータ量を事前チェックし、データ量がしきい値を超えた場合にリージョンを事前分割する機能をサポートします。 [＃16959](https://github.com/pingcap/tidb/pull/16959)
    -   最後に実行されたステートメントがプランキャッシュにヒットしたかどうかを示す、スコープ`Session`を持つ新しい`LAST_PLAN_FROM_CACHE`変数を追加します。 [＃16830](https://github.com/pingcap/tidb/pull/16830)
    -   スローログと`SLOW_LOG` の`Cop_time`情報を記録することをサポート [＃16904](https://github.com/pingcap/tidb/pull/16904)
    -   Grafana に Go Runtime のメモリ状態を監視するメトリクスを追加します [＃16928](https://github.com/pingcap/tidb/pull/16928)
    -   一般ログに`forUpdateTS`および`Read Consistency`分離レベル情報を出力することをサポート [＃16946](https://github.com/pingcap/tidb/pull/16946)
    -   TiKVリージョンでのロック解決の重複リクエストの折りたたみをサポート [＃16925](https://github.com/pingcap/tidb/pull/16925)
    -   `SET CONFIG`ステートメントを使用して PD/TiKV ノードの構成を変更することをサポートします [＃16853](https://github.com/pingcap/tidb/pull/16853)
    -   `CREATE TABLE`の文の`auto_random`オプションをサポートする[＃16813](https://github.com/pingcap/tidb/pull/16813)
    -   TiKV がリクエストをより適切にスケジュールして処理できるように、DistSQL リクエストに TaskID を割り当てます[＃17155](https://github.com/pingcap/tidb/pull/17155)
    -   MySQLクライアントにログインした後、TiDBサーバーのバージョン情報を表示する機能をサポート [＃17187](https://github.com/pingcap/tidb/pull/17187)
    -   `GROUP_CONCAT`関数の`ORDER BY`句をサポートする [＃16990](https://github.com/pingcap/tidb/pull/16990)
    -   スローログに`Plan_from_cache`情報を表示して、ステートメントがプラン キャッシュにヒットしたかどうかを示すことをサポート [＃17121](https://github.com/pingcap/tidb/pull/17121)
    -   TiDB DashboardにTiFlashマルチディスク構成の容量情報を表示できる機能を追加
    -   ダッシュボードでSQL文を使用してTiFlashログを照会する機能を追加

-   TiKV

    -   tikv-ctl の暗号化デバッグをサポートし、暗号化ストレージが有効な場合に tikv-ctl を使用してクラスターを操作および管理できるようになりました[＃7698](https://github.com/tikv/tikv/pull/7698)
    -   スナップショットのロックカラムファミリーの暗号化をサポート [＃7712](https://github.com/tikv/tikv/pull/7712)
    -   Grafanaダッシュボードのヒートマップを使用して、 Raftstoreのレイテンシーサマリーを表示し、ジッターの問題をより適切に診断します[＃7717](https://github.com/tikv/tikv/pull/7717)
    -   gRPC メッセージのサイズの上限設定をサポート[＃7824](https://github.com/tikv/tikv/pull/7824)
    -   Grafanaダッシュボードに暗号化関連の監視メトリクス追加する [＃7827](https://github.com/tikv/tikv/pull/7827)
    -   アプリケーション層プロトコルネゴシエーション（ALPN） サポート [＃7825](https://github.com/tikv/tikv/pull/7825)
    -   Titan に関する統計情報を追加する [＃7818](https://github.com/tikv/tikv/pull/7818)
    -   同じトランザクション内の別のタスクによってタスクの優先度が下げられるのを回避するために、クライアントによって提供されたタスクIDを統合読み取りプールの識別子として使用することをサポートします[＃7814](https://github.com/tikv/tikv/pull/7814)
    -   `batch insert`リクエストのパフォーマンスを向上させる [＃7718](https://github.com/tikv/tikv/pull/7718)

-   PD

    -   ノードをオフラインにするときにピアを削除する際の速度制限を排除[＃2372](https://github.com/pingcap/pd/pull/2372)

-   TiFlash

    -   Grafanaの**Read Index**のCountグラフの名前を**Ops**に変更します
    -   システム負荷が低いときにファイル記述子を開くためのデータを最適化して、システムリソースの消費を削減します。
    -   データストレージ容量を制限するために容量関連の設定パラメータを追加します

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctlに`fetch-mode`サブコマンドを追加して、TiKVクラスタモード印刷します。 [＃287](https://github.com/pingcap/tidb-lightning/pull/287)

    -   TiCDC

        -   `cdc cli` (changefeed) を使用してレプリケーションタスクの管理をサポート [＃546](https://github.com/pingcap/tiflow/pull/546)

    -   Backup & Restore (BR)

        -   バックアップ中のGC時間の自動調整をサポート[＃257](https://github.com/pingcap/br/pull/257)
        -   データの復元時にPDパラメータを調整して復元を高速化します[＃198](https://github.com/pingcap/br/pull/198)

## バグ修正 {#bug-fixes}

-   TiDB

    -   複数の演算子での式実行にベクトル化を使用するかどうかを決定するロジックを改善 [＃16383](https://github.com/pingcap/tidb/pull/16383)
    -   `IndexMerge`ヒントがデータベース名を正しくチェックできない問題を修正[＃16932](https://github.com/pingcap/tidb/pull/16932)
    -   シーケンスオブジェクト切り捨てを禁止する [＃17037](https://github.com/pingcap/tidb/pull/17037)
    -   `INSERT` / `UPDATE` / `ANALYZE` / `DELETE`ステートメントがシーケンスオブジェクトで実行できる問題を修正しました [＃16957](https://github.com/pingcap/tidb/pull/16957)
    -   ブートストラップフェーズの内部SQL文がステートメントサマリーテーブルで内部クエリとして正しくマークされない問題を修正しました。 [＃17062](https://github.com/pingcap/tidb/pull/17062)
    -   TiFlashではサポートされているがTiKVではサポートされていないフィルタ条件が`IndexLookupJoin`演算子にプッシュダウンされたときに発生するエラーを修正しました [＃17036](https://github.com/pingcap/tidb/pull/17036)
    -   照合順序が有効になった後に発生する可能性のある`LIKE`の同時実行の問題を修正[＃16997](https://github.com/pingcap/tidb/pull/16997)
    -   照合順序が有効になった後、 `LIKE`関数が`Range`クエリインデックスを正しく構築できない問題を修正しました[＃16783](https://github.com/pingcap/tidb/pull/16783)
    -   `Plan Cache`文がトリガーされた後に`@@LAST_PLAN_FROM_CACHE`実行すると間違った値が返される問題を修正[＃16831](https://github.com/pingcap/tidb/pull/16831)
    -   `IndexMerge` の候補パスを計算するときにインデックスの`TableFilter`失われる問題を修正しました [＃16947](https://github.com/pingcap/tidb/pull/16947)
    -   `MergeJoin`ヒントを使用し、 `TableDual`演算子が存在する場合に物理クエリプランを生成できない問題を修正しました[＃17016](https://github.com/pingcap/tidb/pull/17016)
    -   ステートメントサマリーテーブルの`Stmt_Type`列の値の大文字と小文字の誤りを修正しました。 [＃17018](https://github.com/pingcap/tidb/pull/17018)
    -   異なるユーザーが同じ`tmp-storage-path` を使用するとサービスを開始できないため、 `Permission Denied`エラーが報告される問題を修正しました。 [＃16996](https://github.com/pingcap/tidb/pull/16996)
    -   結果の型が`CASE WHEN` などの複数の入力列によって決定される式に対して、 `NotNullFlag`結果の型が誤って設定される問題を修正しました。 [＃16995](https://github.com/pingcap/tidb/pull/16995)
    -   ダーティストアが存在する場合にグリーンGCが未解決のロックを残す可能性がある問題を修正[＃16949](https://github.com/pingcap/tidb/pull/16949)
    -   複数の異なるロックを持つ単一のキーに遭遇したときに、グリーンGCが未解決のロックを残す可能性がある問題を修正しました[＃16948](https://github.com/pingcap/tidb/pull/16948)
    -   サブクエリが親クエリ列を参照しているため、 `INSERT VALUE`ステートメントに間違った値が挿入される問題を修正しました。 [＃16952](https://github.com/pingcap/tidb/pull/16952)
    -   `Float`値に`AND`演算子を使用したときに誤った結果が出る問題を修正しました [＃16666](https://github.com/pingcap/tidb/pull/16666)
    -   高価なログの`WAIT_TIME`フィールドの誤った情報を修正 [＃16907](https://github.com/pingcap/tidb/pull/16907)
    -   悲観的トランザクションモードで`SELECT FOR UPDATE`文がスローログに記録できない問題を修正 [＃16897](https://github.com/pingcap/tidb/pull/16897)
    -   `Enum`または`Set`タイプの列で`SELECT DISTINCT`実行したときに発生する誤った結果を修正[＃16892](https://github.com/pingcap/tidb/pull/16892)
    -   `SHOW CREATE TABLE`文の`auto_random_base`の表示エラーを修正 [＃16864](https://github.com/pingcap/tidb/pull/16864)
    -   `WHERE`句の`string_value`の誤った値を修正する [＃16559](https://github.com/pingcap/tidb/pull/16559)
    -   `GROUP BY`ウィンドウ関数のエラーメッセージがMySQL と一致しない問題を修正しました [＃16165](https://github.com/pingcap/tidb/pull/16165)
    -   データベース名に大文字の含まれている場合に`FLASH TABLE`文の実行が失敗する問題を修正しました [＃17167](https://github.com/pingcap/tidb/pull/17167)
    -   投影実行プログラムの不正確なメモリトレースを修正しました [＃17118](https://github.com/pingcap/tidb/pull/17118)
    -   異なるタイムゾーンの`SLOW_QUERY`テーブルで時間フィルタリングが正しく行われない問題を修正しました[＃17164](https://github.com/pingcap/tidb/pull/17164)
    -   仮想生成列で`IndexMerge`が使用された場合に発生するpanic問題を修正 [＃17126](https://github.com/pingcap/tidb/pull/17126)
    -   `INSTR`と`LOCATE`関数の大文字化の問題を修正 [＃17068](https://github.com/pingcap/tidb/pull/17068)
    -   `tidb_allow_batch_cop`構成を有効にした後に`tikv server timeout`エラーが頻繁に報告される問題を修正[＃17161](https://github.com/pingcap/tidb/pull/17161)
    -   Float型に対して`XOR`演算を実行した結果がMySQL 8.0 と一致しない問題を修正 [＃16978](https://github.com/pingcap/tidb/pull/16978)
    -   サポートされていない`ALTER TABLE REORGANIZE PARTITION`文が実行されてもエラーが報告されない問題を修正[＃17178](https://github.com/pingcap/tidb/pull/17178)
    -   `EXPLAIN FORMAT="dot"  FOR CONNECTION ID`サポートされていないプランに遭遇したときにエラーが報告される問題を修正[＃17160](https://github.com/pingcap/tidb/pull/17160)
    -   ステートメントサマリーテーブルの`EXEC_COUNT`列にあるプリペアドステートメントのレコードの問題を修正しました。 [＃17086](https://github.com/pingcap/tidb/pull/17086)
    -   ステートメントサマリーシステム変数を設定するときに値が検証されない問題を修正しました [＃17129](https://github.com/pingcap/tidb/pull/17129)
    -   プランキャッシュが有効な場合に、オーバーフロー値を使用して`UNSIGNED BIGINT`主キーをクエリするとエラーが報告される問題を修正しました[＃17120](https://github.com/pingcap/tidb/pull/17120)
    -   Grafana **TiDB サマリーダッシュ**ボードで、マシンインスタンスとリクエストタイプによる QPS 表示が誤っていた問題を修正しました。 [＃17105](https://github.com/pingcap/tidb/pull/17105)

-   TiKV

    -   復元後に多くの空のリージョンが生成される問題を修正[＃7632](https://github.com/tikv/tikv/pull/7632)
    -   順序がずれたインデックス読み取り応答を受け取ったときにRaftstoreがpanic問題を修正[＃7370](https://github.com/tikv/tikv/pull/7370)
    -   統合スレッドプールが有効な場合に、無効なstorageまたはコプロセッサ読み取りプール構成が拒否されない可能性がある問題を修正しました[＃7513](https://github.com/tikv/tikv/pull/7513)
    -   TiKVサーバーがシャットダウンされたときの`join`操作のpanic問題を修正しました[＃7713](https://github.com/tikv/tikv/pull/7713)
    -   診断API 経由でTiKVスローログを検索しても結果が返されない問題を修正 [＃7776](https://github.com/tikv/tikv/pull/7776)
    -   TiKVノードが長時間実行されると顕著なメモリ断片化が発生する問題を修正[＃7556](https://github.com/tikv/tikv/pull/7556)
    -   無効な日付が格納されている場合にSQL文の実行が失敗する問題を修正[＃7268](https://github.com/tikv/tikv/pull/7268)
    -   GCS からバックアップデータを復元できない問題を修正 [＃7739](https://github.com/tikv/tikv/pull/7739)
    -   保存時の暗号化中にKMSキーIDが検証されない問題を修正[＃7719](https://github.com/tikv/tikv/pull/7719)
    -   異なるアーキテクチャのコンパイラにおけるコプロセッサーの根本的な正確性の問題を修正[＃7714](https://github.com/tikv/tikv/pull/7714) [＃7730](https://github.com/tikv/tikv/pull/7730)
    -   暗号化が有効になっている場合の`snapshot ingestion`エラーを修正[＃7815](https://github.com/tikv/tikv/pull/7815)
    -   設定ファイル書き換え時に発生する`Invalid cross-device link`エラーを修正 [＃7817](https://github.com/tikv/tikv/pull/7817)
    -   設定ファイルを空のファイルに書き込むときに間違った toml 形式になる問題を修正しました[＃7817](https://github.com/tikv/tikv/pull/7817)
    -   Raftstoreで破棄されたピアがリクエストを処理できる問題を修正[＃7836](https://github.com/tikv/tikv/pull/7836)

-   PD

    -   pd-ctl の`region key`コマンドを使用するときに発生する`404`問題を修正しました [＃2399](https://github.com/pingcap/pd/pull/2399)
    -   TSOとID割り当てのモニターメトリックがGrafanaダッシュボードに表示されない問題を修正 [＃2405](https://github.com/pingcap/pd/pull/2405)
    -   pd-recoverがDockerイメージに含まれていない問題を修正 [＃2406](https://github.com/pingcap/pd/pull/2406)
    -   データディレクトリのパスを絶対パスに解析して、TiDB DashboardにPD情報が正しく表示されない問題を修正しました[＃2420](https://github.com/pingcap/pd/pull/2420)
    -   pd-ctl で`scheduler config shuffle-region-scheduler`コマンドを使用したときにデフォルトの出力がない問題を修正しました [＃2416](https://github.com/pingcap/pd/pull/2416)

-   TiFlash

    -   一部のシナリオで使用容量の情報が誤って報告される問題を修正しました

-   ツール

    -   TiDB Binlog

        -   ダウンストリームがKafka 場合に`mediumint`型のデータが処理されない問題を修正 [＃962](https://github.com/pingcap/tidb-binlog/pull/962)
        -   DDL内のデータベース名がキーワード場合にreparoがDDL文の解析に失敗する問題を修正しました [＃961](https://github.com/pingcap/tidb-binlog/pull/961)

    -   TiCDC

        -   `TZ`環境変数が設定されていない場合に間違ったタイムゾーンが使用される問題を修正[＃512](https://github.com/pingcap/tiflow/pull/512)

        -   いくつかのエラーが正しく処理されないため、サーバーが終了したときに所有者がリソースをクリーンアップしない問題を修正しました[＃528](https://github.com/pingcap/tiflow/pull/528)

        -   TiKV に再接続するときにTiCDCが停止する可能性がある問題を修正しました [＃531](https://github.com/pingcap/tiflow/pull/531)

        -   テーブルスキーマ初期化時にメモリ使用量を最適化する [＃534](https://github.com/pingcap/tiflow/pull/534)

        -   `watch`モードを使用してレプリケーションステータスの変化を監視し、準リアルタイム更新を実行してレプリケーション遅延を削減します[＃481](https://github.com/pingcap/tiflow/pull/481)

    <!---->

    -   Backup & Restore (BR)

        -   BRが`auto_random`属性を持つテーブルを復元した後にデータを挿入すると`duplicate entry`エラーが発生する可能性がある問題を修正しました。 [＃241](https://github.com/pingcap/br/issues/241)
