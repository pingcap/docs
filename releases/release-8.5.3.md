---
title: TiDB 8.5.3 Release Notes
summary: TiDB 8.5.3 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 8.5.3 リリースノート {#tidb-8-5-3-release-notes}

発売日：2025年8月14日

TiDB バージョン: 8.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   [コストモデル](/cost-model.md)の内部使用のために、以下のシステム変数を追加します。これらの変数を変更することは推奨され**ません**: [`tidb_opt_hash_agg_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_hash_agg_cost_factor-new-in-v853) 、 [`tidb_opt_hash_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_hash_join_cost_factor-new-in-v853) 、 [`tidb_opt_index_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_join_cost_factor-new-in-v853) 、 [`tidb_opt_index_lookup_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_lookup_cost_factor-new-in-v853) 、 [`tidb_opt_index_merge_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_merge_cost_factor-new-in-v853) 、 [`tidb_opt_index_reader_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_reader_cost_factor-new-in-v853) 、 [`tidb_opt_index_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_scan_cost_factor-new-in-v853) 、 [`tidb_opt_limit_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_limit_cost_factor-new-in-v853) 、 [`tidb_opt_merge_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_merge_join_cost_factor-new-in-v853) 、 [`tidb_opt_sort_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_sort_cost_factor-new-in-v853) 、 [`tidb_opt_stream_agg_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_stream_agg_cost_factor-new-in-v853) 、 [`tidb_opt_table_full_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_full_scan_cost_factor-new-in-v853) 、 [`tidb_opt_table_range_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_range_scan_cost_factor-new-in-v853) 、 [`tidb_opt_table_reader_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_reader_cost_factor-new-in-v853) 、 [`tidb_opt_table_rowid_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_rowid_cost_factor-new-in-v853) 、 [`tidb_opt_table_tiflash_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_tiflash_scan_cost_factor-new-in-v853) 、および[`tidb_opt_topn_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_topn_cost_factor-new-in-v853) [＃60357](https://github.com/pingcap/tidb/issues/60357) @ [テリー・パーセル](https://github.com/terry1purcell)
-   [テレメトリー](https://docs.pingcap.com/tidb/v8.5/telemetry)機能を再導入します。ただし、テレメトリ関連の情報はローカルにのみ記録され、ネットワーク経由で PingCAP にデータが送信されなくなります[＃61766](https://github.com/pingcap/tidb/issues/61766) @ [定義2014](https://github.com/Defined2014)

## 改善点 {#improvements}

-   TiDB

    -   統計情報がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外である場合に、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   グローバルソートを使用して一意のインデックスを追加する際のパフォーマンスを改善し、重複した一意のインデックスを追加する際のエラーメッセージを改良しました[＃61689](https://github.com/pingcap/tidb/issues/61689) @ [CbcWestwolf](https://github.com/CbcWestwolf)
    -   `IMPORT INTO`グローバルソート[＃60361](https://github.com/pingcap/tidb/issues/60361)が有効の場合、TiKV のインポートモードへの切り替えを無効にします ( [D3ハンター](https://github.com/D3Hunter)場合)
    -   インデックス追加[＃60925](https://github.com/pingcap/tidb/issues/60925) @ [CbcWestwolf](https://github.com/CbcWestwolf)中の TiKV への書き込み速度を観察するための監視メトリックを追加します。
    -   `merge sort`サブタスクのスケジュールロジックを最適化してソートパフォーマンスを向上させる[＃60375](https://github.com/pingcap/tidb/issues/60375) @ [接線](https://github.com/tangenta)
    -   外部キーを持つテーブルを大量に作成する場合のテーブル作成を高速化し、メモリ使用効率を最適化します[＃61126](https://github.com/pingcap/tidb/issues/61126) @ [GMHDBJD](https://github.com/GMHDBJD)
    -   `information_schema.tables`テーブル[#62020](https://github.com/pingcap/tidb/issues/62020) @ [接線](https://github.com/tangenta)の読み取りパフォーマンスを向上
    -   データインポート[＃61553](https://github.com/pingcap/tidb/issues/61553) @ [接線](https://github.com/tangenta)中のリージョン分割とデータ取り込みのためのフロー制御インターフェースを追加します
    -   IndexScanのプラン構築プロセスを最適化し、 `fmt.Sprintf()`呼び出しを[＃56649](https://github.com/pingcap/tidb/issues/56649) / [crazycs520](https://github.com/crazycs520)削減
    -   インデックス[＃61025](https://github.com/pingcap/tidb/issues/61025) @ [fzzf678](https://github.com/fzzf678)でグローバルソートを使用する場合のマージソートステージの監視メトリックを追加します。
    -   `IndexLookup`オペレータが`context canceled`エラー[＃61072](https://github.com/pingcap/tidb/issues/61072) @ [イービン87](https://github.com/yibin87)に遭遇したときに冗長なログエントリを削除します
    -   `tidb_replica_read` `closest-adaptive` [＃61745](https://github.com/pingcap/tidb/issues/61745) @ [あなた06](https://github.com/you06)に設定するとパフォーマンスが向上します
    -   大規模クラスタの監視メトリクスデータの量を減らすことで運用コストを削減[＃59990](https://github.com/pingcap/tidb/issues/59990) @ [ジムララ](https://github.com/zimulala)

-   TiKV

    -   フォアグラウンド書き込みをブロックせずにSSTファイルの取り込みをサポートし、レイテンシー[＃18081](https://github.com/tikv/tikv/issues/18081) @ [hhwyt](https://github.com/hhwyt)の影響を軽減します。
    -   フローコントローラ[＃18625](https://github.com/tikv/tikv/issues/18625) @ [hhwyt](https://github.com/hhwyt)によるパフォーマンスジッタを軽減
    -   TiDB [＃18081](https://github.com/tikv/tikv/issues/18081) @ [金星の上](https://github.com/overvenus)での`ADD INDEX`操作中のテールレイテンシーを最適化
    -   Raftstoreの`CompactedEvent`処理を`split-check`ワーカーに移動して最適化し、メインのRaftstoreスレッド[＃18532](https://github.com/tikv/tikv/issues/18532) @ [LykxSassinator](https://github.com/LykxSassinator)のブロッキングを削減します。
    -   SST の取り込みが遅すぎる場合は`SST ingest is experiencing slowdowns`のみをログに記録し、パフォーマンスのジッターを回避するために`get_sst_key_ranges`呼び出しをスキップします[＃18549](https://github.com/tikv/tikv/issues/18549) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   KvDB と RaftDB が別々のマウント パス[＃18463](https://github.com/tikv/tikv/issues/18463) @ [LykxSassinator](https://github.com/LykxSassinator)を使用する場合の KvDB ディスクの I/O ジッターの検出メカニズムを最適化します。
    -   Raft Engineの`fetch_entries_to`のパフォーマンスを最適化して競合を減らし、混合ワークロード[＃18605](https://github.com/tikv/tikv/issues/18605) @ [LykxSassinator](https://github.com/LykxSassinator)でのパフォーマンスを向上します。
    -   残留データのクリーンアップメカニズムを最適化して、リクエストのレイテンシー[＃18107](https://github.com/tikv/tikv/issues/18107) @ [LykxSassinator](https://github.com/LykxSassinator)への影響を軽減します。

-   PD

    -   Prometheus [＃8931](https://github.com/tikv/pd/issues/8931) @ [バッファフライ](https://github.com/bufferflies)に GO ランタイム関連の監視メトリクスを追加
    -   低速ノードリーダーの排除をトリガーした後の回復時間を 600 秒から 900 秒 (15 分) に延長します[＃9329](https://github.com/tikv/pd/issues/9329) @ [rleungx](https://github.com/rleungx)

-   TiFlash

    -   storageスナップショットを取得する際の最大再試行回数を増やし、大規模なテーブルのクエリの安定性を向上させます[＃10300](https://github.com/pingcap/tiflash/issues/10300) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   ワイドテーブルシナリオにおけるTiFlash OOM リスクの観測可能性を強化[＃10272](https://github.com/pingcap/tiflash/issues/10272) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   インデックスを[＃59158](https://github.com/pingcap/tidb/issues/59158) @ [リーヴルス](https://github.com/Leavrth)で同時に修復することにより、PITR 中のインデックス復元速度が向上します。
        -   TiKVのダウンロードAPIは、バックアップファイルをダウンロードする際に特定の時間範囲内のデータをフィルタリングすることをサポートしており、復元時に古いデータバージョンや将来のデータバージョンがインポートされるのを回避します[＃18399](https://github.com/tikv/tikv/issues/18399) @ [3ポイントシュート](https://github.com/3pointer)
        -   PITR [＃61318](https://github.com/pingcap/tidb/issues/61318) @ [3ポイントシュート](https://github.com/3pointer)中にメタデータの読み取りにかかる時間を短縮するために、タイムスタンプによるログ バックアップ メタデータ ファイルのフィルタリングをサポートします。

## バグ修正 {#bug-fixes}

-   TiDB

    -   `ALTER RANGE meta SET PLACEMENT POLICY` [＃60888](https://github.com/pingcap/tidb/issues/60888) @ [ノルーシュ](https://github.com/nolouch)のキー範囲が正しくない問題を修正しました
    -   インデックス作成中にワーカー数を減らすとタスクが[＃59267](https://github.com/pingcap/tidb/issues/59267) @ [D3ハンター](https://github.com/D3Hunter)でハングする可能性がある問題を修正しました
    -   `ADMIN SHOW DDL JOBS`文で行数が正しく表示されない問題を修正[＃59897](https://github.com/pingcap/tidb/issues/59897) @ [接線](https://github.com/tangenta)
    -   インデックス作成時にワーカー数を動的に調整するとデータ競合が発生する可能性がある問題を修正[＃59016](https://github.com/pingcap/tidb/issues/59016) @ [D3ハンター](https://github.com/D3Hunter)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `IMPORT INTO ... FROM SELECT`使用してTiFlash [＃58443](https://github.com/pingcap/tidb/issues/58443) @ [D3ハンター](https://github.com/D3Hunter)にデータをインポートするときにエラーが発生する可能性がある問題を修正しました
    -   `tidb_enable_dist_task`有効にすると TiDB のアップグレードが[＃54061](https://github.com/pingcap/tidb/issues/54061) @ [接線](https://github.com/tangenta)で失敗する問題を修正
    -   統計の不適切な例外処理により、バックグラウンドタスクがタイムアウトしたときにメモリ内の統計が誤って削除される問題を修正しました[＃57901](https://github.com/pingcap/tidb/issues/57901) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   TiDB分散実行フレームワーク（DXF） [＃58573](https://github.com/pingcap/tidb/issues/58573) @ [D3ハンター](https://github.com/D3Hunter)でインデックスを追加したときに行数が正しく更新されない問題を修正しました
    -   損失のあるDDL文[＃61455](https://github.com/pingcap/tidb/issues/61455) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)を実行した後にTiFlashクエリ結果が矛盾する問題を修正しました
    -   GCS [＃59754](https://github.com/pingcap/tidb/issues/59754) @ [D3ハンター](https://github.com/D3Hunter)で EOF エラーが発生したときに TiDB が再試行に失敗する問題を修正しました
    -   グローバルソート[＃59841](https://github.com/pingcap/tidb/issues/59841) @ [GMHDBJD](https://github.com/GMHDBJD)使用時の無効なKV範囲の問題を修正
    -   `CREATE INDEX IF NOT EXISTS`文[＃61265](https://github.com/pingcap/tidb/issues/61265) @ [CbcWestwolf](https://github.com/CbcWestwolf)を実行すると空のインデックス名が生成される問題を修正しました
    -   メタデータ ロック (MDL) を無効にした後、スキーマ バージョン[＃61210](https://github.com/pingcap/tidb/issues/61210) @ [wjhuang2016](https://github.com/wjhuang2016)更新に失敗して DDL 操作が停止する問題を修正しました。
    -   統計システムテーブル[＃60430](https://github.com/pingcap/tidb/issues/60430) @ [接線](https://github.com/tangenta)に非公開インデックスが表示される問題を修正しました
    -   HashAgg 演算子のメモリ追跡が正しく行われず、多数のエラー ログ[＃58822](https://github.com/pingcap/tidb/issues/58822) @ [xzhangxian1008](https://github.com/xzhangxian1008)が発生する問題を修正しました。
    -   HashAgg 演算子[＃61749](https://github.com/pingcap/tidb/issues/61749) @ [xzhangxian1008](https://github.com/xzhangxian1008)で、 `nil`バッファが`basePartialResult4GroupConcat`場合にディスクへの書き込み時にpanicが発生する問題を修正しました。
    -   集計式のエンコードロジックで誤った戻り値がクエリ実行中にpanicを引き起こす問題を修正[＃61735](https://github.com/pingcap/tidb/issues/61735) @ [ヤンケオ](https://github.com/YangKeao)
    -   HashJoin 演算子がメモリの過剰使用により Goroutine リークを引き起こす問題を修正[＃60926](https://github.com/pingcap/tidb/issues/60926) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   `IndexMerge`および`IndexLookUp`演算子の共有 KV リクエストがクエリ[＃60175](https://github.com/pingcap/tidb/issues/60175) @ [あなた06](https://github.com/you06)をプッシュダウンするときにデータ競合を引き起こす問題を修正しました。
    -   `_charset(xxx), _charset(xxx2), ...`を含む SQL 文が[＃58447](https://github.com/pingcap/tidb/issues/58447) @ [xhebox](https://github.com/xhebox)で異なるダイジェストを生成する問題を修正しました
    -   無効な UTF-8 文字を処理するときに TiDB がpanic可能性がある問題を修正[＃47521](https://github.com/pingcap/tidb/issues/47521) @ [定義2014](https://github.com/Defined2014)
    -   無効な夏時間（DST）タイムスタンプを挿入すると`0000-00-00` [＃61334](https://github.com/pingcap/tidb/issues/61334) @ [ミョンス](https://github.com/mjonss)になる問題を修正しました
    -   厳密なSQLモードで`INSERT IGNORE`使用して無効な夏時間のタイムスタンプを挿入すると、MySQL [＃61439](https://github.com/pingcap/tidb/issues/61439) @ [ミョンス](https://github.com/mjonss)と一致しないタイムスタンプになる問題を修正しました。
    -   頻繁なリージョンのマージにより TTL ジョブが[＃61512](https://github.com/pingcap/tidb/issues/61512) @ [ヤンケオ](https://github.com/YangKeao)で開始できなくなる問題を修正しました
    -   ネットワークプロトコルでTiDBが返す列の長さが`0`なる場合がある問題を修正しました`0`の場合、TiDBは各フィールドタイプのデフォルトの長さである[＃60503](https://github.com/pingcap/tidb/issues/60503) @ [xhebox](https://github.com/xhebox)を返します。
    -   ネットワークプロトコルで返される型`blob`が MySQL [＃60195](https://github.com/pingcap/tidb/issues/60195) @ [ドヴェーデン](https://github.com/dveeden)と一致しない問題を修正しました
    -   `CAST()`で返される長さが MySQL [＃61350](https://github.com/pingcap/tidb/issues/61350) @ [ヤンケオ](https://github.com/YangKeao)と互換性がない問題を修正しました
    -   `latin1_bin`の比較動作が`utf8mb4_bin`および`utf8_bin` [＃60701](https://github.com/pingcap/tidb/issues/60701) @ [ホーキングレイ](https://github.com/hawkingrei)と異なる問題を修正しました
    -   クエリが終了したときに悲観的ロックが残る可能性がある問題を修正[＃61454](https://github.com/pingcap/tidb/issues/61454) @ [ジグアン](https://github.com/zyguan)
    -   1回のリクエストでPDからあまりにも多くのリージョンをロードするため、TiDBが大規模なクエリを実行するとエラーが発生する問題を修正[＃1704](https://github.com/tikv/client-go/issues/1704) @ [あなた06](https://github.com/you06)

-   TiKV

    -   TiKV が正常なシャットダウン中に進行中の手動圧縮タスクを終了できない問題を修正[＃18396](https://github.com/tikv/tikv/issues/18396) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   クラスタのアップグレード後にデフォルトのリージョンサイズが予期せず変更される問題を修正[＃18503](https://github.com/tikv/tikv/issues/18503) @ [LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVがクライアントが[＃18079](https://github.com/tikv/tikv/issues/18079) @ [エキシウム](https://github.com/ekexium)をデコードできない圧縮アルゴリズムを使用する可能性がある問題を修正しました
    -   Titan を無効にした後に BLOB インデックスがスナップショットの適用エラーを引き起こす可能性がある問題を修正[＃18434](https://github.com/tikv/tikv/issues/18434) @ [v01dstar](https://github.com/v01dstar)
    -   スローログ[＃18561](https://github.com/tikv/tikv/issues/18561) @ [LykxSassinator](https://github.com/LykxSassinator)の`StoreMsg`ログエントリの誤解を招く説明を修正
    -   TiKV が高同時実行[＃18452](https://github.com/tikv/tikv/issues/18452) @ [ヒビシェン](https://github.com/hbisheng)で過剰な SST 取り込み要求を許可する問題を修正
    -   ロックスキャン[＃16818](https://github.com/tikv/tikv/issues/16818) @ [cfzjywxk](https://github.com/cfzjywxk)中に重複した結果によりTiKVがpanic可能性がある問題を修正

-   PD

    -   低速ノード検出メカニズム[＃9384](https://github.com/tikv/pd/issues/9384) @ [rleungx](https://github.com/rleungx)で`recovery-duration`有効にならない問題を修正
    -   クラスタのアップグレード後にEvict Leaderスケジューラが誤って一時停止される可能性がある問題を修正[＃9416](https://github.com/tikv/pd/issues/9416) @ [rleungx](https://github.com/rleungx)
    -   TiDBダッシュボードTCP接続を不適切に閉じるとPDゴルーチンリークが発生する可能性がある問題を修正[＃9402](https://github.com/tikv/pd/issues/9402) @ [バウリン](https://github.com/baurine)
    -   新しく追加された TiKV ノードが[＃9145](https://github.com/tikv/pd/issues/9145) @ [バッファフライ](https://github.com/bufferflies)にスケジュールされない可能性がある問題を修正しました

-   TiFlash

    -   `((NULL))`形式で式インデックスを作成するとTiFlash が[＃9891](https://github.com/pingcap/tiflash/issues/9891) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)でpanicになる問題を修正しました
    -   Join 演算子内の不整合なミューテックスにより、特定の環境でTiFlashがクラッシュする問題を修正しました[＃10163](https://github.com/pingcap/tiflash/issues/10163) @ [ウィンドトーカー](https://github.com/windtalker)
    -   リソース制御の低トークン信号が欠落するとクエリスロットリング[＃10137](https://github.com/pingcap/tiflash/issues/10137) @ [グオシャオゲ](https://github.com/guo-shaoge)が発生する問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   ブレークポイントリカバリ[＃54316](https://github.com/pingcap/tidb/issues/54316) @ [リーヴルス](https://github.com/Leavrth)中にstorageノードの使用可能スペースが不必要に再チェックされる問題を修正
        -   HTTP/2 GOAWAYエラーが発生したときに外部storageからのデータインポートが自動的に再試行されない問題を修正[＃60143](https://github.com/pingcap/tidb/issues/60143) @ [ヨッヘンrh](https://github.com/joechenrh)
        -   インポートモードの切り替えにより復元中に発生する`keepalive watchdog timedout`エラーを修正[＃18541](https://github.com/tikv/tikv/issues/18541) @ [リーヴルス](https://github.com/Leavrth)
        -   大量のデータを転送するときに Azure Blob Storage へのログ バックアップのアップロードが遅くなる問題を修正[＃18410](https://github.com/tikv/tikv/issues/18410) @ [ユジュンセン](https://github.com/YuJuncen)
        -   `-f` [＃61592](https://github.com/pingcap/tidb/issues/61592) @ [リドリスR](https://github.com/RidRisR)でテーブルをフィルタリングするときに、 BR が対応するテーブルがクラスター内に存在するかどうかをチェックしない問題を修正しました。
        -   PITRが3072バイトを超えるインデックスの復元に失敗する問題を修正[＃58430](https://github.com/pingcap/tidb/issues/58430) @ [ユジュンセン](https://github.com/YuJuncen)
        -   フルバックアップ[＃58587](https://github.com/pingcap/tidb/issues/58587) @ [3ポイントシュート](https://github.com/3pointer)中に RangeTree 結果がメモリを非効率的に消費する問題を修正しました

    -   TiCDC

        -   仮想列を含むテーブルでイベントフィルタ式を評価するとpanicが発生する可能性がある問題を修正[＃12206](https://github.com/pingcap/tiflow/issues/12206) @ [リデジュ](https://github.com/lidezhu)
        -   古いストア ID [＃12162](https://github.com/pingcap/tiflow/issues/12162) @ [3エースショーハンド](https://github.com/3AceShowHand)が原因で、同じ IP アドレス上の TiKV ノードをスケールインまたはスケールアウトした後に、解決された ts ラグが増加し続ける問題を修正しました。
        -   ディスパッチャ構成[＃12103](https://github.com/pingcap/tiflow/issues/12103) @ [wk989898](https://github.com/wk989898)における列名とインデックス名の大文字と小文字を区別するマッチングの問題を修正しました
        -   Debeziumプロトコルで`column-selector`設定するとpanic[＃12208](https://github.com/pingcap/tiflow/issues/12208) @ [wk989898](https://github.com/wk989898)が発生する可能性がある問題を修正しました

    -   TiDB Lightning

        -   TiKVへのRPCリクエストが[＃60143](https://github.com/pingcap/tidb/issues/60143) @ [ヨッヘンrh](https://github.com/joechenrh)でタイムアウトするとTiDB Lightningが`context deadline exceeded`エラーを返す問題を修正しました
