---
title: TiDB 7.1.1 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.1.
---

# TiDB 7.1.1 リリースノート {#tidb-7-1-1-release-notes}

発売日：2023年7月24日

TiDB バージョン: 7.1.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.1.1#version-list)

## 互換性の変更 {#compatibility-changes}

-   TiDB は、変更されていないキーをロックするかどうかを制御する新しいシステム変数`tidb_lock_unchanged_keys`を導入します[#44714](https://github.com/pingcap/tidb/issues/44714) @ [エキシウム](https://github.com/ekexium)

## 改善点 {#improvements}

-   TiDB

    -   プラン キャッシュは、200 を超えるパラメーター[#44823](https://github.com/pingcap/tidb/issues/44823) @ [qw4990](https://github.com/qw4990)を含むクエリをサポートします
    -   ディスク[#45125](https://github.com/pingcap/tidb/issues/45125) @ [ヤンケオ](https://github.com/YangKeao)からダンプされたチャンクを読み取るパフォーマンスを最適化します。
    -   複雑な条件をインデックス スキャン範囲[#41572](https://github.com/pingcap/tidb/issues/41572) [#44389](https://github.com/pingcap/tidb/issues/44389) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)に変換できるように、インデックス スキャン範囲を構築するロジックを最適化します。
    -   古い読み取りの再試行リーダーがロックに遭遇すると、TiDB はロックを解決した後にリーダーで強制的に再試行します。これにより、不要なオーバーヘッドが回避されます[#43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)

-   PD

    -   Swaggerサーバーが無効になっている場合、PD はデフォルトで Swagger API をブロックします[#6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   TiCDC

        -   TiCDC がデータをオブジェクトstorageサービス[#9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートするときのバイナリ フィールドのエンコード形式を最適化します。
        -   Kafka [#8865](https://github.com/pingcap/tiflow/issues/8865) @ [こんにちはラスティン](https://github.com/hi-rustin)へのレプリケーションのシナリオで OAUTHBEARER 認証をサポートします。

    -   TiDB Lightning

        -   チェックサム フェーズ[#45301](https://github.com/pingcap/tidb/issues/45301) @ [ランス6716](https://github.com/lance6716)中の PD `ClientTSOStreamClosed`エラーに対するTiDB Lightningの再試行ロジックを改善しました。
        -   インポート後に SQL でチェックサムを検証し、検証の安定性を向上させる[#41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   Dumpling

        -   Dumpling は、 `--sql`パラメーターが使用されている場合にテーブル クエリの実行を回避し、それによってエクスポートのオーバーヘッド[#45239](https://github.com/pingcap/tidb/issues/45239) @ [ランス6716](https://github.com/lance6716)を削減します。

    -   TiDBBinlog

        -   テーブル情報の取得方法を最適化し、 Drainer [#1137](https://github.com/pingcap/tidb-binlog/issues/1137) @ [リチュンジュ](https://github.com/lichunzhu)の初期化時間とメモリ使用量を削減します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   GC Resolve Locks ステップで一部の悲観的ロック[#45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)が見逃される可能性がある問題を修正します。
    -   新しいセッションの作成時に統計コレクターがデッドロックを引き起こす可能性がある問題を修正[#44502](https://github.com/pingcap/tidb/issues/44502) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)
    -   メモリトラッカー[#44612](https://github.com/pingcap/tidb/issues/44612) @ [wshwsh12](https://github.com/wshwsh12)の潜在的なメモリリークの問題を修正
    -   バッチ コプロセッサの再試行により、クエリ失敗[#44622](https://github.com/pingcap/tidb/issues/44622) @ [ウィンドトーカー](https://github.com/windtalker)の原因となる誤ったリージョン情報が生成される可能性がある問題を修正します。
    -   インデックス スキャン[#45126](https://github.com/pingcap/tidb/issues/45126) @ [wshwsh12](https://github.com/wshwsh12)における潜在的なデータ競合の問題を修正
    -   `tidb_enable_parallel_apply`が有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正します[#45299](https://github.com/pingcap/tidb/issues/45299) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `indexMerge`のクエリが[#45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正します。
    -   統計における SQL 実行の詳細の過剰なメモリ消費により、極端な場合に TiDB OOM が発生する問題を修正します[#44047](https://github.com/pingcap/tidb/issues/44047) @ [wshwsh12](https://github.com/wshwsh12)
    -   `FormatSQL()`メソッドが入力[#44542](https://github.com/pingcap/tidb/issues/44542) @ [ホーキングレイ](https://github.com/hawkingrei)の非常に長い SQL ステートメントを適切に切り詰めることができない問題を修正します。
    -   クラスターのアップグレード中に DDL 操作がスタックし、アップグレードの失敗が発生する問題を修正します[#44158](https://github.com/pingcap/tidb/issues/44158) @ [ジムララ](https://github.com/zimulala)
    -   1 つの TiDB ノード[#45022](https://github.com/pingcap/tidb/issues/45022) @ [ルクワンチャオ](https://github.com/lcwangchao)で障害が発生した後、他の TiDB ノードが TTL タスクを引き継がない問題を修正します。
    -   MySQL カーソル フェッチ プロトコルを使用すると、結果セットのメモリ消費量が`tidb_mem_quota_query`制限を超え、TiDB OOM が発生する可能性がある問題を修正します。修正後、TiDB は自動的に結果セットをディスクに書き込み、メモリ[#43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)を解放します。
    -   ユーザーが権限なしでも`INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの情報を表示できる問題を修正[#45320](https://github.com/pingcap/tidb/issues/45320) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `ADMIN SHOW DDL JOBS`ステートメントによって返される`ROW_COUNT`が不正確な[#44044](https://github.com/pingcap/tidb/issues/44044) @ [タンジェンタ](https://github.com/tangenta)になる問題を修正します。
    -   Range COLUMNSパーティションテーブルでエラー[#43459](https://github.com/pingcap/tidb/issues/43459) @ [むじょん](https://github.com/mjonss)が発生する可能性がある問題を修正します。
    -   一時停止された DDL タスクの再開が失敗する問題を修正[#44217](https://github.com/pingcap/tidb/issues/44217) @ [ジサム](https://github.com/dhysum)
    -   メモリ内悲観的ロックにより`FLASHBACK`失敗とデータの不整合が発生する[#44292](https://github.com/pingcap/tidb/issues/44292) @ [Jmポテト](https://github.com/JmPotato)という問題を修正
    -   削除されたテーブルが引き続き`INFORMATION_SCHEMA` [#43714](https://github.com/pingcap/tidb/issues/43714) @ [タンジェンタ](https://github.com/tangenta)から読み取れる問題を修正
    -   アップグレード前に一時停止された DDL 操作があるとクラスターのアップグレードが失敗する問題を修正[#44225](https://github.com/pingcap/tidb/issues/44225) @ [ジムララ](https://github.com/zimulala)
    -   BR [#44716](https://github.com/pingcap/tidb/issues/44716) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を使用して`AUTO_ID_CACHE=1`持つテーブルを復元するときに発生する`duplicate entry`エラーを修正しました。
    -   DDL 所有者[#44619](https://github.com/pingcap/tidb/issues/44619) @ [タンジェンタ](https://github.com/tangenta)の複数の切り替えによって引き起こされるデータ インデックスの不整合の問題を修正
    -   `ADD INDEX` DDL タスクを`none`ステータスでキャンセルすると、このタスクがバックエンド タスク キュー[#44205](https://github.com/pingcap/tidb/issues/44205) @ [タンジェンタ](https://github.com/tangenta)から削除されないため、メモリリークが発生する可能性がある問題を修正します。
    -   特定の誤ったデータ[#43205](https://github.com/pingcap/tidb/issues/43205) @ [ブラックティア23](https://github.com/blacktear23)を処理するときに、プロキシ プロトコルが`Header read timeout`エラーを報告する問題を修正します。
    -   PD 分離により実行中の DDL [#44267](https://github.com/pingcap/tidb/issues/44267) @ [wjhuang2016](https://github.com/wjhuang2016)がブロックされる可能性がある問題を修正
    -   ステートメント内の`n`負の数[#44786](https://github.com/pingcap/tidb/issues/44786) @ [ゼボックス](https://github.com/xhebox)である場合、 `SELECT CAST(n AS CHAR)`ステートメントのクエリ結果が正しくない問題を修正します。
    -   多数の空のパーティションテーブル[#44308](https://github.com/pingcap/tidb/issues/44308) @ [ホーキングレイ](https://github.com/hawkingrei)を作成した後の過剰なメモリ使用量の問題を修正
    -   結合したテーブルの再配置により不正な外部結合結果[#44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)が発生する可能性がある問題を修正
    -   共通テーブル式 (CTE) を含むクエリによりディスク容量不足が発生する可能性がある問題を修正します[#44477](https://github.com/pingcap/tidb/issues/44477) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   データベースを削除すると GC の進行が遅くなる問題を修正[#33069](https://github.com/pingcap/tidb/issues/33069) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   インジェストモード[#44137](https://github.com/pingcap/tidb/issues/44137) @ [タンジェンタ](https://github.com/tangenta)でインデックスの追加が失敗する問題を修正
    -   テーブル パーティション定義で`FLOOR()`関数を使用してパーティション列[#42323](https://github.com/pingcap/tidb/issues/42323) @ [ジフフスト](https://github.com/jiyfhust)を四捨五入する場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正します。
    -   フォロワー読み取りが再試行する前にフラッシュバック エラーを処理せず、クエリ エラー[#43673](https://github.com/pingcap/tidb/issues/43673) @ [あなた06](https://github.com/you06)が発生する問題を修正します。
    -   カーソルフェッチで`memTracker`を使用するとメモリリーク[#44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)が発生する問題を修正
    -   `SHOW PROCESSLIST`ステートメントがサブクエリ時間の長いステートメント[#40851](https://github.com/pingcap/tidb/issues/40851) @ [クレイジークス520](https://github.com/crazycs520)のトランザクションの TxnStart を表示できない問題を修正
    -   `LEADING`ヒントがブロック エイリアス[#44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)のクエリをサポートしていない問題を修正します。
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"`が`tidb_mem_quota_query` [#44320](https://github.com/pingcap/tidb/issues/44320) @ [クリサン](https://github.com/chrysan)に殺される可能性がある問題を修正
    -   空の`processInfo` [#43829](https://github.com/pingcap/tidb/issues/43829) @ [ジムララ](https://github.com/zimulala)によって引き起こされるpanicの問題を修正
    -   `ON UPDATE`ステートメントが主キー[#44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合、データとインデックスが矛盾する問題を修正します。
    -   `tidb_opt_agg_push_down`が有効になっている場合にクエリが間違った結果を返す可能性がある問題を修正します[#44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   CTE と相関サブクエリを同時に使用すると、不正なクエリ結果またはpanicが発生する可能性がある問題を修正します[#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @ [ウィノロス](https://github.com/winoros) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   ロールバック状態で DDL タスクをキャンセルすると、関連するメタデータ[#44143](https://github.com/pingcap/tidb/issues/44143) @ [wjhuang2016](https://github.com/wjhuang2016)でエラーが発生する問題を修正します。
    -   `UPDATE`ステートメントを実行すると、外部キー制約[#44848](https://github.com/pingcap/tidb/issues/44848) @ [クレイジークス520](https://github.com/crazycs520)のチェックによりエラーが発生する問題を修正します。

-   PD

    -   リソース マネージャーがデフォルトのリソース グループ[#6787](https://github.com/tikv/pd/issues/6787) @ [グロルフ](https://github.com/glorv)を繰り返し初期化する問題を修正します。
    -   場合によっては、SQL の配置ルールで設定された`location-labels`期待どおりにスケジュールされない問題を修正します[#6662](https://github.com/tikv/pd/issues/6662) @ [ルルンクス](https://github.com/rleungx)
    -   一部の特殊なケースで冗長レプリカが自動的に修復できない問題を修正[#6573](https://github.com/tikv/pd/issues/6573) @ [ノールーシュ](https://github.com/nolouch)

-   TiFlash

    -   非集約storageおよびコンピューティングアーキテクチャモードで、 TiFlashコンピューティング ノードが不正確な CPU コア情報[#7436](https://github.com/pingcap/tiflash/issues/7436) @ [グオシャオゲ](https://github.com/guo-shaoge)をフェッチする問題を修正します。
    -   Online Unsafe Recovery [#7671](https://github.com/pingcap/tiflash/issues/7671) @ [ホンユニャン](https://github.com/hongyunyan)を使用した後のTiFlash の再起動に時間がかかりすぎる問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   `checksum mismatch`が[#44472](https://github.com/pingcap/tidb/issues/44472) @ [レヴルス](https://github.com/Leavrth)と誤って報告される場合がある問題を修正

    -   TiCDC

        -   PD 例外によりレプリケーション タスクが停止する可能性がある問題を修正[#8808](https://github.com/pingcap/tiflow/issues/8808) [#9054](https://github.com/pingcap/tiflow/issues/9054) @ [東門](https://github.com/asddongmen) @ [フビンジ](https://github.com/fubinzh)
        -   オブジェクトstorageサービス[#8894](https://github.com/pingcap/tiflow/issues/8894) @ [CharlesCheung96](https://github.com/CharlesCheung96)にレプリケートする際の過剰なメモリ消費の問題を修正します。
        -   REDO ログが有効で、ダウンストリーム[#9172](https://github.com/pingcap/tiflow/issues/9172) @ [CharlesCheung96](https://github.com/CharlesCheung96)で例外が発生した場合にレプリケーション タスクが停止する可能性がある問題を修正します。
        -   ダウンストリーム障害が発生したときに TiCDC が再試行を続け、再試行時間が長すぎる原因となる問題を修正します[#9272](https://github.com/pingcap/tiflow/issues/9272) @ [東門](https://github.com/asddongmen)
        -   データを Kafka [#8959](https://github.com/pingcap/tiflow/issues/8959) @ [こんにちはラスティン](https://github.com/hi-rustin)にレプリケートするときに、ダウンストリーム メタデータを頻繁に読み取ることによって引き起こされる過度のダウンストリーム プレッシャーの問題を修正します。
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームで過度のワークロードが発生する問題を修正します[#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   一部の特殊なシナリオ[#8974](https://github.com/pingcap/tiflow/issues/8974) @ [ひっくり返る](https://github.com/hicqu)におけるソーターコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正します。
        -   Avro または CSV プロトコルが使用されている場合、 `UPDATE`操作で古い値を出力できない問題を修正[#9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   データをstorageサービスにレプリケートするときに、ダウンストリーム DDL ステートメントに対応する JSON ファイルにテーブル フィールド[#9066](https://github.com/pingcap/tiflow/issues/9066) @ [CharlesCheung96](https://github.com/CharlesCheung96)のデフォルト値が記録されない問題を修正します。
        -   TiDB または MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @ [東門](https://github.com/asddongmen)にデータをレプリケートするときに、ダウンストリーム双方向レプリケーション関連の変数を頻繁に設定することによって発生するダウンストリーム ログが多すぎる問題を修正します。
        -   Kafka メッセージのサイズ超過によりレプリケーション エラーが発生した場合、メッセージ本文がログ[#9031](https://github.com/pingcap/tiflow/issues/9031) @ [ダラエス](https://github.com/darraes)に記録される問題を修正
        -   ネットワーク分離や PD オーナー ノードの再起動など、PD が失敗したときに TiCDC がスタックする問題を修正[#8808](https://github.com/pingcap/tiflow/issues/8808) [#8812](https://github.com/pingcap/tiflow/issues/8812) [#8877](https://github.com/pingcap/tiflow/issues/8877) @ [東門](https://github.com/asddongmen)
        -   Avro プロトコルが`Enum` type 値[#9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)を誤って識別する問題を修正

    -   TiDB データ移行 (DM)

        -   移行対象のテーブル内の一意のインデックスに空の列が含まれている場合に DM マスターが異常終了する問題を修正[#9247](https://github.com/pingcap/tiflow/issues/9247) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightningと PD 間の接続に失敗すると再試行できない問題を修正し、インポート成功率[#43400](https://github.com/pingcap/tidb/issues/43400) @ [リチュンジュ](https://github.com/lichunzhu)を向上させました。
        -   TiKV にデータを書き込むときにスペース不足エラー[#44733](https://github.com/pingcap/tidb/issues/44733) @ [ランス6716](https://github.com/lance6716)が返されたときに、 TiDB Lightning がエラー メッセージを正しく表示しない問題を修正します。
        -   チェックサム操作[#45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)中に`Region is unavailable`エラーが報告される問題を修正
        -   `experimental.allow-expression-index`が有効で、デフォルト値が UUID [#44497](https://github.com/pingcap/tidb/issues/44497) @ [リチュンジュ](https://github.com/lichunzhu)である場合のTiDB Lightningpanicの問題を修正
        -   競合条件[#44867](https://github.com/pingcap/tidb/issues/44867) @ [D3ハンター](https://github.com/D3Hunter)によりディスク クォータが不正確になる可能性がある問題を修正
        -   論理インポート モードで、インポート中にダウンストリームのテーブルを削除すると、 TiDB Lightningメタデータが時間内に更新されなくなる可能性がある問題を修正します[#44614](https://github.com/pingcap/tidb/issues/44614) @ [dsダシュン](https://github.com/dsdashun)

    -   Dumpling

        -   クエリ結果セット`--sql`が空[#45200](https://github.com/pingcap/tidb/issues/45200) @ [D3ハンター](https://github.com/D3Hunter)の場合、 Dumpling が異常終了する問題を修正

    -   TiDBBinlog

        -   PD アドレス[#42643](https://github.com/pingcap/tidb/issues/42643) @ [リチュンジュ](https://github.com/lichunzhu)が完全に変更された後、TiDB が`SHOW PUMP STATUS`または`SHOW DRAINER STATUS`を介してBinlogノードのステータスを正しくクエリできない問題を修正します。
        -   PD アドレス[#42643](https://github.com/pingcap/tidb/issues/42643) @ [ランス6716](https://github.com/lance6716)が完全に変更された後、TiDB がバイナリログを書き込めなくなる問題を修正
        -   etcd クライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [リチュンジュ](https://github.com/lichunzhu)
