---
title: TiDB 6.5.4 Release Notes
summary: TiDB 6.5.4 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.4 リリースノート {#tidb-6-5-4-release-notes}

発売日：2023年8月28日

TiDB バージョン: 6.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   `Cursor Fetch`使用して大きな結果セットを取得するときにTiDBがメモリを大量に消費する問題を修正するために、TiDBは結果セットを自動的にディスクに書き込んでメモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)
-   RocksDBの定期的な圧縮をデフォルトで無効にすることで、TiKV RocksDBのデフォルトの動作がv6.5.0より前のバージョンと一致するようになりました。この変更により、アップグレード後に大量の圧縮が行われることによるパフォーマンスへの影響を回避できます。さらに、TiKVでは2つの新しい設定項目[`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#periodic-compaction-seconds-new-in-v654)と[`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#ttl-new-in-v654)導入され、RocksDB [＃15355](https://github.com/tikv/tikv/issues/15355) @ [LykxSassinator](https://github.com/LykxSassinator)の定期的な圧縮を手動で設定できるようになりました。

### 行動の変化 {#behavior-changes}

-   複数の変更を含むトランザクションにおいて、更新イベントで主キーまたはNULL以外の一意のインデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割し、すべてのイベントが挿入イベントに先行する削除イベントの順序に従うようにします。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-multiple-update-changes)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   代入式[＃46081](https://github.com/pingcap/tidb/issues/46081) @ [ゲンリキ](https://github.com/gengliqi)を含む`LOAD DATA`ステートメントのパフォーマンスを最適化します
    -   ディスク[＃45125](https://github.com/pingcap/tidb/issues/45125)からダンプされたチャンクを読み込む際のパフォーマンスを最適化します[ヤンケオ](https://github.com/YangKeao)
    -   PDスケジュール[＃6493](https://github.com/tikv/pd/issues/6493) @ [Jmポテト](https://github.com/JmPotato)を一時停止するための構成項目を`halt-scheduling`追加します。

-   TiKV

    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィック[＃14553](https://github.com/tikv/tikv/issues/14553) @ [あなた06](https://github.com/you06)を削減します
    -   `Max gap of safe-ts`と`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、resolved-tsと安全な ts の状態をより適切に観察および診断します[＃15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)
    -   TiKV で RocksDB の設定を公開し、ユーザーが TTL や定期的な圧縮などの機能を無効にできるようにします[＃14873](https://github.com/tikv/tikv/issues/14873) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   Titan マニフェストファイルを書き込むときにミューテックスを保持しないようにして、他のスレッドに影響を与えないようにします[＃15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)
    -   圧縮メカニズムを最適化します。リージョンが分割されるときに、分割するキーがない場合、圧縮がトリガーされ、過剰な MVCC バージョン[＃15282](https://github.com/tikv/tikv/issues/15282) @ [スペードA-タン](https://github.com/SpadeA-Tang)が排除されます。

-   PD

    -   Swaggerサーバーが有効になっていない場合に、デフォルトで Swagger API をブロックする機能をサポート[＃6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)
    -   etcd [＃6554](https://github.com/tikv/pd/issues/6554) [＃6442](https://github.com/tikv/pd/issues/6442) @ [lhy1024](https://github.com/lhy1024)の高可用性を向上させる
    -   `GetRegions`リクエスト[＃6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)のメモリ消費を削減
    -   HTTP 接続[＃6913](https://github.com/tikv/pd/issues/6913) @ [ノルーシュ](https://github.com/nolouch)再利用をサポート

-   TiFlash

    -   IOバッチ最適化[＃7735](https://github.com/pingcap/tiflash/issues/7735) @ [リデズ](https://github.com/lidezhu)によるTiFlash書き込みパフォーマンスの向上
    -   不要なfsync操作を削除することでTiFlashの書き込みパフォーマンスを向上[＃7736](https://github.com/pingcap/tiflash/issues/7736) @ [リデズ](https://github.com/lidezhu)
    -   TiFlashコプロセッサタスクキューの最大長を制限して、コプロセッサタスクの過剰なキューイングを回避します。これは TiFlash のサービス可用性に影響を及ぼします[＃7747](https://github.com/pingcap/tiflash/issues/7747) @ [リトルフォール](https://github.com/LittleFall)

-   ツール

    -   バックアップと復元 (BR)

        -   HTTPクライアント[＃46011](https://github.com/pingcap/tidb/issues/46011) @ [リーヴルス](https://github.com/Leavrth)で`MaxIdleConns`と`MaxIdleConnsPerHost`パラメータを設定することで接続の再利用のサポートを強化します
        -   PD または外部 S3storageへの接続に失敗した場合のBRのフォールトトレランスを向上[＃42909](https://github.com/pingcap/tidb/issues/42909) @ [リーヴルス](https://github.com/Leavrth)
        -   新しい復元パラメータ`WaitTiflashReady`を追加します。このパラメータを有効にすると、 TiFlashレプリカが正常に複製された後に復元操作が完了します[＃43828](https://github.com/pingcap/tidb/issues/43828) [＃46302](https://github.com/pingcap/tidb/issues/46302) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiCDC

        -   TiCDC が失敗後に再試行するときのステータス メッセージを改善する[＃9483](https://github.com/pingcap/tiflow/issues/9483) @ [アズドンメン](https://github.com/asddongmen)
        -   TiCDC が Kafka に同期する際に制限を超えるメッセージを処理する方法を最適化し、主キーのみをダウンストリーム[＃9574](https://github.com/pingcap/tiflow/issues/9574) @ [3エースショーハンド](https://github.com/3AceShowHand)に送信することをサポートしました。
        -   ストレージシンクは、HEX形式のデータの16進エンコードをサポートするようになり、AWS DMS形式仕様[＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)と互換性があります。

    -   TiDB データ移行 (DM)

        -   互換性のない DDL ステートメント[＃9112](https://github.com/pingcap/tiflow/issues/9112) @ [GMHDBJD](https://github.com/GMHDBJD)に対して厳密な楽観的モードをサポートする

    -   Dumpling

        -   `-sql`パラメータ[＃45239](https://github.com/pingcap/tidb/issues/45239) @ [ランス6716](https://github.com/lance6716)を使用してデータをエクスポートするときに、すべてのデータベースとテーブルのクエリをスキップすることで、エクスポートのオーバーヘッドを削減します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `STREAM_AGG()`演算子[＃40857](https://github.com/pingcap/tidb/issues/40857) @ [ドゥーシル9](https://github.com/Dousir9)を押し下げると`index out of range`エラーが報告される可能性がある問題を修正しました
    -   `CREATE TABLE`文にサブパーティション定義[＃41198](https://github.com/pingcap/tidb/issues/41198) [＃41200](https://github.com/pingcap/tidb/issues/41200) @ [ミョンス](https://github.com/mjonss)が含まれている場合、TiDB がすべてのパーティション情報を無視して非パーティションテーブルを作成する問題を修正しました。
    -   `stale_read_ts`設定が間違っていると`PREPARE stmt`データを誤って読み取る可能性がある問題を修正[＃43044](https://github.com/pingcap/tidb/issues/43044) @ [あなた06](https://github.com/you06)
    -   ActivateTxn [＃42092](https://github.com/pingcap/tidb/issues/42092) @ [ホーキングレイ](https://github.com/hawkingrei)で起こりうるデータ競合の問題を修正しました
    -   バッチクライアントがタイムリーに再接続しない問題を修正[＃44431](https://github.com/pingcap/tidb/issues/44431) @ [crazycs520](https://github.com/crazycs520)
    -   SQLコンパイルエラーログが編集されない問題を修正[＃41831](https://github.com/pingcap/tidb/issues/41831) @ [ランス6716](https://github.com/lance6716)
    -   CTEと相関サブクエリを同時に使用すると、クエリ結果が不正確になったり、panicが発生する可能性がある問題を修正[＃44649](https://github.com/pingcap/tidb/issues/44649) [＃38170](https://github.com/pingcap/tidb/issues/38170) [＃44774](https://github.com/pingcap/tidb/issues/44774) @ [ウィノロス](https://github.com/winoros) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   TTLタスクが時間[＃40109](https://github.com/pingcap/tidb/issues/40109) @ [ヤンケオ](https://github.com/YangKeao)で統計更新をトリガーできない問題を修正
    -   GC ロック解決ステップで一部の悲観的ロック[＃45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)が見逃される可能性がある問題を修正しました
    -   バイナリプロトコルを使用してTiDBに接続し、多数の`PREPARE`と`EXECUTE`ステートメント[＃44612](https://github.com/pingcap/tidb/issues/44612) @ [wshwsh12](https://github.com/wshwsh12)を実行すると、メモリリークと実行時間が増加し続ける問題を修正しました。
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列目のデータ長が列定義[＃42440](https://github.com/pingcap/tidb/issues/42440) @ [天菜まお](https://github.com/tiancaiamao)を超える可能性がある問題を修正しました
    -   多数のリージョンがあるが、 `Prepare`または`Execute` [＃39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできないという PD OOM 問題を修正しました。
    -   パーティションテーブル[＃41638](https://github.com/pingcap/tidb/issues/41638) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)に新しいインデックスを追加した後、パーティションパーティションテーブルで統計の自動収集が正しくトリガーされない可能性がある問題を修正しました。
    -   統計情報におけるSQL実行詳細のメモリ消費量が多すぎると、極端なケースでTiDB OOMが発生する問題を修正[＃44047](https://github.com/pingcap/tidb/issues/44047) @ [wshwsh12](https://github.com/wshwsh12)
    -   バッチコプロセッサの再試行によって誤ったリージョン情報が生成される可能性があり、クエリが失敗する問題を修正しました[＃44622](https://github.com/pingcap/tidb/issues/44622) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `indexMerge`のクエリが[＃45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正しました
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正しました[＃45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   `tidb_enable_parallel_apply`有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正[＃45299](https://github.com/pingcap/tidb/issues/45299) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `tidb_opt_agg_push_down`有効になっている場合にクエリが誤った結果を返す可能性がある問題を修正[＃44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   仮想列[＃41014](https://github.com/pingcap/tidb/issues/41014) @ [アイリンキッド](https://github.com/AilinKid)によって発生する適切な物理プランが見つからない問題を修正しました
    -   空の`processInfo` [＃43829](https://github.com/pingcap/tidb/issues/43829) @ [ジムララ](https://github.com/zimulala)によって引き起こされるpanic問題を修正
    -   文中の`n`負の数[＃44786](https://github.com/pingcap/tidb/issues/44786) @ [xhebox](https://github.com/xhebox)の場合に文`SELECT CAST(n AS CHAR)`のクエリ結果が正しくない問題を修正しました
    -   MySQLカーソルフェッチプロトコル使用時に、結果セットのメモリ消費量が`tidb_mem_quota_query`上限を超え、TiDBのメモリオーバーフローが発生する問題を修正しました。修正後、TiDBは結果セットを自動的にディスクに書き込み、メモリを解放します[＃43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)
    -   BR [＃44716](https://github.com/pingcap/tidb/issues/44716) @ [天菜まお](https://github.com/tiancaiamao)を使用して`AUTO_ID_CACHE=1`テーブルを復元するときに発生する`duplicate entry`エラーを修正します
    -   テーブルパーティション定義で`FLOOR()`関数を使用してパーティション列を[＃42323](https://github.com/pingcap/tidb/issues/42323) @ [ジフハウス](https://github.com/jiyfhust)に丸めた場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正しました。
    -   同時ビューによって DDL 操作がブロックされる可能性がある問題を修正[＃40352](https://github.com/pingcap/tidb/issues/40352) @ [沢民州](https://github.com/zeminzhou)
    -   `datetime`値が[＃39336](https://github.com/pingcap/tidb/issues/39336) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)と正しくないために統計収集タスクが失敗する問題を修正しました
    -   クラスターのPDノードが交換された後、一部のDDL文が一定期間スタックする可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   PD時間[＃44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)に突然の変化があったときに`resolve lock`ハングする可能性がある問題を修正しました
    -   インデックススキャン[＃45126](https://github.com/pingcap/tidb/issues/45126) @ [wshwsh12](https://github.com/wshwsh12)における潜在的なデータ競合問題を修正
    -   `FormatSQL()`メソッドが入力[＃44542](https://github.com/pingcap/tidb/issues/44542) @ [ホーキングレイ](https://github.com/hawkingrei)の非常に長い SQL 文を適切に切り捨てることができない問題を修正しました。
    -   権限[＃45320](https://github.com/pingcap/tidb/issues/45320) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)がなくてもユーザーが`INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの情報を表示できる問題を修正
    -   `DATETIME`または`TIMESTAMP`列を数値定数[＃38361](https://github.com/pingcap/tidb/issues/38361) @ [イービン87](https://github.com/yibin87)と比較するときに、MySQL と動作が一致しない問題を修正しました。
    -   インデックス結合のエラーによりクエリが停止する可能性がある問題を修正[＃45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   接続を切断すると go コルーチン リークが発生する可能性がある問題を修正[＃46034](https://github.com/pingcap/tidb/issues/46034) @ [ピンギュ](https://github.com/pingyu)
    -   `tmp-storage-quota`設定が[＃45161](https://github.com/pingcap/tidb/issues/45161) [＃26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12)で有効にならない問題を修正
    -   クラスター[＃38484](https://github.com/pingcap/tidb/issues/38484) @ [ヘヘチェン](https://github.com/hehechen)でTiFlashノードがダウンした場合にTiFlashレプリカが利用できなくなる問題を修正しました。
    -   `Config.Labels`同時に読み書きする場合に、データ競合により TiDB がクラッシュする問題を修正[＃45561](https://github.com/pingcap/tidb/issues/45561) @ [ゲンリキ](https://github.com/gengliqi)
    -   クラスタが大きい場合、クライアントが定期的に更新される`min-resolved-ts` PD OOMを引き起こす可能性がある問題を修正しました[＃46664](https://github.com/pingcap/tidb/issues/46664) @ [HuSharp](https://github.com/HuSharp)

-   TiKV

    -   `ttl-check-poll-interval`設定項目がRawKV API V2 [＃15142](https://github.com/tikv/tikv/issues/15142) @ [ピンギュ](https://github.com/pingyu)で有効にならない問題を修正
    -   オンラインアンセーフリカバリがタイムアウト[＃15346](https://github.com/tikv/tikv/issues/15346) @ [コナー1996](https://github.com/Connor1996)で中止されない問題を修正
    -   `FLASHBACK` [＃15258](https://github.com/tikv/tikv/issues/15258) @ [金星の上](https://github.com/overvenus)を実行した後にリージョンマージがブロックされる可能性がある問題を修正しました
    -   1つのTiKVノードが分離され、別のノードが再起動されたときに発生する可能性のあるデータの不整合の問題を修正しました[＃15035](https://github.com/tikv/tikv/issues/15035) @ [金星の上](https://github.com/overvenus)
    -   データレプリケーション自動同期モード[＃14975](https://github.com/tikv/tikv/issues/14975) @ [ノルーシュ](https://github.com/nolouch)で同期回復フェーズでQPSがゼロに低下する問題を修正しました。
    -   暗号化により部分書き込み[＃15080](https://github.com/tikv/tikv/issues/15080) @ [タボキ](https://github.com/tabokie)中にデータ破損が発生する可能性がある問題を修正
    -   ストアハートビートの再試行回数を[＃15184](https://github.com/tikv/tikv/issues/15184) @ [ノルーシュ](https://github.com/nolouch)に減らして、ハートビートストームの問題を修正しました。
    -   保留中の圧縮バイト[＃14392](https://github.com/tikv/tikv/issues/14392) @ [コナー1996](https://github.com/Connor1996)量が多い場合にトラフィック制御が機能しない可能性がある問題を修正しました。
    -   PDとTiKV間のネットワーク中断によりPITRが[＃15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)で停止する可能性がある問題を修正しました
    -   TiCDC の古い値機能が有効になっているときに TiKV がより多くのメモリを消費する可能性がある問題を修正[＃14815](https://github.com/tikv/tikv/issues/14815) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   etcd がすでに起動しているがクライアントがまだ接続していない場合、クライアントを呼び出すと PD がpanic[＃6860](https://github.com/tikv/pd/issues/6860) @ [HuSharp](https://github.com/HuSharp)になる可能性がある問題を修正しました。
    -   リーダーが長時間退出できない問題を修正[＃6918](https://github.com/tikv/pd/issues/6918) @ [バッファフライ](https://github.com/bufferflies)
    -   配置ルールが`LOCATION_LABELS`使用する場合、SQL とルールチェッカーが[＃38605](https://github.com/pingcap/tidb/issues/38605) @ [ノルーシュ](https://github.com/nolouch)と互換性がない問題を修正しました
    -   PD が予期せず複数の学習者をリージョン[＃5786](https://github.com/tikv/pd/issues/5786) @ [ハンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正しました。
    -   ルールチェッカーがピア[＃6559](https://github.com/tikv/pd/issues/6559) @ [ノルーシュ](https://github.com/nolouch)を選択した場合に、不健全なピアを削除できない問題を修正しました
    -   `unsafe recovery`で不合格になった学習者のピアが`auto-detect`モード[＃6690](https://github.com/tikv/pd/issues/6690) @ [v01dstar](https://github.com/v01dstar)で無視される問題を修正

-   TiFlash

    -   `fsp` `DATETIME` 、 `TIMESTAMP` 、または`TIME`データ型[＃7809](https://github.com/pingcap/tiflash/issues/7809) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に変更した後にクエリが失敗する問題を修正しました
    -   領域[＃7762](https://github.com/pingcap/tiflash/issues/7762) @ [リデジュ](https://github.com/lidezhu)の無効な範囲キーによりTiFlashデータが不整合になる問題を修正しました
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに重大な影響を与える可能性がある問題を修正しました[＃7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)
    -   オンラインアンセーフリカバリ[＃7671](https://github.com/pingcap/tiflash/issues/7671) @ [ホンユニャン](https://github.com/hongyunyan)を使用した後、 TiFlashの再起動に時間がかかりすぎる問題を修正しました
    -   TiFlash が[＃6462](https://github.com/pingcap/tiflash/issues/6462) @ [リトルフォール](https://github.com/LittleFall)割り算を行うときに`DECIMAL`結果を誤って丸める問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   BRで使用されるグローバルパラメータ`TableColumnCountLimit`と`IndexLimit`デフォルト値を最大値[＃45793](https://github.com/pingcap/tidb/issues/45793) @ [リーヴルス](https://github.com/Leavrth)に増やすことで、復元が失敗する問題を修正しました。
        -   PITR [＃43184](https://github.com/pingcap/tidb/issues/43184) @ [リーヴルス](https://github.com/Leavrth)で DDL メタ情報を処理するときに書き換えが失敗する問題を修正しました
        -   PITR実行中に関数の戻り値をチェックしないことで発生するpanicの問題を修正[＃45853](https://github.com/pingcap/tidb/issues/45853) @ [リーヴルス](https://github.com/Leavrth)
        -   Amazon S3 [＃41916](https://github.com/pingcap/tidb/issues/41916) [＃42033](https://github.com/pingcap/tidb/issues/42033) @ [3ポイントシュート](https://github.com/3pointer)以外の S3 互換storage使用時に無効なリージョン ID が取得される問題を修正
        -   RawKVモード[＃37085](https://github.com/pingcap/tidb/issues/37085) @ [ピンギュ](https://github.com/pingyu)のきめ細かなバックアップフェーズで発生する可能性のあるエラーを修正
        -   TiDBクラスタ[＃40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)にPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正
        -   リージョンリーダーシップの移行が発生すると、PITR ログバックアップの進行のレイテンシーが長くなるという問題を軽減します[＃13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームでエラーが発生し、 [＃9450](https://github.com/pingcap/tiflow/issues/9450) @ [ヒック](https://github.com/hicqu)で再試行すると、レプリケーションタスクが停止する可能性がある問題を修正しました。
        -   Kafka [＃9504](https://github.com/pingcap/tiflow/issues/9504) @ [3エースショーハンド](https://github.com/3AceShowHand)に同期するときに再試行間隔が短いためにレプリケーションタスクが失敗する問題を修正しました
        -   TiCDC がアップストリーム[＃9430](https://github.com/pingcap/tiflow/issues/9430) @ [スドジ](https://github.com/sdojjy)の 1 つのトランザクションで複数の一意のキー行を変更するときに同期書き込み競合を引き起こす可能性がある問題を修正しました。
        -   TiCDC が誤って名前変更 DDL 操作を同期する可能性がある問題を修正[＃9488](https://github.com/pingcap/tiflow/issues/9488) [＃9378](https://github.com/pingcap/tiflow/issues/9378) [＃9531](https://github.com/pingcap/tiflow/issues/9531) @ [アズドンメン](https://github.com/asddongmen)
        -   下流で短期的な障害が発生したときにレプリケーションタスクが停止する可能性がある問題を修正[＃9542](https://github.com/pingcap/tiflow/issues/9542) [＃9272](https://github.com/pingcap/tiflow/issues/9272) [＃9582](https://github.com/pingcap/tiflow/issues/9582) [＃9592](https://github.com/pingcap/tiflow/issues/9592) @ [ヒック](https://github.com/hicqu)
        -   TiCDC ノードのステータスが[＃9354](https://github.com/pingcap/tiflow/issues/9354) @ [スドジ](https://github.com/sdojjy)に変化したときに発生する可能性のあるpanic問題を修正しました。
        -   Kafka Sink がエラーに遭遇すると、changefeed の進行[＃9309](https://github.com/pingcap/tiflow/issues/9309) @ [ヒック](https://github.com/hicqu)が無期限にブロックされる可能性がある問題を修正しました。
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームに過度のワークロードが発生する問題を修正しました[＃8957](https://github.com/pingcap/tiflow/issues/8957) [＃8959](https://github.com/pingcap/tiflow/issues/8959) @ [ハイラスティン](https://github.com/Rustin170506)
        -   一部の TiCDC ノードがネットワークから分離されているときに発生する可能性のあるデータの不整合の問題を修正[＃9344](https://github.com/pingcap/tiflow/issues/9344) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   再実行ログが有効で、下流に例外[＃9172](https://github.com/pingcap/tiflow/issues/9172) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)がある場合にレプリケーションタスクが停止する可能性がある問題を修正しました。
        -   PD [＃9294](https://github.com/pingcap/tiflow/issues/9294) @ [アズドンメン](https://github.com/asddongmen)が一時的に利用できないために変更フィードが失敗する問題を修正しました
        -   TiDB または MySQL [＃9180](https://github.com/pingcap/tiflow/issues/9180) @ [アズドンメン](https://github.com/asddongmen)にデータを複製するときに、下流の双方向レプリケーション関連の変数を頻繁に設定することによって発生する下流ログが多すぎる問題を修正しました。
        -   Avroプロトコルが`Enum`タイプの値[＃9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)を誤って識別する問題を修正しました

    -   TiDB データ移行 (DM)

        -   一意のキー列名が null の場合に発生するpanic問題を修正[＃9247](https://github.com/pingcap/tiflow/issues/9247) @ [ランス6716](https://github.com/lance6716)
        -   バリデータがエラーを誤って処理した場合に発生する可能性のあるデッドロックの問題を修正し、再試行メカニズムを最適化します[＃9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3ハンター](https://github.com/D3Hunter)
        -   因果関係キー[＃9489](https://github.com/pingcap/tiflow/issues/9489) @ [ヒヒフフ](https://github.com/hihihuhu)を計算するときに照合順序が考慮されない問題を修正しました

    -   TiDB Lightning

        -   エンジンがデータ[＃44867](https://github.com/pingcap/tidb/issues/44867) @ [D3ハンター](https://github.com/D3Hunter)をインポートしているときにディスク クォータ チェックがブロックされる可能性がある問題を修正しました
        -   ターゲットクラスタ[＃45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)で SSL が有効になっているときにチェックサムがエラー`Region is unavailable`を報告する問題を修正しました
        -   エンコードエラーが正しく記録されない問題を修正[＃44321](https://github.com/pingcap/tidb/issues/44321) @ [lyzx2001](https://github.com/lyzx2001)
        -   CSVデータ[＃43284](https://github.com/pingcap/tidb/issues/43284) @ [lyzx2001](https://github.com/lyzx2001)をインポートする際にルートがpanicになる可能性がある問題を修正
        -   論理インポートモードでテーブル A をインポートすると、テーブル B が存在しないと誤って報告される可能性がある問題を修正しました[＃44614](https://github.com/pingcap/tidb/issues/44614) @ [dsdashun](https://github.com/dsdashun)
        -   `NEXT_GLOBAL_ROW_ID` [＃45427](https://github.com/pingcap/tidb/issues/45427) @ [lyzx2001](https://github.com/lyzx2001)を保存するときにデータ型が間違っている問題を修正しました
        -   `checksum = "optional"` [＃45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)のときにチェックサムがエラーを報告する問題を修正しました
        -   PDクラスタアドレスが[＃43436](https://github.com/pingcap/tidb/issues/43436) @ [リチュンジュ](https://github.com/lichunzhu)に変更されるとデータのインポートが失敗する問題を修正しました
        -   一部のPDノードが[＃43400](https://github.com/pingcap/tidb/issues/43400) @ [リチュンジュ](https://github.com/lichunzhu)で失敗した場合にデータのインポートが失敗する問題を修正しました
        -   自動増分列を持つテーブルが`AUTO_ID_CACHE=1`設定すると、ID アロケータのベース値が正しくなくなる[＃46100](https://github.com/pingcap/tidb/issues/46100) @ [D3ハンター](https://github.com/D3Hunter)という問題を修正しました

    -   Dumpling

        -   Amazon S3 [＃45353](https://github.com/pingcap/tidb/issues/45353) @ [リチュンジュ](https://github.com/lichunzhu)にエクスポートするときに、未処理のファイルライターの終了エラーによりエクスポートされたファイルが失われる問題を修正しました

    -   TiDBBinlog

        -   etcdクライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[＃1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [リチュンジュ](https://github.com/lichunzhu)
