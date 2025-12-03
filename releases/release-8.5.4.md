---
title: TiDB 8.5.4 Release Notes
summary: TiDB 8.5.4 の機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 8.5.4 リリースノート {#tidb-8-5-4-release-notes}

発売日：2025年11月27日

TiDB バージョン: 8.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 特徴 {#features}

-   特定のテーブルのデータの再配布をサポート（実験的） [＃63260](https://github.com/pingcap/tidb/issues/63260) @ [バッファフライ](https://github.com/bufferflies)

    PDは、クラスター内のすべてのTiKVノードにデータが可能な限り均等に分散されるように自動的にスケジュールを設定します。ただし、この自動スケジューリングはクラスター全体に焦点を当てています。場合によっては、クラスター全体のデータ分散が均衡していても、特定のテーブルのデータがTiKVノード間で不均等に分散されている可能性があります。

    v8.5.4以降では、 [`SHOW TABLE DISTRIBUTION`](https://docs.pingcap.com/tidb/v8.5/sql-statement-show-table-distribution/)のステートメントを使用して、特定のテーブルのデータがすべてのTiKVノード間でどのように分散されているかを確認できます。データ分散が不均衡な場合は、 [`DISTRIBUTE TABLE`](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table)ステートメントを使用してテーブルのデータを再分散し（実験的）、負荷分散を改善できます。

    特定のテーブルのデータの再配布は、タイムアウト制限のある1回限りのタスクであることに注意してください。タイムアウトまでに配布タスクが完了しない場合、タスクは自動的に終了します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/sql-statement-distribute-table)参照してください。

-   DDL文に埋め込まれた`ANALYZE`サポート[＃57948](https://github.com/pingcap/tidb/issues/57948) @ [テリー・パーセル](https://github.com/terry1purcell) @ [アイリンキッド](https://github.com/AilinKid)

    この機能は、次のタイプの DDL ステートメントに適用されます。

    -   新しいインデックスを作成するDDL文: [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
    -   既存のインデックスを再編成する DDL ステートメント: [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)と[`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)

    この機能を有効にすると、TiDBは新規または再編成されたインデックスがユーザーに表示される前に、自動的に`ANALYZE` （統計収集）操作を実行します。これにより、インデックスの作成または再編成後に一時的に統計が利用できなくなることによる、オプティマイザの推定値の不正確さや潜在的なプラン変更を防止できます。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/ddl_embedded_analyze)参照してください。

-   パーティションテーブルの非一意の列に対するグローバルインデックスの作成をサポート[＃58650](https://github.com/pingcap/tidb/issues/58650) @ [定義2014](https://github.com/Defined2014) @ [ミョンス](https://github.com/mjonss)

    バージョン8.3.0以降、TiDBではパーティションテーブルの一意の列にグローバルインデックスを作成してクエリパフォーマンスを向上できます。ただし、一意でない列へのグローバルインデックスの作成はサポートされていませんでした。バージョン8.5.4以降、TiDBはこの制限を撤廃し、パーティションテーブルの一意でない列にもグローバルインデックスを作成できるようになりました。これにより、グローバルインデックスの使い勝手が向上します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/partitioned-table#global-indexes)参照してください。

-   TiFlash [＃10266](https://github.com/pingcap/tiflash/issues/10266) @ [ゲンリチ](https://github.com/gengliqi)の正常なシャットダウンをサポート

    TiFlashサーバーをシャットダウンする際、 TiFlash は現在実行中の MPP タスクを、設定可能なタイムアウト時間の間継続させ、新しい MPP タスク要求を拒否するようになりました。デフォルトのタイムアウト時間は 600 秒ですが、設定項目[`flash.graceful_wait_shutdown_timeout`](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854)で調整できます。

    -   タイムアウト期間が経過する前に実行中のすべての MPP タスクが終了した場合、 TiFlash は直ちにシャットダウンします。
    -   タイムアウト期間が経過しても未完了の MPP タスクが残っている場合、 TiFlash は強制的にシャットダウンします。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854)参照してください。

-   パフォーマンス、スケーラビリティ、安定性を向上させる新しい TiCDCアーキテクチャオプションを導入[＃442](https://github.com/pingcap/ticdc/issues/442) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)

    この新しいアーキテクチャは、TiCDC コア コンポーネントを再設計し、 [古典的なTiCDCアーキテクチャ](/ticdc/ticdc-classic-architecture.md)の構成、使用法、API との互換性を維持しながら、データ処理ワークフローを最適化します。

    この新しいアーキテクチャを使用するように構成すると、TiCDCはほぼ線形のスケーラビリティを実現し、数百万のテーブルをより少ないリソース消費で複製できます。また、変更フィードのレイテンシーも短縮され、書き込みワークロードが高く、DDL操作が頻繁に行われ、クラスタのスケーリングが行われるシナリオにおいて、より安定したパフォーマンスが得られます。なお、この新しいアーキテクチャは現在約[初期の制限](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture#limitations)です。

    新しいアーキテクチャを使用するには、TiCDC 構成項目[`newarch`](https://docs.pingcap.com/tidb/v8.5/ticdc-server-config#newarch-new-in-v854-release1)を`true`に設定します。

    詳細については[ドキュメント](https://docs.pingcap.com/tidb/v8.5/ticdc-architecture)参照してください。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

-   システム変数[`tidb_mpp_store_fail_ttl`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_mpp_store_fail_ttl)のデフォルト値を`60s`から`0s`に変更します。これにより、クエリの失敗を防ぐための遅延が不要になり、TiDB は新しく起動したTiFlashノードにクエリを送信する前に待機する必要がなくなります[＃61826](https://github.com/pingcap/tidb/issues/61826) @ [ゲンリチ](https://github.com/gengliqi)

-   バージョン8.5.4以降、 [`tidb_replica_read`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_replica_read-new-in-v40)システム変数は読み取り専用SQL文にのみ適用されます。この変更により、データ読み取りの安全性が向上し、他の機能との重複が軽減されます[＃62856](https://github.com/pingcap/tidb/issues/62856) @ [あなた06](https://github.com/you06)

-   次のシステム変数を追加します。

    -   [`tidb_opt_enable_no_decorrelate_in_select`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_no_decorrelate_in_select-new-in-v854) : `SELECT`番目のリスト内のサブクエリの相関を解除するかどうかを制御します。デフォルト値は`OFF`です[＃51116](https://github.com/pingcap/tidb/issues/51116) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   [`tidb_opt_enable_semi_join_rewrite`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_enable_semi_join_rewrite-new-in-v854) : `EXISTS`サブクエリを書き換えるかどうかを制御します。デフォルト値は`OFF`です[＃44850](https://github.com/pingcap/tidb/issues/44850) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   [`tidb_stats_update_during_ddl`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_stats_update_during_ddl-new-in-v854) : 埋め込みDDL分析を有効にするかどうかを制御します。デフォルト値は`OFF`です[＃57948](https://github.com/pingcap/tidb/issues/57948) @ [テリー・パーセル](https://github.com/terry1purcell) @ [アイリンキッド](https://github.com/AilinKid)

### コンフィグレーションパラメータ {#configuration-parameters}

-   次の TiKV 構成項目を廃止し、自動圧縮動作を制御する新しい[`gc.auto-compaction`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file/#gcauto-compaction)構成グループに置き換えます[＃18727](https://github.com/tikv/tikv/issues/18727) @ [v01dスター](https://github.com/v01dstar)

    -   非推奨の構成項目: [`region-compact-check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-interval) 、 [`region-compact-check-step`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-check-step) 、 [`region-compact-min-tombstones`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-tombstones) 、 [`region-compact-tombstones-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-tombstones-percent) 、 [`region-compact-min-redundant-rows`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-min-redundant-rows-new-in-v710) 、および[`region-compact-redundant-rows-percent`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#region-compact-redundant-rows-percent-new-in-v710) 。
    -   新しい構成項目[`gc.auto-compaction.tombstone-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-percent-threshold-new-in-v757-and-v854) [`gc.auto-compaction.check-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#check-interval-new-in-v757-and-v854) [`gc.auto-compaction.redundant-rows-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-threshold-new-in-v757-and-v854) [`gc.auto-compaction.tombstone-num-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#tombstone-num-threshold-new-in-v757-and-v854) [`gc.auto-compaction.redundant-rows-percent-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#redundant-rows-percent-threshold-new-in-v757-and-v854) [`gc.auto-compaction.bottommost-level-force`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#bottommost-level-force-new-in-v757-and-v854)

-   TiFlash設定項目[`flash.graceful_wait_shutdown_timeout`](https://docs.pingcap.com/tidb/v8.5/tiflash-configuration#graceful_wait_shutdown_timeout-new-in-v854)を追加します。これは、 TiFlashサーバーのシャットダウン時の最大待機時間を制御します。デフォルト値は`600`秒です。この期間中、 TiFlash は未完了の MPP タスクの実行を継続しますが、新しいタスクは受け付けません。実行中のすべての MPP タスクがこのタイムアウト前に終了した場合、 TiFlash は直ちにシャットダウンします。それ以外の場合は、待機時間が経過した後に強制的にシャットダウンされます[＃10266](https://github.com/pingcap/tiflash/issues/10266) @ [ゲンリチ](https://github.com/gengliqi)

### MySQLの互換性 {#mysql-compatibility}

v8.5.4以降、TiDBは`DECIMAL`桁の列にデータを挿入する際の動作をMySQLに準拠させました。小数点以下の桁数が列の定義スケールを超える場合、TiDBは自動的に超過桁数を切り捨て、超過小数点以下の桁数に関係なく、切り捨てられたデータを正常に挿入します。以前のバージョンのTiDBでは、挿入された`DECIMAL`値の小数点以下の桁数が72を超えると、挿入は失敗し、エラーが返されていました。詳細については、 [JDBC を使用して TiDB に接続する](https://docs.pingcap.com/tidb/v8.5/dev-guide-sample-application-java-jdbc#mysql-compatibility)参照してください。

## 改善点 {#improvements}

-   ティドブ

    -   `IN`サブクエリ[＃58829](https://github.com/pingcap/tidb/issues/58829) @ [qw4990](https://github.com/qw4990)の Semi テーブル結合に`semi_join_rewrite`ヒントを適用することをサポート
    -   `tidb_opt_ordering_index_selectivity_ratio`システム変数が[＃62817](https://github.com/pingcap/tidb/issues/62817)で[テリー・パーセル](https://github.com/terry1purcell)で効果を発揮するときの推定戦略を最適化する
    -   オプティマイザの選択ロジックを調整して、特定のシナリオで新しく作成されたインデックスが選択される可能性を高めます[＃57948](https://github.com/pingcap/tidb/issues/57948) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   少数の個別値（NDV）を持つ列のクエリ推定ロジックを最適化[＃61792](https://github.com/pingcap/tidb/issues/61792) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   `LIMIT OFFSET` [＃45077](https://github.com/pingcap/tidb/issues/45077) @ [qw4990](https://github.com/qw4990)を含むインデックス結合クエリの推定戦略を最適化する
    -   統計が時間[＃58068](https://github.com/pingcap/tidb/issues/58068) @ [テリー・パーセル](https://github.com/terry1purcell)で収集されない場合の範囲外推定戦略を最適化する
    -   デバッグを容易にするために、Grafanaの**パフォーマンス概要**&gt; **SQL実行時間概要**パネルに`backoff`メトリックを追加します[＃61441](https://github.com/pingcap/tidb/issues/61441) @ [dbsid](https://github.com/dbsid)
    -   監査ログプラグイン[＃63525](https://github.com/pingcap/tidb/issues/63525) @ [ヤンケオ](https://github.com/YangKeao)にステートメント ID 情報を追加します

-   TiKV

    -   BRモジュール内の特定の自動回復可能なエラーのログレベルを`ERROR`から`WARN`に変更して、不要なアラート[＃18493](https://github.com/tikv/tikv/issues/18493) @ [ユジュンセン](https://github.com/YuJuncen)を削減します。
    -   不要なアラートを減らすために、特定の TiKV エラーのログレベルを`ERROR`から`WARN`に変更します[＃18745](https://github.com/tikv/tikv/issues/18745) @ [終了コード1](https://github.com/exit-code-1)
    -   RaftモジュールのGCチェックプロセスを2つのフェーズに分割して、リージョン[＃18695](https://github.com/tikv/tikv/issues/18695) @ [v01dスター](https://github.com/v01dstar)の冗長MVCCバージョンのガベージコレクションの効率を向上させます。
    -   GCセーフポイントとRocksDB統計に基づいてMVCC冗長性を計算し、圧縮[＃18697](https://github.com/tikv/tikv/issues/18697) @ [v01dスター](https://github.com/v01dstar)の効率と精度を向上させます。
    -   リージョンMVCCのGC処理ロジックをGCワーカースレッドで実行するように変更し、GC処理ロジック全体を統一する[＃18727](https://github.com/tikv/tikv/issues/18727) @ [v01dスター](https://github.com/v01dstar)
    -   デフォルトの gRPC スレッド プール サイズの計算方法を最適化し、固定値ではなく CPU クォータの合計に基づいて動的に計算するようにすることで、gRPC スレッド[＃18613](https://github.com/tikv/tikv/issues/18613) @ [LykxSassinator](https://github.com/LykxSassinator)の不足によるパフォーマンスのボトルネックを回避します。
    -   多数の SST ファイルがある環境での非同期スナップショットおよび書き込み操作のテールレイテンシーを最適化します[＃18743](https://github.com/tikv/tikv/issues/18743) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   不要なエラーログを[＃9370](https://github.com/tikv/pd/issues/9370) [バッファフライ](https://github.com/bufferflies)削減
    -   Golangのバージョンを1.23.0から1.23.12にアップグレードし、関連する依存関係[＃9788](https://github.com/tikv/pd/issues/9788) @ [Jmポテト](https://github.com/JmPotato)を更新します。
    -   テーブルレベルでの領域分散をサポートし、 `scatter-role`と`engine`次元にわたってバランスのとれた分散を実現します[＃8986](https://github.com/tikv/pd/issues/8986) @ [バッファフライ](https://github.com/bufferflies)

-   TiFlash

    -   不要なデータの読み取りをスキップして`TableScan`パフォーマンスを向上[＃9875](https://github.com/pingcap/tiflash/issues/9875) @ [ゲンリキ](https://github.com/gengliqi)
    -   TiFlash [＃10361](https://github.com/pingcap/tiflash/issues/10361) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で、多数の列とスパース データ (つまり、 `NULL`または空の値が多い) を含む`TableScan`の広いテーブルのパフォーマンスを最適化します。
    -   多数のテーブル[＃10357](https://github.com/pingcap/tiflash/issues/10357) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を持つクラスターにベクトル インデックスを追加することによって発生するTiFlash CPU オーバーヘッドを削減します。
    -   無駄なRaftコマンドを処理するときに不要なログ出力を最小限に抑えてログ量を減らす[＃10467](https://github.com/pingcap/tiflash/issues/10467) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlash [＃10487](https://github.com/pingcap/tiflash/issues/10487) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の小さなパーティションテーブルで`TableScan`パフォーマンスを向上

-   ツール

    -   TiDB データ移行 (DM)

        -   アップストリーム`GTID_MODE` [＃12167](https://github.com/pingcap/tiflow/issues/12167) @ [オリバーS929](https://github.com/OliverS929)を取得する際に大文字と小文字を区別しないマッチングをサポートします

## バグ修正 {#bug-fixes}

-   ティドブ

    -   `tidb_isolation_read_engines` `tiflash` [＃60869](https://github.com/pingcap/tidb/issues/60869) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)に設定されている場合に`use index`ヒントが有効にならない問題を修正しました
    -   `max_execution_time` `SELECT FOR UPDATE`ステートメント[＃62960](https://github.com/pingcap/tidb/issues/62960) @ [エキシウム](https://github.com/ekexium)に反映されない問題を修正
    -   月または年にわたる行数の推定値が大幅に過大評価される可能性がある問題を修正[＃50080](https://github.com/pingcap/tidb/issues/50080) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   準備済みステートメントの`Decimal`型の処理が MySQL [＃62602](https://github.com/pingcap/tidb/issues/62602) @ [チャンルイ・ライアン](https://github.com/ChangRui-Ryan)と一致しない問題を修正しました
    -   `TRUNCATE()`関数のショートパスが誤って処理される問題を修正[＃57608](https://github.com/pingcap/tidb/issues/57608) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `Out Of Quota For Local Temporary Space`エラーが発生したときに、こぼれたファイルが完全に削除されない可能性がある問題を修正[＃63216](https://github.com/pingcap/tidb/issues/63216) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `INFORMATION_SCHEMA`テーブルに対して正規表現を使用したクエリが誤った結果を返す可能性がある問題を修正しました[＃62347](https://github.com/pingcap/tidb/issues/62347) @ [リバー2000i](https://github.com/River2000i)
    -   PD [＃58871](https://github.com/pingcap/tidb/issues/58871) @ [ジョーチェン](https://github.com/joechenrh)からタイムスタンプを取得できなかった場合に TiDB がエラーを返さない問題を修正しました
    -   `MODIFY COLUMN`ステートメント[＃60264](https://github.com/pingcap/tidb/issues/60264) @ [接線](https://github.com/tangenta)の実行中に、オーナー TiDB インスタンスと非オーナー TiDB インスタンス間でクエリ結果が異なる問題を修正しました。
    -   パラメータ[＃63201](https://github.com/pingcap/tidb/issues/63201) @ [fzzf678](https://github.com/fzzf678)を動的に変更した後、 `ADMIN ALTER DDL JOBS`ステートメントで誤ったパラメータ値が表示される問題を修正しました。
    -   トランザクション[＃62424](https://github.com/pingcap/tidb/issues/62424) @ [wjhuang2016](https://github.com/wjhuang2016)内でインデックスを追加したときに GC セーフ ポイントが進まない問題を修正しました
    -   過度に大きな SST ファイルを L0 に取り込むとフロー制御[＃63466](https://github.com/pingcap/tidb/issues/63466) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)がトリガーされる問題を修正しました
    -   CPU対メモリ比が1:2 [＃60951](https://github.com/pingcap/tidb/issues/60951) @ [wjhuang2016](https://github.com/wjhuang2016)のときにグローバルソートがブロックされる問題を修正
    -   タスク数が[＃63896](https://github.com/pingcap/tidb/issues/63896)を超えると、保留中の Distributed eXecution Framework (DXF) タスクをキャンセルできない問題を修正しました[D3ハンター](https://github.com/D3Hunter)
    -   DXFタスクがキャンセルされた後、他のタスクが[＃63927](https://github.com/pingcap/tidb/issues/63927) @ [D3ハンター](https://github.com/D3Hunter)で終了できない問題を修正しました
    -   `Apply`演算子同時実行を有効にすると（ `tidb_enable_parallel_apply = on` ）、クローン実装[＃59863](https://github.com/pingcap/tidb/issues/59863) @ [ホーキングレイ](https://github.com/hawkingrei)の不足によりプラン生成が失敗する問題を修正しました。
    -   `ATAN2`関数を使用すると誤った結果が生成される可能性がある問題を修正[＃60093](https://github.com/pingcap/tidb/issues/60093) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   `select 1 from dual`インスタンスレベルのプランキャッシュ[＃63075](https://github.com/pingcap/tidb/issues/63075) @ [時間と運命](https://github.com/time-and-fate)を使用できない問題を修正
    -   結合順序を変更するとプランナーが失敗する可能性がある問題を修正[＃61715](https://github.com/pingcap/tidb/issues/61715) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   バインディングで`set_var`ヒントを使用すると変数が元の設定に復元されなくなる問題を修正[＃59822](https://github.com/pingcap/tidb/issues/59822) @ [wddevries](https://github.com/wddevries)
    -   `ONLY_FULL_GROUP_BY`負の値に設定すると検証エラー[＃62617](https://github.com/pingcap/tidb/issues/62617) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正しました
    -   `ONLY_FULL_GROUP_BY`チェックで大文字と小文字が区別されない問題を修正[＃62672](https://github.com/pingcap/tidb/issues/62672) @ [アイリンキッド](https://github.com/AilinKid)
    -   DP結合順序アルゴリズムが誤ったプラン[＃63353](https://github.com/pingcap/tidb/issues/63353) @ [ウィノロス](https://github.com/winoros)を生成する可能性がある問題を修正しました
    -   外部結合を内部結合に書き換えると誤った結果が生成される可能性がある問題を修正[＃61327](https://github.com/pingcap/tidb/issues/61327) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   特定のクエリを実行すると内部panicが発生する可能性がある問題を修正[＃58600](https://github.com/pingcap/tidb/issues/58600) @ [定義2014](https://github.com/Defined2014)
    -   特定の`ALTER PARTITION`操作[＃64084](https://github.com/pingcap/tidb/pull/64084) @ [ミョンス](https://github.com/mjonss)でグローバルインデックスが誤ったデータを読み取る可能性がある問題を修正しました
    -   グローバルインデックスが場合によっては誤った結果を返す可能性がある問題を修正[＃61083](https://github.com/pingcap/tidb/issues/61083) @ [定義2014](https://github.com/Defined2014)
    -   `character_set_results`誤った文字を置き換えるのではなく切り捨てる問題を修正[＃61085](https://github.com/pingcap/tidb/issues/61085) @ [xhebox](https://github.com/xhebox)
    -   `ADD COLUMN`と`UPDATE`ステートメントを同時に実行するとエラー[＃60047](https://github.com/pingcap/tidb/issues/60047) @ [L-メープル](https://github.com/L-maple)が発生する可能性がある問題を修正しました
    -   マージ結合でコスト[＃62917](https://github.com/pingcap/tidb/issues/62917) @ [qw4990](https://github.com/qw4990)を計算するときにフィルター条件が省略される可能性がある問題を修正しました

-   PD

    -   PDクライアントの再試行戦略が正しく初期化されない問題を修正[＃9013](https://github.com/tikv/pd/issues/9013) @ [rleungx](https://github.com/rleungx)
    -   TSO HTTP API `/config`および`/members`が誤った結果[＃9797](https://github.com/tikv/pd/issues/9797) @ [lhy1024](https://github.com/lhy1024)を返す問題を修正しました
    -   TSO Follower Proxy [＃9188](https://github.com/tikv/pd/issues/9188) @ [テーマ](https://github.com/Tema)の誤ったエラー処理ロジックを修正しました
    -   バケットレポートを無効にした後でもバケットの分割が機能する問題を修正[＃9726](https://github.com/tikv/pd/issues/9726) @ [バッファフライ](https://github.com/bufferflies)
    -   リソース マネージャーがトークンを誤って割り当て、クエリが[＃9455](https://github.com/tikv/pd/issues/9455) @ [Jmポテト](https://github.com/JmPotato)でスタックする問題を修正しました。
    -   PDリーダーが[＃9602](https://github.com/tikv/pd/issues/9602) [okJiang](https://github.com/okJiang)で切り替えた後に配置ルールが有効にならない問題を修正しました
    -   PD が科学表記法の大きな数値を解析できず、その結果一部の TTL 関連の設定が有効にならない問題を修正[＃9343](https://github.com/tikv/pd/issues/9343) @ [lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   クエリ対象の列に`NULL`値が[＃10340](https://github.com/pingcap/tiflash/issues/10340) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で多数含まれている場合にクエリが失敗する可能性がある問題を修正しました
    -   TiFlash がRU 消費量[＃10380](https://github.com/pingcap/tiflash/issues/10380) @ [ジンヘリン](https://github.com/JinheLin)の統計を水増し生成する問題を修正しました
    -   分散storageとコンピューティングアーキテクチャ[＃10278](https://github.com/pingcap/tiflash/issues/10278) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で低速クエリが存在する場合にTiFlash がOOM に遭遇する可能性がある問題を修正しました
    -   分散storageおよびコンピューティングアーキテクチャ[＃10424](https://github.com/pingcap/tiflash/issues/10424) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でTiFlashと S3 の間でネットワークパーティションが発生すると、 TiFlash が無期限に再試行する可能性がある問題を修正しました。
    -   `FLOOR()`と`CEIL()`関数のパラメータが`DECIMAL`型[＃10365](https://github.com/pingcap/tiflash/issues/10365) @ [チャンルイ・ライアン](https://github.com/ChangRui-Ryan)の場合に誤った結果を返す可能性がある問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップのzstd圧縮が有効にならず、出力が圧縮されない問題を修正[＃18836](https://github.com/tikv/tikv/issues/18836) @ [3ポイントシュート](https://github.com/3pointer)
        -   Azure Blob Storage [＃18410](https://github.com/tikv/tikv/issues/18410) @ [ユジュンセン](https://github.com/YuJuncen)にデータをバックアップするときにフラッシュ操作が時々遅くなる問題を修正しました
        -   ファイルの削除に失敗した場合に発生する可能性のある問題`log truncate`を修正[＃63358](https://github.com/pingcap/tidb/issues/63358) @ [ユジュンセン](https://github.com/YuJuncen)
        -   バックアップ中に`--checksum`を`false`に設定すると、 [＃60978](https://github.com/pingcap/tidb/issues/60978) @ [リーヴルス](https://github.com/Leavrth)を復元した後に`mysql.stats_meta`テーブルの`count`列が`0`なる可能性がある問題を修正しました。
        -   これらのサービスの帯域幅制限が有効になっている場合に、 BRがS3互換storageサービスからデータを復元できない可能性を低減します[＃18846](https://github.com/tikv/tikv/issues/18846) @ [ケニーtm](https://github.com/kennytm)
        -   `log backup observer`リージョンの観測を失い、ログ バックアップの進行が[＃18243](https://github.com/tikv/tikv/issues/18243) @ [リーヴルス](https://github.com/Leavrth)に進まなくなる可能性がある問題を修正しました。
        -   バックアップされたテーブルに特定の特別なスキーマ[＃63663](https://github.com/pingcap/tidb/issues/63663) @ [リドリスR](https://github.com/RidRisR)が含まれている場合に`restore point`作成が失敗する問題を修正しました

    -   TiCDC

        -   仮想列[＃12241](https://github.com/pingcap/tiflow/issues/12241) @ [wk989898](https://github.com/wk989898)を含む列型パーティションディスパッチャを構成するときに発生する可能性のあるpanicを修正しました。
        -   DDL プラー[＃12244](https://github.com/pingcap/tiflow/issues/12244) @ [wk989898](https://github.com/wk989898)を閉じるときに発生する可能性のあるpanicを修正しました
        -   `filter`構成[＃12286](https://github.com/pingcap/tiflow/issues/12286) @ [アズドンメン](https://github.com/asddongmen)の`ignore-txn-start-ts`パラメータを通じてサポートされていない DDL タイプのフィルタリングをサポートします
        -   Azure Blob Storage をダウンストリーム[＃12277](https://github.com/pingcap/tiflow/issues/12277) @ [ズラクツィア](https://github.com/zurakutsia)として使用すると、変更フィード タスクがスタックする可能性がある問題を修正しました。
        -   `DROP FOREIGN KEY` DDLが下流[＃12328](https://github.com/pingcap/tiflow/issues/12328) @ [3エースショーハンド](https://github.com/3AceShowHand)に複製されない問題を修正
        -   リージョンサブスクリプション[＃19048](https://github.com/tikv/tikv/issues/19048) @ [3エースショーハンド](https://github.com/3AceShowHand)中にロールバックおよび事前書き込みエントリが発生すると TiCDC がpanicになる可能性がある問題を修正しました。
        -   TiKV のアサーションエラーにより TiCDC がpanicになる可能性がある問題を修正[＃18498](https://github.com/tikv/tikv/issues/18498) @ [タランガ](https://github.com/tharanga)
