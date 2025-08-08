---
title: TiDB 8.1.1 Release Notes
summary: TiDB 8.1.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 8.1.1 リリースノート {#tidb-8-1-1-release-notes}

発売日：2024年8月27日

TiDB バージョン: 8.1.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDB Lightningを使用してCSVファイルをインポートする際、並列性とインポートパフォーマンスを向上させるために大きなCSVファイルを複数の小さなCSVファイルに分割するために`strict-format = true`設定する場合は、明示的に`terminator`指定する必要があります。指定できる値は`\r` 、または`\r\n` `\n` 。行末文字を指定しないと、CSVファイルデータの解析時に例外が発生する可能性があります[＃37338](https://github.com/pingcap/tidb/issues/37338) @ [ランス6716](https://github.com/lance6716)
-   [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)使用してCSVファイルをインポートする際、並列処理とインポートパフォーマンスを向上させるために、大きなCSVファイルを複数の小さなCSVファイルに分割するパラメータ`SPLIT_FILE`指定する場合は、行末文字`LINES_TERMINATED_BY`明示的に指定する必要があります。指定できる値は`\r` 、 `\n` 、または`\r\n`です。行末文字を指定しないと、CSVファイルデータの解析時に例外が発生する可能性があります。 [＃37338](https://github.com/pingcap/tidb/issues/37338) @ [ランス6716](https://github.com/lance6716)
-   並列計算中のディスクオーバーフローによるクエリ結果の誤りを回避するため、変数[`tidb_enable_parallel_hashagg_spill`](https://docs.pingcap.com/tidb/v8.1/system-variables#tidb_enable_parallel_hashagg_spill-new-in-v800)のデフォルト値を`ON`から`OFF`に変更してください。v8.0.0またはv8.1.0からv8.1.1にアップグレードしたクラスターの場合、この変数はアップグレード後もデフォルト値の`ON`のままとなるため、手動で`OFF`に変更することをお勧めします[＃55290](https://github.com/pingcap/tidb/issues/55290) @ [xzhangxian1008](https://github.com/xzhangxian1008)
-   TiKV構成項目[`server.grpc-compression-type`](/tikv-configuration-file.md#grpc-compression-type)のスコープを変更します。

    -   v8.1.0 では、この構成項目は TiKV ノード間の gRPC メッセージの圧縮アルゴリズムにのみ影響します。
    -   v8.1.1以降、この設定項目はTiKVからTiDBに送信されるgRPC応答メッセージの圧縮アルゴリズムにも影響します。圧縮を有効にすると、CPUリソースの消費量が増加する可能性があります[＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)

## オフラインパッケージの変更 {#offline-package-changes}

v8.1.1 では、 `TiDB-community-toolkit` [バイナリパッケージ](/binary-package.md)から`arbiter`削除されます。

## 改善点 {#improvements}

-   TiDB

    -   TiFlash配置ルールを一括削除することで、パーティションテーブル[＃54068](https://github.com/pingcap/tidb/issues/54068) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`TRUNCATE`または`DROP`操作を実行した後のデータGCの処理速度が向上します。
    -   MPP ロード バランシング[＃52313](https://github.com/pingcap/tidb/issues/52313) @ [xzhangxian1008](https://github.com/xzhangxian1008)中にリージョンのないストアを削除する
    -   TiKV の高負荷時に広範囲にわたるタイムアウトを回避するために、統計を同期的にロードするタスクの優先度を一時的に高く調整します。タイムアウトにより、統計がロードされない可能性があります[＃50332](https://github.com/pingcap/tidb/issues/50332) @ [ウィノロス](https://github.com/winoros)
    -   `EXPLAIN`ステートメントは`tidb_redact_log`設定の適用をサポートし、ログ処理ロジックをさらに最適化します。
    -   `EXPLAIN`ステートメントの出力に`tidb_redact_log`設定を適用し、ログ[＃54565](https://github.com/pingcap/tidb/issues/54565) @ [ホーキングレイ](https://github.com/hawkingrei)の処理ロジックをさらに最適化することをサポート

-   PD

    -   HTTPクライアント[＃8142](https://github.com/tikv/pd/issues/8142)の再試行ロジックの改善[Jmポテト](https://github.com/JmPotato)

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [ウィンドトーカー](https://github.com/windtalker)
    -   同時実行性の高いデータ読み取り操作におけるロック競合を削減し、短いクエリのパフォーマンスを最適化します[＃9125](https://github.com/pingcap/tiflash/issues/9125) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   ログバックアップ中に生成される一時ファイルの暗号化をサポート[＃15083](https://github.com/tikv/tikv/issues/15083) @ [ユジュンセン](https://github.com/YuJuncen)
        -   `br log restore`サブコマンドを除き、他の`br log`サブコマンドはすべて、メモリ消費量を削減するために TiDB `domain`データ構造のロードをスキップすることをサポートしています[＃52088](https://github.com/pingcap/tidb/issues/52088) @ [リーヴルス](https://github.com/Leavrth)
        -   環境変数[＃45551](https://github.com/pingcap/tidb/issues/45551) @ [リドリスR](https://github.com/RidRisR)による Alibaba Cloud アクセス資格情報の設定をサポート
        -   TiKVが各SSTファイルをダウンロードする前に、TiKVのディスク容量が十分かどうかのチェックをサポートします。容量が不足している場合、 BRは復元を終了し、エラー[＃17224](https://github.com/tikv/tikv/issues/17224) @ [リドリスR](https://github.com/RidRisR)を返します。

    -   TiCDC

        -   シンプルプロトコルを使用したチェンジフィードが[＃11315](https://github.com/pingcap/tiflow/issues/11315) @ [アズドンメン](https://github.com/asddongmen)で開始されたときに、すべてのテーブルの BOOTSTRAP メッセージをダウンストリームに一度に送信することをサポートします。
        -   ダウンストリームがメッセージキュー（MQ）またはクラウドstorageの場合に生のイベントを直接出力することをサポートします[＃11211](https://github.com/pingcap/tiflow/issues/11211) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)

## バグ修正 {#bug-fixes}

-   TiDB

    -   HashAgg 演算子のディスク スピルにより並列計算[＃55290](https://github.com/pingcap/tidb/issues/55290) @ [xzhangxian1008](https://github.com/xzhangxian1008)中に誤ったクエリ結果が発生する問題を修正しました
    -   SQLが異常中断されたときに`INDEX_HASH_JOIN`正常に終了できない問題を修正[＃54688](https://github.com/pingcap/tidb/issues/54688) @ [wshwsh12](https://github.com/wshwsh12)
    -   厳密に自己増分ではないRANGEパーティションテーブルが[＃54829](https://github.com/pingcap/tidb/issues/54829) @ [定義2014](https://github.com/Defined2014)で作成できる問題を修正
    -   `_tidb_rowid`の`PointGet`実行プランが[＃54583](https://github.com/pingcap/tidb/issues/54583) @ [定義2014](https://github.com/Defined2014)で生成できる問題を修正
    -   スローログ内の内部SQL文がデフォルトでnullに編集される問題を修正[＃54190](https://github.com/pingcap/tidb/issues/54190) [＃52743](https://github.com/pingcap/tidb/issues/52743) [＃53264](https://github.com/pingcap/tidb/issues/53264) @ [lcwangchao](https://github.com/lcwangchao)
    -   `UPDATE`操作で複数テーブルシナリオ[＃53742](https://github.com/pingcap/tidb/issues/53742) @ [ホーキングレイ](https://github.com/hawkingrei)で TiDB OOM が発生する可能性がある問題を修正
    -   関連するサブクエリがある場合にウィンドウ関数がpanic可能性がある問題を修正[＃42734](https://github.com/pingcap/tidb/issues/42734) @ [ハイラスティン](https://github.com/hi-rustin)
    -   照合順序が`utf8_bin`または`utf8mb4_bin` [＃53730](https://github.com/pingcap/tidb/issues/53730) @ [エルサ0520](https://github.com/elsa0520)の場合に`LENGTH()`条件が予期せず削除される問題を修正しました
    -   トランザクション内のステートメントが OOM によって強制終了された後、TiDB が同じトランザクション内で次のステートメントの実行を継続すると、エラー`Trying to start aggressive locking while it's already started`が発生し、panic[＃53540](https://github.com/pingcap/tidb/issues/53540) @ [ミョンケミンタ](https://github.com/MyonKeminta)が発生する可能性がある問題を修正しました。
    -   `?`引数を含む`CONV` `EXECUTE` `PREPARE`を複数回実行すると、誤ったクエリ結果が返される可能性がある問題を修正しました[＃53505](https://github.com/pingcap/tidb/issues/53505) @ [qw4990](https://github.com/qw4990)
    -   再帰 CTE 演算子がメモリ使用量[＃54181](https://github.com/pingcap/tidb/issues/54181) @ [グオシャオゲ](https://github.com/guo-shaoge)を誤って追跡する問題を修正しました
    -   `SHOW WARNINGS;`使用して警告を取得するとpanicが発生する可能性がある問題を修正[＃48756](https://github.com/pingcap/tidb/issues/48756) @ [xhebox](https://github.com/xhebox)
    -   TopN演算子が誤って[＃37986](https://github.com/pingcap/tidb/issues/37986) @ [qw4990](https://github.com/qw4990)にプッシュダウンされる可能性がある問題を修正しました
    -   常に`true` [＃46962](https://github.com/pingcap/tidb/issues/46962) @ [エルサ0520](https://github.com/elsa0520)となる述語を持つ`SHOW ERRORS`文を実行すると TiDB がパニックを起こす問題を修正しました。
    -   `STATE`のフィールドのうち`size`番目が定義されていないため、 `INFORMATION_SCHEMA.TIDB_TRX`のテーブルの`STATE`フィールドが空になる問題を修正しました[＃53026](https://github.com/pingcap/tidb/issues/53026) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   `SELECT DISTINCT CAST(col AS DECIMAL), CAST(col AS SIGNED) FROM ...`クエリを実行すると誤った結果が返される可能性がある問題を修正[＃53726](https://github.com/pingcap/tidb/issues/53726) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   DDL ステートメントが etcd を誤って使用し、タスクが[＃52335](https://github.com/pingcap/tidb/issues/52335) @ [wjhuang2016](https://github.com/wjhuang2016)でキューに入れられる問題を修正しました。
    -   グローバル統計の`Distinct_count`情報が間違っている可能性がある問題を修正しました[＃53752](https://github.com/pingcap/tidb/issues/53752) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   自動統計収集中にシステム変数`tidb_enable_async_merge_global_stats`と`tidb_analyze_partition_concurrency`有効にならない問題を修正[＃53972](https://github.com/pingcap/tidb/issues/53972) @ [ハイラスティン](https://github.com/hi-rustin)
    -   最初の引数が`month`で、2番目の引数が負の[＃54908](https://github.com/pingcap/tidb/issues/54908) @ [xzhangxian1008](https://github.com/xzhangxian1008)場合に`TIMESTAMPADD()`関数が無限ループに入る問題を修正しました。
    -   ハンドシェイクが完了する前に一部の接続が終了した場合に、Grafana の接続数監視メトリックが正しく表示されない問題を修正しました[＃54428](https://github.com/pingcap/tidb/issues/54428) @ [ヤンケオ](https://github.com/YangKeao)
    -   TiProxy とリソース グループ[＃54545](https://github.com/pingcap/tidb/issues/54545) @ [ヤンケオ](https://github.com/YangKeao)の使用時に各リソース グループの接続数が正しくない問題を修正しました
    -   再帰CTE [＃49721](https://github.com/pingcap/tidb/issues/49721) @ [ホーキングレイ](https://github.com/hawkingrei)でビューの使用が機能しない問題を修正
    -   大規模並列処理 (MPP) [＃51362](https://github.com/pingcap/tidb/issues/51362) @ [アイリンキッド](https://github.com/AilinKid)で`final` AggMode と`non-final` AggMode が共存できない問題を修正しました
    -   オプティマイザーヒント[＃53767](https://github.com/pingcap/tidb/issues/53767) @ [ホーキングレイ](https://github.com/hawkingrei)使用時に誤った警告情報が表示される問題を修正しました
    -   `HashJoin`または`IndexLookUp`演算子が`Apply`演算子[＃54005](https://github.com/pingcap/tidb/issues/54005) @ [徐淮嶼](https://github.com/XuHuaiyu)の駆動側サブノードである場合に`memTracker`切り離されないことで発生する異常に高いメモリ使用量の問題を修正しました。
    -   不正な列タイプ`DECIMAL(0,0)`場合によっては作成される可能性がある問題を修正[＃53779](https://github.com/pingcap/tidb/issues/53779) @ [接線](https://github.com/tangenta)
    -   `(*PointGetPlan).StatsInfo()` [＃49803](https://github.com/pingcap/tidb/issues/49803) [＃43339](https://github.com/pingcap/tidb/issues/43339) @ [qw4990](https://github.com/qw4990)の実行中に発生する可能性のあるデータ競合の問題を修正しました
    -   特定の状況下でプランキャッシュを使用する際に、メタデータロックの不適切な使用によって異常なデータが書き込まれる可能性がある問題を修正[＃53634](https://github.com/pingcap/tidb/issues/53634) @ [ジムララ](https://github.com/zimulala)
    -   JSON関連の関数がMySQLと矛盾するエラーを返す場合がある問題を修正[＃53799](https://github.com/pingcap/tidb/issues/53799) @ [ドヴェーデン](https://github.com/dveeden)
    -   外部キー[＃53652](https://github.com/pingcap/tidb/issues/53652) @ [ホーキングレイ](https://github.com/hawkingrei)を持つテーブルを作成するときに、TiDBが対応する統計メタデータ（ `stats_meta` ）を作成しない問題を修正しました。
    -   `memory_quota`ヒントがサブクエリ[＃53834](https://github.com/pingcap/tidb/issues/53834) @ [qw4990](https://github.com/qw4990)で機能しない可能性がある問題を修正しました
    -   起動時に統計情報をロードするときにTiDBがGCによるエラーを報告する可能性がある問題を修正[＃53592](https://github.com/pingcap/tidb/issues/53592) @ [あなた06](https://github.com/you06)
    -   `CREATE OR REPLACE VIEW`同時に実行すると`table doesn't exist`エラー[＃53673](https://github.com/pingcap/tidb/issues/53673) @ [接線](https://github.com/tangenta)が発生する可能性がある問題を修正
    -   情報スキーマキャッシュミス[＃53428](https://github.com/pingcap/tidb/issues/53428) @ [crazycs520](https://github.com/crazycs520)により、古い読み取りのクエリレイテンシーが増加する問題を修正しました。
    -   クラスター化インデックスを述語として使用すると`SELECT INTO OUTFILE`が機能しない問題を修正[＃42093](https://github.com/pingcap/tidb/issues/42093) @ [qw4990](https://github.com/qw4990)
    -   `YEAR`型の列を範囲外の符号なし整数と比較すると誤った結果が発生する問題を修正[＃50235](https://github.com/pingcap/tidb/issues/50235) @ [qw4990](https://github.com/qw4990)
    -   データ変更操作[＃53951](https://github.com/pingcap/tidb/issues/53951) @ [qw4990](https://github.com/qw4990)を含むトランザクションで仮想列を含むテーブルをクエリすると、TiDB が誤ったクエリ結果を返す可能性がある問題を修正しました
    -   `auth_socket`認証プラグイン[＃54031](https://github.com/pingcap/tidb/issues/54031) @ [lcwangchao](https://github.com/lcwangchao)を使用しているときに、TiDB が認証されていないユーザーの接続を拒否できないことがある問題を修正しました。
    -   クエリに非相関サブクエリと`LIMIT`句が含まれている場合、列のプルーニングが不完全になり、最適でないプラン[＃54213](https://github.com/pingcap/tidb/issues/54213) @ [qw4990](https://github.com/qw4990)になる可能性がある問題を修正しました。
    -   BIGINT 以外の符号なし整数が文字列/小数点[＃41736](https://github.com/pingcap/tidb/issues/41736) @ [リトルフォール](https://github.com/LittleFall)と比較されたときに誤った結果を生成する可能性がある問題を修正しました
    -   設定`max-index-length`で、分散実行フレームワーク（DXF） [＃53281](https://github.com/pingcap/tidb/issues/53281) @ [ジムララ](https://github.com/zimulala)を使用してインデックスを追加するときにTiDBがpanic問題を修正しました。
    -   クエリ内の特定のフィルター条件により、プランナーモジュールが`invalid memory address or nil pointer dereference`エラー[＃53582](https://github.com/pingcap/tidb/issues/53582) [＃53580](https://github.com/pingcap/tidb/issues/53580) [＃53594](https://github.com/pingcap/tidb/issues/53594) [＃53603](https://github.com/pingcap/tidb/issues/53603) @ [ヤンケオ](https://github.com/YangKeao)を報告する可能性がある問題を修正しました
    -   再帰CTEクエリが無効なポインタ[＃54449](https://github.com/pingcap/tidb/issues/54449) @ [ホーキングレイ](https://github.com/hawkingrei)を生成する可能性がある問題を修正しました
    -   述語[＃45783](https://github.com/pingcap/tidb/issues/45783) @ [ホーキングレイ](https://github.com/hawkingrei)の`Longlong`型のオーバーフローの問題を修正
    -   `GROUP BY`ステートメント内の間接プレースホルダ`?`参照が列[＃53872](https://github.com/pingcap/tidb/issues/53872) @ [qw4990](https://github.com/qw4990)を見つけられない問題を修正しました
    -   トランザクションで使用されるメモリが複数回追跡される可能性がある問題を修正[＃53984](https://github.com/pingcap/tidb/issues/53984) @ [エキシウム](https://github.com/ekexium)
    -   列のデフォルト値として`CURRENT_DATE()`使用するとクエリ結果が不正確になる問題を修正[＃53746](https://github.com/pingcap/tidb/issues/53746) @ [接線](https://github.com/tangenta)
    -   グローバルソート[＃54147](https://github.com/pingcap/tidb/issues/54147) @ [接線](https://github.com/tangenta)を使用してインデックスを追加するとパフォーマンスが不安定になる問題を修正しました
    -   v7.1 [＃54241](https://github.com/pingcap/tidb/issues/54241) @ [接線](https://github.com/tangenta)からアップグレードした後に`SHOW IMPORT JOBS`エラー`Unknown column 'summary'`を報告する問題を修正しました
    -   `root`ユーザーが`tidb_mdl_view` [＃53292](https://github.com/pingcap/tidb/issues/53292) @ [接線](https://github.com/tangenta)を照会できない問題を修正
    -   分散実行フレームワーク (DXF) を使用してインデックスを追加する際のネットワーク パーティションによって、データ インデックス[＃54897](https://github.com/pingcap/tidb/issues/54897) @ [接線](https://github.com/tangenta)の不整合が発生する可能性がある問題を修正しました。
    -   TiDB Lightning物理インポートモードの初期化中にエラーが発生し、リソースリークが発生する可能性がある問題を修正[＃53659](https://github.com/pingcap/tidb/issues/53659) @ [D3ハンター](https://github.com/D3Hunter)
    -   ビュー定義[＃54343](https://github.com/pingcap/tidb/issues/54343) @ [ランス6716](https://github.com/lance6716)でサブクエリが列定義として使用されている場合、 `information_schema.columns`を使用して列情報を取得すると警告1356が返される問題を修正しました。
    -   インデックスアクセラレーションを使用して一意のインデックスを追加すると、所有者が[＃49233](https://github.com/pingcap/tidb/issues/49233) @ [ランス6716](https://github.com/lance6716)に切り替えられたときに`Duplicate entry`エラーが発生する可能性がある問題を修正しました。
    -   `global.tidb_cloud_storage_uri` [＃54096](https://github.com/pingcap/tidb/issues/54096) @ [ランス6716](https://github.com/lance6716)を設定するときに不明瞭なエラーメッセージが表示される問題を修正しました
    -   同期ロードQPSモニタリングメトリックが正しくない問題を修正[＃53558](https://github.com/pingcap/tidb/issues/53558) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   初期統計を同時に[＃53607](https://github.com/pingcap/tidb/issues/53607) @ [ホーキングレイ](https://github.com/hawkingrei)でロードするときに一部の統計情報が失われる可能性がある問題を修正しました
    -   `SELECT ... FOR UPDATE` [＃54652](https://github.com/pingcap/tidb/issues/54652) @ [qw4990](https://github.com/qw4990)の間違ったポイント取得プランを再利用する問題を修正しました

-   TiKV

    -   CDC とログバックアップが`advance-ts-interval`構成を使用して`check_leader`のタイムアウトを制限しないため、TiKV が正常に再起動したときに`resolved_ts`遅延が大きくなる場合がある問題を修正しました[＃17107](https://github.com/tikv/tikv/issues/17107) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   gRPC メッセージ圧縮方式を`grpc-compression-type`で設定しても、TiKV から TiDB [＃17176](https://github.com/tikv/tikv/issues/17176) @ [エキシウム](https://github.com/ekexium)に送信されるメッセージには反映されない問題を修正しました。
    -   `make docker`と`make docker_test`の失敗を修正[＃17075](https://github.com/tikv/tikv/issues/17075) @ [藤田俊希](https://github.com/shunki-fujita)
    -   **gRPC リクエスト ソースの継続時間**メトリックが監視ダッシュボード[＃17133](https://github.com/tikv/tikv/issues/17133) @ [キング・ディラン](https://github.com/King-Dylan)に誤って表示される問題を修正しました
    -   tikv-ctlの`raft region`コマンドの出力にリージョンステータス情報[＃17037](https://github.com/tikv/tikv/issues/17037) @ [栄光](https://github.com/glorv)が含まれていない問題を修正しました
    -   `raftstore.periodic-full-compact-start-times`構成項目をオンラインで変更すると、TiKVがpanic可能性がある問題を修正しました[＃17066](https://github.com/tikv/tikv/issues/17066) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   破損したRaftデータ スナップショット[＃15292](https://github.com/tikv/tikv/issues/15292) @ [LykxSassinator](https://github.com/LykxSassinator)を適用すると TiKV が繰り返しpanic可能性がある問題を修正しました。
    -   キャッシュエントリが永続化される前に解放すると TiKV がpanic[＃17040](https://github.com/tikv/tikv/issues/17040) @ [栄光](https://github.com/glorv)を起こす問題を修正しました

-   PD

    -   テーブル属性[＃55188](https://github.com/pingcap/tidb/issues/55188) @ [Jmポテト](https://github.com/JmPotato)を取得するときに誤った PD API が呼び出される問題を修正しました
    -   `INFORMATION_SCHEMA.RUNAWAY_WATCHES`テーブルの時間データ型が正しくない問題を修正[＃54770](https://github.com/pingcap/tidb/issues/54770) @ [HuSharp](https://github.com/HuSharp)
    -   一部のログが編集されない問題を修正[＃8419](https://github.com/tikv/pd/issues/8419) @ [rleungx](https://github.com/rleungx)
    -   `Filter`監視メトリック[＃8098](https://github.com/tikv/pd/issues/8098) @ [ノルーシュ](https://github.com/nolouch)でデータが欠落している問題を修正しました
    -   TLS が有効になっているときに HTTP クライアントがpanic可能性がある問題を修正[＃8237](https://github.com/tikv/pd/issues/8237) @ [okJiang](https://github.com/okJiang)
    -   暗号化マネージャーが使用前に初期化されない問題を修正[＃8384](https://github.com/tikv/pd/issues/8384) @ [rleungx](https://github.com/rleungx)
    -   同時実行性が高い場合にリソース グループがリソース使用量を効果的に制限できない問題を修正[＃8435](https://github.com/tikv/pd/issues/8435) @ [ノルーシュ](https://github.com/nolouch)
    -   `store limit` [＃8253](https://github.com/tikv/pd/issues/8253) @ [lhy1024](https://github.com/lhy1024)に関連するデータ競合問題を修正
    -   `scheduling`マイクロサービスが[＃8331](https://github.com/tikv/pd/issues/8331) @ [rleungx](https://github.com/rleungx)で有効化された後にスケーリングの進行状況が正しく表示されない問題を修正
    -   `tso`マイクロサービスが有効になった後、TSO ノードが動的に更新されない問題を修正[＃8154](https://github.com/tikv/pd/issues/8154) @ [rleungx](https://github.com/rleungx)
    -   リソースグループ[＃8267](https://github.com/tikv/pd/issues/8267) @ [HuSharp](https://github.com/HuSharp)のデータ競合問題を修正
    -   500 ミリ秒を超えるトークンをリクエストするとリソース グループがクォータ制限に達する問題を修正[＃8349](https://github.com/tikv/pd/issues/8349) @ [ノルーシュ](https://github.com/nolouch)
    -   PDリーダーを手動で転送すると[＃8225](https://github.com/tikv/pd/issues/8225) @ [HuSharp](https://github.com/HuSharp)失敗する可能性がある問題を修正しました
    -   削除されたノードがetcdクライアント[＃8286](https://github.com/tikv/pd/issues/8286) @ [Jmポテト](https://github.com/JmPotato)の候補接続リストにまだ表示される問題を修正
    -   `ALTER PLACEMENT POLICY`配置ポリシー[＃52257](https://github.com/pingcap/tidb/issues/52257) [＃51712](https://github.com/pingcap/tidb/issues/51712) @ [ジフハウス](https://github.com/jiyfhust)を変更できない問題を修正
    -   書き込みホットスポットのスケジュール設定により配置ポリシーの制約が破られる可能性がある問題を修正[＃7848](https://github.com/tikv/pd/issues/7848) @ [lhy1024](https://github.com/lhy1024)
    -   配置ルール[＃7808](https://github.com/tikv/pd/issues/7808) @ [rleungx](https://github.com/rleungx)を使用しているときに、ダウンしたピアが回復しない可能性がある問題を修正しました。
    -   リソースグループクエリ[＃8217](https://github.com/tikv/pd/issues/8217) @ [ノルーシュ](https://github.com/nolouch)をキャンセルするときに再試行回数が多すぎる問題を修正
    -   PD がオペレータ チェック[＃8263](https://github.com/tikv/pd/issues/8263) @ [lhy1024](https://github.com/lhy1024)中に遭遇するデータ競合問題を修正しました
    -   ロールをリソースグループ[＃54417](https://github.com/pingcap/tidb/issues/54417) @ [Jmポテト](https://github.com/JmPotato)にバインドするときにエラーが報告されない問題を修正しました
    -   TiKV構成項目[`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size) 1 MiB未満の値に設定するとPDpanic[＃8323](https://github.com/tikv/pd/issues/8323) @ [Jmポテト](https://github.com/JmPotato)が発生する問題を修正しました

-   TiFlash

    -   TiFlashとPD間のネットワークパーティション（ネットワーク切断）により、読み取り要求タイムアウトエラー[＃9243](https://github.com/pingcap/tiflash/issues/9243) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)が発生する可能性がある問題を修正しました。
    -   `SUBSTRING_INDEX()`関数が一部のコーナーケースでTiFlash のクラッシュを引き起こす可能性がある問題を修正[＃9116](https://github.com/pingcap/tiflash/issues/9116) @ [wshwsh12](https://github.com/wshwsh12)
    -   BRまたはTiDB Lightning [＃9118](https://github.com/pingcap/tiflash/issues/9118) @ [ジンヘリン](https://github.com/JinheLin)経由でデータをインポートした後、FastScanモードで多数の重複行が読み取られる可能性がある問題を修正しました。
    -   データベースの作成直後に削除されるとTiFlash がpanic可能性がある問題を修正[＃9266](https://github.com/pingcap/tiflash/issues/9266) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   TiFlashで SSL 証明書の構成を空の文字列に設定すると、誤って TLS が有効になり、 TiFlashが起動しなくなる問題を修正しました[＃9235](https://github.com/pingcap/tiflash/issues/9235) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   分散storageおよびコンピューティングアーキテクチャで、DDL操作[＃9084](https://github.com/pingcap/tiflash/issues/9084) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で非NULL列を追加した後にクエリでNULL値が誤って返される可能性がある問題を修正しました。
    -   データベース[＃9132](https://github.com/pingcap/tiflash/issues/9132) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)にまたがる空のパーティションを持つパーティションテーブルで`RENAME TABLE ... TO ...`実行した後にTiFlash がpanic可能性がある問題を修正しました。
    -   空のパーティション[＃9024](https://github.com/pingcap/tiflash/issues/9024) @ [ジンヘリン](https://github.com/JinheLin)を含むパーティション テーブルでクエリを実行するときに発生するクエリ タイムアウトの問題を修正しました。
    -   遅延マテリアライゼーションが有効になった後に、一部のクエリで列タイプの不一致エラーが報告される可能性がある問題を修正[＃9175](https://github.com/pingcap/tiflash/issues/9175) @ [ジンヘリン](https://github.com/JinheLin)
    -   遅延マテリアライゼーションが有効になった後、仮想生成列を含むクエリが誤った結果を返す可能性がある問題を修正[＃9188](https://github.com/pingcap/tiflash/issues/9188) @ [ジンヘリン](https://github.com/JinheLin)

-   ツール

    -   バックアップと復元 (BR)

        -   リージョンリーダー[＃17168](https://github.com/tikv/tikv/issues/17168) @ [リーヴルス](https://github.com/Leavrth)の探索の中断により、チェックポイントバックアップ中のバックアップパフォーマンスが影響を受ける問題を修正しました。
        -   増分バックアップ[＃54139](https://github.com/pingcap/tidb/issues/54139) @ [3ポイントシュート](https://github.com/3pointer)中の DDL ジョブのスキャンの非効率性の問題を修正
        -   復元プロセス中に複数のネストされた再試行によりBR がエラーを正しく識別できない問題を修正[＃54053](https://github.com/pingcap/tidb/issues/54053) @ [リドリスR](https://github.com/RidRisR)
        -   空の`EndKey` [＃52574](https://github.com/pingcap/tidb/issues/52574) @ [3ポイントシュート](https://github.com/3pointer)が原因でBR がトランザクション KV クラスターの復元に失敗する問題を修正しました
        -   アドバンサー所有者の移行[＃53561](https://github.com/pingcap/tidb/issues/53561) @ [リドリスR](https://github.com/RidRisR)後にログバックアップが一時停止される可能性がある問題を修正しました
        -   `ADD INDEX`や`MODIFY COLUMN`などのバックフィルを必要とする DDL が、増分リストア[＃54426](https://github.com/pingcap/tidb/issues/54426) @ [3ポイントシュート](https://github.com/3pointer)中に正しく回復されない可能性がある問題を修正しました。
        -   PD接続障害により、ログバックアップアドバンサ所有者が配置されているTiDBインスタンスがpanic[＃52597](https://github.com/pingcap/tidb/issues/52597) @ [ユジュンセン](https://github.com/YuJuncen)になる可能性がある問題を修正しました。

    -   TiCDC

        -   リージョンの変更によりダウンストリームpanicが発生する問題を修正[＃17233](https://github.com/tikv/tikv/issues/17233) @ [ヒック](https://github.com/hicqu)
        -   アップストリーム[＃11371](https://github.com/pingcap/tiflow/issues/11371) @ [リデジュ](https://github.com/lidezhu)で新しい照合順序が無効になっている場合、TiCDC がクラスター化インデックス テーブルの主キーを正しくデコードできない問題を修正しました。
        -   `UPDATE`イベントを[＃11402](https://github.com/pingcap/tiflow/issues/11402) @ [3エースショーハンド](https://github.com/3AceShowHand)に分割した後、チェックサムが正しく`0`に設定されない問題を修正しました。
        -   マルチノード環境で大量の`UPDATE`操作を実行する際にChangefeedを繰り返し再起動するとデータの不整合が発生する可能性がある問題を修正[＃11219](https://github.com/pingcap/tiflow/issues/11219) @ [リデジュ](https://github.com/lidezhu)
        -   下流の Kafka にアクセスできない場合にプロセッサモジュールがスタックする可能性がある問題を修正[＃11340](https://github.com/pingcap/tiflow/issues/11340) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   MariaDBデータの移行中に`SET`ステートメントがDMpanicを引き起こす問題を修正[＃10206](https://github.com/pingcap/tiflow/issues/10206) @ [ドヴェーデン](https://github.com/dveeden)
        -   `go-mysql` [＃11041](https://github.com/pingcap/tiflow/issues/11041) @ [D3ハンター](https://github.com/D3Hunter)にアップグレードして接続ブロックの問題を修正しました
        -   インデックスの長さがデフォルト値の`max-index-length` [＃11459](https://github.com/pingcap/tiflow/issues/11459) @ [マイケル・ムデン](https://github.com/michaelmdeng)を超えるとデータレプリケーションが中断される問題を修正しました
        -   スキーマ トラッカーが LIST パーティション テーブルを誤って処理し、DM エラー[＃11408](https://github.com/pingcap/tiflow/issues/11408) @ [ランス6716](https://github.com/lance6716)が発生する問題を修正しました。

    -   TiDB Lightning

        -   TiDB Lightningがキースペース名[＃54232](https://github.com/pingcap/tidb/issues/54232) @ [ケニーtm](https://github.com/kennytm)の取得に失敗したときに混乱を招く`WARN`ログを出力する問題を修正

    -   Dumpling

        -   テーブルとビューを同時にエクスポートするとDumpling がエラーを報告する問題を修正[＃53682](https://github.com/pingcap/tidb/issues/53682) @ [接線](https://github.com/tangenta)

    -   TiDBBinlog

        -   TiDB Binlogが有効な場合、 `ADD COLUMN`実行中に行を削除するとエラー`data and columnID count not match`が報告される可能性がある問題を修正しました[＃53133](https://github.com/pingcap/tidb/issues/53133) @ [接線](https://github.com/tangenta)
