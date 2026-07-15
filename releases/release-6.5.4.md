---
title: TiDB 6.5.4 Release Notes
summary: TiDB 6.5.4 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.4 リリースノート {#tidb-6-5-4-release-notes}

発売日：2023年8月28日

TiDB バージョン: 6.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   `Cursor Fetch`使用して大きな結果セットを取得するときにTiDBがメモリを大量に消費する問題を修正するために、TiDBは結果セットを自動的にディスクに書き込んでメモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [YangKeao](https://github.com/YangKeao)
-   RocksDBの定期的な圧縮をデフォルトで無効にすることで、TiKV RocksDBのデフォルトの動作がv6.5.0より前のバージョンと一致するようになりました。この変更により、アップグレード後に大量の圧縮が行われることによるパフォーマンスへの影響を回避できます。さらに、TiKVでは2つの新しい設定項目[`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#periodic-compaction-seconds-new-in-v654)と[`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#ttl-new-in-v654)導入され、RocksDB の定期的な圧縮を手動で設定できるようになりました。 [＃15355](https://github.com/tikv/tikv/issues/15355) @ [LykxSassinator](https://github.com/LykxSassinator)

### 動作の変更 {#behavior-changes}

-   複数の変更を含むトランザクションにおいて、更新イベントで主キーまたはNULL以外の一意インデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割し、すべてのイベントが挿入イベントに先行する削除イベントの順序に従うようにします。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-multiple-update-changes)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   代入式を含む`LOAD DATA`ステートメントのパフォーマンスを最適化します [＃46081](https://github.com/pingcap/tidb/issues/46081) @ [gengliqi](https://github.com/gengliqi)
    -   ディスクからダンプされたチャンクを読み込む際のパフォーマンスを最適化します@ [YangKeao](https://github.com/YangKeao) [＃45125](https://github.com/pingcap/tidb/issues/45125)
    -   PDスケジュールを一時停止するための構成項目を`halt-scheduling`追加します。 [＃6493](https://github.com/tikv/pd/issues/6493) @ [JmPotato](https://github.com/JmPotato)

-   TiKV

    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィックを削減します [＃14553](https://github.com/tikv/tikv/issues/14553) @ [you06](https://github.com/you06)
    -   `Max gap of safe-ts`と`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、resolved-tsと安全な ts の状態をより適切に観察および診断します[＃15082](https://github.com/tikv/tikv/issues/15082) @ [ekexium](https://github.com/ekexium)
    -   TiKV で RocksDB の設定を公開し、ユーザーが TTL や定期的な圧縮などの機能を無効にできるようにします[＃14873](https://github.com/tikv/tikv/issues/14873) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   Titan マニフェストファイルを書き込むときにミューテックスを保持しないようにして、他のスレッドに影響を与えないようにします[＃15351](https://github.com/tikv/tikv/issues/15351) @ [Connor1996](https://github.com/Connor1996)
    -   圧縮メカニズムを最適化します。リージョンが分割されるときに、分割するキーがない場合、圧縮がトリガーされ、過剰な MVCC バージョンが排除されます。 [＃15282](https://github.com/tikv/tikv/issues/15282) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)

-   PD

    -   Swaggerサーバーが有効になっていない場合に、デフォルトで Swagger API をブロックする機能をサポート[＃6786](https://github.com/tikv/pd/issues/6786) @ [bufferflies](https://github.com/bufferflies)
    -   etcd の高可用性を向上させる [＃6442](https://github.com/tikv/pd/issues/6442) @ [lhy1024](https://github.com/lhy1024) [＃6554](https://github.com/tikv/pd/issues/6554)
    -   `GetRegions`リクエストのメモリ消費を削減 [＃6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)
    -   HTTP 接続再利用をサポート [＃6913](https://github.com/tikv/pd/issues/6913) @ [nolouch](https://github.com/nolouch)

-   TiFlash

    -   IOバッチ最適化によるTiFlash書き込みパフォーマンスの向上 [＃7735](https://github.com/pingcap/tiflash/issues/7735) @ [lidezhu](https://github.com/lidezhu)
    -   不要なfsync操作を削除することでTiFlashの書き込みパフォーマンスを向上[＃7736](https://github.com/pingcap/tiflash/issues/7736) @ [lidezhu](https://github.com/lidezhu)
    -   TiFlashコプロセッサタスクキューの最大長を制限して、コプロセッサタスクの過剰なキューイングを回避します。これは TiFlash のサービス可用性に影響を及ぼします[＃7747](https://github.com/pingcap/tiflash/issues/7747) @ [LittleFall](https://github.com/LittleFall)

-   ツール

    -   Backup & Restore (BR)

        -   HTTPクライアントで`MaxIdleConns`と`MaxIdleConnsPerHost`パラメータを設定することで接続の再利用のサポートを強化します [＃46011](https://github.com/pingcap/tidb/issues/46011) @ [Leavrth](https://github.com/Leavrth)
        -   PD または外部 S3ストレージへの接続に失敗した場合のBRのフォールトトレランスを向上[＃42909](https://github.com/pingcap/tidb/issues/42909) @ [Leavrth](https://github.com/Leavrth)
        -   新しい復元パラメータ`WaitTiflashReady`を追加します。このパラメータを有効にすると、 TiFlashレプリカが正常に複製された後に復元操作が完了します[＃43828](https://github.com/pingcap/tidb/issues/43828) [＃46302](https://github.com/pingcap/tidb/issues/46302) @ [3pointer](https://github.com/3pointer)

    -   TiCDC

        -   TiCDC が失敗後に再試行するときのステータス メッセージを改善する[＃9483](https://github.com/pingcap/tiflow/issues/9483) @ [asddongmen](https://github.com/asddongmen)
        -   TiCDC が Kafka に同期する際に制限を超えるメッセージを処理する方法を最適化し、主キーのみをダウンストリームに送信することをサポートしました。 [＃9574](https://github.com/pingcap/tiflow/issues/9574) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   ストレージシンクは、HEX形式のデータの16進エンコードをサポートするようになり、AWS DMS形式仕様と互換性があります。 [＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Data Migration (DM)

        -   互換性のない DDL ステートメントに対して厳密な楽観的モードをサポートする [＃9112](https://github.com/pingcap/tiflow/issues/9112) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   Dumpling

        -   `-sql`パラメータを使用してデータをエクスポートするときに、すべてのデータベースとテーブルのクエリをスキップすることで、エクスポートのオーバーヘッドを削減します。 [＃45239](https://github.com/pingcap/tidb/issues/45239) @ [lance6716](https://github.com/lance6716)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `STREAM_AGG()`演算子をプッシュダウンすると`index out of range`エラーが報告される可能性がある問題を修正しました [＃40857](https://github.com/pingcap/tidb/issues/40857) @ [Dousir9](https://github.com/Dousir9)
    -   `CREATE TABLE`文にサブパーティション定義 が含まれている場合、TiDB がすべてのパーティション情報を無視して非パーティションテーブルを作成する問題を修正しました。 [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [mjonss](https://github.com/mjonss) [＃41198](https://github.com/pingcap/tidb/issues/41198)
    -   `stale_read_ts`設定が間違っていると`PREPARE stmt`データを誤って読み取る可能性がある問題を修正[＃43044](https://github.com/pingcap/tidb/issues/43044) @ [you06](https://github.com/you06)
    -   ActivateTxn で起こりうるデータ競合の問題を修正しました [＃42092](https://github.com/pingcap/tidb/issues/42092) @ [hawkingrei](https://github.com/hawkingrei)
    -   バッチクライアントがタイムリーに再接続しない問題を修正[＃44431](https://github.com/pingcap/tidb/issues/44431) @ [crazycs520](https://github.com/crazycs520)
    -   SQLコンパイルエラーログが編集されない問題を修正[＃41831](https://github.com/pingcap/tidb/issues/41831) @ [lance6716](https://github.com/lance6716)
    -   CTEと相関サブクエリを同時に使用すると、クエリ結果が不正確になったり、panicが発生する可能性がある問題を修正[＃44649](https://github.com/pingcap/tidb/issues/44649) [＃38170](https://github.com/pingcap/tidb/issues/38170) [＃44774](https://github.com/pingcap/tidb/issues/44774) @ [winoros](https://github.com/winoros) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   TTLタスクが時間で統計更新をトリガーできない問題を修正 [＃40109](https://github.com/pingcap/tidb/issues/40109) @ [YangKeao](https://github.com/YangKeao)
    -   GC ロック解決ステップで一部の悲観的ロックが見逃される可能性がある問題を修正しました [＃45134](https://github.com/pingcap/tidb/issues/45134) @ [MyonKeminta](https://github.com/MyonKeminta)
    -   バイナリプロトコルを使用してTiDBに接続し、多数の`PREPARE`と`EXECUTE`ステートメントを実行すると、メモリリークと実行時間が増加し続ける問題を修正しました。 [＃44612](https://github.com/pingcap/tidb/issues/44612) @ [wshwsh12](https://github.com/wshwsh12)
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列のデータ長が列定義を超える可能性がある問題を修正しました [＃42440](https://github.com/pingcap/tidb/issues/42440) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   多数のリージョンがあるが、 `Prepare`または`Execute` を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできないという PD OOM 問題を修正しました。 [＃39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)
    -   パーティションテーブルに新しいインデックスを追加した後、パーティションパーティションテーブルで統計の自動収集が正しくトリガーされない可能性がある問題を修正しました。 [＃41638](https://github.com/pingcap/tidb/issues/41638) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   統計情報におけるSQL実行詳細のメモリ消費量が多すぎると、極端なケースでTiDB OOMが発生する問題を修正[＃44047](https://github.com/pingcap/tidb/issues/44047) @ [wshwsh12](https://github.com/wshwsh12)
    -   バッチコプロセッサの再試行によって誤ったリージョン情報が生成される可能性があり、クエリが失敗する問題を修正しました[＃44622](https://github.com/pingcap/tidb/issues/44622) @ [windtalker](https://github.com/windtalker)
    -   `indexMerge`のクエリが強制終了されたときに発生するハングアップの問題を修正しました [＃45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正しました[＃45531](https://github.com/pingcap/tidb/issues/45531) @ [Defined2014](https://github.com/Defined2014)
    -   `tidb_enable_parallel_apply`有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正[＃45299](https://github.com/pingcap/tidb/issues/45299) @ [windtalker](https://github.com/windtalker)
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [AilinKid](https://github.com/AilinKid)
    -   仮想列によって発生する適切な物理プランが見つからない問題を修正しました [＃41014](https://github.com/pingcap/tidb/issues/41014) @ [AilinKid](https://github.com/AilinKid)
    -   空の`processInfo` によって引き起こされるpanic問題を修正 [＃43829](https://github.com/pingcap/tidb/issues/43829) @ [zimulala](https://github.com/zimulala)
    -   文中の`n`負の数の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました [＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)
    -   MySQLカーソルフェッチプロトコル使用時に、結果セットのメモリ消費量が`tidb_mem_quota_query`上限を超え、TiDBのメモリオーバーフローが発生する問題を修正しました。修正後、TiDBは結果セットを自動的にディスクに書き込み、メモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [YangKeao](https://github.com/YangKeao)
    -   BR を使用して`AUTO_ID_CACHE=1`テーブルを復元するときに発生する`duplicate entry`エラーを修正します [＃44716](https://github.com/pingcap/tidb/issues/44716) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   テーブルパーティション定義で`FLOOR()`関数を使用してパーティション列をに丸めた場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正しました。 [＃42323](https://github.com/pingcap/tidb/issues/42323) @ [jiyfhust](https://github.com/jiyfhust)
    -   同時ビューによって DDL 操作がブロックされる可能性がある問題を修正[＃40352](https://github.com/pingcap/tidb/issues/40352) @ [zeminzhou](https://github.com/zeminzhou)
    -   `datetime`値がと正しくないために統計収集タスクが失敗する問題を修正しました [＃39336](https://github.com/pingcap/tidb/issues/39336) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   クラスターのPDノードが交換された後、一部のDDL文が一定期間スタックする可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   PD時間に突然の変化があったときに`resolve lock`ハングする可能性がある問題を修正しました [＃44822](https://github.com/pingcap/tidb/issues/44822) @ [zyguan](https://github.com/zyguan)
    -   インデックススキャンにおける潜在的なデータ競合問題を修正 [＃45126](https://github.com/pingcap/tidb/issues/45126) @ [wshwsh12](https://github.com/wshwsh12)
    -   `FormatSQL()`メソッドが入力の非常に長い SQL 文を適切に切り捨てることができない問題を修正しました。 [＃44542](https://github.com/pingcap/tidb/issues/44542) @ [hawkingrei](https://github.com/hawkingrei)
    -   権限がなくてもユーザーが`INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの情報を表示できる問題を修正 [＃45320](https://github.com/pingcap/tidb/issues/45320) @ [Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   `DATETIME`または`TIMESTAMP`列を数値定数と比較するときに、MySQL と動作が一致しない問題を修正しました。 [＃38361](https://github.com/pingcap/tidb/issues/38361) @ [yibin87](https://github.com/yibin87)
    -   インデックス結合のエラーによりクエリが停止する可能性がある問題を修正[＃45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   接続を切断すると go コルーチン リークが発生する可能性がある問題を修正[＃46034](https://github.com/pingcap/tidb/issues/46034) @ [pingyu](https://github.com/pingyu)
    -   `tmp-storage-quota`設定が で有効にならない問題を修正 [＃26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12) [＃45161](https://github.com/pingcap/tidb/issues/45161)
    -   クラスターでTiFlashノードがダウンした場合にTiFlashレプリカが利用できなくなる問題を修正しました。 [＃38484](https://github.com/pingcap/tidb/issues/38484) @ [hehechen](https://github.com/hehechen)
    -   `Config.Labels`同時に読み書きする場合に、データ競合により TiDB がクラッシュする問題を修正[＃45561](https://github.com/pingcap/tidb/issues/45561) @ [gengliqi](https://github.com/gengliqi)
    -   クラスタが大きい場合、クライアントが定期的に更新される`min-resolved-ts` PD OOMを引き起こす可能性がある問題を修正しました[＃46664](https://github.com/pingcap/tidb/issues/46664) @ [HuSharp](https://github.com/HuSharp)

-   TiKV

    -   `ttl-check-poll-interval`設定項目がRawKV API V2 で有効にならない問題を修正 [＃15142](https://github.com/tikv/tikv/issues/15142) @ [pingyu](https://github.com/pingyu)
    -   オンラインアンセーフリカバリがタイムアウトで中止されない問題を修正 [＃15346](https://github.com/tikv/tikv/issues/15346) @ [Connor1996](https://github.com/Connor1996)
    -   `FLASHBACK` を実行した後にリージョンマージがブロックされる可能性がある問題を修正しました [＃15258](https://github.com/tikv/tikv/issues/15258) @ [overvenus](https://github.com/overvenus)
    -   1つのTiKVノードが分離され、別のノードが再起動されたときに発生する可能性のあるデータの不整合の問題を修正しました[＃15035](https://github.com/tikv/tikv/issues/15035) @ [overvenus](https://github.com/overvenus)
    -   データレプリケーション自動同期モードで同期回復フェーズでQPSがゼロに低下する問題を修正しました。 [＃14975](https://github.com/tikv/tikv/issues/14975) @ [nolouch](https://github.com/nolouch)
    -   暗号化により部分書き込み中にデータ破損が発生する可能性がある問題を修正 [＃15080](https://github.com/tikv/tikv/issues/15080) @ [tabokie](https://github.com/tabokie)
    -   ストアハートビートの再試行回数をに減らして、ハートビートストームの問題を修正しました。 [＃15184](https://github.com/tikv/tikv/issues/15184) @ [nolouch](https://github.com/nolouch)
    -   保留中の圧縮バイト量が多い場合にトラフィック制御が機能しない可能性がある問題を修正しました。 [＃14392](https://github.com/tikv/tikv/issues/14392) @ [Connor1996](https://github.com/Connor1996)
    -   PDとTiKV間のネットワーク中断によりPITRが停止する可能性がある問題を修正しました [＃15279](https://github.com/tikv/tikv/issues/15279) @ [YuJuncen](https://github.com/YuJuncen)
    -   TiCDC の古い値機能が有効になっているときに TiKV がより多くのメモリを消費する可能性がある問題を修正[＃14815](https://github.com/tikv/tikv/issues/14815) @ [YuJuncen](https://github.com/YuJuncen)

-   PD

    -   etcd がすでに起動しているがクライアントがまだ接続していない場合、クライアントを呼び出すと PD がpanicになる可能性がある問題を修正しました。 [＃6860](https://github.com/tikv/pd/issues/6860) @ [HuSharp](https://github.com/HuSharp)
    -   リーダーが長時間退出できない問題を修正[＃6918](https://github.com/tikv/pd/issues/6918) @ [bufferflies](https://github.com/bufferflies)
    -   配置ルールが`LOCATION_LABELS`使用する場合、SQL とルールチェッカーがと互換性がない問題を修正しました [＃38605](https://github.com/pingcap/tidb/issues/38605) @ [nolouch](https://github.com/nolouch)
    -   PD が予期せず複数のラーナーをリージョンに追加する可能性がある問題を修正しました。 [＃5786](https://github.com/tikv/pd/issues/5786) @ [HunDunDM](https://github.com/HunDunDM)
    -   ルールチェッカーがピアを選択した場合に、不健全なピアを削除できない問題を修正しました [＃6559](https://github.com/tikv/pd/issues/6559) @ [nolouch](https://github.com/nolouch)
    -   `unsafe recovery`で不合格になったラーナーのピアが`auto-detect`モードで無視される問題を修正 [＃6690](https://github.com/tikv/pd/issues/6690) @ [v01dstar](https://github.com/v01dstar)

-   TiFlash

    -   `fsp` `DATETIME` 、 `TIMESTAMP` 、または`TIME`データ型に変更した後にクエリが失敗する問題を修正しました [＃7809](https://github.com/pingcap/tiflash/issues/7809) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   領域の無効な範囲キーによりTiFlashデータが不整合になる問題を修正しました [＃7762](https://github.com/pingcap/tiflash/issues/7762) @ [lidezhu](https://github.com/lidezhu)
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに重大な影響を与える可能性がある問題を修正しました[＃7810](https://github.com/pingcap/tiflash/issues/7810) @ [SeaRise](https://github.com/SeaRise)
    -   オンラインアンセーフリカバリを使用した後、 TiFlashの再起動に時間がかかりすぎる問題を修正しました [＃7671](https://github.com/pingcap/tiflash/issues/7671) @ [hongyunyan](https://github.com/hongyunyan)
    -   TiFlash が割り算を行うときに`DECIMAL`結果を誤って丸める問題を修正しました [＃6462](https://github.com/pingcap/tiflash/issues/6462) @ [LittleFall](https://github.com/LittleFall)

-   ツール

    -   Backup & Restore (BR)

        -   BRで使用されるグローバルパラメータ`TableColumnCountLimit`と`IndexLimit`デフォルト値を最大値に増やすことで、復元が失敗する問題を修正しました。 [＃45793](https://github.com/pingcap/tidb/issues/45793) @ [Leavrth](https://github.com/Leavrth)
        -   PITR で DDL メタ情報を処理するときに書き換えが失敗する問題を修正しました [＃43184](https://github.com/pingcap/tidb/issues/43184) @ [Leavrth](https://github.com/Leavrth)
        -   PITR実行中に関数の戻り値をチェックしないことで発生するpanicの問題を修正[＃45853](https://github.com/pingcap/tidb/issues/45853) @ [Leavrth](https://github.com/Leavrth)
        -   Amazon S3 以外の S3 互換storage使用時に無効なリージョン ID が取得される問題を修正 [＃42033](https://github.com/pingcap/tidb/issues/42033) @ [3pointer](https://github.com/3pointer) [＃41916](https://github.com/pingcap/tidb/issues/41916)
        -   RawKVモードのきめ細かなバックアップフェーズで発生する可能性のあるエラーを修正 [＃37085](https://github.com/pingcap/tidb/issues/37085) @ [pingyu](https://github.com/pingyu)
        -   TiDBクラスタにPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正 [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [joccau](https://github.com/joccau)
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を軽減します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームでエラーが発生し、 で再試行すると、レプリケーションタスクが停止する可能性がある問題を修正しました。 [＃9450](https://github.com/pingcap/tiflow/issues/9450) @ [hicqu](https://github.com/hicqu)
        -   Kafka に同期するときに再試行間隔が短いためにレプリケーションタスクが失敗する問題を修正しました [＃9504](https://github.com/pingcap/tiflow/issues/9504) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   TiCDC がアップストリームの 1 つのトランザクションで複数の一意のキー行を変更するときに同期書き込み競合を引き起こす可能性がある問題を修正しました。 [＃9430](https://github.com/pingcap/tiflow/issues/9430) @ [sdojjy](https://github.com/sdojjy)
        -   TiCDC が誤って名前変更 DDL 操作を同期する可能性がある問題を修正[＃9488](https://github.com/pingcap/tiflow/issues/9488) [＃9378](https://github.com/pingcap/tiflow/issues/9378) [＃9531](https://github.com/pingcap/tiflow/issues/9531) @ [asddongmen](https://github.com/asddongmen)
        -   下流で短期的な障害が発生したときにレプリケーションタスクが停止する可能性がある問題を修正[＃9542](https://github.com/pingcap/tiflow/issues/9542) [＃9272](https://github.com/pingcap/tiflow/issues/9272) [＃9582](https://github.com/pingcap/tiflow/issues/9582) [＃9592](https://github.com/pingcap/tiflow/issues/9592) @ [hicqu](https://github.com/hicqu)
        -   TiCDC ノードのステータスがに変化したときに発生する可能性のあるpanic問題を修正しました。 [＃9354](https://github.com/pingcap/tiflow/issues/9354) @ [sdojjy](https://github.com/sdojjy)
        -   Kafka Sink がエラーに遭遇すると、changefeed の進行が無期限にブロックされる可能性がある問題を修正しました。 [＃9309](https://github.com/pingcap/tiflow/issues/9309) @ [hicqu](https://github.com/hicqu)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードが発生する問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [Rustin170506](https://github.com/Rustin170506)
        -   一部の TiCDC ノードがネットワークから分離されているときに発生する可能性のあるデータの不整合の問題を修正[＃9344](https://github.com/pingcap/tiflow/issues/9344) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   再実行ログが有効で、下流に例外がある場合にレプリケーションタスクが停止する可能性がある問題を修正しました。 [＃9172](https://github.com/pingcap/tiflow/issues/9172) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   PD が一時的に利用できないために変更フィードが失敗する問題を修正しました [＃9294](https://github.com/pingcap/tiflow/issues/9294) @ [asddongmen](https://github.com/asddongmen)
        -   TiDB または MySQL にデータを複製するときに、下流の双方向レプリケーション関連の変数を頻繁に設定することによって発生する下流ログが多すぎる問題を修正しました。 [＃9180](https://github.com/pingcap/tiflow/issues/9180) @ [asddongmen](https://github.com/asddongmen)
        -   Avroプロトコルが`Enum`タイプの値を誤って識別する問題を修正しました [＃9259](https://github.com/pingcap/tiflow/issues/9259) @ [3AceShowHand](https://github.com/3AceShowHand)

    -   TiDB Data Migration (DM)

        -   一意のキー列名が null の場合に発生するpanic問題を修正[＃9247](https://github.com/pingcap/tiflow/issues/9247) @ [lance6716](https://github.com/lance6716)
        -   バリデータがエラーを誤って処理した場合に発生する可能性のあるデッドロックの問題を修正し、再試行メカニズムを最適化します[＃9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3Hunter](https://github.com/D3Hunter)
        -   因果関係キーを計算するときに照合順序が考慮されない問題を修正しました [＃9489](https://github.com/pingcap/tiflow/issues/9489) @ [hihihuhu](https://github.com/hihihuhu)

    -   TiDB Lightning

        -   エンジンがデータをインポートしているときにディスク クォータ チェックがブロックされる可能性がある問題を修正しました [＃44867](https://github.com/pingcap/tidb/issues/44867) @ [D3Hunter](https://github.com/D3Hunter)
        -   ターゲットクラスタで SSL が有効になっているときにチェックサムがエラー`Region is unavailable`を報告する問題を修正しました [＃45462](https://github.com/pingcap/tidb/issues/45462) @ [D3Hunter](https://github.com/D3Hunter)
        -   エンコードエラーが正しく記録されない問題を修正[＃44321](https://github.com/pingcap/tidb/issues/44321) @ [lyzx2001](https://github.com/lyzx2001)
        -   CSVデータをインポートする際にルートがpanicになる可能性がある問題を修正 [＃43284](https://github.com/pingcap/tidb/issues/43284) @ [lyzx2001](https://github.com/lyzx2001)
        -   論理インポートモードでテーブル A をインポートすると、テーブル B が存在しないと誤って報告される可能性がある問題を修正しました[＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)
        -   `NEXT_GLOBAL_ROW_ID` を保存するときにデータ型が間違っている問題を修正しました [＃45427](https://github.com/pingcap/tidb/issues/45427) @ [lyzx2001](https://github.com/lyzx2001)
        -   `checksum = "optional"` のときにチェックサムがエラーを報告する問題を修正しました [＃45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)
        -   PDクラスタアドレスがに変更されるとデータのインポートが失敗する問題を修正しました [＃43436](https://github.com/pingcap/tidb/issues/43436) @ [lichunzhu](https://github.com/lichunzhu)
        -   一部のPDノードが失敗した場合にデータのインポートが失敗する問題を修正しました [＃43400](https://github.com/pingcap/tidb/issues/43400) @ [lichunzhu](https://github.com/lichunzhu)
        -   AUTO_INCREMENT列を持つテーブルが`AUTO_ID_CACHE=1`設定すると、ID アロケータのベース値が正しくなくなるという問題を修正しました [＃46100](https://github.com/pingcap/tidb/issues/46100) @ [D3Hunter](https://github.com/D3Hunter)

    -   Dumpling

        -   Amazon S3 にエクスポートするときに、未処理のファイルライターの終了エラーによりエクスポートされたファイルが失われる問題を修正しました [＃45353](https://github.com/pingcap/tidb/issues/45353) @ [lichunzhu](https://github.com/lichunzhu)

    -   TiDB Binlog

        -   etcdクライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[＃1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [lichunzhu](https://github.com/lichunzhu)
