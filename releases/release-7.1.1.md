---
title: TiDB 7.1.1 Release Notes
summary: TiDB 7.1.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.1 リリースノート {#tidb-7-1-1-release-notes}

発売日：2023年7月24日

TiDB バージョン: 7.1.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDBは、変更されていないキー[＃44714](https://github.com/pingcap/tidb/issues/44714)をロックするかどうかを制御するための新しいシステム変数`tidb_lock_unchanged_keys`を導入しました[エキシウム](https://github.com/ekexium)

### 行動の変化 {#behavior-changes}

-   更新イベントの処理中に、イベント内の主キーまたはnull以外の一意のインデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   プランキャッシュは200以上のパラメータを持つクエリをサポートします[＃44823](https://github.com/pingcap/tidb/issues/44823) @ [qw4990](https://github.com/qw4990)
    -   ディスク[＃45125](https://github.com/pingcap/tidb/issues/45125)からダンプされたチャンクを読み込む際のパフォーマンスを最適化します[ヤンケオ](https://github.com/YangKeao)
    -   インデックススキャン範囲を構築するロジックを最適化し、複雑な条件をインデックススキャン範囲[＃41572](https://github.com/pingcap/tidb/issues/41572) [＃44389](https://github.com/pingcap/tidb/issues/44389) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)に変換できるようにしました。
    -   古い読み取りの再試行リーダーがロックに遭遇すると、TiDBはロックを解決した後、リーダーで強制的に再試行し、不要なオーバーヘッドを回避します[＃43659](https://github.com/pingcap/tidb/issues/43659) @ [あなた06](https://github.com/you06)

-   PD

    -   Swaggerサーバーが無効になっている場合、PD はデフォルトで Swagger API をブロックします[＃6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)

-   ツール

    -   TiCDC

        -   TiCDC がオブジェクトstorageサービス[＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)にデータを複製する際のバイナリ フィールドのエンコード形式を最適化します。
        -   Kafka [＃8865](https://github.com/pingcap/tiflow/issues/8865) @ [ハイラスティン](https://github.com/Rustin170506)へのレプリケーションのシナリオでOAUTHBEARER認証をサポート

    -   TiDB Lightning

        -   チェックサムフェーズ[＃45301](https://github.com/pingcap/tidb/issues/45301) @ [ランス6716](https://github.com/lance6716)中の`ClientTSOStreamClosed`エラーに対するTiDB Lightningの再試行ロジックを改善しました。
        -   インポート後にSQLでチェックサムを検証し、検証[＃41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)の安定性を向上

    -   Dumpling

        -   Dumplingは、 `--sql`パラメータが使用されているときにテーブルクエリの実行を回避し、エクスポートのオーバーヘッドを削減します[＃45239](https://github.com/pingcap/tidb/issues/45239) @ [ランス6716](https://github.com/lance6716)

    -   TiDBBinlog

        -   テーブル情報の取得方法を最適化し、 Drainer [＃1137](https://github.com/pingcap/tidb-binlog/issues/1137) @ [リチュンジュ](https://github.com/lichunzhu)の初期化時間とメモリ使用量を削減します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   GC ロック解決ステップで一部の悲観的ロック[＃45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)が見逃される可能性がある問題を修正しました
    -   新しいセッションが作成された場合に統計コレクターがデッドロックを引き起こす可能性がある問題を修正[＃44502](https://github.com/pingcap/tidb/issues/44502) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   メモリトラッカー[＃44612](https://github.com/pingcap/tidb/issues/44612) @ [wshwsh12](https://github.com/wshwsh12)の潜在的なメモリリーク問題を修正
    -   バッチコプロセッサの再試行によって誤ったリージョン情報が生成される可能性があり、クエリが失敗する問題を修正しました[＃44622](https://github.com/pingcap/tidb/issues/44622) @ [ウィンドトーカー](https://github.com/windtalker)
    -   インデックススキャン[＃45126](https://github.com/pingcap/tidb/issues/45126) @ [wshwsh12](https://github.com/wshwsh12)における潜在的なデータ競合問題を修正
    -   `tidb_enable_parallel_apply`有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正[＃45299](https://github.com/pingcap/tidb/issues/45299) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `indexMerge`のクエリが[＃45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正しました
    -   統計情報におけるSQL実行詳細のメモリ消費量が多すぎると、極端なケースでTiDB OOMが発生する問題を修正[＃44047](https://github.com/pingcap/tidb/issues/44047) @ [wshwsh12](https://github.com/wshwsh12)
    -   `FormatSQL()`メソッドが入力[＃44542](https://github.com/pingcap/tidb/issues/44542) @ [ホーキングレイ](https://github.com/hawkingrei)の非常に長い SQL 文を適切に切り捨てることができない問題を修正しました。
    -   クラスタのアップグレード中に DDL 操作が停止し、アップグレードが失敗する問題を修正しました[＃44158](https://github.com/pingcap/tidb/issues/44158) @ [ジムララ](https://github.com/zimulala)
    -   1つのTiDBノード[＃45022](https://github.com/pingcap/tidb/issues/45022) @ [lcwangchao](https://github.com/lcwangchao)で障害が発生した後、他のTiDBノードがTTLタスクを引き継がない問題を修正しました
    -   MySQLカーソルフェッチプロトコル使用時に、結果セットのメモリ消費量が`tidb_mem_quota_query`上限を超え、TiDBのメモリオーバーフローが発生する問題を修正しました。修正後、TiDBは結果セットを自動的にディスクに書き込み、メモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)
    -   権限[＃45320](https://github.com/pingcap/tidb/issues/45320) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)がなくてもユーザーが`INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの情報を表示できる問題を修正
    -   `ADMIN SHOW DDL JOBS`ステートメントによって返される`ROW_COUNT`不正確である問題を修正[＃44044](https://github.com/pingcap/tidb/issues/44044) @ [接線](https://github.com/tangenta)
    -   範囲列パーティションテーブルをクエリするとエラー[＃43459](https://github.com/pingcap/tidb/issues/43459) @ [ミョンス](https://github.com/mjonss)が発生する可能性がある問題を修正しました
    -   一時停止中の DDL タスクの再開が失敗する問題を修正[＃44217](https://github.com/pingcap/tidb/issues/44217) @ [ディサム](https://github.com/dhysum)
    -   メモリ内の悲観的ロックが`FLASHBACK`障害と[＃44292](https://github.com/pingcap/tidb/issues/44292) [Jmポテト](https://github.com/JmPotato)の不整合を引き起こす問題を修正しました。
    -   削除されたテーブルが`INFORMATION_SCHEMA` [＃43714](https://github.com/pingcap/tidb/issues/43714) @ [接線](https://github.com/tangenta)から引き続き読み取ることができる問題を修正しました
    -   アップグレード前に一時停止された DDL 操作がある場合にクラスターのアップグレードが失敗する問題を修正[＃44225](https://github.com/pingcap/tidb/issues/44225) @ [ジムララ](https://github.com/zimulala)
    -   BR [＃44716](https://github.com/pingcap/tidb/issues/44716) @ [天菜まお](https://github.com/tiancaiamao)を使用して`AUTO_ID_CACHE=1`テーブルを復元するときに発生する`duplicate entry`エラーを修正します
    -   DDL 所有者[＃44619](https://github.com/pingcap/tidb/issues/44619) @ [接線](https://github.com/tangenta)の複数回の切り替えによって引き起こされるデータ インデックスの不整合の問題を修正しました。
    -   `none`ステータスの`ADD INDEX` DDL タスクをキャンセルすると、このタスクが Distributed eXecution Framework (DXF) タスク キュー[＃44205](https://github.com/pingcap/tidb/issues/44205) @ [接線](https://github.com/tangenta)から削除されないため、メモリリークが発生する可能性がある問題を修正しました。
    -   特定のエラーデータ[＃43205](https://github.com/pingcap/tidb/issues/43205) @ [ブラックティア23](https://github.com/blacktear23)を処理するときにプロキシプロトコルが`Header read timeout`エラーを報告する問題を修正しました
    -   PD分離により実行中のDDL [＃44267](https://github.com/pingcap/tidb/issues/44267) @ [wjhuang2016](https://github.com/wjhuang2016)がブロックされる可能性がある問題を修正しました
    -   文中の`n`負の数[＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました
    -   多数の空のパーティションテーブル[＃44308](https://github.com/pingcap/tidb/issues/44308) @ [ホーキングレイ](https://github.com/hawkingrei)を作成した後に過剰なメモリ使用が発生する問題を修正しました
    -   結合したテーブルの再配置により外部結合結果が不正確になる可能性がある問題を修正[＃44314](https://github.com/pingcap/tidb/issues/44314) @ [アイリンキッド](https://github.com/AilinKid)
    -   共通テーブル式 (CTE) を含むクエリによってディスク容量が不足する可能性がある問題を修正[＃44477](https://github.com/pingcap/tidb/issues/44477) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   データベースを削除するとGCの進行が遅くなる問題を修正[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [天菜まお](https://github.com/tiancaiamao)
    -   取り込みモード[＃44137](https://github.com/pingcap/tidb/issues/44137) @ [接線](https://github.com/tangenta)でインデックスの追加が失敗する問題を修正
    -   テーブルパーティション定義で`FLOOR()`関数を使用してパーティション列を[＃42323](https://github.com/pingcap/tidb/issues/42323) @ [ジフハウス](https://github.com/jiyfhust)に丸めた場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正しました。
    -   フォロワー読み取りが再試行前にフラッシュバックエラーを処理せず、クエリエラー[＃43673](https://github.com/pingcap/tidb/issues/43673) @ [あなた06](https://github.com/you06)が発生する問題を修正しました
    -   カーソルフェッチで`memTracker`使用するとメモリリークが発生する問題を修正[＃44254](https://github.com/pingcap/tidb/issues/44254) @ [ヤンケオ](https://github.com/YangKeao)
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   `LEADING`ヒントがブロックエイリアス[＃44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)のクエリをサポートしない問題を修正しました
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"` `tidb_mem_quota_query` [＃44320](https://github.com/pingcap/tidb/issues/44320) @ [クリサン](https://github.com/chrysan)で殺される可能性がある問題を修正
    -   空の`processInfo` [＃43829](https://github.com/pingcap/tidb/issues/43829) @ [ジムララ](https://github.com/zimulala)によって引き起こされるpanic問題を修正
    -   `ON UPDATE`文が主キー[＃44565](https://github.com/pingcap/tidb/issues/44565) @ [ジグアン](https://github.com/zyguan)を正しく更新しない場合にデータとインデックスが不整合になる問題を修正しました
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   CTEと相関サブクエリを同時に使用すると、クエリ結果が不正確になったり、panicが発生する可能性がある問題を修正[＃44649](https://github.com/pingcap/tidb/issues/44649) [＃38170](https://github.com/pingcap/tidb/issues/38170) [＃44774](https://github.com/pingcap/tidb/issues/44774) @ [ウィノロス](https://github.com/winoros) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   ロールバック状態でDDLタスクをキャンセルすると、関連するメタデータ[＃44143](https://github.com/pingcap/tidb/issues/44143) @ [wjhuang2016](https://github.com/wjhuang2016)にエラーが発生する問題を修正しました
    -   `UPDATE`文を実行すると外部キー制約[＃44848](https://github.com/pingcap/tidb/issues/44848) @ [crazycs520](https://github.com/crazycs520)のチェックによりエラーが発生する問題を修正しました

-   PD

    -   リソース マネージャーが既定のリソース グループ[＃6787](https://github.com/tikv/pd/issues/6787) @ [栄光](https://github.com/glorv)を繰り返し初期化する問題を修正しました。
    -   SQLの配置ルールで設定された`location-labels` 、期待どおりに[＃6662](https://github.com/tikv/pd/issues/6662) @ [rleungx](https://github.com/rleungx)にスケジュールされない場合がある問題を修正しました。
    -   一部のコーナーケースで冗長レプリカが自動的に修復されない問題を修正[＃6573](https://github.com/tikv/pd/issues/6573) @ [ノルーシュ](https://github.com/nolouch)

-   TiFlash

    -   分散storageおよびコンピューティングアーキテクチャモードで、 TiFlashコンピューティングノードが不正確なCPUコア情報[＃7436](https://github.com/pingcap/tiflash/issues/7436) @ [グオシャオゲ](https://github.com/guo-shaoge)を取得する問題を修正しました。
    -   オンラインアンセーフリカバリ[＃7671](https://github.com/pingcap/tiflash/issues/7671) @ [ホンユニャン](https://github.com/hongyunyan)を使用した後、 TiFlashの再起動に時間がかかりすぎる問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   `checksum mismatch`場合によっては誤って報告される問題を修正[＃44472](https://github.com/pingcap/tidb/issues/44472) @ [リーヴルス](https://github.com/Leavrth)
        -   TiDBクラスタ[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)にPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正

    -   TiCDC

        -   PD例外によりレプリケーションタスクが停止する可能性がある問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃9054](https://github.com/pingcap/tiflow/issues/9054) @ [アズドンメン](https://github.com/asddongmen) @ [フビンズ](https://github.com/fubinzh)
        -   オブジェクトstorageサービス[＃8894](https://github.com/pingcap/tiflow/issues/8894) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)へのレプリケーション時に過剰なメモリ消費が発生する問題を修正
        -   再実行ログが有効で、下流に例外[＃9172](https://github.com/pingcap/tiflow/issues/9172) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)がある場合にレプリケーションタスクが停止する可能性がある問題を修正しました。
        -   下流で障害が発生した場合に TiCDC が再試行を続け、再試行時間が長くなりすぎる問題を修正しました[＃9272](https://github.com/pingcap/tiflow/issues/9272) @ [アズドンメン](https://github.com/asddongmen)
        -   Kafka [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)にデータを複製する際に下流のメタデータを頻繁に読み取ることによって下流に過度の負荷がかかる問題を修正しました
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードが発生する問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)
        -   一部の特殊なシナリオでソートコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正[＃8974](https://github.com/pingcap/tiflow/issues/8974) @ [ヒック](https://github.com/hicqu)
        -   AvroまたはCSVプロトコルが使用されている場合、 `UPDATE`操作で古い値を出力できない問題を修正しました[＃9086](https://github.com/pingcap/tiflow/issues/9086) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   storageサービスにデータを複製するときに、下流のDDLステートメントに対応するJSONファイルにテーブルフィールド[＃9066](https://github.com/pingcap/tiflow/issues/9066) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)のデフォルト値が記録されない問題を修正しました。
        -   TiDB または MySQL [＃9180](https://github.com/pingcap/tiflow/issues/9180) @ [アズドンメン](https://github.com/asddongmen)にデータを複製するときに、下流の双方向レプリケーション関連の変数を頻繁に設定することによって発生する下流ログが多すぎる問題を修正しました。
        -   Kafka メッセージのサイズが大きすぎるためにレプリケーションエラーが発生した場合に、メッセージ本文がログ[＃9031](https://github.com/pingcap/tiflow/issues/9031) @ [ダラエス](https://github.com/darraes)に記録される問題を修正しました。
        -   ネットワーク分離やPDオーナーノードの再起動などのPD障害時にTiCDCが停止する問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [アズドンメン](https://github.com/asddongmen)
        -   Avroプロトコルが`Enum`タイプの値[＃9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)を誤って識別する問題を修正しました

    -   TiDB データ移行 (DM)

        -   移行対象のテーブル内のユニークインデックスに空の列が含まれている場合にDMマスターが異常終了する問題を修正[＃9247](https://github.com/pingcap/tiflow/issues/9247) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB LightningとPD間の接続失敗を再試行できない問題を修正し、インポート成功率[＃43400](https://github.com/pingcap/tidb/issues/43400) @ [リチュンジュ](https://github.com/lichunzhu)を向上
        -   TiKV にデータを書き込むときに、スペース不足エラー[＃44733](https://github.com/pingcap/tidb/issues/44733) @ [ランス6716](https://github.com/lance6716)が返されるときに、 TiDB Lightning がエラー メッセージを正しく表示しない問題を修正しました。
        -   チェックサム操作[＃45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)中に`Region is unavailable`エラーが報告される問題を修正
        -   `experimental.allow-expression-index`が有効でデフォルト値が UUID [＃44497](https://github.com/pingcap/tidb/issues/44497) @ [リチュンジュ](https://github.com/lichunzhu)の場合に発生するTiDB Lightningpanic問題を修正しました
        -   競合条件[＃44867](https://github.com/pingcap/tidb/issues/44867) @ [D3ハンター](https://github.com/D3Hunter)によりディスククォータが不正確になる可能性がある問題を修正
        -   論理インポートモードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータが時間[＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)で更新されない可能性がある問題を修正しました。

    -   Dumpling

        -   クエリ結果セット`--sql`が空の場合にDumpling が異常終了する問題を修正[＃45200](https://github.com/pingcap/tidb/issues/45200) @ [D3ハンター](https://github.com/D3Hunter)

    -   TiDBBinlog

        -   PDアドレス[＃42643](https://github.com/pingcap/tidb/issues/42643) @ [リチュンジュ](https://github.com/lichunzhu)の完全な変更後、TiDBが`SHOW PUMP STATUS`または`SHOW DRAINER STATUS`経由でBinlogノードステータスを正しく照会できない問題を修正しました。
        -   PD アドレス[＃42643](https://github.com/pingcap/tidb/issues/42643) @ [ランス6716](https://github.com/lance6716)の完全な変更後に TiDB がバイナリログを書き込めなくなる問題を修正しました
        -   etcdクライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[＃1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [リチュンジュ](https://github.com/lichunzhu)
