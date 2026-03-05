---
title: TiDB 7.5.6 Release Notes
summary: TiDB 7.5.6 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 7.5.6 リリースノート {#tidb-7-5-6-release-notes}

発売日：2025年3月14日

TiDB バージョン: 7.5.6

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v7.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v7.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   openEuler 22.03 LTS SP3/SP4 オペレーティングシステムをサポートします。詳細については、 [OSおよびプラットフォームの要件](https://docs.pingcap.com/tidb/v7.5/hardware-and-software-requirements#os-and-platform-requirements)参照してください。

## 改善点 {#improvements}

-   TiDB

    -   統計情報がすべて TopN で構成され、対応するテーブル統計の変更された行数が 0 以外である場合に、TopN にヒットしない等価条件の推定結果を 0 から 1 に調整します[＃47400](https://github.com/pingcap/tidb/issues/47400) @ [テリー・パーセル](https://github.com/terry1purcell)
    -   タイムスタンプの有効性チェックを強化する[＃57786](https://github.com/pingcap/tidb/issues/57786) @ [ミョンケミンタ](https://github.com/MyonKeminta)
    -   TTLテーブルと関連する統計収集タスクのGCの実行を所有者ノードに制限することで、オーバーヘッド[＃59357](https://github.com/pingcap/tidb/issues/59357) @ [lcwangchao](https://github.com/lcwangchao)を削減します。

-   TiKV

    -   無効な`max_ts`更新の検出メカニズムを追加[＃17916](https://github.com/tikv/tikv/issues/17916) @ [エキシウム](https://github.com/ekexium)
    -   ピアのスローログを追加し、メッセージ[＃16600](https://github.com/tikv/tikv/issues/16600) @ [コナー1996](https://github.com/Connor1996)を保存します
    -   ログの適用を待つために TiKV を再起動するときに発生する不安定なアクセス遅延を最適化し、TiKV [＃15874](https://github.com/tikv/tikv/issues/15874) @ [LykxSassinator](https://github.com/LykxSassinator)の安定性を向上しました。

-   TiFlash

    -   TLS を有効にした後に証明書を更新することでTiFlash がpanic可能性がある問題を軽減します[＃8535](https://github.com/pingcap/tiflash/issues/8535) @ [ウィンドトーカー](https://github.com/windtalker)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップパフォーマンスを向上させるために、フルバックアップ中のテーブルレベルのチェックサム計算をデフォルトで無効にする（ `--checksum=false` ） [＃56373](https://github.com/pingcap/tidb/issues/56373) @ [トリスタン1900](https://github.com/Tristan1900)
        -   非完全リストア[＃55087](https://github.com/pingcap/tidb/issues/55087) @ [リドリスR](https://github.com/RidRisR)の場合、ターゲット クラスタに同じ名前のテーブルが含まれているかどうかを確認するチェックを追加します。

    -   TiDB Lightning

        -   CSV ファイルを解析するときに行幅チェックを追加して、OOM の問題を防ぐ[＃58590](https://github.com/pingcap/tidb/issues/58590) @ [D3ハンター](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `IndexMerge` [＃58476](https://github.com/pingcap/tidb/issues/58476) @ [ホーキングレイ](https://github.com/hawkingrei)を構築するときに一部の述語が失われる可能性がある問題を修正しました
    -   ビュー[＃53175](https://github.com/pingcap/tidb/issues/53175) @ [ミョンス](https://github.com/mjonss)のステートメントに`ONLY_FULL_GROUP_BY`設定が反映されない問題を修正しました
    -   同じ名前のビューを2つ作成してもエラーが報告されない問題を修正[＃58769](https://github.com/pingcap/tidb/issues/58769) @ [天菜まお](https://github.com/tiancaiamao)
    -   `BIT`型から`CHAR`型にデータを変換すると TiKV パニック[＃56494](https://github.com/pingcap/tidb/issues/56494) @ [lcwangchao](https://github.com/lcwangchao)が発生する可能性がある問題を修正しました
    -   ハートビートを失った TTL ジョブが他のジョブのハートビート[＃57915](https://github.com/pingcap/tidb/issues/57915) @ [ヤンケオ](https://github.com/YangKeao)の取得をブロックする問題を修正しました
    -   不一致な値タイプとタイプ変換エラーを含む条件`IN`使用してパーティション テーブルをクエリすると、誤ったクエリ結果[＃54746](https://github.com/pingcap/tidb/issues/54746) @ [ミョンス](https://github.com/mjonss)が発生する問題を修正しました。
    -   `BIT`列目のデフォルト値が正しくない問題を修正[＃57301](https://github.com/pingcap/tidb/issues/57301) @ [ヤンケオ](https://github.com/YangKeao)
    -   Prepareプロトコルで、クライアントがUTF8以外の文字セット[＃58870](https://github.com/pingcap/tidb/issues/58870) @ [xhebox](https://github.com/xhebox)を使用するとエラーが発生する問題を修正しました。
    -   `CREATE VIEW`ステートメントで変数またはパラメータを使用してもエラーが報告されない問題を修正[＃53176](https://github.com/pingcap/tidb/issues/53176) @ [ミョンス](https://github.com/mjonss)
    -   統計ファイルに NULL 値[＃53966](https://github.com/pingcap/tidb/issues/53966) @ [キング・ディラン](https://github.com/King-Dylan)が含まれている場合、統計を手動でロードすると失敗する可能性がある問題を修正しました。
    -   `information_schema.cluster_slow_query`テーブルをクエリするときに、時間フィルターが追加されていない場合、最新のスローログファイルのみがクエリされる問題を修正しました[＃56100](https://github.com/pingcap/tidb/issues/56100) @ [crazycs520](https://github.com/crazycs520)
    -   一時テーブルをクエリすると、場合によっては予期しない TiKV リクエストがトリガーされる可能性がある問題を修正しました[＃58875](https://github.com/pingcap/tidb/issues/58875) @ [天菜まお](https://github.com/tiancaiamao)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `tidb_ttl_delete_rate_limit` [＃58484](https://github.com/pingcap/tidb/issues/58484) @ [lcwangchao](https://github.com/lcwangchao)を変更するときに一部の TTL ジョブがハングする可能性がある問題を修正しました
    -   統計の不適切な例外処理により、バックグラウンドタスクがタイムアウトしたときにメモリ内の統計が誤って削除される問題を修正しました[＃57901](https://github.com/pingcap/tidb/issues/57901) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   `cluster_slow_query table`クエリするときに`ORDER BY`使用すると、順序付けられていない結果[＃51723](https://github.com/pingcap/tidb/issues/51723) @ [定義2014](https://github.com/Defined2014)が生成される可能性がある問題を修正しました。
    -   仮想生成列の依存関係に属性`ON UPDATE`持つ列が含まれている場合、更新された行のデータとそのインデックスデータが不整合になる可能性がある問題を修正しました[＃56829](https://github.com/pingcap/tidb/issues/56829) @ [ヨッヘンrh](https://github.com/joechenrh)
    -   TiDBハートビートが失われた場合に TTL ジョブをキャンセルできない問題を修正[＃57784](https://github.com/pingcap/tidb/issues/57784) @ [ヤンケオ](https://github.com/YangKeao)
    -   パラメータが`Enum` 、または`Set`型の場合、 `Conv()`関数はTiKV [＃51877](https://github.com/pingcap/tidb/issues/51877) @ [イービン87](https://github.com/yibin87)にプッシュダウンされなくなりました`Bit`
    -   分散storageおよびコンピューティングアーキテクチャのTiFlashノードを含むクラスターで`ALTER TABLE ... PLACEMENT POLICY ...`実行した後、リージョンピアが誤ってTiFlashコンピューティングノード[＃58633](https://github.com/pingcap/tidb/issues/58633) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に追加される可能性がある問題を修正しました。
    -   DDL所有者が[＃52747](https://github.com/pingcap/tidb/issues/52747) @ [D3ハンター](https://github.com/D3Hunter)に変更されるとジョブステータスが上書きされる問題を修正
    -   ハッシュパーティションテーブルで条件`is null`クエリを実行するとpanic[＃58374](https://github.com/pingcap/tidb/issues/58374) @ [定義2014](https://github.com/Defined2014/)が発生する問題を修正
    -   生成された列[＃58475](https://github.com/pingcap/tidb/issues/58475) @ [ヨッヘンrh](https://github.com/joechenrh)を含むパーティション テーブルをクエリするときにエラーが発生する問題を修正しました。
    -   TTLジョブが無視されたり、複数回処理されたりする問題を修正[＃59347](https://github.com/pingcap/tidb/issues/59347) @ [ヤンケオ](https://github.com/YangKeao)
    -   交換パーティションの誤った判断により実行エラーが発生する問題を修正[＃59534](https://github.com/pingcap/tidb/issues/59534) @ [ミョンス](https://github.com/mjonss)
    -   `tidb_audit_log`変数を複数レベルの相対パスで設定すると、ログディレクトリ[＃58971](https://github.com/pingcap/tidb/issues/58971) @ [lcwangchao](https://github.com/lcwangchao)でエラーが発生する問題を修正しました。
    -   Join の等価条件の両側のデータ型が異なると、 TiFlash [＃59877](https://github.com/pingcap/tidb/issues/59877) @ [イービン87](https://github.com/yibin87)で誤った結果が生じる可能性がある問題を修正しました。

-   TiKV

    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602)対[LykxSassinator](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました
    -   タイムロールバックにより異常なRocksDBフロー制御が発生し、パフォーマンスジッター[＃17995](https://github.com/tikv/tikv/issues/17995) @ [LykxSassinator](https://github.com/LykxSassinator)が発生する可能性がある問題を修正しました。
    -   1フェーズコミット（1PC）のみが有効で、非同期コミットが有効になっていない場合に、最後に書き込まれたデータが読み取れない可能性がある問題を修正[＃18117](https://github.com/tikv/tikv/issues/18117) @ [ジグアン](https://github.com/zyguan)
    -   TiKVがブラジルとエジプトのタイムゾーンを誤って変換する問題を修正[＃16220](https://github.com/tikv/tikv/issues/16220) @ [金星の上](https://github.com/overvenus)
    -   GCワーカーに高負荷がかかったときにデッドロックが発生する可能性がある問題を修正[＃18214](https://github.com/tikv/tikv/issues/18214) @ [ジグアン](https://github.com/zyguan)
    -   ディスクストールによりリーダーの移行が妨げられ、パフォーマンスジッター[＃17363](https://github.com/tikv/tikv/issues/17363) @ [hhwyt](https://github.com/hhwyt)が発生する問題を修正しました
    -   GBK/GB18030エンコードデータ[＃17618](https://github.com/tikv/tikv/issues/17618) @ [CbcWestwolf](https://github.com/CbcWestwolf)処理時にエンコードが失敗する可能性がある問題を修正
    -   例外[＃18245](https://github.com/tikv/tikv/issues/18245) @ [wlwilliamx](https://github.com/wlwilliamx)が発生したときに CDC 接続でリソース漏洩が発生する可能性がある問題を修正しました
    -   リージョンマージでRaftインデックスの不一致[＃18129](https://github.com/tikv/tikv/issues/18129) @ [栄光](https://github.com/glorv)により TiKV 異常終了が発生する可能性がある問題を修正しました
    -   解決済み-TSの監視とログが異常になる可能性がある問題を修正[＃17989](https://github.com/tikv/tikv/issues/17989) @ [エキシウム](https://github.com/ekexium)
    -   Titanコンポーネントとの非互換性によりアップグレードが失敗する問題を修正[＃18263](https://github.com/tikv/tikv/issues/18263) @ [v01dstar](https://github.com/v01dstar) @ [LykxSassinator](https://github.com/LykxSassinator)

-   PD

    -   単一のログファイルのデフォルト値`max-size`が正しく設定されていない問題を修正しました[＃9037](https://github.com/tikv/pd/issues/9037) @ [rleungx](https://github.com/rleungx)
    -   `flow-round-by-digit`構成項目の値が再起動後に上書きされる可能性がある問題を修正[＃8980](https://github.com/tikv/pd/issues/8980) @ [ノルーシュ](https://github.com/nolouch)
    -   PDネットワーク[＃8962](https://github.com/tikv/pd/issues/8962) @ [okJiang](https://github.com/okJiang)の不安定さにより、データのインポートやインデックスシナリオの追加操作が失敗する可能性がある問題を修正しました。
    -   `tidb_enable_tso_follower_proxy`システム変数が有効になっているときに PD がpanic可能性がある問題を修正[＃8950](https://github.com/tikv/pd/issues/8950) @ [okJiang](https://github.com/okJiang)
    -   `tidb_enable_tso_follower_proxy`システム変数が[＃8947](https://github.com/tikv/pd/issues/8947) @ [Jmポテト](https://github.com/JmPotato)で有効にならない可能性がある問題を修正しました
    -   TSO [＃9004](https://github.com/tikv/pd/issues/9004) @ [rleungx](https://github.com/rleungx)を割り当てるときにメモリリークが発生する可能性がある問題を修正しました
    -   PDLeader[＃9017](https://github.com/tikv/pd/issues/9017)対[rleungx](https://github.com/rleungx)切り替え時にリージョン同期が間に合わない可能性がある問題を修正しました
    -   PDノードがLeader[＃9051](https://github.com/tikv/pd/issues/9051) @ [rleungx](https://github.com/rleungx)でない場合でもTSOを生成する可能性がある問題を修正しました

-   TiFlash

    -   メモリ使用量が少ないときにTiFlash が予期せずRaftメッセージの処理を拒否する可能性がある問題を修正[＃9745](https://github.com/pingcap/tiflash/issues/9745) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   大量のデータをインポートした後にTiFlash のメモリ使用量が高くなる可能性がある問題を修正[＃9812](https://github.com/pingcap/tiflash/issues/9812) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   パーティションテーブルに対するクエリが、パーティションテーブル[＃9787](https://github.com/pingcap/tiflash/issues/9787) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`ALTER TABLE ... RENAME COLUMN`実行した後にエラーを返す可能性がある問題を修正しました。
    -   特定の状況でTiFlash が予期せず終了したときにエラー スタック トレースを印刷できないことがある問題を修正[＃9902](https://github.com/pingcap/tiflash/issues/9902) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   `profiles.default.init_thread_count_scale` `0` [＃9906](https://github.com/pingcap/tiflash/issues/9906) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に設定するとTiFlash の起動がブロックされる可能性がある問題を修正しました
    -   クエリに仮想列が含まれており、リモート読み取り[＃9561](https://github.com/pingcap/tiflash/issues/9561) @ [グオシャオゲ](https://github.com/guo-shaoge)をトリガーするときに`Not found column`エラーが発生する可能性がある問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャで、 TiFlashコンピューティング ノードがリージョンピア[＃9750](https://github.com/pingcap/tiflash/issues/9750) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を追加するためのターゲット ノードとして誤って選択される可能性がある問題を修正しました。

-   ツール

    -   バックアップと復元 (BR)

        -   PD [＃18087](https://github.com/tikv/tikv/issues/18087) @ [ユジュンセン](https://github.com/YuJuncen)にアクセスできないために致命的なエラーが発生した場合にログバックアップが正常に終了しない問題を修正しました。
        -   TiKV [＃58845](https://github.com/pingcap/tidb/issues/58845) @ [トリスタン1900](https://github.com/Tristan1900)にリクエストを送信するときに`rpcClient is idle`エラーが発生し、 BRが復元に失敗する問題を修正しました。
        -   PITRが3072バイトを超えるインデックスの復元に失敗する問題を修正[＃58430](https://github.com/pingcap/tidb/issues/58430) @ [ユジュンセン](https://github.com/YuJuncen)
        -   `br log status --json` [＃57959](https://github.com/pingcap/tidb/issues/57959) @ [リーヴルス](https://github.com/Leavrth)を使用してログバックアップタスクをクエリすると、結果に`status`フィールドが表示されない問題を修正しました。
        -   アドバンサー所有者が[＃58031](https://github.com/pingcap/tidb/issues/58031) @ [3ポイントシュート](https://github.com/3pointer)に切り替わったときに、ログバックアップが予期せず一時停止状態になる可能性がある問題を修正しました。

    -   TiCDC

        -   多数の小さなテーブルがあるシナリオで TiCDC を有効にすると、TiKV が[＃18142](https://github.com/tikv/tikv/issues/18142) @ [ヒック](https://github.com/hicqu)で再起動する可能性がある問題を修正しました。
        -   アップストリームで新しく追加された列のデフォルト値を`NOT NULL`から`NULL`に変更すると、ダウンストリームのその列のデフォルト値が正しくなくなる問題を修正しました[＃12037](https://github.com/pingcap/tiflow/issues/12037) @ [wk989898](https://github.com/wk989898)
        -   Sarama クライアントによって再送信された順序が乱れたメッセージによって Kafka メッセージの順序が正しくなくなる問題を修正[＃11935](https://github.com/pingcap/tiflow/issues/11935) @ [3エースショーハンド](https://github.com/3AceShowHand)
        -   TiCDC が`RENAME TABLE`操作[＃11946](https://github.com/pingcap/tiflow/issues/11946) @ [wk989898](https://github.com/wk989898)中にフィルタリングに誤ったテーブル名を使用する問題を修正しました
        -   チェンジフィードが削除された後に goroutines リークが発生する問題を修正[＃11954](https://github.com/pingcap/tiflow/issues/11954) @ [ヒック](https://github.com/hicqu)
        -   `changefeed pause`コマンドで`--overwrite-checkpoint-ts`パラメータを使用すると、変更フィードが[＃12055](https://github.com/pingcap/tiflow/issues/12055) @ [ホンユニャン](https://github.com/hongyunyan)で停止する可能性がある問題を修正しました。
        -   Avroプロトコル[＃11994](https://github.com/pingcap/tiflow/issues/11994) @ [wk989898](https://github.com/wk989898)経由で`default NULL`文を複製するときにTiCDCがエラーを報告する問題を修正
        -   PDスケールイン[＃12004](https://github.com/pingcap/tiflow/issues/12004) @ [リデジュ](https://github.com/lidezhu)後にTiCDCがPDに正しく接続できない問題を修正

    -   TiDB Lightning

        -   ログが適切に感度調整されない問題を修正[＃59086](https://github.com/pingcap/tidb/issues/59086) @ [GMHDBJD](https://github.com/GMHDBJD)
