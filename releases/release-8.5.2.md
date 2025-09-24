---
title: TiDB 8.5.2 Release Notes
summary: TiDB 8.5.2 の改善点とバグ修正について説明します。
---

# TiDB 8.5.2 リリースノート {#tidb-8-5-2-release-notes}

発売日：2025年6月12日

TiDB バージョン: 8.5.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 改善点 {#improvements}

-   ティドブ

    -   TTLテーブルと関連する統計収集タスクのGCの実行を所有者ノードに制限することで、オーバーヘッド[＃59357](https://github.com/pingcap/tidb/issues/59357) @ [lcwangchao](https://github.com/lcwangchao)を削減します。

-   ティクブ

    -   `import.num-threads`構成項目を動的に変更するサポート[＃17807](https://github.com/tikv/tikv/issues/17807) @ [リドリスR](https://github.com/RidRisR)

-   ツール

    -   バックアップと復元 (BR)

        -   新しくサポートされた AWS リージョンが検証に失敗することで発生するバックアップエラーを回避するために、AWS リージョン名のチェックを削除します[＃18159](https://github.com/tikv/tikv/issues/18159) @ [3ポイントシュート](https://github.com/3pointer)

    -   TiDB Lightning

        -   CSV ファイルを解析するときに行幅チェックを追加して、OOM の問題を防ぐ[＃58590](https://github.com/pingcap/tidb/issues/58590) @ [D3ハンター](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   ティドブ

    -   `zone`ラベル[＃59402](https://github.com/pingcap/tidb/issues/59402) @ [エキシウム](https://github.com/ekexium)を設定した後、タイムスタンプ検証中に TiDB が TSO を取得できない問題を修正しました。
    -   実行が失敗したときにエラーを報告せずにハッシュ結合が誤った結果を返す問題を修正[＃59377](https://github.com/pingcap/tidb/issues/59377) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   TiFlash がクラッシュしたり、誤った結果を返す可能性がある問題を修正[＃60517](https://github.com/pingcap/tidb/issues/60517) @ [ウィントーカー](https://github.com/wintalker)
    -   `ORDER BY`並列ソートでエラーが発生したり、クエリがキャンセルされたりすると実行がハングする問題を修正[＃59655](https://github.com/pingcap/tidb/issues/59655) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   生成された列[＃58475](https://github.com/pingcap/tidb/issues/58475) @ [ジョーチェン](https://github.com/joechenrh)を含むパーティション テーブルをクエリするときにエラーが発生する問題を修正しました。
    -   同じ名前のビューを2つ作成してもエラーが報告されない問題を修正[＃58769](https://github.com/pingcap/tidb/issues/58769) @ [天菜麻緒](https://github.com/tiancaiamao)
    -   Join の等価条件の両側のデータ型が異なると、 TiFlash [＃59877](https://github.com/pingcap/tidb/issues/59877) @ [yibin87](https://github.com/yibin87)で誤った結果が発生する可能性がある問題を修正しました。
    -   ハッシュパーティションテーブルで条件`is null`クエリを実行するとpanic[＃58374](https://github.com/pingcap/tidb/issues/58374) @ [定義2014](https://github.com/Defined2014/)が発生する問題を修正
    -   分散storageおよびコンピューティングアーキテクチャのTiFlashノードを含むクラスターで`ALTER TABLE ... PLACEMENT POLICY ...`実行した後、リージョンピアが誤ってTiFlashコンピューティングノード[＃58633](https://github.com/pingcap/tidb/issues/58633) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に追加される可能性がある問題を修正しました。
    -   統計ファイルに NULL 値[＃53966](https://github.com/pingcap/tidb/issues/53966) @ [キング・ディラン](https://github.com/King-Dylan)が含まれている場合、統計を手動でロードすると失敗する可能性がある問題を修正しました。
    -   TTLジョブが無視されたり複数回処理されたりする問題を修正[＃59347](https://github.com/pingcap/tidb/issues/59347) @ [ヤンケオ](https://github.com/YangKeao)
    -   交換パーティションの誤った判断により実行エラーが発生する問題を修正[＃59534](https://github.com/pingcap/tidb/issues/59534) @ [ミョンス](https://github.com/mjonss)
    -   統計の不適切な例外処理により、バックグラウンドタスクがタイムアウトしたときにメモリ内の統計が誤って削除される問題を修正しました[＃57901](https://github.com/pingcap/tidb/issues/57901) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   Grafanaの**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正しました[＃57176](https://github.com/pingcap/tidb/issues/57176) @ [ホーキングレイ](https://github.com/hawkingrei)
    -   キャンセルされたTTLタスクによってコミットされていないセッションがグローバルセッションプール[＃58900](https://github.com/pingcap/tidb/issues/58900) @ [ヤンケオ](https://github.com/YangKeao)に配置される可能性がある問題を修正しました
    -   特定のシナリオでログ編集を有効にしても効果がない問題を修正[＃59279](https://github.com/pingcap/tidb/issues/59279) @ [接線](https://github.com/tangenta)
    -   `rowContainer`特定のシナリオで TiDB がpanicを起こす可能性がある問題を修正[＃59976](https://github.com/pingcap/tidb/issues/59976) @ [ヤンケオ](https://github.com/YangKeao)
    -   パーティションテーブル[＃59827](https://github.com/pingcap/tidb/issues/59827) @ [ミョンス](https://github.com/mjonss)のシナリオ`Point_Get`でパーティションプルーニングが正しく行われない可能性がある問題を修正しました。
    -   DDL実行中にパーティションテーブルのレコードを更新するとデータ破損が発生する可能性がある問題を修正[＃57588](https://github.com/pingcap/tidb/issues/57588) @ [定義2014](https://github.com/Defined2014)
    -   特定のシナリオで`information_schema`のパフォーマンスと安定性が影響を受ける問題を修正[＃58142](https://github.com/pingcap/tidb/issues/58142) [＃58363](https://github.com/pingcap/tidb/issues/58363) [＃58712](https://github.com/pingcap/tidb/issues/58712) @ [天菜麻緒](https://github.com/tiancaiamao)
    -   分散実行フレームワーク（DXF）が有効になっている場合、内部TiDBセッションで`tidb_txn_entry_size_limit`動的に調整できない問題を修正しました[＃59506](https://github.com/pingcap/tidb/issues/59506) @ [D3ハンター](https://github.com/D3Hunter)
    -   グローバルソートが有効な場合に、 `IMPORT INTO`機能が一意のキーの競合を適切に処理できない問題を修正[＃59650](https://github.com/pingcap/tidb/issues/59650) @ [ランス6716](https://github.com/lance6716)
    -   グローバルソートデ​​ータパスにネットワークレイテンシーエラーを挿入すると、 `IMPORT INTO`操作が[＃50451](https://github.com/pingcap/tidb/issues/50451) @ [D3ハンター](https://github.com/D3Hunter)で失敗する問題を修正しました。
    -   `ADD UNIQUE INDEX`実行するとデータの不整合が発生する可能性がある問題を修正[＃60339](https://github.com/pingcap/tidb/issues/60339) @ [接線](https://github.com/tangenta)
    -   `INFORMATION_SCHEMA.TIDB_SERVERS_INFO` [＃59245](https://github.com/pingcap/tidb/issues/59245) @ [ランス6716](https://github.com/lance6716)をクエリしたときに`LABELS`列目の値が`BINLOG_STATUS`列目に誤って表示される問題を修正しました
    -   インデックス作成中にkill PD Leaderフォールトを挿入するとデータの不整合が発生する可能性がある問題を修正[＃59701](https://github.com/pingcap/tidb/issues/59701) @ [接線](https://github.com/tangenta)
    -   約650万のテーブル[＃58368](https://github.com/pingcap/tidb/issues/58368) @ [ランス6716](https://github.com/lance6716)を作成した後にTiDBがメモリ不足（OOM）になる問題を修正しました
    -   グローバルソート機能を有効にして大量のデータをインポートするときに、一意のキーの追加が失敗する可能性がある問題を修正[＃59725](https://github.com/pingcap/tidb/issues/59725) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)
    -   S3外部storage[＃59326](https://github.com/pingcap/tidb/issues/59326) @ [ランス6716](https://github.com/lance6716)へのアクセスに失敗した後、TiDBが読み取り不可能なエラーメッセージを返す問題を修正しました
    -   `information_schema.tables`クエリすると、 `table_schema`と`table_name`値が一致しない[＃60593](https://github.com/pingcap/tidb/issues/60593) @ [接線](https://github.com/tangenta)が返される問題を修正しました。
    -   内部SQLコミットが失敗したときにDDL通知が誤った通知を送信する可能性がある問題を修正[＃59055](https://github.com/pingcap/tidb/issues/59055) @ [ランス6716](https://github.com/lance6716)
    -   グローバルソート機能が有効になっている場合、リージョンサイズが 256 MiB [＃59962](https://github.com/pingcap/tidb/issues/59962) @ [D3ハンター](https://github.com/D3Hunter)であるにもかかわらず、 `ADD INDEX` DDL 操作で SST ファイルが 96 MiB に分割される問題を修正しました。
    -   グローバルソート機能を有効にした状態でデータのインポート中にメモリ使用量が 80% を超えると TiDB サーバーのメモリ(OOM) が発生する問題を修正[＃59508](https://github.com/pingcap/tidb/issues/59508) @ [D3ハンター](https://github.com/D3Hunter)

-   ティクブ

    -   `txn_status_cache` [＃18384](https://github.com/tikv/tikv/issues/18384) @ [エキシウム](https://github.com/ekexium)で潜在的なデッドロックが発生する可能性がある問題を修正
    -   解決済み-TSの監視とログが異常になる可能性がある問題を修正[＃17989](https://github.com/tikv/tikv/issues/17989) @ [エキシウム](https://github.com/ekexium)
    -   リージョンマージでRaftインデックスの不一致[＃18129](https://github.com/tikv/tikv/issues/18129) @ [栄光](https://github.com/glorv)により TiKV 異常終了が発生する可能性がある問題を修正しました
    -   ディスクが[＃17939](https://github.com/tikv/tikv/issues/17939) @ [LykxSassinator](https://github.com/LykxSassinator)でスタックしているときに TiKV が PD にハートビートを報告できない問題を修正しました
    -   GCワーカーの負荷が高いときにデッドロックが発生する可能性がある問題を修正[＃18214](https://github.com/tikv/tikv/issues/18214) @ [ジグアン](https://github.com/zyguan)
    -   タイムロールバックによって異常なRocksDBフロー制御が発生し、パフォーマンスジッター[＃17995](https://github.com/tikv/tikv/issues/17995) @ [LykxSassinator](https://github.com/LykxSassinator)が発生する可能性がある問題を修正しました。
    -   例外[＃18245](https://github.com/tikv/tikv/issues/18245) @ [wlwilliamx](https://github.com/wlwilliamx)が発生したときに CDC 接続でリソース漏洩が発生する可能性がある問題を修正しました
    -   リージョンを[＃17602](https://github.com/tikv/tikv/issues/17602)対[LykxSassinator](https://github.com/LykxSassinator)に分割した後、リーダーをすぐに選出できない問題を修正しました
    -   1フェーズコミット（1PC）のみが有効で、非同期コミットが有効になっていない場合に、最後に書き込まれたデータが読み取れない可能性がある問題を修正[＃18117](https://github.com/tikv/tikv/issues/18117) @ [ジグアン](https://github.com/zyguan)
    -   GCワーカーが予期せずエラーログ[＃18213](https://github.com/tikv/tikv/issues/18213) @ [エキシウム](https://github.com/ekexium)を出力問題を修正しました

-   PD

    -   マイクロサービスシナリオ[＃9091](https://github.com/tikv/pd/issues/9091) @ [lhy1024](https://github.com/lhy1024)で TSO を転送するときに発生する可能性のある同時実行の問題を修正します
    -   `BatchScanRegions`で返される結果が[＃9216](https://github.com/tikv/pd/issues/9216) @ [lhy1024](https://github.com/lhy1024)に適切に制限されない問題を修正しました
    -   1人のフォロワーがリーダー[＃9020](https://github.com/tikv/pd/issues/9020) @ [lhy1024](https://github.com/lhy1024)からのネットワーク分割を経験すると予期しない選出が発生する問題を修正しました
    -   リソース制御[＃60404](https://github.com/pingcap/tidb/issues/60404) @ [Jmポテト](https://github.com/JmPotato)で`QUERY_LIMIT`設定されている場合、 `COOLDOWN`または`SWITCH_GROUP`トリガーされない問題を修正しました
    -   `StoreInfo` [＃9185](https://github.com/tikv/pd/issues/9185) @ [okJiang](https://github.com/okJiang)で誤って上書きされる可能性がある問題を修正しました
    -   PDネットワーク[＃8962](https://github.com/tikv/pd/issues/8962) @ [okJiang](https://github.com/okJiang)の不安定さにより、データのインポートやインデックスシナリオの追加操作が失敗する可能性がある問題を修正しました。
    -   単一のログファイルのデフォルト値`max-size`が正しく[＃9037](https://github.com/tikv/pd/issues/9037) @ [rleungx](https://github.com/rleungx)に設定されない問題を修正しました
    -   TSO [＃9004](https://github.com/tikv/pd/issues/9004) @ [rleungx](https://github.com/rleungx)を割り当てるときにメモリリークが発生する可能性がある問題を修正しました
    -   `tidb_enable_tso_follower_proxy`システム変数が[＃8947](https://github.com/tikv/pd/issues/8947) @ [Jmポテト](https://github.com/JmPotato)で有効にならない可能性がある問題を修正しました
    -   PDノードがLeader[＃9051](https://github.com/tikv/pd/issues/9051) @ [rleungx](https://github.com/rleungx)でない場合でもTSOを生成する可能性がある問題を修正しました
    -   PDLeader[＃9017](https://github.com/tikv/pd/issues/9017)対[rleungx](https://github.com/rleungx)切り替え時にリージョン同期が間に合わない問題を修正しました
    -   デフォルト値`lease`が正しく設定されていない問題を修正[＃9156](https://github.com/tikv/pd/issues/9156) @ [rleungx](https://github.com/rleungx)
    -   `tidb_enable_tso_follower_proxy`有効にすると TSO サービスが利用できなくなる可能性がある問題を修正[＃9188](https://github.com/tikv/pd/issues/9188) @ [テーマ](https://github.com/Tema)

-   TiFlash

    -   ソート中にデータが溢れてTiFlashがクラッシュする可能性がある問題を修正[9999](https://github.com/pingcap/tiflash/issues/9999) @ [ウィンドトーカー](https://github.com/windtalker)
    -   `GROUP BY ... WITH ROLLUP` [＃10110](https://github.com/pingcap/tiflash/issues/10110) @ [ゲンリキ](https://github.com/gengliqi)を含むSQL文を実行するとTiFlashが`Exception: Block schema mismatch`エラーを返す可能性がある問題を修正しました。
    -   分散storageおよびコンピューティングアーキテクチャで、 TiFlashコンピューティング ノードがリージョンピア[＃9750](https://github.com/pingcap/tiflash/issues/9750) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を追加するためのターゲット ノードとして誤って選択される可能性がある問題を修正しました。
    -   特定の状況でTiFlash が予期せず終了したときにエラー スタック トレースを印刷できないことがある問題を修正[＃9902](https://github.com/pingcap/tiflash/issues/9902) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   大量のデータをインポートした後にTiFlash のメモリ使用量が高くなる可能性がある問題を修正[＃9812](https://github.com/pingcap/tiflash/issues/9812) @ [カルビンネオ](https://github.com/CalvinNeo)
    -   `profiles.default.init_thread_count_scale` `0` [＃9906](https://github.com/pingcap/tiflash/issues/9906) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)に設定するとTiFlash の起動がブロックされる可能性がある問題を修正しました
    -   パーティションテーブルに対するクエリが、パーティションテーブル[＃9787](https://github.com/pingcap/tiflash/issues/9787) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)で`ALTER TABLE ... RENAME COLUMN`実行した後にエラーを返す可能性がある問題を修正しました。
    -   クエリに仮想列が含まれ、リモート読み取り[＃9561](https://github.com/pingcap/tiflash/issues/9561) @ [グオシャオゲ](https://github.com/guo-shaoge)をトリガーすると`Not found column`エラーが発生する可能性がある問題を修正しました。
    -   クラスター内のテーブルに多数の`ENUM`型列[＃9947](https://github.com/pingcap/tiflash/issues/9947) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)が含まれている場合、 TiFlashが大量のメモリを消費する可能性がある問題を修正しました。
    -   16 MiB [＃10052](https://github.com/pingcap/tiflash/issues/10052) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を超えるデータの単一行を挿入した後にTiFlash が再起動に失敗する可能性がある問題を修正しました
    -   ベクトルインデックスを持つテーブルに新しいデータが挿入された後、 TiFlash が一部のディスクデータを正しく消去せず、異常なディスクスペース消費を引き起こす可能性がある問題を修正しました[＃9946](https://github.com/pingcap/tiflash/issues/9946) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   同じテーブルに複数のベクトルインデックスを作成した後に、 TiFlash が以前に作成されたベクトルインデックスを予期せず削除し、パフォーマンスが低下する可能性がある問題を修正しました[＃9971](https://github.com/pingcap/tiflash/issues/9971) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)
    -   TiFlash が分散storageおよびコンピューティングアーキテクチャ[＃9847](https://github.com/pingcap/tiflash/issues/9847) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)でベクトル検索クエリを高速化するためにベクトルインデックスを使用できない可能性がある問題を修正しました
    -   TiFlash が分散storageおよびコンピューティングアーキテクチャ[＃9955](https://github.com/pingcap/tiflash/issues/9955) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)で大量の`tag=EnumParseOverflowContainer`ログを出力する可能性がある問題を修正しました
    -   TiFlash が`SELECT ... AS OF TIMESTAMP`クエリ[＃10046](https://github.com/pingcap/tiflash/issues/10046) @ [カルビンネオ](https://github.com/CalvinNeo)を実行するときにLearner Read を期待どおりにスキップしない問題を修正しました
    -   不規則なリージョンキー範囲[＃10147](https://github.com/pingcap/tiflash/issues/10147) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を持つスナップショットを処理するときにTiFlash がpanic可能性がある問題を修正しました

-   ツール

    -   バックアップと復元 (BR)

        -   データの復元中に SST ファイルを繰り返しダウンロードすると、極端な場合には TiKV がpanic可能性がある問題を修正しました[＃18335](https://github.com/tikv/tikv/issues/18335) @ [3ポイントシュート](https://github.com/3pointer)
        -   `br log status --json` [＃57959](https://github.com/pingcap/tidb/issues/57959) @ [リーヴルス](https://github.com/Leavrth)を使用してログバックアップタスクをクエリすると、結果に`status`フィールドが表示されない問題を修正しました。
        -   TiKV [＃58845](https://github.com/pingcap/tidb/issues/58845) @ [トリスタン1900](https://github.com/Tristan1900)にリクエストを送信するときに`rpcClient is idle`エラーが発生し、 BRが復元に失敗する問題を修正しました。
        -   PD [＃18087](https://github.com/tikv/tikv/issues/18087) @ [ユジュンセン](https://github.com/YuJuncen)にアクセスできないために致命的なエラーが発生した場合にログバックアップが正常に終了しない問題を修正しました。
        -   PITRが3072バイトを超えるインデックスの復元に失敗する問題を修正[＃58430](https://github.com/pingcap/tidb/issues/58430) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   レプリケーショントラフィックが下流の Kafka [＃12110](https://github.com/pingcap/tiflow/issues/12110) @ [3エースショーハンド](https://github.com/3AceShowHand)のトラフィックしきい値を超えた後に、変更フィードがスタックする可能性がある問題を修正しました。
        -   `pulsar+http`または`pulsar+https`プロトコルが使用されている場合、Kafka シンクのディスパッチルールが有効にならない問題を修正しました[＃12068](https://github.com/pingcap/tiflow/issues/12068) @ [サンディープ・パディ](https://github.com/SandeepPadhi)
        -   TiCDC が PD リーダーの移行を時間内に監視できず、レプリケーションのレイテンシーが[＃11997](https://github.com/pingcap/tiflow/issues/11997) @ [リデジュ](https://github.com/lidezhu)に増加する問題を修正しました。
        -   Avroプロトコル[＃11994](https://github.com/pingcap/tiflow/issues/11994) @ [wk989898](https://github.com/wk989898)経由で`default NULL`文を複製するときにTiCDCがエラーを報告する問題を修正
        -   アップストリームで新しく追加された列のデフォルト値を`NOT NULL`から`NULL`に変更すると、ダウンストリームのその列のデフォルト値が正しくなくなる問題を修正しました[＃12037](https://github.com/pingcap/tiflow/issues/12037) @ [wk989898](https://github.com/wk989898)
        -   PDスケールイン[＃12004](https://github.com/pingcap/tiflow/issues/12004) @ [リデジュ](https://github.com/lidezhu)後にTiCDCがPDに正しく接続できない問題を修正
        -   `CREATE TABLE IF NOT EXISTS`または`CREATE DATABASE IF NOT EXISTS`ステートメント[＃11839](https://github.com/pingcap/tiflow/issues/11839) @ [チャールズ・チャン96](https://github.com/CharlesCheung96)を複製するときに TiCDC がpanic可能性がある問題を修正しました

    -   TiDB データ移行 (DM)

        -   TLSと`shard-mode`両方が[＃11842](https://github.com/pingcap/tiflow/issues/11842) @ [孫暁光](https://github.com/sunxiaoguang)に設定されている場合に`start-task`の事前チェックが失敗する問題を修正

    -   TiDB Lightning

        -   高同時実行シナリオでクラウドstorageからデータをインポートするときにパフォーマンスが低下する問題を修正[＃57413](https://github.com/pingcap/tidb/issues/57413) @ [xuanyu66](https://github.com/xuanyu66)
        -   TiDB Lightning [＃58085](https://github.com/pingcap/tidb/issues/58085) @ [ランス6716](https://github.com/lance6716)を使用してデータをインポートするときにエラーレポートの出力が切り捨てられる問題を修正しました
        -   ログが適切に感度調整されない問題を修正[＃59086](https://github.com/pingcap/tidb/issues/59086) @ [GMHDBJD](https://github.com/GMHDBJD)
        -   外部アカウントを使用して GCSstorage操作[＃60155](https://github.com/pingcap/tidb/issues/60155) @ [ランス6716](https://github.com/lance6716)を実行すると、認証が`context canceled`エラーで失敗する問題を修正しました
        -   クラウドstorageから TiDB [＃60224](https://github.com/pingcap/tidb/issues/60224) @ [ジョーチェン](https://github.com/joechenrh)に Parquet ファイルをインポートするときに、 TiDB Lightning が数時間停止する可能性がある問題を修正しました。
        -   大量のデータをインポートする際に、 TiDB Lightning がSST ファイルの書き込みまたは TiKV クラスターへの取り込み中にメモリ(OOM) になる可能性がある問題を修正しました[＃59947](https://github.com/pingcap/tidb/issues/59947) @ [オリバーS929](https://github.com/OliverS929)
        -   テーブル作成時の最大 QPS が低く、 `information_schema.tables`へのアクセスが遅いため、数百万のテーブルがあるシナリオでTiDB Lightning がスキーマ ジョブをディスパッチする速度が遅くなる問題を修正しました[＃58141](https://github.com/pingcap/tidb/issues/58141) @ [D3ハンター](https://github.com/D3Hunter)

    -   NGモニタリング

        -   DocDB が高負荷時にメモリを大量に消費する問題を修正し、DocDB [＃267](https://github.com/pingcap/ng-monitoring/issues/267) @ [モーニクス](https://github.com/mornyx)のオプションのバックエンドとして SQLite を使用するようになりました。
        -   時系列データのカーディナリティが高い場合に TSDB がメモリを大量に消費する問題を修正し、TSDB [＃295](https://github.com/pingcap/ng-monitoring/issues/295) @ [モーニクス](https://github.com/mornyx)のメモリ構成オプションを提供します。
