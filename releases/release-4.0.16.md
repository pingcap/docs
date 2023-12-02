---
title: TiDB 4.0.16 Release Notes
---

# TiDB 4.0.16 リリースノート {#tidb-4-0-16-release-notes}

発売日：2021年12月17日

TiDB バージョン: 4.0.16

## 互換性の変更 {#compatibility-changes}

-   TiKV

    -   v4.0.16 より前では、TiDB が不正な UTF-8 文字列を実数型に変換すると、エラーが直接報告されます。 v4.0.16 以降、TiDB は文字列[#11466](https://github.com/tikv/tikv/issues/11466)内の正当な UTF-8 プレフィックスに従って変換を処理します。

-   ツール

    -   TiCDC

        -   TiCDC が Kafka クラスター[#2962](https://github.com/pingcap/tiflow/issues/2962)に大きすぎるメッセージを送信しないように、Kafka シンク`max-message-bytes`のデフォルト値を 1 MB に変更します。
        -   TiCDC が Kafka パーティション間でメッセージをより均等に分散できるように、Kafka Sink のデフォルト値`partition-num`を[#3337](https://github.com/pingcap/tiflow/issues/3337)に変更します。

## 改善点 {#improvements}

-   TiDB

    -   Grafana バージョンを 7.5.7 から 7.5.11 にアップグレードします。

-   TiKV

    -   バックアップと復元を使用してデータを復元するとき、または TiDB Lightning [#11469](https://github.com/tikv/tikv/issues/11469)のローカル バックエンドを使用してデータをインポートするときに、zstd アルゴリズムを採用して SST ファイルを圧縮することにより、ディスク容量の消費をTiDB Lightning。

-   ツール

    -   バックアップと復元 (BR)

        -   復元の堅牢性の向上[#27421](https://github.com/pingcap/tidb/issues/27421)

    -   TiCDC

        -   頻繁な etcd 書き込みが PD サービスに影響を与えるのを防ぐために、EtcdWorker にティック頻度制限を追加します[#3112](https://github.com/pingcap/tiflow/issues/3112)
        -   TiKV リロードのレート制限制御を最適化し、チェンジフィードの初期化中の gPRC の輻輳を軽減します[#3110](https://github.com/pingcap/tiflow/issues/3110)

## バグの修正 {#bug-fixes}

-   TiDB

    -   コスト見積もり[#23625](https://github.com/pingcap/tidb/issues/23625)ために範囲をポイントに変換するときに、統計モジュールのオーバーフローによって引き起こされるpanicを修正しました。
    -   制御関数（ `IF`や`CASE WHEN`など）の関数として`ENUM`種類のデータを使用した場合の誤った結果を修正[#23114](https://github.com/pingcap/tidb/issues/23114)
    -   `tidb_enable_vectorized_expression` ( `on`または`off` ) [#29434](https://github.com/pingcap/tidb/issues/29434)の値が異なるために`GREATEST`関数が一貫性のない結果を返す問題を修正します。
    -   場合によってはプレフィックスインデックスにインデックス結合を適用するときのpanicを修正しました[#24547](https://github.com/pingcap/tidb/issues/24547)
    -   場合によってはプランナーが`join`の無効なプランをキャッシュする可能性がある問題を修正します[#28087](https://github.com/pingcap/tidb/issues/28087)
    -   `sql_mode` [#11648](https://github.com/pingcap/tidb/issues/11648)空の場合、TiDB が null 以外の列に`null`を挿入できないバグを修正
    -   `GREATEST`と`LEAST`関数の間違った結果の型を修正[#29019](https://github.com/pingcap/tidb/issues/29019)
    -   グローバル レベルの権限を付与および取り消すための`grant`および`revoke`操作を実行するときの`privilege check fail`エラーを修正します[#29675](https://github.com/pingcap/tidb/issues/29675)
    -   `ENUM`データ型[#29357](https://github.com/pingcap/tidb/issues/29357)で`CASE WHEN`関数を使用するときのpanicを修正しました。
    -   ベクトル化された式[#29244](https://github.com/pingcap/tidb/issues/29244)の関数`microsecond`の誤った結果を修正します。
    -   ベクトル化された式[#28643](https://github.com/pingcap/tidb/issues/28643)の関数`hour`の誤った結果を修正しました。
    -   楽観的トランザクションの競合によってトランザクションが互いにブロックされる可能性がある問題を修正します[#11148](https://github.com/tikv/tikv/issues/11148)
    -   `auto analyze`結果[#29188](https://github.com/pingcap/tidb/issues/29188)のログ情報が不完全である問題を修正
    -   `SQL_MODE`が &#39;NO_ZERO_IN_DATE&#39; [#26766](https://github.com/pingcap/tidb/issues/26766)の場合、無効なデフォルト日付を使用してもエラーが報告されない問題を修正します。
    -   Grafana の[コプロセッサーキャッシュ] パネルにメトリクスが表示されない問題を修正します。これで、Grafana は`hits` / `miss` / `evict` [#26338](https://github.com/pingcap/tidb/issues/26338)の数字を表示します
    -   同じパーティションを同時に切り詰めると DDL ステートメントがスタックする問題を修正します[#26229](https://github.com/pingcap/tidb/issues/26229)
    -   `Decimal`を`String` [#29417](https://github.com/pingcap/tidb/issues/29417)に変換する際に長さ情報が間違っている問題を修正
    -   `NATURAL JOIN`を使用して複数のテーブルを結合する場合、クエリ結果に余分な列が表示される問題を修正します[#29481](https://github.com/pingcap/tidb/issues/29481)
    -   `IndexScan`プレフィックス インデックス[#29711](https://github.com/pingcap/tidb/issues/29711)を使用する場合、 `TopN`が誤って`indexPlan`にプッシュダウンされる問題を修正します。
    -   `DOUBLE`タイプの自動インクリメント列でトランザクションを再試行するとデータ破損が発生する問題を修正します[#29892](https://github.com/pingcap/tidb/issues/29892)

-   TiKV

    -   極端な条件でリージョンのマージ、ConfChange、およびスナップショットが同時に発生したときに発生するpanicの問題を修正します[#11475](https://github.com/tikv/tikv/issues/11475)
    -   10 進数の除算結果が 0 の場合の負号の問題を修正します[#29586](https://github.com/pingcap/tidb/issues/29586)
    -   TiKV メトリクス[#11299](https://github.com/tikv/tikv/issues/11299)でインスタンスごとの gRPC リクエストの平均レイテンシーが不正確である問題を修正します。
    -   ダウンストリーム データベースが見つからない場合に発生する TiCDCpanicの問題を修正します[#11123](https://github.com/tikv/tikv/issues/11123)
    -   チャンネルがいっぱいの場合、 Raft接続が切断される問題を修正[#11047](https://github.com/tikv/tikv/issues/11047)
    -   TiDB が`Max` / `Min`関数の`Int64`型が符号付き整数であるかどうかを正しく識別できず、 `Max` / `Min`という間違った計算結果が発生する問題を修正[#10158](https://github.com/tikv/tikv/issues/10158)
    -   輻輳エラー[#11082](https://github.com/tikv/tikv/issues/11082)が原因で CDC がスキャンの再試行を頻繁に追加する問題を修正します。

-   PD

    -   TiKV ノードが削除された後に発生するpanicの問題を修正します[#4344](https://github.com/tikv/pd/issues/4344)
    -   リージョン同期器[#3936](https://github.com/tikv/pd/issues/3936)のスタックによって引き起こされるリーダー選出の遅さを修正
    -   エビクト リーダー スケジューラが異常なピアのあるリージョンをスケジュールできることのサポート[#4093](https://github.com/tikv/pd/issues/4093)

-   TiFlash

    -   ライブラリ`nsl`がないため、一部のプラットフォームでTiFlash が起動できない問題を修正

-   ツール

    -   TiDBBinlog

        -   1 GBを超えるトランザクションを転送するとDrainerが終了するバグを修正[#28659](https://github.com/pingcap/tidb/issues/28659)

    -   TiCDC

        -   チェンジフィードチェックポイントラグ[#3010](https://github.com/pingcap/tiflow/issues/3010)の負の値エラーを修正
        -   コンテナ環境での OOM の修正[#1798](https://github.com/pingcap/tiflow/issues/1798)
        -   複数の TiKV がクラッシュしたとき、または強制再起動中に TiCDC レプリケーションが中断される問題を修正します[#3288](https://github.com/pingcap/tiflow/issues/3288)
        -   DDL 処理後のメモリリーク問題を修正[#3174](https://github.com/pingcap/tiflow/issues/3174)
        -   ErrGCTTLExceeded エラーが発生したときに変更フィードが十分な速度で失敗しない問題を修正します[#3111](https://github.com/pingcap/tiflow/issues/3111)
        -   上流の TiDB インスタンスが予期せず終了すると、TiCDC レプリケーション タスクが終了する可能性がある問題を修正します[#3061](https://github.com/pingcap/tiflow/issues/3061)
        -   TiKV が同じリージョン[#2386](https://github.com/pingcap/tiflow/issues/2386)に重複したリクエストを送信すると、TiCDC プロセスがパニックになる可能panicがある問題を修正
        -   TiCDC によって生成される Kafka メッセージの量が`max-message-size` [#2962](https://github.com/pingcap/tiflow/issues/2962)の制限を受けない問題を修正
        -   変更フィード[#11017](https://github.com/tikv/tikv/issues/11017)がないときに`tikv_cdc_min_resolved_ts_no_change_for_1m`がアラートを出し続ける問題を修正します。
        -   Kafka メッセージの書き込み中にエラーが発生したときに TiCDC 同期タスクが一時停止することがある問題を修正します[#2978](https://github.com/pingcap/tiflow/issues/2978)
        -   `force-replicate`が有効な場合、有効なインデックスのない一部のパーティション テーブルが無視される可能性がある問題を修正します[#2834](https://github.com/pingcap/tiflow/issues/2834)
        -   新しいチェンジフィード作成時のメモリリーク問題を修正[#2389](https://github.com/pingcap/tiflow/issues/2389)
        -   シンク コンポーネントが早期に解決されるためにデータの不整合が発生する可能性がある問題を修正します[#3503](https://github.com/pingcap/tiflow/issues/3503)
        -   ストック データのスキャンに時間がかかりすぎる場合、TiKV が GC を実行するためにストック データのスキャンが失敗する可能性がある問題を修正します[#2470](https://github.com/pingcap/tiflow/issues/2470)
        -   Changefeed update コマンドがグローバル コマンド ライン パラメータ[#2803](https://github.com/pingcap/tiflow/issues/2803)を認識しない問題を修正します。
