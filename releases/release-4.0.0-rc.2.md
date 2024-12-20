---
title: TiDB 4.0 RC.2 Release Notes
summary: TiDB 4.0 RC.2 は、2020 年 5 月 15 日にリリースされました。このリリースには、TiDB、TiKV、PD、 TiFlash、およびさまざまなツールの互換性の変更、重要なバグ修正、新機能、バグ修正が含まれています。注目すべき変更点としては、TiDB Binlogが有効になっている場合の単一トランザクションのサイズ制限の削除、BACKUP コマンドと RESTORE コマンドのサポート、Grafana ダッシュボードへの暗号化関連の監視メトリックの追加などがあります。さらに、パーティションの選択ミス、インデックス範囲の構築ミス、パフォーマンスの低下などの問題に対する多数のバグ修正もあります。このリリースでは、CREATE TABLE ステートメントでの auto_random オプションのサポートや、cdc cli を使用してレプリケーション タスクを管理する機能などの新機能も導入されています。
---

# TiDB 4.0 RC.2 リリースノート {#tidb-4-0-rc-2-release-notes}

発売日: 2020年5月15日

TiDB バージョン: 4.0.0-rc.2

## 互換性の変更 {#compatibility-changes}

-   ティビ

    -   TiDB Binlogが有効な場合、単一トランザクションのサイズ制限 (100 MB) を削除します。現在、トランザクションのサイズ制限は 10 GB です。ただし、TiDB Binlogが有効で、ダウンストリームが Kafka の場合は、Kafka [＃16941](https://github.com/pingcap/tidb/pull/16941)のメッセージ サイズ制限 1 GB に従って`txn-total-size-limit`パラメータを設定します。
    -   `CLUSTER_LOG`テーブル[＃17003](https://github.com/pingcap/tidb/pull/17003)を照会するときに時間範囲が指定されていない場合は、デフォルトの時間範囲を照会するのではなく、エラーを返して指定された時間範囲を要求するように動作を変更します。
    -   `CREATE TABLE`ステートメントを使用してパーティションテーブルを作成するときに、サポートされていない`sub-partition`または`linear hash`オプションが指定された場合、オプションが無視されたパーティションテーブルではなく、通常のテーブルが作成されます[＃17197](https://github.com/pingcap/tidb/pull/17197)

-   ティクヴ

    -   暗号化関連の設定をセキュリティ関連の設定に移動します。つまり、TiKV設定ファイルの`[encryption]` `[security.encryption]` [＃7810](https://github.com/tikv/tikv/pull/7810)に変更します。

-   ツール

    -   TiDB Lightning

        -   互換性を向上させるために、データをインポートするときにデフォルトのSQLモードを`ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER`に変更します[＃316](https://github.com/pingcap/tidb-lightning/pull/316)
        -   tidb-backend モード[＃312](https://github.com/pingcap/tidb-lightning/pull/312)で PD または TiKV ポートへのアクセスを禁止する
        -   ログ情報をデフォルトでtmpファイルに出力し、 TiDB Lightningの起動時にtmpファイルのパスを出力します[＃313](https://github.com/pingcap/tidb-lightning/pull/313)

## 重要なバグ修正 {#important-bug-fixes}

-   ティビ

    -   `WHERE`節に同等の条件が 1 つしかない場合に間違ったパーティションが選択される問題を修正[＃17054](https://github.com/pingcap/tidb/pull/17054)
    -   `WHERE`句に文字列列[＃16660](https://github.com/pingcap/tidb/pull/16660)のみが含まれている場合に、誤ったインデックス範囲を構築することで誤った結果が発生する問題を修正しました。
    -   `DELETE`操作[＃16991](https://github.com/pingcap/tidb/pull/16991)後にトランザクション内の`PointGet`クエリを実行するときに発生するpanic問題を修正
    -   エラーが発生したときにGCワーカーがデッドロックに遭遇する可能性がある問題を修正[＃16915](https://github.com/pingcap/tidb/pull/16915)
    -   TiKV 応答が遅いがダウンしていない場合に、不要な RegionMiss 再試行を回避する[＃16956](https://github.com/pingcap/tidb/pull/16956)
    -   MySQLプロトコルのハンドシェイクフェーズでクライアントのログレベルを`DEBUG`に変更して、ログ出力[＃16881](https://github.com/pingcap/tidb/pull/16881)を妨げる問題を解決します。
    -   `TRUNCATE`操作[＃16776](https://github.com/pingcap/tidb/pull/16776)の後に、テーブルで定義された`PRE_SPLIT_REGIONS`情報に従ってリージョンが事前に分割されない問題を修正しました。
    -   2 フェーズコミット[＃16876](https://github.com/pingcap/tidb/pull/16876)の 2 番目のフェーズで TiKV が利用できない場合に再試行によって発生するゴルーチンの急上昇の問題を修正しました。
    -   一部の式をプッシュダウンできない場合のステートメント実行のpanic問題を修正[＃16869](https://github.com/pingcap/tidb/pull/16869)
    -   パーティションテーブル[＃17124](https://github.com/pingcap/tidb/pull/17124)での IndexMerge 操作の誤った実行結果を修正
    -   メモリトラッカー[＃17234](https://github.com/pingcap/tidb/pull/17234)のミューテックスの競合によって発生する`wide_table`のパフォーマンス低下を修正

-   TiFlash

    -   データベースまたはテーブルの名前に特殊文字が含まれている場合、アップグレード後にシステムが正常に起動できない問題を修正しました。

## 新機能 {#new-features}

-   ティビ

    -   データのバックアップと復元のためのコマンド`BACKUP`と`RESTORE`のサポートを追加[＃16960](https://github.com/pingcap/tidb/pull/16960)
    -   コミット前に単一リージョン内のデータ量を事前チェックし、データ量がしきい値[＃16959](https://github.com/pingcap/tidb/pull/16959)を超えた場合にリージョンを事前分割する機能をサポートします。
    -   最後に実行されたステートメントがプランキャッシュ[＃16830](https://github.com/pingcap/tidb/pull/16830)にヒットしたかどうかを示すために、スコープ`Session`を持つ新しい`LAST_PLAN_FROM_CACHE`変数を追加します。
    -   スローログと[＃16904](https://github.com/pingcap/tidb/pull/16904) `SLOW_LOG` `Cop_time`情報を記録することをサポート
    -   Go Runtime [＃16928](https://github.com/pingcap/tidb/pull/16928)のメモリ状態を監視するメトリクスを Grafana に追加する
    -   一般ログ[＃16946](https://github.com/pingcap/tidb/pull/16946)に`forUpdateTS`および`Read Consistency`分離レベル情報を出力することをサポート
    -   TiKVリージョン[＃16925](https://github.com/pingcap/tidb/pull/16925)でのロック解決の重複リクエストの折りたたみをサポート
    -   `SET CONFIG`ステートメントを使用して PD/TiKV ノード[＃16853](https://github.com/pingcap/tidb/pull/16853)の構成を変更することをサポートします。
    -   `CREATE TABLE`文[＃16813](https://github.com/pingcap/tidb/pull/16813)の`auto_random`オプションを支持する
    -   TiKV がリクエストをより適切にスケジュールおよび処理できるように、DistSQL リクエストに TaskID を割り当てます[＃17155](https://github.com/pingcap/tidb/pull/17155)
    -   MySQLクライアントにログインした後、TiDBサーバーのバージョン情報を表示する機能をサポート[＃17187](https://github.com/pingcap/tidb/pull/17187)
    -   `GROUP_CONCAT`関数[＃16990](https://github.com/pingcap/tidb/pull/16990)の`ORDER BY`節をサポートする
    -   スローログに`Plan_from_cache`情報を表示して、ステートメントがプラン キャッシュ[＃17121](https://github.com/pingcap/tidb/pull/17121)にヒットしたかどうかを示す機能をサポートします。
    -   TiDBダッシュボードにTiFlashマルチディスク展開の容量情報を表示できる機能を追加
    -   ダッシュボードでSQL文を使用してTiFlashログを照会する機能を追加

-   ティクヴ

    -   tikv-ctl の暗号化デバッグをサポートし、暗号化storageが有効な場合に tikv-ctl を使用してクラスターを操作および管理できるようにします[＃7698](https://github.com/tikv/tikv/pull/7698)
    -   スナップショット[＃7712](https://github.com/tikv/tikv/pull/7712)のロックカラムファミリーの暗号化をサポート
    -   Grafanaダッシュボードのヒートマップを使用してRaftstoreのレイテンシーの概要を確認し、ジッターの問題をより適切に診断します[＃7717](https://github.com/tikv/tikv/pull/7717)
    -   gRPC メッセージのサイズの上限設定をサポート[＃7824](https://github.com/tikv/tikv/pull/7824)
    -   Grafanaダッシュボードに暗号化関連の監視メトリックを追加する[＃7827](https://github.com/tikv/tikv/pull/7827)
    -   アプリケーション層プロトコルネゴシエーション (ALPN) [＃7825](https://github.com/tikv/tikv/pull/7825)をサポート
    -   Titan [＃7818](https://github.com/tikv/tikv/pull/7818)に関する統計情報を追加
    -   同じトランザクション内の別のタスクによってタスクの優先度が下げられるのを回避するために、クライアントによって提供されたタスク ID を統合読み取りプールの識別子として使用することをサポートします[＃7814](https://github.com/tikv/tikv/pull/7814)
    -   `batch insert`リクエスト[＃7718](https://github.com/tikv/tikv/pull/7718)のパフォーマンスを向上させる

-   PD

    -   ノードをオフラインにするときにピアを削除する際の速度制限を排除[＃2372](https://github.com/pingcap/pd/pull/2372)

-   TiFlash

    -   Grafanaの**Read Index**のCountグラフの名前を**Ops**に変更する
    -   システム負荷が低いときにファイル記述子を開くためのデータを最適化して、システムリソースの消費を削減します。
    -   データstorage容量を制限するために容量関連の設定パラメータを追加します

-   ツール

    -   TiDB Lightning

        -   tidb-lightning-ctlに`fetch-mode`サブコマンドを追加して、TiKVクラスタモード[＃287](https://github.com/pingcap/tidb-lightning/pull/287)を印刷します。

    -   ティCDC

        -   `cdc cli` (changefeed) [＃546](https://github.com/pingcap/tiflow/pull/546)を使用してレプリケーションタスクの管理をサポート

    -   バックアップと復元 (BR)

        -   バックアップ中のGC時間の自動調整をサポート[＃257](https://github.com/pingcap/br/pull/257)
        -   データの復元時にPDパラメータを調整して復元を高速化します[＃198](https://github.com/pingcap/br/pull/198)

## バグ修正 {#bug-fixes}

-   ティビ

    -   複数の演算子での式実行にベクトル化を使用するかどうかを決定するロジックを改善[＃16383](https://github.com/pingcap/tidb/pull/16383)
    -   `IndexMerge`ヒントがデータベース名を正しくチェックできない問題を修正[＃16932](https://github.com/pingcap/tidb/pull/16932)
    -   シーケンスオブジェクト[＃17037](https://github.com/pingcap/tidb/pull/17037)切り捨てを禁止する
    -   `INSERT` / `UPDATE` / `ANALYZE` / `DELETE`ステートメントがシーケンスオブジェクト[＃16957](https://github.com/pingcap/tidb/pull/16957)で実行できる問題を修正
    -   ブートストラップフェーズの内部SQL文がステートメントサマリーテーブル[＃17062](https://github.com/pingcap/tidb/pull/17062)で内部クエリとして正しくマークされない問題を修正しました。
    -   TiFlashではサポートされているが TiKV ではサポートされていないフィルター条件が`IndexLookupJoin`演算子[＃17036](https://github.com/pingcap/tidb/pull/17036)にプッシュダウンされたときに発生するエラーを修正しました。
    -   照合順序が有効になった後に発生する可能性のある`LIKE`式の同時実行の問題を修正[＃16997](https://github.com/pingcap/tidb/pull/16997)
    -   照合順序が有効になった後、 `LIKE`関数が`Range`クエリインデックスを正しく構築できない問題を修正しました[＃16783](https://github.com/pingcap/tidb/pull/16783)
    -   `Plan Cache`文がトリガーされた後に`@@LAST_PLAN_FROM_CACHE`実行すると間違った値が返される問題を修正[＃16831](https://github.com/pingcap/tidb/pull/16831)
    -   `IndexMerge` [＃16947](https://github.com/pingcap/tidb/pull/16947)の候補パスを計算するときにインデックスの`TableFilter`失われる問題を修正
    -   `MergeJoin`ヒントを使用し、 `TableDual`演算子が存在する場合に物理クエリ プランを生成できない問題を修正しました[＃17016](https://github.com/pingcap/tidb/pull/17016)
    -   ステートメントサマリーテーブル[＃17018](https://github.com/pingcap/tidb/pull/17018)の`Stmt_Type`列目の値の大文字と小文字の誤りを修正
    -   異なるユーザーが同じ`tmp-storage-path` [＃16996](https://github.com/pingcap/tidb/pull/16996)を使用するとサービスを開始できないため、 `Permission Denied`エラーが報告される問題を修正しました。
    -   `CASE WHEN` [＃16995](https://github.com/pingcap/tidb/pull/16995)などの複数の入力列によって結果の型が決定される式に対して、 `NotNullFlag`結果の型が誤って設定される問題を修正しました。
    -   ダーティストアが存在する場合にグリーンGCが未解決のロックを残す可能性がある問題を修正[＃16949](https://github.com/pingcap/tidb/pull/16949)
    -   複数の異なるロックを持つ単一のキーに遭遇したときに、グリーン GC が未解決のロックを残す可能性がある問題を修正[＃16948](https://github.com/pingcap/tidb/pull/16948)
    -   サブクエリが親クエリ列[＃16952](https://github.com/pingcap/tidb/pull/16952)を参照しているため、 `INSERT VALUE`ステートメントに間違った値が挿入される問題を修正しました。
    -   `Float`値[＃16666](https://github.com/pingcap/tidb/pull/16666)に`AND`演算子を使用した場合に誤った結果になる問題を修正しました
    -   高価なログ[＃16907](https://github.com/pingcap/tidb/pull/16907)の`WAIT_TIME`フィールドの誤った情報を修正
    -   悲観的トランザクションモード[＃16897](https://github.com/pingcap/tidb/pull/16897)で`SELECT FOR UPDATE`文がスローログに記録できない問題を修正
    -   `Enum`または`Set`タイプの列で`SELECT DISTINCT`実行したときに発生する誤った結果を修正しました[＃16892](https://github.com/pingcap/tidb/pull/16892)
    -   `SHOW CREATE TABLE`文[＃16864](https://github.com/pingcap/tidb/pull/16864)の`auto_random_base`の表示エラーを修正
    -   `WHERE`節[＃16559](https://github.com/pingcap/tidb/pull/16559)の`string_value`の誤った値を修正
    -   `GROUP BY`ウィンドウ関数のエラーメッセージがMySQL [＃16165](https://github.com/pingcap/tidb/pull/16165)のものと一致しない問題を修正
    -   データベース名に大文字の[＃17167](https://github.com/pingcap/tidb/pull/17167)が含まれている場合に`FLASH TABLE`ステートメントの実行が失敗する問題を修正しました
    -   Projection Executor [＃17118](https://github.com/pingcap/tidb/pull/17118)の不正確なメモリトレースを修正しました
    -   異なるタイムゾーンの`SLOW_QUERY`のテーブルで時間フィルタリングが正しく行われない問題を修正[＃17164](https://github.com/pingcap/tidb/pull/17164)
    -   仮想生成列[＃17126](https://github.com/pingcap/tidb/pull/17126)で`IndexMerge`が使用された場合に発生するpanic問題を修正しました
    -   `INSTR`と`LOCATE`関数[＃17068](https://github.com/pingcap/tidb/pull/17068)の大文字化の問題を修正
    -   `tidb_allow_batch_cop`構成を有効にした後に`tikv server timeout`エラーが頻繁に報告される問題を修正[＃17161](https://github.com/pingcap/tidb/pull/17161)
    -   Float型に対して`XOR`演算を実行した結果がMySQL 8.0 [＃16978](https://github.com/pingcap/tidb/pull/16978)の結果と一致しない問題を修正
    -   サポートされていない`ALTER TABLE REORGANIZE PARTITION`文が実行されてもエラーが報告されない問題を修正しました[＃17178](https://github.com/pingcap/tidb/pull/17178)
    -   `EXPLAIN FORMAT="dot"  FOR CONNECTION ID`サポートされていないプランに遭遇したときにエラーが報告される問題を修正[＃17160](https://github.com/pingcap/tidb/pull/17160)
    -   ステートメントサマリーテーブル[＃17086](https://github.com/pingcap/tidb/pull/17086)の`EXEC_COUNT`列目にあるプリペアドステートメントのレコードの問題を修正
    -   ステートメントサマリーシステム変数[＃17129](https://github.com/pingcap/tidb/pull/17129)を設定するときに値が検証されない問題を修正
    -   プランキャッシュが有効な場合に、オーバーフロー値を使用して`UNSIGNED BIGINT`主キーをクエリするとエラーが報告される問題を修正[＃17120](https://github.com/pingcap/tidb/pull/17120)
    -   Grafana **TiDB サマリー**ダッシュボード[＃17105](https://github.com/pingcap/tidb/pull/17105)でマシン インスタンスとリクエスト タイプによる QPS 表示が誤っていた問題を修正

-   ティクヴ

    -   復元後に多くの空の領域が生成される問題を修正[＃7632](https://github.com/tikv/tikv/pull/7632)
    -   順序が乱れたインデックス読み取り応答を受け取ったときにRaftstoreがpanic問題を修正[＃7370](https://github.com/tikv/tikv/pull/7370)
    -   統合スレッドプールが有効になっている場合に、無効なstorageまたはコプロセッサ読み取りプール構成が拒否されない可能性がある問題を修正[＃7513](https://github.com/tikv/tikv/pull/7513)
    -   TiKVサーバーがシャットダウンされたときの`join`操作のpanic問題を修正[＃7713](https://github.com/tikv/tikv/pull/7713)
    -   診断API [＃7776](https://github.com/tikv/tikv/pull/7776)経由でTiKVスローログを検索しても結果が返されない問題を修正
    -   TiKVノードが長時間実行されると顕著なメモリ断片化が発生する問題を修正[＃7556](https://github.com/tikv/tikv/pull/7556)
    -   無効な日付が格納されている場合にSQL文の実行が失敗する問題を修正[＃7268](https://github.com/tikv/tikv/pull/7268)
    -   GCS [＃7739](https://github.com/tikv/tikv/pull/7739)からバックアップデータを復元できない問題を修正
    -   保存時の暗号化中に KMS キー ID が検証されない問題を修正[＃7719](https://github.com/tikv/tikv/pull/7719)
    -   異なるアーキテクチャのコンパイラにおけるコプロセッサーの根本的な正確性の問題を修正[＃7714](https://github.com/tikv/tikv/pull/7714) [＃7730](https://github.com/tikv/tikv/pull/7730)
    -   暗号化が有効になっている場合の`snapshot ingestion`エラーを修正[＃7815](https://github.com/tikv/tikv/pull/7815)
    -   設定ファイル[＃7817](https://github.com/tikv/tikv/pull/7817)の書き換え時に`Invalid cross-device link`エラーを修正
    -   設定ファイルを空のファイルに書き込むときに間違った toml 形式になる問題を修正[＃7817](https://github.com/tikv/tikv/pull/7817)
    -   Raftstoreで破棄されたピアがリクエストを処理できる問題を修正[＃7836](https://github.com/tikv/tikv/pull/7836)

-   PD

    -   pd-ctl [＃2399](https://github.com/pingcap/pd/pull/2399)の`region key`コマンドを使用するときに発生する`404`問題を修正しました
    -   TSO と ID 割り当てのモニター メトリックが Grafana ダッシュボード[＃2405](https://github.com/pingcap/pd/pull/2405)に表示されない問題を修正しました。
    -   pd-recoverがDockerイメージ[＃2406](https://github.com/pingcap/pd/pull/2406)に含まれていない問題を修正
    -   データディレクトリのパスを絶対パスに解析して、TiDBダッシュボードにPD情報が正しく表示されない問題を修正しました[＃2420](https://github.com/pingcap/pd/pull/2420)
    -   pd-ctl [＃2416](https://github.com/pingcap/pd/pull/2416)で`scheduler config shuffle-region-scheduler`コマンドを使用したときにデフォルトの出力がない問題を修正しました

-   TiFlash

    -   一部のシナリオで使用容量の情報が誤って報告される問題を修正

-   ツール

    -   TiDBBinlog

        -   ダウンストリームがKafka [＃962](https://github.com/pingcap/tidb-binlog/pull/962)の場合に`mediumint`型のデータが処理されない問題を修正
        -   DDL 内のデータベース名がキーワード[＃961](https://github.com/pingcap/tidb-binlog/pull/961)の場合に、reparo が DDL ステートメントの解析に失敗する問題を修正しました。

    -   ティCDC

        -   `TZ`環境変数が設定されていない場合に間違ったタイムゾーンが使用される問題を修正[＃512](https://github.com/pingcap/tiflow/pull/512)

        -   いくつかのエラーが正しく処理されないため、サーバーが終了したときに所有者がリソースをクリーンアップしない問題を修正しました[＃528](https://github.com/pingcap/tiflow/pull/528)

        -   TiKV [＃531](https://github.com/pingcap/tiflow/pull/531)に再接続するときにTiCDCが停止する可能性がある問題を修正

        -   テーブルスキーマ[＃534](https://github.com/pingcap/tiflow/pull/534)の初期化時にメモリ使用量を最適化する

        -   `watch`モードを使用してレプリケーションステータスの変更を監視し、準リアルタイム更新を実行してレプリケーション遅延を削減します[＃481](https://github.com/pingcap/tiflow/pull/481)

    <!---->

    -   バックアップと復元 (BR)

        -   BRが`auto_random`属性[＃241](https://github.com/pingcap/br/issues/241)を持つテーブルを復元した後、データを挿入すると`duplicate entry`エラーが発生する可能性がある問題を修正しました。
