---
title: TiDB 4.0.16 Release Notes
---

# TiDB4.0.16リリースノート {#tidb-4-0-16-release-notes}

発売日：2021年12月17日

TiDBバージョン：4.0.16

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   v4.0.16より前では、TiDBが不正なUTF-8文字列をRealタイプに変換すると、エラーが直接報告されます。 v4.0.16以降、TiDBは文字列[＃11466](https://github.com/tikv/tikv/issues/11466)の有効なUTF-8プレフィックスに従って変換を処理します。

-   ツール

    -   TiCDC

        -   TiCDCがKafkaクラスターに大きすぎるメッセージを送信しないように、KafkaSink1のデフォルト値を`max-message-bytes`に変更します[＃2962](https://github.com/pingcap/tiflow/issues/2962)
        -   Kafka Sink `partition-num`のデフォルト値を3に変更して、TiCDCがKafkaパーティション間でメッセージをより均等に分散するようにします[＃3337](https://github.com/pingcap/tiflow/issues/3337)

## 改善 {#improvements}

-   TiDB

    -   Grafanaバージョンを7.5.7から7.5.11にアップグレードします

-   TiKV

    -   バックアップと復元を使用してデータを復元するとき、またはTiDB Lightning [＃11469](https://github.com/tikv/tikv/issues/11469)のローカルバックエンドを使用してデータをインポートするときに、zstdアルゴリズムを採用してSSTファイルを圧縮することにより、ディスク容量の消費を削減します。

-   ツール

    -   バックアップと復元（BR）

        -   復元の堅牢性を向上させる[＃27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiCDC

        -   EtcdWorkerにティック頻度制限を追加して、頻繁なetcd書き込みがPDサービスに影響を与えないようにします[＃3112](https://github.com/pingcap/tiflow/issues/3112)
        -   TiKVリロードのレート制限制御を最適化して、チェンジフィード初期化中のgPRC輻輳を低減します[＃3110](https://github.com/pingcap/tiflow/issues/3110)

## バグの修正 {#bug-fixes}

-   TiDB

    -   コスト見積もりのために範囲をポイントに変換するときに統計モジュールのオーバーフローによって引き起こされるクエリpanicを修正します[＃23625](https://github.com/pingcap/tidb/issues/23625)
    -   `ENUM`種類のデータをそのような関数のパラメーターとして使用する場合の制御関数（ `IF`や`CASE WHEN`など）の誤った結果を修正します[＃23114](https://github.com/pingcap/tidb/issues/23114)
    -   `tidb_enable_vectorized_expression` （ `on`または`off` ） [＃29434](https://github.com/pingcap/tidb/issues/29434)の値が異なるために、 `GREATEST`関数が一貫性のない結果を返す問題を修正します。
    -   場合によってはプレフィックスインデックスにインデックス結合を適用するときのpanicを修正します[＃24547](https://github.com/pingcap/tidb/issues/24547)
    -   プランナーが`join` 、場合によっては[＃28087](https://github.com/pingcap/tidb/issues/28087)の無効なプランをキャッシュする可能性がある問題を修正します
    -   `sql_mode`が空の場合にTiDBがnull以外の列に`null`を挿入できないバグを修正します[＃11648](https://github.com/pingcap/tidb/issues/11648)
    -   `GREATEST`および`LEAST`関数の間違った結果タイプを修正します[＃29019](https://github.com/pingcap/tidb/issues/29019)
    -   グローバルレベルの特権を付与および取り消すために`grant`および`revoke`の操作を実行するときの`privilege check fail`のエラーを修正します[＃29675](https://github.com/pingcap/tidb/issues/29675)
    -   `ENUM`データ型[＃29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのpanicを修正します
    -   ベクトル化された式[＃29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の誤った結果を修正します
    -   ベクトル化された式[＃28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の誤った結果を修正します
    -   楽観的なトランザクションの競合により、トランザクションが互いにブロックする可能性があるという問題を修正します[＃11148](https://github.com/tikv/tikv/issues/11148)
    -   `auto analyze`の結果からの不完全なログ情報の問題を修正します[＃29188](https://github.com/pingcap/tidb/issues/29188)
    -   `SQL_MODE`が「NO_ZERO_IN_DATE」の場合に無効なデフォルトの日付を使用してもエラーが報告されない問題を修正します[＃26766](https://github.com/pingcap/tidb/issues/26766)
    -   Grafanaのコプロセッサーキャッシュパネルにメトリックが表示されない問題を修正します。これで、 `miss`は`hits`の数を[＃26338](https://github.com/pingcap/tidb/issues/26338)し`evict`
    -   同じパーティションを同時に切り捨てると、DDLステートメントがスタックする問題を修正します[＃26229](https://github.com/pingcap/tidb/issues/26229)
    -   `Decimal`から[＃29417](https://github.com/pingcap/tidb/issues/29417)に変換するときに長さ情報が間違っている問題を修正し`String`
    -   `NATURAL JOIN`を使用して複数のテーブルを結合する場合のクエリ結果の余分な列の問題を修正します[＃29481](https://github.com/pingcap/tidb/issues/29481)
    -   `IndexScan`がプレフィックスインデックス[＃29711](https://github.com/pingcap/tidb/issues/29711)を使用しているときに、 `TopN`が誤って`indexPlan`にプッシュダウンされる問題を修正します。
    -   `DOUBLE`タイプの自動インクリメント列を使用してトランザクションを再試行すると、データが破損する問題を修正します[＃29892](https://github.com/pingcap/tidb/issues/29892)

-   TiKV

    -   リージョンマージ、ConfChange、およびスナップショットが極端な条件で同時に発生するときに発生するpanicの問題を修正します[＃11475](https://github.com/tikv/tikv/issues/11475)
    -   10進数の除算結果がゼロの場合の負の符号の問題を修正します[＃29586](https://github.com/pingcap/tidb/issues/29586)
    -   インスタンスごとのgRPCリクエストの平均レイテンシがTiKVメトリクス[＃11299](https://github.com/tikv/tikv/issues/11299)で不正確であるという問題を修正します
    -   ダウンストリームデータベースが欠落しているときに発生するTiCDCpanicの問題を修正します[＃11123](https://github.com/tikv/tikv/issues/11123)
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正します[＃11047](https://github.com/tikv/tikv/issues/11047)
    -   `Max`関数の`Int64`タイプが符号付き整数であるかどうかを[＃10158](https://github.com/tikv/tikv/issues/10158)が正しく識別できない問題を修正し`Min` 。これにより、 `Max` /911の誤った計算結果が発生し`Min` 。
    -   輻輳エラー[＃11082](https://github.com/tikv/tikv/issues/11082)が原因でCDCがスキャンの再試行を頻繁に追加する問題を修正します

-   PD

    -   TiKVノードが削除された後に発生するpanicの問題を修正します[＃4344](https://github.com/tikv/pd/issues/4344)
    -   スタックしたリージョンシンカー[＃3936](https://github.com/tikv/pd/issues/3936)によって引き起こされる遅いリーダー選出を修正
    -   エビクトリーダースケジューラが異常なピアのあるリージョンをスケジュールできることをサポートする[＃4093](https://github.com/tikv/pd/issues/4093)

-   TiFlash

    -   ライブラリ`nsl`がないために、一部のプラットフォームでTiFlashが起動しない問題を修正します。

-   ツール

    -   TiDB Binlog

        -   1GBを超えるトランザクションを転送するときにDrainerが終了するバグを修正します[＃28659](https://github.com/pingcap/tidb/issues/28659)

    -   TiCDC

        -   チェンジフィードチェックポイントラグ[＃3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正しました
        -   コンテナ環境でのOOMの修正[＃1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数のTiKVがクラッシュしたとき、または強制的に再起動したときのTiCDCレプリケーションの中断の問題を修正します[＃3288](https://github.com/pingcap/tiflow/issues/3288)
        -   DDLの処理後のメモリリークの問題を修正[＃3174](https://github.com/pingcap/tiflow/issues/3174)
        -   ErrGCTTLExceededエラーが発生したときにchangefeedが十分に速く失敗しない問題を修正します[＃3111](https://github.com/pingcap/tiflow/issues/3111)
        -   アップストリームTiDBインスタンスが予期せず終了したときにTiCDCレプリケーションタスクが終了する可能性がある問題を修正します[＃3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKVが同じリージョン[＃2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDCプロセスがpanicになる可能性がある問題を修正します。
        -   TiCDCによって生成されるKafkaメッセージの量が[＃2962](https://github.com/pingcap/tiflow/issues/2962)によって制約されないという問題を修正し`max-message-size`
        -   チェンジフィードがない場合に`tikv_cdc_min_resolved_ts_no_change_for_1m`がアラートを出し続ける問題を修正します[＃11017](https://github.com/tikv/tikv/issues/11017)
        -   Kafkaメッセージの書き込み中にエラーが発生したときにTiCDC同期タスクが一時停止する可能性がある問題を修正します[＃2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効になっている場合、有効なインデックスのない一部のパーティションテーブルが無視される可能性がある問題を修正します[＃2834](https://github.com/pingcap/tiflow/issues/2834)
        -   新しいチェンジフィードを作成するときのメモリリークの問題を修正します[＃2389](https://github.com/pingcap/tiflow/issues/2389)
        -   シンクコンポーネントが早期に解決されたtsを進めるためにデータの一貫性が失われる可能性がある問題を修正します[＃3503](https://github.com/pingcap/tiflow/issues/3503)
        -   ストックデータのスキャンに時間がかかりすぎると、TiKVがGCを実行するためにストックデータのスキャンが失敗する可能性がある問題を修正します[＃2470](https://github.com/pingcap/tiflow/issues/2470)
        -   changefeedupdateコマンドがグローバルコマンドラインパラメーターを認識しない問題を修正します[＃2803](https://github.com/pingcap/tiflow/issues/2803)
