---
title: TiDB 7.1.2 Release Notes
summary: TiDB 7.1.2 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.2 リリースノート {#tidb-7-1-2-release-notes}

発売日：2023年10月25日

TiDB バージョン: 7.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   セキュリティ強化モード（SEM）で[`require_secure_transport`](https://docs.pingcap.com/tidb/v7.1/system-variables#require_secure_transport-new-in-v610)を`ON`に設定することを禁止し、ユーザーの潜在的な接続問題を防ぎます。 [＃47665](https://github.com/pingcap/tidb/issues/47665) @ [tiancaiamao](https://github.com/tiancaiamao)
-   [スムーズなアップグレード](/smooth-upgrade-tidb.md)機能はデフォルトで無効になっています。有効にするには、 `/upgrade/start`と`upgrade/finish` HTTPリクエストをに送信します。 [＃47172](https://github.com/pingcap/tidb/issues/47172) @ [zimulala](https://github.com/zimulala)
-   オプティマイザがテーブルに対してハッシュ結合を選択するかどうかを制御する[`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_opt_enable_hash_join-new-in-v712)システム変数を導入します。 [＃46695](https://github.com/pingcap/tidb/issues/46695) @ [coderplay](https://github.com/coderplay)
-   RocksDBの定期的な圧縮をデフォルトで無効にすることで、TiKV RocksDBのデフォルトの動作がv6.5.0より前のバージョンと一致するようになりました。この変更により、アップグレード後に大量の圧縮が行われることによるパフォーマンスへの影響を回避できます。さらに、TiKVでは2つの新しい設定項目[`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#periodic-compaction-seconds-new-in-v712)と[`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#ttl-new-in-v712)導入され、RocksDB の定期的な圧縮を手動で設定できるようになりました。 [＃15355](https://github.com/tikv/tikv/issues/15355) @ [LykxSassinator](https://github.com/LykxSassinator)
-   TiCDCは、CSVプロトコルにおけるバイナリデータのエンコード方式を制御するための設定項目[`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)導入しました。デフォルト値は`'base64'` です。 [＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)
-   TiCDC では、設定項目[`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)導入されています。デフォルトでは空で、メッセージサイズが Kafka トピックの制限を超えると changefeed が失敗します。この設定を`"handle-key-only"`に設定すると、メッセージがサイズ制限を超えた場合、メッセージサイズを縮小するためにハンドルキーのみが送信されます。縮小されたメッセージでも制限を超える場合、changefeed はで失敗します。 [＃9680](https://github.com/pingcap/tiflow/issues/9680) @ [3AceShowHand](https://github.com/3AceShowHand)

### 動作の変更 {#behavior-changes}

-   複数の変更を含むトランザクションにおいて、更新イベントで主キーまたはNULL以外の一意インデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割し、すべてのイベントが挿入イベントに先行する削除イベントの順序に従うようにします。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-multiple-update-changes)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-)、[`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)、[`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)、[`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-)、[`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-)を含む新しいオプティマイザヒントを追加 [＃45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    -   コプロセッサに関連する要求元情報を追加します [＃46514](https://github.com/pingcap/tidb/issues/46514) @ [you06](https://github.com/you06)
    -   TiDBノードのアップグレードステータスの開始と終了をマークするために`/upgrade/start`と`upgrade/finish` APIを追加します。 [＃47172](https://github.com/pingcap/tidb/issues/47172) @ [zimulala](https://github.com/zimulala)

-   TiKV

    -   圧縮メカニズムを最適化します。リージョンが分割されるときに、分割するキーがない場合、圧縮がトリガーされ、過剰な MVCC バージョンが排除されます。 [＃15282](https://github.com/tikv/tikv/issues/15282) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   ルータオブジェクトのLRUCacheを排除してメモリ使用量を削減し、OOM を防止します。 [＃15430](https://github.com/tikv/tikv/issues/15430) @ [Connor1996](https://github.com/Connor1996)
    -   `Max gap of safe-ts`と`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、resolved-tsと安全な ts の状態をより適切に観察および診断します[＃15082](https://github.com/tikv/tikv/issues/15082) @ [ekexium](https://github.com/ekexium)
    -   TiKV で RocksDB の設定を公開し、ユーザーが TTL や定期的な圧縮などの機能を無効にできるようにします[＃14873](https://github.com/tikv/tikv/issues/14873) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   接続再試行のプロセスでPDクライアントのバックオフメカニズムを追加し、エラー再試行中に再試行間隔を徐々に増やしてPD圧力を軽減します。 [＃15428](https://github.com/tikv/tikv/issues/15428) @ [nolouch](https://github.com/nolouch)
    -   Titan マニフェストファイルを書き込むときにミューテックスを保持しないようにして、他のスレッドに影響を与えないようにします[＃15351](https://github.com/tikv/tikv/issues/15351) @ [Connor1996](https://github.com/Connor1996)
    -   OOM を防ぐためにリゾルバのメモリ使用量を最適化します [＃15458](https://github.com/tikv/tikv/issues/15458) @ [overvenus](https://github.com/overvenus)

-   PD

    -   PD 呼び出し元のバックオフ メカニズムを最適化して、呼び出しが失敗したときの RPC 要求の頻度を減らします[＃6556](https://github.com/tikv/pd/issues/6556) @ [nolouch](https://github.com/nolouch) @ [rleungx](https://github.com/rleungx) @ [HuSharp](https://github.com/HuSharp)
    -   発信者が切断されたときにCPUとメモリを時間内に解放するために、 `GetRegions`インターフェースにキャンセルメカニズムを導入する[＃6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   Grafana のインデックスデータのメモリ使用量の監視メトリックを追加します [＃8050](https://github.com/pingcap/tiflash/issues/8050) @ [hongyunyan](https://github.com/hongyunyan)

-   ツール

    -   Backup & Restore (BR)

        -   HTTPクライアントで`MaxIdleConns`と`MaxIdleConnsPerHost`パラメータを設定することにより、ログバックアップとPITRリストアタスクの接続再利用のサポートを強化します。 [＃46011](https://github.com/pingcap/tidb/issues/46011) @ [Leavrth](https://github.com/Leavrth)
        -   ログバックアップのCPUオーバーヘッドを削減`resolve lock` [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [3pointer](https://github.com/3pointer)
        -   新しい復元パラメータ`WaitTiflashReady`を追加します。このパラメータを有効にすると、 TiFlashレプリカが正常に複製された後に復元操作が完了します[＃43828](https://github.com/pingcap/tidb/issues/43828) [＃46302](https://github.com/pingcap/tidb/issues/46302) @ [3pointer](https://github.com/3pointer)

    -   TiCDC

        -   複数の TiCDC 監視メトリックとアラームルールを最適化します [＃9047](https://github.com/pingcap/tiflow/issues/9047) @ [asddongmen](https://github.com/asddongmen)
        -   Kafka Sink は、メッセージが大きすぎる場合に[ハンドルキーデータのみを送信する](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)サポートし、過剰なメッセージ サイズによって引き起こされる変更フィードの失敗を回避します。 [＃9680](https://github.com/pingcap/tiflow/issues/9680) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   `ADD INDEX` DDL操作を複製する実行ロジックを最適化して、後続のDMLステートメントをブロックしないようにします。 [＃9644](https://github.com/pingcap/tiflow/issues/9644) @ [sdojjy](https://github.com/sdojjy)
        -   TiCDC が失敗後に再試行するときのステータス メッセージを改善する[＃9483](https://github.com/pingcap/tiflow/issues/9483) @ [asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   互換性のない DDL ステートメントに対して厳密な楽観的モードをサポートする [＃9112](https://github.com/pingcap/tiflow/issues/9112) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   インポートタスクのパフォーマンスを向上させるために、デフォルト値の`checksum-via-sql`を`false`に変更します[＃45368](https://github.com/pingcap/tidb/issues/45368) [＃45094](https://github.com/pingcap/tidb/issues/45094) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   データインポートフェーズ中の`no leader`エラーに対するTiDB Lightningの再試行ロジックを最適化します。 [＃46253](https://github.com/pingcap/tidb/issues/46253) @ [lance6716](https://github.com/lance6716)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `GROUP_CONCAT` `ORDER BY`列を解析できない問題を修正 [＃41986](https://github.com/pingcap/tidb/issues/41986) @ [AilinKid](https://github.com/AilinKid)
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正しました[＃45531](https://github.com/pingcap/tidb/issues/45531) @ [Defined2014](https://github.com/Defined2014)
    -   メタデータの読み取りに 1 つの DDL リースよりも長い時間がかかる場合に TiDB のアップグレードが停止する問題を修正しました [＃45176](https://github.com/pingcap/tidb/issues/45176) @ [zimulala](https://github.com/zimulala)
    -   CTE を含む DML 文を実行するとpanicが発生する問題を修正しました [＃46083](https://github.com/pingcap/tidb/issues/46083) @ [winoros](https://github.com/winoros)
    -   パーティション交換中にパーティション定義に準拠していないデータを検出できない問題を修正 [＃46492](https://github.com/pingcap/tidb/issues/46492) @ [mjonss](https://github.com/mjonss)
    -   `MERGE_JOIN`の結果が間違っている問題を修正[＃46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)
    -   符号なし型と`Duration`型定数を比較したときに発生する誤った結果を修正しました [＃45410](https://github.com/pingcap/tidb/issues/45410) @ [wshwsh12](https://github.com/wshwsh12)
    -   `AUTO_ID_CACHE=1` に設定されている場合に`Duplicate entry`発生する可能性がある問題を修正しました [＃46444](https://github.com/pingcap/tidb/issues/46444) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   TTLが実行されているときのメモリリークの問題を修正しました [＃45510](https://github.com/pingcap/tidb/issues/45510) @ [lcwangchao](https://github.com/lcwangchao)
    -   接続を切断すると go コルーチン リークが発生する可能性がある問題を修正[＃46034](https://github.com/pingcap/tidb/issues/46034) @ [pingyu](https://github.com/pingyu)
    -   インデックス結合のエラーによりクエリが停止する可能性がある問題を修正[＃45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   ハッシュパーティションテーブルに対して`BatchPointGet`演算子が誤った結果を返す問題を修正しました [＃46779](https://github.com/pingcap/tidb/issues/46779) @ [jiyfhust](https://github.com/jiyfhust)
    -   `EXCHANGE PARTITION`失敗またはキャンセルされた場合に、パーティションテーブルの制限が元のテーブルに残る問題を修正[＃45920](https://github.com/pingcap/tidb/issues/45920) [＃45791](https://github.com/pingcap/tidb/issues/45791) @ [mjonss](https://github.com/mjonss)
    -   2つのサブクエリを結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正しました [＃46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)
    -   `DATETIME`または`TIMESTAMP`列を数値定数と比較するときに、MySQL と動作が一致しない問題を修正しました。 [＃38361](https://github.com/pingcap/tidb/issues/38361) @ [yibin87](https://github.com/yibin87)
    -   深くネストされた式に対してハッシュコードが繰り返し計算され、メモリ使用量が増加し、OOM が発生する問題を修正しました。 [＃42788](https://github.com/pingcap/tidb/issues/42788) @ [AilinKid](https://github.com/AilinKid)
    -   アクセスパスプルーニングロジックが`READ_FROM_STORAGE(TIFLASH[...])`ヒントを無視し、 `Can't find a proper physical plan`エラーが発生する問題を修正しました。 [＃40146](https://github.com/pingcap/tidb/issues/40146) @ [AilinKid](https://github.com/AilinKid)
    -   CAST に精度損失がないのに条件`cast(col)=range`で FullScan が発生する問題を修正[＃45199](https://github.com/pingcap/tidb/issues/45199) @ [AilinKid](https://github.com/AilinKid)
    -   `plan replayer dump explain`エラーを報告する問題を修正 [＃46197](https://github.com/pingcap/tidb/issues/46197) @ [time-and-fate](https://github.com/time-and-fate)
    -   `tmp-storage-quota`設定が で有効にならない問題を修正 [＃26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12) [＃45161](https://github.com/pingcap/tidb/issues/45161)
    -   TiDBパーサーが状態のままになり、解析エラーが発生する問題を修正[＃45898](https://github.com/pingcap/tidb/issues/45898) @ [qw4990](https://github.com/qw4990)
    -   MPP実行プランで集計がユニオンを介してプッシュダウンされると、結果が正しくなくなる問題を修正[＃45850](https://github.com/pingcap/tidb/issues/45850) @ [AilinKid](https://github.com/AilinKid)
    -   `AUTO_ID_CACHE=1` に設定されている場合に、panic後に TiDB がゆっくりと回復する問題を修正しました。 [＃46454](https://github.com/pingcap/tidb/issues/46454) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   ソート演算子がスピルプロセス中に TiDB をクラッシュさせる可能性がある問題を修正[＃47538](https://github.com/pingcap/tidb/issues/47538) @ [windtalker](https://github.com/windtalker)
    -   BRを使用して`AUTO_ID_CACHE=1` の非クラスター化インデックステーブルを復元するときに重複する主キーの問題を修正しました。 [＃46093](https://github.com/pingcap/tidb/issues/46093) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   静的プルーニングモードでパーティションテーブルをクエリし、実行プランに`IndexLookUp` が含まれている場合にクエリがエラーを報告する可能性がある問題を修正しました。 [＃45757](https://github.com/pingcap/tidb/issues/45757) @ [Defined2014](https://github.com/Defined2014)
    -   パーティションテーブルと配置ポリシーテーブル間でパーティションを交換した後に、パーティションテーブルへのデータの挿入が失敗する可能性がある問題を修正しました。 [＃45791](https://github.com/pingcap/tidb/issues/45791) @ [mjonss](https://github.com/mjonss)
    -   タイムゾーン情報が正しくない時間フィールドをエンコードする問題を修正[＃46033](https://github.com/pingcap/tidb/issues/46033) @ [tangenta](https://github.com/tangenta)
    -   `tmp`ディレクトリが存在しない場合にインデックスを高速に追加する DDL 文がスタックする問題を修正しました[＃45456](https://github.com/pingcap/tidb/issues/45456) @ [tangenta](https://github.com/tangenta)
    -   複数の TiDB インスタンスを同時にアップグレードするとアップグレードプロセスがブロックされる可能性がある問題を修正[＃46228](https://github.com/pingcap/tidb/issues/46228) @ [zimulala](https://github.com/zimulala)
    -   領域を分割する際に誤ったパラメータが使用されることで発生する、リージョンが不均一に分散される問題を修正しました。 [＃46135](https://github.com/pingcap/tidb/issues/46135) @ [zimulala](https://github.com/zimulala)
    -   TiDB の再起動後に DDL 操作が停止する可能性がある問題を修正[＃46751](https://github.com/pingcap/tidb/issues/46751) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   非整数クラスター化インデックスでのテーブル分割操作を禁止する [＃47350](https://github.com/pingcap/tidb/issues/47350) @ [tangenta](https://github.com/tangenta)
    -   不正なMDL処理によりDDL操作が永続的にブロックされる可能性がある問題を修正 [＃46920](https://github.com/pingcap/tidb/issues/46920) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   テーブルの名前変更によって発生する`information_schema.columns`の重複行の問題を修正 [＃47064](https://github.com/pingcap/tidb/issues/47064) @ [jiyfhust](https://github.com/jiyfhust)
    -   `batch-client` in `client-go` のpanic問題を修正 [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [crazycs520](https://github.com/crazycs520)
    -   パーティション化されたテーブルの統計収集が、メモリ使用量がメモリ制限を超えたときに時間内に強制終了されない問題を修正しました。 [＃45706](https://github.com/pingcap/tidb/issues/45706) @ [hawkingrei](https://github.com/hawkingrei)
    -   クエリに`UNHEX`条件が含まれている場合にクエリ結果が不正確になる問題を修正しました [＃45378](https://github.com/pingcap/tidb/issues/45378) @ [qw4990](https://github.com/qw4990)
    -   TiDBが`GROUP_CONCAT` のクエリに対して`Can't find column`返す問題を修正 [＃41957](https://github.com/pingcap/tidb/issues/41957) @ [AilinKid](https://github.com/AilinKid)

-   TiKV

    -   `ttl-check-poll-interval`設定項目がRawKV API V2 で有効にならない問題を修正 [＃15142](https://github.com/tikv/tikv/issues/15142) @ [pingyu](https://github.com/pingyu)
    -   raftstore-applys が継続的に増加するデータエラーを修正しました [＃15371](https://github.com/tikv/tikv/issues/15371) @ [Connor1996](https://github.com/Connor1996)
    -   データレプリケーション自動同期モードで同期回復フェーズでQPSがゼロに低下する問題を修正しました。 [＃14975](https://github.com/tikv/tikv/issues/14975) @ [nolouch](https://github.com/nolouch)
    -   1つのTiKVノードが分離され、別のノードが再起動されたときに発生する可能性のあるデータの不整合の問題を修正しました[＃15035](https://github.com/tikv/tikv/issues/15035) @ [overvenus](https://github.com/overvenus)
    -   オンラインアンセーフリカバリがマージ中止を処理できない問題を修正 [＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)
    -   PDとTiKV間のネットワーク中断によりPITRが停止する可能性がある問題を修正しました [＃15279](https://github.com/tikv/tikv/issues/15279) @ [YuJuncen](https://github.com/YuJuncen)
    -   `FLASHBACK` を実行した後にリージョンマージがブロックされる可能性がある問題を修正しました [＃15258](https://github.com/tikv/tikv/issues/15258) @ [overvenus](https://github.com/overvenus)
    -   ストアハートビートの再試行回数をに減らして、ハートビートストームの問題を修正しました。 [＃15184](https://github.com/tikv/tikv/issues/15184) @ [nolouch](https://github.com/nolouch)
    -   オンラインアンセーフリカバリがタイムアウトで中止されない問題を修正 [＃15346](https://github.com/tikv/tikv/issues/15346) @ [Connor1996](https://github.com/Connor1996)
    -   暗号化により部分書き込み中にデータ破損が発生する可能性がある問題を修正 [＃15080](https://github.com/tikv/tikv/issues/15080) @ [tabokie](https://github.com/tabokie)
    -   リージョンのメタデータが正しくないことによって引き起こされるTiKV panic問題を修正しました [＃13311](https://github.com/tikv/tikv/issues/13311) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   オンラインワークロードがある場合にTiDB Lightningチェックサムコプロセッサの要求がタイムアウトする問題を修正しました [＃15565](https://github.com/tikv/tikv/issues/15565) @ [lance6716](https://github.com/lance6716)
    -   ピアを移動するとFollower Readのパフォーマンスが低下する可能性がある問題を修正[＃15468](https://github.com/tikv/tikv/issues/15468) @ [YuJuncen](https://github.com/YuJuncen)

-   PD

    -   v2 スケジューラ アルゴリズムでホット リージョンがスケジュールされない可能性がある問題を修正しました [＃6645](https://github.com/tikv/pd/issues/6645) @ [lhy1024](https://github.com/lhy1024)
    -   TLSハンドシェイクにより空のクラスタでCPU使用率が上昇する可能性がある問題を修正 [＃6913](https://github.com/tikv/pd/issues/6913) @ [nolouch](https://github.com/nolouch)
    -   PDノード間の注入エラーによりPD panicが発生する可能性がある問題を修正しました [＃6858](https://github.com/tikv/pd/issues/6858) @ [HuSharp](https://github.com/HuSharp)
    -   ストア情報の同期によりPDリーダーが終了し、 で停止する可能性がある問題を修正しました。 [＃6918](https://github.com/tikv/pd/issues/6918) @ [rleungx](https://github.com/rleungx)
    -   フラッシュバック後にリージョン情報が更新されない問題を修正 [＃6912](https://github.com/tikv/pd/issues/6912) @ [overvenus](https://github.com/overvenus)
    -   終了時に PD がpanicになる可能性がある問題を修正しました [＃7053](https://github.com/tikv/pd/issues/7053) @ [HuSharp](https://github.com/HuSharp)
    -   コンテキストタイムアウトにより`lease timeout`エラーが発生する可能性がある問題を修正 [＃6926](https://github.com/tikv/pd/issues/6926) @ [rleungx](https://github.com/rleungx)
    -   ピアがグループごとに適切に分散されず、リーダーの分布が不均等になる可能性がある問題を修正しました。 [＃6962](https://github.com/tikv/pd/issues/6962) @ [rleungx](https://github.com/rleungx)
    -   pd-ctl を使用して更新するときに分離レベル ラベルが同期されない問題を修正しました [＃7121](https://github.com/tikv/pd/issues/7121) @ [rleungx](https://github.com/rleungx)
    -   `evict-leader-scheduler`が構成を失う可能性がある問題を修正 [＃6897](https://github.com/tikv/pd/issues/6897) @[HuSharp](https://github.com/HuSharp)
    -   プラグインディレクトリとファイルの潜在的なセキュリティリスクを修正[＃7094](https://github.com/tikv/pd/issues/7094) @ [HuSharp](https://github.com/HuSharp)
    -   リソース制御を有効にした後に DDL がアトミック性を保証しない可能性がある問題を修正しました [＃45050](https://github.com/pingcap/tidb/issues/45050) @ [glorv](https://github.com/glorv)
    -   ルールチェッカーがピアを選択した場合に、不健全なピアを削除できない問題を修正しました [＃6559](https://github.com/tikv/pd/issues/6559) @ [nolouch](https://github.com/nolouch)
    -   etcd がすでに起動しているがクライアントがまだ接続していない場合、クライアントを呼び出すと PD がpanicになる可能性がある問題を修正しました。 [＃6860](https://github.com/tikv/pd/issues/6860) @ [HuSharp](https://github.com/HuSharp)
    -   RU消費量が0未満の場合にPDがクラッシュする問題を修正 [＃6973](https://github.com/tikv/pd/issues/6973) @ [CabinfeverB](https://github.com/CabinfeverB)
    -   クラスタが大きい場合、クライアントが定期的に更新される`min-resolved-ts` PD OOMを引き起こす可能性がある問題を修正しました[＃46664](https://github.com/pingcap/tidb/issues/46664) @ [HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   MemoryTracker によって報告されるメモリ使用量が不正確であるという問題を修正[＃8128](https://github.com/pingcap/tiflash/issues/8128) @ [JinheLin](https://github.com/JinheLin)
    -   領域の無効な範囲キーによりTiFlashデータが不整合になる問題を修正しました [＃7762](https://github.com/pingcap/tiflash/issues/7762) @ [lidezhu](https://github.com/lidezhu)
    -   `fsp` `DATETIME` 、 `TIMESTAMP` 、または`TIME`データ型に変更した後にクエリが失敗する問題を修正しました [＃7809](https://github.com/pingcap/tiflash/issues/7809) @ [JaySon-Huang](https://github.com/JaySon-Huang)
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに重大な影響を与える可能性がある問題を修正しました[＃7810](https://github.com/pingcap/tiflash/issues/7810) @ [SeaRise](https://github.com/SeaRise)

-   ツール

    -   Backup & Restore (BR)

        -   PITR を使用して暗黙の主キーを回復すると競合が発生する可能性がある問題を修正[＃46520](https://github.com/pingcap/tidb/issues/46520) @ [3pointer](https://github.com/3pointer)
        -   PITRがGCS からデータを回復できない問題を修正 [＃47022](https://github.com/pingcap/tidb/issues/47022) @ [Leavrth](https://github.com/Leavrth)
        -   RawKVモードのきめ細かなバックアップフェーズで発生する可能性のあるエラーを修正 [＃37085](https://github.com/pingcap/tidb/issues/37085) @ [pingyu](https://github.com/pingyu)
        -   PITRを使用してメタkvを回復するとエラーが発生する可能性がある問題を修正しました [＃46578](https://github.com/pingcap/tidb/issues/46578) @ [Leavrth](https://github.com/Leavrth)
        -   BR統合テストケースのエラーを修正 [＃46561](https://github.com/pingcap/tidb/issues/46561) @ [purelind](https://github.com/purelind)
        -   BRで使用されるグローバルパラメータ`TableColumnCountLimit`と`IndexLimit`デフォルト値を最大値に増やすことで、復元が失敗する問題を修正しました。 [＃45793](https://github.com/pingcap/tidb/issues/45793) @ [Leavrth](https://github.com/Leavrth)
        -   復元されたデータをスキャンするときに br CLI クライアントが停止する問題を修正しました [＃45476](https://github.com/pingcap/tidb/issues/45476) @ [3pointer](https://github.com/3pointer)
        -   PITRが`CREATE INDEX` DDL文の復元をスキップする可能性がある問題を修正しました [＃47482](https://github.com/pingcap/tidb/issues/47482) @ [Leavrth](https://github.com/Leavrth)
        -   1分以内にPITRを複数回実行するとデータ損失が発生する可能性がある問題を修正[＃15483](https://github.com/tikv/tikv/issues/15483) @ [YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   異常な状態のレプリケーションタスクが上流のGC をブロックする問題を修正しました [＃9543](https://github.com/pingcap/tiflow/issues/9543) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   オブジェクトストレージにデータを複製するとデータの不整合が発生する可能性がある問題を修正[＃9592](https://github.com/pingcap/tiflow/issues/9592) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `redo-resolved-ts`有効にすると、changefeed が失敗する可能性がある問題を修正[＃9769](https://github.com/pingcap/tiflow/issues/9769) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   間違ったメモリ情報を取得すると、一部のオペレーティングシステムで OOM 問題が発生する可能性がある問題を修正[＃9762](https://github.com/pingcap/tiflow/issues/9762) @ [sdojjy](https://github.com/sdojjy)
        -   `scale-out`が有効になっている場合のノード間の書き込みキーの不均等な配布の問題を修正[＃9665](https://github.com/pingcap/tiflow/issues/9665) @ [sdojjy](https://github.com/sdojjy)
        -   ログに機密ユーザー情報が記録される問題を修正 [＃9690](https://github.com/pingcap/tiflow/issues/9690) @ [sdojjy](https://github.com/sdojjy)
        -   TiCDC が誤って名前変更 DDL 操作を同期する可能性がある問題を修正[＃9488](https://github.com/pingcap/tiflow/issues/9488) [＃9378](https://github.com/pingcap/tiflow/issues/9378) [＃9531](https://github.com/pingcap/tiflow/issues/9531) @ [asddongmen](https://github.com/asddongmen)
        -   すべての変更フィードが削除された後に上流の TiDB GC がブロックされる問題を修正[＃9633](https://github.com/pingcap/tiflow/issues/9633) @ [sdojjy](https://github.com/sdojjy)
        -   一部のコーナーケースで TiCDC レプリケーションタスクが失敗する可能性がある問題を修正[＃9685](https://github.com/pingcap/tiflow/issues/9685) [＃9697](https://github.com/pingcap/tiflow/issues/9697) [＃9695](https://github.com/pingcap/tiflow/issues/9695) [＃9736](https://github.com/pingcap/tiflow/issues/9736) @ [hicqu](https://github.com/hicqu) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   PDノードのネットワーク分離によって発生するTiCDCレプリケーションのレイテンシーが大きくなる問題を修正 [＃9565](https://github.com/pingcap/tiflow/issues/9565) @ [asddongmen](https://github.com/asddongmen)
        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正[＃9584](https://github.com/pingcap/tiflow/issues/9584) @ [fubinzh](https://github.com/fubinzh) @ [asddongmen](https://github.com/asddongmen)
        -   上流にリージョンが多数ある場合、TiCDC が TiKV ノード障害から迅速に回復できない問題を修正しました。 [＃9741](https://github.com/pingcap/tiflow/issues/9741) @ [sdojjy](https://github.com/sdojjy)
        -   CSV形式を使用するとTiCDCが誤って`UPDATE`演算を`INSERT`に変更する問題を修正 [＃9658](https://github.com/pingcap/tiflow/issues/9658) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   アップストリームで同じDDL文で複数のテーブルの名前を変更するとレプリケーションエラーが発生する問題を修正 [＃9488](https://github.com/pingcap/tiflow/issues/9488) @ [CharlesCheung96](https://github.com/CharlesCheung96) [＃9476](https://github.com/pingcap/tiflow/issues/9476) @ [asddongmen](https://github.com/asddongmen)
        -   Kafka に同期するときに再試行間隔が短いためにレプリケーションタスクが失敗する問題を修正しました [＃9504](https://github.com/pingcap/tiflow/issues/9504) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   アップストリームで 1 つのトランザクションで複数の行の一意のキーが変更されると、レプリケーション書き込み競合が発生する可能性がある問題を修正しました。 [＃9430](https://github.com/pingcap/tiflow/issues/9430) @ [sdojjy](https://github.com/sdojjy)
        -   ダウンストリームで短期的な障害が発生したときにレプリケーションタスクが停止する可能性がある問題を修正[＃9542](https://github.com/pingcap/tiflow/issues/9542) [＃9272](https://github.com/pingcap/tiflow/issues/9272) [＃9582](https://github.com/pingcap/tiflow/issues/9582) [＃9592](https://github.com/pingcap/tiflow/issues/9592) @ [hicqu](https://github.com/hicqu)
        -   ダウンストリームでエラーが発生し、 で再試行すると、レプリケーションタスクが停止する可能性がある問題を修正しました。 [＃9450](https://github.com/pingcap/tiflow/issues/9450) @ [hicqu](https://github.com/hicqu)
        -   Kafka にデータを複製するときに TiCDC が停止する可能性がある問題を修正しました [＃9855](https://github.com/pingcap/tiflow/issues/9855) @ [hicqu](https://github.com/hicqu)

    -   TiDB Data Migration (DM)

        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合に、DM によって返されるレプリケーション ラグが増大し続ける問題を修正しました[＃9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3Hunter](https://github.com/D3Hunter)
        -   DM が大文字と小文字を区別しない照合で競合を正しく処理できない問題を修正しました [＃9489](https://github.com/pingcap/tiflow/issues/9489) @ [hihihuhu](https://github.com/hihihuhu)
        -   DM バリデーターのデッドロック問題を修正し、再試行をに強化しました。 [＃9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3Hunter](https://github.com/D3Hunter)
        -   楽観的モードでタスクを再開するときに DM がすべての DML をスキップする問題を修正しました [＃9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   オンライン DDL をスキップするときに DM が上流のテーブル スキーマを適切に追跡できない問題を修正しました [＃9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   DMが楽観的モードでパーティションDDLをスキップする問題を修正 [＃9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   `AUTO_ID_CACHE=1`を含むテーブルをインポートするときに、間違った`row_id`がに割り当てられる問題を修正しました [＃46100](https://github.com/pingcap/tidb/issues/46100) @ [D3Hunter](https://github.com/D3Hunter)
        -   `NEXT_GLOBAL_ROW_ID` を保存するときにデータ型が間違っている問題を修正しました [＃45427](https://github.com/pingcap/tidb/issues/45427) @ [lyzx2001](https://github.com/lyzx2001)
        -   `checksum = "optional"` のときにチェックサムがエラーを報告する問題を修正しました [＃45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)
        -   PDクラスタアドレスがに変更されるとデータのインポートが失敗する問題を修正しました [＃43436](https://github.com/pingcap/tidb/issues/43436) @ [lichunzhu](https://github.com/lichunzhu)
        -   PDトポロジが変更されるとTiDB Lightningが起動に失敗する問題を修正[＃46688](https://github.com/pingcap/tidb/issues/46688) @ [lance6716](https://github.com/lance6716)
        -   CSVデータをインポートする際にルートがpanicになる可能性がある問題を修正 [＃43284](https://github.com/pingcap/tidb/issues/43284) @ [lyzx2001](https://github.com/lyzx2001)

    -   TiDB Binlog

        -   1 GB を超えるトランザクションを転送するときにDrainer が終了する問題を修正しました [＃28659](https://github.com/pingcap/tidb/issues/28659) @ [jackysp](https://github.com/jackysp)
