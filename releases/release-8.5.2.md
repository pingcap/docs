---
title: TiDB 8.5.2 Release Notes
summary: TiDB 8.5.2 の改善点とバグ修正について学びましょう。
---

# TiDB 8.5.2 リリースノート {#tidb-8-5-2-release-notes}

発売日：2025年6月12日

TiDBバージョン：8.5.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb)| [本番環境への展開](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## 改善点 {#improvements}

-   TiDB

    -   TTLテーブルおよび関連する統計収集タスクのGC実行をオーナーノードに限定することで、オーバーヘッドを削減します [#59357](https://github.com/pingcap/tidb/issues/59357) @[lcwangchao](https://github.com/lcwangchao)

-   ティクヴ

    -   `import.num-threads`設定項目を動的に変更するサポート [#17807](https://github.com/tikv/tikv/issues/17807) @[RidRisR](https://github.com/RidRisR)

-   ツール

    -   バックアップと復元 (BR)

        -   新しくサポートされた AWS リージョンが検証に失敗することによって引き起こされるバックアップ エラーを避けるために、AWS リージョン名のチェックを削除します [#18159](https://github.com/tikv/tikv/issues/18159) @[3pointer](https://github.com/3pointer)シュート

    -   TiDB Lightning

        -   OOM の問題を防ぐために CSV ファイルを解析するときに行幅チェックを追加 [#58590](https://github.com/pingcap/tidb/issues/58590) @[D3Hunter](https://github.com/D3Hunter)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `zone`ラベルを設定した後、タイムスタンプ検証中にTiDBがTSOを取得できない問題を修正しました [#59402](https://github.com/pingcap/tidb/issues/59402) @[ekexium](https://github.com/ekexium)
    -   ハッシュ結合が実行失敗時にエラーを報告せずに誤った結果を返す問題を修正 [#59377](https://github.com/pingcap/tidb/issues/59377) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   TiFlashがクラッシュしたり、誤った結果を返す可能性がある問題を修正しました [#60517](https://github.com/pingcap/tidb/issues/60517) @[wintalker](https://github.com/wintalker)
    -   `ORDER BY`を使用した並列ソートでエラーが発生したり、クエリがキャンセルされたりした場合に実行がハングアップする問題を修正します [#59655](https://github.com/pingcap/tidb/issues/59655) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   生成列を含むパーティションテーブルをクエリするとエラーが発生する問題を修正します [#58475](https://github.com/pingcap/tidb/issues/58475) @[joechenrh](https://github.com/joechenrh)
    -   同じ名前のビューを2つ作成してもエラーが報告されない問題を修正 [#58769](https://github.com/pingcap/tidb/issues/58769) @[tiancaiamao](https://github.com/tiancaiamao)
    -   TiFlashの Join における等価条件の両側のデータ型が異なると、誤った結果が生じる可能性がある問題を修正しました [#59877](https://github.com/pingcap/tidb/issues/59877) @[yibin87](https://github.com/yibin87)
    -   ハッシュパーティションテーブルで`is null`条件を含むクエリがpanicを引き起こす問題を修正 [#58374](https://github.com/pingcap/tidb/issues/58374) @[Defined2014](https://github.com/Defined2014)
    -   分散storageおよびコンピューティングアーキテクチャのTiFlashノードを含むクラスタで`ALTER TABLE ... PLACEMENT POLICY ...`を実行した後、リージョンピアが誤ってTiFlash Compute ノードに追加される可能性がある問題を修正しました [#58633](https://github.com/pingcap/tidb/issues/58633) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   統計ファイルにnull値が含まれている場合、統計の手動読み込みに失敗することがある問題を修正 [#53966](https://github.com/pingcap/tidb/issues/53966) @[King-Dylan](https://github.com/King-Dylan)
    -   TTLジョブが無視されたり、複数回処理されたりする問題を修正 [#59347](https://github.com/pingcap/tidb/issues/59347) @[YangKeao](https://github.com/YangKeao)
    -   交換パーティションでの誤った判断により実行が失敗する問題を修正 [#59534](https://github.com/pingcap/tidb/issues/59534) @[mjonss](https://github.com/mjonss)
    -   バックグラウンドタスクがタイムアウトした際に、統計情報の例外処理が不適切であるためにメモリ内の統計情報が誤って削除される問題を修正 [#57901](https://github.com/pingcap/tidb/issues/57901) @[hawkingrei](https://github.com/hawkingrei)
    -   Grafana の**Stats Healthy Distribution**パネルのデータが正しくない可能性がある問題を修正 [#57176](https://github.com/pingcap/tidb/issues/57176) @[hawkingrei](https://github.com/hawkingrei)
    -   キャンセルされたTTLタスクが未コミットのセッションをグローバルセッションプールに配置する可能性がある問題を修正 [#58900](https://github.com/pingcap/tidb/issues/58900) @[YangKeao](https://github.com/YangKeao)
    -   ログの編集を有効にしても特定のシナリオで効果がない問題を修正 [#59279](https://github.com/pingcap/tidb/issues/59279) @[tangenta](https://github.com/tangenta)
    -   `rowContainer`が特定のシナリオで TiDB をpanic可能性がある問題を修正 [#59976](https://github.com/pingcap/tidb/issues/59976) @[YangKeao](https://github.com/YangKeao)
    -   パーティション化されたテーブルの`Point_Get`シナリオでパーティションプルーニングが正しくない可能性がある問題を修正 [#59827](https://github.com/pingcap/tidb/issues/59827) @[mjonss](https://github.com/mjonss)
    -   DDL 実行中にパーティション テーブル内のレコードを更新するとデータ破損が発生する可能性がある問題を修正 [#57588](https://github.com/pingcap/tidb/issues/57588) @[Defined2014](https://github.com/Defined2014)
    -   `information_schema`のパフォーマンスと安定性が特定のシナリオで影響を受ける問題を修正しました[#58142](https://github.com/pingcap/tidb/issues/58142) [#58363](https://github.com/pingcap/tidb/issues/58363) [#58712](https://github.com/pingcap/tidb/issues/58712) @[tiancaiamao](https://github.com/tiancaiamao)
    -   分散実行フレームワーク（DXF）が有効になっている場合、内部TiDBセッションで`tidb_txn_entry_size_limit`を動的に調整できない問題を修正します [#59506](https://github.com/pingcap/tidb/issues/59506) @[D3Hunter](https://github.com/D3Hunter)
    -   `IMPORT INTO`機能がグローバルソートが有効になっている場合に一意キーの競合を適切に処理できない問題を修正します [#59650](https://github.com/pingcap/tidb/issues/59650) @[lance6716](https://github.com/lance6716)
    -   グローバルソートデ​​ータパスにネットワークレイテンシーエラーを注入すると、 `IMPORT INTO`操作が失敗する問題を修正 [#50451](https://github.com/pingcap/tidb/issues/50451) @[D3Hunter](https://github.com/D3Hunter)
    -   `ADD UNIQUE INDEX`の実行時にデータ不整合が発生する可能性がある問題を修正 [#60339](https://github.com/pingcap/tidb/issues/60339) @[tangenta](https://github.com/tangenta)
    -   `LABELS`をクエリした際に`BINLOG_STATUS`列の値が誤って表示される問題を修正しました`INFORMATION_SCHEMA.TIDB_SERVERS_INFO` [#59245](https://github.com/pingcap/tidb/issues/59245) @[lance6716](https://github.com/lance6716)
    -   インデックス作成中にPDLeaderの強制終了エラーを注入するとデータ不整合が発生する可能性がある問題を修正 [#59701](https://github.com/pingcap/tidb/issues/59701) @[tangenta](https://github.com/tangenta)
    -   TiDBが約650万個のテーブルを作成した後にメモリ不足（OOM）になる問題を修正 [#58368](https://github.com/pingcap/tidb/issues/58368) @[lance6716](https://github.com/lance6716)
    -   グローバルソート機能を有効にして大量のデータをインポートする際に、一意キーの追加が失敗する可能性がある問題を修正しました [#59725](https://github.com/pingcap/tidb/issues/59725) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   TiDBがS3外部storageへのアクセスに失敗した後に判読不能なエラーメッセージを返す問題を修正 [#59326](https://github.com/pingcap/tidb/issues/59326) @[lance6716](https://github.com/lance6716)
    -   `information_schema.tables`をクエリすると、 `table_schema`と`table_name`の値が一致しない問題を修正 [#60593](https://github.com/pingcap/tidb/issues/60593) @[tangenta](https://github.com/tangenta)
    -   内部SQLコミットが失敗した場合にDDL通知機能が誤った通知を送信する可能性がある問題を修正しました [#59055](https://github.com/pingcap/tidb/issues/59055) @[lance6716](https://github.com/lance6716)
    -   `ADD INDEX` DDL 操作で、リージョンサイズが 256 MiB であるにもかかわらず、グローバルソート機能が有効になっている場合に SST ファイルが 96 MiB ずつ分割される問題を修正します。 [#59962](https://github.com/pingcap/tidb/issues/59962) @[D3Hunter](https://github.com/D3Hunter)
    -   グローバルソート機能を有効にした状態でデータインポート中にメモリ使用率が80%を超えるとTiDBサーバーがメモリ不足（OOM）になる問題を修正 [#59508](https://github.com/pingcap/tidb/issues/59508) @[D3Hunter](https://github.com/D3Hunter)

-   ティクヴ

    -   `txn_status_cache` [#18384](https://github.com/tikv/tikv/issues/18384)でデッドロックが発生する可能性がある問題を修正しました @[ekexium](https://github.com/ekexium)
    -   Resolved-TS の監視とログが異常になる可能性がある問題を修正 [#17989](https://github.com/tikv/tikv/issues/17989) @[ekexium](https://github.com/ekexium)
    -   リージョンマージによってRaftインデックスの不一致が原因でTiKVが異常終了する可能性がある問題を修正 [#18129](https://github.com/tikv/tikv/issues/18129) @[glorv](https://github.com/glorv)
    -   ディスクがスタックしているときに TiKV が PD にハートビートを報告できない問題を修正 [#17939](https://github.com/tikv/tikv/issues/17939) @[LykxSassinator](https://github.com/LykxSassinator)
    -   GCワーカーに高負荷がかかっているときにデッドロックが発生する可能性がある問題を修正 [#18214](https://github.com/tikv/tikv/issues/18214) @[zyguan](https://github.com/zyguan)
    -   タイムロールバックが異常な RocksDB フロー制御を引き起こし、パフォーマンスのジッターにつながる可能性がある問題を修正しました [#17995](https://github.com/tikv/tikv/issues/17995) @[LykxSassinator](https://github.com/LykxSassinator)
    -   CDC接続で例外が発生した際にリソースリークが発生する可能性がある問題を修正 [#18245](https://github.com/tikv/tikv/issues/18245) @[wlwilliamx](https://github.com/wlwilliamx)
    -   リージョン分割後にリーダーが迅速に選出されない問題を修正 [#17602](https://github.com/tikv/tikv/issues/17602) @[LykxSassinator](https://github.com/LykxSassinator)
    -   1フェーズコミット（1PC）のみが有効で非同期コミットが有効になっていない場合に、最新の書き込みデータが読み取れない可能性がある問題を修正しました [#18117](https://github.com/tikv/tikv/issues/18117) @[zyguan](https://github.com/zyguan)
    -   GCワーカーが予期せずエラーログを出力問題を修正 [#18213](https://github.com/tikv/tikv/issues/18213) @[ekexium](https://github.com/ekexium)

-   PD

    -   マイクロサービスシナリオでTSOを転送する際に発生する可能性のある同時実行性の問題を修正します [#9091](https://github.com/tikv/pd/issues/9091) @[lhy1024](https://github.com/lhy1024)
    -   `BatchScanRegions`によって返される結果が適切に制限されない問題を修正します [#9216](https://github.com/tikv/pd/issues/9216) @[lhy1024](https://github.com/lhy1024)
    -   フォロワーの1人がリーダーからネットワーク分断を受けた際に予期しない選挙が発生する問題を修正します [#9020](https://github.com/tikv/pd/issues/9020) @[lhy1024](https://github.com/lhy1024)
    -   リソース制御で`COOLDOWN`が設定されている場合、 `SWITCH_GROUP`または`QUERY_LIMIT`がトリガーされない問題を修正します [#60404](https://github.com/pingcap/tidb/issues/60404) @[JmPotato](https://github.com/JmPotato)
    -   `StoreInfo`が誤って上書きされる可能性がある問題を修正 [#9185](https://github.com/tikv/pd/issues/9185) @[okJiang](https://github.com/okJiang)
    -   PDネットワークの不安定さにより、データインポートまたはインデックス追加シナリオでの操作が失敗する可能性がある問題を修正しました [#8962](https://github.com/tikv/pd/issues/8962) @[okJiang](https://github.com/okJiang)
    -   単一のログファイルに対する`max-size`のデフォルト値が正しく設定されていない問題を修正 [#9037](https://github.com/tikv/pd/issues/9037) @[rleungx](https://github.com/rleungx)
    -   TSOを割り当てる際にメモリリークが発生する可能性がある問題を修正 [#9004](https://github.com/tikv/pd/issues/9004) @[rleungx](https://github.com/rleungx)
    -   `tidb_enable_tso_follower_proxy`システム変数が有効にならない可能性がある問題を修正 [#8947](https://github.com/tikv/pd/issues/8947) @[JmPotato](https://github.com/JmPotato)
    -   PDノードがLeaderではない場合でもTSOを生成する可能性がある問題を修正 [#9051](https://github.com/tikv/pd/issues/9051) @[rleungx](https://github.com/rleungx)
    -   PDLeader切り替え中にリージョンシンカーが時間内に終了しない可能性がある問題を修正 [#9017](https://github.com/tikv/pd/issues/9017) @[rleungx](https://github.com/rleungx)
    -   `lease`のデフォルト値が正しく設定されていない問題を修正 [#9156](https://github.com/tikv/pd/issues/9156) @[rleungx](https://github.com/rleungx)
    -   `tidb_enable_tso_follower_proxy`を有効にするとTSOサービスが利用できなくなる可能性がある問題を修正しました [#9188](https://github.com/tikv/pd/issues/9188) @[Tema](https://github.com/Tema)

-   TiFlash

    -   ソート中にデータが流出してTiFlashがクラッシュする可能性がある問題を修正 [#9999](https://github.com/pingcap/tiflash/issues/9999) @[windtalker](https://github.com/windtalker)
    -   TiFlashが`Exception: Block schema mismatch`を含むSQL文を実行する際に`GROUP BY ... WITH ROLLUP`エラーを返す可能性がある問題を修正しました。 [#10110](https://github.com/pingcap/tiflash/issues/10110) @[gengliqi](https://github.com/gengliqi)
    -   分散storageとコンピューティングアーキテクチャで、 TiFlashコンピューティング ノードがリージョンピアを追加するターゲット ノードとして誤って選択される可能性がある問題を修正 [#9750](https://github.com/pingcap/tiflash/issues/9750) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   特定の状況でTiFlash が予期せず終了した場合に、エラー スタック トレースの出力に失敗することがある問題を修正 [#9902](https://github.com/pingcap/tiflash/issues/9902) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   大量のデータをインポートした後にTiFlash が高いメモリ使用量を維持する可能性がある問題を修正 [#9812](https://github.com/pingcap/tiflash/issues/9812) @[CalvinNeo](https://github.com/CalvinNeo)
    -   `profiles.default.init_thread_count_scale`が`0`に設定されている場合、 TiFlash の起動がブロックされる場合がある問題を修正 [#9906](https://github.com/pingcap/tiflash/issues/9906) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   パーティションテーブルで`ALTER TABLE ... RENAME COLUMN`を実行した後、そのパーティションテーブルに対するクエリがエラーを返すことがある問題を修正 [#9787](https://github.com/pingcap/tiflash/issues/9787) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)ポティガー
    -   クエリに仮想列が含まれ、リモート読み取りがトリガーされた場合に`Not found column`エラーが発生する可能性がある問題を修正 [#9561](https://github.com/pingcap/tiflash/issues/9561) @[guo-shaoge](https://github.com/guo-shaoge)
    -   クラスター内のテーブルに多数の`ENUM`タイプのカラムが含まれている場合、 TiFlash が大量のメモリを消費する可能性がある問題を修正 [#9947](https://github.com/pingcap/tiflash/issues/9947) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   16 MiB を超えるデータを 1 行挿入するとTiFlash が再起動に失敗することがある問題を修正 [#10052](https://github.com/pingcap/tiflash/issues/10052) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   ベクター インデックスを持つテーブルに新しいデータが挿入された後、 TiFlash が一部のディスク データを正しくクリーンアップできず、ディスク容量が異常に消費される問題を修正 [#9946](https://github.com/pingcap/tiflash/issues/9946) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   TiFlashが同じテーブルに複数のベクターインデックスを作成した後、以前に作成されたベクターインデックスを予期せず削除し、パフォーマンスの低下を引き起こす可能性がある問題を修正しました [#9971](https://github.com/pingcap/tiflash/issues/9971) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   TiFlashが分散storageおよびコンピューティングアーキテクチャでベクトルインデックスを使用してベクトル検索クエリを高速化できない可能性がある問題を修正 [#9847](https://github.com/pingcap/tiflash/issues/9847) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    -   TiFlash が分散storageおよびコンピューティングアーキテクチャで大量の`tag=EnumParseOverflowContainer`ログを出力する可能性がある問題を修正 [#9955](https://github.com/pingcap/tiflash/issues/9955) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   `SELECT ... AS OF TIMESTAMP`クエリの実行時にTiFlash が期待どおりにLearnerの読み取りをスキップしない問題を修正 [#10046](https://github.com/pingcap/tiflash/issues/10046) @[CalvinNeo](https://github.com/CalvinNeo)
    -   リージョンのキー範囲が不規則なスナップショットを処理するとTiFlash がpanicになる問題を修正 [#10147](https://github.com/pingcap/tiflash/issues/10147) @[JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   バックアップと復元 (BR)

        -   データ復元中に SST ファイルのダウンロードを繰り返すと、極端な場合に TiKV がpanicを引き起こす可能性がある問題を修正 [#18335](https://github.com/tikv/tikv/issues/18335) @[3pointer](https://github.com/3pointer)
        -   `status`を使用してログバックアップタスクをクエリした際に、結果に`br log status --json`フィールドが欠落する問題を修正 [#57959](https://github.com/pingcap/tidb/issues/57959) @[Leavrth](https://github.com/Leavrth)
        -   TiKVへのリクエスト送信時に`rpcClient is idle`エラーが発生し、 BRの復元に失敗する問題を修正します。 [#58845](https://github.com/pingcap/tidb/issues/58845) @[Tristan1900](https://github.com/Tristan1900)
        -   PDにアクセスできないために致命的なエラーが発生した場合にログバックアップが正常に終了しない問題を修正 [#18087](https://github.com/tikv/tikv/issues/18087) @[YuJuncen](https://github.com/YuJuncen)
        -   PITR が 3072 バイトを超えるインデックスの復元に失敗する問題を修正 [#58430](https://github.com/pingcap/tidb/issues/58430) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   レプリケーション トラフィックがダウンストリーム Kafka のトラフィックしきい値を超えた後に変更フィードが停止する可能性がある問題を修正 [#12110](https://github.com/pingcap/tiflow/issues/12110) @[3AceShowHand](https://github.com/3AceShowHand)ハンド
        -   `pulsar+http`または`pulsar+https`プロトコルが使用されている場合に Kafka シンクのディスパッチ ルールが有効にならない問題を修正 [#12068](https://github.com/pingcap/tiflow/issues/12068) @[SandeepPadhi](https://github.com/SandeepPadhi)
        -   TiCDCがPDリーダーの移行を時間内に監視できず、レプリケーションレイテンシーが増加する問題を修正 [#11997](https://github.com/pingcap/tiflow/issues/11997) @[lidezhu](https://github.com/lidezhu)
        -   TiCDCがAvroプロトコル経由で`default NULL` SQLステートメントを複製する際にエラーを報告する問題を修正しました [#11994](https://github.com/pingcap/tiflow/issues/11994) @[wk989898](https://github.com/wk989898)
        -   アップストリームで新しく追加された列のデフォルト値が`NOT NULL`から`NULL`に変更された後、ダウンストリームのその列のデフォルト値が正しくない問題を修正します [#12037](https://github.com/pingcap/tiflow/issues/12037) @[wk989898](https://github.com/wk989898)
        -   PDスケールイン後にTiCDCがPDに正しく接続できない問題を修正 [#12004](https://github.com/pingcap/tiflow/issues/12004) @[lidezhu](https://github.com/lidezhu)
        -   TiCDCが`CREATE TABLE IF NOT EXISTS`または`CREATE DATABASE IF NOT EXISTS`ステートメントを複製する際にpanic可能性がある問題を修正しました [#11839](https://github.com/pingcap/tiflow/issues/11839) @[CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDBデータ移行（DM）

        -   TLSと`start-task`の両方が設定されている場合、 `shard-mode`の事前チェックが失敗する問題を修正 [#11842](https://github.com/pingcap/tiflow/issues/11842) @[sunxiaoguang](https://github.com/sunxiaoguang)

    -   TiDB Lightning

        -   高同時実行シナリオでクラウドstorageからデータをインポートする際にパフォーマンスが低下する問題を修正 [#57413](https://github.com/pingcap/tidb/issues/57413) @[xuanyu66](https://github.com/xuanyu66)
        -   TiDB Lightningを使用してデータをインポートする際に、エラーレポートの出力が切り詰められる問題を修正しました [#58085](https://github.com/pingcap/tidb/issues/58085) @[lance6716](https://github.com/lance6716)
        -   ログが適切に匿名化されていない問題を修正 [#59086](https://github.com/pingcap/tidb/issues/59086) @[GMHDBJD](https://github.com/GMHDBJD)
        -   外部アカウントを使用してGCSstorage操作を実行する際に、認証が`context canceled`エラーで失敗する問題を修正しました [#60155](https://github.com/pingcap/tidb/issues/60155) @[lance6716](https://github.com/lance6716)
        -   TiDB LightningがクラウドstorageからParquetファイルをTiDBにインポートする際に数時間停止する問題を修正します [#60224](https://github.com/pingcap/tidb/issues/60224) @[joechenrh](https://github.com/joechenrh)
        -   TiDB Lightningが大量のデータをインポートする際に、SSTファイルをTiKVクラスターに書き込んだり取り込んだりする際にメモリ不足（OOM）になる可能性がある問題を修正しました。 [#59947](https://github.com/pingcap/tidb/issues/59947) @[OliverS929](https://github.com/OliverS929)
        -   テーブル作成時の最大QPSが低いことと`information_schema.tables`へのアクセスが遅いことが原因で、数百万のテーブルが存在するシナリオでTiDB Lightningがスキーマジョブのディスパッチが遅くなる問題を修正しました [#58141](https://github.com/pingcap/tidb/issues/58141) @[D3Hunter](https://github.com/D3Hunter)

    -   NGモニタリング

        -   DocDBが高負荷時にメモリを過剰に消費する問題を修正し、DocDBのオプションのバックエンドとしてSQLiteを使用する [#267](https://github.com/pingcap/ng-monitoring/issues/267) @[mornyx](https://github.com/mornyx)
        -   時系列データのカーディナリティが高い場合にTSDBがメモリを過剰に消費する問題を修正し、TSDBのメモリ設定オプションを提供します [#295](https://github.com/pingcap/ng-monitoring/issues/295) @[mornyx](https://github.com/mornyx)
