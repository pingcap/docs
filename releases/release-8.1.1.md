---
title: TiDB 8.1.1 Release Notes
summary: TiDB 8.1.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 8.1.1 リリースノート {#tidb-8-1-1-release-notes}

発売日：2024年8月27日

TiDB バージョン: 8.1.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB Lightningを使用してCSVファイルをインポートする際、並列性とインポートパフォーマンスを向上させるために大きなCSVファイルを複数の小さなCSVファイルに分割するために`strict-format = true`設定する場合は、明示的に`terminator`を指定する必要があります。値は`\r` 、または`\r\n` `\n`かです。行末文字を指定しないと、CSVファイルデータの解析時に例外が発生する可能性があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [lance6716](https://github.com/lance6716)
-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用してCSVファイルをインポートする際、 `SPLIT_FILE`パラメータを指定して大きなCSVファイルを複数の小さなCSVファイルに分割し、同時実行性とインポートパフォーマンスを向上させる場合は、行末文字`LINES_TERMINATED_BY`を明示的に指定する必要があります。値は`\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSVファイルデータの解析時に例外が発生する可能性があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [lance6716](https://github.com/lance6716)
-   並列計算中のディスクオーバーフローによるクエリ結果の誤りを回避するため、変数[`tidb_enable_parallel_hashagg_spill`](https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800)のデフォルト値を`ON`から`OFF`に変更してください。v8.0.0またはv8.1.0からv8.1.1にアップグレードしたクラスターの場合、この変数はアップグレード後もデフォルト値の`ON`のままとなるため、手動で`OFF`に変更することをお勧めします[＃55290](https://github.com/pingcap/tidb/issues/55290) @ [xzhangxian1008](https://github.com/xzhangxian1008)
-   TiKV構成項目[`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)のスコープを変更します。

    -   v8.1.0 では、この構成項目は TiKV ノード間の gRPC メッセージの圧縮アルゴリズムにのみ影響します。
    -   v8.1.1以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)

## オフラインパッケージの変更 {#offline-package-changes}

