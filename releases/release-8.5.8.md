---
title: TiDB 8.5.8 Release Notes
summary: TiDB 8.5.8 の改善点とバグ修正について説明します。
---

# TiDB 8.5.8 Release Notes

リリース日: 2026年8月27日

TiDB バージョン: 8.5.8

クイックアクセス: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 改善点 {#improvements}

+ TiDB

    - 仮想カラムを含む複合インデックスについて、カラム統計が利用できない場合にインデックス統計へフォールバックすることで、オプティマイザの行数推定を改善し、TiDB がより正確にインデックスを選択できるようにしました [#69134](https://github.com/pingcap/tidb/issues/69134) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70327 -->

+ Tools

    + TiCDC

        - delete イベントが無視される場合の TiCDC changefeed スキャン性能を改善し、delete が多いワークロードの履歴追いつき処理中に不要な DML デコードを削減しました [#5430](https://github.com/pingcap/ticdc/issues/5430) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5767 -->
        - 適応型スキャンウィンドウアルゴリズムを導入することで、メモリプレッシャー下での TiCDC event service の安定性とスループットを改善し、DDL や sync point シナリオにおける dispatcher の starvation と reset イベントを減らしました [#4172](https://github.com/pingcap/ticdc/issues/4172) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5761 -->
        - 検証時に起動時専用の処理を回避し、既存トピックに対して Schema Registry などの encoder 依存関係を確認し、TiCDC がトピックを作成する必要がある場合にのみ `replication-factor` を検証することで、TiCDC Kafka Sink の検証をより軽量かつ完全なものに改善しました [#5618](https://github.com/pingcap/ticdc/issues/5618) [#5720](https://github.com/pingcap/ticdc/issues/5720) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5811 -->
        - 同じ Sink 内のすべての Encoder で単一の `ClaimCheck` インスタンスを共有することで、Claim-Check を有効にした TiCDC Kafka Sink における外部ストレージクライアントと接続の使用量を削減しました [#5719](https://github.com/pingcap/ticdc/issues/5719) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5811 -->
        - 設定、Admin API、および producer エラーの分類とラップを標準化することで、TiCDC Kafka Sink のエラーハンドリングを簡素化および統一し、リトライ分類とトラブルシューティングを容易にしました [#5790](https://github.com/pingcap/ticdc/issues/5790) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5811 -->

## バグ修正 {#bug-fixes}

+ TiDB

    - `MODIFY COLUMN` を含むマルチスキーマ変更が、ingest または分散 backfill を使用せずにトランザクション backfill にフォールバックしてしまう問題を修正しました [#70136](https://github.com/pingcap/tidb/issues/70136) @[joechenrh](https://github.com/joechenrh) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/70188 -->
    - パーティションテーブルでインデックスを追加する進捗が、再編成中に後退する可能性がある問題を修正しました [#62496](https://github.com/pingcap/tidb/issues/62496) @[GMHDBJD](https://github.com/GMHDBJD) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/68782 -->
    - `ADMIN ALTER DDL JOBS` で、実行中のトランザクションモード backfill のスレッド数またはバッチサイズを動的に調整できない問題を修正しました [#70138](https://github.com/pingcap/tidb/issues/70138) @[joechenrh](https://github.com/joechenrh) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/70256 -->
    - クエリがネストした `NOT IN` 式のオペランドとして `IN` サブクエリを使用した場合に、TiDB が panic を起こしてユーザーセッションを終了する可能性がある問題を修正しました [#64854](https://github.com/pingcap/tidb/issues/64854) @[hawkingrei](https://github.com/hawkingrei) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70259 -->
    - それ以外ではキャッシュ安全な `JSON_EXTRACT()` を使用するクエリが、プリペアドプランキャッシュまたは非プリペアドプランキャッシュを使用できない問題を修正しました [#69522](https://github.com/pingcap/tidb/issues/69522) @[winoros](https://github.com/winoros) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70257 -->
    - `ALTER TABLE ADD COLUMN` で追加された仮想生成カラムの統計が誤って初期化される可能性があり、その結果 `SHOW STATS_HISTOGRAMS` の出力が不正確になり、プレースホルダー統計が不要に読み込まれる問題を修正しました [#69160](https://github.com/pingcap/tidb/issues/69160) @[qw4990](https://github.com/qw4990) <!-- component: planner --> <!-- pr: https://github.com/pingcap/tidb/pull/70325 -->
    - 実行やリセットを行わないままプリペアドステートメントに対して `COM_STMT_SEND_LONG_DATA` リクエストを繰り返し受信すると、TiDB が接続メモリを無制限に消費する可能性がある問題を修正しました [#70349](https://github.com/pingcap/tidb/issues/70349) @[djshow832](https://github.com/djshow832) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70369 -->
    - SQL 文またはオプティマイザヒントを、過度に深くネストした括弧を含む形で解析すると、TiDB がクラッシュする可能性がある問題を修正しました [#70192](https://github.com/pingcap/tidb/issues/70192) @[Debra-He](https://github.com/Debra-He) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70264 -->
    - PD クライアントが無効なネスト runtime trace リージョンを出力するため、バッチ TSO リクエスト中に TiDB runtime trace の解析が失敗する可能性がある問題を修正しました [#69743](https://github.com/pingcap/tidb/issues/69743) @[YangKeao](https://github.com/YangKeao) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70310 -->
    - `COM_CHANGE_USER` 認証失敗時に、接続が不整合なセッション状態のまま残る可能性がある問題を修正しました [#69691](https://github.com/pingcap/tidb/issues/69691) @[bb7133](https://github.com/bb7133) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70229 -->
    - `COM_STMT_SEND_LONG_DATA` が単一のプリペアドステートメントに対してパラメータデータを無制限に蓄積できてしまう問題を修正しました。TiDB は現在、セッションの `max_allowed_packet` 設定を使用して蓄積サイズを制限し、制限を超えた場合は packet-too-large エラーを返します [#69693](https://github.com/pingcap/tidb/issues/69693) @[bb7133](https://github.com/bb7133) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70231 -->
    - 特別に細工された圧縮入力を処理する際に、`UNCOMPRESS()` が追跡されない過剰なメモリを消費し、クエリのメモリクォータを超える可能性がある問題を修正しました [#70198](https://github.com/pingcap/tidb/issues/70198) @[Debra-He](https://github.com/Debra-He) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70279 -->
    - 権限のないユーザーが `INFORMATION_SCHEMA.USER_ATTRIBUTES` を通じて他ユーザーの属性を読み取れる問題を修正しました [#70277](https://github.com/pingcap/tidb/issues/70277) @[djshow832](https://github.com/djshow832) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70317 -->
    - メモリ使用量がアラーム比率を頻繁に超える場合に、OOM 診断用 goroutine プロファイルの記録によって stop-the-world の停止時間が長引き、クエリレイテンシーが増加する可能性がある問題を修正しました [#62080](https://github.com/pingcap/tidb/issues/62080) @[YangKeao](https://github.com/YangKeao) <!-- component: sql-infra --> <!-- pr: https://github.com/pingcap/tidb/pull/70228 -->
    - 悲観的トランザクション内の `LOAD DATA LOCAL INFILE` が、リトライ可能なロック競合の後に内部リトライを行い、クライアント接続との同期がずれ、元のデッドロックエラーではなく無効なシーケンスエラーを返す問題を修正しました [#69793](https://github.com/pingcap/tidb/issues/69793) @[lance6716](https://github.com/lance6716) <!-- component: transaction, sql-infra, execution --> <!-- pr: https://github.com/pingcap/tidb/pull/70194 -->
    - `ALTER TABLE ... REORGANIZE PARTITION` により、パーティション順序で再編成対象パーティションの後ろにある非再編成パーティション内の行に対するエントリを持たないままグローバルインデックスが再構築される可能性があり、その結果、それらのインデックスを使用するクエリで行が欠落し、重複したインデックス値の挿入が許される可能性がある問題を修正しました [#70023](https://github.com/pingcap/tidb/issues/70023) @[mjonss](https://github.com/mjonss) <!-- component: ddl --> <!-- pr: https://github.com/pingcap/tidb/pull/70479 -->
    - テーブル結合操作、`UPDATE` 文、および `DELETE` 文で、特に高並行時や幅広い行を処理する場合に、初期 Chunk に過剰なメモリが割り当てられる可能性がある問題を修正しました [#68545](https://github.com/pingcap/tidb/issues/68545) @[solotzg](https://github.com/solotzg) <!-- component: execution --> <!-- pr: https://github.com/pingcap/tidb/pull/69965 -->

+ TiKV

    - 高速な Raftstore メッセージバッチに対して TiKV が不要な slow-log メッセージ整形を行い、追加の CPU オーバーヘッドが発生する問題を修正しました [#19861](https://github.com/tikv/tikv/issues/19861) @[pingyu](https://github.com/pingyu) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19910 -->
    - 不正な UTF-8 入力またはパターン、`BIT` 値、あるいは特定の照合順序を含む pushdown された `LIKE` 式をコプロセッサーが評価する際に、TiKV が panic を起こす可能性がある問題を修正しました [#66597](https://github.com/pingcap/tidb/issues/66597) [#67082](https://github.com/pingcap/tidb/issues/67082) [#19811](https://github.com/tikv/tikv/issues/19811) @[jebter](https://github.com/jebter) <!-- component: execution, tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19893 --> <!-- pr: https://github.com/tikv/tikv/pull/19894 -->
    - 外部 SST 取り込み時に、取り込みとフォアグラウンド書き込みが競合すると TiKV が不整合な MVCC 状態を生成し、トランザクション状態チェックで panic を引き起こす可能性がある問題を修正しました [#19891](https://github.com/tikv/tikv/issues/19891) @[gengliqi](https://github.com/gengliqi) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19916 -->
    - FIPS 環境で `ENABLE_FIPS=1` を指定して TiKV をビルドできない問題を修正しました [#19743](https://github.com/tikv/tikv/issues/19743) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19753 --> <!-- pr: https://github.com/tikv/tikv/pull/19904 --> <!-- pr: https://github.com/tikv/tikv/pull/19754 -->
    - バックグラウンドタスクのリソース制御のみを有効にした場合に、TiKV が不要にトランザクションスケジューラを優先度スケジューリングへ切り替えるため、書き込み負荷の高いワークロードで 5% から 10% の性能低下が発生する問題を修正しました [#19858](https://github.com/tikv/tikv/issues/19858) @[glorv](https://github.com/glorv) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19895 -->
    - `tidb` モードでの TiDB Lightning データインポート中に TiKV がクラッシュする可能性がある問題を修正しました [#18671](https://github.com/tikv/tikv/issues/18671) @[Dog-Du](https://github.com/Dog-Du) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19907 -->
    - etcd compaction エラー後に TiKV In-Memory Engine がリージョンラベルの更新を停止し、label watch が無期限にリトライし続ける問題を修正しました [#19792](https://github.com/tikv/tikv/issues/19792) @[akashchakrabortymsc-cmd](https://github.com/akashchakrabortymsc-cmd) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19898 -->
    - インメモリエンジンのキャッシュウォームアップが停止した状態で ACK の期限前に transfer リクエストが繰り返し到着すると、リージョンの Leader 転送が無期限にブロックされる可能性がある問題を修正しました [#19776](https://github.com/tikv/tikv/issues/19776) @[overvenus](https://github.com/overvenus) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19921 -->
    - 一時的な RocksDB compaction スパイク時に、TiKV が不要な書き込みフロー制御を適用する可能性がある問題を修正しました [#19667](https://github.com/tikv/tikv/issues/19667) @[hbisheng](https://github.com/hbisheng) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19828 -->
    - 対象ストアの登録完了前に PD が一時的に store-not-found エラーを返すと、TiKV が Raft 接続を恒久的にブロックする可能性がある問題を修正しました [#19980](https://github.com/tikv/tikv/issues/19980) @[LykxSassinator](https://github.com/LykxSassinator) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19999 --> <!-- exported-on-2026-08-24 -->
    - TiKV における外部 SST 取り込みでフォアグラウンド書き込みが許可されなくなり、取り込み中の書き込みレイテンシーが増加する問題を修正しました [#19954](https://github.com/tikv/tikv/issues/19954) @[gengliqi](https://github.com/gengliqi) <!-- component: tikv --> <!-- pr: https://github.com/tikv/tikv/pull/19977 --> <!-- exported-on-2026-08-24 -->

+ PD

    - PD `/metric/query` および `/metric/query_range` が SSRF に悪用されたり、上流レスポンスの詳細を露出したりする可能性がある問題を修正しました @[rleungx](https://github.com/rleungx) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11107 -->
    - 同じリソースグループ内でリクエストレートが不均一な場合に、RU トークンが TiDB インスタンス間で不均等に割り当てられ、高需要インスタンスで RU 待機時間の増加とレイテンシー上昇を引き起こす問題を修正しました [#9605](https://github.com/tikv/pd/issues/9605) @[JmPotato](https://github.com/JmPotato) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/10024 -->
    - クライアントが任意の `ConfigPath` またはパス形式の設定名を指定した場合に、PD GlobalConfig gRPC API が意図した名前空間外の etcd キーへアクセスする可能性がある問題を修正しました [#11079](https://github.com/tikv/pd/issues/11079) @[rleungx](https://github.com/rleungx) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11075 -->
    - `pd-forwarded-host` で渡された呼び出し元指定のアドレスに対して、現在の PD leader の advertised client URLs に転送先を制限せず、PD が外向き gRPC 接続を確立してしまう可能性がある問題を修正しました [#11070](https://github.com/tikv/pd/issues/11070) @[rleungx](https://github.com/rleungx) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11091 -->
    - 新しく作成されたリソースグループコントローラが定期的な状態更新と競合した場合に、resource group client が `NaN` トークンリクエストを恒久的に送信し続ける可能性がある問題を修正しました [#11022](https://github.com/tikv/pd/issues/11022) @[JmPotato](https://github.com/JmPotato) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11028 -->
    - PD Resource Manager の leader ハンドオフ後、または新しい TiDB インスタンス参加時に、新しい Resource Control client が RU 割り当て 0 を受け取る可能性があり、一時的なレイテンシースパイクや `ERROR 8252 Exceeded resource group quota limitation` を引き起こす問題を修正しました [#11148](https://github.com/tikv/pd/issues/11148) @[JmPotato](https://github.com/JmPotato) <!-- component: pd --> <!-- pr: https://github.com/tikv/pd/pull/11150 --> <!-- exported-on-2026-08-24 -->

+ TiFlash

    - TiFlash のリソース制御によりローカル admission controller トークンが低い水準のまま残り、トラフィックバースト時にリクエストがキューに残り続けたり、予期せずスロットリングされたりする問題を修正しました [#10996](https://github.com/pingcap/tiflash/issues/10996) @[yongman](https://github.com/yongman) <!-- component: tiflash --> <!-- pr: https://github.com/pingcap/tiflash/pull/11015 --> <!-- exported-on-2026-08-24 -->

+ Tools

    + Backup & Restore (BR)

        - point-in-time recovery 中に BR のログリストアが設定されたレート制限を適用せず、ログ適用ダウンロード速度が制限を超える問題を修正しました [#63505](https://github.com/pingcap/tidb/issues/63505) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/pingcap/tidb/pull/69153 -->
        - `AUTO_ID_CACHE=1` を持つテーブルに対する BR point-in-time restore で、リストア後最初の `INSERT` 時に重複キーエラーが発生する可能性がある問題を修正しました [#69485](https://github.com/pingcap/tidb/issues/69485) @[vldmit](https://github.com/vldmit) <!-- component: br --> <!-- pr: https://github.com/pingcap/tidb/pull/70253 -->
        - ログバックアップタスク停止後に BR ログバックアップが古い GC safepoint を残し、クリーンアップや safepoint 管理に影響する可能性がある問題を修正しました [#19832](https://github.com/tikv/tikv/issues/19832) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/tikv/tikv/pull/19911 -->
        - 複数のリストアタスクが同時実行される場合に、BR が SST ダウンロードのレート制限を正しく更新できず、あるタスクの制限変更が反映されない可能性がある問題を修正しました [#19454](https://github.com/tikv/tikv/issues/19454) @[Leavrth](https://github.com/Leavrth) <!-- component: br --> <!-- pr: https://github.com/tikv/tikv/pull/19924 -->

    + TiCDC

        - maintainer フェイルオーバー中に TiCDC が重複した dispatcher を作成し、下流で書き込み競合を引き起こす可能性がある問題を修正しました [#5083](https://github.com/pingcap/ticdc/issues/5083) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5788 --> <!-- pr: https://github.com/pingcap/ticdc/pull/5792 --> <!-- pr: https://github.com/pingcap/ticdc/pull/5791 -->
        - Kafka controller 障害後に、TiCDC が上流と下流の間で不整合なデータを生成する可能性がある問題を修正しました [#5437](https://github.com/pingcap/ticdc/issues/5437) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5773 -->
        - 既存の changefeed ID メタデータが JSON 内で `keyspace` ではなく旧来の `namespace` フィールドを使用している場合、TiCDC アップグレード後に changefeed が消える可能性がある問題を修正しました [#4079](https://github.com/pingcap/ticdc/issues/4079) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5332 -->
        - `CREATE TABLE ... LIKE ...` をレプリケートする際に、参照元テーブルが changefeed によってフィルタリングされていると、TiCDC の checkpoint 進行が停止する問題を修正しました [#5150](https://github.com/pingcap/ticdc/issues/5150) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5951 -->
        - changefeed の完了、停止、削除、または別 owner への移動後も、TiCDC owner の checkpoint timestamp および lag メトリクスが古いまま残る問題を修正しました [#5490](https://github.com/pingcap/ticdc/issues/5490) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5766 -->
        - TiCDC の新アーキテクチャで、TiCDC フェイルオーバーまたは dispatcher リセット後に changefeed が停止する可能性がある問題を修正しました [#5553](https://github.com/pingcap/ticdc/issues/5553) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5769 -->
        - TiCDC maintainer が削除されてシャットダウン引き継ぎが開始された後も、dispatcher の再スケジュールまたは再作成を続ける可能性がある問題を修正しました [#4827](https://github.com/pingcap/ticdc/issues/4827) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5403 -->
        - `ScanLock` の対象 timestamp により TiKV ローカル MaxTS が最新の PD TSO を超えて進む可能性があるため、残存する async-commit ロックに対する TiCDC の stale-lock 解決が失敗する問題を修正しました [#5418](https://github.com/pingcap/ticdc/issues/5418) @[tenfyzhong](https://github.com/tenfyzhong) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5753 -->
        - テーブル削除後に TiCDC event service が同じ raw event を繰り返しスキャンし、スキャン進行が停止する問題を修正しました [#5040](https://github.com/pingcap/ticdc/issues/5040) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5765 -->
        - maintainer フェイルオーバーにより進行中の scheduling または merge operator が不整合なまま残り、TiCDC のテーブルスケジューリングが自動的に収束しなくなる問題を修正しました [#4763](https://github.com/pingcap/ticdc/issues/4763) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5817 -->
        - フロー制御によってリージョンイベントの push が一時停止している場合に、graceful shutdown 中の TiCDC がハングする可能性がある問題を修正しました [#5608](https://github.com/pingcap/ticdc/issues/5608) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5754 -->
        - maintainer の確認応答が到着する前に TiCDC の table-trigger checkpoint が add-table DDL を追い越して進み、新しく追加されたテーブル dispatcher が後続のテーブル DDL をスキップする問題を修正しました [#5401](https://github.com/pingcap/ticdc/issues/5401) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5787 -->
        - 同じ maintainer heartbeat 内で checkpoint 進行が進んだ場合に、TiCDC がリトライ不能な changefeed エラーを無視し、failed 状態に入らず normal のままになる問題を修正しました [#5246](https://github.com/pingcap/ticdc/issues/5246) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5771 -->
        - Avro または Debezium-Avro を使用する TiCDC changefeed で、Schema Registry が HTTP 500 エラーを返しても正常状態を報告し続ける可能性がある問題を修正しました。影響を受ける changefeed は現在、`last_warning` に registry エラーを含む warning 状態を報告します [#5653](https://github.com/pingcap/ticdc/issues/5653) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5823 -->
        - coordinator が設定された scheduler concurrency 制限を尊重しないため、多数のアイドル changefeed を一括作成すると TiCDC のメモリおよび CPU 使用量が急増する可能性がある問題を修正しました [#4831](https://github.com/pingcap/ticdc/issues/4831) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5396 -->
        - 削除されたビューが物理テーブルとして誤ってスケジュールされ、孤立した dispatcher が残ることで、capture 置き換え後に TiCDC changefeed の checkpoint が停止する可能性がある問題を修正しました [#5710](https://github.com/pingcap/ticdc/issues/5710) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5770 -->
        - ハードコードされた最大互換バージョンのため、新アーキテクチャで TiCDC が新しい PD、TiKV、または TiCDC バージョンを誤って拒否する可能性がある問題を修正しました [#4681](https://github.com/pingcap/ticdc/issues/4681) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5327 -->
        - changefeed 作成直後に consumer が開始されると、TiCDC Kafka changefeed が broker のデフォルトパーティション設定でトピックを作成し、メッセージ配信失敗やレプリケーション遅延増加を引き起こす可能性がある問題を修正しました [#5896](https://github.com/pingcap/ticdc/issues/5896) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5897 -->
        - 古い TiCDC capture が etcd セッションを失った後も下流への書き込みを続け、フェイルオーバー中に重複または安全でない下流書き込みを引き起こす可能性がある問題を修正しました [#5202](https://github.com/pingcap/ticdc/issues/5202) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5764 -->
        - 共有下流接続プールが枯渇した後、DML セッションによって DDL およびメタデータ操作がブロックされると、TiCDC MySQL sink がハングする可能性がある問題を修正しました [#5360](https://github.com/pingcap/ticdc/issues/5360) @[hongyunyan](https://github.com/hongyunyan) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5763 -->
        - すべての基盤リージョンが初期スキャンを完了する前に、TiCDC が subscription span を初期化済みとしてマークし、初期化依存の操作が早すぎるタイミングでトリガーされる可能性がある問題を修正しました [#5658](https://github.com/pingcap/ticdc/issues/5658) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5757 -->
        - `cdc cli changefeed resume` が実行中の changefeed に対して成功を報告し、無効な resume リクエストに対して不要な一時 resume GC guard を作成する問題を修正しました [#4893](https://github.com/pingcap/ticdc/issues/4893) @[wlwilliamx](https://github.com/wlwilliamx) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5328 -->
        - sink URI 検証失敗時に、TiCDC が OpenAPI エラーメッセージおよびログ内で機密性の高い sink URI 情報を露出する可能性がある問題を修正しました [#5094](https://github.com/pingcap/ticdc/issues/5094) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5762 -->
        - checkpoint 進行後に、TiCDC の Kafka、Pulsar、および storage consumer が順序外に再生された DML イベントを無視し、下流データ不整合を引き起こす可能性がある問題を修正しました [#5713](https://github.com/pingcap/ticdc/issues/5713) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5833 -->
        - フェイルオーバーまたはメッセージ順序入れ替わり時に、対応する DDL が処理される前に TiCDC 下流 consumer が DML イベントを適用し、`Unknown column` などのエラーを引き起こす問題を修正しました [#5587](https://github.com/pingcap/ticdc/issues/5587) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5778 -->
        - 初期スキーマスナップショットが上流 GC によって失われている場合に、TiCDC schema store の初期化が永遠にリトライされ、ネットワーク分断などの障害から回復した後も changefeed が停止したままになる問題を修正しました [#3249](https://github.com/pingcap/ticdc/issues/3249) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5768 -->
        - 不正な heartbeat または congestion-control メッセージを受信した際に、TiCDC が changefeed スキャンクォータをリークしたり panic を起こしたりする可能性がある問題を修正しました [#5642](https://github.com/pingcap/ticdc/issues/5642) @[lidezhu](https://github.com/lidezhu) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5752 -->
        - DR Auto-Sync シナリオで、古い tiflow 依存関係によりネットワーク分断中に TiCDC が TiKV panic を引き起こす可能性がある問題を修正しました [#5774](https://github.com/pingcap/ticdc/issues/5774) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5780 -->
        - イベント数と総バイト数の両方に基づく event collector のバッチ処理をサポートし、changefeed 設定でバッチ上書きを可能にすることで、redo apply が複数回実行された際に TiCDC がメモリ不足になる問題を修正しました [#5950](https://github.com/pingcap/ticdc/issues/5950) @[3AceShowHand](https://github.com/3AceShowHand) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5942 -->
        - event-service のスキャンウィンドウが固定され、DDL barrier が進行できない場合に、パーティションテーブルでの `TRUNCATE TABLE` 後に TiCDC changefeed が停止する可能性がある問題を修正しました [#4365](https://github.com/pingcap/ticdc/issues/4365) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5761 -->
        - グローバルスキャンウィンドウが固定され、dispatcher に保留中の syncpoint barrier がある場合に、TiCDC event service のスキャン進行が停止する可能性がある問題を修正しました [#5546](https://github.com/pingcap/ticdc/issues/5546) @[asddongmen](https://github.com/asddongmen) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/5761 -->
        - 重複した dispatcher を作成し、下流データ不整合を引き起こす可能性がある TiCDC の race condition を修正しました [#6069](https://github.com/pingcap/ticdc/issues/6069) @[wk989898](https://github.com/wk989898) <!-- component: cdc --> <!-- pr: https://github.com/pingcap/ticdc/pull/6086 --> <!-- exported-on-2026-08-26 -->

    + TiDB Lightning

        - 一時的な conflict-deletion commit エラー後に、`IMPORT INTO` が不整合なインデックスを伴ったまま成功を報告する可能性がある問題を修正しました [#69792](https://github.com/pingcap/tidb/issues/69792) @[D3Hunter](https://github.com/D3Hunter) <!-- component: lightning --> <!-- pr: https://github.com/pingcap/tidb/pull/70254 -->
        - ローカルエンジンファイルが正しくクリーンアップされない場合に、インポートエラーまたはリトライ後の `IMPORT INTO` が `lock held by current process` エラーで失敗する可能性がある問題を修正しました [#65645](https://github.com/pingcap/tidb/issues/65645) @[D3Hunter](https://github.com/D3Hunter) <!-- component: lightning --> <!-- pr: https://github.com/pingcap/tidb/pull/69478 -->
        - 繰り返し出現する辞書エンコードされた Parquet `DECIMAL` 値に対して、`IMPORT INTO` が誤った値を黙って書き込む問題を修正しました [#70365](https://github.com/pingcap/tidb/issues/70365) @[joechenrh](https://github.com/joechenrh) <!-- component: lightning --> <!-- pr: https://github.com/pingcap/tidb/pull/70461 -->
        - ジョブ生成がキャンセルされた場合に、`IMPORT INTO` または関連するローカルバックエンド取り込みタスクがハングする可能性がある問題を修正しました [#69240](https://github.com/pingcap/tidb/issues/69240) @[D3Hunter](https://github.com/D3Hunter) <!-- component: lightning, dxf --> <!-- pr: https://github.com/pingcap/tidb/pull/70234 -->

> **Note:**
>
> これらのリリースノートでは、TiDB v8.5.8 におけるユーザー向けの変更点に焦点を当てています。v8.5.7 と v8.5.8 の間のコード変更については、GitHub の [#68750](https://github.com/pingcap/tidb/issues/68750#issuecomment-5436067898) を参照してください。