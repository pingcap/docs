---
title: TiDB 7.1.1 Release Notes
summary: TiDB 7.1.1 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.1 リリースノート {#tidb-7-1-1-release-notes}

発売日：2023年7月24日

TiDB バージョン: 7.1.1

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiDBは、変更されていないキーをロックするかどうかを制御するための新しいシステム変数`tidb_lock_unchanged_keys`を導入しました@ [ekexium](https://github.com/ekexium) [＃44714](https://github.com/pingcap/tidb/issues/44714)

### 動作の変更 {#behavior-changes}

-   更新イベントの処理中に、イベント内の主キーまたはnull以外の一意インデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割します。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-a-single-update-change)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   プランキャッシュは200以上のパラメータを持つクエリをサポートします[＃44823](https://github.com/pingcap/tidb/issues/44823) @ [qw4990](https://github.com/qw4990)
    -   ディスクからダンプされたチャンクを読み込む際のパフォーマンスを最適化します@ [YangKeao](https://github.com/YangKeao) [＃45125](https://github.com/pingcap/tidb/issues/45125)
    -   インデックススキャン範囲を構築するロジックを最適化し、複雑な条件をインデックススキャン範囲 に変換できるようにしました。 [＃44389](https://github.com/pingcap/tidb/issues/44389) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes) [＃41572](https://github.com/pingcap/tidb/issues/41572)
    -   古い読み取りの再試行リーダーがロックに遭遇すると、TiDBはロックを解決した後、リーダーで強制的に再試行し、不要なオーバーヘッドを回避します[＃43659](https://github.com/pingcap/tidb/issues/43659) @ [you06](https://github.com/you06)

-   PD

    -   Swaggerサーバーが無効になっている場合、PD はデフォルトで Swagger API をブロックします[＃6786](https://github.com/tikv/pd/issues/6786) @ [bufferflies](https://github.com/bufferflies)

-   ツール

    -   TiCDC

        -   TiCDC がオブジェクトストレージサービスにデータを複製する際のバイナリ フィールドのエンコード形式を最適化します。 [＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   Kafka へのレプリケーションのシナリオでOAUTHBEARER認証をサポート [＃8865](https://github.com/pingcap/tiflow/issues/8865) @ [Rustin170506](https://github.com/Rustin170506)

    -   TiDB Lightning

        -   チェックサムフェーズ中の`ClientTSOStreamClosed`エラーに対するTiDB Lightningの再試行ロジックを改善しました。 [＃45301](https://github.com/pingcap/tidb/issues/45301) @ [lance6716](https://github.com/lance6716)
        -   インポート後にSQLでチェックサムを検証し、検証の安定性を向上 [＃41941](https://github.com/pingcap/tidb/issues/41941) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   Dumpling

        -   Dumplingは、 `--sql`パラメータが使用されているときにテーブルクエリの実行を回避し、エクスポートのオーバーヘッドを削減します[＃45239](https://github.com/pingcap/tidb/issues/45239) @ [lance6716](https://github.com/lance6716)

    -   TiDB Binlog

        -   テーブル情報の取得方法を最適化し、 Drainer の初期化時間とメモリ使用量を削減します。 [＃1137](https://github.com/pingcap/tidb-binlog/issues/1137) @ [lichunzhu](https://github.com/lichunzhu)

## バグ修正 {#bug-fixes}

-   TiDB

    -   GC ロック解決ステップで一部の悲観的ロックが見逃される可能性がある問題を修正しました [＃45134](https://github.com/pingcap/tidb/issues/45134) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   新しいセッションが作成された場合に統計コレクターがデッドロックを引き起こす可能性がある問題を修正[＃44502](https://github.com/pingcap/tidb/issues/44502) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   メモリトラッカーの潜在的なメモリリーク問題を修正 [＃44612](https://github.com/pingcap/tidb/issues/44612) @ [wshwsh12](https://github.com/wshwsh12)
    -   バッチコプロセッサの再試行によって誤ったリージョン情報が生成される可能性があり、クエリが失敗する問題を修正しました[＃44622](https://github.com/pingcap/tidb/issues/44622) @ [windtalker](https://github.com/windtalker)
    -   インデックススキャンにおける潜在的なデータ競合問題を修正 [＃45126](https://github.com/pingcap/tidb/issues/45126) @ [wshwsh12](https://github.com/wshwsh12)
    -   `tidb_enable_parallel_apply`有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正[＃45299](https://github.com/pingcap/tidb/issues/45299) @ [windtalker](https://github.com/windtalker)
    -   `indexMerge`のクエリが強制終了されたときに発生するハングアップの問題を修正しました [＃45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   統計情報におけるSQL実行詳細のメモリ消費量が多すぎると、極端なケースでTiDB OOMが発生する問題を修正[＃44047](https://github.com/pingcap/tidb/issues/44047) @ [wshwsh12](https://github.com/wshwsh12)
    -   `FormatSQL()`メソッドが入力の非常に長い SQL 文を適切に切り捨てることができない問題を修正しました。 [＃44542](https://github.com/pingcap/tidb/issues/44542) @ [hawkingrei](https://github.com/hawkingrei)
    -   クラスタのアップグレード中に DDL 操作が停止し、アップグレードが失敗する問題を修正しました[＃44158](https://github.com/pingcap/tidb/issues/44158) @ [zimulala](https://github.com/zimulala)
    -   1つのTiDBノードで障害が発生した後、他のTiDBノードがTTLタスクを引き継がない問題を修正しました [＃45022](https://github.com/pingcap/tidb/issues/45022) @ [lcwangchao](https://github.com/lcwangchao)
    -   MySQLカーソルフェッチプロトコル使用時に、結果セットのメモリ消費量が`tidb_mem_quota_query`上限を超え、TiDBのメモリオーバーフローが発生する問題を修正しました。修正後、TiDBは結果セットを自動的にディスクに書き込み、メモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [YangKeao](https://github.com/YangKeao)
    -   権限がなくてもユーザーが`INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの情報を表示できる問題を修正 [＃45320](https://github.com/pingcap/tidb/issues/45320) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `ADMIN SHOW DDL JOBS`ステートメントによって返される`ROW_COUNT`不正確である問題を修正[＃44044](https://github.com/pingcap/tidb/issues/44044) @ [tangenta](https://github.com/tangenta)
    -   範囲列パーティションテーブルをクエリするとエラーが発生する可能性がある問題を修正しました [＃43459](https://github.com/pingcap/tidb/issues/43459) @ [mjonss](https://github.com/mjonss)
    -   一時停止中の DDL タスクの再開が失敗する問題を修正[＃44217](https://github.com/pingcap/tidb/issues/44217) @ [dhysum](https://github.com/dhysum)
    -   メモリ内の悲観的ロックが`FLASHBACK`障害と[＃44292](https://github.com/pingcap/tidb/issues/44292) [Jmポテト](https://github.com/JmPotato)の不整合を引き起こす問題を修正しました。
    -   削除されたテーブルが`INFORMATION_SCHEMA` から引き続き読み取ることができる問題を修正しました [＃43714](https://github.com/pingcap/tidb/issues/43714) @ [tangenta](https://github.com/tangenta)
    -   アップグレード前に一時停止された DDL 操作がある場合にクラスターのアップグレードが失敗する問題を修正[＃44225](https://github.com/pingcap/tidb/issues/44225) @ [zimulala](https://github.com/zimulala)
    -   BR を使用して`AUTO_ID_CACHE=1`テーブルを復元するときに発生する`duplicate entry`エラーを修正します [＃44716](https://github.com/pingcap/tidb/issues/44716) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   DDL 所有者の複数回の切り替えによって引き起こされるデータ インデックスの不整合の問題を修正しました。 [＃44619](https://github.com/pingcap/tidb/issues/44619) @ [tangenta](https://github.com/tangenta)
    -   `none`ステータスの`ADD INDEX` DDL タスクをキャンセルすると、このタスクが Distributed eXecution Framework (DXF) タスク キューから削除されないため、メモリリークが発生する可能性がある問題を修正しました。 [＃44205](https://github.com/pingcap/tidb/issues/44205) @ [tangenta](https://github.com/tangenta)
    -   特定のエラーデータを処理するときにプロキシプロトコルが`Header read timeout`エラーを報告する問題を修正しました [＃43205](https://github.com/pingcap/tidb/issues/43205) @ [blacktear23](https://github.com/blacktear23)
    -   PD分離により実行中のDDL がブロックされる可能性がある問題を修正しました [＃44267](https://github.com/pingcap/tidb/issues/44267) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   文中の`n`負の数の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました [＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)
    -   多数の空のパーティションテーブルを作成した後に過剰なメモリ使用が発生する問題を修正しました [＃44308](https://github.com/pingcap/tidb/issues/44308) @ [hawkingrei](https://github.com/hawkingrei)
    -   結合したテーブルの再配置により外部結合結果が不正確になる可能性がある問題を修正[＃44314](https://github.com/pingcap/tidb/issues/44314) @ [AilinKid](https://github.com/AilinKid)
    -   共通テーブル式 (CTE) を含むクエリによってディスク容量が不足する可能性がある問題を修正[＃44477](https://github.com/pingcap/tidb/issues/44477) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   データベースを削除するとGCの進行が遅くなる問題を修正[＃33069](https://github.com/pingcap/tidb/issues/33069) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   取り込みモードでインデックスの追加が失敗する問題を修正 [＃44137](https://github.com/pingcap/tidb/issues/44137) @ [tangenta](https://github.com/tangenta)
    -   テーブルパーティション定義で`FLOOR()`関数を使用してパーティション列をに丸めた場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正しました。 [＃42323](https://github.com/pingcap/tidb/issues/42323) @ [jiyfhust](https://github.com/jiyfhust)
    -   フォロワー読み取りが再試行前にフラッシュバックエラーを処理せず、クエリエラーが発生する問題を修正しました [＃43673](https://github.com/pingcap/tidb/issues/43673) @ [you06](https://github.com/you06)
    -   カーソルフェッチで`memTracker`使用するとメモリリークが発生する問題を修正[＃44254](https://github.com/pingcap/tidb/issues/44254) @ [YangKeao](https://github.com/YangKeao)
    -   `SHOW PROCESSLIST`文でサブクエリ時間が長い文のトランザクションの TxnStart を表示できない問題を修正[＃40851](https://github.com/pingcap/tidb/issues/40851) @ [crazycs520](https://github.com/crazycs520)
    -   `LEADING`ヒントがブロックエイリアスのクエリをサポートしない問題を修正しました [＃44645](https://github.com/pingcap/tidb/issues/44645) @ [qw4990](https://github.com/qw4990)
    -   `PREPARE stmt FROM "ANALYZE TABLE xxx"` `tidb_mem_quota_query` で殺される可能性がある問題を修正 [＃44320](https://github.com/pingcap/tidb/issues/44320) @ [chrysan](https://github.com/chrysan)
    -   空の`processInfo` によって引き起こされるpanic問題を修正 [＃43829](https://github.com/pingcap/tidb/issues/43829) @ [zimulala](https://github.com/zimulala)
    -   `ON UPDATE`文が主キーを正しく更新しない場合にデータとインデックスが不整合になる問題を修正しました [＃44565](https://github.com/pingcap/tidb/issues/44565) @ [zyguan](https://github.com/zyguan)
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [AilinKid](https://github.com/AilinKid)
    -   CTEと相関サブクエリを同時に使用すると、クエリ結果が不正確になったり、panicが発生する可能性がある問題を修正[＃44649](https://github.com/pingcap/tidb/issues/44649) [＃38170](https://github.com/pingcap/tidb/issues/38170) [＃44774](https://github.com/pingcap/tidb/issues/44774) @ [winoros](https://github.com/winoros) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   ロールバック状態でDDLタスクをキャンセルすると、関連するメタデータにエラーが発生する問題を修正しました [＃44143](https://github.com/pingcap/tidb/issues/44143) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   `UPDATE`文を実行すると外部キー制約のチェックによりエラーが発生する問題を修正しました [＃44848](https://github.com/pingcap/tidb/issues/44848) @ [crazycs520](https://github.com/crazycs520)

-   PD

    -   リソース マネージャーが既定のリソース グループを繰り返し初期化する問題を修正しました。 [＃6787](https://github.com/tikv/pd/issues/6787) @ [glorv](https://github.com/glorv)
    -   SQLの配置ルールで設定された`location-labels` 、期待どおりにスケジュールされない場合がある問題を修正しました。 [＃6662](https://github.com/tikv/pd/issues/6662) @ [rleungx](https://github.com/rleungx)
    -   一部のコーナーケースで冗長レプリカが自動的に修復されない問題を修正[＃6573](https://github.com/tikv/pd/issues/6573) @ [nolouch](https://github.com/nolouch)

-   TiFlash

    -   分散ストレージおよびコンピューティングアーキテクチャモードで、 TiFlashコンピューティングノードが不正確なCPUコア情報を取得する問題を修正しました。 [＃7436](https://github.com/pingcap/tiflash/issues/7436) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   オンラインアンセーフリカバリを使用した後、 TiFlashの再起動に時間がかかりすぎる問題を修正しました [＃7671](https://github.com/pingcap/tiflash/issues/7671) @ [hongyunyan](https://github.com/hongyunyan)

-   ツール

    -   Backup & Restore (BR)

        -   `checksum mismatch`が場合によっては誤って報告される問題を修正[＃44472](https://github.com/pingcap/tidb/issues/44472) @ [Leavrth](https://github.com/Leavrth)
        -   TiDBクラスタにPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正 [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [joccau](https://github.com/joccau)

    -   TiCDC

        -   PD例外によりレプリケーションタスクが停止する可能性がある問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃9054](https://github.com/pingcap/tiflow/issues/9054) @ [asddongmen](https://github.com/asddongmen) @ [fubinzh](https://github.com/fubinzh)
        -   オブジェクトストレージサービスへのレプリケーション時に過剰なメモリ消費が発生する問題を修正 [＃8894](https://github.com/pingcap/tiflow/issues/8894) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   再実行ログが有効で、下流に例外がある場合にレプリケーションタスクが停止する可能性がある問題を修正しました。 [＃9172](https://github.com/pingcap/tiflow/issues/9172) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   下流で障害が発生した場合に TiCDC が再試行を続け、再試行時間が長くなりすぎる問題を修正しました[＃9272](https://github.com/pingcap/tiflow/issues/9272) @ [asddongmen](https://github.com/asddongmen)
        -   Kafka にデータを複製する際に下流のメタデータを頻繁に読み取ることによって下流に過度の負荷がかかる問題を修正しました [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [Rustin170506](https://github.com/Rustin170506)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードが発生する問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [Rustin170506](https://github.com/Rustin170506)
        -   一部の特殊なシナリオでソートコンポーネントの過剰なメモリ使用によって引き起こされる OOM 問題を修正[＃8974](https://github.com/pingcap/tiflow/issues/8974) @ [hicqu](https://github.com/hicqu)
        -   AvroまたはCSVプロトコルが使用されている場合、 `UPDATE`操作で古い値を出力できない問題を修正しました[＃9086](https://github.com/pingcap/tiflow/issues/9086) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   ストレージサービスにデータを複製するときに、下流のDDLステートメントに対応するJSONファイルにテーブルフィールドのデフォルト値が記録されない問題を修正しました。 [＃9066](https://github.com/pingcap/tiflow/issues/9066) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   TiDB または MySQL にデータを複製するときに、下流の双方向レプリケーション関連の変数を頻繁に設定することによって発生する下流ログが多すぎる問題を修正しました。 [＃9180](https://github.com/pingcap/tiflow/issues/9180) @ [asddongmen](https://github.com/asddongmen)
        -   Kafka メッセージのサイズが大きすぎるためにレプリケーションエラーが発生した場合に、メッセージ本文がログに記録される問題を修正しました。 [＃9031](https://github.com/pingcap/tiflow/issues/9031) @ [darraes](https://github.com/darraes)
        -   ネットワーク分離やPDオーナーノードの再起動などのPD障害時にTiCDCが停止する問題を修正[＃8808](https://github.com/pingcap/tiflow/issues/8808) [＃8812](https://github.com/pingcap/tiflow/issues/8812) [＃8877](https://github.com/pingcap/tiflow/issues/8877) @ [asddongmen](https://github.com/asddongmen)
        -   Avroプロトコルが`Enum`タイプの値を誤って識別する問題を修正しました [＃9259](https://github.com/pingcap/tiflow/issues/9259) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Data Migration (DM)

        -   移行対象のテーブル内の一意インデックスに空の列が含まれている場合にDMマスターが異常終了する問題を修正[＃9247](https://github.com/pingcap/tiflow/issues/9247) @ [lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB LightningとPD間の接続失敗を再試行できない問題を修正し、インポート成功率を向上 [＃43400](https://github.com/pingcap/tidb/issues/43400) @ [lichunzhu](https://github.com/lichunzhu)
        -   TiKV にデータを書き込むときに、スペース不足エラーが返されるときに、 TiDB Lightning がエラー メッセージを正しく表示しない問題を修正しました。 [＃44733](https://github.com/pingcap/tidb/issues/44733) @ [lance6716](https://github.com/lance6716)
        -   チェックサム操作中に`Region is unavailable`エラーが報告される問題を修正 [＃45462](https://github.com/pingcap/tidb/issues/45462) @ [D3Hunter](https://github.com/D3Hunter)
        -   `experimental.allow-expression-index`が有効でデフォルト値が UUID の場合に発生するTiDB Lightning panic問題を修正しました [＃44497](https://github.com/pingcap/tidb/issues/44497) @ [lichunzhu](https://github.com/lichunzhu)
        -   競合条件によりディスククォータが不正確になる可能性がある問題を修正 [＃44867](https://github.com/pingcap/tidb/issues/44867) @ [D3Hunter](https://github.com/D3Hunter)
        -   論理インポートモードで、インポート中に下流のテーブルを削除すると、 TiDB Lightningメタデータが時間で更新されない可能性がある問題を修正しました。 [＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)

    -   Dumpling

        -   クエリ結果セット`--sql`が空の場合にDumpling が異常終了する問題を修正[＃45200](https://github.com/pingcap/tidb/issues/45200) @ [D3Hunter](https://github.com/D3Hunter)

    -   TiDB Binlog

        -   PDアドレスの完全な変更後、TiDBが`SHOW PUMP STATUS`または`SHOW DRAINER STATUS`経由でBinlogノードステータスを正しく照会できない問題を修正しました。 [＃42643](https://github.com/pingcap/tidb/issues/42643) @ [lichunzhu](https://github.com/lichunzhu)
        -   PD アドレスの完全な変更後に TiDB がバイナリログを書き込めなくなる問題を修正しました [＃42643](https://github.com/pingcap/tidb/issues/42643) @ [lance6716](https://github.com/lance6716)
        -   etcdクライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[＃1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [lichunzhu](https://github.com/lichunzhu)