v8.1.1 では、 `TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から`arbiter`が削除されます。

## 改善点 {#improvements}

-   TiDB

    -   TiFlash配置ルールを一括削除することで、パーティションテーブルで`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。 [＃54068](https://github.com/pingcap/tidb/issues/54068) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   MPP ロード バランシング中にリージョンのないストアを削除する [＃52313](https://github.com/pingcap/tidb/issues/52313) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   TiKV の高負荷時に広範囲にわたるタイムアウトを回避するために、統計を同期的にロードするタスクの優先度を一時的に高く調整します。タイムアウトにより、統計がロードされない可能性があります[＃50332](https://github.com/pingcap/tidb/issues/50332) @ [winoros](https://github.com/winoros)
    -   `EXPLAIN`ステートメントは`tidb_redact_log`設定の適用をサポートし、ログ処理ロジックをさらに最適化します。
    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログの処理ロジックをさらに最適化することをサポート [＃54565](https://github.com/pingcap/tidb/issues/54565) @ [hawkingrei](https://github.com/hawkingrei)

-   PD

    -   HTTPクライアントの再試行ロジックを改善する [＃8142](https://github.com/tikv/pd/issues/8142) @ [JmPotato](https://github.com/JmPotato)

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [windtalker](https://github.com/windtalker)
    -   同時実行性の高いデータ読み取り操作におけるロック競合を減らし、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   ログバックアップ中に生成される一時ファイルの暗号化をサポート[＃15083](https://github.com/tikv/tikv/issues/15083) @ [YuJuncen](https://github.com/YuJuncen)
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [Leavrth](https://github.com/Leavrth)
        -   環境変数を介した Alibaba Cloud アクセス資格情報の設定をサポート [＃45551](https://github.com/pingcap/tidb/issues/45551) @ [RidRisR](https://github.com/RidRisR)
        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラーを返します。 [＃17224](https://github.com/tikv/tikv/issues/17224) @ [RidRisR](https://github.com/RidRisR)

    -   TiCDC

        -   シンプルプロトコルを使用したチェンジフィードが開始されたときに、すべてのテーブルの BOOTSTRAP メッセージをダウンストリームに一度に送信することをサポートします。 [＃11315](https://github.com/pingcap/tiflow/issues/11315) @ [asddongmen](https://github.com/asddongmen)
        -   ダウンストリームがメッセージキュー（MQ）またはクラウドストレージの場合、生のイベントを直接出力することをサポート[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   HashAgg 演算子のディスク スピルにより並列計算中に誤ったクエリ結果が発生する問題を修正しました。 [＃55290](https://github.com/pingcap/tidb/issues/55290) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   SQLが異常に中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   厳密に自己増分ではないRANGEパーティションテーブルが作成できる問題を修正 [＃54829](https://github.com/pingcap/tidb/issues/54829) @ [Defined2014](https://github.com/Defined2014)
    -   `_tidb_rowid`の`PointGet`実行プランが生成できる問題を修正 [＃54583](https://github.com/pingcap/tidb/issues/54583) @ [Defined2014](https://github.com/Defined2014)
    -   スローログ内の内部SQL文がデフォルトでnullに編集される問題を修正[＃54190](https://github.com/pingcap/tidb/issues/54190) [＃52743](https://github.com/pingcap/tidb/issues/52743) [＃53264](https://github.com/pingcap/tidb/issues/53264) @ [lcwangchao](https://github.com/lcwangchao)
    -   `UPDATE`操作で複数テーブルシナリオで TiDB OOM が発生する可能性がある問題を修正 [＃53742](https://github.com/pingcap/tidb/issues/53742) @ [hawkingrei](https://github.com/hawkingrei)
    -   関連するサブクエリがある場合にウィンドウ関数がpanic可能性がある問題を修正[＃42734](https://github.com/pingcap/tidb/issues/42734) @ [hi-rustin](https://github.com/hi-rustin)
    -   照合順序が`utf8_bin`または`utf8mb4_bin` の場合に`LENGTH()`条件が予期せず削除される問題を修正しました [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [elsa0520](https://github.com/elsa0520)
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panicが発生する可能性がある問題を修正しました。 [＃53540](https://github.com/pingcap/tidb/issues/53540) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   `?`の引数を含む`CONV`の式を持つ`PREPARE` `EXECUTE`ステートメントを複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   再帰CTE演算子がメモリ使用量を誤って追跡する問題を修正しました [＃54181](https://github.com/pingcap/tidb/issues/54181) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   `SHOW WARNINGS;`使用して警告を取得するとpanicが発生する可能性がある問題を修正しました [＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   TopN演算子が誤ってプッシュダウンされる可能性がある問題を修正しました [＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)
    -   常に`true` となる述語を持つ`SHOW ERRORS`ステートメントを実行すると TiDB がパニックを起こす問題を修正しました。 [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [elsa0520](https://github.com/elsa0520)
    -   `STATE`フィールドのうち`size`が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`テーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [hawkingrei](https://github.com/hawkingrei)
    -   DDL ステートメントが etcd を誤って使用し、タスクがキューに入れられる問題を修正しました。 [＃52335](https://github.com/pingcap/tidb/issues/52335) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   グローバル統計の`Distinct_count`情報が間違っている可能性がある問題を修正しました[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [hawkingrei](https://github.com/hawkingrei)
    -   自動統計収集中にシステム変数`tidb_enable_async_merge_global_stats`と`tidb_analyze_partition_concurrency`有効にならない問題を修正[＃53972](https://github.com/pingcap/tidb/issues/53972) @ [hi-rustin](https://github.com/hi-rustin)
    -   最初の引数が`month`で、2番目の引数が負の場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。 [＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   ハンドシェイクが完了する前に一部の接続が終了した場合に、Grafana の接続数監視メトリックが正しくない問題を修正しました[＃54428](https://github.com/pingcap/tidb/issues/54428) @ [YangKeao](https://github.com/YangKeao)
    -   TiProxy とリソース グループを使用するときに、各リソース グループの接続数が正しくない問題を修正しました。 [＃54545](https://github.com/pingcap/tidb/issues/54545) @ [YangKeao](https://github.com/YangKeao)
    -   再帰CTE でビューの使用が機能しない問題を修正 [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [hawkingrei](https://github.com/hawkingrei)
    -   大規模並列処理 (MPP) で`final` AggMode と`non-final` AggMode が共存できない問題を修正しました [＃51362](https://github.com/pingcap/tidb/issues/51362) @ [AilinKid](https://github.com/AilinKid)
    -   オプティマイザーヒント使用時に誤った警告情報が表示される問題を修正しました [＃53767](https://github.com/pingcap/tidb/issues/53767) @ [hawkingrei](https://github.com/hawkingrei)
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。 [＃54005](https://github.com/pingcap/tidb/issues/54005) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   場合によっては無効な列タイプ`DECIMAL(0,0)`が作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [tangenta](https://github.com/tangenta)
    -   `(*PointGetPlan).StatsInfo()` の実行中に発生する可能性のあるデータ競合の問題を修正しました [＃43339](https://github.com/pingcap/tidb/issues/43339) @ [qw4990](https://github.com/qw4990) [＃49803](https://github.com/pingcap/tidb/issues/49803)
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正しました[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [zimulala](https://github.com/zimulala)
    -   JSON関連の関数がMySQLと矛盾するエラーを返す場合がある問題を修正[＃53799](https://github.com/pingcap/tidb/issues/53799) @ [dveeden](https://github.com/dveeden)
    -   外部キーを持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました。 [＃53652](https://github.com/pingcap/tidb/issues/53652) @ [hawkingrei](https://github.com/hawkingrei)
    -   `memory_quota`ヒントがサブクエリで機能しない可能性がある問題を修正しました [＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)
    -   起動時に統計情報をロードするときに、TiDB が GC によるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [you06](https://github.com/you06)
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラーが発生する可能性がある問題を修正 [＃53673](https://github.com/pingcap/tidb/issues/53673) @ [tangenta](https://github.com/tangenta)
    -   情報スキーマキャッシュミスにより、古い読み取りのクエリレイテンシーが増加する問題を修正しました。 [＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   データ変更操作を含むトランザクションで仮想列を持つテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました [＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)
    -   `auth_socket`認証プラグインを使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。 [＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)
    -   クエリに非相関サブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適でないプランになる可能性がある問題を修正しました。 [＃54213](https://github.com/pingcap/tidb/issues/54213) @ [qw4990](https://github.com/qw4990)
    -   BIGINT 以外の符号なし整数が文字列/小数点と比較されたときに誤った結果を生成する可能性がある問題を修正しました [＃41736](https://github.com/pingcap/tidb/issues/41736) @ [LittleFall](https://github.com/LittleFall)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加するときに設定`max-index-length`で TiDB がpanicになる問題を修正しました [＃53281](https://github.com/pingcap/tidb/issues/53281) @ [zimulala](https://github.com/zimulala)
    -   クエリ内の特定のフィルタ条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) を報告する可能性がある問題を修正しました [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [YangKeao](https://github.com/YangKeao) [＃53594](https://github.com/pingcap/tidb/issues/53594)
    -   再帰CTEクエリが無効なポインタを生成する可能性がある問題を修正しました [＃54449](https://github.com/pingcap/tidb/issues/54449) @ [hawkingrei](https://github.com/hawkingrei)
    -   述語の`Longlong`型のオーバーフローの問題を修正 [＃45783](https://github.com/pingcap/tidb/issues/45783) @ [hawkingrei](https://github.com/hawkingrei)
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列を見つけられない問題を修正しました [＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [ekexium](https://github.com/ekexium)
    -   列のデフォルト値として`CURRENT_DATE()`使用すると、クエリ結果が正しくなくなる問題を修正しました [＃53746](https://github.com/pingcap/tidb/issues/53746) @ [tangenta](https://github.com/tangenta)
    -   グローバルソートを使用してインデックスを追加するときにパフォーマンスが不安定になる問題を修正しました [＃54147](https://github.com/pingcap/tidb/issues/54147) @ [tangenta](https://github.com/tangenta)
    -   v7.1 からアップグレードした後に`SHOW IMPORT JOBS`エラー`Unknown column 'summary'`を報告する問題を修正しました [＃54241](https://github.com/pingcap/tidb/issues/54241) @ [tangenta](https://github.com/tangenta)
    -   `root`ユーザーが`tidb_mdl_view` を照会できない問題を修正 [＃53292](https://github.com/pingcap/tidb/issues/53292) @ [tangenta](https://github.com/tangenta)
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加する際のネットワーク パーティションによって、データ インデックスの不整合が発生する可能性がある問題を修正しました。 [＃54897](https://github.com/pingcap/tidb/issues/54897) @ [tangenta](https://github.com/tangenta)
    -   TiDB Lightning物理インポートモードの初期化中にエラーが発生し、リソースリークが発生する可能性がある問題を修正[＃53659](https://github.com/pingcap/tidb/issues/53659) @ [D3Hunter](https://github.com/D3Hunter)
    -   ビュー定義でサブクエリが列定義として使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告1356が返される問題を修正しました。 [＃54343](https://github.com/pingcap/tidb/issues/54343) @ [lance6716](https://github.com/lance6716)
    -   インデックスアクセラレーションを使用して一意インデックスを追加すると、所有者がに切り替えられたときに`Duplicate entry`エラーが発生する可能性がある問題を修正しました。 [＃49233](https://github.com/pingcap/tidb/issues/49233) @ [lance6716](https://github.com/lance6716)
    -   `global.tidb_cloud_storage_uri` を設定するときに不明瞭なエラーメッセージが表示される問題を修正しました [＃54096](https://github.com/pingcap/tidb/issues/54096) @ [lance6716](https://github.com/lance6716)
    -   同期負荷QPSモニタリングメトリックが正しくない問題を修正[＃53558](https://github.com/pingcap/tidb/issues/53558) @ [hawkingrei](https://github.com/hawkingrei)
    -   初期統計を同時にでロードするときに一部の統計情報が失われる可能性がある問題を修正しました [＃53607](https://github.com/pingcap/tidb/issues/53607) @ [hawkingrei](https://github.com/hawkingrei)
    -   `SELECT ... FOR UPDATE` の間違ったPointGetプランを再利用する問題を修正しました [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)

-   TiKV

    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB に送信されるメッセージには反映されない問題を修正しました。 [＃17176](https://github.com/tikv/tikv/issues/17176) @ [ekexium](https://github.com/ekexium)
    -   `make docker`と`make docker_test`の失敗を修正[＃17075](https://github.com/tikv/tikv/issues/17075) @ [shunki-fujita](https://github.com/shunki-fujita)
    -   **gRPC リクエスト ソースの継続時間**メトリックが監視ダッシュボードに誤って表示される問題を修正しました [＃17133](https://github.com/tikv/tikv/issues/17133) @ [King-Dylan](https://github.com/King-Dylan)
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報が含まれていない問題を修正しました [＃17037](https://github.com/tikv/tikv/issues/17037) @ [glorv](https://github.com/glorv)
    -   `raftstore.periodic-full-compact-start-times`構成項目をオンラインで変更すると、TiKVがpanicを起こす可能性がある問題を修正しました[＃17066](https://github.com/tikv/tikv/issues/17066) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   破損したRaftデータ スナップショットを適用すると TiKV が繰り返しpanic可能性がある問題を修正しました。 [＃15292](https://github.com/tikv/tikv/issues/15292) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   キャッシュエントリが永続化される前に解放すると TiKV がpanicを起こす問題を修正しました [＃17040](https://github.com/tikv/tikv/issues/17040) @ [glorv](https://github.com/glorv)

-   PD

    -   テーブル属性を取得するときに誤った PD API が呼び出される問題を修正しました [＃55188](https://github.com/pingcap/tidb/issues/55188) @ [JmPotato](https://github.com/JmPotato)
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [HuSharp](https://github.com/HuSharp)
    -   一部のログが編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   `Filter`監視メトリックでデータが欠落している問題を修正しました [＃8098](https://github.com/tikv/pd/issues/8098) @ [nolouch](https://github.com/nolouch)
    -   TLS が有効になっているときに HTTP クライアントがpanic可能性がある問題を修正[＃8237](https://github.com/tikv/pd/issues/8237) @ [okJiang](https://github.com/okJiang)
    -   暗号化マネージャーが使用前に初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [rleungx](https://github.com/rleungx)
    -   同時実行性が高い場合にリソース グループがリソース使用量を効果的に制限できない問題を修正[＃8435](https://github.com/tikv/pd/issues/8435) @ [nolouch](https://github.com/nolouch)
    -   `store limit` に関連するデータ競合問題を修正 [＃8253](https://github.com/tikv/pd/issues/8253) @ [lhy1024](https://github.com/lhy1024)
    -   `scheduling`マイクロサービスが有効化された後にスケーリングの進行状況が正しく表示されない問題を修正しました [＃8331](https://github.com/tikv/pd/issues/8331) @ [rleungx](https://github.com/rleungx)
    -   `tso`マイクロサービスが有効になった後、TSO ノードが動的に更新されない問題を修正[＃8154](https://github.com/tikv/pd/issues/8154) @ [rleungx](https://github.com/rleungx)
    -   リソースグループのデータ競合問題を修正 [＃8267](https://github.com/tikv/pd/issues/8267) @ [HuSharp](https://github.com/HuSharp)
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [nolouch](https://github.com/nolouch)
    -   PDリーダーを手動で転送すると失敗する可能性がある問題を修正しました [＃8225](https://github.com/tikv/pd/issues/8225) @ [HuSharp](https://github.com/HuSharp)
    -   削除されたノードがetcdクライアントの候補接続リストにまだ表示される問題を修正 [＃8286](https://github.com/tikv/pd/issues/8286) @ [JmPotato](https://github.com/JmPotato)
    -   `ALTER PLACEMENT POLICY`配置ポリシー を変更できない問題を修正 [＃51712](https://github.com/pingcap/tidb/issues/51712) @ [jiyfhust](https://github.com/jiyfhust) [＃52257](https://github.com/pingcap/tidb/issues/52257)
    -   書き込みホットスポットのスケジュール設定により配置ポリシーの制約が破られる可能性がある問題を修正[＃7848](https://github.com/tikv/pd/issues/7848) @ [lhy1024](https://github.com/lhy1024)
    -   配置ルールを使用しているときに、ダウンしたピアが回復しない可能性がある問題を修正しました。 [＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)
    -   リソースグループクエリをキャンセルするときに再試行回数が多すぎる問題を修正 [＃8217](https://github.com/tikv/pd/issues/8217) @ [nolouch](https://github.com/nolouch)
    -   PD がオペレータ チェック中に遭遇するデータ競合問題を修正しました [＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)
    -   ロールをリソースグループにバインドするときにエラーが報告されない問題を修正しました [＃54417](https://github.com/pingcap/tidb/issues/54417) @ [JmPotato](https://github.com/JmPotato)
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPD panicが発生する問題を修正しました [＃8323](https://github.com/tikv/pd/issues/8323) @ [JmPotato](https://github.com/JmPotato)

-   TiFlash

    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラーが発生する可能性がある問題を修正しました。 [＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash のクラッシュを引き起こす可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   BRまたはTiDB Lightning 経由でデータをインポートした後、FastScanモードで多数の重複行が読み取られる可能性がある問題を修正しました。 [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [JinheLin](https://github.com/JinheLin)
    -   データベースが作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlash が起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   分散ストレージおよびコンピューティングアーキテクチャで、DDL操作で非NULL列を追加した後にクエリでNULL値が誤って返される可能性がある問題を修正しました。 [＃9084](https://github.com/pingcap/tiflash/issues/9084) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   データベースにまたがる空のパーティションを持つパーティションテーブルで`RENAME TABLE ... TO ...`実行した後にTiFlash がpanic可能性がある問題を修正しました。 [＃9132](https://github.com/pingcap/tiflash/issues/9132) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   空のパーティションを含むパーティション テーブルでクエリを実行するときに発生するクエリ タイムアウトの問題を修正しました。 [＃9024](https://github.com/pingcap/tiflash/issues/9024) @ [JinheLin](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される可能性がある問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [JinheLin](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [JinheLin](https://github.com/JinheLin)

-   ツール

    -   Backup & Restore (BR)

        -   リージョンリーダーの探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。 [＃17168](https://github.com/tikv/tikv/issues/17168) @ [Leavrth](https://github.com/Leavrth)
        -   増分バックアップ中の DDL ジョブのスキャンの非効率性の問題を修正 [＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3pointer](https://github.com/3pointer)
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [RidRisR](https://github.com/RidRisR)
        -   空の`EndKey` が原因でBR がトランザクション KV クラスターの復元に失敗する問題を修正しました [＃52574](https://github.com/pingcap/tidb/issues/52574) @ [3pointer](https://github.com/3pointer)
        -   アドバンサーオーナーの移行後にログバックアップが一時停止される可能性がある問題を修正しました [＃53561](https://github.com/pingcap/tidb/issues/53561) @ [RidRisR](https://github.com/RidRisR)
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア中に正しく回復されない可能性がある問題を修正しました。 [＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3pointer](https://github.com/3pointer)
        -   PD接続障害により、ログバックアップアドバンサ所有者が配置されているTiDBインスタンスがpanicになる可能性がある問題を修正しました。 [＃52597](https://github.com/pingcap/tidb/issues/52597) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   リージョンの変更によりダウンストリームpanicが発生する問題を修正[＃17233](https://github.com/tikv/tikv/issues/17233) @ [hicqu](https://github.com/hicqu)
        -   アップストリームで新しい照合順序が無効になっている場合、TiCDC がクラスター化インデックス テーブルの主キーを正しくデコードできない問題を修正しました。 [＃11371](https://github.com/pingcap/tiflow/issues/11371) @ [lidezhu](https://github.com/lidezhu)
        -   `UPDATE`イベントをに分割した後、チェックサムが正しく`0`に設定されない問題を修正しました。 [＃11402](https://github.com/pingcap/tiflow/issues/11402) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   マルチノード環境で大量の`UPDATE`操作を実行する際にChangefeedを繰り返し再起動するとデータの不整合が発生する可能性がある問題を修正[＃11219](https://github.com/pingcap/tiflow/issues/11219) @ [lidezhu](https://github.com/lidezhu)
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   MariaDBデータの移行中に`SET`ステートメントがDM panicを引き起こす問題を修正[＃10206](https://github.com/pingcap/tiflow/issues/10206) @ [dveeden](https://github.com/dveeden)
        -   `go-mysql` にアップグレードして接続ブロックの問題を修正しました [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3Hunter](https://github.com/D3Hunter)
        -   インデックスの長さがデフォルト値の`max-index-length` を超えるとデータレプリケーションが中断される問題を修正しました [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [michaelmdeng](https://github.com/michaelmdeng)
        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラーが発生する問題を修正しました。 [＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightningがキースペース名の取得に失敗した場合、混乱を招く`WARN`ログを出力する問題を修正しました [＃54232](https://github.com/pingcap/tidb/issues/54232) @ [kennytm](https://github.com/kennytm)

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [tangenta](https://github.com/tangenta)

    -   TiDB Binlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`の実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正しました[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [tangenta](https://github.com/tangenta)
