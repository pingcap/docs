---
title: TiDB 8.5.3 Release Notes
summary: TiDB 8.5.3における互換性の変更点、改善点、およびバグ修正についてご確認ください。
---

# TiDB 8.5.3 リリースノート {#tidb-8-5-3-release-notes}

発売日：2025年8月14日

TiDBバージョン：8.5.3

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb)| [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   KVDBとRaftDBが別々のディスクにデプロイされているシナリオで、KVDBディスクI/Oジッター検出の感度を向上させるため、TiKV構成項目[`raftstore.inspect-kvdb-interval`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#inspect-kvdb-interval-new-in-v812)のデフォルト値を`2s`から`100ms`に変更します。 [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
-   [コストモデル](/cost-model.md)による内部使用のために次のシステム変数を追加します。これらの変数を変更することは推奨さ**れません**: [`tidb_opt_hash_agg_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_hash_agg_cost_factor-new-in-v853) 、 [`tidb_opt_hash_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_hash_join_cost_factor-new-in-v853) 、 [`tidb_opt_index_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_join_cost_factor-new-in-v853) 、 [`tidb_opt_index_lookup_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_lookup_cost_factor-new-in-v853) 、 [`tidb_opt_index_merge_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_merge_cost_factor-new-in-v853) 、 [`tidb_opt_index_reader_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_reader_cost_factor-new-in-v853) 、 [`tidb_opt_index_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_index_scan_cost_factor-new-in-v853) 、 [`tidb_opt_limit_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_limit_cost_factor-new-in-v853) 、 [`tidb_opt_merge_join_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_merge_join_cost_factor-new-in-v853) 、 [`tidb_opt_sort_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_sort_cost_factor-new-in-v853) 、 [`tidb_opt_stream_agg_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_stream_agg_cost_factor-new-in-v853) 、 [`tidb_opt_table_full_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_full_scan_cost_factor-new-in-v853) 、 [`tidb_opt_table_range_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_range_scan_cost_factor-new-in-v853) 、 [`tidb_opt_table_reader_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_reader_cost_factor-new-in-v853) 、 [`tidb_opt_table_rowid_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_rowid_cost_factor-new-in-v853) 、 [`tidb_opt_table_tiflash_scan_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_table_tiflash_scan_cost_factor-new-in-v853) 、および[`tidb_opt_topn_cost_factor`](https://docs.pingcap.com/tidb/v8.5/system-variables/#tidb_opt_topn_cost_factor-new-in-v853) [#60357](https://github.com/pingcap/tidb/issues/60357) @[terry1purcell](https://github.com/terry1purcell)
-   [テレメトリー](https://docs.pingcap.com/tidb/v8.5/telemetry)機能を再導入します。ただし、テレメトリ関連の情報をローカルに記録するだけであり、ネットワーク経由で PingCAP にデータを送信することはなくなりました [#61766](https://github.com/pingcap/tidb/issues/61766) @[Defined2014](https://github.com/Defined2014)

## 改善点 {#improvements}

-   TiDB

    -   統計情報が完全に TopN で構成され、対応するテーブル統計情報の変更された行数がゼロでない場合、TopN に到達しない等価条件の推定結果を 0 から 1 に調整します。 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    -   グローバルソートを使用した一意インデックスの追加パフォーマンスを改善し、重複する一意インデックスを追加する際のエラーメッセージを改善します [#61689](https://github.com/pingcap/tidb/issues/61689) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   `IMPORT INTO`がグローバルソートを有効にしている場合、TiKV のインポートモードへの切り替えを無効にする [#60361](https://github.com/pingcap/tidb/issues/60361) @[D3Hunter](https://github.com/D3Hunter)
    -   インデックス追加中の TiKV への書き込み速度を監視するためのモニタリング メトリックを追加 [#60925](https://github.com/pingcap/tidb/issues/60925) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   `merge sort`サブタスクのスケジューリングロジックを最適化してソートパフォーマンスを向上させる [#60375](https://github.com/pingcap/tidb/issues/60375) @[tangenta](https://github.com/tangenta)
    -   外部キーを持つ多数のテーブルを作成する際のテーブル作成を高速化し、メモリ使用効率を最適化する [#61126](https://github.com/pingcap/tidb/issues/61126) @[GMHDBJD](https://github.com/GMHDBJD)
    -   `information_schema.tables`テーブル [#62020](https://github.com/pingcap/tidb/issues/62020)の読み取りパフォーマンスを改善します @[tangenta](https://github.com/tangenta)
    -   データインポート時のリージョン分割とデータ取り込みのためのフロー制御インターフェースを追加 [#61553](https://github.com/pingcap/tidb/issues/61553) @[tangenta](https://github.com/tangenta)
    -   IndexScan のプラン構築プロセスを最適化し、 `fmt.Sprintf()`呼び出しを削減します [#56649](https://github.com/pingcap/tidb/issues/56649) @[crazycs520](https://github.com/crazycs520)
    -   インデックスを使用したグローバルソート時にマージソート段階の監視メトリクスを追加する [#61025](https://github.com/pingcap/tidb/issues/61025) @[fzzf678](https://github.com/fzzf678)
    -   `IndexLookup`オペレーターが`context canceled`エラーに遭遇したときに、冗長なログエントリを削除します [#61072](https://github.com/pingcap/tidb/issues/61072) @[yibin87](https://github.com/yibin87)
    -   `tidb_replica_read`を`closest-adaptive`に設定した場合のパフォーマンスを改善します [#61745](https://github.com/pingcap/tidb/issues/61745) @[you06](https://github.com/you06)
    -   大規模クラスタにおける監視メトリクスデータの量を減らすことで運用コストを削減する [#59990](https://github.com/pingcap/tidb/issues/59990) @[zimulala](https://github.com/zimulala)

-   ティクヴ

    -   フォアグラウンド書き込みをブロックせずにSSTファイルを取り込むことをサポートし、レイテンシーの影響を軽減します [#18081](https://github.com/tikv/tikv/issues/18081) @[hhwyt](https://github.com/hhwyt)
    -   フローコントローラによって引き起こされるパフォーマンスのジッターを軽減します [#18625](https://github.com/tikv/tikv/issues/18625) @[hhwyt](https://github.com/hhwyt)
    -   TiDB での`ADD INDEX`操作中のテールレイテンシーを最適化 [#18081](https://github.com/tikv/tikv/issues/18081) @[overvenus](https://github.com/overvenus)
    -   Raftstoreでの`CompactedEvent`の処理を​​最適化し`split-check`ワーカーに移動することで、メインのRaftstoreスレッドでのブロッキングを軽減します [#18532](https://github.com/tikv/tikv/issues/18532) @[LykxSassinator](https://github.com/LykxSassinator)
    -   SST の取り込みが遅すぎる場合のみ`SST ingest is experiencing slowdowns`をログに記録し、パフォーマンスのジッターを回避するために`get_sst_key_ranges`の呼び出しをスキップします [#18549](https://github.com/tikv/tikv/issues/18549) @[LykxSassinator](https://github.com/LykxSassinator)
    -   KvDBとRaftDBが別々のマウントパスを使用する場合のKvDBディスクのI/Oジッター検出メカニズムを最適化する [#18463](https://github.com/tikv/tikv/issues/18463) @[LykxSassinator](https://github.com/LykxSassinator)
    -   Raft Engineの`fetch_entries_to`のパフォーマンスを最適化して競合を減らし、混合ワークロード下でのパフォーマンスを向上させます [#18605](https://github.com/tikv/tikv/issues/18605) @[LykxSassinator](https://github.com/LykxSassinator)
    -   リクエストのレイテンシーへの影響を軽減するために、残留データのクリーンアップメカニズムを最適化します [#18107](https://github.com/tikv/tikv/issues/18107) @[LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   GO ランタイム関連の監視メトリクスを Prometheus に追加 [#8931](https://github.com/tikv/pd/issues/8931) @[bufferflies](https://github.com/bufferflies)
    -   スローノードリーダーの強制退去後のリカバリ時間を600秒から900秒（15分）に延長 [#9329](https://github.com/tikv/pd/issues/9329) @[rleungx](https://github.com/rleungx)

-   TiFlash

    -   storageスナップショット取得時の最大リトライ回数を増やし、大規模テーブルのクエリの安定性を向上 [#10300](https://github.com/pingcap/tiflash/issues/10300) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   ワイドテーブルシナリオにおけるTiFlash OOM リスクの可観測性を強化 [#10272](https://github.com/pingcap/tiflash/issues/10272) @[JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   PITR中のインデックス修復速度を向上させるため、インデックスを同時修復する [#59158](https://github.com/pingcap/tidb/issues/59158) @[Leavrth](https://github.com/Leavrth)
        -   TiKV のダウンロード API は、バックアップ ファイルをダウンロードする際に、特定の時間範囲内のデータをフィルタリングして除外することをサポートしています。これにより、復元中に古いバージョンまたは将来のデータ バージョンがインポートされるのを回避できます [#18399](https://github.com/tikv/tikv/issues/18399) @[3pointer](https://github.com/3pointer)
        -   タイムスタンプによるログ バックアップ メタデータ ファイルのフィルタリングをサポートし、PITR [#61318](https://github.com/pingcap/tidb/issues/61318) @[3pointer](https://github.com/3pointer)中のメタデータの読み取りにかかる時間を削減します

## バグ修正 {#bug-fixes}

-   TiDB

    -   `ALTER RANGE meta SET PLACEMENT POLICY`のキー範囲が間違っている問題を修正 [#60888](https://github.com/pingcap/tidb/issues/60888) @[nolouch](https://github.com/nolouch)
    -   インデックス作成中にワーカー数を減らすとタスクがハングアップする可能性がある問題を修正 [#59267](https://github.com/pingcap/tidb/issues/59267) @[D3Hunter](https://github.com/D3Hunter)
    -   `ADMIN SHOW DDL JOBS`ステートメントで行数が正しく表示されない問題を修正 [#59897](https://github.com/pingcap/tidb/issues/59897) @[tangenta](https://github.com/tangenta)
    -   インデックス作成中にワーカー数を動的に調整するとデータ競合が発生する可能性がある問題を修正 [#59016](https://github.com/pingcap/tidb/issues/59016) @[D3Hunter](https://github.com/D3Hunter)
    -   Grafana の**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    -   `IMPORT INTO ... FROM SELECT`を使用してTiFlashにデータをインポートする際にエラーが発生する可能性がある問題を修正しました [#58443](https://github.com/pingcap/tidb/issues/58443) @[D3Hunter](https://github.com/D3Hunter)
    -   `tidb_enable_dist_task`を有効にすると TiDB アップグレードが失敗する問題を修正 [#54061](https://github.com/pingcap/tidb/issues/54061) @[tangenta](https://github.com/tangenta)
    -   バックグラウンドタスクがタイムアウトした際に、統計情報の例外処理が不適切であるためにメモリ内の統計情報が誤って削除される問題を修正 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    -   TiDB Distributed eXecution Framework (DXF) でインデックスを追加した際に、行数が正しく更新されない問題を修正しました [#58573](https://github.com/pingcap/tidb/issues/58573) @[D3Hunter](https://github.com/D3Hunter)
    -   非可逆 DDL ステートメントを実行した後にTiFlashクエリの結果が矛盾する問題を修正 [#61455](https://github.com/pingcap/tidb/issues/61455) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   TiDBがGCSでEOFエラーに遭遇した際に再試行に失敗する問題を修正 [#59754](https://github.com/pingcap/tidb/issues/59754) @[D3Hunter](https://github.com/D3Hunter)
    -   グローバルソート使用時の無効なKV範囲の問題を修正 [#59841](https://github.com/pingcap/tidb/issues/59841) @[GMHDBJD](https://github.com/GMHDBJD)
    -   `CREATE INDEX IF NOT EXISTS`ステートメントの実行時に空のインデックス名が生成される問題を修正 [#61265](https://github.com/pingcap/tidb/issues/61265) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   メタデータロック（MDL）を無効にした後、スキーマバージョンの更新に失敗してDDL操作が停止する問題を修正しました [#61210](https://github.com/pingcap/tidb/issues/61210) @[wjhuang2016](https://github.com/wjhuang2016)
    -   非公開インデックスが統計システムテーブルに表示される問題を修正 [#60430](https://github.com/pingcap/tidb/issues/60430) @[tangenta](https://github.com/tangenta)
    -   HashAgg演算子におけるメモリ追跡の誤りにより、大量のエラーログが発生する問題を修正しました [#58822](https://github.com/pingcap/tidb/issues/58822) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   HashAgg オペレーターでディスク スピル中に`nil`内の`basePartialResult4GroupConcat`バッファがpanicを引き起こす問題を修正しました [#61749](https://github.com/pingcap/tidb/issues/61749) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   集計式のエンコードロジックにおける誤った戻り値がクエリ実行中にpanicを引き起こす問題を修正 [#61735](https://github.com/pingcap/tidb/issues/61735) @[YangKeao](https://github.com/YangKeao)
    -   HashJoin演算子がメモリの過剰使用によりゴルーチンリークを引き起こす問題を修正 [#60926](https://github.com/pingcap/tidb/issues/60926) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `IndexMerge`および`IndexLookUp`オペレーターで共有 KV リクエストがクエリのプッシュダウン時にデータ競合を引き起こす問題を修正しました [#60175](https://github.com/pingcap/tidb/issues/60175) @[you06](https://github.com/you06)
    -   `_charset(xxx), _charset(xxx2), ...`を含む SQL ステートメントが異なるダイジェストを生成する問題を修正 [#58447](https://github.com/pingcap/tidb/issues/58447) @[xhebox](https://github.com/xhebox)
    -   無効な UTF-8 文字を処理するときに TiDB がpanic可能性がある問題を修正 [#47521](https://github.com/pingcap/tidb/issues/47521) @[Defined2014](https://github.com/Defined2014)
    -   無効な夏時間 (DST) タイムスタンプを挿入すると`0000-00-00`になる問題を修正 [#61334](https://github.com/pingcap/tidb/issues/61334) @[mjonss](https://github.com/mjonss)
    -   `INSERT IGNORE`を使用して厳密なSQLモードで無効な夏時間タイムスタンプを挿入すると、MySQLと矛盾するタイムスタンプが生成される問題を修正しました [#61439](https://github.com/pingcap/tidb/issues/61439) @[mjonss](https://github.com/mjonss)
    -   リージョンのマージが頻繁に行われるとTTLジョブの開始が妨げられる問題を修正 [#61512](https://github.com/pingcap/tidb/issues/61512) @[YangKeao](https://github.com/YangKeao)
    -   TiDB がネットワーク プロトコルで返す列の長さが`0`になる可能性がある問題を修正します。もし`0`であれば、TiDB は各フィールド タイプのデフォルトの長さを返します。 [#60503](https://github.com/pingcap/tidb/issues/60503) @[xhebox](https://github.com/xhebox)
    -   ネットワークプロトコルにおける`blob`の戻り値の型が MySQL と一致しない問題を修正しました [#60195](https://github.com/pingcap/tidb/issues/60195) @[dveeden](https://github.com/dveeden)
    -   `CAST()`が返す長さが MySQL と互換性がない問題を修正 [#61350](https://github.com/pingcap/tidb/issues/61350) @[YangKeao](https://github.com/YangKeao)
    -   `latin1_bin`の比較動作が`utf8mb4_bin`および`utf8_bin`と異なる問題を修正 [#60701](https://github.com/pingcap/tidb/issues/60701) @[hawkingrei](https://github.com/hawkingrei)
    -   クエリが終了したときに悲観的ロックが残る可能性がある問題を修正 [#61454](https://github.com/pingcap/tidb/issues/61454) @[zyguan](https://github.com/zyguan)
    -   TiDBがPDから単一のリクエストでリージョンを多数ロードしたために大規模なクエリを実行する際にエラーが発生する問題を修正しました [#1704](https://github.com/tikv/client-go/issues/1704) @[you06](https://github.com/you06)

-   ティクヴ

    -   TiKV が正常シャットダウン中に進行中の手動圧縮タスクを終了できない問題を修正 [#18396](https://github.com/tikv/tikv/issues/18396) @[LykxSassinator](https://github.com/LykxSassinator)
    -   クラスターのアップグレード後にデフォルトのリージョンサイズが予期せず変更される問題を修正 [#18503](https://github.com/tikv/tikv/issues/18503) @[LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVがクライアントがデコードできない圧縮アルゴリズムを使用する可能性がある問題を修正 [#18079](https://github.com/tikv/tikv/issues/18079) @[ekexium](https://github.com/ekexium)
    -   Titanが無効化された後に、ブロブインデックスが原因でスナップショットの適用が失敗する可能性がある問題を修正しました [#18434](https://github.com/tikv/tikv/issues/18434) @[v01dstar](https://github.com/v01dstar)
    -   スローログの`StoreMsg`ログエントリの誤解を招く説明を修正 [#18561](https://github.com/tikv/tikv/issues/18561) @[LykxSassinator](https://github.com/LykxSassinator)
    -   TiKVが高同時実行時に過剰なSST取り込みリクエストを許可してしまう問題を修正 [#18452](https://github.com/tikv/tikv/issues/18452) @[hbisheng](https://github.com/hbisheng)
    -   ロックスキャン中に重複した結果が原因でTiKVがpanic可能性がある問題を修正 [#16818](https://github.com/tikv/tikv/issues/16818) @[cfzjywxk](https://github.com/cfzjywxk)

-   PD

    -   `recovery-duration`が低速ノード検出メカニズムで有効にならない問題を修正 [#9384](https://github.com/tikv/pd/issues/9384) @[rleungx](https://github.com/rleungx)
    -   クラスタのアップグレード後に Evict Leaderスケジューラが誤って一時停止される可能性がある問題を修正しました [#9416](https://github.com/tikv/pd/issues/9416) @[rleungx](https://github.com/rleungx)
    -   TiDB DashboardのTCP接続を不適切に閉じるとPDゴルーチンリークが発生する問題を修正しました [#9402](https://github.com/tikv/pd/issues/9402) @[baurine](https://github.com/baurine)
    -   新しく追加された TiKV ノードがスケジュールに失敗する可能性がある問題を修正 [#9145](https://github.com/tikv/pd/issues/9145) @[bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   `((NULL))`の形式で式インデックスを作成するとTiFlash がpanicになる問題を修正 [#9891](https://github.com/pingcap/tiflash/issues/9891) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   Join オペレーターのミューテックスの位置がずれていると、特定の環境でTiFlashがクラッシュする問題を修正 [#10163](https://github.com/pingcap/tiflash/issues/10163) @[windtalker](https://github.com/windtalker)
    -   リソース制御の低トークンシグナルが欠落するとクエリのスロットリングが発生する問題を修正 [#10137](https://github.com/pingcap/tiflash/issues/10137) @[guo-shaoge](https://github.com/guo-shaoge)

-   ツール

    -   バックアップと復元 (BR)

        -   ブレークポイントリカバリ中にstorageノードの空き容量が不必要に再チェックされる問題を修正 [#54316](https://github.com/pingcap/tidb/issues/54316) @[Leavrth](https://github.com/Leavrth)
        -   HTTP/2 GOAWAY エラーが発生した際に、外部storageからのデータインポートが自動的に再試行されない問題を修正 [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
        -   インポートモードの切り替えにより復元中に発生する`keepalive watchdog timedout`エラーを修正 [#18541](https://github.com/tikv/tikv/issues/18541) @[Leavrth](https://github.com/Leavrth)
        -   大量のデータを転送する際に、ログバックアップのAzure Blob Storageへのアップロードが遅くなる問題を修正しました [#18410](https://github.com/tikv/tikv/issues/18410) @[YuJuncen](https://github.com/YuJuncen)
        -   `-f`でテーブルをフィルタリングする際に、 BRが対応するテーブルがクラスタ内に存在するかどうかをチェックしない問題を修正 [#61592](https://github.com/pingcap/tidb/issues/61592) @[RidRisR](https://github.com/RidRisR)
        -   PITR が 3072 バイトを超えるインデックスの復元に失敗する問題を修正 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)
        -   RangeTree の結果が完全バックアップ中にメモリを非効率的に消費する問題を修正 [#58587](https://github.com/pingcap/tidb/issues/58587) @[3pointer](https://github.com/3pointer)

    -   TiCDC

        -   仮想列を含むテーブルでイベントフィルタ式を評価するとpanicが発生する可能性がある問題を修正 [#12206](https://github.com/pingcap/tiflow/issues/12206) @[lidezhu](https://github.com/lidezhu)
        -   古いストア ID が原因で、同じ IP アドレス上の TiKV ノードをスケールインまたはスケールアウトした後、解決された ts ラグが増加し続ける問題を修正 [#12162](https://github.com/pingcap/tiflow/issues/12162) @[3AceShowHand](https://github.com/3AceShowHand)
        -   ディスパッチャ構成における列名とインデックス名の大文字小文字を区別するマッチングの問題を修正 [#12103](https://github.com/pingcap/tiflow/issues/12103) @[wk989898](https://github.com/wk989898)
        -   Debeziumプロトコルで`column-selector`を設定するとpanicが発生する可能性がある問題を修正しました [#12208](https://github.com/pingcap/tiflow/issues/12208) @[wk989898](https://github.com/wk989898)

    -   TiDB Lightning

        -   TiDB LightningがTiKVへのRPCリクエストがタイムアウトした際に`context deadline exceeded`エラーを返す問題を修正 [#60143](https://github.com/pingcap/tidb/issues/60143) @[joechenrh](https://github.com/joechenrh)
