---
title: TiDB 7.1.2 Release Notes
summary: TiDB 7.1.2 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.1.2 リリースノート {#tidb-7-1-2-release-notes}

発売日：2023年10月25日

TiDB バージョン: 7.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   Security強化モード（SEM）で設定[`require_secure_transport`](https://docs.pingcap.com/tidb/v7.1/system-variables#require_secure_transport-new-in-v610) ～ `ON`を禁止し、ユーザー[＃47665](https://github.com/pingcap/tidb/issues/47665) @ [天菜まお](https://github.com/tiancaiamao)の潜在的な接続問題を防ぎます。
-   [スムーズなアップグレード](/smooth-upgrade-tidb.md)機能はデフォルトで無効になっています。有効にするには、 `/upgrade/start`と`upgrade/finish` HTTPリクエストを[＃47172](https://github.com/pingcap/tidb/issues/47172) @ [ジムララ](https://github.com/zimulala)に送信します。
-   オプティマイザがテーブル[＃46695](https://github.com/pingcap/tidb/issues/46695) @ [コーダープレイ](https://github.com/coderplay)に対してハッシュ結合を選択するかどうかを制御する[`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_opt_enable_hash_join-new-in-v712)システム変数を導入します。
-   RocksDBの定期的な圧縮をデフォルトで無効にすることで、TiKV RocksDBのデフォルトの動作がv6.5.0より前のバージョンと一致するようになりました。この変更により、アップグレード後に大量の圧縮が行われることによるパフォーマンスへの影響を回避できます。さらに、TiKVでは2つの新しい設定項目[`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#periodic-compaction-seconds-new-in-v712)と[`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#ttl-new-in-v712)導入され、RocksDB [＃15355](https://github.com/tikv/tikv/issues/15355) @ [LykxSassinator](https://github.com/LykxSassinator)の定期的な圧縮を手動で設定できるようになりました。
-   TiCDCは、CSVプロトコルにおけるバイナリデータのエンコード方式を制御するための設定項目[`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)導入しました。デフォルト値は`'base64'` [＃9373](https://github.com/pingcap/tiflow/issues/9373) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)です。
-   TiCDC では、設定項目[`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)導入されています。デフォルトでは空で、メッセージサイズが Kafka トピックの制限を超えると changefeed が失敗します。この設定を`"handle-key-only"`に設定すると、メッセージがサイズ制限を超えた場合、メッセージサイズを縮小するためにハンドルキーのみが送信されます。縮小されたメッセージでも制限を超える場合、changefeed は[＃9680](https://github.com/pingcap/tiflow/issues/9680) @ [3エースショーハンド](https://github.com/3AceShowHand)で失敗します。

### 行動の変化 {#behavior-changes}

-   複数の変更を含むトランザクションにおいて、更新イベントで主キーまたはNULL以外の一意のインデックス値が変更された場合、TiCDCはイベントを削除イベントと挿入イベントに分割し、すべてのイベントが挿入イベントに先行する削除イベントの順序に従うようにします。詳細については、 [ドキュメント](/ticdc/ticdc-split-update-behavior.md#transactions-containing-multiple-update-changes)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-) @ [＃45520](https://github.com/pingcap/tidb/issues/45520) [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-)含む新しいオプティマイザヒント[`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-) [qw4990](https://github.com/qw4990)し[`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-)
    -   コプロセッサ[＃46514](https://github.com/pingcap/tidb/issues/46514) @ [あなた06](https://github.com/you06)に関連する要求元情報を追加します
    -   TiDBノード[＃47172](https://github.com/pingcap/tidb/issues/47172) @ [ジムララ](https://github.com/zimulala)のアップグレードステータスの開始と終了をマークするために`/upgrade/start`と`upgrade/finish` APIを追加します。

-   TiKV

    -   圧縮メカニズムを最適化します。リージョンが分割されるときに、分割するキーがない場合、圧縮がトリガーされ、過剰な MVCC バージョン[＃15282](https://github.com/tikv/tikv/issues/15282) @ [スペードA-タン](https://github.com/SpadeA-Tang)が排除されます。
    -   ルータオブジェクトのLRUCacheを排除してメモリ使用量を削減し、OOM [＃15430](https://github.com/tikv/tikv/issues/15430) @ [コナー1996](https://github.com/Connor1996)を防止します。
    -   `Max gap of safe-ts`と`Min safe ts region`メトリックを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、resolved-tsと安全な ts の状態をより適切に観察および診断します[＃15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)
    -   TiKV で RocksDB の設定を公開し、ユーザーが TTL や定期的な圧縮などの機能を無効にできるようにします[＃14873](https://github.com/tikv/tikv/issues/14873) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   接続再試行のプロセスでPDクライアントのバックオフメカニズムを追加し、エラー再試行中に再試行間隔を徐々に増やしてPD圧力[＃15428](https://github.com/tikv/tikv/issues/15428) @ [ノルーシュ](https://github.com/nolouch)を軽減します。
    -   Titan マニフェストファイルを書き込むときにミューテックスを保持しないようにして、他のスレッドに影響を与えないようにします[＃15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)
    -   OOM [＃15458](https://github.com/tikv/tikv/issues/15458) @ [金星の上](https://github.com/overvenus)を防ぐためにリゾルバのメモリ使用量を最適化します

-   PD

    -   PD 呼び出し元のバックオフ メカニズムを最適化して、呼び出しが失敗したときの RPC 要求の頻度を減らします[＃6556](https://github.com/tikv/pd/issues/6556) @ [ノルーシュ](https://github.com/nolouch) @ [rleungx](https://github.com/rleungx) @ [HuSharp](https://github.com/HuSharp)
    -   発信者が切断されたときにCPUとメモリを時間内に解放するために、 `GetRegions`インターフェースにキャンセルメカニズムを導入する[＃6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   Grafana [＃8050](https://github.com/pingcap/tiflash/issues/8050) @ [ホンユニャン](https://github.com/hongyunyan)のインデックスデータのメモリ使用量の監視メトリックを追加します

-   ツール

    -   バックアップと復元 (BR)

        -   HTTPクライアント[＃46011](https://github.com/pingcap/tidb/issues/46011) @ [リーヴルス](https://github.com/Leavrth)で`MaxIdleConns`と`MaxIdleConnsPerHost`パラメータを設定することにより、ログバックアップとPITRリストアタスクの接続再利用のサポートを強化します。
        -   ログバックアップのCPUオーバーヘッドを削減`resolve lock` [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [3ポイントシュート](https://github.com/3pointer)
        -   新しい復元パラメータ`WaitTiflashReady`を追加します。このパラメータを有効にすると、 TiFlashレプリカが正常に複製された後に復元操作が完了します[＃43828](https://github.com/pingcap/tidb/issues/43828) [＃46302](https://github.com/pingcap/tidb/issues/46302) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiCDC

        -   複数の TiCDC 監視メトリックとアラームルールを[＃9047](https://github.com/pingcap/tiflow/issues/9047) @ [アズドンメン](https://github.com/asddongmen)最適化します
        -   Kafka Sink は、メッセージが大きすぎる場合に[ハンドルキーデータのみを送信する](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)サポートし、過剰なメッセージ サイズ[＃9680](https://github.com/pingcap/tiflow/issues/9680) @ [3エースショーハンド](https://github.com/3AceShowHand)によって引き起こされる変更フィードの失敗を回避します。
        -   `ADD INDEX` DDL操作を複製する実行ロジックを最適化して、後続のDMLステートメント[＃9644](https://github.com/pingcap/tiflow/issues/9644) @ [スドジ](https://github.com/sdojjy)をブロックしないようにします。
        -   TiCDC が失敗後に再試行するときのステータス メッセージを改善する[＃9483](https://github.com/pingcap/tiflow/issues/9483) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   互換性のない DDL ステートメント[＃9112](https://github.com/pingcap/tiflow/issues/9112) @ [GMHDBJD](https://github.com/GMHDBJD)に対して厳密な楽観的モードをサポートする

    -   TiDB Lightning

        -   インポートタスクのパフォーマンスを向上させるために、デフォルト値の`checksum-via-sql`を`false`に変更します[＃45368](https://github.com/pingcap/tidb/issues/45368) [＃45094](https://github.com/pingcap/tidb/issues/45094) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   データインポートフェーズ[＃46253](https://github.com/pingcap/tidb/issues/46253) @ [ランス6716](https://github.com/lance6716)中の`no leader`エラーに対するTiDB Lightningの再試行ロジックを最適化します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `GROUP_CONCAT` `ORDER BY`列[＃41986](https://github.com/pingcap/tidb/issues/41986) @ [アイリンキッド](https://github.com/AilinKid)を解析できない問題を修正
    -   システムテーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正しました[＃45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   メタデータの読み取りに 1 つの DDL リース[＃45176](https://github.com/pingcap/tidb/issues/45176) @ [ジムララ](https://github.com/zimulala)よりも長い時間がかかる場合に TiDB のアップグレードが停止する問題を修正しました
    -   CTE を含む DML 文を実行するとpanic[＃46083](https://github.com/pingcap/tidb/issues/46083) @ [ウィノロス](https://github.com/winoros)が発生する問題を修正しました
    -   パーティション交換[＃46492](https://github.com/pingcap/tidb/issues/46492) @ [ミョンス](https://github.com/mjonss)中にパーティション定義に準拠していないデータを検出できない問題を修正
    -   `MERGE_JOIN`の結果が間違っている問題を修正[＃46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)
    -   符号なし型と`Duration`型定数[＃45410](https://github.com/pingcap/tidb/issues/45410) @ [wshwsh12](https://github.com/wshwsh12)を比較したときに発生する誤った結果を修正しました
    -   `AUTO_ID_CACHE=1` [＃46444](https://github.com/pingcap/tidb/issues/46444) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に`Duplicate entry`発生する可能性がある問題を修正しました
    -   TTLが[＃45510](https://github.com/pingcap/tidb/issues/45510) @ [lcwangchao](https://github.com/lcwangchao)で実行されているときのメモリリークの問題を修正しました
    -   接続を切断すると go コルーチン リークが発生する可能性がある問題を修正[＃46034](https://github.com/pingcap/tidb/issues/46034) @ [ピンギュ](https://github.com/pingyu)
    -   インデックス結合のエラーによりクエリが停止する可能性がある問題を修正[＃45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   ハッシュパーティションテーブル[＃46779](https://github.com/pingcap/tidb/issues/46779) @ [ジフハウス](https://github.com/jiyfhust)に対して`BatchPointGet`演算子が誤った結果を返す問題を修正しました
    -   `EXCHANGE PARTITION`失敗またはキャンセルされた場合に、パーティションテーブルの制限が元のテーブルに残る問題を修正[＃45920](https://github.com/pingcap/tidb/issues/45920) [＃45791](https://github.com/pingcap/tidb/issues/45791) @ [ミョンス](https://github.com/mjonss)
    -   2つのサブクエリ[＃46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)を結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正しました
    -   `DATETIME`または`TIMESTAMP`列を数値定数[＃38361](https://github.com/pingcap/tidb/issues/38361) @ [イービン87](https://github.com/yibin87)と比較するときに、MySQL と動作が一致しない問題を修正しました。
    -   深くネストされた式に対してハッシュコードが繰り返し計算され、メモリ使用量が増加し、OOM [＃42788](https://github.com/pingcap/tidb/issues/42788) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正しました。
    -   アクセスパスプルーニングロジックが`READ_FROM_STORAGE(TIFLASH[...])`ヒントを無視し、 `Can't find a proper physical plan`エラー[＃40146](https://github.com/pingcap/tidb/issues/40146) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正しました。
    -   CAST に精度損失がないのに条件`cast(col)=range`で FullScan が発生する問題を修正[＃45199](https://github.com/pingcap/tidb/issues/45199) @ [アイリンキッド](https://github.com/AilinKid)
    -   `plan replayer dump explain`エラー[＃46197](https://github.com/pingcap/tidb/issues/46197) @ [時間と運命](https://github.com/time-and-fate)を報告する問題を修正
    -   `tmp-storage-quota`設定が[＃45161](https://github.com/pingcap/tidb/issues/45161) [＃26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12)で有効にならない問題を修正
    -   TiDBパーサーが状態のままになり、解析エラーが発生する問題を修正[＃45898](https://github.com/pingcap/tidb/issues/45898) @ [qw4990](https://github.com/qw4990)
    -   MPP実行プランで集計がユニオンを介してプッシュダウンされると、結果が正しくなくなる問題を修正[＃45850](https://github.com/pingcap/tidb/issues/45850) @ [アイリンキッド](https://github.com/AilinKid)
    -   `AUTO_ID_CACHE=1` [＃46454](https://github.com/pingcap/tidb/issues/46454) @ [天菜まお](https://github.com/tiancaiamao)に設定されている場合に、panic後に TiDB がゆっくりと回復する問題を修正しました。
    -   ソート演算子がスピルプロセス中に TiDB をクラッシュさせる可能性がある問題を修正[＃47538](https://github.com/pingcap/tidb/issues/47538) @ [ウィンドトーカー](https://github.com/windtalker)
    -   BRを使用して`AUTO_ID_CACHE=1` [＃46093](https://github.com/pingcap/tidb/issues/46093) @ [天菜まお](https://github.com/tiancaiamao)の非クラスタ化インデックステーブルを復元するときに重複する主キーの問題を修正しました。
    -   静的プルーニングモードでパーティションテーブルをクエリし、実行プランに`IndexLookUp` [＃45757](https://github.com/pingcap/tidb/issues/45757) @ [定義2014](https://github.com/Defined2014)が含まれている場合にクエリがエラーを報告する可能性がある問題を修正しました。
    -   パーティションテーブルと配置ポリシー[＃45791](https://github.com/pingcap/tidb/issues/45791) @ [ミョンス](https://github.com/mjonss)テーブル間でパーティションを交換した後に、パーティションテーブルへのデータの挿入が失敗する可能性がある問題を修正しました。
    -   タイムゾーン情報が正しくない時間フィールドをエンコードする問題を修正[＃46033](https://github.com/pingcap/tidb/issues/46033) @ [接線](https://github.com/tangenta)
    -   `tmp`ディレクトリが存在しない場合にインデックスを高速に追加する DDL 文がスタックする問題を修正しました[＃45456](https://github.com/pingcap/tidb/issues/45456) @ [接線](https://github.com/tangenta)
    -   複数の TiDB インスタンスを同時にアップグレードするとアップグレードプロセスがブロックされる可能性がある問題を修正[＃46228](https://github.com/pingcap/tidb/issues/46228) @ [ジムララ](https://github.com/zimulala)
    -   領域[＃46135](https://github.com/pingcap/tidb/issues/46135) @ [ジムララ](https://github.com/zimulala)を分割する際に誤ったパラメータが使用されることで発生する、リージョンが不均一に分散される問題を修正しました。
    -   TiDB の再起動後に DDL 操作が停止する可能性がある問題を修正[＃46751](https://github.com/pingcap/tidb/issues/46751) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   非整数クラスター化インデックス[＃47350](https://github.com/pingcap/tidb/issues/47350) @ [接線](https://github.com/tangenta)でのテーブル分割操作を禁止する
    -   不正なMDL処理[＃46920](https://github.com/pingcap/tidb/issues/46920) @ [wjhuang2016](https://github.com/wjhuang2016)によりDDL操作が永続的にブロックされる可能性がある問題を修正
    -   テーブル[＃47064](https://github.com/pingcap/tidb/issues/47064) @ [ジフハウス](https://github.com/jiyfhust)の名前変更によって発生する`information_schema.columns`の重複行の問題を修正
    -   `batch-client` in `client-go` [＃47691](https://github.com/pingcap/tidb/issues/47691) @ [crazycs520](https://github.com/crazycs520)のpanic問題を修正
    -   パーティション化されたテーブルの統計収集が、メモリ使用量がメモリ制限[＃45706](https://github.com/pingcap/tidb/issues/45706) @ [ホーキングレイ](https://github.com/hawkingrei)を超えたときに時間内に強制終了されない問題を修正しました。
    -   クエリに`UNHEX`条件[＃45378](https://github.com/pingcap/tidb/issues/45378) @ [qw4990](https://github.com/qw4990)が含まれている場合にクエリ結果が不正確になる問題を修正しました
    -   TiDBが`GROUP_CONCAT` [＃41957](https://github.com/pingcap/tidb/issues/41957) @ [アイリンキッド](https://github.com/AilinKid)のクエリに対して`Can't find column`返す問題を修正

-   TiKV

    -   `ttl-check-poll-interval`設定項目がRawKV API V2 [＃15142](https://github.com/tikv/tikv/issues/15142) @ [ピンギュ](https://github.com/pingyu)で有効にならない問題を修正
    -   raftstore-applys [＃15371](https://github.com/tikv/tikv/issues/15371) @ [コナー1996](https://github.com/Connor1996)が継続的に増加するデータエラーを修正しました
    -   データレプリケーション自動同期モード[＃14975](https://github.com/tikv/tikv/issues/14975) @ [ノルーシュ](https://github.com/nolouch)で同期回復フェーズでQPSがゼロに低下する問題を修正しました。
    -   1つのTiKVノードが分離され、別のノードが再起動されたときに発生する可能性のあるデータの不整合の問題を修正しました[＃15035](https://github.com/tikv/tikv/issues/15035) @ [金星の上](https://github.com/overvenus)
    -   オンラインアンセーフリカバリがマージ中止[＃15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)を処理できない問題を修正
    -   PDとTiKV間のネットワーク中断によりPITRが[＃15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)で停止する可能性がある問題を修正しました
    -   `FLASHBACK` [＃15258](https://github.com/tikv/tikv/issues/15258) @ [金星の上](https://github.com/overvenus)を実行した後にリージョンマージがブロックされる可能性がある問題を修正しました
    -   ストアハートビートの再試行回数を[＃15184](https://github.com/tikv/tikv/issues/15184) @ [ノルーシュ](https://github.com/nolouch)に減らして、ハートビートストームの問題を修正しました。
    -   オンラインアンセーフリカバリがタイムアウト[＃15346](https://github.com/tikv/tikv/issues/15346) @ [コナー1996](https://github.com/Connor1996)で中止されない問題を修正
    -   暗号化により部分書き込み[＃15080](https://github.com/tikv/tikv/issues/15080) @ [タボキ](https://github.com/tabokie)中にデータ破損が発生する可能性がある問題を修正
    -   リージョン[＃13311](https://github.com/tikv/tikv/issues/13311) @ [cfzjywxk](https://github.com/cfzjywxk)のメタデータが正しくないことによって引き起こされるTiKVpanic問題を修正しました
    -   オンラインワークロード[＃15565](https://github.com/tikv/tikv/issues/15565) @ [ランス6716](https://github.com/lance6716)がある場合にTiDB Lightningチェックサムコプロセッサの要求がタイムアウトする問題を修正しました
    -   ピアを移動するとFollower Readのパフォーマンスが低下する可能性がある問題を修正[＃15468](https://github.com/tikv/tikv/issues/15468) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   v2 スケジューラ アルゴリズム[＃6645](https://github.com/tikv/pd/issues/6645) @ [lhy1024](https://github.com/lhy1024)でホット リージョンがスケジュールされない可能性がある問題を修正しました
    -   TLSハンドシェイクにより空のクラスタ[＃6913](https://github.com/tikv/pd/issues/6913) @ [ノルーシュ](https://github.com/nolouch)でCPU使用率が上昇する可能性がある問題を修正
    -   PDノード間の注入エラーによりPDpanic[＃6858](https://github.com/tikv/pd/issues/6858) @ [HuSharp](https://github.com/HuSharp)が発生する可能性がある問題を修正しました
    -   ストア情報の同期によりPDリーダーが終了し、 [＃6918](https://github.com/tikv/pd/issues/6918) @ [rleungx](https://github.com/rleungx)で停止する可能性がある問題を修正しました。
    -   フラッシュバック[＃6912](https://github.com/tikv/pd/issues/6912) @ [金星の上](https://github.com/overvenus)後にリージョン情報が更新されない問題を修正
    -   [＃7053](https://github.com/tikv/pd/issues/7053) @ [HuSharp](https://github.com/HuSharp)終了時に PD がpanicになる可能性がある問題を修正しました
    -   コンテキストタイムアウトにより`lease timeout`エラー[＃6926](https://github.com/tikv/pd/issues/6926) @ [rleungx](https://github.com/rleungx)が発生する可能性がある問題を修正
    -   ピアがグループごとに適切に分散されず、リーダー[＃6962](https://github.com/tikv/pd/issues/6962) @ [rleungx](https://github.com/rleungx)の分布が不均等になる可能性がある問題を修正しました。
    -   pd-ctl [＃7121](https://github.com/tikv/pd/issues/7121) @ [rleungx](https://github.com/rleungx)を使用して更新するときに分離レベル ラベルが同期されない問題を修正しました
    -   `evict-leader-scheduler` [HuSharp](https://github.com/HuSharp)で構成[＃6897](https://github.com/tikv/pd/issues/6897)失う可能性がある問題を修正
    -   プラグインディレクトリとファイルの潜在的なセキュリティリスクを修正[＃7094](https://github.com/tikv/pd/issues/7094) @ [HuSharp](https://github.com/HuSharp)
    -   リソース制御[＃45050](https://github.com/pingcap/tidb/issues/45050) @ [栄光](https://github.com/glorv)を有効にした後に DDL がアトミック性を保証しない可能性がある問題を修正しました
    -   ルールチェッカーがピア[＃6559](https://github.com/tikv/pd/issues/6559) @ [ノルーシュ](https://github.com/nolouch)を選択した場合に、不健全なピアを削除できない問題を修正しました
    -   etcd がすでに起動しているがクライアントがまだ接続していない場合、クライアントを呼び出すと PD がpanic[＃6860](https://github.com/tikv/pd/issues/6860) @ [HuSharp](https://github.com/HuSharp)になる可能性がある問題を修正しました。
    -   RU消費量が0未満の場合にPDが[＃6973](https://github.com/tikv/pd/issues/6973) @ [キャビンフィーバーB](https://github.com/CabinfeverB)でクラッシュする問題を修正
    -   クラスタが大きい場合、クライアントが定期的に更新される`min-resolved-ts` PD OOMを引き起こす可能性がある問題を修正しました[＃46664](https://github.com/pingcap/tidb/issues/46664) @ [HuSharp](https://github.com/HuSharp)

-   TiFlash

    -   MemoryTracker によって報告されるメモリ使用量が不正確であるという問題を修正[＃8128](https://github.com/pingcap/tiflash/issues/8128) @ [ジンヘリン](https://github.com/JinheLin)
    -   領域[＃7762](https://github.com/pingcap/tiflash/issues/7762) @ [リデジュ](https://github.com/lidezhu)の無効な範囲キーによりTiFlashデータが不整合になる問題を修正しました
    -   `fsp` `DATETIME` 、 `TIMESTAMP` 、または`TIME`データ型[＃7809](https://github.com/pingcap/tiflash/issues/7809) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に変更した後にクエリが失敗する問題を修正しました
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに非常に長い時間がかかり、クエリのパフォーマンスに重大な影響を与える可能性がある問題を修正しました[＃7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)

-   ツール

    -   バックアップと復元 (BR)

        -   PITR を使用して暗黙の主キーを回復すると競合が発生する可能性がある問題を修正[＃46520](https://github.com/pingcap/tidb/issues/46520) @ [3ポイントシュート](https://github.com/3pointer)
        -   PITRがGCS [＃47022](https://github.com/pingcap/tidb/issues/47022) @ [リーヴルス](https://github.com/Leavrth)からデータを回復できない問題を修正
        -   RawKVモード[＃37085](https://github.com/pingcap/tidb/issues/37085) @ [ピンギュ](https://github.com/pingyu)のきめ細かなバックアップフェーズで発生する可能性のあるエラーを修正
        -   PITRを使用してメタkvを回復するとエラー[＃46578](https://github.com/pingcap/tidb/issues/46578) @ [リーヴルス](https://github.com/Leavrth)が発生する可能性がある問題を修正しました
        -   BR統合テストケース[＃46561](https://github.com/pingcap/tidb/issues/46561) @ [ピュアリンド](https://github.com/purelind)のエラーを修正
        -   BRで使用されるグローバルパラメータ`TableColumnCountLimit`と`IndexLimit`デフォルト値を最大値[＃45793](https://github.com/pingcap/tidb/issues/45793) @ [リーヴルス](https://github.com/Leavrth)に増やすことで、復元が失敗する問題を修正しました。
        -   復元されたデータ[＃45476](https://github.com/pingcap/tidb/issues/45476) @ [3ポイントシュート](https://github.com/3pointer)をスキャンするときに br CLI クライアントが停止する問題を修正しました
        -   PITRが`CREATE INDEX` DDL文[＃47482](https://github.com/pingcap/tidb/issues/47482) @ [リーヴルス](https://github.com/Leavrth)の復元をスキップする可能性がある問題を修正しました
        -   1分以内にPITRを複数回実行するとデータ損失が発生する可能性がある問題を修正[＃15483](https://github.com/tikv/tikv/issues/15483) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   異常な状態のレプリケーションタスクが上流のGC [＃9543](https://github.com/pingcap/tiflow/issues/9543) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)をブロックする問題を修正しました
        -   オブジェクトstorageにデータを複製するとデータの不整合が発生する可能性がある問題を修正[＃9592](https://github.com/pingcap/tiflow/issues/9592) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   `redo-resolved-ts`有効にすると、changefeed が失敗する可能性がある問題を修正[＃9769](https://github.com/pingcap/tiflow/issues/9769) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   間違ったメモリ情報を取得すると、一部のオペレーティングシステムで OOM 問題が発生する可能性がある問題を修正[＃9762](https://github.com/pingcap/tiflow/issues/9762) @ [スドジ](https://github.com/sdojjy)
        -   `scale-out`が有効になっている場合のノード間の書き込みキーの不均等な配布の問題を修正[＃9665](https://github.com/pingcap/tiflow/issues/9665) @ [スドジ](https://github.com/sdojjy)
        -   ログ[＃9690](https://github.com/pingcap/tiflow/issues/9690) @ [スドジ](https://github.com/sdojjy)に機密ユーザー情報が記録される問題を修正
        -   TiCDC が誤って名前変更 DDL 操作を同期する可能性がある問題を修正[＃9488](https://github.com/pingcap/tiflow/issues/9488) [＃9378](https://github.com/pingcap/tiflow/issues/9378) [＃9531](https://github.com/pingcap/tiflow/issues/9531) @ [アズドンメン](https://github.com/asddongmen)
        -   すべての変更フィードが削除された後に上流の TiDB GC がブロックされる問題を修正[＃9633](https://github.com/pingcap/tiflow/issues/9633) @ [スドジ](https://github.com/sdojjy)
        -   一部のコーナーケースで TiCDC レプリケーションタスクが失敗する可能性がある問題を修正[＃9685](https://github.com/pingcap/tiflow/issues/9685) [＃9697](https://github.com/pingcap/tiflow/issues/9697) [＃9695](https://github.com/pingcap/tiflow/issues/9695) [＃9736](https://github.com/pingcap/tiflow/issues/9736) @ [ヒック](https://github.com/hicqu) @ [チャールズ・チュン96](https://github.com/CharlesCheung96)
        -   PDノード[＃9565](https://github.com/pingcap/tiflow/issues/9565) @ [アズドンメン](https://github.com/asddongmen)のネットワーク分離によって発生するTiCDCレプリケーションのレイテンシーが大きくなる問題を修正
        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正[＃9584](https://github.com/pingcap/tiflow/issues/9584) @ [フビンズ](https://github.com/fubinzh) @ [アズドンメン](https://github.com/asddongmen)
        -   上流にリージョン[＃9741](https://github.com/pingcap/tiflow/issues/9741) @ [スドジ](https://github.com/sdojjy)が多数ある場合、TiCDC が TiKV ノード障害から迅速に回復できない問題を修正しました。
        -   CSV形式[＃9658](https://github.com/pingcap/tiflow/issues/9658) @ [3エースショーハンド](https://github.com/3AceShowHand)を使用するとTiCDCが誤って`UPDATE`演算を`INSERT`に変更する問題を修正
        -   アップストリーム[＃9476](https://github.com/pingcap/tiflow/issues/9476) [＃9488](https://github.com/pingcap/tiflow/issues/9488) @ [チャールズ・チュン96](https://github.com/CharlesCheung96) @ [アズドンメン](https://github.com/asddongmen)で同じDDL文で複数のテーブルの名前を変更するとレプリケーションエラーが発生する問題を修正
        -   Kafka [＃9504](https://github.com/pingcap/tiflow/issues/9504) @ [3エースショーハンド](https://github.com/3AceShowHand)に同期するときに再試行間隔が短いためにレプリケーションタスクが失敗する問題を修正しました
        -   アップストリーム[＃9430](https://github.com/pingcap/tiflow/issues/9430) @ [スドジ](https://github.com/sdojjy)で 1 つのトランザクションで複数の行の一意のキーが変更されると、レプリケーション書き込み競合が発生する可能性がある問題を修正しました。
        -   ダウンストリームで短期的な障害が発生したときにレプリケーションタスクが停止する可能性がある問題を修正[＃9542](https://github.com/pingcap/tiflow/issues/9542) [＃9272](https://github.com/pingcap/tiflow/issues/9272) [＃9582](https://github.com/pingcap/tiflow/issues/9582) [＃9592](https://github.com/pingcap/tiflow/issues/9592) @ [ヒック](https://github.com/hicqu)
        -   ダウンストリームでエラーが発生し、 [＃9450](https://github.com/pingcap/tiflow/issues/9450) @ [ヒック](https://github.com/hicqu)で再試行すると、レプリケーションタスクが停止する可能性がある問題を修正しました。
        -   Kafka [＃9855](https://github.com/pingcap/tiflow/issues/9855) @ [ヒック](https://github.com/hicqu)にデータを複製するときに TiCDC が停止する可能性がある問題を修正しました

    -   TiDB データ移行 (DM)

        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合に、DM によって返されるレプリケーション ラグが増大し続ける問題を修正しました[＃9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3ハンター](https://github.com/D3Hunter)
        -   DM が大文字と小文字を区別しない照合[＃9489](https://github.com/pingcap/tiflow/issues/9489) @ [ヒヒフフ](https://github.com/hihihuhu)で競合を正しく処理できない問題を修正しました
        -   DM バリデーターのデッドロック問題を修正し、再試行を[＃9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3ハンター](https://github.com/D3Hunter)に強化しました。
        -   楽観的モード[＃9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)でタスクを再開するときに DM がすべての DML をスキップする問題を修正しました
        -   オンライン DDL [＃9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)をスキップするときに DM が上流のテーブル スキーマを適切に追跡できない問題を修正しました
        -   DMが楽観的モード[＃9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)でパーティションDDLをスキップする問題を修正

    -   TiDB Lightning

        -   `AUTO_ID_CACHE=1`を含むテーブルをインポートするときに、間違った`row_id`が[＃46100](https://github.com/pingcap/tidb/issues/46100) @ [D3ハンター](https://github.com/D3Hunter)に割り当てられる問題を修正しました
        -   `NEXT_GLOBAL_ROW_ID` [＃45427](https://github.com/pingcap/tidb/issues/45427) @ [lyzx2001](https://github.com/lyzx2001)を保存するときにデータ型が間違っている問題を修正しました
        -   `checksum = "optional"` [＃45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)のときにチェックサムがエラーを報告する問題を修正しました
        -   PDクラスタアドレスが[＃43436](https://github.com/pingcap/tidb/issues/43436) @ [リチュンジュ](https://github.com/lichunzhu)に変更されるとデータのインポートが失敗する問題を修正しました
        -   PDトポロジが変更されるとTiDB Lightningが起動に失敗する問題を修正[＃46688](https://github.com/pingcap/tidb/issues/46688) @ [ランス6716](https://github.com/lance6716)
        -   CSVデータ[＃43284](https://github.com/pingcap/tidb/issues/43284) @ [lyzx2001](https://github.com/lyzx2001)をインポートする際にルートがpanicになる可能性がある問題を修正

    -   TiDBBinlog

        -   1 GB [＃28659](https://github.com/pingcap/tidb/issues/28659) @ [ジャッキーsp](https://github.com/jackysp)を超えるトランザクションを転送するときにDrainer が終了する問題を修正しました
