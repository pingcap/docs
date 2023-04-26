---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 リリースノート {#tidb-4-0-16-release-notes}

発売日：2021年12月17日

TiDB バージョン: 4.0.16

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   v4.0.16 より前では、TiDB が不正な UTF-8 文字列を Real 型に変換すると、エラーが直接報告されます。 v4.0.16 以降、TiDB は文字列[#11466](https://github.com/tikv/tikv/issues/11466)の正当な UTF-8 プレフィックスに従って変換を処理します。

-   ツール

    -   TiCDC

        -   Kafka Sink `max-message-bytes`のデフォルト値を 1 MB に変更して、TiCDC が大きすぎるメッセージを Kafka クラスターに送信しないようにします[#2962](https://github.com/pingcap/tiflow/issues/2962)
        -   Kafka Sink `partition-num`のデフォルト値を 3 に変更して、TiCDC が Kafka パーティション間でメッセージをより均等に分散するようにします[#3337](https://github.com/pingcap/tiflow/issues/3337)

## 改良点 {#improvements}

-   TiDB

    -   Grafana のバージョンを 7.5.7 から 7.5.11 にアップグレードする

-   TiKV

    -   バックアップと復元を使用してデータを復元するとき、またはTiDB Lightning [#11469](https://github.com/tikv/tikv/issues/11469)のローカル バックエンドを使用してデータをインポートするときに、zstd アルゴリズムを採用して SST ファイルを圧縮することにより、ディスク容量の消費を削減します。

-   ツール

    -   バックアップと復元 (BR)

        -   復元の堅牢性の向上[#27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiCDC

        -   EtcdWorker にティック頻度制限を追加して、頻繁な etcd 書き込みが PD サービスに影響を与えないようにします[#3112](https://github.com/pingcap/tiflow/issues/3112)
        -   TiKV リロードのレート制限制御を最適化して、変更フィードの初期化中の gPRC の輻輳を軽減します[#3110](https://github.com/pingcap/tiflow/issues/3110)

## バグの修正 {#bug-fixes}

-   TiDB

    -   コストpanicのために範囲をポイントに変換するときに、統計モジュールのオーバーフローによって引き起こされるクエリ パニックを修正します[#23625](https://github.com/pingcap/tidb/issues/23625)
    -   制御関数( `IF`や`CASE WHEN`など) のような関数のパラメーターとして`ENUM`型のデータを使用する場合の誤った結果を修正します[#23114](https://github.com/pingcap/tidb/issues/23114)
    -   `tidb_enable_vectorized_expression` ( `on`または`off` ) [#29434](https://github.com/pingcap/tidb/issues/29434)の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します。
    -   場合によっては、プレフィックス インデックスにインデックス結合を適用する際のpanicを修正します[#24547](https://github.com/pingcap/tidb/issues/24547)
    -   Planner が`join`の無効なプランをキャッシュする場合がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   `sql_mode`が空の場合、TiDB が null 以外の列に`null`を挿入できないバグを修正[#11648](https://github.com/pingcap/tidb/issues/11648)
    -   `GREATEST`および`LEAST`関数の誤った結果タイプを修正します[#29019](https://github.com/pingcap/tidb/issues/29019)
    -   `grant`および`revoke`操作を実行してグローバル レベルの権限を付与および取り消すときの`privilege check fail`エラーを修正します[#29675](https://github.com/pingcap/tidb/issues/29675)
    -   `ENUM`データ型[#29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用したときのpanicを修正
    -   ベクトル化された式[#29244](https://github.com/pingcap/tidb/issues/29244)の`microsecond`関数の間違った結果を修正
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の`hour`関数の間違った結果を修正
    -   楽観的トランザクションの競合により、トランザクションが相互にブロックされる可能性があるという問題を修正します[#11148](https://github.com/tikv/tikv/issues/11148)
    -   `auto analyze`結果[#29188](https://github.com/pingcap/tidb/issues/29188)の不完全なログ情報の問題を修正
    -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [#26766](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。
    -   Grafana のコプロセッサー Cache パネルにメトリックが表示されない問題を修正します。これで、Grafana は`hits` / `miss` / `evict` [#26338](https://github.com/pingcap/tidb/issues/26338)の数を表示します
    -   同じパーティションを同時に切り捨てると DDL ステートメントがスタックする問題を修正します[#26229](https://github.com/pingcap/tidb/issues/26229)
    -   `Decimal`を`String` [#29417](https://github.com/pingcap/tidb/issues/29417)に変換するときに長さ情報が間違っている問題を修正
    -   `NATURAL JOIN`を使用して複数のテーブルを結合する場合に、クエリ結果に余分な列が含まれる問題を修正します[#29481](https://github.com/pingcap/tidb/issues/29481)
    -   `IndexScan`プレフィックス インデックス[#29711](https://github.com/pingcap/tidb/issues/29711)を使用すると、 `TopN`が誤って`indexPlan`にプッシュ ダウンされる問題を修正します。
    -   タイプ`DOUBLE`の自動インクリメント列でトランザクションを再試行するとデータが破損する問題を修正します[#29892](https://github.com/pingcap/tidb/issues/29892)

-   TiKV

    -   極端な状況でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   10 進数の除算結果がゼロ[#29586](https://github.com/pingcap/tidb/issues/29586)の場合の負号の問題を修正
    -   インスタンスごとの gRPC リクエストの平均レイテンシーが TiKV メトリクスで不正確である問題を修正します[#11299](https://github.com/tikv/tikv/issues/11299)
    -   ダウンストリーム データベースが見つからない場合に発生する TiCDCpanicの問題を修正します[#11123](https://github.com/tikv/tikv/issues/11123)
    -   チャネルがいっぱいになるとRaft接続が切断される問題を修正します[#11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDB が`Max` / `Min`関数の`Int64`型が符号付き整数かどうかを正しく識別できず、 `Max` / `Min` [#10158](https://github.com/tikv/tikv/issues/10158)という誤った計算結果になる問題を修正
    -   Congest エラー[#11082](https://github.com/tikv/tikv/issues/11082)により、CDC が頻繁にスキャンの再試行を追加する問題を修正します。

-   PD

    -   TiKV ノードが削除された後に発生するpanicの問題を修正します[#4344](https://github.com/tikv/pd/issues/4344)
    -   リージョン シンサー[#3936](https://github.com/tikv/pd/issues/3936)のスタックによるリーダー選出の遅さを修正
    -   エビクト リーダー スケジューラが異常なピアを含むリージョンをスケジュールできるようにするサポート[#4093](https://github.com/tikv/pd/issues/4093)

-   TiFlash

    -   ライブラリ`nsl`が存在しないため、一部のプラットフォームでTiFlash が起動しない問題を修正

-   ツール

    -   TiDBBinlog

        -   1 GB を超えるトランザクションを転送するとDrainerが終了するバグを修正します[#28659](https://github.com/pingcap/tidb/issues/28659)

    -   TiCDC

        -   changefeed チェックポイントラグ[#3010](https://github.com/pingcap/tiflow/issues/3010)の負の値のエラーを修正します。
        -   コンテナ環境で OOM を修正する[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュしたとき、または強制再起動中に TiCDC レプリケーションが中断する問題を修正します[#3288](https://github.com/pingcap/tiflow/issues/3288)
        -   DDL [#3174](https://github.com/pingcap/tiflow/issues/3174)の処理後のメモリリークの問題を修正します。
        -   ErrGCTTLExceeded エラーが発生したときに changefeed が十分な速さで失敗しないという問題を修正します[#3111](https://github.com/pingcap/tiflow/issues/3111)
        -   アップストリームの TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正します。
        -   TiCDC によって生成される Kafka メッセージの量が`max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)によって制限されないという問題を修正します
        -   `tikv_cdc_min_resolved_ts_no_change_for_1m`変更フィードがないときにアラートが鳴り続ける問題を修正[#11017](https://github.com/tikv/tikv/issues/11017)
        -   Kafka メッセージの書き込み中にエラーが発生すると、TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性があるという問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   新しい変更フィード[#2389](https://github.com/pingcap/tiflow/issues/2389)を作成するときのメモリリークの問題を修正します。
        -   シンク コンポーネントが解決済みの ts を早期に進めることにより、データの不整合が発生する可能性がある問題を修正します[#3503](https://github.com/pingcap/tiflow/issues/3503)
        -   株式データのスキャンに時間がかかりすぎると、TiKV が GC を実行するために株式データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   changefeed update コマンドがグローバル コマンド ライン パラメーターを認識しない問題を修正します[#2803](https://github.com/pingcap/tiflow/issues/2803)
