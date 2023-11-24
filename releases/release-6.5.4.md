---
title: TiDB 6.5.4 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 6.5.4.
---

# TiDB 6.5.4 リリースノート {#tidb-6-5-4-release-notes}

発売日：2023年8月28日

TiDB バージョン: 6.5.4

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.5.4#version-list)

## 互換性の変更 {#compatibility-changes}

-   `Cursor Fetch`を使用して大きな結果セットをフェッチすると、TiDB がメモリを大量に消費する問題を修正するために、TiDB は自動的に結果セットをディスクに書き込み、メモリ[#43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)を解放します。
-   RocksDB の定期的な圧縮をデフォルトで無効にすることで、TiKV RocksDB のデフォルトの動作が v6.5.0 より前のバージョンの動作と一致するようになりました。この変更により、アップグレード後の大量の圧縮によって引き起こされる潜在的なパフォーマンスへの影響が防止されます。さらに、TiKV では 2 つの新しい構成項目[`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#periodic-compaction-seconds-new-in-v654)および[`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v6.5/tikv-configuration-file#ttl-new-in-v654)が導入され、RocksDB [#15355](https://github.com/tikv/tikv/issues/15355) @ [リククスサシネーター](https://github.com/LykxSassinator)の定期的な圧縮を手動で構成できるようになります。

## 改善点 {#improvements}

-   TiDB

    -   代入式[#46081](https://github.com/pingcap/tidb/issues/46081) @ [ゲンリキ](https://github.com/gengliqi)を含む`LOAD DATA`ステートメントのパフォーマンスを最適化します。
    -   ディスク[#45125](https://github.com/pingcap/tidb/issues/45125) @ [ヤンケオ](https://github.com/YangKeao)からダンプされたチャンクを読み取るパフォーマンスを最適化します。
    -   PD スケジューリング[#6493](https://github.com/tikv/pd/issues/6493) @ [Jmポテト](https://github.com/JmPotato)を一時停止する`halt-scheduling`構成項目を追加します。

-   TiKV

    -   `check_leader`リクエストに gzip 圧縮を使用してトラフィック[#14553](https://github.com/tikv/tikv/issues/14553) @ [あなた06](https://github.com/you06)を削減します
    -   `Max gap of safe-ts`と`Min safe ts region`メトリクスを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、 resolved-tsとsafe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)のステータスをより適切に観察および診断します。
    -   TiKV で一部の RocksDB 構成を公開し、ユーザーが TTL や定期的な圧縮などの機能を無効にできるようにします[#14873](https://github.com/tikv/tikv/issues/14873) @ [リククスサシネーター](https://github.com/LykxSassinator)
    -   他のスレッドへの影響を防ぐために、Titan マニフェスト ファイルを書き込むときにミューテックスを保持しないようにします[#15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)

-   PD

    -   Swaggerサーバーが有効になっていない場合、デフォルトで Swagger API のブロックをサポート[#6786](https://github.com/tikv/pd/issues/6786) @ [バッファフライ](https://github.com/bufferflies)
    -   etcd [#6554](https://github.com/tikv/pd/issues/6554) [#6442](https://github.com/tikv/pd/issues/6442) @ [lhy1024](https://github.com/lhy1024)の高可用性を向上させます
    -   `GetRegions`リクエスト[#6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)のメモリ消費量を削減
    -   HTTP 接続の再利用をサポート[#6913](https://github.com/tikv/pd/issues/6913) @ [ノールーシュ](https://github.com/nolouch)

-   TiFlash

    -   IO バッチ最適化[#7735](https://github.com/pingcap/tiflash/issues/7735) @ [リデジュ](https://github.com/lidezhu)によりTiFlash書き込みパフォーマンスを向上
    -   不要な fsync 操作を削除することで、 TiFlash書き込みパフォーマンスを向上させます[#7736](https://github.com/pingcap/tiflash/issues/7736) @ [リデジュ](https://github.com/lidezhu)
    -   TiFlashコプロセッサ タスク キューの最大長を制限して、TiFlash のサービス可用性に影響を与えるコプロセッサ タスクの過剰なキューイングを回避します[#7747](https://github.com/pingcap/tiflash/issues/7747) @ [リトルフォール](https://github.com/LittleFall)

-   ツール

    -   バックアップと復元 (BR)

        -   HTTP クライアント[#46011](https://github.com/pingcap/tidb/issues/46011) @ [レヴルス](https://github.com/Leavrth)で`MaxIdleConns`および`MaxIdleConnsPerHost`パラメータを設定することにより、接続再利用のサポートを強化します。
        -   PD または外部 S3storage[#42909](https://github.com/pingcap/tidb/issues/42909) @ [レヴルス](https://github.com/Leavrth)への接続に失敗した場合のBRのフォールト トレランスを向上させます。
        -   新しい復元パラメータを追加します`WaitTiflashReady` 。このパラメータが有効な場合、 TiFlashレプリカが正常に複製された後に復元操作が完了します[#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @ [3ポインター](https://github.com/3pointer)

    -   TiCDC

        -   TiCDC が失敗後に再試行するときのステータス メッセージを調整します[#9483](https://github.com/pingcap/tiflow/issues/9483) @ [東門](https://github.com/asddongmen)
        -   ダウンストリーム[#9574](https://github.com/pingcap/tiflow/issues/9574) @ [3エースショーハンド](https://github.com/3AceShowHand)への主キーの送信のみをサポートすることにより、Kafka と同期するときに制限を超えるメッセージを TiCDC が処理する方法を最適化します。
        -   Storage Sink は、HEX 形式のデータの 16 進エンコードをサポートするようになり、AWS DMS 形式仕様[#9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)と互換性があります。

    -   TiDB データ移行 (DM)

        -   互換性のない DDL ステートメントに対する厳密な楽観的モードのサポート[#9112](https://github.com/pingcap/tiflow/issues/9112) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   Dumpling

        -   `-sql`パラメータ[#45239](https://github.com/pingcap/tidb/issues/45239) @ [ランス6716](https://github.com/lance6716)を使用してデータをエクスポートするときに、すべてのデータベースとテーブルのクエリをスキップすることで、エクスポートのオーバーヘッドを削減します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `STREAM_AGG()`演算子[#40857](https://github.com/pingcap/tidb/issues/40857) @ [ドゥーシール9](https://github.com/Dousir9)を押し下げると`index out of range`エラーが報告されることがある問題を修正
    -   `CREATE TABLE`ステートメントにサブパーティション定義[#41198](https://github.com/pingcap/tidb/issues/41198) [#41200](https://github.com/pingcap/tidb/issues/41200) @ [むじょん](https://github.com/mjonss)が含まれている場合、TiDB がすべてのパーティション情報を無視し、非パーティションテーブルを作成する問題を修正します。
    -   `stale_read_ts`設定が間違っていると`PREPARE stmt`がデータを誤って読み取る可能性がある問題を修正します[#43044](https://github.com/pingcap/tidb/issues/43044) @ [あなた06](https://github.com/you06)
    -   ActivateTxn [#42092](https://github.com/pingcap/tidb/issues/42092) @ [ホーキングレイ](https://github.com/hawkingrei)で発生する可能性のあるデータ競合の問題を修正
    -   バッチ クライアントがタイムリーに再接続しない問題を修正[#44431](https://github.com/pingcap/tidb/issues/44431) @ [クレイジークス520](https://github.com/crazycs520)
    -   SQL コンパイル エラー ログが編集されない問題を修正[#41831](https://github.com/pingcap/tidb/issues/41831) @ [ランス6716](https://github.com/lance6716)
    -   CTE と相関サブクエリを同時に使用すると、不正なクエリ結果またはpanicが発生する可能性がある問題を修正します[#44649](https://github.com/pingcap/tidb/issues/44649) [#38170](https://github.com/pingcap/tidb/issues/38170) [#44774](https://github.com/pingcap/tidb/issues/44774) @ [ウィノロス](https://github.com/winoros) @ [グオシャオゲ](https://github.com/guo-shaoge)
    -   TTL タスクが時間[#40109](https://github.com/pingcap/tidb/issues/40109) @ [ヤンケオ](https://github.com/YangKeao)で統計更新をトリガーできない問題を修正
    -   GC Resolve Locks ステップで一部の悲観的ロック[#45134](https://github.com/pingcap/tidb/issues/45134) @ [ミョンケミンタ](https://github.com/MyonKeminta)が見逃される可能性がある問題を修正します。
    -   メモリトラッカー[#44612](https://github.com/pingcap/tidb/issues/44612) @ [wshwsh12](https://github.com/wshwsh12)の潜在的なメモリリークの問題を修正
    -   `INFORMATION_SCHEMA.DDL_JOBS`テーブルの`QUERY`列のデータ長が列定義[#42440](https://github.com/pingcap/tidb/issues/42440) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を超える場合がある問題を修正
    -   多数のリージョンがあるにもかかわらず、 `Prepare`または`Execute` [#39605](https://github.com/pingcap/tidb/issues/39605) @ [djshow832](https://github.com/djshow832)を使用して一部の仮想テーブルをクエリするときにテーブル ID をプッシュダウンできない場合の PD OOM の問題を修正します。
    -   パーティションテーブル[#41638](https://github.com/pingcap/tidb/issues/41638) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)に新しいインデックスを追加した後、パーティションテーブルテーブルで統計の自動収集が正しくトリガーされないことがある問題を修正します。
    -   統計における SQL 実行の詳細の過剰なメモリ消費により、極端な場合に TiDB OOM が発生する問題を修正します[#44047](https://github.com/pingcap/tidb/issues/44047) @ [wshwsh12](https://github.com/wshwsh12)
    -   バッチ コプロセッサの再試行により、クエリ失敗[#44622](https://github.com/pingcap/tidb/issues/44622) @ [ウィンドトーカー](https://github.com/windtalker)の原因となる誤ったリージョン情報が生成される可能性がある問題を修正します。
    -   `indexMerge`のクエリが[#45279](https://github.com/pingcap/tidb/issues/45279) @ [xzhangxian1008](https://github.com/xzhangxian1008)で強制終了されたときに発生するハングアップの問題を修正します。
    -   システム テーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正します[#45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   `tidb_enable_parallel_apply`が有効になっている場合、MPP モードでのクエリ結果が正しくない問題を修正します[#45299](https://github.com/pingcap/tidb/issues/45299) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `tidb_opt_agg_push_down`が有効になっている場合にクエリが間違った結果を返す可能性がある問題を修正します[#44795](https://github.com/pingcap/tidb/issues/44795) @ [アイリンキッド](https://github.com/AilinKid)
    -   仮想列[#41014](https://github.com/pingcap/tidb/issues/41014) @ [アイリンキッド](https://github.com/AilinKid)によって引き起こされる適切な物理プランが見つからない問題を修正
    -   空の`processInfo` [#43829](https://github.com/pingcap/tidb/issues/43829) @ [ジムララ](https://github.com/zimulala)によって引き起こされるpanicの問題を修正
    -   ステートメント内の`n`負の数[#44786](https://github.com/pingcap/tidb/issues/44786) @ [ゼボックス](https://github.com/xhebox)である場合、 `SELECT CAST(n AS CHAR)`ステートメントのクエリ結果が正しくない問題を修正します。
    -   MySQL カーソル フェッチ プロトコルを使用すると、結果セットのメモリ消費量が`tidb_mem_quota_query`制限を超え、TiDB OOM が発生する可能性がある問題を修正します。修正後、TiDB は自動的に結果セットをディスクに書き込み、メモリ[#43233](https://github.com/pingcap/tidb/issues/43233) @ [ヤンケオ](https://github.com/YangKeao)を解放します。
    -   BR [#44716](https://github.com/pingcap/tidb/issues/44716) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を使用して`AUTO_ID_CACHE=1`持つテーブルを復元するときに発生する`duplicate entry`エラーを修正しました。
    -   テーブル パーティション定義で`FLOOR()`関数を使用してパーティション列[#42323](https://github.com/pingcap/tidb/issues/42323) @ [ジフフスト](https://github.com/jiyfhust)を四捨五入する場合、 `SELECT`ステートメントがパーティションテーブルに対してエラーを返す問題を修正します。
    -   同時ビューにより DDL 操作がブロックされる可能性がある問題を修正[#40352](https://github.com/pingcap/tidb/issues/40352) @ [沢民州](https://github.com/zeminzhou)
    -   不正な`datetime`値[#39336](https://github.com/pingcap/tidb/issues/39336) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)が原因で統計収集タスクが失敗する問題を修正します。
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間スタックすることがある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   PD時間[#44822](https://github.com/pingcap/tidb/issues/44822) @ [ジグアン](https://github.com/zyguan)が急変した場合に`resolve lock`がハングすることがある問題を修正
    -   インデックス スキャン[#45126](https://github.com/pingcap/tidb/issues/45126) @ [wshwsh12](https://github.com/wshwsh12)における潜在的なデータ競合の問題を修正
    -   `FormatSQL()`メソッドが入力[#44542](https://github.com/pingcap/tidb/issues/44542) @ [ホーキングレイ](https://github.com/hawkingrei)の非常に長い SQL ステートメントを適切に切り詰めることができない問題を修正します。
    -   ユーザーが権限なしでも`INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの情報を表示できる問題を修正[#45320](https://github.com/pingcap/tidb/issues/45320) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   `DATETIME`または`TIMESTAMP`列を数値定数[#38361](https://github.com/pingcap/tidb/issues/38361) @ [イービン87](https://github.com/yibin87)と比較するときに動作が MySQL と矛盾する問題を修正
    -   インデックス結合のエラーによりクエリがスタックする可能性がある問題を修正します[#45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   接続を強制終了すると go コルーチン リーク[#46034](https://github.com/pingcap/tidb/issues/46034) @ [ピンギュ](https://github.com/pingyu)が発生する可能性がある問題を修正
    -   `tmp-storage-quota`設定が有効にならない問題を修正[#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12)
    -   クラスター[#38484](https://github.com/pingcap/tidb/issues/38484) @ [へへへん](https://github.com/hehechen)でTiFlashノードがダウンしているときに、 TiFlashレプリカが利用できなくなる可能性がある問題を修正
    -   `Config.Lables` [#45561](https://github.com/pingcap/tidb/issues/45561) @ [ゲンリキ](https://github.com/gengliqi)を同時に読み書きすると、データ競合の可能性が原因で TiDB がクラッシュする問題を修正
    -   クラスターが大きい[#46664](https://github.com/pingcap/tidb/issues/46664) @ [ヒューシャープ](https://github.com/HuSharp)の場合、client-go を定期的`min-resolved-ts`更新すると PD OOM が発生する可能性がある問題を修正

-   TiKV

    -   RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @ [ピンギュ](https://github.com/pingyu)で`ttl-check-poll-interval`設定項目が有効にならない問題を修正
    -   オンライン安全でないリカバリがタイムアウト[#15346](https://github.com/tikv/tikv/issues/15346) @ [コナー1996](https://github.com/Connor1996)で中止されない問題を修正
    -   `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @ [オーバーヴィーナス](https://github.com/overvenus)を実行した後、 リージョン Merge がブロックされる場合がある問題を修正
    -   1 つの TiKV ノードが分離され、別のノードが再起動されたときに発生する可能性があるデータの不整合の問題を修正します[#15035](https://github.com/tikv/tikv/issues/15035) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   データ レプリケーション自動同期モード[#14975](https://github.com/tikv/tikv/issues/14975) @ [ノールーシュ](https://github.com/nolouch)の同期回復フェーズで QPS がゼロに低下する問題を修正します。
    -   暗号化により部分書き込み[#15080](https://github.com/tikv/tikv/issues/15080) @ [タボキー](https://github.com/tabokie)中にデータ破損が発生する可能性がある問題を修正
    -   ストア ハートビートの再試行数を[#15184](https://github.com/tikv/tikv/issues/15184) @ [ノールーシュ](https://github.com/nolouch)に減らすことで、ハートビートハートビートストームの問題を修正します。
    -   保留中の圧縮バイト[#14392](https://github.com/tikv/tikv/issues/14392) @ [コナー1996](https://github.com/Connor1996)が大量にある場合、トラフィック制御が機能しない可能性がある問題を修正
    -   PD と TiKV の間のネットワークの中断により PITR がスタックする可能性がある問題を修正します[#15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)
    -   TiCDC の古い値機能が有効になっている場合、TiKV がより多くのメモリを消費する可能性がある問題を修正します[#14815](https://github.com/tikv/tikv/issues/14815) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   etcd がすでに開始されているが、クライアントがまだ接続していないときに、クライアントを呼び出すと PD がpanic[#6860](https://github.com/tikv/pd/issues/6860) @ [ヒューシャープ](https://github.com/HuSharp)になる可能性がある問題を修正します。
    -   リーダーが長時間抜けられない問題を修正[#6918](https://github.com/tikv/pd/issues/6918) @ [バッファフライ](https://github.com/bufferflies)
    -   配置ルールが`LOCATION_LABLES`使用する場合、SQL とルール チェッカーに互換性がないという問題を修正します[#38605](https://github.com/pingcap/tidb/issues/38605) @ [ノールーシュ](https://github.com/nolouch)
    -   PD が予期せず複数の学習者をリージョン[#5786](https://github.com/tikv/pd/issues/5786) @ [フンドゥンDM](https://github.com/HunDunDM)に追加する可能性がある問題を修正
    -   ルールチェッカーがピア[#6559](https://github.com/tikv/pd/issues/6559) @ [ノールーシュ](https://github.com/nolouch)を選択すると、異常なピアを削除できない問題を修正
    -   `unsafe recovery`で失敗した学習者ピアが`auto-detect`モード[#6690](https://github.com/tikv/pd/issues/6690) @ [v01dstar](https://github.com/v01dstar)で無視される問題を修正

-   TiFlash

    -   `DATETIME` 、 `TIMESTAMP` 、または`TIME`データ型[#7809](https://github.com/pingcap/tiflash/issues/7809) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)の`fsp`が変更された後にクエリが失敗する問題を修正します。
    -   リージョン[#7762](https://github.com/pingcap/tiflash/issues/7762) @ [リデズ](https://github.com/lidezhu)の無効な範囲キーによりTiFlashデータが不整合になる問題を修正
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに過度に時​​間がかかり、クエリのパフォーマンス[#7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)に深刻な影響を与える可能性がある問題を修正します。
    -   Online Unsafe Recovery [#7671](https://github.com/pingcap/tiflash/issues/7671) @ [ホンユニャン](https://github.com/hongyunyan)を使用した後のTiFlash の再起動に時間がかかりすぎる問題を修正
    -   除算[#6462](https://github.com/pingcap/tiflash/issues/6462) @ [リトルフォール](https://github.com/LittleFall)を実行するときにTiFlash が`DECIMAL`結果を誤って丸める問題を修正

-   ツール

    -   バックアップと復元 (BR)

        -   BRで使用されるグローバル パラメータ`TableColumnCountLimit`および`IndexLimit`のデフォルト値を最大値[#45793](https://github.com/pingcap/tidb/issues/45793) @ [レヴルス](https://github.com/Leavrth)に増やすことで、復元の失敗の問題を修正します。
        -   PITR [#43184](https://github.com/pingcap/tidb/issues/43184) @ [レヴルス](https://github.com/Leavrth)で DDL メタ情報を処理するときに書き換えが失敗する問題を修正
        -   PITR 実行中に関数の戻り値をチェックしないことによって発生するpanicの問題を修正[#45853](https://github.com/pingcap/tidb/issues/45853) @ [レヴルス](https://github.com/Leavrth)
        -   Amazon S3 [#41916](https://github.com/pingcap/tidb/issues/41916) [#42033](https://github.com/pingcap/tidb/issues/42033) @ [3ポインター](https://github.com/3pointer)以外の S3 互換storageを使用する場合に無効なリージョン ID を取得する問題を修正
        -   RawKV モード[#37085](https://github.com/pingcap/tidb/issues/37085) @ [ピンギュ](https://github.com/pingyu)の詳細なバックアップ フェーズで発生する可能性のあるエラーを修正しました。
        -   TiDB クラスター[#40759](https://github.com/pingcap/tidb/issues/40759) @ [ジョッカウ](https://github.com/joccau)に PITR バックアップ タスクがない場合、 `resolve lock`の頻度が高すぎる問題を修正
        -   リージョンリーダーの移行が発生したときに PITR ログ バックアップの進行状況のレイテンシーが増加する問題を緩和します[#13638](https://github.com/tikv/tikv/issues/13638) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   ダウンストリームでエラーが発生し、 [#9450](https://github.com/pingcap/tiflow/issues/9450) @ [ひっくり返る](https://github.com/hicqu)を再試行すると、レプリケーション タスクが停止する可能性がある問題を修正します。
        -   Kafka [#9504](https://github.com/pingcap/tiflow/issues/9504) @ [3エースショーハンド](https://github.com/3AceShowHand)と同期するときに、再試行間隔が短いためにレプリケーション タスクが失敗する問題を修正します。
        -   アップストリーム[#9430](https://github.com/pingcap/tiflow/issues/9430) @ [スドジ](https://github.com/sdojjy)の 1 つのトランザクションで複数の一意のキー行を変更すると、TiCDC が同期書き込みの競合を引き起こす可能性がある問題を修正します。
        -   TiCDC が名前変更 DDL 操作を誤って同期する可能性がある問題を修正します[#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @ [東門](https://github.com/asddongmen)
        -   ダウンストリームで短期間の障害が発生したときにレプリケーション タスクが停止する可能性がある問題を修正します[#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272) [#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @ [ひっくり返る](https://github.com/hicqu)
        -   TiCDC ノードのステータスが[#9354](https://github.com/pingcap/tiflow/issues/9354) @ [スドジ](https://github.com/sdojjy)に変化したときに発生する可能性があるpanicの問題を修正しました。
        -   Kafka シンクでエラーが発生すると、変更フィードの進行が無期限にブロックされる可能性がある問題を修正します[#9309](https://github.com/pingcap/tiflow/issues/9309) @ [ひっくり返る](https://github.com/hicqu)
        -   ダウンストリームが Kafka の場合、TiCDC がダウンストリームのメタデータを頻繁にクエリし、ダウンストリームで過度のワークロードが発生する問題を修正します[#8957](https://github.com/pingcap/tiflow/issues/8957) [#8959](https://github.com/pingcap/tiflow/issues/8959) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   一部の TiCDC ノードがネットワーク[#9344](https://github.com/pingcap/tiflow/issues/9344) @ [CharlesCheung96](https://github.com/CharlesCheung96)から分離されている場合に発生する可能性があるデータの不整合の問題を修正します。
        -   REDO ログが有効で、ダウンストリーム[#9172](https://github.com/pingcap/tiflow/issues/9172) @ [CharlesCheung96](https://github.com/CharlesCheung96)で例外が発生した場合にレプリケーション タスクが停止する可能性がある問題を修正します。
        -   PD [#9294](https://github.com/pingcap/tiflow/issues/9294) @ [東門](https://github.com/asddongmen)が一時的に利用できないために変更フィードが失敗する問題を修正
        -   データを TiDB または MySQL [#9180](https://github.com/pingcap/tiflow/issues/9180) @ [東門](https://github.com/asddongmen)にレプリケートするときに、ダウンストリーム双方向レプリケーション関連の変数を頻繁に設定することによって発生するダウンストリーム ログが多すぎる問題を修正します。
        -   Avro プロトコルが`Enum` type 値[#9259](https://github.com/pingcap/tiflow/issues/9259) @ [3エースショーハンド](https://github.com/3AceShowHand)を誤って識別する問題を修正

    -   TiDB データ移行 (DM)

        -   一意のキー列名が null [#9247](https://github.com/pingcap/tiflow/issues/9247) @ [ランス6716](https://github.com/lance6716)の場合のpanicの問題を修正
        -   バリデーターがエラーを正しく処理しない場合に発生する可能性のあるデッドロックの問題を修正し、再試行メカニズム[#9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3ハンター](https://github.com/D3Hunter)を最適化します。
        -   因果関係キー[#9489](https://github.com/pingcap/tiflow/issues/9489) @ [ヒヒヒヒヒ](https://github.com/hihihuhu)を計算するときに照合順序が考慮されない問題を修正

    -   TiDB Lightning

        -   エンジンがデータ[#44867](https://github.com/pingcap/tidb/issues/44867) @ [D3ハンター](https://github.com/D3Hunter)をインポートしているときにディスク クォータ チェックがブロックされる可能性がある問題を修正します。
        -   ターゲット クラスタ[#45462](https://github.com/pingcap/tidb/issues/45462) @ [D3ハンター](https://github.com/D3Hunter)で SSL が有効になっている場合、チェックサムがエラー`Region is unavailable`を報告する問題を修正します。
        -   エンコードエラーが正しくログに記録されない問題を修正[#44321](https://github.com/pingcap/tidb/issues/44321) @ [lyzx2001](https://github.com/lyzx2001)
        -   CSVデータ[#43284](https://github.com/pingcap/tidb/issues/43284) @ [lyzx2001](https://github.com/lyzx2001)のインポート時にルートがpanicになる問題を修正
        -   論理インポート モードでテーブル A をインポートすると、テーブル B が存在しないと誤って報告される可能性がある問題を修正します[#44614](https://github.com/pingcap/tidb/issues/44614) @ [dsダシュン](https://github.com/dsdashun)
        -   `NEXT_GLOBAL_ROW_ID` [#45427](https://github.com/pingcap/tidb/issues/45427) @ [lyzx2001](https://github.com/lyzx2001)を保存する際にデータ型が間違っている問題を修正
        -   `checksum = "optional"` [#45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)の場合でもチェックサムがエラーを報告する問題を修正
        -   PDクラスタアドレスが[#43436](https://github.com/pingcap/tidb/issues/43436) @ [リチュンジュ](https://github.com/lichunzhu)に変更されるとデータインポートが失敗する問題を修正
        -   一部の PD ノードが失敗した場合にデータのインポートが失敗する問題を修正[#43400](https://github.com/pingcap/tidb/issues/43400) @ [リチュンジュ](https://github.com/lichunzhu)
        -   自動インクリメンタル列を持つテーブルが`AUTO_ID_CACHE=1`設定されている場合、ID アロケーターの基本値が正しくない[#46100](https://github.com/pingcap/tidb/issues/46100) @ [D3ハンター](https://github.com/D3Hunter)という問題を修正します。

    -   Dumpling

        -   Amazon S3 [#45353](https://github.com/pingcap/tidb/issues/45353) @ [リチュンジュ](https://github.com/lichunzhu)にエクスポートするときに、未処理のファイルライター終了エラーによりエクスポートされたファイルが失われる問題を修正

    -   TiDBBinlog

        -   etcd クライアントが初期化中に最新のノード情報を自動的に同期しない問題を修正[#1236](https://github.com/pingcap/tidb-binlog/issues/1236) @ [リチュンジュ](https://github.com/lichunzhu)
