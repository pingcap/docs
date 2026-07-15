---
title: TiDB 6.5.2 Release Notes
summary: TiDB 6.5.2 における互換性の変更、改善、およびバグ修正について説明します。
---

# TiDB 6.5.2 リリースノート {#tidb-6-5-2-release-notes}

発売日：2023年4月21日

TiDB バージョン: 6.5.2

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup)

## 互換性の変更 {#compatibility-changes}

-   TiCDCは、Avro で`FLOAT`データのエンコードが正しくない問題を修正しました。 [＃8490](https://github.com/pingcap/tiflow/issues/8490) @ [3AceShowHand](https://github.com/3AceShowHand)

    TiCDC クラスターを v6.5.2 またはそれ以降の v6.5.x バージョンにアップグレードする際、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整し、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。

-   パーティションテーブルをストレージサービスにレプリケーションする際にデータ損失が発生する可能性がある問題を修正するため、TiCDC [`sink.enable-partition-separator`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)構成項目のデフォルト値が`false`から`true`に変更されました。これは、テーブル内のパーティションがデフォルトで別々のディレクトリに保存されることを意味します。データ損失の問題を回避するため、この値は`true`のままにしておくことをお勧めします[＃8724](https://github.com/pingcap/tiflow/issues/8724) @ [CharlesCheung96](https://github.com/CharlesCheung96)

## 改善点 {#improvements}

-   TiDB

    -   プリペアドプランキャッシュで`BatchPointGet`実行プランのキャッシュをサポート [＃42125](https://github.com/pingcap/tidb/issues/42125) @ [qw4990](https://github.com/qw4990)
    -   インデックス結合より多くの SQL 形式をサポート [＃40505](https://github.com/pingcap/tidb/issues/40505) @ [Yisaer](https://github.com/Yisaer)
    -   一部のインデックスマージリーダーのログレベルを`"info"`から`"debug"` に変更します [＃41949](https://github.com/pingcap/tidb/issues/41949) @ [yibin87](https://github.com/yibin87)
    -   範囲パーティションテーブルに Limit を設定した`distsql_concurrency`設定を最適化して、クエリのレイテンシーを削減します。 [＃41480](https://github.com/pingcap/tidb/issues/41480) @ [you06](https://github.com/you06)

-   TiFlash

    -   TiFlash読み取り時のタスク スケジューリングの CPU 消費を削減[＃6495](https://github.com/pingcap/tiflash/issues/6495) @ [JinheLin](https://github.com/JinheLin)
    -   デフォルト設定でBRおよびTiDB LightningからTiFlashへのデータインポートのパフォーマンスを向上 [＃7272](https://github.com/pingcap/tiflash/issues/7272) @ [breezewish](https://github.com/breezewish)

-   ツール

    -   TiCDC

        -   TiCDC オープン API v2.0 をリリース [＃8743](https://github.com/pingcap/tiflow/issues/8743) @ [sdojjy](https://github.com/sdojjy)
        -   TiCDC の OOM 問題を防ぐために`gomemlimit`を導入する[＃8675](https://github.com/pingcap/tiflow/issues/8675) @ [amyangfei](https://github.com/amyangfei)
        -   `UPDATE`ステートメントを[＃8057](https://github.com/pingcap/tiflow/issues/8057) @ [amyangfei](https://github.com/amyangfei)つ実行するシナリオでは、マルチステートメントアプローチを使用してレプリケーションのパフォーマンスを最適化します。
        -   災害復旧シナリオにおけるスループットの向上とRTOの短縮のために、REDOアプライヤでのトランザクション分割をサポートする[＃8318](https://github.com/pingcap/tiflow/issues/8318) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   REDOログへのDDLイベントの適用をサポート [＃8361](https://github.com/pingcap/tiflow/issues/8361) @ [CharlesCheung96](https://github.com/CharlesCheung96)

    -   TiDB Lightning

        -   BOM ヘッダーを含む CSV データファイルのインポートをサポート [＃40744](https://github.com/pingcap/tidb/issues/40744) @ [dsdashun](https://github.com/dsdashun)

## バグ修正 {#bug-fixes}

-   TiDB
    -   キャッシュテーブルに新しい列が追加された後、列のデフォルト値ではなく値が`NULL`なる問題を修正しました。 [＃42928](https://github.com/pingcap/tidb/issues/42928) @ [lqs](https://github.com/lqs)
    -   多数のパーティションとTiFlashレプリカを持つパーティション テーブルに対して`TRUNCATE TABLE`実行するときに書き込み競合によって発生する DDL 再試行の問題を修正しました。 [＃42940](https://github.com/pingcap/tidb/issues/42940) @ [mjonss](https://github.com/mjonss)
    -   `DROP TABLE`操作が実行されているときに`ADMIN SHOW DDL JOBS`結果にテーブル名が表示されない問題を修正[＃42268](https://github.com/pingcap/tidb/issues/42268) @ [tiancaiamao](https://github.com/tiancaiamao)
    -   cgroup 情報の読み取りエラーにより、TiDBサーバーが起動できない問題を修正しました。エラー メッセージは「cgroup v1 からファイルメモリ.stat を読み取れません: /sys/メモリ.stat をオープンすると、そのようなファイルまたはディレクトリが見つかりません」です[＃42659](https://github.com/pingcap/tidb/issues/42659) @ [hawkingrei](https://github.com/hawkingrei)
    -   DDLデータバックフィルを実行するときにトランザクションで頻繁に発生する書き込み競合を修正 [＃24427](https://github.com/pingcap/tidb/issues/24427) @ [mjonss](https://github.com/mjonss)
    -   実行プラン[＃41622](https://github.com/pingcap/tidb/issues/41622) @ [tiancaiamao](https://github.com/tiancaiamao)を生成する際に不整合な InfoSchema が取得され、TiDBpanicが発生する問題を修正しました。
    -   DDLを使用して浮動小数点型を変更し、長さを変更せずに小数点以下の桁数を減らしても、古いデータが同じままになる問題を修正しました[＃41281](https://github.com/pingcap/tidb/issues/41281) @ [zimulala](https://github.com/zimulala)
    -   トランザクション内で`PointUpdate`実行した後、TiDB が`SELECT`文に対して誤った結果を返す問題を修正しました。 [＃28011](https://github.com/pingcap/tidb/issues/28011) @ [zyguan](https://github.com/zyguan)
    -   カーソルフェッチを使用し、実行、フェッチ、およびクローズの間に他のステートメントを実行すると、フェッチおよびクローズコマンドが誤った結果を返したり、TiDB がpanicたりする可能性がある問題を修正しました[＃40094](https://github.com/pingcap/tidb/issues/40094) @ [YangKeao](https://github.com/YangKeao)
    -   `INSERT IGNORE`と`REPLACE`ステートメントが値を変更しないキーをロックしない問題を修正しました [＃42121](https://github.com/pingcap/tidb/issues/42121) @ [zyguan](https://github.com/zyguan)
    -   実行中にTiFlash が生成された列に対してエラーを報告する問題を修正[＃40663](https://github.com/pingcap/tidb/issues/40663) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   単一のSQL文に異なるパーティションテーブルが出現した場合にTiDBが誤った結果を生成する可能性がある問題を修正[＃42135](https://github.com/pingcap/tidb/issues/42135) @ [mjonss](https://github.com/mjonss)
    -   プリペアドプランキャッシュが有効な場合にフルインデックススキャンでエラーが発生する可能性がある問題を修正[＃42150](https://github.com/pingcap/tidb/issues/42150) @ [fzzf678](https://github.com/fzzf678)
    -   プリペアドプランキャッシュが有効な場合に IndexMerge が誤った結果を生成する可能性がある問題を修正[＃41828](https://github.com/pingcap/tidb/issues/41828) @ [qw4990](https://github.com/qw4990)
    -   `max_prepared_stmt_count`の設定が反映されない問題を修正 [＃39735](https://github.com/pingcap/tidb/issues/39735) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)
    -   グローバルメモリ制御が、メモリ使用量が`tidb_server_memory_limit_sess_min_size` 未満の SQL 文を誤って強制終了する可能性がある問題を修正しました。 [＃42662](https://github.com/pingcap/tidb/issues/42662) @ [XuHuaiyu](https://github.com/XuHuaiyu)
    -   パーティションテーブルの動的トリミングモードでインデックス結合によりpanicが発生する可能性がある問題を修正しました。 [＃40596](https://github.com/pingcap/tidb/issues/40596) @ [tiancaiamao](https://github.com/tiancaiamao)

-   TiKV

    -   TiKVがcgroupパスを処理するときに`:`文字目を正しく解析しない問題を修正しました [＃14538](https://github.com/tikv/tikv/issues/14538) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)

-   PD

    -   PD が予期せず複数のラーナーをリージョンに追加する可能性がある問題を修正しました。 [＃5786](https://github.com/tikv/pd/issues/5786) @ [HunDunDM](https://github.com/HunDunDM)
    -   配置ルールの切り替えにより、リーダーの分布が不均等になる可能性がある問題を修正しました。 [＃6195](https://github.com/tikv/pd/issues/6195) @ [bufferflies](https://github.com/bufferflies)

-   TiFlash

    -   TiFlashが生成された列を認識できない問題を修正 [＃6801](https://github.com/pingcap/tiflash/issues/6801) @ [guo-shaoge](https://github.com/guo-shaoge)
    -   特定のケースで小数点以下の桁が切り上げられない問題を修正[＃7022](https://github.com/pingcap/tiflash/issues/7022) @ [LittleFall](https://github.com/LittleFall)
    -   特定のケースで 10 進キャストが誤って切り上げられる問題を修正しました [＃6994](https://github.com/pingcap/tiflash/issues/6994) @ [windtalker](https://github.com/windtalker)
    -   新しい照合順序を有効にした後に TopN/Sort 演算子が誤った結果を生成する問題を修正しました [＃6807](https://github.com/pingcap/tiflash/issues/6807) @ [xzhangxian1008](https://github.com/xzhangxian1008)
    -   TiCDC の非互換性によるTiFlashプロセス障害の問題を修正[＃7212](https://github.com/pingcap/tiflash/issues/7212) @ [hongyunyan](https://github.com/hongyunyan)

-   ツール

    -   Backup & Restore (BR)

        -   TiDBクラスタにPITRバックアップタスクがない場合に頻度`resolve lock`が高すぎる問題を修正 [＃40759](https://github.com/pingcap/tidb/issues/40759) @ [joccau](https://github.com/joccau)
        -   PITRリカバリプロセス中に分割リージョンの再試行の待機時間が不十分になる問題を修正 [＃42001](https://github.com/pingcap/tidb/issues/42001) @ [joccau](https://github.com/joccau)

    -   TiCDC

        -   TiCDCがオブジェクトストレージにデータを複製するときにパーティションセパレーターが機能しない問題を修正しました [＃8581](https://github.com/pingcap/tiflow/issues/8581) @ [CharlesCheung96](https://github.com/CharlesCheung96) @ [Rustin170506](https://github.com/Rustin170506)
        -   TiCDC がオブジェクトストレージにデータを複製するときにテーブル スケジューリングによってデータ損失が発生する可能性がある問題を修正しました。 [＃8256](https://github.com/pingcap/tiflow/issues/8256) @ [zhaoxinyu](https://github.com/zhaoxinyu)
        -   非再入可能DDL文によりレプリケーションが停止する問題を修正 [＃8662](https://github.com/pingcap/tiflow/issues/8662) @ [hicqu](https://github.com/hicqu)
        -   TiCDC がオブジェクトストレージにデータを複製するときに、TiCDC スケーリングによってデータ損失が発生する可能性がある問題を修正しました。 [＃8666](https://github.com/pingcap/tiflow/issues/8666) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `db sorter`のメモリ使用量が`cgroup memory limit` で制御されない問題を修正 [＃8588](https://github.com/pingcap/tiflow/issues/8588) @ [amyangfei](https://github.com/amyangfei)
        -   Redo ログの適用中に特別なケースでデータ損失が発生する可能性がある問題を修正しました [＃8591](https://github.com/pingcap/tiflow/issues/8591) @ [CharlesCheung96](https://github.com/CharlesCheung96)
        -   `db sorter`のメモリ使用量が`cgroup memory limit` で制御されない問題を修正 [＃8588](https://github.com/pingcap/tiflow/issues/8588) @ [amyangfei](https://github.com/amyangfei)
        -   データレプリケーション中の`UPDATE`と`INSERT`ステートメントの順序が乱れると、 `Duplicate entry`エラーが発生する可能性がある問題を修正しました。 [＃8597](https://github.com/pingcap/tiflow/issues/8597) @ [sdojjy](https://github.com/sdojjy)
        -   PDとTiCDC 間のネットワーク分離によって発生するTiCDCサービスの異常終了問題を修正 [＃8562](https://github.com/pingcap/tiflow/issues/8562) @ [overvenus](https://github.com/overvenus)
        -   Kubernetes で TiCDC クラスターの正常なアップグレードが失敗する問題を修正しました [＃8484](https://github.com/pingcap/tiflow/issues/8484) @ [overvenus](https://github.com/overvenus)
        -   すべての下流 Kafka サーバーが利用できない場合に TiCDCサーバーがパニックになる問題を修正[＃8523](https://github.com/pingcap/tiflow/issues/8523) @ [3AceShowHand](https://github.com/3AceShowHand)
        -   変更フィードを再開するとデータが失われる可能性がある、またはチェックポイントがに進めない問題を修正しました。 [＃8242](https://github.com/pingcap/tiflow/issues/8242) @ [overvenus](https://github.com/overvenus)
