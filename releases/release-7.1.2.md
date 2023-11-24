---
title: TiDB 7.1.2 Release Notes
summary: Learn about the compatibility changes, improvements, and bug fixes in TiDB 7.1.2.
---

# TiDB 7.1.2 リリースノート {#tidb-7-1-2-release-notes}

発売日：2023年10月25日

TiDB バージョン: 7.1.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v7.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v7.1.2#version-list)

## 互換性の変更 {#compatibility-changes}

-   [`tidb_opt_enable_hash_join`](https://docs.pingcap.com/tidb/v7.1/system-variables#tidb_opt_enable_hash_join-new-in-v712)システム変数を導入して、オプティマイザがテーブル[#46695](https://github.com/pingcap/tidb/issues/46695) @ [コードプレイ](https://github.com/coderplay)のハッシュ結合を選択するかどうかを制御します。
-   RocksDB の定期的な圧縮をデフォルトで無効にすることで、TiKV RocksDB のデフォルトの動作が v6.5.0 より前のバージョンの動作と一致するようになりました。この変更により、アップグレード後の大量の圧縮によって引き起こされる潜在的なパフォーマンスへの影響が防止されます。さらに、TiKV では 2 つの新しい構成項目[`rocksdb.[defaultcf|writecf|lockcf].periodic-compaction-seconds`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#periodic-compaction-seconds-new-in-v712)および[`rocksdb.[defaultcf|writecf|lockcf].ttl`](https://docs.pingcap.com/tidb/v7.1/tikv-configuration-file#ttl-new-in-v712)が導入され、RocksDB [#15355](https://github.com/tikv/tikv/issues/15355) @ [リククスサシネーター](https://github.com/LykxSassinator)の定期的な圧縮を手動で構成できるようになります。
-   TiCDC では、CSV プロトコルにおけるバイナリ データのエンコード方法を制御する[`sink.csv.binary-encoding-method`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)設定項目を導入しています。デフォルト値は`'base64'` [#9373](https://github.com/pingcap/tiflow/issues/9373) @ [CharlesCheung96](https://github.com/CharlesCheung96)です。
-   TiCDC は[`large-message-handle-option`](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)構成アイテムを導入します。デフォルトでは空です。これは、メッセージ サイズが Kafka トピックの制限を超えると変更フィードが失敗することを意味します。この構成が`"handle-key-only"`に設定されている場合、メッセージがサイズ制限を超えた場合、メッセージ サイズを減らすためにハンドル キーのみが送信されます。削減されたメッセージが依然として制限を超えている場合、変更フィードは失敗します[#9680](https://github.com/pingcap/tiflow/issues/9680) @ [3エースショーハンド](https://github.com/3AceShowHand)

## 改善点 {#improvements}

-   TiDB

    -   新しいオプティマイザー ヒント ( [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-) 、 [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-) 、 [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-) 、 [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-) 、 [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [#45520](https://github.com/pingcap/tidb/issues/45520) @ [qw4990](https://github.com/qw4990)など) を追加します。
    -   コプロセッサ[#46514](https://github.com/pingcap/tidb/issues/46514) @ [あなた06](https://github.com/you06)に関するリクエスト元情報を追加
    -   `/upgrade/start`および`upgrade/finish` API を追加して、TiDB ノード[#47172](https://github.com/pingcap/tidb/issues/47172) @ [ジムララ](https://github.com/zimulala)のアップグレード ステータスの開始と終了をマークします。

-   TiKV

    -   圧縮メカニズムを最適化します。リージョンが分割されるときに、分割するキーがない場合、過剰な MVCC バージョン[#15282](https://github.com/tikv/tikv/issues/15282) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)を排除するために圧縮がトリガーされます。
    -   Router オブジェクトの LRUCache を削除してメモリ使用量を削減し、OOM [#15430](https://github.com/tikv/tikv/issues/15430) @ [コナー1996](https://github.com/Connor1996)を防止します。
    -   `Max gap of safe-ts`と`Min safe ts region`メトリクスを追加し、 `tikv-ctl get-region-read-progress`コマンドを導入して、 resolved-tsとsafe-ts [#15082](https://github.com/tikv/tikv/issues/15082) @ [エキシウム](https://github.com/ekexium)のステータスをより適切に観察および診断します。
    -   TiKV で一部の RocksDB 構成を公開し、ユーザーが TTL や定期的な圧縮などの機能を無効にできるようにします[#14873](https://github.com/tikv/tikv/issues/14873) @ [リククスサシネーター](https://github.com/LykxSassinator)
    -   接続再試行のプロセスで PD クライアントのバックオフ メカニズムを追加します。これにより、エラー再試行中の再試行間隔が徐々に増加し、PD プレッシャー[#15428](https://github.com/tikv/tikv/issues/15428) @ [ノールーシュ](https://github.com/nolouch)が軽減されます。
    -   他のスレッドへの影響を防ぐために、Titan マニフェスト ファイルを書き込むときにミューテックスを保持しないようにします[#15351](https://github.com/tikv/tikv/issues/15351) @ [コナー1996](https://github.com/Connor1996)
    -   OOM [#15458](https://github.com/tikv/tikv/issues/15458) @ [オーバーヴィーナス](https://github.com/overvenus)を防ぐためにリゾルバーのメモリ使用量を最適化します。

-   PD

    -   PD 呼び出し元のバックオフ メカニズムを最適化して、呼び出しが失敗した場合の RPC リクエストの頻度を削減します[#6556](https://github.com/tikv/pd/issues/6556) @ [ノールーシュ](https://github.com/nolouch) @ [ルルンクス](https://github.com/rleungx) @ [ヒューシャープ](https://github.com/HuSharp)
    -   `GetRegions`インターフェイスにキャンセル メカニズムを導入し、発信者が切断されたときに CPU とメモリを解放します[#6835](https://github.com/tikv/pd/issues/6835) @ [lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   Grafana [#8050](https://github.com/pingcap/tiflash/issues/8050) @ [ホンユニャン](https://github.com/hongyunyan)のインデックス データのメモリ使用量の監視メトリクスを追加

-   ツール

    -   バックアップと復元 (BR)

        -   HTTP クライアント[#46011](https://github.com/pingcap/tidb/issues/46011) @ [レヴルス](https://github.com/Leavrth)で`MaxIdleConns`および`MaxIdleConnsPerHost`パラメータを設定することにより、ログ バックアップおよび PITR 復元タスクの接続再利用のサポートを強化します。
        -   ログバックアップの CPU オーバーヘッドを削減`resolve lock` [#40759](https://github.com/pingcap/tidb/issues/40759) @ [3ポインター](https://github.com/3pointer)
        -   新しい復元パラメータを追加します`WaitTiflashReady` 。このパラメータが有効な場合、 TiFlashレプリカが正常に複製された後に復元操作が完了します[#43828](https://github.com/pingcap/tidb/issues/43828) [#46302](https://github.com/pingcap/tidb/issues/46302) @ [3ポインター](https://github.com/3pointer)

    -   TiCDC

        -   いくつかの TiCDC モニタリング メトリックとアラーム ルール[#9047](https://github.com/pingcap/tiflow/issues/9047) @ [東門](https://github.com/asddongmen)を最適化します。
        -   Kafka シンクは、メッセージが大きすぎる場合に[ハンドルキーデータのみを送信する](/ticdc/ticdc-sink-to-kafka.md#handle-messages-that-exceed-the-kafka-topic-limit)をサポートし、過剰なメッセージ サイズによるチェンジフィードの失敗を回避します[#9680](https://github.com/pingcap/tiflow/issues/9680) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   `ADD INDEX` DDL 操作を複製する実行ロジックを最適化して、後続の DML ステートメントのブロックを回避します[#9644](https://github.com/pingcap/tiflow/issues/9644) @ [スドジ](https://github.com/sdojjy)
        -   TiCDC が失敗後に再試行するときのステータス メッセージを調整します[#9483](https://github.com/pingcap/tiflow/issues/9483) @ [東門](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   互換性のない DDL ステートメントに対する厳密な楽観的モードのサポート[#9112](https://github.com/pingcap/tiflow/issues/9112) @ [GMHDBJD](https://github.com/GMHDBJD)

    -   TiDB Lightning

        -   デフォルト値の`checksum-via-sql`を`false`に変更して、インポート タスクのパフォーマンスを向上させます[#45368](https://github.com/pingcap/tidb/issues/45368) [#45094](https://github.com/pingcap/tidb/issues/45094) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   データ インポート フェーズ[#46253](https://github.com/pingcap/tidb/issues/46253) @ [ランス6716](https://github.com/lance6716)中の`no leader`エラーに対するTiDB Lightningの再試行ロジックを最適化します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `GROUP_CONCAT`が`ORDER BY`列[#41986](https://github.com/pingcap/tidb/issues/41986) @ [アイリンキッド](https://github.com/AilinKid)を解析できない問題を修正
    -   システム テーブル`INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると、場合によっては誤った結果が返される問題を修正します[#45531](https://github.com/pingcap/tidb/issues/45531) @ [定義2014](https://github.com/Defined2014)
    -   メタデータの読み取りに 1 回の DDL リース[#45176](https://github.com/pingcap/tidb/issues/45176) @ [ジムララ](https://github.com/zimulala)よりも長い時間がかかると TiDB のアップグレードが停止する問題を修正
    -   CTE を使用して DML ステートメントを実行するとpanic[#46083](https://github.com/pingcap/tidb/issues/46083) @ [ウィノロス](https://github.com/winoros)が発生する可能性がある問題を修正
    -   パーティション交換[#46492](https://github.com/pingcap/tidb/issues/46492) @ [むじょん](https://github.com/mjonss)時にパーティション定義に準拠しないデータを検出できない問題を修正
    -   `MERGE_JOIN`の結果が正しくない問題を修正[#46580](https://github.com/pingcap/tidb/issues/46580) @ [qw4990](https://github.com/qw4990)
    -   符号なし型と`Duration`型定数[#45410](https://github.com/pingcap/tidb/issues/45410) @ [wshwsh12](https://github.com/wshwsh12)を比較するときに発生する誤った結果を修正しました。
    -   `AUTO_ID_CACHE=1`を[#46444](https://github.com/pingcap/tidb/issues/46444) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定すると`Duplicate entry`発生する場合がある問題を修正
    -   TTL [#45510](https://github.com/pingcap/tidb/issues/45510) @ [ルクワンチャオ](https://github.com/lcwangchao)実行時のメモリリークの問題を修正
    -   接続を強制終了すると go コルーチン リーク[#46034](https://github.com/pingcap/tidb/issues/46034) @ [ピンギュ](https://github.com/pingyu)が発生する可能性がある問題を修正
    -   インデックス結合のエラーによりクエリがスタックする可能性がある問題を修正します[#45716](https://github.com/pingcap/tidb/issues/45716) @ [wshwsh12](https://github.com/wshwsh12)
    -   `BatchPointGet`演算子がハッシュ パーティション テーブル[#46779](https://github.com/pingcap/tidb/issues/46779) @ [ジフフスト](https://github.com/jiyfhust)に対して誤った結果を返す問題を修正
    -   `EXCHANGE PARTITION`失敗するかキャンセルされると、パーティション テーブルに対する制限が元のテーブルに残る問題を修正します[#45920](https://github.com/pingcap/tidb/issues/45920) [#45791](https://github.com/pingcap/tidb/issues/45791) @ [むじょん](https://github.com/mjonss)
    -   2 つのサブクエリ[#46160](https://github.com/pingcap/tidb/issues/46160) @ [qw4990](https://github.com/qw4990)を結合するときに`TIDB_INLJ`ヒントが有効にならない問題を修正
    -   `DATETIME`または`TIMESTAMP`列を数値定数[#38361](https://github.com/pingcap/tidb/issues/38361) @ [イービン87](https://github.com/yibin87)と比較するときに動作が MySQL と矛盾する問題を修正
    -   深くネストされた式に対して HashCode が繰り返し計算され、メモリ使用量が増加し、OOM [#42788](https://github.com/pingcap/tidb/issues/42788) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正します。
    -   アクセス パス プルーニング ロジックが`READ_FROM_STORAGE(TIFLASH[...])`ヒントを無視し、 `Can't find a proper physical plan`エラー[#40146](https://github.com/pingcap/tidb/issues/40146) @ [アイリンキッド](https://github.com/AilinKid)を引き起こす問題を修正します。
    -   CAST に精度の損失がない[#45199](https://github.com/pingcap/tidb/issues/45199) @ [アイリンキッド](https://github.com/AilinKid)のときに、 `cast(col)=range`条件によってフルスキャンが発生する問題を修正します。
    -   `plan replayer dump explain`がエラー[#46197](https://github.com/pingcap/tidb/issues/46197) @ [時間と運命](https://github.com/time-and-fate)を報告する問題を修正
    -   `tmp-storage-quota`設定が有効にならない問題を修正[#45161](https://github.com/pingcap/tidb/issues/45161) [#26806](https://github.com/pingcap/tidb/issues/26806) @ [wshwsh12](https://github.com/wshwsh12)
    -   TiDB パーサーが状態のままになり、解析エラー[#45898](https://github.com/pingcap/tidb/issues/45898) @ [qw4990](https://github.com/qw4990)が発生する問題を修正します。
    -   MPP 実行プランの Union を介して集計がプッシュダウンされると、結果が正しくない[#45850](https://github.com/pingcap/tidb/issues/45850) @ [アイリンキッド](https://github.com/AilinKid)という問題を修正します。
    -   `AUTO_ID_CACHE=1`を[#46454](https://github.com/pingcap/tidb/issues/46454) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)に設定すると、panic後の TiDB の回復が遅くなる問題を修正
    -   Sort オペレーターにより、スピル プロセス[#47538](https://github.com/pingcap/tidb/issues/47538) @ [ウィンドトーカー](https://github.com/windtalker)中に TiDB がクラッシュする可能性がある問題を修正します。
    -   BRを使用して`AUTO_ID_CACHE=1` [#46093](https://github.com/pingcap/tidb/issues/46093) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)の非クラスター化インデックス テーブルを復元するときに重複する主キーの問題を修正します。
    -   静的プルーニング モードでパーティション テーブルをクエリし、実行プランに`IndexLookUp` [#45757](https://github.com/pingcap/tidb/issues/45757) @ [定義2014](https://github.com/Defined2014)が含まれている場合、クエリでエラーが報告される可能性がある問題を修正します。
    -   パーティションテーブルテーブルと配置ポリシー[#45791](https://github.com/pingcap/tidb/issues/45791) @ [むじょん](https://github.com/mjonss)を持つテーブルの間でパーティションを交換した後、パーティション テーブルへのデータの挿入が失敗することがある問題を修正します。
    -   間違ったタイムゾーン情報[#46033](https://github.com/pingcap/tidb/issues/46033) @ [タンジェンタ](https://github.com/tangenta)を使用して時間フィールドをエンコードする問題を修正
    -   `tmp`ディレクトリが存在しない場合、インデックスを高速追加する DDL ステートメントがスタックする問題を修正[#45456](https://github.com/pingcap/tidb/issues/45456) @ [タンジェンタ](https://github.com/tangenta)
    -   複数の TiDB インスタンスを同時にアップグレードすると、アップグレード プロセス[#46288](https://github.com/pingcap/tidb/issues/46228) @ [ジムララ](https://github.com/zimulala)がブロックされる可能性がある問題を修正します。
    -   領域[#46135](https://github.com/pingcap/tidb/issues/46135) @ [ジムララ](https://github.com/zimulala)の分割に使用される不正なパラメータによって引き起こされる不均一なリージョン散乱の問題を修正します。
    -   TiDB の再起動後に DDL 操作が停止する可能性がある問題を修正[#46751](https://github.com/pingcap/tidb/issues/46751) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   非整数クラスター化インデックス[#47350](https://github.com/pingcap/tidb/issues/47350) @ [タンジェンタ](https://github.com/tangenta)での分割テーブル操作の禁止
    -   不適切な MDL 処理[#46920](https://github.com/pingcap/tidb/issues/46920) @ [wjhuang2016](https://github.com/wjhuang2016)が原因で DDL 操作が永続的にブロックされる可能性がある問題を修正します。
    -   `RENAME TABLE`操作[#47064](https://github.com/pingcap/tidb/issues/47064) @ [ジフフスト](https://github.com/jiyfhust)によって引き起こされるテーブル内の重複列の問題を修正
    -   `batch-client` `client-go` @ [クレイジークス520](https://github.com/crazycs520) [#47691](https://github.com/pingcap/tidb/issues/47691)panicの問題を修正
    -   メモリ使用量がメモリ制限[#45706](https://github.com/pingcap/tidb/issues/45706) @ [ホーキングレイ](https://github.com/hawkingrei)を超えた場合、パーティション テーブルの統計収集が時間内に強制終了されない問題を修正します。
    -   クエリに`UNHEX`条件[#45378](https://github.com/pingcap/tidb/issues/45378) @ [qw4990](https://github.com/qw4990)が含まれる場合、クエリ結果が不正確になる問題を修正します。
    -   TiDB が`GROUP_CONCAT` [#41957](https://github.com/pingcap/tidb/issues/41957) @ [アイリンキッド](https://github.com/AilinKid)のクエリに対して`Can't find column`を返す問題を修正

-   TiKV

    -   RawKV API V2 [#15142](https://github.com/tikv/tikv/issues/15142) @ [ピンギュ](https://github.com/pingyu)で`ttl-check-poll-interval`設定項目が有効にならない問題を修正
    -   raftstore-applys [#15371](https://github.com/tikv/tikv/issues/15371) @ [コナー1996](https://github.com/Connor1996)が増加し続けるデータ エラーを修正
    -   データ レプリケーション自動同期モード[#14975](https://github.com/tikv/tikv/issues/14975) @ [ノールーシュ](https://github.com/nolouch)の同期回復フェーズで QPS がゼロに低下する問題を修正します。
    -   1 つの TiKV ノードが分離され、別のノードが再起動されたときに発生する可能性があるデータの不整合の問題を修正します[#15035](https://github.com/tikv/tikv/issues/15035) @ [オーバーヴィーナス](https://github.com/overvenus)
    -   Online Unsafe Recovery がマージ中止[#15580](https://github.com/tikv/tikv/issues/15580) @ [v01dstar](https://github.com/v01dstar)を処理できない問題を修正
    -   PD と TiKV の間のネットワークの中断により PITR がスタックする可能性がある問題を修正します[#15279](https://github.com/tikv/tikv/issues/15279) @ [ユジュンセン](https://github.com/YuJuncen)
    -   `FLASHBACK` [#15258](https://github.com/tikv/tikv/issues/15258) @ [オーバーヴィーナス](https://github.com/overvenus)を実行した後、 リージョン Merge がブロックされる場合がある問題を修正
    -   ストアハートビートビートの再試行数を[#15184](https://github.com/tikv/tikv/issues/15184) @ [ノールーシュ](https://github.com/nolouch)に減らすことで、ハートビートビート ストームの問題を修正します。
    -   オンライン安全でないリカバリがタイムアウト[#15346](https://github.com/tikv/tikv/issues/15346) @ [コナー1996](https://github.com/Connor1996)で中止されない問題を修正
    -   暗号化により部分書き込み[#15080](https://github.com/tikv/tikv/issues/15080) @ [タボキー](https://github.com/tabokie)中にデータ破損が発生する可能性がある問題を修正
    -   リージョン[#13311](https://github.com/tikv/tikv/issues/13311) @ [cfzjywxk](https://github.com/cfzjywxk)の不正なメタデータによって引き起こされる TiKVpanic問題を修正
    -   オンライン ワークロード[#15565](https://github.com/tikv/tikv/issues/15565) @ [ランス6716](https://github.com/lance6716)があるときにTiDB Lightningチェックサム コプロセッサのリクエストがタイムアウトになる問題を修正
    -   ピアを移動するとFollower Readのパフォーマンスが低下する可能性がある問題を修正[#15468](https://github.com/tikv/tikv/issues/15468) @ [ユジュンセン](https://github.com/YuJuncen)

-   PD

    -   v2 スケジューラ アルゴリズム[#6645](https://github.com/tikv/pd/issues/6645) @ [lhy1024](https://github.com/lhy1024)でホット リージョンがスケジュールされない可能性がある問題を修正
    -   TLS ハンドシェイクにより空のクラスター[#6913](https://github.com/tikv/pd/issues/6913) @ [ノールーシュ](https://github.com/nolouch)で CPU 使用率が高くなる可能性がある問題を修正
    -   PD ノード間のインジェクション エラーにより PDpanic[#6858](https://github.com/tikv/pd/issues/6858) @ [ヒューシャープ](https://github.com/HuSharp)が発生する可能性がある問題を修正
    -   ストア情報の同期により PD リーダーが終了してスタックする可能性がある問題を修正[#6918](https://github.com/tikv/pd/issues/6918) @ [ルルンクス](https://github.com/rleungx)
    -   Flashback [#6912](https://github.com/tikv/pd/issues/6912) @ [オーバーヴィーナス](https://github.com/overvenus)後にリージョン情報が更新されない問題を修正
    -   [#7053](https://github.com/tikv/pd/issues/7053) @ [ヒューシャープ](https://github.com/HuSharp)の終了中に PD がpanicになる問題を修正
    -   コンテキスト タイムアウトにより`lease timeout`エラー[#6926](https://github.com/tikv/pd/issues/6926) @ [ルルンクス](https://github.com/rleungx)が発生する可能性がある問題を修正
    -   ピアがグループごとに適切に分散されていないため、リーダー[#6962](https://github.com/tikv/pd/issues/6962) @ [ルルンクス](https://github.com/rleungx)が不均等に分散される可能性がある問題を修正します。
    -   pd-ctl [#7121](https://github.com/tikv/pd/issues/7121) @ [ルルンクス](https://github.com/rleungx)を使用した更新時に分離レベルラベルが同期されない問題を修正
    -   `evict-leader-scheduler`が設定[#6897](https://github.com/tikv/pd/issues/6897) @ [ヒューシャープ](https://github.com/HuSharp)を失う可能性がある問題を修正
    -   プラグインのディレクトリとファイルの潜在的なセキュリティ リスクを修正[#7094](https://github.com/tikv/pd/issues/7094) @ [ヒューシャープ](https://github.com/HuSharp)
    -   リソース制御[#45050](https://github.com/pingcap/tidb/issues/45050) @ [グロルフ](https://github.com/glorv)を有効にした後、DDL がアトミック性を保証しない可能性がある問題を修正
    -   ルールチェッカーがピア[#6559](https://github.com/tikv/pd/issues/6559) @ [ノールーシュ](https://github.com/nolouch)を選択すると、異常なピアを削除できない問題を修正
    -   etcd がすでに開始されているが、クライアントがまだ接続していないときに、クライアントを呼び出すと PD がpanic[#6860](https://github.com/tikv/pd/issues/6860) @ [ヒューシャープ](https://github.com/HuSharp)になる可能性がある問題を修正します。
    -   RU 消費量が 0 未満であると PD がクラッシュする問題を修正します[#6973](https://github.com/tikv/pd/issues/6973) @ [キャビンフィーバーB](https://github.com/CabinfeverB)
    -   クラスターが大きい[#46664](https://github.com/pingcap/tidb/issues/46664) @ [ヒューシャープ](https://github.com/HuSharp)の場合、client-go を定期的`min-resolved-ts`更新すると PD OOM が発生する可能性がある問題を修正

-   TiFlash

    -   MemoryTracker によって報告されるメモリ使用量が不正確である問題を修正[#8128](https://github.com/pingcap/tiflash/issues/8128) @ [ジンヘリン](https://github.com/JinheLin)
    -   リージョン[#7762](https://github.com/pingcap/tiflash/issues/7762) @ [リデズ](https://github.com/lidezhu)の無効な範囲キーによりTiFlashデータが不整合になる問題を修正
    -   `DATETIME` 、 `TIMESTAMP` 、または`TIME`データ型[#7809](https://github.com/pingcap/tiflash/issues/7809) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)の`fsp`が変更された後にクエリが失敗する問題を修正します。
    -   同じ MPP タスク内に複数の HashAgg 演算子がある場合、MPP タスクのコンパイルに過度に時​​間がかかり、クエリのパフォーマンス[#7810](https://github.com/pingcap/tiflash/issues/7810) @ [シーライズ](https://github.com/SeaRise)に深刻な影響を与える可能性がある問題を修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   PITR を使用して暗黙的な主キーを回復すると競合が発生する可能性がある問題を修正[#46520](https://github.com/pingcap/tidb/issues/46520) @ [3ポインター](https://github.com/3pointer)
        -   PITR が GCS [#47022](https://github.com/pingcap/tidb/issues/47022) @ [レヴルス](https://github.com/Leavrth)からのデータの回復に失敗する問題を修正
        -   RawKV モード[#37085](https://github.com/pingcap/tidb/issues/37085) @ [ピンギュ](https://github.com/pingyu)の詳細なバックアップ フェーズで発生する可能性のあるエラーを修正しました。
        -   PITR を使用してメタ KV を回復するとエラー[#46578](https://github.com/pingcap/tidb/issues/46578) @ [レヴルス](https://github.com/Leavrth)が発生する可能性がある問題を修正
        -   BR統合テスト ケース[#45561](https://github.com/pingcap/tidb/issues/46561) @ [ピュアリンド](https://github.com/purelind)のエラーを修正
        -   BRで使用されるグローバル パラメータ`TableColumnCountLimit`および`IndexLimit`のデフォルト値を最大値[#45793](https://github.com/pingcap/tidb/issues/45793) @ [レヴルス](https://github.com/Leavrth)に増やすことで、復元の失敗の問題を修正します。
        -   復元されたデータ[#45476](https://github.com/pingcap/tidb/issues/45476) @ [3ポインター](https://github.com/3pointer)をスキャンするときに br CLI クライアントがスタックする問題を修正
        -   PITR が`CREATE INDEX` DDL ステートメント[#47482](https://github.com/pingcap/tidb/issues/47482) @ [レヴルス](https://github.com/Leavrth)の復元をスキップする可能性がある問題を修正します。
        -   1 分以内に PITR を複数回実行するとデータ損失[#15483](https://github.com/tikv/tikv/issues/15483) @ [ユジュンセン](https://github.com/YuJuncen)が発生する可能性がある問題を修正

    -   TiCDC

        -   異常状態のレプリケーションタスクが上流の GC [#9543](https://github.com/pingcap/tiflow/issues/9543) @ [CharlesCheung96](https://github.com/CharlesCheung96)をブロックする問題を修正
        -   オブジェクトstorageにデータをレプリケートするとデータの不整合が発生する可能性がある問題を修正します[#9592](https://github.com/pingcap/tiflow/issues/9592) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `redo-resolved-ts`を有効にすると変更フィードが失敗する可能性がある問題を修正します[#9769](https://github.com/pingcap/tiflow/issues/9769) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   一部のオペレーティング システム[#9762](https://github.com/pingcap/tiflow/issues/9762) @ [スドジ](https://github.com/sdojjy)で、間違ったメモリ情報を取得すると OOM の問題が発生する可能性がある問題を修正します。
        -   `scale-out`が有効になっている場合、 [#9665](https://github.com/pingcap/tiflow/issues/9665) @ [スドジ](https://github.com/sdojjy)の場合にノード間で書き込みキーが不均等に分散される問題を修正します。
        -   機密ユーザー情報がログ[#9690](https://github.com/pingcap/tiflow/issues/9690) @ [スドジ](https://github.com/sdojjy)に記録される問題を修正
        -   TiCDC が名前変更 DDL 操作を誤って同期する可能性がある問題を修正します[#9488](https://github.com/pingcap/tiflow/issues/9488) [#9378](https://github.com/pingcap/tiflow/issues/9378) [#9531](https://github.com/pingcap/tiflow/issues/9531) @ [東門](https://github.com/asddongmen)
        -   すべての変更フィードが削除された後、上流の TiDB GC がブロックされる問題を修正[#9633](https://github.com/pingcap/tiflow/issues/9633) @ [スドジ](https://github.com/sdojjy)
        -   TiCDC レプリケーション タスクが特殊なケースで失敗する可能性がある問題を修正します[#9685](https://github.com/pingcap/tiflow/issues/9685) [#9697](https://github.com/pingcap/tiflow/issues/9697) [#9695](https://github.com/pingcap/tiflow/issues/9695) [#9736](https://github.com/pingcap/tiflow/issues/9736) @ [ひっくり返る](https://github.com/hicqu) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   PD ノード[#9565](https://github.com/pingcap/tiflow/issues/9565) @ [東門](https://github.com/asddongmen)のネットワーク分離によって引き起こされる高い TiCDC レプリケーションレイテンシーの問題を修正します。
        -   PD のスケールアップおよびスケールダウン中に TiCDC が無効な古いアドレスにアクセスする問題を修正します[#9584](https://github.com/pingcap/tiflow/issues/9584) @ [フビンジ](https://github.com/fubinzh) @ [東門](https://github.com/asddongmen)
        -   アップストリーム[#9741](https://github.com/pingcap/tiflow/issues/9741) @ [スドジ](https://github.com/sdojjy)に多数のリージョンがある場合、TiCDC が TiKV ノードの障害から迅速に回復できない問題を修正
        -   CSV 形式[#9658](https://github.com/pingcap/tiflow/issues/9658) @ [3エースショーハンド](https://github.com/3AceShowHand)を使用すると、TiCDC が`UPDATE`操作を誤って`INSERT`に変更する問題を修正します。
        -   アップストリーム[#9476](https://github.com/pingcap/tiflow/issues/9476) [#9488](https://github.com/pingcap/tiflow/issues/9488) @ [CharlesCheung96](https://github.com/CharlesCheung96) @ [東門](https://github.com/asddongmen)の同じ DDL ステートメントで複数のテーブルの名前が変更されると、レプリケーション エラーが発生する問題を修正します。
        -   Kafka [#9504](https://github.com/pingcap/tiflow/issues/9504) @ [3エースショーハンド](https://github.com/3AceShowHand)と同期するときに、再試行間隔が短いためにレプリケーション タスクが失敗する問題を修正します。
        -   アップストリーム[#9430](https://github.com/pingcap/tiflow/issues/9430) @ [スドジ](https://github.com/sdojjy)の 1 つのトランザクションで複数の行の一意のキーが変更されると、レプリケーション書き込みの競合が発生する可能性がある問題を修正します。
        -   ダウンストリームで短期間の障害が発生したときにレプリケーション タスクが停止する可能性がある問題を修正します[#9542](https://github.com/pingcap/tiflow/issues/9542) [#9272](https://github.com/pingcap/tiflow/issues/9272) [#9582](https://github.com/pingcap/tiflow/issues/9582) [#9592](https://github.com/pingcap/tiflow/issues/9592) @ [ひっくり返る](https://github.com/hicqu)
        -   ダウンストリームでエラーが発生し、 [#9450](https://github.com/pingcap/tiflow/issues/9450) @ [ひっくり返る](https://github.com/hicqu)を再試行すると、レプリケーション タスクが停止する可能性がある問題を修正します。

    -   TiDB データ移行 (DM)

        -   失敗した DDL がスキップされ、後続の DDL が実行されない場合、DM から返されるレプリケーション ラグが増大し続ける問題を修正します[#9605](https://github.com/pingcap/tiflow/issues/9605) @ [D3ハンター](https://github.com/D3Hunter)
        -   DM が大文字と小文字を区別しない照合順序[#9489](https://github.com/pingcap/tiflow/issues/9489) @ [ヒヒヒヒヒ](https://github.com/hihihuhu)との競合を正しく処理できない問題を修正します。
        -   DM バリデーターのデッドロック問題を修正し、再試行[#9257](https://github.com/pingcap/tiflow/issues/9257) @ [D3ハンター](https://github.com/D3Hunter)を強化しました。
        -   楽観的モード[#9588](https://github.com/pingcap/tiflow/issues/9588) @ [GMHDBJD](https://github.com/GMHDBJD)でタスクを再開すると、DM がすべての DML をスキップする問題を修正します。
        -   オンライン DDL [#9587](https://github.com/pingcap/tiflow/issues/9587) @ [GMHDBJD](https://github.com/GMHDBJD)をスキップすると、DM がアップストリーム テーブル スキーマを適切に追跡できない問題を修正します。
        -   DM が楽観的モード[#9788](https://github.com/pingcap/tiflow/issues/9788) @ [GMHDBJD](https://github.com/GMHDBJD)でパーティション DDL をスキップする問題を修正

    -   TiDB Lightning

        -   `AUTO_ID_CACHE=1`を含むテーブルをインポートすると、間違った`row_id`が[#46100](https://github.com/pingcap/tidb/issues/46100) @ [D3ハンター](https://github.com/D3Hunter)に割り当てられる問題を修正します。
        -   `NEXT_GLOBAL_ROW_ID` [#45427](https://github.com/pingcap/tidb/issues/45427) @ [lyzx2001](https://github.com/lyzx2001)を保存する際にデータ型が間違っている問題を修正
        -   `checksum = "optional"` [#45382](https://github.com/pingcap/tidb/issues/45382) @ [lyzx2001](https://github.com/lyzx2001)の場合でもチェックサムがエラーを報告する問題を修正
        -   PDクラスタアドレスが[#43436](https://github.com/pingcap/tidb/issues/43436) @ [リチュンジュ](https://github.com/lichunzhu)に変更されるとデータインポートが失敗する問題を修正
        -   PD トポロジを変更するとTiDB Lightning が起動できない問題を修正[#46688](https://github.com/pingcap/tidb/issues/46688) @ [ランス6716](https://github.com/lance6716)
        -   CSVデータ[#43284](https://github.com/pingcap/tidb/issues/43284) @ [lyzx2001](https://github.com/lyzx2001)のインポート時にルートがpanicになる問題を修正

    -   TiDBBinlog

        -   1 GB [#28659](https://github.com/pingcap/tidb/issues/28659) @ [ジャッキースプ](https://github.com/jackysp)を超えるトランザクションを転送するときにDrainerが終了する問題を修正
